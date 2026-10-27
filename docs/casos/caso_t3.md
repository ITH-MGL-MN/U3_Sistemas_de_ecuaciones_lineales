# 🎛️ Caso T3: Red de Filtros Pasivos RC en Escalera de 3 Etapas

> **# 🔹 BLOQUE A: Equipos de 2 Integrantes (Sistemas $3 \times 3$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T3`
* **Tamaño de equipo:** 2 integrantes
* **Área:** Electrónica / Procesamiento de Señales
* **Ecuación del sistema:** $\mathbf{A} \mathbf{v} = \mathbf{v}_{in}$

#### 1. Descripción Física y Modelo
Una red en escalera de 3 etapas RC para acondicionamiento de señal en un sensor industrial se analiza en régimen permanente. El balance de nodos conduce al sistema:

$$\begin{bmatrix}
(1 + \frac{R_1}{R_2}) & -1 & 0 \\
-1 & (2 + \frac{R_2}{R_3}) & -1 \\
0 & -1 & (1 + \frac{R_3}{R_L})
\end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \\ v_3 \end{bmatrix} =
\begin{bmatrix} v_{in} \\ 0 \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Tridiagonal pura de tamaño $3 \times 3$.
* **Solver Ideal:** Algoritmo de Thomas ($O(n)$ operaciones).
* **Análisis de Ingeniería:** Comparar el tiempo de ejecución del Algoritmo de Thomas frente a `inv(A) * b` y determinar la atenuación de voltaje $v_3 / v_{in}$.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

