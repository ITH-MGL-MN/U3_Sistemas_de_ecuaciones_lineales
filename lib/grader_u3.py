"""grader_u3 — motor de calificación de la Unidad 3 (Álgebra Lineal).

Mismo contrato que el motor de U2_T3B: el cuaderno solo ve los nombres que este
archivo declara en ``__all__``. El cuaderno se identifica con el correo
institucional, y de ahí sale el Número de Control (NC) que siembra los datos:
cada alumno recibe matrices distintas, así que copiar no sirve.

Flujo típico en el cuaderno::

    MI_TAREA = generar_tarea(alumno_id, nombre)   # una sola vez
    pregunta(1)                                   # muestra la pregunta 1
    ...
    puntos, maximo = calificar()                  # sin enviar
    enviar(alumno_id)                             # envía (máx. 2 intentos)

Este archivo NO debe distribuirse al alumno en texto claro: se empaqueta en
``grader_ofuscado.txt`` con ``tools/build_grader.py``.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import json
import os
import random
import re
import zlib
from string import ascii_lowercase

try:
    import yaml
except ImportError:  # el cuaderno instala lo que falte
    yaml = None

__all__ = [
    'consultar_calificacion',
    'calificar',
    'enviar',
    'extraer_nc',
    'generar_tarea',
    'pregunta',
    'semilla_de',
    'ultimo_envio',
    'ver_preguntas',
    'MAX_INTENTOS',
]

MAX_INTENTOS = 2
_TAREA_ID = 'U3_01_Algebra_Lineal'

# ---------------------------------------------------------------------
# Rutas. El motor vive en lib/, así que la raíz del repo es su padre — pero
# cuando el cuaderno carga el blob con exec() NO existe __file__, así que hay
# que deducir la raíz de otra forma.
# ---------------------------------------------------------------------

def _detectar_raiz():
    """Carpeta del repo, en el orden en que conviene creerle a cada pista."""
    # 1) El cuaderno la inyecta antes de exec() (modo blob): la más confiable.
    pista = globals().get('_REPO_U3')
    if pista and os.path.isdir(pista):
        return os.path.abspath(pista)
    # 2) Importado como módulo de lib/.
    archivo = globals().get('__file__')
    if archivo:
        return os.path.dirname(os.path.dirname(os.path.abspath(archivo)))
    # 3) Subir desde la carpeta actual hasta topar con config/.
    base = os.getcwd()
    for _ in range(6):
        if os.path.exists(os.path.join(base, 'config', 'config.yaml')):
            return base
        padre = os.path.dirname(base)
        if padre == base:
            break
        base = padre
    return os.getcwd()


_RAIZ = _detectar_raiz()

# Lo llena tools/build_grader.py al final del archivo empaquetado. En modo
# módulos vale None y el banco se lee del YAML.
_BANCO_EMPAQUETADO = None


def _leer_cfg():
    """Lee config/config.yaml (si existe) para URL y token del backend."""
    ruta = os.path.join(_RAIZ, 'config', 'config.yaml')
    datos = {}
    if os.path.exists(ruta) and yaml is not None:
        try:
            with open(ruta, encoding='utf-8') as f:
                datos = yaml.safe_load(f) or {}
        except Exception:
            datos = {}
    ev = (datos.get('evaluacion') or {})
    return {
        'url': os.environ.get('U3_APPS_URL') or ev.get('apps_script_url', '') or '',
        'token': os.environ.get('U3_TOKEN') or ev.get('webhook_token', '') or '',
        # OJO: NO se toma de config.yaml. `tarea` viaja al backend y define la
        # pestaña donde se guarda, así que tiene que ser el id del cuaderno que
        # está enviando; si lo tomáramos de config.yaml, el Cuaderno 01
        # escribiría en la pestaña del Cuaderno 02.
        'tarea': _TAREA_ID,
    }


_CFG = _leer_cfg()


def _leer_banco():
    """Lee el banco de opción múltiple.

    Si el motor viene empaquetado (blob), el banco va DENTRO del blob y no hace
    falta el YAML: en un clon limpio del repositorio el archivo del banco no
    existe (solo lo tiene el profesor), y sin esto la tarea saldría con 3
    preguntas en vez de 11.
    """
    if _BANCO_EMPAQUETADO is not None:
        return _BANCO_EMPAQUETADO
    ruta = os.path.join(_RAIZ, 'config', 'preguntas_u3.yaml')
    if not os.path.exists(ruta) or yaml is None:
        return {}
    with open(ruta, encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


# =====================================================================
# Identificación
# =====================================================================

def extraer_nc(identificador) -> str | None:
    """Extrae el Número de Control de un correo institucional.

    Formatos aceptados::

        'm16330887@hermosillo.tecnm.mx' -> '16330887'
        '16330887@hermosillo.tecnm.mx'  -> '16330887'
        'm{16330887}@tecnm.mx'          -> '16330887'
    """
    if identificador is None:
        return None
    s = str(identificador).strip()
    entre_llaves = re.search(r'\{([^}]+)\}', s)
    if entre_llaves:
        return entre_llaves.group(1).strip()
    local = s.split('@')[0]
    digitos = re.search(r'\d{4,}', local)
    return digitos.group(0) if digitos else None


def semilla_de(identificador) -> int:
    """Semilla determinista a partir del NC (mismo alumno -> mismos datos)."""
    nc = extraer_nc(identificador) or str(identificador)
    h = hashlib.sha256(nc.encode('utf-8')).hexdigest()
    return int(h[:8], 16)


# =====================================================================
# Datos sembrados por alumno
# =====================================================================

def _matriz_aumentada(rng):
    """Genera un sistema 3x3 con solución entera y devuelve (A, b, aumentada)."""
    while True:
        A = [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        # descartar matrices singulares
        det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
               - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
               + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
        if det == 0:
            continue
        x = [rng.randint(-3, 3) for _ in range(3)]
        b = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]
        aumentada = [A[i] + [b[i]] for i in range(3)]
        return A, b, aumentada


def _signo_y_factor(m):
    """Descompone ``R2 <- R2 - m*R1`` en ``R2 <- R2 + signo*factor*R1``.

    Es la ÚNICA fuente de verdad de la operación: la usan tanto el cálculo de
    la matriz esperada como el texto que se muestra. Antes cada uno tenía su
    propia convención de signo y, con m = ±1, la pantalla pedía una cosa y la
    clave esperaba otra.
    """
    return (-1, abs(m)) if m > 0 else (1, abs(m))


def _operacion_renglon(rng):
    """Genera una matriz 3x3 y la operación R2 <- R2 - m*R1 con m entero."""
    while True:
        A = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        if A[0][0] == 0:
            continue
        m = rng.choice([-3, -2, -1, 1, 2, 3])
        signo, factor = _signo_y_factor(m)
        resultado = [fila[:] for fila in A]
        resultado[1] = [A[1][j] + signo * factor * A[0][j] for j in range(3)]
        return A, m, resultado


def _datos_alumno(alumno_id):
    """Todos los datos sembrados que usan las preguntas."""
    rng = random.Random(semilla_de(alumno_id))
    A1, b1, aum = _matriz_aumentada(rng)
    A2, m2, res2 = _operacion_renglon(rng)
    escalar = rng.randint(2, 9)
    return {
        'A1': A1, 'b1': b1, 'aumentada': aum,
        'A2': A2, 'm2': m2, 'res2': res2,
        'escalar': escalar,
    }


# =====================================================================
# Generación de la tarea
# =====================================================================

def _tex(M):
    """Matriz -> LaTeX de un bmatrix, SIN los delimitadores ``$``.

    Los `$` los pone quien llama, porque a veces va en línea (`$...$`) y a
    veces en su propio renglón (`$$...$$`).
    """
    filas = r' \\ '.join(' & '.join(f'{v:g}' if isinstance(v, (int, float)) else str(v)
                                    for v in fila) for fila in M)
    return r'\begin{bmatrix}' + filas + r'\end{bmatrix}'


def _op_renglon_tex(m):
    """Texto LaTeX de ``R2 <- R2 + signo*factor*R1``, sin dobles signos.

    Deriva el signo del mismo ``_signo_y_factor`` que calcula la matriz
    esperada, así que lo que se lee y lo que se califica no pueden diferir.
    """
    signo, factor = _signo_y_factor(m)
    op = '-' if signo < 0 else '+'
    if factor == 1:
        return rf'R_2 \leftarrow R_2 {op} R_1'
    return rf'R_2 \leftarrow R_2 {op} {factor}R_1'


def _revisar_coherencia(datos):
    """Comprueba que lo que se MUESTRA reproduce lo que se ESPERA.

    Recorre los seis valores posibles de ``m``, toma el texto tal como lo lee
    el alumno, le extrae el signo y el factor, y aplica la operación a la
    matriz. El resultado tiene que dar lo mismo que la clave. Si el texto y el
    cálculo vuelven a divergir, salta aquí en vez de costarle puntos a un
    grupo entero.
    """
    base = datos['A2']
    for m in (-3, -2, -1, 1, 2, 3):
        tex = _op_renglon_tex(m)
        # se relee el texto, no el generador: eso es lo que ve el alumno
        cuerpo = tex.split('leftarrow')[-1]
        leido_txt = re.search(r'R_2\s*([+-])\s*(\d*)R_1', cuerpo)
        if leido_txt is None:
            raise AssertionError(f'El texto de la operación no tiene la forma esperada: {tex}')
        signo = -1 if leido_txt.group(1) == '-' else 1
        factor = int(leido_txt.group(2)) if leido_txt.group(2) else 1

        leido = [base[1][j] + signo * factor * base[0][j] for j in range(3)]
        s, f = _signo_y_factor(m)
        esperado = [base[1][j] + s * f * base[0][j] for j in range(3)]
        if leido != esperado:
            raise AssertionError(
                f'La operación mostrada ({tex}) no reproduce la respuesta '
                f'esperada para m={m}: {leido} vs {esperado}')
    return True


def generar_tarea(alumno_id, nombre=''):
    """Construye la tarea del alumno: preguntas, datos sembrados y widgets.

    Devuelve un diccionario que el cuaderno guarda en ``MI_TAREA``. Llamarla
    dos veces con el mismo correo da exactamente lo mismo.
    """
    if alumno_id is None:
        raise RuntimeError('Necesito tu correo institucional para generar la tarea.')

    banco = _leer_banco()
    datos = _datos_alumno(alumno_id)
    nc = extraer_nc(alumno_id)
    _revisar_coherencia(datos)

    preguntas = []

    # ---- Opción múltiple (del YAML, barajadas) ----
    rng = random.Random(semilla_de(alumno_id) ^ 0x5F5F)
    for bloque in ('ALG_INICIO',):
        for item in banco.get(bloque, []):
            # El YAML escribe las opciones como "a) ...", "b) ...", pero al
            # barajarlas esas letras quedarían fuera de orden, así que se
            # quitan aquí: el alumno ve las opciones sin letra.
            opciones = [re.sub(r'^[a-zA-Z]\s*\)\s*', '', o) for o in item['opciones']]
            buena = opciones[item['correcta']]
            rng.shuffle(opciones)
            preguntas.append({
                'tipo': 'mcq',
                'id': item['id'],
                'titulo': item.get('titulo', ''),
                'enunciado': item['pregunta'],
                'opciones': opciones,
                'esperado': opciones.index(buena),
            })

    # ---- Matriz: escribir la aumentada ----
    preguntas.append({
        'tipo': 'matriz',
        'id': 'mat_aumentada',
        'titulo': 'Matriz aumentada',
        'enunciado': (
            'Dado el sistema con\n\n'
            f'$$\\mathbf{{A}} = {_tex(datos["A1"])}$$\n\n'
            f'$$\\mathbf{{b}} = {_tex([[v] for v in datos["b1"]])}$$\n\n'
            '**escribe la matriz aumentada** $[\\mathbf{A}\\mid\\mathbf{b}]$.'
        ),
        'esperado': datos['aumentada'],
        'ayuda': 'Se apila b como última columna. Escribe [[a,b,c],[d,e,f],[g,h,i]].',
    })

    # ---- Matriz: operación de renglón ----
    preguntas.append({
        'tipo': 'matriz',
        'id': 'mat_renglon',
        'titulo': 'Operación de renglón',
        'enunciado': (
            f'Parte de\n\n$${_tex(datos["A2"])}$$\n\n'
            f'Aplica la operación ${_op_renglon_tex(datos["m2"])}$\n\n'
            'y **escribe la matriz resultante**.'
        ),
        'esperado': datos['res2'],
        'ayuda': 'Solo cambia el renglón 2; el 1 y el 3 quedan igual.',
    })

    # ---- Número: elemento de una matriz escalada ----
    preguntas.append({
        'tipo': 'numero',
        'id': 'num_escalar',
        'titulo': 'Producto por escalar',
        'enunciado': (
            f'Con\n\n$${_tex(datos["A1"])}$$\n\n'
            f'¿cuánto vale el elemento de la **posición (2,3)** de '
            f'${datos["escalar"]}\\,\\mathbf{{A}}$?'
        ),
        'esperado': datos['escalar'] * datos['A1'][1][2],
        'ayuda': 'Multiplica cada entrada; la posición (2,3) es renglón 2, columna 3.',
    })

    return _activar({
        'alumno_id': alumno_id,
        'nombre': nombre,
        'nc': nc,
        'tarea': _CFG['tarea'],
        'semilla': semilla_de(alumno_id),
        'preguntas': preguntas,
        'datos': datos,
        'respuestas': [None] * len(preguntas),   # lo llenan los widgets
        'widgets': [None] * len(preguntas),
        'terminada': False,
    })


# =====================================================================
# Mostrar preguntas
# =====================================================================

def _widgets():
    import ipywidgets as w
    return w


def _letras(n):
    """a, b, c, d, ... para marcar las opciones."""
    return ascii_lowercase[:n]


def pregunta(n, tarea=None):
    """Muestra la pregunta ``n`` (1..N) con su widget de respuesta.

    El enunciado y las opciones van como Markdown (así MathJax pinta el
    LaTeX); el widget solo sirve para ELEGIR. Por eso las opciones del
    selector son nada más ``a``, ``b``, ``c``…: si se pusieran los textos
    dentro del widget, saldrían sin formatear.
    """
    t = tarea if tarea is not None else _TAREA_ACTIVA()
    if not 1 <= n <= len(t['preguntas']):
        raise ValueError(f'La pregunta {n} no existe (hay {len(t["preguntas"])})')

    from IPython.display import Markdown, display
    import ipywidgets as w

    q = t['preguntas'][n - 1]
    encabezado = f"### Pregunta {n} — {q['titulo']}\n\n{q['enunciado']}"

    if q['tipo'] == 'mcq':
        letras = _letras(len(q['opciones']))
        cuerpo = '\n'.join(f'- **{l})** {o}' for l, o in zip(letras, q['opciones']))
        display(Markdown(f'{encabezado}\n\n{cuerpo}'))
        ctrl = w.RadioButtons(
            options=[(l, i) for i, l in enumerate(letras)],
            value=None,
            layout=w.Layout(width='100%'),
        )
        pregunta_letras = ' / '.join(letras)
        texto_boton = f'Elegir {pregunta_letras} y guardar'
    else:
        display(Markdown(encabezado))
        if q['tipo'] == 'matriz':
            ctrl = w.Text(placeholder='[[1,2,3],[4,5,6],[7,8,9]]',
                          layout=w.Layout(width='90%'))
        else:
            ctrl = w.Text(placeholder='escribe un número',
                          layout=w.Layout(width='40%'))
        texto_boton = 'Guardar respuesta'

    salida = w.Output()

    def _guardar(_=None):
        t['respuestas'][n - 1] = ctrl.value
        with salida:
            salida.clear_output()
            if ctrl.value is None or (isinstance(ctrl.value, str) and not ctrl.value.strip()):
                print(f'⚠️ La pregunta {n} sigue sin respuesta.')
                return
            if q['tipo'] == 'mcq':
                letra = _letras(len(q['opciones']))[int(ctrl.value)]
                print(f'Respuesta {n} guardada: opción {letra}.')
            else:
                print(f'Respuesta {n} guardada.')

    boton = w.Button(description=texto_boton, button_style='primary')
    boton.on_click(_guardar)
    t['widgets'][n - 1] = ctrl
    display(w.VBox([ctrl, boton, salida]))
    if q.get('ayuda'):
        display(Markdown(f"> 💡 {q['ayuda']}"))


def ver_preguntas(tarea=None):
    """Lista todas las preguntas con su estado (sin revelar la respuesta)."""
    t = tarea if tarea is not None else _TAREA_ACTIVA()
    for i, q in enumerate(t['preguntas'], 1):
        estado = '✅ contestada' if t['respuestas'][i - 1] is not None else '⬜ pendiente'
        print(f'{i:>2}. [{q["tipo"]:>6}] {q["titulo"]:<28} {estado}')


# =====================================================================
# Calificar
# =====================================================================

def _a_lista(texto):
    """Convierte el texto del alumno en lista de listas (seguro, sin eval)."""
    if texto is None:
        return None
    if isinstance(texto, (list, tuple)):
        return [list(f) if isinstance(f, (list, tuple)) else [f] for f in texto]
    s = str(texto).strip()
    if not s:
        return None
    try:
        v = ast.literal_eval(s)
    except Exception:
        return None
    if isinstance(v, (int, float)):
        return [[v]]
    if isinstance(v, (list, tuple)):
        if v and isinstance(v[0], (list, tuple)):
            return [list(f) for f in v]
        return [list(v)]
    return None


def _matriz_igual(respuesta, esperado, tol=1e-6):
    r = _a_lista(respuesta)
    if r is None:
        return False
    e = esperado
    if len(r) != len(e) or any(len(f) != len(e[i]) for i, f in enumerate(r)):
        return False
    for i, fila in enumerate(r):
        for j, v in enumerate(fila):
            try:
                if abs(float(v) - float(e[i][j])) > tol:
                    return False
            except (TypeError, ValueError):
                return False
    return True


def _contestar(q, respuesta):
    """¿La respuesta es correcta? Devuelve 1 o 0."""
    if respuesta is None:
        return 0
    if q['tipo'] == 'mcq':
        try:
            return 1 if int(respuesta) == int(q['esperado']) else 0
        except (TypeError, ValueError):
            return 0
    if q['tipo'] == 'matriz':
        return 1 if _matriz_igual(respuesta, q['esperado']) else 0
    # numero
    try:
        return 1 if abs(float(respuesta) - float(q['esperado'])) < 1e-6 else 0
    except (TypeError, ValueError):
        return 0


def calificar(tarea=None):
    """Califica sin enviar. Devuelve ``(puntos, maximo)``."""
    t = tarea if tarea is not None else _TAREA_ACTIVA()
    aciertos = [_contestar(q, t['respuestas'][i]) for i, q in enumerate(t['preguntas'])]
    t['ultimo_calculo'] = aciertos
    puntos, maximo = sum(aciertos), len(aciertos)
    print('Resultados:', ' '.join('✅' if a else '❌' for a in aciertos))
    print(f'Puntaje: {puntos} / {maximo}')
    pendientes = [i + 1 for i, r in enumerate(t['respuestas']) if r is None]
    if pendientes:
        print('⚠️ Sin contestar:', pendientes)
    return puntos, maximo


# =====================================================================
# Enviar al backend (Apps Script)
# =====================================================================

def _historial_path():
    return os.path.join(_RAIZ, 'config', '.envios.json')


def _leer_historial():
    ruta = _historial_path()
    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _guardar_historial(h):
    ruta = _historial_path()
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(h, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def _post(payload):
    import urllib.request
    req = urllib.request.Request(
        _CFG['url'],
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode('utf-8'))
    if resp.get('status') != 'ok':
        raise RuntimeError(resp.get('message', 'Error del backend'))
    return resp.get('data', {})


def consultar_calificacion(alumno_id=None):
    """Pregunta al backend cuántos intentos llevas (necesita URL y token)."""
    if alumno_id is None:
        alumno_id = _TAREA_ACTIVA()['alumno_id']
    if not _CFG['url'] or not _CFG['token']:
        print('ℹ️ Backend sin configurar: no hay nada que consultar.')
        return None
    nc = extraer_nc(alumno_id) or str(alumno_id)
    try:
        datos = _post({'accion': 'intento', 'token': _CFG['token'],
                       'NC': nc, 'tarea': _CFG['tarea']})
    except Exception as exc:
        print('⛔ No se pudo consultar:', exc)
        return None
    if not datos:
        print(f'NC {nc}: todavía no hay envíos registrados.')
        return datos
    intentos = datos.get('intento', 0)
    print(f"NC {nc}: {intentos} de {MAX_INTENTOS} intentos usados · "
          f"puntaje {datos.get('total', 0)}")
    print(f'   Intentos restantes: {max(0, MAX_INTENTOS - intentos)}')
    return datos


def enviar(alumno_id, tarea=None):
    """Envía la calificación. Respeta el máximo de intentos del backend."""
    t = tarea if tarea is not None else _TAREA_ACTIVA()
    nc = extraer_nc(alumno_id) or str(alumno_id)

    aciertos = t.get('ultimo_calculo')
    if aciertos is None:
        aciertos = [_contestar(q, t['respuestas'][i]) for i, q in enumerate(t['preguntas'])]
    puntos, maximo = sum(aciertos), len(aciertos)

    if not _CFG['url'] or not _CFG['token']:
        print('ℹ️ Backend sin configurar: la calificación NO se envió.')
        print('   El profesor debe llenar config/config.yaml con la URL y el token.')
        print(f'   Resultado local: {puntos} / {maximo}')
        return None

    payload = {
        'accion': 'guardar',
        'token': _CFG['token'],
        'NC': nc,
        'tarea': _CFG['tarea'],
        'respuestas': aciertos,
        'pesos': [1] * maximo,
        'maxPuntos': 1,
    }
    try:
        res = _post(payload)
    except Exception as exc:
        print('⛔ No se pudo enviar:', exc)
        return None

    h = _leer_historial()
    h[nc] = {'intento': res.get('intento'), 'total': res.get('total'),
             'puntos': puntos, 'maximo': maximo}
    _guardar_historial(h)

    print(f"✅ Enviado. Intento {res.get('intento')} · Total {res.get('total', 0):.1f}/100")
    print(f"   Respuestas: {aciertos}")
    intento = res.get('intento') or 0
    if intento >= MAX_INTENTOS:
        print(f'   ⚠️ Este fue tu último intento (máximo {MAX_INTENTOS}).')
    return res


def ultimo_envio(alumno_id):
    """Muestra lo último que quedó registrado para este NC."""
    nc = extraer_nc(alumno_id) or str(alumno_id)
    h = _leer_historial().get(nc)
    if not h:
        print('No hay envíos registrados en este equipo.')
        return None
    print(f"NC {nc}: intento {h['intento']} · {h['puntos']}/{h['maximo']} "
          f"({h['total']:.1f}/100)")
    return h


# =====================================================================
# Estado activo
# =====================================================================

_ACTIVA = {'tarea': None}


def _TAREA_ACTIVA():  # noqa: N802
    t = _ACTIVA['tarea']
    if t is None:
        raise RuntimeError(
            'Primero ejecuta la celda de identificación: MI_TAREA = generar_tarea(...)')
    return t


def _activar(t):
    """La llama el cuaderno después de generar MI_TAREA."""
    _ACTIVA['tarea'] = t
    return t
