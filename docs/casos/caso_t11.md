# 🚰 Caso T11: Distribución de Caudales en Red de Tuberías Linealizada

> **# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T11`
* **Tamaño de equipo:** 4 integrantes
* **Área:** Ingeniería Hidráulica / Civil
* **Ecuación del sistema:** $\mathbf{H} \mathbf{Q} = \mathbf{d}_h$

#### 1. Descripción Física y Modelo
Una red de distribución de agua para una planta industrial consta de 5 nodos piezométricos interconectados alimentados por tanques elevados. Aplicando la conservación de masa y la ecuación de pérdidas linealizada $h_f = R_k Q_k$:

$$\begin{bmatrix}
(R_1 + R_2) & -R_2 & 0 & 0 & 0 \\
-R_2 & (R_2 + R_3 + R_4) & -R_4 & 0 & 0 \\
0 & -R_4 & (R_4 + R_5) & -R_5 & 0 \\
0 & 0 & -R_5 & (R_5 + R_6) & -R_6 \\
0 & 0 & 0 & -R_6 & (R_6 + R_7)
\end{bmatrix}
\begin{bmatrix} Q_1 \\ Q_2 \\ Q_3 \\ Q_4 \\ Q_5 \end{bmatrix} = \mathbf{d}_{tanques}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Laplaciana simétrica tridiagonal $5 \times 5$.
* **Solver Ideal:** Algoritmo de Thomas o Factorización LU.
* **Análisis de Ingeniería:** Identificar tramos con caída de presión excesiva y calcular el número de condición de la red.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

