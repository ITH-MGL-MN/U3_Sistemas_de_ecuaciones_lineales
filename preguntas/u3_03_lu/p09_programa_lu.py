"""Pregunta 9 — PROGRAMAR la factorización  ·  id: prog_lu

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Casos: tres matrices de tamaños **2, 3 y 4**, sembradas por NC. Son ocultos: no
se muestran, solo se dice si pasaron.

La respuesta son DOS matrices (L y U), así que se comparan por separado.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_lu'
TITULO = 'Programa: factorización LU'
SAL = 0x4D          # semilla propia de esta pregunta

FUNCION = 'mi_lu'
FIRMA = 'mi_lu(A)'
SALIDA = 'varias'
REFERENCIA = 'lu_doolittle'   # verificable por tools/build_grader.py


def _sistema(rng, n):
    return ref.sistema_eliminable(rng, n)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: la matriz del cuaderno, siempre la misma.
    A_ej = sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])

    casos = []
    for n in (2, 3, 4):
        A, _ = _sistema(rng, n)
        casos.append(((A,), ref.lu_doolittle(A)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_lu(A)` que factorice $\\mathbf{A}$ como '
            '$\\mathbf{L}\\mathbf{U}$ (Doolittle) y devuelva **las dos '
            'matrices**: `return L, U`.\n\n'
            'Se probará con **tres matrices de tamaños distintos**, no solo '
            'con la de 3×3 del cuaderno.'
        ),
        'ayuda': 'Es la misma eliminación del cuaderno, pero en vez de restar '
                 'sobre [A|b] se resta sobre A y se guarda cada multiplicador '
                 'en la L que empieza como identidad.',
        'ejemplo': ((A_ej,), ref.lu_doolittle(A_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
