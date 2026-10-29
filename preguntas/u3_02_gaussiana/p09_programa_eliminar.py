"""Pregunta 9 — PROGRAMAR la eliminación hacia adelante  ·  id: prog_eliminar

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Casos: tres sistemas de tamaños **2, 3 y 4**, sembrados por NC. El de 3 es el
del cuaderno; los otros dos existen para que una implementación clavada a
3×3 no pase. Son ocultos: no se muestran, solo se dice si pasaron.

El ejemplo visible (3×3) es el que usa `practica()`, para que el alumno pueda
comprobarse antes de enviar.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_eliminar'
TITULO = 'Programa: eliminación hacia adelante'
SAL = 0xF7          # semilla propia de esta pregunta

FUNCION = 'mi_gauss_eliminar'
FIRMA = 'mi_gauss_eliminar(A, b)'
SALIDA = 'matriz'
REFERENCIA = 'gauss_eliminar'   # verificable por tools/build_grader.py


def _sistema(rng, n):
    """Sistema n x n resoluble por eliminación sin pivoteo (ver solvers_u3)."""
    return ref.sistema_eliminable(rng, n)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: el sistema 3x3 del cuaderno, siempre el mismo.
    A_ej = sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    b_ej = sp.Matrix([8, -11, -3])

    casos = []
    for n in (2, 3, 4):
        A, b = _sistema(rng, n)
        esperado = ref.gauss_eliminar(A, b)
        # Red de seguridad: el caso debe ser resoluble sin pivoteo.
        casos.append(((A, b), esperado))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_gauss_eliminar(A, b)` que devuelva la '
            '**matriz aumentada ya triangularizada** (sin pivoteo).\n\n'
            'Se probará con **tres sistemas de tamaños distintos**, no solo '
            'el de 3×3 del cuaderno: tiene que servir para cualquier $n$.'
        ),
        'ayuda': 'Devuelve una matriz de n renglones y n+1 columnas. '
                 'Usa M.sym[[A, b]] para armarla y no toques los argumentos.',
        'ejemplo': ((A_ej, b_ej), ref.gauss_eliminar(A_ej, b_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
