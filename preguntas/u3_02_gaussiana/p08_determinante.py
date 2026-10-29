"""Pregunta 8 — Determinante por los pivotes  ·  id: gau_determinante

Qué evalúa: que se use el producto de los pivotes para obtener el determinante,
en vez de expandir por cofactores.
"""
import random

from mn_motor.comun import tex

ID = 'gau_determinante'
TITULO = 'Determinante por los pivotes'
SAL = 0xE6          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Matriz 3x3 con determinante distinto de cero y pivotes cómodos.
    while True:
        A = [[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]
        if A[0][0] == 0:
            continue
        det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
               - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
               + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
        if det != 0:
            break

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Para la matriz\n\n$${tex(A)}$$\n\n'
            '**¿cuánto vale su determinante?** '
            '(Sugerencia: triangulariza y multiplica los pivotes de la diagonal.)'
        ),
        'esperado': det,
        'ayuda': 'Con eliminación sin intercambios, det = producto de la diagonal '
                 'de la matriz triangular.',
        'datos': {'A': A},
    }
