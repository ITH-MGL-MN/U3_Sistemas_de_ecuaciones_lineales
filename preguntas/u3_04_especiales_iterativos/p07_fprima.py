"""Pregunta 7 — El pivote modificado de Thomas  ·  id: esp_fprima

Qué evalúa: la recursión de la fase 1 del algoritmo,

    e'_k = e_k / f'_{k-1},     f'_k = f_k - e'_k * g_{k-1}.

Se pide un solo número (``f'_2``) para que se conteste a mano.

Se sortea con ``e[1]`` múltiplo de ``f[0]``, de modo que ``f'_2`` sale **entero**
y se puede escribir sin decimales.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref
from mn_motor.comun import tex

ID = 'esp_fprima'
TITULO = 'El pivote modificado de Thomas'
SAL = 0x8D          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    n = 3
    f0 = rng.choice([2, 3, 4])
    f = [f0, rng.choice([3, 4, 5, 6, 7]), rng.choice([3, 4, 5, 6, 7])]
    # e[1] múltiplo de f[0] -> e'_2 entero -> f'_2 entero.
    e = [0, f0 * rng.choice([-2, -1, 1, 2]), rng.choice([-2, -1, 1, 2])]
    g = [rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(2)] + [0]
    r = [rng.choice([-5, -4, -3, 3, 4, 5]) for _ in range(n)]

    fp, _ = ref.thomas_descomposicion(e, f, g, r)
    esperado = sp.nsimplify(fp[1])

    # Red de seguridad: la respuesta tiene que ser un entero escribible a mano.
    if not esperado.is_Integer:
        raise AssertionError(f'f\'_2 salió {esperado}, no entero')

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            'Para el sistema tridiagonal con\n\n'
            f'$$e = {tex([e])}, \\qquad f = {tex([f])}, \\qquad '
            f'g = {tex([g])}$$\n\n'
            '**¿cuánto vale $f\'_2$**, el segundo pivote modificado del '
            'algoritmo de Thomas?'
        ),
        'esperado': int(esperado),
        'ayuda': r"$e'_2 = e_2/f_1$ y $f'_2 = f_2 - e'_2\,g_1$. Recuerda que "
                 r"$f_1$ ya está modificado: en la primera fila $f'_1 = f_1$.",
        'datos': {'e': e, 'f': f, 'g': g, 'r': r, 'fprima': [str(v) for v in fp]},
    }
