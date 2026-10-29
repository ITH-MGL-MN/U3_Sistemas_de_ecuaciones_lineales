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
    9   p09_programa_eliminar.py            funcion  programar la eliminación
    10  p10_programa_sustitucion.py         funcion  programar la sustitución
    11  p11_programa_solve.py               funcion  programar el método completo

Las de opción múltiple son SOLO su .md (la correcta se marca con ``- [x]``).
Las demás son un .py con ``construir(semilla)``.

Las de tipo ``funcion`` (9-11) no piden teclear nada: el alumno escribe la
función en el cuaderno y aquí se le busca por nombre (``FUNCION``) para probarla
con casos ocultos de tamaños 2, 3 y 4. ``REFERENCIA`` dice qué función de
``mn_motor.solvers_u3`` resuelve el caso: la usa ``tools/build_grader.py`` para
comprobar el blob de punta a punta.
"""
from mn_motor.mcq import desde_markdown

from . import (p06_triangular, p07_multiplicador, p08_determinante,
               p09_programa_eliminar, p10_programa_sustitucion,
               p11_programa_solve)

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
    p09_programa_eliminar,
    p10_programa_sustitucion,
    p11_programa_solve,
]
