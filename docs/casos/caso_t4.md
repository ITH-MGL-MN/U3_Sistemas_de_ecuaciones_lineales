# 🌡️ Caso T4: Conducción Térmica 1D en Barra Discretizada

> **# 🔹 BLOQUE A: Equipos de 2 Integrantes (Sistemas $3 \times 3$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T4`
* **Tamaño de equipo:** 2 integrantes
* **Área:** Ingeniería Mecánica / Térmica
* **Ecuación del sistema:** $\mathbf{K}_T \mathbf{T} = \mathbf{b}_T$

#### 1. Descripción Física y Modelo
Una barra metálica de longitud $L$ aislada lateralmente tiene sus extremos fijos a temperaturas $T_A$ y $T_B$. Discretizando el interior en 3 nodos con diferencias finitas para $d^2 T / dx^2 = 0$:

$$\begin{bmatrix}
-2 & 1 & 0 \\
1 & -2 & 1 \\
0 & 1 & -2
\end{bmatrix}
\begin{bmatrix} T_1 \\ T_2 \\ T_3 \end{bmatrix} =
\begin{bmatrix} -T_A \\ 0 \\ -T_B \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Tridiagonal simétrica, negativa definida.
* **Solver Ideal:** Algoritmo de Thomas o Descomposición LU (Doolittle).
* **Análisis de Ingeniería:** Verificar la linealidad del perfil de temperaturas resultante y calcular el flujo de calor conducido $q = -k \frac{dT}{dx}$.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

