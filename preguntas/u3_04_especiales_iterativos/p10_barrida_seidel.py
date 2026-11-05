"""Pregunta 10 — Una barrida de Gauss-Seidel A MANO  ·  id: iter_barrida_seidel

Qué evalúa: la diferencia real entre Jacobi y Gauss-Seidel, calculando a mano
una sola barrida. Aquí sí se reutiliza lo recién calculado.

Se usa la MISMA construcción que la pregunta 9 (diagonal 2, 4, 8 y arranque
entero) para que las respuestas sean decimales exactos.
"""
import random

import sympy as sp

from mn_motor.comun import tex

ID = 'iter_barrida_seidel'
TITULO = 'Una barrida de Gauss-Seidel a mano'
SAL = 0x6E          # semilla propia de esta pregunta

DIAGONAL = (2, 4, 8)


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    n = 3
    # Se sortea hasta que las dos barridas DEN DISTINTO: si coinciden, la
    # pregunta no enseña la diferencia entre Jacobi y Gauss-Seidel.
    for _ in range(200):
        A = sp.zeros(n, n)
        for i in range(n):
            A[i, i] = DIAGONAL[i]
            for j in range(n):
                if j != i:
                    A[i, j] = rng.randint(-3, 3)
        b = sp.Matrix([rng.randint(-8, 8) for _ in range(n)])
        viejo = [rng.choice([-2, -1, 1, 2]) for _ in range(n)]

        # Gauss-Seidel: se sobrescribe al vuelo y el renglón siguiente ve lo nuevo.
        x = [sp.Integer(v) for v in viejo]
        x0 = list(x)
        for i in range(n):
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x[i] = sp.nsimplify((sp.N(b[i]) - suma) / sp.N(A[i, i]))

        # Jacobi con el mismo arranque, para comparar.
        jac = []
        for i in range(n):
            suma = sum(A[i, j] * x0[j] for j in range(n) if j != i)
            jac.append(sp.nsimplify((sp.N(b[i]) - suma) / sp.N(A[i, i])))

        if jac == x:
            continue
        if any(int(sp.denom(sp.Rational(v))) & (int(sp.denom(sp.Rational(v))) - 1)
               for v in x):
            continue
        break
    else:
        raise RuntimeError('no encontré datos donde las dos barridas difieran')

    esperado = [[float(v)] for v in x]

    b_col = [[int(sp.N(v))] for v in b]

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Mismo sistema y mismo arranque:\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}, \\qquad '
            f'\\mathbf{{b}} = {tex(b_col)}, \\qquad '
            f'\\mathbf{{x}}^{{(0)}} = {tex([viejo])}$$\n\n'
            '**Escribe $\\mathbf{x}^{(1)}$ después de UNA barrida de '
            'Gauss-Seidel.**'
        ),
        'esperado': esperado,
        'ayuda': 'Ve en orden: calcula $x_1$ con el vector viejo, y para $x_2$ '
                 'usa YA el $x_1$ nuevo. Para $x_3$, usa el $x_1$ y el $x_2$ '
                 'nuevos. Escríbelo como [[a],[b],[c]].',
        'datos': {'A': A.tolist(), 'b': [int(sp.N(v)) for v in b],
                  'x0': viejo, 'x1': [str(v) for v in x],
                  'jacobi': [str(v) for v in jac]},
    }
