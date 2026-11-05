"""solvers_u3 — implementaciones de REFERENCIA de los métodos directos.

Viven en el motor, nunca en el cuaderno: son contra lo que se comparan las
funciones que escriben los alumnos. Igual que en la tarea de U2, aquí está el
método completo y (más adelante) los pasos sueltos que se calculan a mano.

Todo trabaja con aritmética EXACTA (sympy). Así la comparación no depende de
tolerancias y un error de redondeo no se confunde con un error de método.
"""
from __future__ import annotations

from typing import cast

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


def _a_vector(x) -> list[sp.Expr]:
    """Lista plana o matriz -> lista plana de expresiones."""
    m = _a_matriz(x)
    if m.rows == 1 and m.cols > 1:
        m = m.T
    return [cast(sp.Expr, sp.nsimplify(v)) for v in m]


# ============================================================
# Descomposición LU (Cuaderno 03)
# ============================================================
def lu_doolittle(A):
    """A = L U con L de unos en la diagonal (Doolittle).

    Devuelve ``(L, U)`` como listas de listas. ``L`` guarda los multiplicadores
    de la eliminación y ``U`` los pivotes ya actualizados, así que es la misma
    cuenta de ``gauss_eliminar`` pero sin tocar el lado derecho.
    """
    M = _a_matriz(A)
    n = M.rows
    U = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    L = [[sp.Integer(1) if i == j else sp.Integer(0) for j in range(n)]
         for i in range(n)]
    for k in range(n):
        if U[k][k] == 0:
            raise ZeroDivisionError(f'pivote cero en la columna {k + 1}')
        for i in range(k + 1, n):
            m = sp.nsimplify(U[i][k] / U[k][k])
            L[i][k] = m
            U[i] = [sp.nsimplify(U[i][j] - m * U[k][j]) for j in range(n)]
    return L, U


def sustitucion_adelante(L, b):
    """Resuelve ``L y = b`` con L triangular inferior. Devuelve y (columna)."""
    M = _a_matriz(L).row_join(_a_columna(b))
    n = M.rows
    A = [[sp.nsimplify(M[i, j]) for j in range(n + 1)] for i in range(n)]
    y: list[sp.Expr] = [sp.Integer(0)] * n
    for i in range(n):
        suma = sum(A[i][j] * y[j] for j in range(i))
        if A[i][i] == 0:
            raise ZeroDivisionError(f'pivote cero en la fila {i + 1}')
        y[i] = sp.nsimplify((A[i][n] - suma) / A[i][i])
    return [[v] for v in y]


def lu_solve(L, U, b):
    """Las dos sustituciones: y de L y = b, luego x de U x = y."""
    y = sustitucion_adelante(L, b)
    return sustitucion_atras(_a_matriz(U).row_join(_a_matriz(y)))


def lu_completo(A, b):
    """Factoriza y resuelve: A x = b por LU."""
    L, U = lu_doolittle(A)
    return lu_solve(L, U, b)


# ============================================================
# Métodos iterativos y matrices especiales (Cuaderno 04)
# ============================================================
def jacobi_paso(A, b, x):
    """UNA barrida de Jacobi: todo se calcula con el vector viejo."""
    M = _a_matriz(A)
    n = M.rows
    coef = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    rhs = _a_vector(b)
    viejo = _a_vector(x)
    nuevo: list[sp.Expr] = [sp.Integer(0)] * n
    for i in range(n):
        suma = sum(coef[i][j] * viejo[j] for j in range(n) if j != i)
        nuevo[i] = sp.nsimplify((rhs[i] - suma) / coef[i][i])
    return [[v] for v in nuevo]


def gauss_seidel_paso(A, b, x):
    """UNA barrida de Gauss-Seidel: reutiliza lo recién calculado."""
    M = _a_matriz(A)
    n = M.rows
    coef = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    rhs = _a_vector(b)
    v: list[sp.Expr] = _a_vector(x)
    for i in range(n):
        suma = sum(coef[i][j] * v[j] for j in range(n) if j != i)
        v[i] = sp.nsimplify((rhs[i] - suma) / coef[i][i])
    return [[valor] for valor in v]


