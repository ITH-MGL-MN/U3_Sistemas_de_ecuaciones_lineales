# ⚗️ Caso T14: Separación por Etapas en Columna de Destilación

> **# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T14`
* **Tamaño de equipo:** 4 integrantes
* **Área:** Ingeniería Química / Procesos
* **Ecuación del sistema:** $\mathbf{M}_{dest} \mathbf{y} = \mathbf{f}$

#### 1. Descripción Física y Modelo
Una columna de destilación binaria de 6 platos teóricos separa una mezcla hidrocarburo. El balance de materia en cada plato $j$ con relación de equilibrio $y_j = K_j x_j$ se modela mediante el algoritmo tridiagonal de Thomas:

$$\begin{bmatrix}
B_1 & C_1 & 0 & 0 & 0 & 0 \\
A_2 & B_2 & C_2 & 0 & 0 & 0 \\
0 & A_3 & B_3 & C_3 & 0 & 0 \\
0 & 0 & A_4 & B_4 & C_4 & 0 \\
0 & 0 & 0 & A_5 & B_5 & C_5 \\
0 & 0 & 0 & 0 & A_6 & B_6
\end{bmatrix}
\begin{bmatrix} y_1 \\ y_2 \\ y_3 \\ y_4 \\ y_5 \\ y_6 \end{bmatrix} =
\begin{bmatrix} F_1 \\ F_2 \\ F_3 \\ F_4 \\ F_5 \\ F_6 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Tridiagonal de $6 \times 6$.
* **Solver Ideal:** Algoritmo de Thomas ($O(n)$).
* **Análisis de Ingeniería:** Determinar el perfil de concentraciones plato a plato y la pureza del producto de cabeza (destilado).

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

