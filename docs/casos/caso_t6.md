# ⚙️ Caso T6: Sistema Masa-Resorte de 4 Masas Acopladas

> **# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T6`
* **Tamaño de equipo:** 3 integrantes
* **Área:** Ingeniería Mecánica / Vibraciones
* **Ecuación del sistema:** $\mathbf{K} \mathbf{x} = \mathbf{F}$

#### 1. Descripción Física y Modelo
Cuatro masas $m_1, m_2, m_3, m_4$ conectadas en línea por resortes de rigidez $k_1, k_2, k_3, k_4, k_5$ entre dos paredes fijas se someten a fuerzas estáticas $F_1, F_2, F_3, F_4$:

$$\begin{bmatrix}
(k_1 + k_2) & -k_2 & 0 & 0 \\
-k_2 & (k_2 + k_3) & -k_3 & 0 \\
0 & -k_3 & (k_3 + k_4) & -k_4 \\
0 & 0 & -k_4 & (k_4 + k_5)
\end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{bmatrix} =
\begin{bmatrix} F_1 \\ F_2 \\ F_3 \\ F_4 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Simétrica, tridiagonal y definida positiva.
* **Solver Ideal:** Factorización de Cholesky o Algoritmo de Thomas.
* **Análisis de Ingeniería:** Obtener la matriz inversa de rigidez $\mathbf{F} = \mathbf{K}^{-1}$ (matriz de flexibilidad) e interpretar el significado físico de sus columnas.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

