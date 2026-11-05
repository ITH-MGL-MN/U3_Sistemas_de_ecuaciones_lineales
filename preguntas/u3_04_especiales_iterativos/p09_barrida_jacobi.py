"""Pregunta 9 — Una barrida de Jacobi A MANO  ·  id: iter_barrida_jacobi

Qué evalúa: aplicar el algoritmo de Jacobi UNA vez, con el vector viejo, y
escribir el vector resultante. Es el equivalente de las cuentas a mano de la
Unidad 2: primero se entiende el paso, después se programa el método completo.

Cómo se garantiza que la respuesta se escriba EXACTA: la diagonal son potencias
de 2 (2, 4 y 8) y los datos son enteros, así que una barrida desde x = 0 solo
produce fracciones diádicas: todas tienen expansión decimal finita.
"""
import random

import sympy as sp

from mn_motor.comun import tex

ID = 'iter_barrida_jacobi'
TITULO = 'Una barrida de Jacobi a mano'
SAL = 0x37          # semilla propia de esta pregunta

DIAGONAL = (2, 4, 8)    # potencias de 2: los resultados son decimales exactos


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    n = 3
    A = sp.zeros(n, n)
    for i in range(n):
        A[i, i] = DIAGONAL[i]
        for j in range(n):
            if j != i:
                A[i, j] = rng.randint(-3, 3)
    b = sp.Matrix([rng.randint(-8, 8) for _ in range(n)])

    # Arranque entero y DISTINTO de cero: si fuera el vector de ceros, la
    # primera barrida se reduciría a b_i/a_ii y no haría falta el algoritmo.
    viejo = [rng.choice([-2, -1, 1, 2]) for _ in range(n)]
    nuevo = []
    for i in range(n):
        suma = sum(A[i, j] * viejo[j] for j in range(n) if j != i)
        nuevo.append(sp.nsimplify((sp.N(b[i]) - suma) / sp.N(A[i, i])))

    esperado = [[float(v)] for v in nuevo]

    # Red de seguridad: sin decimales exactos la pregunta no se puede escribir.
    for v in nuevo:
        den = int(sp.denom(sp.Rational(v)))
        if den & (den - 1):
            raise AssertionError(f'{v} no tiene expansion decimal finita')

    b_col = [[int(sp.N(v))] for v in b]

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Con el sistema\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}, \\qquad '
            f'\\mathbf{{b}} = {tex(b_col)}$$\n\n'
            f'y el arranque $\\mathbf{{x}}^{{(0)}} = {tex([viejo])}$, '
            '**escribe $\\mathbf{x}^{(1)}$ después de UNA barrida de Jacobi**.\n\n'
            'En Jacobi todas las incógnitas nuevas se calculan con el vector '
            'viejo, no con las que ya salieron.'
        ),
        'esperado': esperado,
        'ayuda': '$x_i^{(1)} = \\left(b_i - \\sum_{j \\neq i} a_{ij}'
                 'x_j^{(0)}\\right)/a_{ii}$. Usa el vector viejo COMPLETO en '
                 'las tres cuentas. Escríbelo como [[a],[b],[c]].',
        'datos': {'A': A.tolist(), 'b': [int(sp.N(v)) for v in b],
                  'x0': viejo, 'x1': [str(v) for v in nuevo]},
    }
