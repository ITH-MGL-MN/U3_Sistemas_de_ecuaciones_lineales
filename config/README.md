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

> El id viaja en el payload desde `TAREA_ID` (en `lib/mn_motor/ajustes.py`), **no**
> se lee de `config.yaml`. Si se leyera, el Cuaderno 01 escribiría en la pestaña
> del Cuaderno 02.

## 5. El motor de calificación

El cuaderno **no** trae las respuestas: se las pide a un motor empaquetado.

| Ruta | ¿Va al repo público? | Para qué |
|---|---|---|
| [`lib/mn_motor/`](../lib/mn_motor/) | ❌ no (`gitignore`) | el framework: mostrar, calificar, enviar |
| [`preguntas/`](../preguntas/) | ❌ no (`gitignore`) | las preguntas de cada cuaderno (una carpeta por cuaderno) |
| `grader/<cuaderno>.txt` | ✅ sí | **lo que usa el alumno** (base64 + zlib, con motor y preguntas dentro) |
| [`tools/build_grader.py`](../tools/build_grader.py) | ✅ sí | genera los blobs |

**Un cuaderno = una carpeta en `preguntas/` = un blob en `grader/`.**

| Cuaderno | Carpeta | Blob | Pestaña (`tarea`) |
|---|---|---|---|
| 01 · Álgebra Lineal | `u3_01_algebra_lineal` | `grader/u3_01_algebra_lineal.txt` | `U3_01_Algebra_Lineal` |
| 02 · Eliminación Gaussiana | `u3_02_gaussiana` | `grader/u3_02_gaussiana.txt` | `U3_02_Eliminacion_Gaussiana` |
| 03 · Descomposición LU | `u3_03_lu` | `grader/u3_03_lu.txt` | `U3_03_Descomposicion_LU` |
| 04 · Especiales e iterativos | `u3_04_especiales_iterativos` | `grader/u3_04_especiales_iterativos.txt` | `U3_04_Especiales_Iterativos` |

Cada cuaderno declara el suyo en su primera celda con
`usar_cuaderno("u3_02_gaussiana", "U3_02_Eliminacion_Gaussiana")`. Eso fija a la
vez qué preguntas se cargan y en qué pestaña se guarda la calificación.

> La ofuscación no es cifrado: frena el vistazo casual, no a quien se proponga
> descomprimirlo. El anti-copia de verdad son **los datos sembrados por NC**: a
> cada alumno le tocan matrices distintas, así que copiar la respuesta del
> compañero da mal.

### Dónde se toca cada cosa

| Quiero cambiar… | Voy a |
|---|---|
| una pregunta | `preguntas/<cuaderno>/pNN_*.py` (o su `.md` si es de opción múltiple) |
| el orden o el número de preguntas | `preguntas/<cuaderno>/__init__.py` — es el índice |
| cómo se muestran las preguntas | `lib/mn_motor/ui.py` |
| cómo se califican | `lib/mn_motor/califica.py` |
| el envío al backend | `lib/mn_motor/envio.py` |

### Reconstruir los blobs

Cada vez que cambies el motor o cualquier pregunta:

```powershell
.\.venv\Scripts\python.exe tools\build_grader.py
```

Sin `--cuaderno` regenera **todos** los que tengan carpeta de preguntas. Para uno
solo:

```powershell
.\.venv\Scripts\python.exe tools\build_grader.py --cuaderno u3_02_gaussiana
```

El script, **antes** de escribir nada, carga el paquete en memoria (igual que lo
hará el alumno), genera una tarea, la contesta toda bien y comprueba que dé
puntos completos. Si algo falla, no sobreescribe el blob. **Si no lo corres, el
alumno sigue recibiendo la versión vieja.**

### Modos de carga

| `MODO_MOTOR` | Cuándo | Qué hace |
|---|---|---|
| `"modulos"` | tu computadora | importa `lib/mn_motor/` y `preguntas/`; Pylance lo entiende (F12, autocompletado, puntos de ruptura) |
| `"blob"` | Colab (forzado) | descomprime `grader_ofuscado.txt` |

En un clon sin `preguntas/` el cuaderno cae solo a `"blob"`.

### ⚠️ Al probar, no ejecutes la celda de envío

`enviar(alumno_id)` **manda de verdad** al Apps Script y consume uno de los 5
intentos del NC. Para probar el cuaderno de punta a punta, borra o salta esa
celda, o usa un NC de prueba. `calificar()` no envía nada: es seguro.

> El límite vive en `procesarTarea.gs` (`MAX_INTENTOS`). Si lo cambias ahí,
> cámbialo también en `lib/mn_motor/ajustes.py` y en `config.yaml`, que solo
> sirven para avisar al alumno antes de gastar el último.

## 6. Verificar

Desde el Cuaderno 03, con el backend configurado:

```python
res = _post("u3_temas")
print(len(res["temas"]), "casos disponibles")
```

Debe imprimir `17 casos disponibles`.
