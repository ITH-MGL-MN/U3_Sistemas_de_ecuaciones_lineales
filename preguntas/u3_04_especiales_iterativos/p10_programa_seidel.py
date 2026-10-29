"""Pregunta 10 — PROGRAMAR una barrida de Gauss-Seidel  ·  id: prog_seidel

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Se pide UNA barrida, no el método completo: la respuesta es exacta y no depende
del criterio de paro.

El vector inicial de cada caso no es cero para que no se pueda ignorar el
argumento ``x``.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_seidel'
TITULO = 'Programa: una barrida de Gauss-Seidel'
SAL = 0x63          # semilla propia de esta pregunta

FUNCION = 'mi_gauss_seidel_paso'
FIRMA = 'mi_gauss_seidel_paso(A, b, x)'
SALIDA = 'matriz'
REFERENCIA = 'gauss_seidel_paso'   # verificable por tools/build_grader.py


def _arranque(rng, n):
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
        casos.append(((A, b, x0), ref.gauss_seidel_paso(A, b, x0)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_gauss_seidel_paso(A, b, x)` que haga '
            '**una sola barrida** de Gauss-Seidel y devuelva el vector como '
            'columna.\n\n'
            'Se probará con tres sistemas de tamaños distintos y con vectores '
            'iniciales que **no** son cero.'
        ),
        'ayuda': 'Aquí NO se guarda el vector viejo: en cuanto calculas x[i] lo '
                 'usas para el renglón siguiente. Sobrescribe la misma lista.',
        'ejemplo': ((A_ej, b_ej, x_ej),
                    ref.gauss_seidel_paso(A_ej, b_ej, x_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
