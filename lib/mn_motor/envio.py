"""Envío de la calificación al backend de Apps Script.

Si no hay URL y token configurados, el motor NO falla: avisa y deja el
resultado local. Así el cuaderno se puede usar sin backend mientras el profesor
no despliegue la hoja.
"""
import json
import os

import mn_motor.ajustes as ajustes
import mn_motor.califica as califica
import mn_motor.comun as comun
import mn_motor.tarea as tarea

try:
    import yaml
except ImportError:
    yaml = None


def configuracion():
    """URL, token y pestaña de destino. Se lee en cada llamada (no al importar)."""
    datos = {}
    ruta = os.path.join(ajustes.raiz(), 'config', 'config.yaml')
    if os.path.exists(ruta) and yaml is not None:
        try:
            with open(ruta, encoding='utf-8') as f:
                datos = yaml.safe_load(f) or {}
        except Exception:
            datos = {}
    ev = datos.get('evaluacion') or {}
    return {
        'url': os.environ.get('U3_APPS_URL') or ev.get('apps_script_url', '') or '',
        'token': os.environ.get('U3_TOKEN') or ev.get('webhook_token', '') or '',
        # La pestaña la define el cuaderno que envía, no config.yaml: si se
        # leyera de ahí, el Cuaderno 01 escribiría en la pestaña del 02.
        'tarea': ajustes.TAREA_ID,
    }


def _post(payload):
    import urllib.request
    cfg = configuracion()
    req = urllib.request.Request(
        cfg['url'],
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode('utf-8'))
    if resp.get('status') != 'ok':
        raise RuntimeError(resp.get('message', 'Error del backend'))
    return resp.get('data', {})


def enviar(alumno_id, tarea_=None):
    """Envía la calificación. Respeta el máximo de intentos del backend."""
    t = tarea_ if tarea_ is not None else tarea.tarea_activa()
    cfg = configuracion()
    nc = comun.extraer_nc(alumno_id) or str(alumno_id)

    aciertos = t.get('ultimo_calculo')
    if aciertos is None:
        aciertos = [califica.acierto(q, t['respuestas'][i])
                    for i, q in enumerate(t['preguntas'])]
    puntos, maximo = sum(aciertos), len(aciertos)

    if not cfg['url'] or not cfg['token']:
        print('ℹ️ Backend sin configurar: la calificación NO se envió.')
        print('   El profesor debe llenar config/config.yaml (URL y token).')
        print(f'   Resultado local: {puntos} / {maximo}')
        return None

    try:
        res = _post({
            'accion': 'guardar',
            'token': cfg['token'],
            'NC': nc,
            'tarea': cfg['tarea'],
            'respuestas': aciertos,
            'pesos': [1] * maximo,
            'maxPuntos': 1,
        })
    except Exception as exc:
        print('⛔ No se pudo enviar:', exc)
        return None

    _guardar_historial(nc, {
        'intento': res.get('intento'),
        'total': res.get('total'),
        'puntos': puntos,
        'maximo': maximo,
    })

    print(f"✅ Enviado. Intento {res.get('intento')} · "
          f"Total {res.get('total', 0):.1f}/100")
    print(f'   Respuestas: {aciertos}')
    if (res.get('intento') or 0) >= ajustes.MAX_INTENTOS:
        print(f'   ⚠️ Este fue tu último intento (máximo {ajustes.MAX_INTENTOS}).')
    return res


def consultar_calificacion(alumno_id=None):
    """Pregunta al backend cuántos intentos llevas."""
    if alumno_id is None:
        alumno_id = tarea.tarea_activa()['alumno_id']
    cfg = configuracion()
    if not cfg['url'] or not cfg['token']:
        print('ℹ️ Backend sin configurar: no hay nada que consultar.')
        return None

    nc = comun.extraer_nc(alumno_id) or str(alumno_id)
    try:
        datos = _post({'accion': 'intento', 'token': cfg['token'],
                       'NC': nc, 'tarea': cfg['tarea']})
    except Exception as exc:
        print('⛔ No se pudo consultar:', exc)
        return None

    if not datos:
        print(f'NC {nc}: todavía no hay envíos registrados.')
        return datos

    intentos = datos.get('intento', 0)
    print(f"NC {nc}: {intentos} de {ajustes.MAX_INTENTOS} intentos usados · "
          f"puntaje {datos.get('total', 0)}")
    print(f'   Intentos restantes: {max(0, ajustes.MAX_INTENTOS - intentos)}')
    return datos


def ultimo_envio(alumno_id):
    """Muestra lo último que quedó registrado en este equipo."""
    nc = comun.extraer_nc(alumno_id) or str(alumno_id)
    h = _leer_historial().get(nc)
    if not h:
        print('No hay envíos registrados en este equipo.')
        return None
    print(f"NC {nc}: intento {h['intento']} · {h['puntos']}/{h['maximo']} "
          f"({h['total']:.1f}/100)")
    return h


# ---------------------------------------------------------------------
# Historial local (solo para no perder el rastro si falla la red)
# ---------------------------------------------------------------------

def _historial_path():
    return os.path.join(ajustes.raiz(), 'config', '.envios.json')


def _leer_historial():
    ruta = _historial_path()
    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _guardar_historial(nc, registro):
    h = _leer_historial()
    h[nc] = registro
    try:
        with open(_historial_path(), 'w', encoding='utf-8') as f:
            json.dump(h, f, ensure_ascii=False, indent=1)
    except Exception:
        pass
