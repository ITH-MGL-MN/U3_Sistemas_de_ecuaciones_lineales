# 🧪 Caso T9: Balance de Materia en 4 Reactores CSTR Acoplados

> **# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T9`
* **Tamaño de equipo:** 3 integrantes
* **Área:** Ingeniería Química / Procesos
* **Ecuación del sistema:** $\mathbf{Q} \mathbf{c} = \mathbf{b}_c$

#### 1. Descripción Física y Modelo
Cuatro reactores continuos de mezcla completa (CSTR) se interconectan con flujos de entrada, salida y recirculación continua. El balance de masa en régimen permanente para una especie reactiva con reacción de primer orden ($k_i V_i$) es:

$$\begin{bmatrix}
(Q_{11} + k_1 V_1) & -Q_{21} & 0 & -Q_{41} \\
-Q_{12} & (Q_{22} + k_2 V_2) & -Q_{32} & 0 \\
0 & -Q_{23} & (Q_{33} + k_3 V_3) & -Q_{43} \\
-Q_{14} & 0 & -Q_{34} & (Q_{44} + k_4 V_4)
\end{bmatrix}
\begin{bmatrix} c_1 \\ c_2 \\ c_3 \\ c_4 \end{bmatrix} =
\begin{bmatrix} Q_0 c_0 \\ 0 \\ 0 \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Dominancia diagonal estricta por renglones debido a la presencia de los términos de reacción y salida acumulada $Q_{ii} + k_i V_i$.
* **Solver Ideal:** Método de Gauss-Seidel o Sobrerrelajación Sucesiva (SOR con $\lambda = 1.1$).
* **Análisis de Ingeniería:** Calcular la conversión global del sistema $\eta = (c_0 - c_4) / c_0 \times 100\%$ y evaluar el impacto del gasto de recirculación.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

