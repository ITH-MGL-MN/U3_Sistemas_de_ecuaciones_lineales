"""Calificación local: convierte las respuestas del alumno en 1/0.

No envía nada; para eso está ``envio.py``.
"""
import mn_motor.comun as comun
import mn_motor.tarea as tarea


def acierto(q, respuesta):
    """¿La respuesta de esta pregunta es correcta? Devuelve 1 o 0."""
    if respuesta is None:
        return 0
    if q['tipo'] == 'mcq':
        try:
            return 1 if int(respuesta) == int(q['esperado']) else 0
        except (TypeError, ValueError):
            return 0
    if q['tipo'] == 'matriz':
        return 1 if comun.matriz_igual(respuesta, q['esperado']) else 0
    if q['tipo'] == 'numero':
        return 1 if comun.numero_igual(respuesta, q['esperado']) else 0
    raise ValueError(f"Tipo de pregunta desconocido: {q['tipo']!r}")


def calificar(tarea_=None):
    """Califica sin enviar. Devuelve ``(puntos, maximo)``."""
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    aciertos = [acierto(q, t['respuestas'][i]) for i, q in enumerate(t['preguntas'])]
    t['ultimo_calculo'] = aciertos

    puntos, maximo = sum(aciertos), len(aciertos)
    print('Resultados:', ' '.join('✅' if a else '❌' for a in aciertos))
    print(f'Puntaje: {puntos} / {maximo}')

    pendientes = [i + 1 for i, r in enumerate(t['respuestas']) if r is None]
    if pendientes:
        print('⚠️ Sin contestar:', pendientes)
    return puntos, maximo
