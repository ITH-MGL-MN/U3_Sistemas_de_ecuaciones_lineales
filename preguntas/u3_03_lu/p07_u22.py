"""Pregunta 7 — El segundo pivote  ·  id: lu_u22

Qué evalúa: entender que la diagonal de U son los pivotes que va dejando la
eliminación, y calcular el segundo a mano.

Se construye ``A = L @ U`` con ``L`` unitaria inferior entera y ``U`` con
diagonal entera distinta de cero, así que ``u22`` es un entero.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref
from mn_motor.comun import tex

ID = 'lu_u22'
TITULO = 'El segundo pivote de U'
SAL = 0x6B          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    U = sp.zeros(3, 3)
    for i in range(3):
        U[i, i] = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        for j in range(i + 1, 3):
            U[i, j] = rng.randint(-3, 3)

    L = sp.eye(3)
    for i in range(3):
        for j in range(i):
            L[i, j] = rng.choice([-2, -1, 1, 2])

    A = L * U
    if A.det() == 0:                      # u33 podría salir 0: no sirve
        raise AssertionError('matriz singular; cambia la semilla')

    _, U_ref = ref.lu_doolittle(A)
    esperado = int(U_ref[1][1])

    if esperado != int(U[1, 1]):
        raise AssertionError('el pivote calculado no es el de diseño')

    return {
        'tipo': 'numero',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Para la matriz\n\n$$\\mathbf{{A}} = {tex(A.tolist())}$$\n\n'
            '**¿cuánto vale $u_{22}$**, el segundo pivote de la '
            'factorización $\\mathbf{A} = \\mathbf{L}\\mathbf{U}$?'
        ),
        'esperado': esperado,
        'ayuda': 'Es el elemento $(2,2)$ que queda después de eliminar $x_1$ '
                 'del segundo y tercer renglón: $u_{22} = a_{22} - m_{21}a_{12}$.',
        'datos': {'A': A.tolist(), 'U': U.tolist()},
    }
