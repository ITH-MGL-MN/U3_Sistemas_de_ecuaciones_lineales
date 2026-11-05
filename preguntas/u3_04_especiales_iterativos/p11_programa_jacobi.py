"""Pregunta 11 — PROGRAMAR Jacobi completo  ·  id: prog_jacobi

Qué evalúa: el método completo, con reordenamiento de filas para lograr la
dominancia y criterio de paro. La convención va DECLARADA en el enunciado y en
la llamada con la que se califica (tol = 1e-6, max_iter = 100).

Los casos ocultos usan ``sistema_permutado``: sistemas cuya solución es entera
pero cuyas filas están desordenadas. Sin reordenar, la iteración explota
(error de 10^70 o división entre cero); reordenando, converge en menos de 30
iteraciones. Así el caso de verdad evalúa el reordenamiento.

Se califica en float (no con M.sym): es el método iterativo, no un método exacto.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref

ID = 'prog_jacobi'
TITULO = 'Programa: Jacobi completo'
SAL = 0x1F          # semilla propia de esta pregunta

FUNCION = 'mi_jacobi'
FIRMA = 'mi_jacobi(A, b, tol=1e-6, max_iter=100)'
SALIDA = 'matriz_iteraciones'
REFERENCIA = 'jacobi'
TOL = 1e-6
MAX_ITER = 100
TOL_CALIFICACION = 1e-4     # margen para el error propio del criterio de paro


def _caso(rng, n):
    A, b = ref.sistema_permutado(rng, n)
    x, _ = ref.jacobi(A, b, TOL, MAX_ITER)
    return ((A.tolist(), [int(sp.N(v)) for v in b], TOL, MAX_ITER),
            [[v] for v in x])


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Ejemplo visible: el sistema del cuaderno, con sus filas en orden.
    A_ej = sp.Matrix([[4, 1, -1], [2, 7, 1], [1, -3, 12]])
    b_ej = sp.Matrix([3, 19, 31])
    x_ej, _ = ref.jacobi(A_ej, b_ej, TOL, MAX_ITER)

    casos = [_caso(rng, n) for n in (2, 3, 4)]

    # Red de seguridad: la referencia tiene que llegar a la solución exacta en
    # todos los casos; si no, el caso oculto no se puede calificar.
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
            'Escribe `mi_jacobi(A, b, tol=1e-6, max_iter=100)` que resuelva '
            'el sistema y devuelva **`(x, iteraciones)`**.\n\n'
            '**Dentro de la función**, en este orden:\n'
            '1. reordena las ecuaciones para que la diagonal sea dominante;\n'
            '2. itera con Jacobi;\n'
            '3. se detiene cuando '
            '$\\|\\mathbf{x}^{(k+1)}-\\mathbf{x}^{(k)}\\|_\\infty / '
            '\\|\\mathbf{x}^{(k+1)}\\|_\\infty < \\text{tol}$, '
            'o al llegar a `max_iter`.\n\n'
            'Se probará con tres sistemas cuyas **filas vienen desordenadas**: '
            'si no reordenas, la iteración se dispara.'
        ),
        'ayuda': 'Trabaja con float, no con M.sym. Reordenar: para cada '
                 'columna k elige, entre las ecuaciones que quedan, la del '
                 'mayor |a_ik|. En Jacobi guarda los valores nuevos en OTRA '
                 'lista y usa sólo el vector viejo.',
        'ejemplo': ((A_ej.tolist(), [int(sp.N(v)) for v in b_ej], TOL, MAX_ITER),
                    [[v] for v in x_ej]),
        'casos': casos,
        'datos': {'n_casos': [len(c[0][0]) for c in casos]},
    }
