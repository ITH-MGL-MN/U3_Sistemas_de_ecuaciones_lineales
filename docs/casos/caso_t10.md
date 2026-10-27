# 🔲 Caso T10: Conducción Térmica 2D en Placa Rectangular

> **# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T10`
* **Tamaño de equipo:** 4 integrantes
* **Área:** Ingeniería Mecánica / Térmica
* **Ecuación del sistema:** $\mathbf{A}_{2D} \mathbf{T} = \mathbf{b}_{2D}$

#### 1. Descripción Física y Modelo
Una placa metálica plana se somete a temperaturas de borde fijas. Discretizando el dominio interior en una malla de $3 \times 2 = 6$ nodos con la ecuación de Laplace $\nabla^2 T = 0$:

$$T_{i+1,j} + T_{i-1,j} + T_{i,j+1} + T_{i,j-1} - 4T_{i,j} = 0$$

El sistema $6 \times 6$ resultante toma la forma de matriz de banda:

$$\begin{bmatrix}
-4 & 1 & 0 & 1 & 0 & 0 \\
1 & -4 & 1 & 0 & 1 & 0 \\
0 & 1 & -4 & 0 & 0 & 1 \\
1 & 0 & 0 & -4 & 1 & 0 \\
0 & 1 & 0 & 1 & -4 & 1 \\
0 & 0 & 1 & 0 & 1 & -4
\end{bmatrix}
\begin{bmatrix} T_1 \\ T_2 \\ T_3 \\ T_4 \\ T_5 \\ T_6 \end{bmatrix} = \mathbf{b}_{borde}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Matriz de banda con dominancia diagonal simétrica.
* **Solver Ideal:** Gauss-Seidel o Cholesky de banda.
* **Análisis de Ingeniería:** Graficar las isotermas de la placa usando `contour` de Matplotlib y verificar la simetría del campo térmico.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

