"""Lectura de recursos (los .md de las preguntas) en los dos modos de carga.

- Modo módulos (tu computadora): el archivo se lee del disco.
- Modo blob (Colab): el contenido viaja DENTRO del blob y se sirve desde
  ``EMPAQUETADOS``, porque en el clon del alumno los .md tampoco existen.

La clave es siempre la ruta relativa a la raíz del repositorio, escrita con
diagonal normal: ``preguntas/u3_01_algebra_lineal/alg_01.md``.
"""
import os

import mn_motor.ajustes as ajustes

# Lo llena el blob al cargarse. En modo módulos se queda vacío.
EMPAQUETADOS = {}


def leer(nombre):
    """Devuelve el texto del recurso ``nombre`` (ruta relativa al repositorio)."""
    if nombre in EMPAQUETADOS:
        return EMPAQUETADOS[nombre]

    ruta = os.path.join(ajustes.raiz(), *nombre.split('/'))
    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f'No encuentro el recurso {nombre!r}.\n'
            f'  Buscado en: {ruta}\n'
            f'  Si cambiaste de rama, el archivo pudo haberse borrado: '
            f'git checkout test -- preguntas/'
        )
    with open(ruta, encoding='utf-8') as f:
        return f.read()


def existe(nombre):
    return nombre in EMPAQUETADOS or os.path.exists(
        os.path.join(ajustes.raiz(), *nombre.split('/')))
