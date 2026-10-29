"""Preguntas de opción múltiple escritas en Markdown.

El enunciado y las opciones viven en un ``.md`` para que se puedan leer y
corregir sin tocar Python. Este módulo solo lo traduce a la estructura que
entiende el motor.

Formato del archivo (``---`` delimita la cabecera YAML)::

    ---
    id: alg_01
    titulo: Producto matricial vs elemento a elemento
    ---

    En la biblioteca del curso, **¿qué hace el operador `@`**?

    - [ ] El producto matricial (fila por columna)
    - [x] El producto elemento a elemento
    - [ ] La traspuesta del producto

La opción correcta se marca con ``[x]``: no hay índices que contar, así que no
hay forma de equivocarse al editar. Hace falta EXACTAMENTE una marcada.

Variables: si el enunciado cambia según el alumno, se pasan con
``variables(semilla)`` y se escriben en el .md entre dobles llaves, p. ej.
``La matriz {{A}} tiene...``.
"""
import random
import re

import yaml

import mn_motor.recursos as recursos


class PreguntaMarkdown:
    """Una pregunta de opción múltiple que se lee de un archivo .md."""

    def __init__(self, ruta, variables=None):
        self.ruta = ruta
        self.variables = variables
        self._cache = None

    # -- lectura -------------------------------------------------------
    def _leer(self):
        if self._cache is not None:
            return self._cache
        texto = recursos.leer(self.ruta)
        cabecera, cuerpo = _separar_cabecera(texto, self.ruta)
        if 'id' not in cabecera:
            raise ValueError(f'{self.ruta}: falta "id" en la cabecera')
        if 'titulo' not in cabecera:
            raise ValueError(f'{self.ruta}: falta "titulo" en la cabecera')
        enunciado, opciones, correcta = _separar_cuerpo(cuerpo, self.ruta)
        self._cache = {
            'id': cabecera['id'],
            'titulo': cabecera['titulo'],
            'enunciado': enunciado,
            'opciones': opciones,
            'correcta': correcta,
            'ayuda': cabecera.get('ayuda'),
        }
        return self._cache

    # -- contrato de una pregunta --------------------------------------
    def construir(self, semilla):
        """Devuelve el dict de la pregunta, con las opciones ya barajadas."""
        base = self._leer()
        valores = self.variables(semilla) if self.variables else {}

        enunciado = _sustituir(base['enunciado'], valores, self.ruta)
        opciones = [_sustituir(o, valores, self.ruta) for o in base['opciones']]
        buena = opciones[base['correcta']]

        # Barajar sin que se repita el orden entre alumnos. Como la respuesta
        # se guarda por índice, hay que reubicar también cuál es la buena.
        random.Random(semilla ^ 0x5F5F).shuffle(opciones)

        return {
            'tipo': 'mcq',
            'id': base['id'],
            'titulo': base['titulo'],
            'enunciado': enunciado,
            'opciones': opciones,
            'esperado': opciones.index(buena),
            'ayuda': base['ayuda'],
        }


def desde_markdown(ruta, variables=None):
    """Atajo para declarar una pregunta en el índice del cuaderno."""
    return PreguntaMarkdown(ruta, variables=variables)


# ---------------------------------------------------------------------
# Parseo
# ---------------------------------------------------------------------

def _separar_cabecera(texto, ruta):
    """Separa la cabecera YAML del cuerpo en Markdown."""
    if not texto.lstrip().startswith('---'):
        raise ValueError(f'{ruta}: debe empezar con una cabecera --- ... ---')
    partes = texto.split('---', 2)
    if len(partes) < 3:
        raise ValueError(f'{ruta}: la cabecera --- no está cerrada')
    cabecera = yaml.safe_load(partes[1]) or {}
    return cabecera, partes[2]


def _separar_cuerpo(cuerpo, ruta):
    """Devuelve (enunciado, opciones, índice de la correcta)."""
    lineas = cuerpo.splitlines()
    opciones, correcta = [], None
    i = 0
    while i < len(lineas):
        m = re.match(r'^\s*-\s*\[( |x|X)\]\s*(.+?)\s*$', lineas[i])
        if m:
            if m.group(1).strip().lower() == 'x':
                if correcta is not None:
                    raise ValueError(
                        f'{ruta}: hay más de una opción marcada con [x]')
                correcta = len(opciones)
            opciones.append(m.group(2))
            lineas[i] = None
        i += 1

    if len(opciones) < 2:
        raise ValueError(f'{ruta}: necesita al menos 2 opciones "- [ ] ..."')
    if correcta is None:
        raise ValueError(f'{ruta}: ninguna opción está marcada con [x]')

    enunciado = '\n'.join(l for l in lineas if l is not None).strip()
    if not enunciado:
        raise ValueError(f'{ruta}: el enunciado quedó vacío')
    return enunciado, opciones, correcta


def _sustituir(texto, valores, ruta):
    """Reemplaza ``{{clave}}`` por su valor. Falla si falta alguna."""
    for clave in set(re.findall(r'\{\{(\w+)\}\}', texto)):
        if clave not in valores:
            raise ValueError(
                f'{ruta}: el texto usa {{{{{clave}}}}} pero variables() no la define')
        texto = texto.replace('{{' + clave + '}}', str(valores[clave]))
    return texto
