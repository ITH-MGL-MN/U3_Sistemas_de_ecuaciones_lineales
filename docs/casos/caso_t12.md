# 🔥 Caso T12: Estequiometría de Combustión Compleja

> **# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T12`
* **Tamaño de equipo:** 4 integrantes
* **Área:** Ingeniería Química / Automotriz
* **Ecuación del sistema:** $\mathbf{E} \mathbf{x} = \mathbf{b}_e$

#### 1. Descripción Física y Modelo
La combustión de un hidrocarburo complejo ($C_8 H_{18}$) con aire enriquecido en un motor de combustión interna genera 5 especies en los gases de escape ($CO_2, H_2O, CO, O_2, N_2$). El balance atómico de C, H, O, N y la relación molar fija forma un sistema $5 \times 5$:

$$\begin{bmatrix}
8 & 0 & 1 & 0 & 0 \\
0 & 2 & 0 & 0 & 0 \\
16 & 1 & 1 & 2 & 0 \\
0 & 0 & 0 & 0 & 2 \\
0 & 0 & -0.1 & 1 & -3.76
\end{bmatrix}
\begin{bmatrix} x_{CO2} \\ x_{H2O} \\ x_{CO} \\ x_{O2} \\ x_{N2} \end{bmatrix} =
\begin{bmatrix} 8 \\ 18 \\ 25 \\ 94 \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Asimétrica densa.
* **Solver Ideal:** Eliminación Gaussiana con pivoteo parcial.
* **Análisis de Ingeniería:** Determinar la relación aire-combustible ($\text{AFR}$) real y la concentración de monóxido de carbono en ppm.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

