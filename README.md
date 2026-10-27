# ⚡ Unidad 3: Sistemas de Ecuaciones Lineales

## 🎯 Objetivo General
Analizar, implementar y evaluar métodos numéricos directos e iterativos para la resolución de **sistemas de ecuaciones algebraicas lineales** $\mathbf{A}\mathbf{x} = \mathbf{b}$, aplicando herramientas de álgebra matricial, simulación estocástica de **Monte Carlo** y análisis de sensibilidad sobre casos reales de ingeniería (circuitos eléctricos, estructuras robóticas, redes de tuberías y balance de masa).

---

## 🗺️ Mapa de Navegación del Repositorio

```text
U3/
├── README.md                      <-- Centro de mando e instrucciones generales
├── docs/
│   ├── metodos/                   <-- Guías teóricas completas con ecuaciones en LaTeX
│   │   ├── 01_eliminacion_gaussiana.md
│   │   ├── 02_descomposicion_lu.md
│   │   ├── 03_metodos_iterativos.md
│   │   ├── 04_matrices_especiales.md
│   │   └── 05_comparativa.md
│   └── casos/                     <-- Fichas técnicas de los 17 casos de ingeniería
│       ├── casos_index.md
│       └── caso_t01.md … caso_t17.md
├── notebooks/                     <-- Cuadernos interactivos en Google Colab
│   ├── U3_01_Algebra_Lineal.ipynb
│   ├── U3_02_Laboratorios_Metodos.ipynb
│   ├── U3_03_Seleccion_Casos.ipynb
│   └── U3_04_Analisis_Casos.ipynb
├── lib/                           <-- Helpers: matlab_like + robomat (fusión)
├── config/                        <-- config.yaml + guía del backend Apps Script
└── reporte/                       <-- Plantilla LaTeX del reporte final
```

---

## 🚀 Cuadernos Interactivos en Google Colab

Haz clic en las insignias para abrir cada cuaderno en Google Colab.

| # | Cuaderno / Actividad | Descripción y Alcance | Enlace Directo |
|---|---|---|:---:|
| **01** | **Álgebra Lineal** | Introducción práctica a matrices con `matlab_like` + `robomat` fusionados: construcción de matrices, operaciones de renglón, determinante, inversa y manipulación simbólica. | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1aEIZ7s9Y9HbS9fnOVf3-42uq94VrnVcl) |
| **02** | **Laboratorios de Métodos** | Laboratorios y prácticas sobre [los 4 métodos](docs/metodos/): Eliminación Gaussiana, LU, Gauss-Seidel y Thomas/Cholesky. Preguntas de opción múltiple y numéricas abiertas, comparación Python vs MATLAB (teórico). | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1eWIoYtyad4EM_7rcUaALZvfZoqwLdh0z) |
| **03** | **Selección de Equipos y Casos** | Registro del equipo y asignación determinista del Caso de Estudio (T1–T17) mediante la semilla del Número de Control (NC). | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CM18n8fFl5YmgiNKsCUSQqxRmF-9KbNs) |
| **04** | **Análisis de Caso y Reporte** | Cada método implementado en un archivo `.py`, comparación versión manual vs `numpy`/`scipy`, y exportación de resultados/figuras para el reporte en LaTeX. | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1oczPp_-MehZ2mauySE4yYPiorykkFyGG) |

---

## 📚 Documentación Teórica por Método

Consulta los archivos de documentación para estudiar las ecuaciones, diagramas de flujo e interpretación matemática necesaria para tu reporte y exposición:

1. 📖 [**Eliminación Gaussiana y Pivoteo Parcial**](docs/metodos/01_eliminacion_gaussiana.md)
   * Formación de la matriz aumentada $[\mathbf{A} \mid \mathbf{b}]$, factores de eliminación $m_{ik}$, estrategia de pivoteo por renglón y sustitución hacia atrás.
2. 📖 [**Descomposición LU e Inversión de Matrices**](docs/metodos/02_descomposicion_lu.md)
   * Factorización $\mathbf{A} = \mathbf{L}\mathbf{U}$ (Doolittle y Crout), resolución de $\mathbf{L}\mathbf{d} = \mathbf{b}$ y $\mathbf{U}\mathbf{x} = \mathbf{d}$, y cálculo de $\mathbf{A}^{-1}$.
3. 📖 [**Métodos Iterativos: Gauss-Seidel y Relajación**](docs/metodos/03_metodos_iterativos.md)
   * Despeje componente a componente, criterio de dominancia diagonal estricta y factor de relajación $\lambda$ (SOR).
4. 📖 [**Matrices Especiales: Thomas y Cholesky**](docs/metodos/04_matrices_especiales.md)
   * Algoritmo de Thomas $O(n)$ para sistemas tridiagonales y factorización de Cholesky para matrices simétricas definidas positivas.
5. 🔄 [**Referencias Cruzadas y Matriz Comparativa**](docs/metodos/05_comparativa.md)
   * Tabla comparativa de complejidad, memoria, estabilidad y caso de uso ideal de cada método.

---

## 🏭 Casos de Estudio de Ingeniería

Cada equipo trabajará sobre un problema real asignado en el **Cuaderno 03**. Consulta el [🗂️ índice completo de los 17 casos](docs/casos/casos_index.md), organizados por tamaño de equipo:

| Bloque | Integrantes | Casos | Temática |
|:---:|:---:|:---:|---|
| **A** | 2 | T1–T4 | Circuitos de malla, nodos, filtros RC y conducción térmica 1D ($3\times3$) |
| **B** | 3 | T5–T9 | Cercha robótica, masa-resorte, viga, suspensión y reactores CSTR ($4\times4$) |
| **C** | 4 | T10–T14 | Térmica 2D, tuberías, combustión, Leontief y destilación ($5\times5$–$6\times6$) |
| **D** | 5 | T15–T16 | Cercha espacial 3D e intercambiadores de calor (mal condicionados) |
| **E** | 6 | T17 | Flujo de carga DC en red de potencia ($8\times8$) |

---

## 💯 Criterios de Evaluación

La **Mega Tarea Integradora de la Unidad 3** se evalúa mediante tres componentes:

| Componente | Peso (%) | Formato de Entrega | Método de Registro |
|---|:---:|---|---|
| **Autograder de Teoría y Código** | **40%** | Cuadernos Colab 02 y 04 | Envío automático a Google Sheets vía Apps Script |
| **Reporte Escrito en LaTeX** | **40%** | Documento PDF compilado en LaTeX | Entrega del `.tex` y PDF en la plataforma |
| **Exposición del Caso de Estudio** | **20%** | Exposición de 5 minutos por equipo | Presencial/grabada, apoyada en la teoría del repositorio |

---

## 🛠️ Herramientas y Requisitos

No requieres instalar software adicional: el entorno de Colab carga automáticamente la librería personalizada (`matlab_like` + `robomat`) para simplificar las operaciones matriciales y simbólicas. La fusión vive en [`lib/`](lib/) y se precarga desde los cuadernos.

```python
# Carga directa del entorno enriquecido en Colab (ver lib/)
import urllib.request
url = "https://raw.githubusercontent.com/ITH-MGL-MN/U3_Sistemas_de_ecuaciones_lineales/main/lib/robomat.py"
urllib.request.urlretrieve(url, "robomat.py")
exec(open("robomat.py").read(), globals())
```

---

### 📩 Soporte y Dudas
Si encuentras algún detalle en los algoritmos o cuadernos, abre un *Issue* en este repositorio o consulta las fechas límite registradas en la hoja de control de la materia.
