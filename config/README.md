# 🔌 Configuración del backend (Apps Script)

Los cuadernos **03** (registro de equipos) y **02** (calificación de laboratorios)
se conectan a una hoja de Google Sheets mediante un **Apps Script**.

## 1. Preparar la hoja de cálculo

La hoja debe tener una pestaña **`Resultados`** con al menos estas columnas:

| NC | Apellido | Nombre |
|---|---|---|
| 21340001 | Pérez | Ana |

*(Es la misma hoja de roster que ya usa el curso.)*

## 2. Instalar el backend

1. Abre el proyecto de Apps Script de la hoja (`Extensiones → Apps Script`).
2. Copia el archivo [`App Script/proyectos_u3.gs`](../../../../App%20Script/proyectos_u3.gs)
   junto a `doPost.gs` y `procesarTarea.gs`.
3. En `doPost.gs`, dentro del `try`, añade **antes** del flujo de tarea normal:

   ```javascript
   // ========== U3: registro de equipos y asignación de caso ==========
   if (data.accion && data.accion.indexOf('u3_') === 0) {
     return u3Handle(data);
   }
   ```

4. Ejecuta `setupWebhookToken()` una vez y copia el token que imprime.
5. Implementa (`Implementar → Nueva implementación → Aplicación web`),
   con acceso **"Cualquier persona"** y ejecutar como **"Yo"**.
6. Copia la URL que termina en `/exec`.

## 3. Conectar los cuadernos

En la **primera celda** del Cuaderno 02 y del Cuaderno 03, llena:

```python
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfy.../exec"
WEBHOOK_TOKEN   = "el-token-que-imprimio-setupWebhookToken"
```

> ⚠️ No subas el token al repositorio público. Los cuadernos lo piden al alumno
> o lo inyecta el profesor en su copia de Colab.

## 4. Acciones disponibles

| Acción | Payload | Devuelve |
|---|---|---|
| `u3_temas` | `{}` | catálogo de los 17 casos (bloque, tamaño, equipos registrados) |
| `u3_alumnos` | `{}` | roster `[{nc, nombre}]` |
| `u3_registrar` | `{NC_Jefe, integrantes:[nc,...]}` | equipo con caso **asignado determinísticamente** |
| `u3_equipo` | `{NC}` | estado del equipo (o `null`) |
| `u3_eliminar` | `{NC_Jefe, confirmar:true}` | borra el equipo (solo para corregir) |

Las calificaciones usan la acción estándar `guardar` (la misma de
`procesarTarea.gs`). El campo `tarea` del payload es el **id del cuaderno** que
envía, y define la pestaña donde se guarda:

| Cuaderno | `tarea` |
|---|---|
| 01 · Álgebra Lineal | `U3_01_Algebra_Lineal` |
| 02 · Laboratorios de Métodos | `U3_02_Laboratorios` |

> El id viaja en el payload desde la constante `_TAREA_ID` del motor, **no** se
> lee de `config.yaml`. Si se leyera, el Cuaderno 01 escribiría en la pestaña
> del Cuaderno 02.

## 5. El motor de calificación

El cuaderno **no** trae las respuestas: se las pide a un motor empaquetado.

| Archivo | ¿Va al repo público? | Para qué |
|---|---|---|
| [`lib/grader_u3.py`](../lib/grader_u3.py) | ❌ no (`gitignore`) | fuente del motor; se edita aquí |
| [`config/preguntas_u3.yaml`](preguntas_u3.yaml) | ❌ no (`gitignore`) | banco de opción múltiple |
| `grader_ofuscado.txt` | ✅ sí | **lo que usa el alumno** (base64 + zlib, con el banco incrustado) |
| [`tools/build_grader.py`](../tools/build_grader.py) | ✅ sí | genera el blob |

> La ofuscación no es cifrado: frena el vistazo casual, no a quien se proponga
> descomprimirlo. El anti-copia de verdad son **los datos sembrados por NC**: a
> cada alumno le tocan matrices distintas, así que copiar la respuesta del
> compañero da mal.

### Reconstruir el blob

Cada vez que cambies el motor o el banco:

```powershell
.\.venv\Scripts\python.exe tools\build_grader.py
```

El script verifica que el motor compile, que al ejecutarse incruste el banco y
que el blob se descomprima igual antes de darlo por bueno. **Si no lo corres, el
alumno sigue recibiendo la versión vieja.**

### Modos de carga

| `MODO_MOTOR` | Cuándo | Qué hace |
|---|---|---|
| `"modulos"` | tu computadora | importa `lib/grader_u3.py`; Pylance lo entiende (F12, autocompletado, puntos de ruptura) |
| `"blob"` | Colab (forzado) | descomprime `grader_ofuscado.txt` |

En un clon sin `lib/grader_u3.py` el cuaderno cae solo a `"blob"`.

## 6. Verificar

Desde el Cuaderno 03, con el backend configurado:

```python
res = _post("u3_temas")
print(len(res["temas"]), "casos disponibles")
```

Debe imprimir `17 casos disponibles`.
