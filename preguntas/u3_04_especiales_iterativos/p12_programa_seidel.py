"""Pregunta 12 — PROGRAMAR Gauss-Seidel completo  ·  id: prog_seidel

Igual que la 11 pero con Gauss-Seidel: misma convención declarada, mismos
requisitos (reordenar, criterio de paro, devolver (x, iteraciones)).

La diferencia está en el cuerpo del método: aquí se reutiliza al instante cada
valor recién calculado.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_seidel'
TITULO = 'Programa: Gauss-Seidel completo'
SAL = 0x63          # semilla propia de esta pregunta

FUNCION = 'mi_gauss_seidel'
FIRMA = 'mi_gauss_seidel(A, b, tol=1e-6, max_iter=100)'
SALIDA = 'matriz_iteraciones'
REFERENCIA = 'gauss_seidel'
TOL = 1e-6
MAX_ITER = 100
TOL_CALIFICACION = 1e-4


def _caso(rng, n):
    A, b = ref.sistema_permutado(rng, n)
    x, _ = ref.gauss_seidel(A, b, TOL, MAX_ITER)
    return ((A.tolist(), [int(sp.N(v)) for v in b], TOL, MAX_ITER),
            [[v] for v in x])


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    A_ej = sp.Matrix([[4, 1, -1], [2, 7, 1], [1, -3, 12]])
    b_ej = sp.Matrix([3, 19, 31])
    x_ej, _ = ref.gauss_seidel(A_ej, b_ej, TOL, MAX_ITER)

    casos = [_caso(rng, n) for n in (2, 3, 4)]

    for (A, b, _, _), esperado in casos:
        sol = ref.solucion_exacta(A, b)
        if max(abs(esperado[i][0] - sol[i]) for i in range(len(sol))) > TOL_CALIFICACION:
            raise AssertionError('la referencia no converge en un caso oculto')

    return {
        'tipo': 'funcion',
        'id': ID,
        'titulo': TITULO,
        'funcion': FUNCION,
        'firma': FIRMA,
        'salida': SALIDA,
        'referencia': REFERENCIA,
        'tol': TOL_CALIFICACION,
        'max_iter': MAX_ITER,
        'enunciado': (
            'Escribe `mi_gauss_seidel(A, b, tol=1e-6, max_iter=100)` que '
            'resuelva el sistema y devuelva **`(x, iteraciones)`**.\n\n'
            '**Dentro de la función**, en este orden:\n'
            '1. reordena las ecuaciones para que la diagonal sea dominante;\n'
            '2. itera con Gauss-Seidel (cada valor se usa en cuanto sale);\n'
            '3. se detiene cuando '
            '$\\|\\mathbf{x}^{(k+1)}-\\mathbf{x}^{(k)}\\|_\\infty / '
            '\\|\\mathbf{x}^{(k+1)}\\|_\\infty < \\text{tol}$, '
            'o al llegar a `max_iter`.\n\n'
            'Se probará con tres sistemas cuyas **filas vienen desordenadas**.'
        ),
        'ayuda': 'Trabaja con float, no con M.sym. Aquí basta UNA lista: '
                 'sobrescribe x[i] y el renglón siguiente ya ve el valor nuevo. '
                 'Para el error, guarda una copia antes de la barrida.',
        'ejemplo': ((A_ej.tolist(), [int(sp.N(v)) for v in b_ej], TOL, MAX_ITER),
                    [[v] for v in x_ej]),
        'casos': casos,
        'datos': {'n_casos': [len(c[0][0]) for c in casos]},
    }
