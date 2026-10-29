"""Pregunta 10 — Operación de renglón  ·  id: mat_renglon

Qué evalúa: que el alumno aplique una operación elemental
``R2 <- R2 - m*R1`` sobre una matriz 3x3.

HISTORIA (importante): esta pregunta tuvo un error de signo. La clave
calculaba ``R2 - m*R1`` mientras el enunciado, con su propia convención,
mostraba lo contrario para m = -1 y m = 1. Como m se sortea entre seis
valores, un tercio de los alumnos contestaba correctamente lo que la pantalla
pedía y salía mal calificado.

Por eso ahora hay UNA sola función, ``_signo_y_factor``, que decide el signo y
lo usan tanto el cálculo como el texto. Y ``_revisar_coherencia`` comprueba en
cada tarea que el texto, leído como lo lee el alumno, reproduce la respuesta
esperada. Si algún día vuelven a divergir, truena al generar la tarea en vez
de calificar mal.
"""
import random
import re

from mn_motor.comun import tex

ID = 'mat_renglon'
TITULO = 'Operación de renglón'
SAL = 0xA2          # semilla propia de esta pregunta (ver comun.semilla_pregunta)


def _signo_y_factor(m):
    """Descompone ``R2 - m*R1`` en ``R2 + signo*factor*R1``.

    ÚNICA fuente de verdad de la operación: la usan el cálculo de la matriz
    esperada y el texto del enunciado, así no pueden contradecirse.
    """
    return (-1, abs(m)) if m > 0 else (1, abs(m))


def _texto_operacion(m):
    """LaTeX de la operación, tal como la lee el alumno en pantalla."""
    signo, factor = _signo_y_factor(m)
    op = '-' if signo < 0 else '+'
    if factor == 1:
        return rf'R_2 \leftarrow R_2 {op} R_1'
    return rf'R_2 \leftarrow R_2 {op} {factor}R_1'


def _aplicar(A, m):
    """Matriz resultante de ``R2 <- R2 - m*R1``."""
    signo, factor = _signo_y_factor(m)
    resultado = [fila[:] for fila in A]
    resultado[1] = [A[1][j] + signo * factor * A[0][j] for j in range(3)]
    return resultado


def _revisar_coherencia(A):
    """El texto mostrado tiene que reproducir la respuesta esperada.

    Relee el texto (no el generador), le saca el signo y el factor que verá el
    alumno, aplica la operación y lo compara con la clave, para los seis
    valores posibles de m. Es la red que impide repetir el error del historial.
    """
    for m in (-3, -2, -1, 1, 2, 3):
        texto = _texto_operacion(m)
        leido = re.search(r'R_2\s*([+-])\s*(\d*)R_1', texto.split('leftarrow')[-1])
        if leido is None:
            raise AssertionError(f'El texto no tiene la forma esperada: {texto}')
        signo = 1 if leido.group(1) == '+' else -1
        factor = int(leido.group(2)) if leido.group(2) else 1

        lo_que_hace_el_alumno = [A[1][j] + signo * factor * A[0][j] for j in range(3)]
        if lo_que_hace_el_alumno != _aplicar(A, m)[1]:
            raise AssertionError(
                f'La operación mostrada ({texto}) no da lo que la clave espera '
                f'para m={m}: {lo_que_hace_el_alumno} vs {_aplicar(A, m)[1]}')


def construir(semilla):
    rng = random.Random(semilla ^ SAL)
    while True:
        A = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        if A[0][0] != 0:        # sin pivote nulo: la operación es legal
            break
    m = rng.choice([-3, -2, -1, 1, 2, 3])

    _revisar_coherencia(A)
    resultado = _aplicar(A, m)

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Parte de\n\n$${tex(A)}$$\n\n'
            f'Aplica la operación ${_texto_operacion(m)}$\n\n'
            'y **escribe la matriz resultante**.'
        ),
        'esperado': resultado,
        'ayuda': 'Solo cambia el renglón 2; el 1 y el 3 quedan igual.',
        'datos': {'A': A, 'm': m},
    }
