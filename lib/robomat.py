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

Operadores (importante): ``A @ B`` es el producto matricial y ``A * B`` el
producto elemento a elemento, igual en NumPy y en SymPy (en SymPy puro ``*`` sería
matricial; la clase MatrizRobomat lo cambia para que no haya ambigüedad).

Constructores: ``zeros(3)`` da una matriz 3x3 (convención de MATLAB), no un vector;
para un vector usa ``zeros(3, 1)`` o ``zeros(1, 3)``. Las versiones simbólicas son
``zeros.sym``, ``ones.sym`` y ``eye.sym``.

Concatenar: ``c_[A, b]`` y ``r_[a, b]`` son de NumPy (horizontal y vertical) y no
admiten símbolos. Para matrices simbólicas usa ``apilar_columnas`` y
``apilar_filas``, que hacen lo mismo y sí los aceptan.
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
# zeros / ones / eye con sintaxis de MATLAB.
# En MATLAB zeros(3) es una matriz 3x3; en NumPy zeros(3) es un vector,
# y ademas zeros(3, 4) fallaba porque el segundo argumento se tomaba
# como `dtype`. Aqui se sigue MATLAB: zeros(3) -> matriz 3x3.
# Para un vector usa zeros(n, 1) o zeros(1, n), que deja clara la forma.
# Las versiones _sym devuelven matrices SIMBOLICAS (para llenar con letras).
# ------------------------------------------------------------------
_np_zeros = np.zeros
_np_ones = np.ones


def _dimensiones(args):
    """Interpreta los argumentos como dimensiones, o devuelve None."""
    if not args:
        return None
    if len(args) == 1 and isinstance(args[0], (tuple, list)):
        return tuple(int(d) for d in args[0])
    if all(isinstance(a, (int, np.integer)) for a in args):
        return tuple(int(a) for a in args)
    return None


def zeros(*args, **kwargs):
    """zeros(n) -> matriz n x n de ceros;  zeros(m, n) -> matriz m x n.

    Sigue la convención de MATLAB. Para un vector usa zeros(n, 1) o zeros(1, n).
    """
    dims = _dimensiones(args)
    if dims is not None:
        return _np_zeros(dims if len(dims) > 1 else (dims[0], dims[0]), **kwargs)
    return _np_zeros(*args, **kwargs)


def ones(*args, **kwargs):
    """ones(n) -> matriz n x n de unos;  ones(m, n) -> matriz m x n.

    Sigue la convención de MATLAB. Para un vector usa ones(n, 1) o ones(1, n).
    """
    dims = _dimensiones(args)
    if dims is not None:
        return _np_ones(dims if len(dims) > 1 else (dims[0], dims[0]), **kwargs)
    return _np_ones(*args, **kwargs)


def eye(*args, **kwargs):
    """eye(n) -> identidad n x n;  eye(m, n) -> identidad rectangular m x n."""
    return np.eye(*args, **kwargs)


def _forma_simbolica(args):
    """Dimensiones para las variantes simbólicas: (n, n) si recibe solo n."""
    dims = _dimensiones(args)
    if dims is None:
        raise TypeError('Usa zeros.sym(n), zeros.sym(m, n) o zeros.sym((m, n)).')
    return dims if len(dims) > 1 else (dims[0], dims[0])


def zeros_sym(*args):
    """Matriz SIMBÓLICA de ceros: zeros_sym(3) -> 3x3, zeros_sym(2, 3) -> 2x3.

    También disponible como ``zeros.sym(...)``.
    """
    return MatrizRobomat(sym.zeros(*_forma_simbolica(args)))


def ones_sym(*args):
    """Matriz SIMBÓLICA de unos. También disponible como ``ones.sym(...)``."""
    return MatrizRobomat(sym.ones(*_forma_simbolica(args)))


def eye_sym(*args):
    """Matriz SIMBÓLICA identidad. También disponible como ``eye.sym(...)``."""
    return MatrizRobomat(sym.eye(*_forma_simbolica(args)))


