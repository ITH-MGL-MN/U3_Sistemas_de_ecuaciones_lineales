"""Práctica libre: prueba TU función contra el ejemplo del enunciado.

No es la calificación: aquí no hay puntos ni intentos. Sirve para que el alumno
sepa si su método ya funciona antes de enviar. Los casos que cuentan son los
ocultos de la pregunta calificable.

La referencia se calcula aquí dentro y **no se muestra**: solo el veredicto.
"""
import inspect

import mn_motor.califica as califica
import mn_motor.comun as comun
import mn_motor.tarea as tarea


def practica(id_pregunta, tarea_=None):
    """Prueba la función de la pregunta ``id_pregunta`` con su ejemplo visible.

    Se llama desde el cuaderno después de definir la función::

        practica('prog_eliminar')

    Devuelve True/False (útil para probar), o None si falta algo.
    """
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    q = next((x for x in t['preguntas'] if x['id'] == id_pregunta), None)
    if q is None:
        print(f'⚠️ No hay ninguna pregunta con id {id_pregunta!r} en este cuaderno.')
        return None
    if q['tipo'] != 'funcion':
        print(f'⚠️ La pregunta {id_pregunta!r} no es de programar.')
        return None

    marco_de_arriba = inspect.currentframe()
    if marco_de_arriba is None or marco_de_arriba.f_back is None:
        print('⚠️ No pude leer las variables del cuaderno; ejecuta esto desde Colab.')
        return None
    fn = califica.funcion_del_alumno(marco_de_arriba.f_back.f_globals, q['funcion'])
    if fn is None:
        print(f'⚠️ Todavía no defines tu función `{q["funcion"]}`. '
              f'Escríbela arriba y vuelve a ejecutar esta celda.')
        return None

    entrada, esperado = q['ejemplo']
    print(f'Probando `{q["funcion"]}` con el ejemplo del enunciado…')
    try:
        res = fn(*entrada)
    except NotImplementedError:
        print('⏳ Tu función todavía tiene `raise NotImplementedError`.')
        return False
    except Exception as exc:
        print(f'⛔ Tu función lanzó {type(exc).__name__}: {exc}')
        return False

    if res is None:
        print('⏳ Tu función devolvió `None`: todavía no calcula nada.')
        return False

    if comun.matriz_igual(res, esperado):
        print('✅ Coincide con la referencia.')
        _mostrar(res)
        return True

    print('❌ Todavía no coincide. Tu resultado:')
    _mostrar(res)
    print('   Revisa el pseudocódigo del cuaderno y los índices '
          '(Python empieza en 0, el libro en 1).')
    return False


def _mostrar(valor):
    """Pinta el resultado del alumno, sin revelar la referencia."""
    from IPython.display import Math, display
    try:
        import sympy as sp
        m = sp.Matrix(valor)
        display(Math(sp.latex(m)))
    except Exception:
        print(valor)
