# ⚡ Unidad 3: Sistemas de Ecuaciones Lineales

## 🎯 Objetivo General

Analizar, implementar y evaluar métodos numéricos **directos e iterativos** para
resolver sistemas de ecuaciones algebraicas lineales $\mathbf{A}\mathbf{x} =
\mathbf{b}$, con aritmética exacta cuando el método lo permite y flotante cuando
no, y aplicarlos a casos reales de ingeniería (circuitos, estructuras, redes de
tuberías, balance de masa).

---

## 🧭 Los cuatro cuadernos

La unidad se recorre en cuatro cuadernos. Cada uno mezcla teoría, laboratorio y
preguntas calificables: **no hay documentos aparte que leer antes**; el cuaderno
es autosuficiente.

| # | Cuaderno | Qué se aprende |
|---|---|---|
| **01** | **Álgebra Lineal** | Construir matrices con sintaxis estilo MATLAB, operaciones de renglón, matriz aumentada, determinante, inversa, álgebra simbólica. |
| **02** | **Eliminación Gaussiana** | Triangularizar un sistema, multiplicadores, sustitución hacia atrás, **pivoteo** (pivote cero y pivote diminuto), determinante y costo $O(n^3)$. |
| **03** | **Descomposición LU** | Factorizar $\mathbf{A} = \mathbf{L}\mathbf{U}$ (Doolittle, Crout), reusar la factorización para varios $\mathbf{b}$, inversa. |
| **04** | **Matrices Especiales y Métodos Iterativos** | Thomas y Cholesky primero; después Gauss-Seidel, Jacobi, relajación y convergencia. Cierra con las funciones de álgebra lineal que ya traen NumPy/SciPy/SymPy y una comparativa de cuándo conviene cada método. El orden sigue a Chapra. |

---

## 🗺️ Mapa del Repositorio

```text
U3_Repo/
├── README.md                      <-- este archivo
├── docs/
│   ├── metodos/                   <-- teoría de apoyo (el cuaderno ya la incluye)
│   │   ├── 01_eliminacion_gaussiana.md
│   │   ├── 02_descomposicion_lu.md
│   │   ├── 03_metodos_iterativos.md
│   │   ├── 04_matrices_especiales.md
│   │   └── 05_comparativa.md
│   └── casos/                     <-- banco de 17 casos de ingeniería
├── notebooks/                     <-- los cuatro cuadernos
├── lib/
│   ├── robomat.py                 <-- biblioteca del curso (sintaxis MATLAB)
│   └── mn_motor/                  <-- motor de calificación (no se publica)
├── preguntas/                     <-- preguntas de cada cuaderno (no se publica)
├── grader/                        <-- un blob por cuaderno: lo que usa el alumno
├── config/                        <-- config.yaml + guía del backend Apps Script
├── tools/                         <-- build_grader.py
└── reporte/                       <-- plantilla LaTeX de otra unidad (sin uso aquí)
```

---

## 🚀 Cómo se usan los cuadernos

1. Abre el cuaderno en Google Colab.
2. Ejecuta la **primera celda**: monta tu Drive, clona o actualiza el repositorio
   en `MyDrive/CursoMN/U3_Repo` y carga la biblioteca y el motor.
3. Ejecuta la celda de **identificación**: lee tu correo `@….tecnm.mx`, saca tu
   Número de Control y genera **tus** preguntas. Cada alumno recibe matrices
   distintas, así que copiar no sirve.
4. Trabaja el cuaderno de arriba abajo. Las secciones de laboratorio no se
   califican: ahí conviene romper cosas y experimentar.
5. Al final, contesta las preguntas, ejecuta **Calificar** (no envía nada) y,
   cuando estés conforme, **Enviar**.

### 📤 Intentos de envío

| | |
|---|---|
| Calificar sin enviar | las veces que quieras |
| **Envíos al profesor** | **5 como máximo** por cuaderno |

El límite lo impone el backend (Apps Script); el motor solo avisa antes de gastar
el último.

---

## 📚 Documentación Teórica por Método