# Forma corta preferida: zeros.sym(3), ones.sym(2, 3), eye.sym(3)
zeros.sym = zeros_sym
ones.sym = ones_sym
eye.sym = eye_sym


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
    """Matriz simbólica con la misma semántica de operadores que NumPy.

    En SymPy puro ``*`` es el producto matricial; aquí se cambia a propósito
    para que el resultado **no dependa** de si la matriz tiene números o letras:

        A * B    -> producto ELEMENTO A ELEMENTO
        A @ B    -> producto MATRICIAL
        A ** 2   -> potencia ELEMENTO A ELEMENTO

    Hay que redefinir también ``__matmul__`` y ``__pow__`` porque SymPy los
    deriva de ``__mul__``: si solo se cambiara ``*``, ``@`` quedaría haciendo el
    producto elemento a elemento sin avisar.
    """

    __array_priority__ = 1000.0   # que NumPy ceda el paso a nuestra __rmul__

    @property
    def T(self):
        return MatrizRobomat(self.transpose())

    def __array__(self, dtype=None, *args, **kwargs):
        """Permite np.array(m) y operaciones NumPy sobre la matriz."""
        return np.array(self.tolist(), dtype=dtype or float)

    @staticmethod
    def _como_matriz(otro):
        """Convierte un arreglo de NumPy a matriz simbólica."""
        return sym.Matrix(np.asarray(otro).tolist())

    def __mul__(self, otro):
        """Producto elemento a elemento (como ``.*`` de MATLAB)."""
        if isinstance(otro, np.ndarray):
            otro = self._como_matriz(otro)
        if isinstance(otro, sym.MatrixBase):
            return MatrizRobomat(self.multiply_elementwise(otro))
        if isinstance(otro, (int, float, complex, np.number, sym.Basic)):
            return MatrizRobomat(self.applyfunc(lambda e: e * otro))
        return NotImplemented

    def __rmul__(self, otro):
        return self.__mul__(otro)

    def __matmul__(self, otro):
        """Producto matricial (el que en SymPy sería ``*``)."""
        if isinstance(otro, np.ndarray):
            otro = self._como_matriz(otro)
        return MatrizRobomat(sym.MutableDenseMatrix.__mul__(self, otro))

    def __rmatmul__(self, otro):
        if isinstance(otro, np.ndarray):
            otro = self._como_matriz(otro)
        return MatrizRobomat(sym.MutableDenseMatrix.__rmul__(self, otro))

    def __pow__(self, n):
        """Potencia elemento a elemento (como en NumPy)."""
        if isinstance(n, (int, np.integer)):
            return MatrizRobomat(self.applyfunc(lambda e: e ** n))
        return NotImplemented


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
    """I[4] -> eye(4); I[3, 4] -> identidad rectangular eye(3, 4).

    Con ``I.sym[...]`` devuelve la versión simbólica: I.sym[3], I.sym[3, 4].
    """

    def __getitem__(self, dims):
        if isinstance(dims, (int, np.integer)):
            return np.eye(int(dims))
        if isinstance(dims, tuple) and len(dims) == 2:
            return np.eye(int(dims[0]), int(dims[1]))
        raise ValueError(
            'Usa I[n] para la identidad n x n, o I[m, n] para la rectangular. '
            'Para desplazar la diagonal usa eye(m, n, k).')

    @property
    def sym(self):
        """Versión simbólica: I.sym[3] -> identidad simbólica 3x3."""
        return _CreadorIdentidadSimbolica()


class _CreadorIdentidadSimbolica:
    """I.sym[4] -> eye_sym(4); I.sym[3, 4] -> eye_sym(3, 4)."""

    def __getitem__(self, dims):
        if isinstance(dims, (int, np.integer)):
            return MatrizRobomat(sym.eye(int(dims)))
        if isinstance(dims, tuple) and len(dims) == 2:
            return MatrizRobomat(sym.eye(int(dims[0]), int(dims[1])))
        raise ValueError('Usa I.sym[n] o I.sym[m, n].')


M = _CreadorMatriz()
I = _CreadorIdentidad()


