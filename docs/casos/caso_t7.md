# 🏗️ Caso T7: Deflexión de Viga Continua sobre Múltiples Apoyos

> **# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T7`
* **Tamaño de equipo:** 3 integrantes
* **Área:** Ingeniería Civil / Mecánica
* **Ecuación del sistema:** $\mathbf{M}_{3T} \mathbf{\theta} = \mathbf{d}$

#### 1. Descripción Física e Ecuación
Una viga hiperestática sobre 5 apoyos simples (4 tramos) sometida a carga uniforme $w$ se analiza con la ecuación de los tres momentos para los momentos flectores $M_1, M_2, M_3, M_4$:

$$\begin{bmatrix}
2(L_1 + L_2) & L_2 & 0 & 0 \\
L_2 & 2(L_2 + L_3) & L_3 & 0 \\
0 & L_3 & 2(L_3 + L_4) & L_4 \\
0 & 0 & L_4 & 2(L_4 + L_5)
\end{bmatrix}
\begin{bmatrix} M_1 \\ M_2 \\ M_3 \\ M_4 \end{bmatrix} =
\begin{bmatrix} d_1 \\ d_2 \\ d_3 \\ d_4 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Estrictamente tridiagonal con fuerte dominancia diagonal ($2(L_i + L_{i+1}) > L_i + L_{i+1}$).
* **Solver Ideal:** Algoritmo de Thomas ($O(n)$) o Descomposición LU.
* **Análisis de Ingeniería:** Graficar el diagrama de momentos flectores y localizar los puntos de inflexión ($M(x) = 0$).

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

