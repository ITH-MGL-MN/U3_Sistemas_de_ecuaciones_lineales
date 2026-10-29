"""mn_motor — motor de calificación de los cuadernos de Métodos Numéricos.

El cuaderno solo ve los nombres de ``__all__``. Todo lo demás (qué preguntas
hay, cómo se siembran, cómo se comparan las respuestas) vive en:

    lib/mn_motor/            el framework, igual para todos los cuadernos
    preguntas/<cuaderno>/    las preguntas de UN cuaderno

Flujo típico en el cuaderno::

    MI_TAREA = generar_tarea(alumno_id, nombre)   # una sola vez
    pregunta(1)                                   # muestra la pregunta 1
    puntos, maximo = calificar()                  # sin enviar
    enviar(alumno_id)                             # envía (máx. 2 intentos)

Dónde tocar cada cosa:

    una pregunta concreta      -> preguntas/<cuaderno>/pNN_*.py  (o su .md)
    el orden de las preguntas  -> preguntas/<cuaderno>/__init__.py
    cómo se muestran           -> lib/mn_motor/ui.py
    cómo se califican          -> lib/mn_motor/califica.py
    el envío al backend        -> lib/mn_motor/envio.py
"""
from mn_motor.ajustes import CUADERNO, MAX_INTENTOS, TAREA_ID
from mn_motor.califica import calificar
from mn_motor.comun import extraer_nc, semilla_de
from mn_motor.envio import consultar_calificacion, enviar, ultimo_envio
from mn_motor.tarea import generar_tarea, preguntas_del_cuaderno, ver_preguntas
from mn_motor.ui import pregunta

__all__ = [
    'consultar_calificacion',
    'calificar',
    'cuaderno',
    'enviar',
    'extraer_nc',
    'generar_tarea',
    'pregunta',
    'semilla_de',
    'ultimo_envio',
    'ver_preguntas',
    'MAX_INTENTOS',
]


def cuaderno():
    """Nombre de la carpeta de preguntas que se está usando."""
    import mn_motor.ajustes as ajustes
    return ajustes.CUADERNO
