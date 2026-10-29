"""Pregunta 10 — PROGRAMAR la sustitución hacia atrás  ·  id: prog_sustitucion

La entrada es una matriz aumentada YA triangular, así que esta pregunta se
puede resolver aunque la anterior no esté lista.

Casos: triangularizadas de sistemas de tamaños **2, 3 y 4**, sembrados por NC.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_sustitucion'
TITULO = 'Programa: sustitución hacia atrás'
SAL = 0x18          # semilla propia de esta pregunta

FUNCION = 'mi_sustitucion_atras'
FIRMA = 'mi_sustitucion_atras(Ab)'
SALIDA = 'matriz'
REFERENCIA = 'sustitucion_atras'   # verificable por tools/build_grader.py


def _triangular(rng, n):
    """Una matriz aumentada triangular con solución entera."""
    A, b = ref.sistema_eliminable(rng, n)
    return sp.Matrix(ref.gauss_eliminar(A, b))


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: la triangular del sistema 3x3 del cuaderno.
    Ab_ej = sp.Matrix(ref.gauss_eliminar(
        sp.Matrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]),
        sp.Matrix([8, -11, -3])))

    casos = []
    for n in (2, 3, 4):
        Ab = _triangular(rng, n)
        casos.append(((Ab,), ref.sustitucion_atras(Ab)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_sustitucion_atras(Ab)` que reciba una '
            'matriz aumentada **ya triangular** y devuelva el vector '
            '$\\mathbf{x}$ como columna.\n\n'
            'Se probará con tres matrices de tamaños distintos.'
        ),
        'ayuda': 'Recorre las filas de abajo hacia arriba. La suma va sobre las '
                 'columnas a la derecha de la diagonal, que son las ya conocidas.',
        'ejemplo': ((Ab_ej,), ref.sustitucion_atras(Ab_ej)),
        'casos': casos,
        'datos': {'n_casos': [c[0][0].rows for c in casos]},
    }
