# 🔌 Caso T2: Análisis de Nodos de Voltaje con Fuentes de Corriente

> **# 🔹 BLOQUE A: Equipos de 2 Integrantes (Sistemas $3 \times 3$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T2`
* **Tamaño de equipo:** 2 integrantes
* **Área:** Ingeniería Electrónica / Eléctrica
* **Ecuación del sistema:** $\mathbf{G} \mathbf{V} = \mathbf{I}$

#### 1. Descripción Física y Modelo
Un circuito plano de 3 nodos principales alimentado por fuentes de corriente independientes $I_a, I_b$ se modela mediante la Ley de Corrientes de Kirchhoff (LCK) en términos de conductancias $G_k = 1/R_k$:

$$\begin{bmatrix}
(G_1 + G_2 + G_3) & -G_2 & -G_3 \\
-G_2 & (G_2 + G_4) & -G_4 \\
-G_3 & -G_4 & (G_3 + G_4 + G_5)
\end{bmatrix}
\begin{bmatrix} V_1 \\ V_2 \\ V_3 \end{bmatrix} =
\begin{bmatrix} I_a \\ I_b \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Estrictamente diagonal dominante por renglones ($|g_{ii}| > \sum_{j \neq i} |g_{ij}|$).
* **Solver Ideal:** Método iterativo de Gauss-Seidel o Eliminación Gaussiana directa.
* **Análisis de Ingeniería:** Comprobar la rapidez de convergencia de Gauss-Seidel ($\le 10$ iteraciones con tolerancia $10^{-6}$) dada la fuerte dominancia diagonal de las conductancias.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

