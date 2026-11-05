"""ÍNDICE de las preguntas del Cuaderno 04 — Especiales e iterativos.

    #   archivo                            tipo     qué evalúa
    1   esp_01_dominancia.md               mcq      qué garantiza la dominancia
    2   esp_02_jacobi_gs.md                mcq      Jacobi contra Gauss-Seidel
    3   esp_03_thomas.md                   mcq      qué gana Thomas
    4   esp_04_cholesky.md                 mcq      cuándo se usa Cholesky
    5   esp_05_paro.md                     mcq      criterio de paro
    6   p06_tridiagonal.py                 matriz   armar A desde e, f, g
    7   p07_fprima.py                      numero   el pivote modificado f'_2
    8   p08_cholesky.py                    numero   la diagonal l_33
    9   p09_barrida_jacobi.py              matriz   una barrida de Jacobi A MANO
    10  p10_barrida_seidel.py              matriz   una barrida de Gauss-Seidel A MANO
    11  p11_programa_jacobi.py             funcion  Jacobi completo
    12  p12_programa_seidel.py             funcion  Gauss-Seidel completo
    13  p13_programa_thomas.py             funcion  el algoritmo de Thomas

Orden del cuaderno: primero las matrices especiales (Thomas y Cholesky), que
son métodos EXACTOS y continúan lo de los cuadernos 02 y 03; después los
iterativos, que se trabajan en float.

Las de opción múltiple son SOLO su .md (la correcta se marca con ``- [x]``).
Las demás son un .py con ``construir(semilla)``.

Las preguntas 9 y 10 son cuentas a mano (como las de la Unidad 2): una sola
barrida, escrita con decimales exactos. Las 11 y 12 piden el método COMPLETO,
con reordenamiento de filas y criterio de paro declarado en la firma; la
llamada de calificación pasa ``tol=1e-6`` y ``max_iter=100``. La 13 queda en
aritmética exacta, porque Thomas sí es un método exacto.
"""
from mn_motor.mcq import desde_markdown

from . import (p06_tridiagonal, p07_fprima, p08_cholesky, p09_barrida_jacobi,
               p10_barrida_seidel, p11_programa_jacobi, p12_programa_seidel,
               p13_programa_thomas)

CARPETA = 'preguntas/u3_04_especiales_iterativos'

PREGUNTAS = [
    desde_markdown(f'{CARPETA}/esp_01_dominancia.md'),
    desde_markdown(f'{CARPETA}/esp_02_jacobi_gs.md'),
    desde_markdown(f'{CARPETA}/esp_03_thomas.md'),
    desde_markdown(f'{CARPETA}/esp_04_cholesky.md'),
    desde_markdown(f'{CARPETA}/esp_05_paro.md'),
    p06_tridiagonal,
    p07_fprima,
    p08_cholesky,
    p09_barrida_jacobi,
    p10_barrida_seidel,
    p11_programa_jacobi,
    p12_programa_seidel,
    p13_programa_thomas,
]
