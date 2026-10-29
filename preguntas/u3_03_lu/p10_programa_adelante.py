"""Pregunta 10 — PROGRAMAR la sustitución hacia adelante  ·  id: prog_adelante

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Casos: tres sistemas triangulares inferiores de tamaños **2, 3 y 4**. Uno de
ellos no tiene la diagonal en unos, para que no se pueda suponer ``l_ii = 1``.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_adelante'
TITULO = 'Programa: sustitución hacia adelante'
SAL = 0x2E          # semilla propia de esta pregunta

FUNCION = 'mi_sustitucion_adelante'
FIRMA = 'mi_sustitucion_adelante(L, b)'
SALIDA = 'matriz'
REFERENCIA = 'sustitucion_adelante'   # verificable por tools/build_grader.py


def _triangular_inferior(rng, n):
    """L invertible triangular inferior y un b con solución entera."""
    L = sp.zeros(n, n)
    for i in range(n):
        L[i, i] = rng.choice([-3, -2, -1, 1, 2, 3])
        for j in range(i):
            L[i, j] = rng.randint(-3, 3)
    y = [sp.Integer(rng.randint(-3, 3)) for _ in range(n)]
    return L, L * sp.Matrix(y)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: la L del cuaderno y su b.
    L_ej = sp.Matrix([[1, 0, 0], [sp.Rational(-3, 2), 1, 0], [-1, 4, 1]])
    b_ej = sp.Matrix([8, -11, -3])

    casos = []
    for n in (2, 3, 4):
        L, b = _triangular_inferior(rng, n)
        casos.append(((L, b), ref.sustitucion_adelante(L, b)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_sustitucion_adelante(L, b)` que resuelva '
            '$\\mathbf{L}\\mathbf{y} = \\mathbf{b}$ y devuelva $\\mathbf{y}$ '
            'como columna.\n\n'
            'Se probará con tres matrices de tamaños distintos. **No supongas '
            'que la diagonal de L son unos:** una de ellas no los tiene.'
        ),
        'ayuda': 'Es la sustitución hacia atrás leída al revés: empieza por el '
                 'primer renglón y la suma va sobre las columnas a la '
                 'IZQUIERDA de la diagonal, con las y ya conocidas.',
        'ejemplo': ((L_ej, b_ej), ref.sustitucion_adelante(L_ej, b_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
