"""ÍNDICE de las preguntas del Cuaderno 01 — Álgebra Lineal.

Este archivo es el mapa: aquí se ve, de un vistazo, qué preguntas hay, en qué
orden salen y dónde vive cada una.

    #   archivo                                  tipo     qué evalúa
    1   alg_01_op_matricial.md                   mcq      @ es el producto matricial
    2   alg_02_asterisco.md                      mcq      * es elemento a elemento
    3   alg_03_forma_vector.md                   mcq      M[[1,2,3]] es un renglón
    4   alg_04_matriz_aumentada.md               mcq      cómo se forma [A|b]
    5   alg_05_np_array.md                       mcq      por qué np.array no concatena
    6   alg_06_traspuesta.md                     mcq      para qué sirve A.T
    7   alg_07_zeros.md                          mcq      zeros(3) es 3x3
    8   alg_08_enteros.md                        mcq      la trampa de los enteros
    9   p09_matriz_aumentada.py                   matriz   escribir la aumentada
    10  p10_operacion_renglon.py                 matriz   aplicar R2 <- R2 - m*R1
    11  p11_producto_escalar.py                  numero   leer una posición de k*A

Las de opción múltiple son SOLO su .md: no tienen lógica en Python, así que se
editan directamente ahí. La correcta se marca con ``- [x]``.

Las demás son un .py con una función ``construir(semilla)`` que devuelve la
pregunta ya sembrada. Para cambiarlas se abre su archivo y nada más.

Para AÑADIR una pregunta: se crea el archivo y se agrega a ``PREGUNTAS``.
Para cambiar el ORDEN: se mueve la línea aquí.
"""
from mn_motor.mcq import desde_markdown

from . import p09_matriz_aumentada, p10_operacion_renglon, p11_producto_escalar

CARPETA = 'preguntas/u3_01_algebra_lineal'

# Cada elemento tiene un método construir(semilla). Los objetos que devuelve
# desde_markdown() y los módulos de pregunta cumplen el mismo contrato.
PREGUNTAS = [
    desde_markdown(f'{CARPETA}/alg_01_op_matricial.md'),
    desde_markdown(f'{CARPETA}/alg_02_asterisco.md'),
    desde_markdown(f'{CARPETA}/alg_03_forma_vector.md'),
    desde_markdown(f'{CARPETA}/alg_04_matriz_aumentada.md'),
    desde_markdown(f'{CARPETA}/alg_05_np_array.md'),
    desde_markdown(f'{CARPETA}/alg_06_traspuesta.md'),
    desde_markdown(f'{CARPETA}/alg_07_zeros.md'),
    desde_markdown(f'{CARPETA}/alg_08_enteros.md'),
    p09_matriz_aumentada,
    p10_operacion_renglon,
    p11_producto_escalar,
]
