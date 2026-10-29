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
├── u3_02_gaussiana/            Cuaderno 02 — Eliminación Gaussiana
├── u3_03_lu/                   Cuaderno 03 — Descomposición LU
└── u3_04_especiales_iterativos/  Cuaderno 04 — Especiales e iterativos
```

Cada cuaderno tiene 11 preguntas: 5 de opción múltiple, 3 con dato calculado y 3
de **programar**.

## Cómo se llega a una pregunta

1. Abre `preguntas/<cuaderno>/__init__.py`. Es el índice: lista las preguntas en
   orden, con el archivo de cada una y qué evalúa.
2. Abre el archivo que te interese. Nada más.

## Los tres tipos

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
        'tipo': 'matriz',            # mcq | matriz | numero | funcion
        'id': ID,
        'titulo': TITULO,
        'enunciado': '...',          # Markdown con LaTeX
        'esperado': resultado,
        'ayuda': '...',
        'datos': {'A': A, 'm': m},   # para poder auditar
    }
```

**De programar** (`'tipo': 'funcion'`) — no hay nada que teclear: el alumno
escribe una función en el cuaderno y el motor la busca **por nombre** entre las
variables del cuaderno y la prueba con casos ocultos.

```python
FUNCION = 'mi_gauss_eliminar'       # el nombre que debe tener su función
FIRMA = 'mi_gauss_eliminar(A, b)'   # se le muestra al alumno
REFERENCIA = 'gauss_eliminar'       # quién lo resuelve, en solvers_u3

    return {
        'tipo': 'funcion',
        'funcion': FUNCION,
        'firma': FIRMA,
        'referencia': REFERENCIA,
        'ejemplo': ((A_ej, b_ej), referencia(A_ej, b_ej)),   # para practica()
        'casos': [((A, b), referencia(A, b)), ...],          # ocultos
    }
```

- Los `casos` deben ser de **tamaños distintos** (2, 3 y 4). Es lo que hace que
  una implementación clavada a 3×3 no pase.
- La `referencia` se usa en dos lugares: `practica()` compara contra el ejemplo
  visible, y `tools/build_grader.py` la entrega como "alumno perfecto" para
  comprobar el blob antes de escribirlo.
- Si la respuesta son **varias matrices** (`return L, U`), el esperado es una
  tupla de matrices y `comun.comparar` las revisa por separado.

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
