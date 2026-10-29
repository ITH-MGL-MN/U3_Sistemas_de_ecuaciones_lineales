"""Constantes del motor: qué cuaderno se califica y dónde está el repositorio.

Todo lo que cambia de un cuaderno a otro vive aquí y en su carpeta de
``preguntas/``. Nada de esto depende del archivo que se esté ejecutando, porque
el motor también corre desde el blob empaquetado, donde no existe ``__file__``.
"""
import os

# ---------------------------------------------------------------------
# Qué se califica. tools/build_grader.py sobreescribe estos dos valores al
# empaquetar el blob de cada cuaderno, así que aquí solo están los de por
# defecto (Cuaderno 01) para cuando se corre desde el repositorio.
# ---------------------------------------------------------------------
CUADERNO = 'u3_01_algebra_lineal'
TAREA_ID = 'U3_01_Algebra_Lineal'

# Envíos permitidos al backend. Lo impone el Apps Script (procesarTarea.gs);
# este valor solo sirve para avisar al alumno antes de gastar el último.
MAX_INTENTOS = 5


def raiz():
    """Carpeta del repositorio (la que tiene config/config.yaml).

    Se busca en cada llamada y no al importar, para que el cuaderno pueda
    cambiar de carpeta sin recargar el módulo.
    """
    # 1) La variable de entorno manda (útil para pruebas).
    pista = os.environ.get('U3_REPO')
    if pista and os.path.isdir(pista):
        return os.path.abspath(pista)
    # 2) Subir desde la carpeta de este archivo (modo módulos).
    for base in (os.path.dirname(os.path.abspath(__file__)), os.getcwd()):
        b = base
        for _ in range(6):
            if os.path.exists(os.path.join(b, 'config', 'config.yaml')):
                return b
            padre = os.path.dirname(b)
            if padre == b:
                break
            b = padre
    return os.getcwd()
