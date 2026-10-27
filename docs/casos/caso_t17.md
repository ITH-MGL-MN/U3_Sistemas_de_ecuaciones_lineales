# ⚡ Caso T17: Flujo de Carga Linealizado (DC Power Flow) en Red de Potencia

> **# 🔹 BLOQUE E: Equipos de 6 Integrantes (Reto Integrador $8 \times 8$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T17`
* **Tamaño de equipo:** 6 integrantes
* **Área:** Ingeniería Eléctrica / Potencia / Mecatrónica
* **Ecuación del sistema:** $\mathbf{B}' \mathbf{\theta} = \mathbf{P}_{net}$

#### 1. Descripción Física y Modelo
Una red de transmisión de energía eléctrica de 8 subestaciones (nodos) se analiza mediante la aproximación linealizada de flujo de potencia DC. La matriz de susceptancia nodal de red $\mathbf{B}'$ de tamaño $8 \times 8$ relaciona los ángulos de fase de voltaje $\theta_k$ con la potencia activa neta inyectada $P_k$:

$$\begin{bmatrix}
B'_{11} & -B'_{12} & 0 & 0 & -B'_{15} & 0 & 0 & 0 \\
-B'_{21} & B'_{22} & -B'_{23} & 0 & 0 & 0 & 0 & 0 \\
0 & -B'_{32} & B'_{33} & -B'_{34} & 0 & 0 & 0 & 0 \\
0 & 0 & -B'_{43} & B'_{44} & -B'_{45} & -B'_{46} & 0 & 0 \\
-B'_{51} & 0 & 0 & -B'_{54} & B'_{55} & 0 & -B'_{57} & 0 \\
0 & 0 & 0 & -B'_{64} & 0 & B'_{66} & -B'_{67} & -B'_{68} \\
0 & 0 & 0 & 0 & -B'_{75} & -B'_{76} & B'_{77} & -B'_{78} \\
0 & 0 & 0 & 0 & 0 & -B'_{86} & -B'_{88} & B'_{88}
\end{bmatrix}
\begin{bmatrix} \theta_1 \\ \theta_2 \\ \theta_3 \\ \theta_4 \\ \theta_5 \\ \theta_6 \\ \theta_7 \\ \theta_8 \end{bmatrix} =
\begin{bmatrix} P_1 \\ P_2 \\ P_3 \\ P_4 \\ P_5 \\ P_6 \\ P_7 \\ P_8 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Simétrica, dispersa y singular si no se fija un nodo de referencia ($\theta_{ref} = 0$). Eliminando el nodo de referencia se obtiene una matriz $7 \times 7$ definida positiva.
* **Solver Ideal:** Inversión de Matrices mediante Descomposición LU para obtener la matriz de factores de distribución de transferencia de potencia (PTDF).
* **Análisis de Ingeniería:** 
  1. Calcular la matriz inversa $(\mathbf{B}')^{-1}$ para determinar cómo afecta el fallo de una línea de transmisión a los flujos en las demás líneas.
  2. Evaluar el número de condición de la red $\text{Cond}(\mathbf{B}')$ y localizar cuellos de botella en la capacidad de transmisión.

---

### 📝 Resumen Metodológico para el Reporte de los Alumnos

Para cualquier caso asignado (T1 a T17), el reporte escrito en LaTeX y la presentación deberán incluir:
1. **Modelado Físico:** Deducción de la matriz $\mathbf{A}$ y vector $\mathbf{b}$ a partir de las leyes de conservación.
2. **Propiedades Numéricas:** Cálculo explícito de $\det(\mathbf{A})$, $\|\mathbf{A}\|_\infty$, $\|\mathbf{A}^{-1}\|_\infty$ y el número de condición $\text{Cond}(\mathbf{A})$.
3. **Resolución y Comparación:** Ejecución del sistema mediante el solver primario asignado y contraste contra `np.linalg.solve(A, b)`.
4. **Interpretación de Ingeniería:** Conclusiones físicas sobre las tensiones, temperaturas, voltajes o caudales obtenidos.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

