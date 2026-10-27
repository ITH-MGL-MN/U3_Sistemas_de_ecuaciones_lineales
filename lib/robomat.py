"""robomat — entorno unificado estilo MATLAB para álgebra lineal, robótica y métodos numéricos.

Fusión de ``matlab_like`` (precarga NumPy/Matplotlib/SciPy con sintaxis MATLAB)
y ``robomat`` (atajos simbólicos y de robótica), pensada para la Unidad 3
(Sistemas de Ecuaciones Lineales).

Se ejecuta en el notebook con::

    exec(open("robomat.py").read(), globals())

De esta forma el alumno escribe directamente, por ejemplo::

    A = M[[1, 2], [3, 4]]        # matriz numérica
    b = M[[5], [6]]              # vector columna
    x = solve(A, b)              # np.linalg.solve
    mostrar(x)                   # render en LaTeX

    q1, q2 = var('q1', 'q2')     # variables simbólicas
    J = jacobiano(M[[cos(q1)]], [q1])

Operadores (importante): ``A @ B`` es el producto matricial y funciona igual en
NumPy y en SymPy. Como ``*`` significa cosas distintas en cada biblioteca, para el
producto elemento a elemento (el ``.*`` de MATLAB) usa ``hadamard(A, B)``, y para
la potencia entrada por entrada, ``potencia_elem(A, n)``.
"""

# ============================================================
# Parte 1 — matlab_like: precarga NumPy / Matplotlib / SciPy
# ============================================================
# `from numpy import *` sombrea los builtins `any`, `all`, `sum`, `max`,
# `min` y `abs`. Guardamos los builtins para usarlos donde haga falta.
import builtins as _builtins

from numpy import *            # noqa: F401,F403  (estilo MATLAB)
from numpy.linalg import *     # noqa: F401,F403  (solve, inv, det, eig, ...)
import numpy as np
from matplotlib.pyplot import *  # noqa: F401,F403
import matplotlib.pyplot as plt

try:
    from scipy.integrate import *  # noqa: F401,F403
except ImportError:
    pass

# Configuración visual estilo MATLAB
np.set_printoptions(precision=4, suppress=True, linewidth=120)
plt.rcParams['figure.figsize'] = (8, 6)

# Alias cortos estilo MATLAB
lin = linspace


# ------------------------------------------------------------------
# Re-exponer builtins sombreados por `from numpy import *` para que
# abs / max / min / sum / any / all funcionen como en Python/MATLAB
# tanto con escalares, listas y generadores como con arreglos NumPy.
# ------------------------------------------------------------------
def _abs(x):
    return _builtins.abs(x) if not isinstance(x, np.ndarray) else np.abs(x)


def _max(*args):
    if len(args) == 1:
        a = args[0]
        return np.max(a) if isinstance(a, np.ndarray) else _builtins.max(a)
    return _builtins.max(*args)


def _min(*args):
    if len(args) == 1:
        a = args[0]
        return np.min(a) if isinstance(a, np.ndarray) else _builtins.min(a)
    return _builtins.min(*args)


def _sum(iterable, *args, **kwargs):
    if isinstance(iterable, np.ndarray):
        return np.sum(iterable, *args, **kwargs)
    return _builtins.sum(iterable, *args)


def _any(iterable):
    return bool(np.any(iterable)) if isinstance(iterable, np.ndarray) else _builtins.any(iterable)


def _all(iterable):
    return bool(np.all(iterable)) if isinstance(iterable, np.ndarray) else _builtins.all(iterable)


abs = _abs
max = _max
min = _min
sum = _sum
any = _any
all = _all


# ============================================================
# Parte 2 — robomat: sintaxis simbólica y de robótica
# ============================================================
import sympy as sym
from IPython.display import display, Math

sym.init_printing(use_latex='mathjax')


def mostrar(expr):
    """Renderiza una matriz o expresión en LaTeX."""
    if isinstance(expr, (sym.MatrixBase, MatrizRobomat)):
        display(Math(sym.latex(expr)))
    else:
        display(expr)


