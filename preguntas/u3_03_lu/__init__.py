"""ÍNDICE de las preguntas del Cuaderno 03 — Descomposición LU.

    #   archivo                            tipo     qué evalúa
    1   lu_01_multiplicadores.md           mcq      qué guarda L
    2   lu_02_diagonal.md                  mcq      por qué L lleva unos
    3   lu_03_cuando.md                    mcq      cuándo conviene factorizar
    4   lu_04_adelante.md                  mcq      qué resuelve L y = b
    5   lu_05_doolittle_crout.md           mcq      Doolittle contra Crout
    6   p06_matriz_l.py                    matriz   escribir L (multiplicadores)
    7   p07_u22.py                         numero   el segundo pivote
    8   p08_y2.py                          numero   una componente de y
    9   p09_programa_lu.py                 funcion  programar la factorización
    10  p10_programa_adelante.py           funcion  programar la sust. adelante
    11  p11_programa_lu_solve.py           funcion  programar el resolvedor
    12  p12_condicion.py                   numero   el número de condición

Las de opción múltiple son SOLO su .md (la correcta se marca con ``- [x]``).
Las demás son un .py con ``construir(semilla)``.

La pregunta 12 es la única que no es de los cuatro cuadernos "de siempre": mide
la confiabilidad del resultado (condicionamiento) y se contesta después de la
sección 7 del cuaderno. Por eso este cuaderno tiene 12 preguntas y los otros 11.

La pregunta 9 devuelve DOS matrices (``L`` y ``U``): ``comun.comparar`` las
compara por separado cuando lo esperado tiene tres niveles de anidamiento.
"""
from mn_motor.mcq import desde_markdown

from . import (p06_matriz_l, p07_u22, p08_y2, p09_programa_lu,
               p10_programa_adelante, p11_programa_lu_solve, p12_condicion)

CARPETA = 'preguntas/u3_03_lu'

PREGUNTAS = [
    desde_markdown(f'{CARPETA}/lu_01_multiplicadores.md'),
    desde_markdown(f'{CARPETA}/lu_02_diagonal.md'),
    desde_markdown(f'{CARPETA}/lu_03_cuando.md'),
    desde_markdown(f'{CARPETA}/lu_04_adelante.md'),
    desde_markdown(f'{CARPETA}/lu_05_doolittle_crout.md'),
    p06_matriz_l,
    p07_u22,
    p08_y2,
    p09_programa_lu,
    p10_programa_adelante,
    p11_programa_lu_solve,
    p12_condicion,
]
