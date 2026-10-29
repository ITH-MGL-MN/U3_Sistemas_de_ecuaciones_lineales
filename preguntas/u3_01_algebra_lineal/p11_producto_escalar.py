"""Pregunta 11 — Producto por escalar  ·  id: num_escalar

Qué evalúa: que el alumno sepa leer una posición concreta (renglón, columna)
de una matriz multiplicada por un escalar, sin multiplicar toda la matriz.

Nota: usa su PROPIA matriz, distinta de la de la pregunta 9. Cada pregunta se
siembra por separado a propósito, así una no delata la respuesta de la otra.
"""
import random

from mn_motor.comun import tex

ID = 'num_escalar'
TITULO = 'Producto por escalar'
SAL = 0xB3          # semilla propia de esta pregunta (ver comun.semilla_pregunta)

FILA = 2            # renglón que se pregunta
COLUMNA = 3         # columna que se pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)
    A = [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
    escalar = rng.randint(2, 9)

    # El elemento (2,3) es índice [1][2] en Python (base 0).
    esperado = escalar * A[FILA - 1][COLUMNA - 1]

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Con\n\n$${tex(A)}$$\n\n'
            f'¿cuánto vale el elemento de la **posición ({FILA},{COLUMNA})** de '
            f'${escalar}\\,\\mathbf{{A}}$?'
        ),
        'esperado': esperado,
        'ayuda': f'Multiplica cada entrada; la posición ({FILA},{COLUMNA}) es '
                 f'renglón {FILA}, columna {COLUMNA}.',
        'datos': {'A': A, 'escalar': escalar},
    }
