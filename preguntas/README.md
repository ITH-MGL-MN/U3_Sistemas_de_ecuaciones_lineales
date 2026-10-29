# Preguntas de los cuadernos

Una carpeta por cuaderno. Cada carpeta contiene UNA PREGUNTA POR ARCHIVO, para
que se pueda auditar una sin leer las demás.

```
preguntas/
├── u3_01_algebra_lineal/       Cuaderno 01 — Álgebra Lineal
│   ├── __init__.py             ← ÍNDICE: qué preguntas hay y en qué orden
│   ├── alg_01_op_matricial.md  ┐
│   ├── alg_02_asterisco.md     │ opción múltiple: SOLO el .md
│   ├── ...                     │ (no llevan Python, se editan aquí)
│   ├── alg_08_enteros.md       ┘
│   ├── p09_matriz_aumentada.py    con datos sembrados por NC
│   ├── p10_operacion_renglon.py
│   └── p11_producto_escalar.py
└── (u3_02_laboratorios a futuro)
```

## Cómo se llega a una pregunta

1. Abre `preguntas/<cuaderno>/__init__.py`. Es el índice: lista las preguntas en
   orden, con el archivo de cada una y qué evalúa.
2. Abre el archivo que te interese. Nada más.

## Los dos tipos

**Opción múltiple** — solo `.md`. La cabecera declara `id` y `titulo`; la
correcta se marca con `- [x]`, así que no hay índices que contar:

```markdown
---
id: alg_01
titulo: Producto matricial vs elemento a elemento
---

En la biblioteca del curso, **¿qué hace el operador `@`**?

- [x] El producto matricial (fila por columna)
- [ ] El producto elemento a elemento
```

**Con datos sembrados** — un `.py` con una función `construir(semilla)` que
devuelve la pregunta completa. La semilla sale del Número de Control, así que
cada alumno recibe números distintos pero siempre los mismos:

```python
def construir(semilla):
    rng = random.Random(semilla ^ SAL)
    ...
    return {
        'tipo': 'matriz',            # mcq | matriz | numero
        'id': ID,
        'titulo': TITULO,
        'enunciado': '...',          # Markdown con LaTeX
        'esperado': resultado,
        'ayuda': '...',
        'datos': {'A': A, 'm': m},   # para poder auditar
    }
```

## Reglas

- **Nada de estado global.** Cada `construir()` recibe la semilla y no lee nada
  más; así dos preguntas no se pisan.
- **Cada pregunta usa su propio `SAL`**, distinto del de las demás, para que no
  reciban los mismos números por casualidad.
- **Lo que solo usa una pregunta vive en su archivo** (aunque se repita con
  otra). Lo común está en `lib/mn_motor/comun.py`.
- **Si una pregunta muestra algo que depende de datos**, verifica en el mismo
  archivo que el texto y la respuesta esperada coincidan. La pregunta 10 lo hace
  y explica por qué.

## Después de cambiar algo

```powershell
.\.venv\Scripts\python.exe tools\build_grader.py
```

Regenera `grader_ofuscado.txt`, que es lo único que ve el alumno. El script
comprueba que el paquete cargue y califique bien antes de escribir.
