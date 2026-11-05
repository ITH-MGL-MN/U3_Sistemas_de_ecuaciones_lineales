"""Calificación local: convierte las respuestas del alumno en 1/0.

No envía nada; para eso está ``envio.py``.

Incluye el tipo de pregunta ``funcion``: la respuesta del alumno no es un texto,
sino una FUNCIÓN que programó. Se le busca por nombre en las variables del
cuaderno y se prueba con casos ocultos (sembrados por NC), igual que en la
tarea de U2.
"""
import inspect

import mn_motor.comun as comun
import mn_motor.tarea as tarea


def _marco_del_cuaderno(marco=None, saltos=2):
    """Variables globales de la celda del cuaderno (donde vive la función).

    Si no se pasa explícitamente, se sube ``saltos`` marcos en la pila hasta
    salir del motor.
    """
    if marco is not None:
        return marco
    f = inspect.currentframe()
    for _ in range(saltos):
        if f is None:
            return None
        f = f.f_back
    if f is None:
        return None
    return f.f_globals


def funcion_del_alumno(marco, nombre):
    """La función que escribió el alumno, o None si no existe todavía."""
    if marco is None:
        return None
    fn = marco.get(nombre) if isinstance(marco, dict) else getattr(marco, nombre, None)
    return fn if callable(fn) else None


def _llamar(fn, entrada, segundos=None):
    """Llama a la función del alumno con un LÍMITE DE TIEMPO opcional.

    Un alumno puede escribir `while error > tol:` sobre un sistema que no
    converge, y eso colgaría la calificación. Se corre en un hilo aparte y, si
    no termina a tiempo, se abandona y cuenta como fallo.

    OJO: un hilo de Python no se puede matar. Un `while True: pass` se queda
    girando y compite por el GIL, así que el límite se usa con un valor corto y
    sólo como red de seguridad (por omisión NO se pone: ver `tiempo_limite`).
    """
    if not segundos:
        return fn(*entrada)

    import threading

    caja = {}

    def _correr():
        try:
            caja['res'] = fn(*entrada)
        except BaseException as exc:      # noqa: BLE001 - se reporta como fallo
            caja['exc'] = exc

    hilo = threading.Thread(target=_correr, daemon=True)
    hilo.start()
    hilo.join(segundos)
    if hilo.is_alive():
        raise TimeoutError(f'tu función no terminó en {segundos:g} s '
                           f'(¿un ciclo que nunca acaba? Revisa max_iter.)')
    if 'exc' in caja:
        raise caja['exc']
    return caja.get('res')


def _desempaquetar(res, q):
    """Separa el valor calificable del conteo de iteraciones, si lo hay.

    Las preguntas de métodos iterativos piden ``return x, iteraciones``. Aquí
    se acepta tanto eso como devolver solo el vector: si el segundo elemento
    es un número, se toma como conteo y se comprueba que respete ``max_iter``.
    """
    if q.get('salida') != 'matriz_iteraciones':
        return res, None
    if (isinstance(res, (tuple, list)) and len(res) == 2
            and isinstance(res[1], (int, float)) and not isinstance(res[1], bool)):
        return res[0], int(res[1])
    return res, None


def _acierto_funcion(q, marco):
    """¿La función del alumno pasa TODOS los casos ocultos? Devuelve 1 o 0."""
    fn = funcion_del_alumno(marco, q['funcion'])
    if fn is None:
        return 0
    segundos = q.get('tiempo_limite')      # None = sin limite
    tol = q.get('tol', 1e-6)
    maximo = q.get('max_iter')
    for entrada, esperado in q['casos']:
        try:
            res = _llamar(fn, entrada, segundos)
        except Exception:
            return 0
        valor, iteraciones = _desempaquetar(res, q)
        if valor is None or not comun.comparar(valor, esperado, tol=tol):
            return 0
        if maximo is not None and iteraciones is not None and iteraciones > maximo:
            return 0
    return 1


def acierto(q, respuesta, marco=None):
    """¿La respuesta de esta pregunta es correcta? Devuelve 1 o 0."""
    if q['tipo'] == 'funcion':
        return _acierto_funcion(q, marco)

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


def calificar(tarea_=None, marco=None):
    """Califica sin enviar. Devuelve ``(puntos, maximo)``."""
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    marco = _marco_del_cuaderno(marco)

    aciertos = [acierto(q, t['respuestas'][i], marco)
                for i, q in enumerate(t['preguntas'])]
    t['ultimo_calculo'] = aciertos

    puntos, maximo = sum(aciertos), len(aciertos)
    print('Resultados:', ' '.join('✅' if a else '❌' for a in aciertos))
    print(f'Puntaje: {puntos} / {maximo}')

    for i, q in enumerate(t['preguntas'], 1):
        if q['tipo'] == 'funcion' and not aciertos[i - 1]:
            _detalle_funcion(i, q, marco)

    pendientes = [i + 1 for i, r in enumerate(t['respuestas'])
                  if r is None and t['preguntas'][i]['tipo'] != 'funcion']
    if pendientes:
        print('⚠️ Sin contestar:', pendientes)
    return puntos, maximo


def _detalle_funcion(i, q, marco):
    """Explica por qué falló la función del alumno, caso por caso."""
    fn = funcion_del_alumno(marco, q['funcion'])
    if fn is None:
        print(f'   P{i}: no encuentro tu función `{q["funcion"]}`. '
              f'Defínela en el cuaderno (firma: {q.get("firma", "")}).')
        return
    print(f'   P{i}: `{q["funcion"]}` no pasó todos los casos:')
    for k, (entrada, esperado) in enumerate(q['casos'], 1):
        try:
            res = fn(*entrada)
        except Exception as exc:
            print(f'      caso {k}: ⛔ lanzó {type(exc).__name__}: {exc}')
            continue
        ok = res is not None and comun.comparar(res, esperado)
        print(f'      caso {k}: {"✅" if ok else "❌"}')
