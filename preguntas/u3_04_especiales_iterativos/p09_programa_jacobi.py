"""Pregunta 9 — PROGRAMAR una barrida de Jacobi  ·  id: prog_jacobi

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Se pide UNA barrida, no el método completo: así la respuesta es exacta, no
depende del criterio de paro y se puede comparar sin tolerancias.

El vector inicial de cada caso **no es cero** a propósito: si alguien ignorara
el argumento ``x`` y arrancara de ceros, pasaría el ejemplo y fallaría los casos.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_jacobi'
TITULO = 'Programa: una barrida de Jacobi'
SAL = 0x1F          # semilla propia de esta pregunta

FUNCION = 'mi_jacobi_paso'
FIRMA = 'mi_jacobi_paso(A, b, x)'
SALIDA = 'matriz'
REFERENCIA = 'jacobi_paso'   # verificable por tools/build_grader.py


def _arranque(rng, n):
    """Vector inicial con valores distintos de cero (que no sea el vector nulo)."""
    while True:
        x = [rng.choice([-2, -1, 1, 2]) for _ in range(n)]
        if any(v != 0 for v in x):
            return x


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    A_ej = sp.Matrix([[4, 1, -1], [2, 7, 1], [1, -3, 12]])
    b_ej = sp.Matrix([3, 19, 31])
    x_ej = [0, 0, 0]

    casos = []
    for n in (2, 3, 4):
        A, b = ref.sistema_dominante(rng, n)
        x0 = _arranque(rng, n)
        casos.append(((A, b, x0), ref.jacobi_paso(A, b, x0)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_jacobi_paso(A, b, x)` que haga **una sola '
            'barrida** de Jacobi y devuelva el vector nuevo como columna.\n\n'
            'Se probará con tres sistemas de tamaños distintos y con vectores '
            'iniciales que **no** son cero.'
        ),
        'ayuda': 'Todo se calcula con el vector VIEJO: guarda los valores '
                 'nuevos en otra lista y devuélvela al final. Usa x[j] para '
                 'todos los j, también los que ya calculaste.',
        'ejemplo': ((A_ej, b_ej, x_ej), ref.jacobi_paso(A_ej, b_ej, x_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
