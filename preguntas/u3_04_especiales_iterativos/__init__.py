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
    9   p09_programa_jacobi.py             funcion  una barrida de Jacobi
    10  p10_programa_seidel.py             funcion  una barrida de Gauss-Seidel
    11  p11_programa_thomas.py             funcion  el algoritmo de Thomas

Las de opción múltiple son SOLO su .md (la correcta se marca con ``- [x]``).
Las demás son un .py con ``construir(semilla)``.

Las de programar piden UNA barrida (o el método completo, en Thomas) y no el
método iterativo completo: así la respuesta es exacta y no depende del criterio
de paro, que es una convención y no un resultado.
"""
from mn_motor.mcq import desde_markdown

from . import (p06_tridiagonal, p07_fprima, p08_cholesky, p09_programa_jacobi,
               p10_programa_seidel, p11_programa_thomas)

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
    p09_programa_jacobi,
    p10_programa_seidel,
    p11_programa_thomas,
]
