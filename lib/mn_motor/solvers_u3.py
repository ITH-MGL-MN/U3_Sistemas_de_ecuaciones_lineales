"""solvers_u3 — implementaciones de REFERENCIA de los métodos directos.

Viven en el motor, nunca en el cuaderno: son contra lo que se comparan las
funciones que escriben los alumnos. Igual que en la tarea de U2, aquí está el
método completo y (más adelante) los pasos sueltos que se calculan a mano.

Todo trabaja con aritmética EXACTA (sympy). Así la comparación no depende de
tolerancias y un error de redondeo no se confunde con un error de método.
"""
from __future__ import annotations

import sympy as sp


def _a_matriz(x):
    """Cualquier cosa razonable -> Matrix de sympy."""
    if isinstance(x, sp.MatrixBase):
        return sp.Matrix(x)
    return sp.Matrix(x)


def _a_columna(x):
    """Lista plana o matriz -> Matrix columna."""
    m = _a_matriz(x)
    if m.rows == 1 and m.cols > 1:
        return m.T
    return m


def gauss_eliminar(A, b):
    """Triangulariza [A|b] hacia adelante, SIN pivoteo.

    Devuelve la matriz aumentada triangular como lista de listas, para que la
    comparación con la del alumno sea directa.

    Lanza ZeroDivisionError si aparece un pivote nulo: sin pivoteo el método
    se detiene, y eso es justo lo que enseña la sección de pivoteo.
    """
    Ab = _a_matriz(A).row_join(_a_columna(b))
    n = Ab.rows
    Ab = [[sp.nsimplify(Ab[i, j]) for j in range(n + 1)] for i in range(n)]
    for k in range(n - 1):
        if Ab[k][k] == 0:
            raise ZeroDivisionError(f'pivote cero en la columna {k + 1}')
        for i in range(k + 1, n):
            m = Ab[i][k] / Ab[k][k]
            Ab[i] = [sp.nsimplify(Ab[i][j] - m * Ab[k][j]) for j in range(n + 1)]
    return Ab


def sustitucion_atras(Ab):
    """Despeja x de una matriz aumentada triangular superior.

    Devuelve una columna como lista de listas: [[x1], [x2], ...].
    """
    M = _a_matriz(Ab)
    n = M.rows
    A = [[sp.nsimplify(M[i, j]) for j in range(n + 1)] for i in range(n)]
    x: list[sp.Expr] = [sp.Integer(0)] * n
    for i in range(n - 1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        if A[i][i] == 0:
            raise ZeroDivisionError(f'pivote cero en la fila {i + 1}')
        x[i] = sp.nsimplify((A[i][n] - suma) / A[i][i])
    return [[v] for v in x]


def gauss_solve(A, b):
    """Los dos pasos juntos: devuelve x como lista de listas (columna)."""
    return sustitucion_atras(_a_matriz(gauss_eliminar(A, b)))


def residual_cero(A, x, b):
    """¿A@x - b es exactamente cero? (para verificar, no para calificar)."""
    A = _a_matriz(A)
    x = _a_columna(x)
    b = _a_columna(b)
    return (A * x - b).is_zero_matrix


def sistema_eliminable(rng, n, intentos=300):
    """Sistema n x n cuya eliminación SIN pivoteo corre hasta el final.

    No basta con que la diagonal original no tenga ceros: la eliminación
    MODIFICA los coeficientes de abajo, así que un pivote intermedio puede
    anularse aunque el original no. Por eso se comprueba intentando eliminar,
    y si aparece un pivote nulo se descarta y se sortea otro.
    """
    for _ in range(intentos):
        A = sp.Matrix([[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)])
        if A.det() == 0:
            continue          # singular: la última diagonal quedaría en cero
        x = [rng.randint(-3, 3) for _ in range(n)]
        b = sp.Matrix([sum(A[i, j] * x[j] for j in range(n)) for i in range(n)])
        try:
            gauss_eliminar(A, b)
        except ZeroDivisionError:
            continue
        return A, b
    raise RuntimeError(f'no encontré un sistema {n}x{n} eliminable sin pivoteo')
