"""Pregunta 12 — El número de condición  ·  id: lu_condicion

Qué evalúa: calcular Cond_inf(A) = ||A||_inf * ||A^-1||_inf a mano, que es
la única forma de entender qué mide. La sección 2.5 del documento 02 y la
sección 7 del cuaderno lo explican.

Cómo se garantiza que la respuesta sea ENTERA: la matriz se construye como
producto de matrices elementales enteras, así que det(A) = 1 y A^-1 tiene
entradas enteras. Las dos normas infinito son entonces enteros y el producto
también.
"""
import random

import sympy as sp

from mn_motor.comun import tex

ID = 'lu_condicion'
TITULO = 'El número de condición'
SAL = 0xC7          # semilla propia de esta pregunta


def _norma_inf(A):
    """Máximo de las sumas por renglón."""
    M = sp.Matrix(A)
    filas = [[sp.nsimplify(M[i, j]) for j in range(M.cols)]
             for i in range(M.rows)]
    return max(sum(abs(v) for v in fila) for fila in filas)


def _unimodular(rng):
    """Producto de matrices elementales: det = 1 y A^-1 entera."""
    A = sp.eye(2)
    for _ in range(rng.randint(2, 4)):
        k = rng.choice([-3, -2, -1, 1, 2, 3])
        E = (sp.Matrix([[1, k], [0, 1]]) if rng.random() < 0.5
             else sp.Matrix([[1, 0], [k, 1]]))
        A = A * E
    return A


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    # Se busca una matriz con entradas legibles y un condición interesante:
    # ni trivial (2) ni imposible de hacer a mano (millones).
    for _ in range(300):
        A = _unimodular(rng)
        if A.det() != 1:
            continue
        if any(abs(A[i, j]) > 30 for i in range(2) for j in range(2)):
            continue
        cond = _norma_inf(A) * _norma_inf(A.inv())
        if 5 <= cond <= 2000:
            break
    else:
        raise RuntimeError('no encontré una matriz con condición utilizable')

    nA = int(_norma_inf(A))
    nAi = int(_norma_inf(A.inv()))
    esperado = int(cond)

    # Red de seguridad: la inversa tiene que ser entera y el producto cuadrar.
    inv = A.inv()
    if not all(v.is_Integer for v in inv):
        raise AssertionError('la inversa no salió entera')
    if nA * nAi != esperado:
        raise AssertionError('el número de condición no cuadra')

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Para la matriz\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}$$\n\n'
            '**¿cuánto vale $\\text{Cond}_\\infty(\\mathbf{A}) = '
            '\\|\\mathbf{A}\\|_\\infty \\cdot '
            '\\|\\mathbf{A}^{-1}\\|_\\infty$?**'
        ),
        'esperado': esperado,
        'ayuda': 'Primero $\\|\\mathbf{A}\\|_\\infty$: suma el valor absoluto '
                 'de cada renglón y toma el mayor. Después lo mismo con '
                 '$\\mathbf{A}^{-1}$, que aquí tiene entradas enteras porque '
                 '$\\det(\\mathbf{A}) = 1$. Multiplica los dos números.',
        'datos': {'A': A.tolist(), 'A_inv': A.inv().tolist(),
                  'norma_A': nA, 'norma_A_inv': nAi},
    }
