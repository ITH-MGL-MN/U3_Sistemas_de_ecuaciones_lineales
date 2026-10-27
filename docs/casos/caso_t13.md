# 🏭 Caso T13: Modelo Insumo-Producto de Leontief

> **# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T13`
* **Tamaño de equipo:** 4 integrantes
* **Área:** Ingeniería Industrial / Producción
* **Ecuación del sistema:** $(\mathbf{I} - \mathbf{C}) \mathbf{x} = \mathbf{d}$

#### 1. Descripción Física y Modelo
Una planta de manufactura integrada cuenta con 5 departamentos interdependientes (Metalmecánica, Ensamble, Pintura, Empaque, Mantenimiento). La matriz de consumos intersectoriales $\mathbf{C}$ y el vector de demanda final $\mathbf{d}$ definen el nivel de producción total $\mathbf{x}$:

$$\begin{bmatrix}
0.85 & -0.10 & -0.05 & -0.02 & -0.05 \\
-0.12 & 0.88 & -0.10 & -0.05 & -0.01 \\
-0.05 & -0.15 & 0.80 & -0.10 & -0.02 \\
-0.02 & -0.05 & -0.08 & 0.90 & -0.05 \\
-0.10 & -0.10 & -0.05 & -0.05 & 0.85
\end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \end{bmatrix} =
\begin{bmatrix} d_1 \\ d_2 \\ d_3 \\ d_4 \\ d_5 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Matriz de Leontief con dominante diagonal fuerte ($1 - c_{ii} > \sum c_{ij}$).
* **Solver Ideal:** Método de Gauss-Seidel o Inversión de Matrices mediante LU.
* **Análisis de Ingeniería:** Calcular la matriz inversa de Leontief $(\mathbf{I} - \mathbf{C})^{-1}$ para evaluar el impacto del incremento de demanda en un departamento sobre toda la planta.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

