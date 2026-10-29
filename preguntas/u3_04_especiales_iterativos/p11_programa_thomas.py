"""Pregunta 11 — PROGRAMAR el algoritmo de Thomas  ·  id: prog_thomas

El alumno escribe su propia función; aquí no hay respuesta que teclear.

Casos: tres sistemas tridiagonales de tamaños **3, 4 y 5**, sembrados por NC.

Convención (la del documento): ``e[i]`` multiplica a ``x_{i-1}`` y ``g[i]`` a
``x_{i+1}``; ``e[0]`` y ``g[n-1]`` valen 0 y no se usan.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_thomas'
TITULO = 'Programa: algoritmo de Thomas'
SAL = 0xAE          # semilla propia de esta pregunta

FUNCION = 'mi_thomas'
FIRMA = 'mi_thomas(e, f, g, r)'
SALIDA = 'matriz'
REFERENCIA = 'thomas'   # verificable por tools/build_grader.py


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: el sistema 3x3 del documento, solución [1, 1, 1].
    e_ej = [0, -1, -1]
    f_ej = [2, 2, 2]
    g_ej = [-1, -1, 0]
    r_ej = [1, 0, 1]

    casos = []
    for n in (3, 4, 5):
        e, f, g, r = ref.sistema_tridiagonal(rng, n)
        casos.append(((e, f, g, r), ref.thomas(e, f, g, r)))

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'enunciado': (
            'Escribe la función `mi_thomas(e, f, g, r)` que resuelva el '
            'sistema tridiagonal y devuelva $\\mathbf{x}$ como columna.\n\n'
            'Los cuatro vectores tienen longitud $n$; $e_1$ y $g_n$ valen 0 '
            '(esas posiciones no existen). Se probará con $n = 3, 4$ y $5$.'
        ),
        'ayuda': 'Tres fases: modificar $f$ y $r$ hacia adelante, despejar '
                 '$x_n$, y subir con $x_k = (r_k - g_k x_{k+1})/f_k$. Ojo: en '
                 'la primera fila $f_1$ y $r_1$ NO se modifican.',
        'ejemplo': ((e_ej, f_ej, g_ej, r_ej),
                    ref.thomas(e_ej, f_ej, g_ej, r_ej)),
        'casos': casos,
        'datos': {'n_casos': [len(c[0][1]) for c in casos]},
    }
