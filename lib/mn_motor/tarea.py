"""Armado de la tarea de un alumno y estado de la sesión.

La lista de preguntas NO está aquí: vive en ``preguntas/<cuaderno>/__init__.py``.
Este módulo solo las pide, les pasa la semilla del alumno y guarda el resultado
en ``MI_TAREA``.
"""
from importlib import import_module

import mn_motor.ajustes as ajustes
import mn_motor.comun as comun


def preguntas_del_cuaderno(semilla, cuaderno=None):
    """Construye todas las preguntas del cuaderno en el orden del índice.

    Cada elemento de ``PREGUNTAS`` cumple el mismo contrato: tiene un método
    ``construir(semilla)`` que devuelve el dict de una pregunta.
    """
    nombre = cuaderno or ajustes.CUADERNO
    try:
        indice = import_module(f'preguntas.{nombre}')
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f'No encuentro el índice de preguntas del cuaderno {nombre!r}.\n'
            f'  Debería estar en preguntas/{nombre}/__init__.py\n'
            f'  Detalle: {exc}'
        ) from exc
    return [pregunta.construir(semilla) for pregunta in indice.PREGUNTAS]


def generar_tarea(alumno_id, nombre=''):
    """Arma la tarea del alumno: preguntas sembradas, respuestas y widgets.

    Llamarla dos veces con el mismo correo devuelve exactamente lo mismo.
    """
    if alumno_id is None:
        raise RuntimeError('Necesito tu correo institucional para generar la tarea.')

    semilla = comun.semilla_de(alumno_id)
    preguntas = preguntas_del_cuaderno(semilla)

    return _activar({
        'alumno_id': alumno_id,
        'nombre': nombre,
        'nc': comun.extraer_nc(alumno_id),
        'tarea': ajustes.TAREA_ID,
        'cuaderno': ajustes.CUADERNO,
        'semilla': semilla,
        'preguntas': preguntas,
        'respuestas': [None] * len(preguntas),
        'widgets': [None] * len(preguntas),
    })


def ver_preguntas(tarea=None):
    """Lista las preguntas con su estado, sin revelar ninguna respuesta."""
    t = tarea if tarea is not None else tarea_activa()
    for i, q in enumerate(t['preguntas'], 1):
        estado = '✅ contestada' if t['respuestas'][i - 1] is not None else '⬜ pendiente'
        print(f'{i:>2}. [{q["tipo"]:>6}] {q["titulo"]:<34} {estado}')
    print(f'\n{len(t["preguntas"])} preguntas · cuaderno {t["cuaderno"]}')


# ---------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------

_ACTIVA = {'tarea': None}


def tarea_activa():
    t = _ACTIVA['tarea']
    if t is None:
        raise RuntimeError(
            'Primero ejecuta la celda de identificación: '
            'MI_TAREA = generar_tarea(alumno_id, nombre)')
    return t


def _activar(t):
    _ACTIVA['tarea'] = t
    return t
