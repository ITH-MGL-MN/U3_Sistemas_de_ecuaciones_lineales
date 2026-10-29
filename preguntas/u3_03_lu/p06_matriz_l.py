"""Pregunta 6 — Escribir la matriz L  ·  id: lu_matriz_L

Qué evalúa: sacar los multiplicadores de una eliminación y colocarlos en su
lugar (la parte que LU agrega respecto a Gauss).

Cómo se garantiza que la respuesta sea ENTERA: se construye ``A = L @ U`` con
``L`` unitaria inferior y ``U`` unitaria superior, ambas enteras. Al eliminar
``A`` sin pivoteo se recupera exactamente ``U`` y los multiplicadores son las
entradas de ``L``, así que la respuesta es la ``L`` de diseño.
"""
import random

import sympy as sp

from mn_motor import solvers_u3 as ref
from mn_motor.comun import tex

ID = 'lu_matriz_L'
TITULO = 'Escribe la matriz L'
SAL = 0x3A          # semilla propia de esta pregunta


def construir(semilla):
    rng = random.Random(semilla ^ SAL)

    U = sp.eye(3)
    for i in range(3):
        for j in range(i + 1, 3):
            U[i, j] = rng.randint(-3, 3)

    L = sp.eye(3)
    for i in range(3):
        for j in range(i):
            L[i, j] = rng.choice([-3, -2, -1, 1, 2, 3])

    A = L * U
    L_ref, U_ref = ref.lu_doolittle(A)

    # Red de seguridad: la factorización tiene que devolver la L y la U usadas.
    if L_ref != L.tolist() or U_ref != U.tolist():
        raise AssertionError('la factorización no recuperó la L de diseño')

    return {
        'tipo': 'matriz',
        'id': ID,
        'titulo': TITULO,
        'enunciado': (
            f'Se factoriza $\\mathbf{{A}} = \\mathbf{{L}}\\mathbf{{U}}$ '
            f'(Doolittle, unos en la diagonal de $\\mathbf{{L}}$) con\n\n'
            f'$$\\mathbf{{A}} = {tex(A.tolist())}$$\n\n'
            '**Escribe la matriz $\\mathbf{L}$.**'
        ),
        'esperado': L.tolist(),
        'ayuda': 'Elimina como siempre y ve guardando cada multiplicador '
                 '$m_{ik}$ en la posición $(i,k)$ de una matriz que empieza '
                 'siendo la identidad. Escribe [[a,b,c],[d,e,f],[g,h,i]].',
        'datos': {'A': A.tolist(), 'U': U.tolist()},
    }
