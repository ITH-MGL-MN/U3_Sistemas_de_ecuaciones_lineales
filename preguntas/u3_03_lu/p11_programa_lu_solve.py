"""Pregunta 11 — PROGRAMAR el resolvedor LU completo  ·  id: prog_lu_solve

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Casos: tres sistemas de tamaños **2, 3 y 4**, sembrados por NC.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_lu_solve'
TITULO = 'Programa: resolver con LU'
SAL = 0x07          # semilla propia de esta pregunta

FUNCION = 'mi_lu_solve'
FIRMA = 'mi_lu_solve(L, U, b)'
SALIDA = 'matriz'
REFERENCIA = 'lu_solve'   # verificable por tools/build_grader.py


def _sistema(rng, n):
    return ref.sistema_eliminable(rng, n)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    A_ej = sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    b_ej = sp.Matrix([8, -11, -3])
    L_ej, U_ej = ref.lu_doolittle(A_ej)

    casos = []
    for n in (2, 3, 4):
        A, b = _sistema(rng, n)
        L, U = ref.lu_doolittle(A)
        # Los casos entregan L y U como MATRICES (no listas): así la función
        # del alumno puede usar L.rows, L[i, k] o el operador @ sin sorpresas.
        casos.append(((sp.Matrix(L), sp.Matrix(U), b),
                      ref.lu_solve(L, U, b)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_lu_solve(L, U, b)` que, con la '
            'factorización ya hecha, devuelva $\\mathbf{x}$ como columna.\n\n'
            'Se probará con tres sistemas de tamaños distintos.'
        ),
        'ayuda': 'Dos sustituciones seguidas: primero '
                 '$\\mathbf{L}\\mathbf{y}=\\mathbf{b}$ (hacia adelante) y luego '
                 '$\\mathbf{U}\\mathbf{x}=\\mathbf{y}$ (hacia atrás).',
        'ejemplo': ((sp.Matrix(L_ej), sp.Matrix(U_ej), b_ej),
                    ref.lu_solve(L_ej, U_ej, b_ej)),
        'casos': casos,
        'datos': {'n_casos': [len(c[0][0]) for c in casos]},
    }
