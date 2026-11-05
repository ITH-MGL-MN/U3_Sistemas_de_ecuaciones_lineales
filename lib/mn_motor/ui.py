"""Mostrar una pregunta y recoger la respuesta del alumno.

El enunciado y las opciones se pintan con ``display(Markdown(...))`` para que
MathJax interprete el LaTeX. El widget NO muestra texto: solo las letras
``a``, ``b``, ``c``… porque los widgets de ipywidgets no interpretan Markdown y
el LaTeX saldría literal.

La respuesta se guarda **sola** en cuanto el alumno elige o escribe: si hubiera
que pulsar un botón por pregunta, quien se olvide de uno saca cero en esa
pregunta al calificar. El botón queda como confirmación explícita.
"""
import mn_motor.comun as comun
import mn_motor.tarea as tarea


def pregunta(n, tarea_=None):
    """Muestra la pregunta ``n`` (1..N) con su control de respuesta."""
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    if not 1 <= n <= len(t['preguntas']):
        raise ValueError(f'La pregunta {n} no existe (hay {len(t["preguntas"])})')

    from IPython.display import Markdown, display
    import ipywidgets as w

    q = t['preguntas'][n - 1]
    encabezado = f"### Pregunta {n} — {q['titulo']}\n\n{q['enunciado']}"

    if q['tipo'] == 'funcion':
        # Aquí no hay nada que teclear: la respuesta es la función que el
        # alumno definió unas celdas más arriba.
        display(Markdown(encabezado))
        display(Markdown(
            f"> 💻 **Esta respuesta no se teclea:** es la función "
            f"`{q['funcion']}` que definiste arriba.\n>\n"
            f"> Firma: `{q.get('firma', '')}`\n>\n"
            f"> Compruébala antes de enviar con `practica('{q['id']}')`."))
        if q.get('ayuda'):
            display(Markdown(f"> 💡 {q['ayuda']}"))
        return

    if q['tipo'] == 'mcq':
        letras = comun.letras(len(q['opciones']))
        cuerpo = '\n'.join(f'- **{l})** {o}' for l, o in zip(letras, q['opciones']))
        display(Markdown(f'{encabezado}\n\n{cuerpo}'))
        ctrl = w.RadioButtons(
            options=[(l, i) for i, l in enumerate(letras)],
            value=None,
            layout=w.Layout(width='100%'),
        )
    else:
        display(Markdown(encabezado))
        if q['tipo'] == 'matriz':
            ctrl = w.Text(placeholder='[[1,2,3],[4,5,6],[7,8,9]]',
                          continuous_update=False,      # guarda al salir del campo
                          layout=w.Layout(width='90%'))
        else:
            ctrl = w.Text(placeholder='escribe un número',
                          continuous_update=False,
                          layout=w.Layout(width='40%'))

    salida = w.Output()

    def _mensaje():
        valor = t['respuestas'][n - 1]
        with salida:
            salida.clear_output()
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                print(f'⚠️ La pregunta {n} sigue sin respuesta.')
                return
            if q['tipo'] == 'mcq':
                print(f'✅ Guardada: opción {comun.letra(int(valor))}.')
            else:
                print(f'✅ Guardada: {valor}')

    def _guardar(_=None):
        t['respuestas'][n - 1] = ctrl.value
        _mensaje()

    def _al_cambiar(change):
        """Se dispara en cuanto el alumno elige una opción o escribe."""
        t['respuestas'][n - 1] = change['new']
        _mensaje()

    ctrl.observe(_al_cambiar, names='value')
    boton = w.Button(description='Guardar', button_style='primary')
    boton.on_click(_guardar)
    t['widgets'][n - 1] = ctrl
    display(w.VBox([ctrl, boton, salida]))
    if q.get('ayuda'):
        display(Markdown(f"> 💡 {q['ayuda']}"))