def es_diagonal_dominante(A):
    """¿Se cumple |a_ii| > suma de los demás |a_ij| en TODOS los renglones?"""
    M = _a_matriz(A)
    n = M.rows
    coef = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        resto = sum(abs(coef[i][j]) for j in range(n) if j != i)
        if not abs(coef[i][i]) > resto:
            return False
    return True


# ============================================================
# Métodos iterativos COMPLETOS, en punto flotante
# ============================================================
# Aquí NO se usa aritmética exacta: los métodos iterativos se usan en sistemas
# grandes, donde el costo de las fracciones crece sin control y donde el error
# de redondeo es parte de la lección. Todo lo de abajo trabaja en float.
def _a_float(A):
    """Matriz -> lista de listas de float."""
    M = _a_matriz(A)
    return [[float(sp.N(M[i, j])) for j in range(M.cols)]
            for i in range(M.rows)]


def _b_float(b):
    """Vector -> lista de float."""
    return [float(sp.N(v)) for v in _a_vector(b)]


def reordenar_dominante(A, b):
    """Reordena las ECUACIONES (filas) para que la diagonal sea dominante.

    Regla (la misma que se declara en el cuaderno): para cada columna k, de las
    ecuaciones que todavía no se han usado, se elige la del mayor |a_ik|. Las
    incógnitas NO se mueven; solo cambia el orden de las ecuaciones.

    Devuelve ``(A2, b2)`` como listas de float.
    """
    A2 = _a_float(A)
    b2 = _b_float(b)
    n = len(b2)
    orden: list[int] = []
    usadas: set[int] = set()
    for k in range(n):
        disponibles = [i for i in range(n) if i not in usadas]
        elegida = max(disponibles, key=lambda i: abs(A2[i][k]))
        orden.append(elegida)
        usadas.add(elegida)
    return [A2[i] for i in orden], [b2[i] for i in orden]


def error_relativo_inf(x_nuevo, x_viejo):
    """||x_nuevo - x_viejo||_inf / ||x_nuevo||_inf, con guarda en cero.

    Se usa la norma infinito del VECTOR (la componente mayor), no el cociente
    componente por componente: si una incógnita tiende a cero, dividir entre
    ella hace que el error nunca baje de la tolerancia.
    """
    dif = max((abs(a - b) for a, b in zip(x_nuevo, x_viejo)), default=0.0)
    escala = max((abs(v) for v in x_nuevo), default=0.0)
    return dif / escala if escala != 0 else dif


def _jacobi_crudo(A2, b2, tol, max_iter):
    """Jacobi sobre la matriz TAL CUAL, sin reordenar (uso interno)."""
    n = len(b2)
    x = [0.0] * n
    for k in range(1, max_iter + 1):
        nuevo = [0.0] * n
        for i in range(n):
            suma = sum(A2[i][j] * x[j] for j in range(n) if j != i)
            nuevo[i] = (b2[i] - suma) / A2[i][i]
        err = error_relativo_inf(nuevo, x)
        x = nuevo
        if err < tol:
            return x, k
    return x, max_iter


