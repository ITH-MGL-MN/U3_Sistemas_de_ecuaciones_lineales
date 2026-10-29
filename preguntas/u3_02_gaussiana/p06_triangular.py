"""Pregunta 6 — Triangularizar un sistema  ·  id: gau_triangular

Qué evalúa: aplicar la eliminación hacia adelante completa y escribir la matriz
aumentada resultante.

Cómo se garantiza que la respuesta sea ENTERA (y por tanto escribible a mano):
la matriz se construye como ``A = L @ U`` con ``L`` triangular inferior unitaria
y ``U`` triangular superior **unitaria**, ambas enteras. Al eliminar ``A`` sin
pivoteo se recupera exactamente ``U``, y los multiplicadores son las entradas de
``L``: enteros. Así ningún paso produce fracciones.
"""
import random

import sympy as sp

from mn_motor.comun import tex

ID = 'gau_triangular'
TITULO = 'Triangularizar el sistema'
SAL = 0xC4          # semilla propia de esta pregunta


def _entera_que_triangulariza(rng):
    """A = L@U con L y U unitarias enteras: la eliminación sale entera."""
    U = sp.eye(3)
    for i in range(3):
        for j in range(i + 1, 3):
            U[i, j] = rng.randint(-3, 3)
    L = sp.eye(3)
    for i in range(3):
        for j in range(i):
            L[i, j] = rng.choice([-2, -1, 1, 2])
    return L * U, U


def construir(semilla):
    rng = random.Random(semilla ^ SAL)
    A, U = _entera_que_triangulariza(rng)

    x = [rng.randint(-3, 3) for _ in range(3)]
    b = [sum(A[i, j] * x[j] for j in range(3)) for i in range(3)]

    # La eliminación (sin pivoteo) de [A|b] debe dar exactamente [U|d].
    Ab = sp.Matrix(A).row_join(sp.Matrix(b))
    for k in range(2):
        for i in range(k + 1, 3):
            m = Ab[i, k] / Ab[k, k]
            Ab[i, :] = Ab[i, :] - m * Ab[k, :]

    esperado = [[int(v) for v in Ab[i, :]] for i in range(3)]

    # Red de seguridad: si algún paso hubiera dado fracciones, la pregunta no
    # se podría contestar escribiendo enteros y habría que cambiar la semilla.
    if not all(v.is_Integer for v in Ab):
        raise AssertionError('la triangularizada salió con fracciones')

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Dado el sistema con\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}$$\n\n'
            f'$$\\mathbf{{b}} = {tex([[v] for v in b])}$$\n\n'
            '**escribe la matriz aumentada ya triangularizada**, es decir, '
            'después de la eliminación hacia adelante (sin pivoteo).'
        ),
        'esperado': esperado,
        'ayuda': 'Elimina x1 del renglón 2 y del 3, y luego x2 del renglón 3. '
                 'Escribe [[a,b,c,d],[e,f,g,h],[i,j,k,l]].',
        'datos': {'A': A.tolist(), 'b': b, 'U': U.tolist()},
    }
