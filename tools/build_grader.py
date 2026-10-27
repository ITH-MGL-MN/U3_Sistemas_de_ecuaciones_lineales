"""build_grader.py — empaqueta el motor del grader en un blob ofuscado.

El alumno recibe ``grader_ofuscado.txt`` (base64 + zlib). No es cifrado —quien
sepa descomprimirlo puede leerlo— pero evita que las respuestas queden a la
vista de un simple vistazo, que es justo lo que se busca en una tarea.

El banco de preguntas (``config/preguntas_u3.yaml``) se INCRUSTA en el blob: en
un clon limpio del repositorio ese archivo no existe, y sin incrustarlo la tarea
saldría con 3 preguntas en vez de 11.

Uso::

    python tools/build_grader.py
"""
import base64
import os
import sys
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FUENTE = os.path.join(RAIZ, 'lib', 'grader_u3.py')
BANCO = os.path.join(RAIZ, 'config', 'preguntas_u3.yaml')
SALIDA = os.path.join(RAIZ, 'grader_ofuscado.txt')

_COLA = """

# =====================================================================
# Banco de preguntas incrustado por tools/build_grader.py
# =====================================================================
# Va al final a propósito: la definición de arriba vale None y esto la
# reemplaza, así que _leer_banco() ya no necesita el YAML en disco.
_BANCO_EMPAQUETADO = {banco!r}
"""


def main():
    if not os.path.exists(FUENTE):
        print(f'No encuentro {FUENTE}', file=sys.stderr)
        return 1
    if not os.path.exists(BANCO):
        print(f'No encuentro {BANCO} (es el banco de preguntas)', file=sys.stderr)
        return 1

    import yaml

    with open(FUENTE, encoding='utf-8') as f:
        codigo = f.read()
    with open(BANCO, encoding='utf-8') as f:
        banco = yaml.safe_load(f) or {}

    n_preguntas = sum(len(v) for v in banco.values() if isinstance(v, list))
    empaquetado = codigo + _COLA.format(banco=banco)

    # Verificar que compila antes de empaquetar
    try:
        compile(empaquetado, FUENTE, 'exec')
    except SyntaxError as exc:
        print(f'El motor tiene un error de sintaxis: {exc}', file=sys.stderr)
        return 1

    # Y que al ejecutarlo el banco quede incrustado de verdad
    prueba = {'_REPO_U3': RAIZ, '__name__': 'prueba_grader'}
    try:
        exec(empaquetado, prueba)
    except Exception as exc:
        print(f'El motor falla al ejecutarse: {exc!r}', file=sys.stderr)
        return 1
    if prueba.get('_BANCO_EMPAQUETADO') != banco:
        print('El banco no quedó incrustado', file=sys.stderr)
        return 1

    blob = base64.b64encode(zlib.compress(empaquetado.encode('utf-8'), 9)).decode('ascii')
    with open(SALIDA, 'w', encoding='utf-8', newline='\n') as f:
        f.write(blob)

    print(f'Motor       : {FUENTE} ({len(codigo):,} caracteres)')
    print(f'Banco       : {BANCO} ({n_preguntas} preguntas)')
    print(f'Empaquetado : {len(empaquetado):,} caracteres')
    print(f'Salida      : {SALIDA} ({len(blob):,} caracteres)')
    print(f'Ratio       : {len(blob)/len(empaquetado):.2f}x')

    vuelta = zlib.decompress(base64.b64decode(blob)).decode('utf-8')
    assert vuelta == empaquetado, 'la descompresion no coincide'
    print('Verificado: el blob se descomprime al codigo empaquetado.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