class MatrizRobomat(sym.MutableDenseMatrix):
    """Matriz simbólica cuya propiedad .T devuelve otra MatrizRobomat."""

    @property
    def T(self):
        return MatrizRobomat(self.transpose())

    def __array__(self, dtype=None, *args, **kwargs):
        """Permite np.array(m) y operaciones NumPy sobre la matriz."""
        return np.array(self.tolist(), dtype=dtype or float)


def _es_simbolico(x):
    return isinstance(x, (sym.Symbol, sym.Expr)) or hasattr(x, 'free_symbols')


# Trigonométricas "inteligentes": SymPy si la entrada es simbólica, NumPy si es numérica.
def sin(x):
    return sym.sin(x) if _es_simbolico(x) else np.sin(x)


def cos(x):
    return sym.cos(x) if _es_simbolico(x) else np.cos(x)


def tan(x):
    return sym.tan(x) if _es_simbolico(x) else np.tan(x)


pi = np.pi
rad = np.radians
deg = np.degrees


class _CreadorMatriz:
    """M[[...], [...]] -> matriz (numérica o simbólica)."""

    def __getitem__(self, datos):
        if not isinstance(datos, (list, tuple)):
            datos = [datos]
        filas = [fila if isinstance(fila, (list, tuple)) else [fila] for fila in datos]
        plano = [x for fila in filas for x in fila]
        if _builtins.any(_es_simbolico(x) for x in plano):
            return MatrizRobomat(filas)
        return np.array(filas, dtype=float)


class _CreadorIdentidad:
    """I[4] -> eye(4); I[3, 4] -> eye(3, 4)."""

    def __getitem__(self, dims):
        if isinstance(dims, int):
            return np.eye(dims)
        if isinstance(dims, tuple) and len(dims) == 2:
            return np.eye(dims[0], dims[1])
        raise ValueError('Usa I[n] o I[m, n]')


M = _CreadorMatriz()
I = _CreadorIdentidad()


def var(*nombres):
    """Crea variables simbólicas: var('q1', 'q2', 'L1')."""
    return sym.symbols(' '.join(nombres))


variables_articulares = var  # alias legible


def jacobiano(vector_posicion, variables):
    if not isinstance(vector_posicion, sym.MatrixBase):
        vector_posicion = sym.Matrix(vector_posicion)
    return MatrizRobomat(vector_posicion.jacobian(sym.Matrix(variables)))


def evaluar(expresion, variables, valores):
    if not isinstance(expresion, (sym.MatrixBase, MatrizRobomat)):
        return np.array(expresion, dtype=float)
    sustituciones = list(zip(variables, valores))
    resultado = expresion.subs(sustituciones)
    return np.array(resultado.tolist(), dtype=float)


def hadamard(A, B):
    """Producto elemento a elemento (producto de Hadamard).

    Equivale al `.*` de MATLAB. Existe porque `*` significa cosas distintas en
    cada biblioteca: en NumPy multiplica elemento a elemento, pero en SymPy hace
    el producto matricial. Esta función da **el mismo resultado** con las dos.

        hadamard(M[[1, 2], [3, 4]], M[[2, 0], [1, 2]])   ->  [[2, 0], [3, 8]]

    Para el producto matricial usa siempre `@`, que sí coincide en ambas.
    """
    es_simbolico = isinstance(A, (sym.MatrixBase, MatrizRobomat)) or \
                   isinstance(B, (sym.MatrixBase, MatrizRobomat))
    if es_simbolico:
        Ma = A if isinstance(A, sym.MatrixBase) else sym.Matrix(A)
        Mb = B if isinstance(B, sym.MatrixBase) else sym.Matrix(B)
        return MatrizRobomat(Ma.multiply_elementwise(Mb))
    return np.multiply(A, B)


elem = hadamard  # alias corto


def potencia_elem(A, n):
    """Potencia ELEMENTO A ELEMENTO de una matriz o vector.

    Hace falta porque `A ** 2` tampoco coincide: en NumPy eleva cada entrada,
    pero en SymPy calcula la potencia matricial. Aquí el resultado es el mismo
    en los dos casos.
    """
    if isinstance(A, (sym.MatrixBase, MatrizRobomat)):
        M0 = A if isinstance(A, sym.MatrixBase) else sym.Matrix(A)
        return MatrizRobomat(M0.applyfunc(lambda e: e ** n))
    return np.power(A, n)
