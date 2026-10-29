"""Pregunta 8 — La primera incógnita intermedia  ·  id: lu_y2

Qué evalúa: la sustitución hacia adelante sobre L y = b, que es el paso que
LU agrega antes de la sustitución hacia atrás. Se pide solo una componente
para que la respuesta sea un entero corto y se pueda escribir a mano.

Se sortea ``y`` entero, ``L`` unitaria inferior entera y se arma ``b = L y``:
así la sustitución devuelve exactamente ``y``.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref
from mn_motor.comun import tex

ID = 'lu_y2'
TITULO = 'El vector intermedio'
SAL = 0x91          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    L = sp.eye(3)
    for i in range(3):
        for j in range(i):
            L[i, j] = rng.choice([-2, -1, 1, 2])

    # Se sortea y hasta que el lado derecho no tenga un cero en la posición 2:
    # así y2 nunca es "0 por casualidad" y la pregunta siempre tiene sentido.
    for _ in range(50):
        y = [sp.Integer(rng.randint(-4, 4)) for _ in range(3)]
        b = L * sp.Matrix(y)
        if b[1] != 0:
            break
    else:
        raise RuntimeError('no encontré un lado derecho utilizable')

    y_ref = ref.sustitucion_adelante(L, b)
    esperado = int(y_ref[1][0])

    if esperado != int(y[1]):
        raise AssertionError('la sustitución no recuperó la y de diseño')

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'En la solución por LU, el primer paso es resolver '
            '$\\mathbf{L}\\mathbf{y} = \\mathbf{b}$ con\n\n'
            f'$$\\mathbf{{L}} = {tex(L.tolist())}, \\qquad '
            f'\\mathbf{{b}} = {tex([[int(v)] for v in b])}$$\n\n'
            '**¿cuánto vale $y_2$?**'
        ),
        'esperado': esperado,
        'ayuda': 'De arriba hacia abajo: $y_1$ sale del primer renglón y luego '
                 '$y_2 = (b_2 - l_{21}y_1)/l_{22}$. Ojo: la diagonal de L son '
                 'unos.',
        'datos': {'L': L.tolist(), 'b': [int(v) for v in b], 'y': [int(v) for v in y]},
    }