def _a_exacto(e):
    """Convierte un Float a Integer o Rational exacto.

    La tolerancia es absoluta (1e-10) para reconocer fracciones "obvias" como
    0.1 -> 1/10 o 7.85 -> 157/20. Además se exige que la fracción tenga una
    magnitud comparable a la del número original: así 1e-18 NO se convierte en
    cero, que sería destructivo.
    """
    if not getattr(e, "is_Float", False):
        return e
    v = float(e)
    if v.is_integer():
        return sym.Integer(int(v))
    r = sym.nsimplify(e, rational=True, tolerance=1e-10)
    if not r.is_Rational or r == 0:
        return e
    razon = abs(float(r)) / abs(v)
    return r if 0.1 <= razon <= 10 else e


def _matriz_exacta(datos):
    """Matriz simbólica a partir de listas, con los números en forma exacta."""
    return sym.Matrix(datos).applyfunc(_a_exacto)


def var(*args):
    """Crea símbolos o convierte a simbólico, según el tipo de entrada.

    - ``var('q1', 'q2')``        -> crea variables simbólicas
    - ``var(A)``                 -> convierte la matriz A (NumPy o lista) a simbólica
    - ``var(2.5)``               -> convierte un número a su forma exacta

    Al convertir, los números pasan a su forma exacta: ``1.0`` se vuelve ``1``,
    ``0.1`` se vuelve ``1/10`` y ``7.85`` se vuelve ``157/20``. Así el álgebra
    simbólica trabaja sin errores de redondeo. Los valores demasiado pequeños
    (como ``1e-18``) se dejan como flotantes para no destruirlos.

    Como ``sym(A)`` en MATLAB: la misma función sirve para las dos cosas y
    decide sola mirando lo que recibe.
    """
    if len(args) == 1 and not isinstance(args[0], str):
        dato = args[0]
        if isinstance(dato, MatrizRobomat):
            return MatrizRobomat(dato.applyfunc(_a_exacto))
        if isinstance(dato, sym.MatrixBase):
            return MatrizRobomat(dato.applyfunc(_a_exacto))
        if isinstance(dato, np.ndarray):
            return MatrizRobomat(_matriz_exacta(dato.tolist()))
        if isinstance(dato, (list, tuple)):
            return MatrizRobomat(_matriz_exacta(dato))
        if isinstance(dato, float):
            return _a_exacto(sym.Float(dato))
        return sym.sympify(dato)
    if not all(isinstance(a, str) for a in args):
        raise TypeError("var() espera nombres ('x', 'y'), una matriz o un número")
    return sym.symbols(' '.join(args))


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


def _bloques_a_matrices(bloques):
    """Separa los bloques en simbólicos y numéricos, y decide el tipo del result."""
    hay_simbolico = any(isinstance(b, (sym.MatrixBase, MatrizRobomat)) for b in bloques)
    if hay_simbolico:
        return [MatrizRobomat(sym.Matrix(b)) if not isinstance(b, MatrizRobomat)
                else b for b in bloques], True
    return [np.atleast_2d(b) for b in bloques], False


def apilar_filas(*bloques):
    """Apila bloques EN VERTICAL (uno debajo de otro).

    Equivale a ``r_[...]`` de NumPy, pero funciona también con matrices
    simbólicas. Sirve para armar una matriz renglón por renglón:

        apilar_filas(M[[1, 2, 3]], M[[4, 5, 6]])   ->  matriz 2 x 3
    """
    partes, simbolico = _bloques_a_matrices(bloques)
    if simbolico:
        filas = []
        for p in partes:
            for i in range(p.rows):
                filas.append([p[i, j] for j in range(p.cols)])
        return MatrizRobomat(sym.Matrix(filas))
    return np.vstack(partes)


def apilar_columnas(*bloques):
    """Apila bloques EN HORIZONTAL (uno al lado de otro).

    Equivale a ``c_[...]`` de NumPy, pero funciona también con matrices
    simbólicas. Es lo que forma la matriz aumentada [A | b].
    """
    partes, simbolico = _bloques_a_matrices(bloques)
    if simbolico:
        return MatrizRobomat(partes[0].row_join(*partes[1:]))
    return np.hstack(partes)