def _gs_crudo(A2, b2, tol, max_iter):
    """Gauss-Seidel sobre la matriz TAL CUAL, sin reordenar (uso interno)."""
    n = len(b2)
    x = [0.0] * n
    for k in range(1, max_iter + 1):
        viejo = list(x)
        for i in range(n):
            suma = sum(A2[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b2[i] - suma) / A2[i][i]
        if error_relativo_inf(x, viejo) < tol:
            return x, k
    return x, max_iter


def jacobi(A, b, tol=1e-6, max_iter=100):
    """Jacobi completo. Devuelve ``(x, iteraciones)``.

    Reordena las filas primero (ver ``reordenar_dominante``) y se detiene cuando
    el error relativo infinito baja de ``tol`` o al llegar a ``max_iter``.
    """
    A2, b2 = reordenar_dominante(A, b)
    return _jacobi_crudo(A2, b2, tol, max_iter)


def gauss_seidel(A, b, tol=1e-6, max_iter=100):
    """Gauss-Seidel completo. Devuelve ``(x, iteraciones)``."""
    A2, b2 = reordenar_dominante(A, b)
    return _gs_crudo(A2, b2, tol, max_iter)


def solucion_exacta(A, b):
    """La solución del sistema como lista de float (para calificar)."""
    M = _a_matriz(A)
    sol = M.inv() * sp.Matrix(_b_float(b))
    return [float(v) for v in sol]


def thomas_descomposicion(e, f, g, r):
    """Fases 1 y 2 de Thomas: devuelve ``(f', r')`` ya modificados.

    Se separa de ``thomas`` para que la pregunta que pide ``f'_2`` a mano use
    exactamente la misma cuenta que el método completo.
    """
    ev, fv = _a_vector(e), _a_vector(f)
    gv, rv = _a_vector(g), _a_vector(r)
    n = len(fv)
    fp: list[sp.Expr] = [sp.Integer(0)] * n
    rp: list[sp.Expr] = [sp.Integer(0)] * n
    fp[0], rp[0] = fv[0], rv[0]
    for k in range(1, n):
        if fp[k - 1] == 0:
            raise ZeroDivisionError(f'pivote cero en la fila {k}')
        ek = sp.nsimplify(ev[k] / fp[k - 1])
        fp[k] = sp.nsimplify(fv[k] - ek * gv[k - 1])
        rp[k] = sp.nsimplify(rv[k] - ek * rp[k - 1])
    return fp, rp


def thomas(e, f, g, r):
    """Algoritmo de Thomas para una tridiagonal.

    Convención del documento: ``e[i]`` multiplica a ``x_{i-1}`` y ``g[i]`` a
    ``x_{i+1}``; por eso ``e[0]`` y ``g[n-1]`` no se usan (vale poner 0).
    Devuelve x como columna.
    """
    gv = _a_vector(g)
    fp, rp = thomas_descomposicion(e, f, g, r)
    n = len(fp)
    x: list[sp.Expr] = [sp.Integer(0)] * n
    if fp[n - 1] == 0:
        raise ZeroDivisionError('pivote cero en la ultima fila')
    x[n - 1] = sp.nsimplify(rp[n - 1] / fp[n - 1])
    for k in range(n - 2, -1, -1):
        x[k] = sp.nsimplify((rp[k] - gv[k] * x[k + 1]) / fp[k])
    return [[v] for v in x]


def cholesky(A):
    """A = L L^T para A simétrica definida positiva. Devuelve L."""
    M = _a_matriz(A)
    n = M.rows
    coef = [[sp.nsimplify(M[i, j]) for j in range(n)] for i in range(n)]
    L: list[list[sp.Expr]] = [[sp.Integer(0)] * n for _ in range(n)]
    for k in range(n):
        radicando = sp.nsimplify(coef[k][k] - sum(L[k][j] ** 2 for j in range(k)))
        if radicando <= 0:
            raise ValueError('la matriz no es definida positiva')
        L[k][k] = sp.sqrt(radicando)
        for i in range(k + 1, n):
            L[i][k] = sp.nsimplify(
                (coef[i][k] - sum(L[i][j] * L[k][j] for j in range(k)))
                / L[k][k])
    return L


# ============================================================
# Generadores de datos para los casos ocultos
# ============================================================
def sistema_dominante(rng, n, intentos=300):
    """Sistema con dominancia diagonal ESTRICTA y solución entera.

    Se sortea la solución y se arma el lado derecho, así que la respuesta es
    exacta aunque se llegue a ella iterando.
    """
    for _ in range(intentos):
        coef = [[sp.Integer(rng.randint(-3, 3)) for _ in range(n)]
                for _ in range(n)]
        for i in range(n):
            otros = sum(abs(coef[i][j]) for j in range(n) if j != i)
            coef[i][i] = sp.nsimplify(otros + rng.randint(1, 4))
        A = sp.Matrix(coef)
        if A.det() == 0:
            continue
        x = [rng.randint(-3, 3) for _ in range(n)]
        b = sp.Matrix([sum(A[i, j] * x[j] for j in range(n)) for i in range(n)])
        return A, b
    raise RuntimeError(f'no encontré un sistema {n}x{n} dominante')


def sistema_tridiagonal(rng, n, intentos=300):
    """Tridiagonal dominante con solución entera.

    Devuelve ``(e, f, g, r)`` con la convención de ``thomas``: e[0] = 0 y
    g[n-1] = 0, y los cuatro vectores de longitud n.
    """
    for _ in range(intentos):
        e = [sp.Integer(0)] + [sp.Integer(rng.randint(-3, 3)) for _ in range(n - 1)]
        g = [sp.Integer(rng.randint(-3, 3)) for _ in range(n - 1)] + [sp.Integer(0)]
        f: list[sp.Expr] = []
        for i in range(n):
            vecinos = abs(e[i]) + abs(g[i])
            f.append(sp.Integer(vecinos + rng.randint(1, 4)))
        x = [sp.Integer(rng.randint(-3, 3)) for _ in range(n)]
        r: list[sp.Expr] = []
        for i in range(n):
            valor = f[i] * x[i]
            if i > 0:
                valor += e[i] * x[i - 1]
            if i < n - 1:
                valor += g[i] * x[i + 1]
            r.append(sp.nsimplify(valor))
        try:
            thomas(e, f, g, r)
        except ZeroDivisionError:
            continue
        return e, f, g, r
    raise RuntimeError(f'no encontré una tridiagonal {n}x{n}')


def sistema_spd(rng, n):
    """Matriz simétrica definida positiva con entradas enteras (B^T B + n I)."""
    for _ in range(300):
        B = sp.Matrix([[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)])
        A = B.T * B + n * sp.eye(n)
        if A.det() == 0:
            continue
        return A
    raise RuntimeError(f'no encontré una matriz {n}x{n} definida positiva')


def sistema_permutado(rng, n, intentos=300):
    """Sistema dominante con las filas DESORDENADAS a propósito.

    La solución es entera, pero para llegar a ella hay que reordenar las
    ecuaciones: tal como viene, Gauss-Seidel y Jacobi no convergen (o
    convergen a paso de tortuga). Se acepta sólo si el reordenamiento por
    columnas la vuelve dominante y los dos métodos llegan en menos de 100
    iteraciones, para que los casos ocultos sean reproducibles.
    """
    for _ in range(intentos):
        A, b = sistema_dominante(rng, n)
        perm = list(range(n))
        rng.shuffle(perm)
        if perm == list(range(n)):
            continue
        filas = A.tolist()
        valores = [int(sp.N(v)) for v in b]
        A2 = sp.Matrix([filas[i] for i in perm])
        b2 = sp.Matrix([valores[i] for i in perm])
        if es_diagonal_dominante(A2):
            continue          # el desorden no cambió nada: no sirve de caso
        A3, _ = reordenar_dominante(A2, b2)
        if not es_diagonal_dominante(sp.Matrix(A3)):
            continue
        try:
            x_gs, k_gs = gauss_seidel(A2, b2)
            x_ja, k_ja = jacobi(A2, b2)
        except ZeroDivisionError:
            continue
        if k_gs >= 100 or k_ja >= 100:
            continue
        sol = solucion_exacta(A2, b2)
        if max(abs(x_gs[i] - sol[i]) for i in range(n)) > 1e-4:
            continue
        if max(abs(x_ja[i] - sol[i]) for i in range(n)) > 1e-4:
            continue
        # El caso solo sirve si SIN reordenar de verdad falla: si converge de
        # todos modos, no está evaluando el reordenamiento.
        A_crudo, b_crudo = _a_float(A2), _b_float(b2)
        try:
            x_c, _ = _gs_crudo(A_crudo, b_crudo, 1e-6, 100)
        except (ZeroDivisionError, OverflowError):
            return A2, b2        # sin reordenar ni siquiera se puede dividir
        if max(abs(x_c[i] - sol[i]) for i in range(n)) < 1e-3:
            continue
        return A2, b2
    raise RuntimeError(f'no encontré un sistema {n}x{n} permutado utilizable')


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