Los cuadernos ya traen la teoría completa. Estos archivos sirven para consultar
las ecuaciones sin abrir el cuaderno, o para exponer:

1. 📖 [**Eliminación Gaussiana y Pivoteo Parcial**](docs/metodos/01_eliminacion_gaussiana.md)
   * Matriz aumentada $[\mathbf{A}\mid\mathbf{b}]$, multiplicadores $m_{ik}$,
     pivoteo por renglón y sustitución hacia atrás.
2. 📖 [**Descomposición LU**](docs/metodos/02_descomposicion_lu.md)
   * $\mathbf{A}=\mathbf{L}\mathbf{U}$ (Doolittle y Crout), resolución de
     $\mathbf{L}\mathbf{d}=\mathbf{b}$ y $\mathbf{U}\mathbf{x}=\mathbf{d}$.
3. 📖 [**Métodos Iterativos**](docs/metodos/03_metodos_iterativos.md)
   * Despeje componente a componente, dominancia diagonal y relajación (SOR).
4. 📖 [**Matrices Especiales: Thomas y Cholesky**](docs/metodos/04_matrices_especiales.md)
   * Thomas $O(n)$ para tridiagonales y Cholesky para simétricas definidas
     positivas.
5. 🔄 [**Comparativa entre Métodos**](docs/metodos/05_comparativa.md)
   * Complejidad, memoria, estabilidad y caso de uso ideal de cada uno.

---

## 🏭 Casos de Ingeniería

Los casos se aplican **dentro de cada cuaderno**, en su sección final: un
problema real resuelto con el método que se acaba de estudiar, comprobado de
forma analítica (residual cero, verificación física) y con una discusión de
**por qué ese método y no otro**.

El [🗂️ banco completo de 17 casos](docs/casos/casos_index.md) queda como reserva
para tareas y exámenes, organizado por tamaño de sistema:

| Bloque | Tamaño | Casos | Temática |
|:---:|:---:|:---:|---|
| **A** | $3\times3$ | T1–T4 | Circuitos de malla, nodos, filtros RC, conducción térmica 1D |
| **B** | $4\times4$ | T5–T9 | Cercha robótica, masa-resorte, viga, suspensión, reactores CSTR |
| **C** | $5\times5$–$6\times6$ | T10–T14 | Térmica 2D, tuberías, combustión, Leontief, destilación |
| **D** | $6\times6$–$7\times7$ | T15–T16 | Cercha espacial 3D e intercambiadores (mal condicionados) |
| **E** | $8\times8$ | T17 | Flujo de carga DC en red de potencia |

---

## 💯 Evaluación

| Componente | Peso | Cómo se registra |
|---|:---:|---|
| Autograder de los cuadernos 01–04 | 100% | Envío automático a Google Sheets vía Apps Script |

No hay reporte en LaTeX ni exposición en esta unidad: se integrarán con las
demás unidades en un proyecto final.

---

## 🛠️ Herramientas

No hay que instalar nada: la primera celda de cada cuaderno monta Drive, trae el
repositorio y deja lista la biblioteca. La sintaxis es **estilo MATLAB**, con dos
caminos para construir matrices:

```python
A = M[[2, 1], [1, 3]]        # numérico (float64), como MATLAB por omisión
A = M.sym[[2, 1], [1, 3]]    # exacto: enteros y fracciones (MatrizRobomat)

A @ B        # producto matricial
A * B        # producto elemento a elemento (el .* de MATLAB)
eye_sym(n)   # identidad exacta, para arrancar la L de una factorización
sqrt(x)      # raíz exacta si x es simbólico (Cholesky), NumPy si es decimal
mostrar(A)   # pinta la matriz en LaTeX
```

Para los métodos directos conviene `M.sym`: no hay error de redondeo y las
fracciones se leen tal cual. `es_exacto(x)` dice si un resultado quedó sin
ningún flotante.

---

### 📩 Soporte

Si encuentras un error en los algoritmos o en los cuadernos, abre un *Issue* en
este repositorio.
