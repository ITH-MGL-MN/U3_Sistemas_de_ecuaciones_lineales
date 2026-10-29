"""Pregunta 6 — Armar la matriz tridiagonal  ·  id: esp_tridiagonal

Qué evalúa: la convención de los tres vectores. El error típico no es de
cálculo, es de colocación: poner ``e`` o ``g`` en la diagonal equivocada.

Se dan ``e``, ``f`` y ``g`` como listas de longitud n con ``e[0] = 0`` y
``g[n-1] = 0`` (las posiciones que no existen), igual que en ``solvers_u3``.
"""
import random

import sympy as sp

from mn_motor.comun import tex

ID = 'esp_tridiagonal'
TITULO = 'Arma la matriz tridiagonal'
SAL = 0x5C          # semilla propia de esta pregunta


def _vectores(rng, n):
    e = [0] + [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(n - 1)]
    g = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(n - 1)] + [0]
    f = [rng.choice([-5, -4, -3, 3, 4, 5]) for _ in range(n)]
    return e, f, g


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    n = 4
    e, f, g = _vectores(rng, n)

    A = sp.zeros(n, n)
    for i in range(n):
        A[i, i] = f[i]
        if i > 0:
            A[i, i - 1] = e[i]
        if i < n - 1:
            A[i, i + 1] = g[i]

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Un sistema tridiagonal de $4\\times4$ se guarda en tres vectores '
            '(las posiciones que no existen valen 0):\n\n'
            f'$$e = {tex([e])}$$\n\n'
            f'$$f = {tex([f])}$$\n\n'
            f'$$g = {tex([g])}$$\n\n'
            '**Escribe la matriz $\\mathbf{A}$ completa** ($4\\times4$), con '
            'los ceros donde corresponden.'
        ),
        'esperado': A.tolist(),
        'ayuda': '$f$ es la diagonal principal, $e$ la de abajo (cada $e_i$ '
                 'va en la fila $i$, columna $i-1$) y $g$ la de arriba '
                 '(cada $g_i$ va en la fila $i$, columna $i+1$).',
        'datos': {'e': e, 'f': f, 'g': g},
    }
