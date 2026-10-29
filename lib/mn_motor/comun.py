"""Utilidades compartidas por las preguntas. Nada aquí sabe de una pregunta concreta.

Si algo solo lo usa UNA pregunta, va en el archivo de esa pregunta: así el
archivo se puede auditar solo, sin saltar a otro lado.
"""
import ast
import hashlib
import re
from string import ascii_lowercase


# ---------------------------------------------------------------------
# Identificación del alumno
# ---------------------------------------------------------------------

def extraer_nc(identificador):
    """Número de Control a partir del correo institucional.

        'm16330887@hermosillo.tecnm.mx' -> '16330887'
        '16330887@hermosillo.tecnm.mx'  -> '16330887'
        'm{16330887}@tecnm.mx'          -> '16330887'
    """
    if identificador is None:
        return None
    s = str(identificador).strip()
    entre_llaves = re.search(r'\{([^}]+)\}', s)
    if entre_llaves:
        return entre_llaves.group(1).strip()
    local = s.split('@')[0]
    digitos = re.search(r'\d{4,}', local)
    return digitos.group(0) if digitos else None


def semilla_de(identificador):
    """Semilla determinista del NC: el mismo alumno recibe siempre lo mismo."""
    nc = extraer_nc(identificador) or str(identificador)
    return int(hashlib.sha256(nc.encode('utf-8')).hexdigest()[:8], 16)


def semilla_pregunta(identificador, sal):
    """Semilla independiente por pregunta.

    El sal es una constante distinta en cada archivo de pregunta, de modo que
    dos preguntas no reciben por casualidad los mismos números y una no puede
    delatar la respuesta de otra.
    """
    return semilla_de(identificador) ^ sal


# ---------------------------------------------------------------------
# Presentación en LaTeX
# ---------------------------------------------------------------------

def tex(matriz):
    """Matriz -> LaTeX de un bmatrix, SIN los delimitadores ``$``.

    Los ``$`` los pone quien llama, porque a veces va en línea (``$...$``) y a
    veces en su propio renglón (``$$...$$``).
    """
    filas = r' \\ '.join(
        ' & '.join(f'{v:g}' if isinstance(v, (int, float)) else str(v) for v in fila)
        for fila in matriz)
    return r'\begin{bmatrix}' + filas + r'\end{bmatrix}'


def tex_vector(valores):
    """Columna a partir de una lista plana, en LaTeX sin ``$``."""
    return tex([[v] for v in valores])


def letra(n):
    """0 -> 'a', 1 -> 'b', ..."""
    return ascii_lowercase[n]


def letras(n):
    """0..n -> 'abcd' (para marcar las opciones de opción múltiple)."""
    return ascii_lowercase[:n]


# ---------------------------------------------------------------------
# Comparar respuestas
# ---------------------------------------------------------------------

def a_lista(texto):
    """Texto del alumno -> lista de listas. Seguro: no usa ``eval``.

    Acepta también matrices (ndarray, sympy Matrix o MatrizRobomat), que es lo
    que devuelven las funciones que programan los alumnos: ``str(Matrix(...))``
    no es evaluable por ``literal_eval``, así que hay que convertirlas antes.
    """
    if texto is None:
        return None
    if hasattr(texto, 'tolist') and not isinstance(texto, (list, tuple)):
        v = texto.tolist()
        if isinstance(v, (int, float)):
            return [[v]]
        if v and isinstance(v[0], (list, tuple)):
            return [list(f) for f in v]
        return [list(v)]
    if isinstance(texto, (list, tuple)):
        return [list(f) if isinstance(f, (list, tuple)) else [f] for f in texto]
    s = str(texto).strip()
    if not s:
        return None
    try:
        v = ast.literal_eval(s)
    except Exception:
        return None
    if isinstance(v, (int, float)):
        return [[v]]
    if isinstance(v, (list, tuple)):
        if v and isinstance(v[0], (list, tuple)):
            return [list(f) for f in v]
        return [list(v)]
    return None


def matriz_igual(respuesta, esperado, tol=1e-6):
    """¿La respuesta del alumno coincide con la matriz esperada?"""
    r = a_lista(respuesta)
    if r is None:
        return False
    if len(r) != len(esperado):
        return False
    if any(len(f) != len(esperado[i]) for i, f in enumerate(r)):
        return False
    for i, fila in enumerate(r):
        for j, v in enumerate(fila):
            try:
                # Se compara al revés a propósito: con `>` un NaN pasaría,
                # porque `nan > tol` es False y el bucle seguiría.
                if not abs(float(v) - float(esperado[i][j])) <= tol:
                    return False
            except (TypeError, ValueError):
                return False
    return True


def _es_lista_de_matrices(x):
    """¿Es una tupla/lista de matrices (y no una sola matriz)?

    Una matriz es ``[[...], [...]]``: dos niveles. Una lista de matrices tiene
    tres, porque el primer elemento ya es ``[[...], ...]``.
    """
    if not isinstance(x, (list, tuple)) or not x:
        return False
    primero = x[0]
    return (isinstance(primero, (list, tuple)) and bool(primero)
            and isinstance(primero[0], (list, tuple)))


def comparar(respuesta, esperado):
    """Compara la respuesta con lo esperado, admitiendo VARIAS matrices.

    Los métodos que devuelven dos resultados (por ejemplo LU entrega ``L`` y
    ``U``) se comparan pieza por pieza. Todo lo demás pasa por ``matriz_igual``.
    """
    if _es_lista_de_matrices(esperado):
        try:
            partes = list(respuesta)
        except TypeError:
            return False
        if len(partes) != len(esperado):
            return False
        return all(matriz_igual(p, e) for p, e in zip(partes, esperado))
    return matriz_igual(respuesta, esperado)


def numero_igual(respuesta, esperado, tol=1e-6):
    try:
        return abs(float(respuesta) - float(esperado)) < tol
    except (TypeError, ValueError):
        return False
