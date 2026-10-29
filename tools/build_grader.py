"""build_grader.py — empaqueta un cuaderno completo dentro de un blob ofuscado.

El alumno recibe UN archivo, ``grader_ofuscado.txt`` (base64 + zlib), con:

    - todo el framework ``lib/mn_motor/``
    - todas las preguntas de ``preguntas/<cuaderno>/`` (los .py y los .md)

No es cifrado: quien sepa descomprimirlo puede leerlo. Sirve para que las
respuestas no estén a la vista de un simple vistazo. El anti-copia de verdad
son los datos sembrados por Número de Control.

Uso::

    python tools/build_grader.py                          # Cuaderno 01
    python tools/build_grader.py --cuaderno u3_02_...     # otro cuaderno

Antes de escribir el blob comprueba, sobre el paquete REAL:
    1. que todo compile,
    2. que el paquete se cargue desde memoria (como lo hará el alumno),
    3. que genere las preguntas esperadas y que una tarea completa califique.
Si algo falla, no escribe nada.
"""
import argparse
import base64
import os
import sys
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MOTOR = os.path.join(RAIZ, 'lib', 'mn_motor')
PREGUNTAS = os.path.join(RAIZ, 'preguntas')

# Nombre de la pestaña del backend por cuaderno. El id viaja en el payload y
# define dónde se guarda la calificación.
# Un cuaderno = una carpeta de preguntas = un blob. El `tarea_id` es la pestaña
# del backend donde se guarda la calificación de ese cuaderno.
CUADERNOS = {
    'u3_01_algebra_lineal': {'tarea_id': 'U3_01_Algebra_Lineal'},
    'u3_02_gaussiana': {'tarea_id': 'U3_02_Eliminacion_Gaussiana'},
    'u3_03_lu': {'tarea_id': 'U3_03_Descomposicion_LU'},
    'u3_04_especiales_iterativos': {'tarea_id': 'U3_04_Especiales_Iterativos'},
}

_COLA = '''

# =====================================================================
# Cargador generado por tools/build_grader.py
# =====================================================================
_MODULOS_PY = {modulos!r}

_RECURSOS = {recursos!r}


def _instalar(modulos):
    # Crea los módulos en memoria, sin tocar el disco ni sys.path.
    import sys as _sys
    import types as _types

    raices = {{n.split('.')[0] for n in modulos}}
    for nombre in list(_sys.modules):
        if nombre.split('.')[0] in raices:
            del _sys.modules[nombre]

    # 1) Un módulo vacío por nombre y el atributo puesto en su padre: las
    #    importaciones entre ellos resuelven aunque todavía no hayan corrido.
    for nombre in modulos:
        partes = nombre.split('.')
        for i in range(1, len(partes) + 1):
            parcial = '.'.join(partes[:i])
            if parcial in _sys.modules:
                continue
            modulo = _types.ModuleType(parcial)
            modulo.__path__ = []
            _sys.modules[parcial] = modulo
            if i > 1:
                setattr(_sys.modules['.'.join(partes[:i - 1])], partes[i - 1], modulo)

    # 2) Ejecutarlos. No hay un orden fijo que sirva para todos (un paquete
    #    importa a sus hijos y un hijo importa a sus hermanos), así que se
    #    reintenta hasta que todos corran: el primero que falla por una
    #    importación pendiente espera a la siguiente vuelta.
    pendientes = dict(modulos)
    ultimo_error = None
    while pendientes:
        progreso = False
        for nombre in list(pendientes):
            modulo = _sys.modules[nombre]
            modulo.__file__ = '<blob>/' + nombre.replace('.', '/') + '.py'
            codigo = compile(pendientes[nombre], modulo.__file__, 'exec')
            try:
                exec(codigo, modulo.__dict__)
            except ImportError as exc:
                ultimo_error = exc
                continue
            del pendientes[nombre]
            progreso = True
        if not progreso:
            raise ImportError(
                'No pude cargar el blob: ' + repr(ultimo_error) +
                ' (faltan ' + ', '.join(sorted(pendientes)) + ')')


_instalar(_MODULOS_PY)

import mn_motor.ajustes as _ajustes
import mn_motor.recursos as _recursos

_ajustes.CUADERNO = {cuaderno!r}
_ajustes.TAREA_ID = {tarea_id!r}
_recursos.EMPAQUETADOS.update(_RECURSOS)

import mn_motor as _motor

__all__ = list(_motor.__all__)
globals().update({{nombre: getattr(_motor, nombre) for nombre in _motor.__all__}})
'''


def _leer_py(carpeta, prefijo):
    """Módulos de un paquete: {nombre_punteado: fuente}."""
    modulos = {}
    for raiz, subcarpetas, archivos in os.walk(carpeta):
        subcarpetas[:] = [d for d in subcarpetas if d != '__pycache__']
        for archivo in sorted(archivos):
            if not archivo.endswith('.py'):
                continue
            ruta = os.path.join(raiz, archivo)
            relativa = os.path.relpath(ruta, carpeta)
            partes = relativa.replace(os.sep, '/')[:-3].split('/')
            if partes[-1] == '__init__':
                partes = partes[:-1]
            nombre = '.'.join(([prefijo] + partes) if partes else [prefijo])
            with open(ruta, encoding='utf-8') as f:
                modulos[nombre] = f.read()
    return modulos


