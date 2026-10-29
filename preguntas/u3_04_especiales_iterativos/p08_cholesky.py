"""Pregunta 8 — La última entrada de L en Cholesky  ·  id: esp_cholesky

Qué evalúa: la recursión de Cholesky, en particular la raíz de la diagonal,

    l_kk = sqrt(a_kk - suma de los l_kj^2 ya calculados).

Se construye ``A = L L^T`` con ``L`` triangular inferior **entera**, así que la
factorización devuelve exactamente esa ``L`` y ``l_33`` es un entero.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref
from mn_motor.comun import tex

ID = 'esp_cholesky'
TITULO = 'La diagonal de Cholesky'
SAL = 0xB3          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    n = 3
    L = sp.zeros(n, n)
    for i in range(n):
        L[i, i] = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        for j in range(i):
            L[i, j] = rng.randint(-4, 4)
    A = L * L.T

    L_ref = ref.cholesky(A)
    if sp.Matrix(L_ref) * sp.Matrix(L_ref).T != A:
        raise AssertionError('Cholesky no reconstruyó A')

    esperado = int(sp.nsimplify(L_ref[2][2]))

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Para la matriz simétrica definida positiva\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}$$\n\n'
            '**¿cuánto vale $l_{33}$**, la última entrada de la diagonal de '
            'la factorización $\\mathbf{A} = \\mathbf{L}\\mathbf{L}^{T}$?'
        ),
        'esperado': esperado,
        'ayuda': '$l_{33} = \\sqrt{a_{33} - l_{31}^2 - l_{32}^2}$. Primero '
                 'salen la diagonal $l_{11}$ y la columna 1, luego $l_{22}$ y '
                 'la columna 2, y al final $l_{33}$.',
        'datos': {'A': A.tolist(), 'L': L_ref},
    }
