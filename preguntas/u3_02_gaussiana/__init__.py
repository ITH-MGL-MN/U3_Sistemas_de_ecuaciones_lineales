"""ÍNDICE de las preguntas del Cuaderno 02 — Eliminación Gaussiana.

    #   archivo                            tipo     qué evalúa
    1   gau_01_multiplicador.md             mcq      qué es m_ik
    2   gau_02_pivoteo.md                   mcq      para qué el pivoteo parcial
    3   gau_03_pivote_cero.md               mcq      qué pasa con pivote cero
    4   gau_04_triangular.md                mcq      qué significa triangular superior
    5   gau_05_costo.md                     mcq      costo O(n^3)
    6   p06_triangular.py                   matriz   triangularizar un sistema
    7   p07_multiplicador.py                numero   calcular m21
    8   p08_determinante.py                 numero   determinante por pivotes

Las de opción múltiple son SOLO su .md (la correcta se marca con ``- [x]``).
Las demás son un .py con ``construir(semilla)``.
"""
from mn_motor.mcq import desde_markdown

from . import p06_triangular, p07_multiplicador, p08_determinante

CARPETA = 'preguntas/u3_02_gaussiana'

PREGUNTAS = [
    desde_markdown(f'{CARPETA}/gau_01_multiplicador.md'),
    desde_markdown(f'{CARPETA}/gau_02_pivoteo.md'),
    desde_markdown(f'{CARPETA}/gau_03_pivote_cero.md'),
    desde_markdown(f'{CARPETA}/gau_04_triangular.md'),
    desde_markdown(f'{CARPETA}/gau_05_costo.md'),
    p06_triangular,
    p07_multiplicador,
    p08_determinante,
]
