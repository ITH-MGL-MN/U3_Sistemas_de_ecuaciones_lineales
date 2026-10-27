# ⚡ Caso T1: Análisis de Corrientes de Malla en Circuito de CD

> **# 🔹 BLOQUE A: Equipos de 2 Integrantes (Sistemas $3 \times 3$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T1`
* **Tamaño de equipo:** 2 integrantes
* **Área:** Ingeniería Mecatrónica / Eléctrica
* **Ecuación del sistema:** $\mathbf{R} \mathbf{I} = \mathbf{V}$

#### 1. Descripción Física y Modelo
Un circuito de corriente directa consta de 3 mallas interconectadas con resistencias $R_1, R_2, R_3, R_4, R_5$ y fuentes de voltaje $V_1, V_2$. Aplicando la Ley de Voltajes de Kirchhoff (LVK) a cada malla:

$$\begin{bmatrix}
(R_1 + R_2) & -R_2 & 0 \\
-R_2 & (R_2 + R_3 + R_4) & -R_4 \\
0 & -R_4 & (R_4 + R_5)
\end{bmatrix}
\begin{bmatrix} I_1 \\ I_2 \\ I_3 \end{bmatrix} =
\begin{bmatrix} V_1 \\ 0 \\ -V_2 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Simétrica, tridiagonal y definida positiva.
* **Solver Ideal:** Algoritmo de Thomas o Factorización de Cholesky ($\mathbf{A} = \mathbf{L}\mathbf{L}^T$).
* **Análisis de Ingeniería:** Evaluar la caída de potencia $P_i = I_i^2 R_i$ y verificar que $\text{Cond}(\mathbf{R}) < 100$, garantizando alta estabilidad ante tolerancias comerciales de resistencias ($5\%$).

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

