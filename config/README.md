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

Las calificaciones de laboratorio usan la acción estándar `guardar`
(la misma de `procesarTarea.gs`), con `tarea = "U3_02_Laboratorios"`.

## 5. Verificar

Desde el Cuaderno 03, con el backend configurado:

```python
res = _post("u3_temas")
print(len(res["temas"]), "casos disponibles")
```

Debe imprimir `17 casos disponibles`.
