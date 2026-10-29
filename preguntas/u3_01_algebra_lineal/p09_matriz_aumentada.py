"""Pregunta 9 — Matriz aumentada  ·  id: mat_aumentada

Qué evalúa: que el alumno sepa apilar el vector b como última columna de A.

Datos sembrados: un sistema 3x3 con solución entera, para que la aumentada
tenga números chicos y con sentido.
"""
import random

from mn_motor.comun import tex, tex_vector

ID = 'mat_aumentada'
TITULO = 'Matriz aumentada'
SAL = 0x91          # semilla propia de esta pregunta (ver comun.semilla_pregunta)


def _matriz_no_singular(rng):
    """A 3x3 con determinante distinto de cero, para que el sistema tenga solución única."""
    while True:
        A = [[rng.randint(-4, 4) for _ in range(3)] for _ in range(3)]
        det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
               - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
               + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
        if det != 0:
            return A


def construir(semilla):
    rng = random.Random(semilla ^ SAL)
    A = _matriz_no_singular(rng)
    x = [rng.randint(-3, 3) for _ in range(3)]
    b = [sum(A[i][j] * x[j] for j in range(3)) for i in range(3)]

    aumentada = [A[i] + [b[i]] for i in range(3)]

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Dado el sistema con\n\n'
            f'$$\\mathbf{{A}} = {tex(A)}$$\n\n'
            f'$$\\mathbf{{b}} = {tex_vector(b)}$$\n\n'
            '**escribe la matriz aumentada** $[\\mathbf{A}\\mid\\mathbf{b}]$.'
        ),
        'esperado': aumentada,
        'ayuda': 'Se apila b como última columna. '
                 'Escribe [[a,b,c],[d,e,f],[g,h,i]].',
        # Se guardan para poder auditar o depurar sin recalcular nada.
        'datos': {'A': A, 'b': b, 'x': x},
    }
