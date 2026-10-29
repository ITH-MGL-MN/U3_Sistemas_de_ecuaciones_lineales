"""Pregunta 7 — El multiplicador  ·  id: gau_multiplicador

Qué evalúa: identificar y calcular el multiplicador de un paso concreto.

El elemento se construye como ``a21 = k * a11``, así que ``m21 = a21/a11 = k``
es un entero y la respuesta se escribe sin fracciones.
"""
import random

from mn_motor.comun import tex

ID = 'gau_multiplicador'
TITULO = 'El multiplicador del paso'
SAL = 0xD5          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    a11 = rng.choice([2, 3, 4, 5])
    k = rng.choice([-3, -2, -1, 1, 2, 3])
    a21 = k * a11                      # el multiplicador será exactamente k
    a12 = rng.randint(-4, 4)
    a22 = rng.randint(-4, 4)
    while a22 == k * a12:              # si no, la segunda fila se anula entera
        a22 = rng.randint(-4, 4)

    A = [[a11, a12], [a21, a22]]

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Para el sistema\n\n$${tex(A)}$$\n\n'
            '**¿cuánto vale el multiplicador** $m_{21}$ que elimina $x_1$ '
            'del renglón 2?'
        ),
        'esperado': k,
        'ayuda': r'$m_{21} = a_{21}/a_{11}$. El signo importa.',
        'datos': {'A': A, 'a11': a11, 'a21': a21},
    }