def _leer_recursos(carpeta, relativa):
    """Los .md del cuaderno: {ruta relativa al repo: texto}."""
    recursos = {}
    for raiz, subcarpetas, archivos in os.walk(carpeta):
        subcarpetas[:] = [d for d in subcarpetas if d != '__pycache__']
        for archivo in sorted(archivos):
            if not archivo.endswith('.md'):
                continue
            ruta = os.path.join(raiz, archivo)
            clave = os.path.relpath(ruta, RAIZ).replace(os.sep, '/')
            if not clave.startswith(relativa):
                raise AssertionError(f'ruta inesperada: {clave}')
            with open(ruta, encoding='utf-8') as f:
                recursos[clave] = f.read()
    return recursos


def _verificar(codigo, cuaderno, tarea_id):
    """Carga el blob en un namespace limpio y comprueba que funciona."""
    ns = {'__name__': 'blob_prueba', '__file__': '<blob>'}
    exec(compile(codigo, '<blob>', 'exec'), ns)

    for nombre in ns['__all__']:
        if nombre not in ns:
            raise AssertionError(f'__all__ menciona {nombre!r} pero no se exportó')
    if ns['cuaderno']() != cuaderno:
        raise AssertionError(f'el blob quedó apuntando a {ns["cuaderno"]()!r}')

    # Un alumno cualquiera: se generan sus preguntas y se contestan todas bien.
    tarea = ns['generar_tarea']('m16330887@hermosillo.tecnm.mx', 'Prueba')
    if not tarea['preguntas']:
        raise AssertionError('la tarea salió sin preguntas')
    if tarea['tarea'] != tarea_id:
        raise AssertionError(f'la tarea se envía como {tarea["tarea"]!r}')

    # Dos alumnos distintos tienen que recibir datos distintos.
    otra = ns['generar_tarea']('m99999999@hermosillo.tecnm.mx', 'Otro')
    if [q['esperado'] for q in tarea['preguntas']] == \
       [q['esperado'] for q in otra['preguntas']]:
        raise AssertionError('dos alumnos recibieron exactamente la misma tarea')

    tarea['respuestas'] = [q['esperado'] for q in tarea['preguntas']]
    puntos, maximo = ns['calificar'](tarea)
    if puntos != maximo:
        raise AssertionError(f'contestar todo bien dio {puntos}/{maximo}')

    return len(tarea['preguntas']), ns['cuaderno']()


def construir_blob(cuaderno, salida=None, verboso=True):
    """Empaqueta un cuaderno. Devuelve (ok, mensaje)."""
    carpeta = os.path.join(PREGUNTAS, cuaderno)
    if not os.path.isdir(carpeta):
        return False, f'no existe preguntas/{cuaderno}/'

    modulos = _leer_py(MOTOR, 'mn_motor')
    # El paquete raíz de preguntas también va (es solo su docstring).
    with open(os.path.join(PREGUNTAS, '__init__.py'), encoding='utf-8') as f:
        modulos['preguntas'] = f.read()
    modulos.update(_leer_py(carpeta, 'preguntas.' + cuaderno))
    recursos = _leer_recursos(carpeta, 'preguntas/' + cuaderno + '/')

    if 'preguntas.' + cuaderno not in modulos:
        return False, f'falta preguntas/{cuaderno}/__init__.py'

    tarea_id = CUADERNOS[cuaderno]['tarea_id']
    codigo = _COLA.format(
        modulos=modulos, recursos=recursos, cuaderno=cuaderno, tarea_id=tarea_id,
    )

    try:
        n_preguntas, _ = _verificar(codigo, cuaderno, tarea_id)
    except Exception as exc:
        return False, f'el paquete no funciona: {exc!r}'

    blob = base64.b64encode(zlib.compress(codigo.encode('utf-8'), 9)).decode('ascii')
    destino = salida or os.path.join(RAIZ, 'grader', cuaderno + '.txt')
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'w', encoding='utf-8', newline='\n') as f:
        f.write(blob)

    vuelta = zlib.decompress(base64.b64decode(blob)).decode('utf-8')
    if vuelta != codigo:
        return False, 'la descompresión no coincide'

    if verboso:
        print(f'{cuaderno}')
        print(f'  preguntas   : {n_preguntas}')
        print(f'  módulos     : {len(modulos)} · recursos: {len(recursos)}')
        print(f'  empaquetado : {len(codigo):,} → {len(blob):,} caracteres '
              f'({len(blob)/len(codigo):.2f}x)')
        print(f'  salida      : {destino}')
    return True, destino


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cuaderno', default=None, choices=sorted(CUADERNOS),
                    help='carpeta de preguntas a empaquetar (por omisión: todas las que existan)')
    ap.add_argument('--salida', default=None,
                    help='archivo de salida (por omisión: grader/<cuaderno>.txt)')
    args = ap.parse_args()

    if args.cuaderno:
        lista = [args.cuaderno]
    else:
        lista = [c for c in CUADERNOS
                 if os.path.isdir(os.path.join(PREGUNTAS, c))]
        if not lista:
            print('No hay ninguna carpeta de preguntas para empaquetar.', file=sys.stderr)
            return 1

    fallos = 0
    for cuaderno in lista:
        ok, msg = construir_blob(cuaderno, args.salida, verboso=True)
        if not ok:
            fallos += 1
            print(f'⛔ {cuaderno}: {msg}', file=sys.stderr)
        print()

    if fallos:
        return 1
    print(f'Verificado: {len(lista)} blob(s) se descomprimen, cargan en memoria y califican todo bien.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
