"""Pregunta 11 — PROGRAMAR el método completo  ·  id: prog_solve

Junta las dos funciones anteriores: resolver A x = b de principio a fin.

Casos: sistemas de tamaños **2, 3 y 4**, sembrados por NC. Esta pregunta premia
que las dos anteriores estén bien, así que conviene dejarla para el final.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_solve'
TITULO = 'Programa: resolver A x = b'
SAL = 0x29          # semilla propia de esta pregunta

FUNCION = 'mi_gauss_solve'
FIRMA = 'mi_gauss_solve(A, b)'
SALIDA = 'matriz'
REFERENCIA = 'gauss_solve'   # verificable por tools/build_grader.py


def _sistema(rng, n):
    return ref.sistema_eliminable(rng, n)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    A_ej = sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    b_ej = sp.Matrix([8, -11, -3])

    casos = []
    for n in (2, 3, 4):
        A, b = _sistema(rng, n)
        casos.append(((A, b), ref.gauss_solve(A, b)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_gauss_solve(A, b)` que resuelva '
            '$\\mathbf{A}\\mathbf{x} = \\mathbf{b}$ y devuelva $\\mathbf{x}$ '
            'como columna.\n\n'
            'Se probará con tres sistemas de tamaños distintos.'
        ),
        'ayuda': 'Es unir tus dos funciones: triangular y luego despejar. '
                 'No hace falta volver a escribir la eliminación.',
        'ejemplo': ((A_ej, b_ej), ref.gauss_solve(A_ej, b_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
