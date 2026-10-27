# 🦾 Caso T5: Cercha Plana 2D de Brazo Robótico (4 Nodos / 5 Barras)

> **# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T5`
* **Tamaño de equipo:** 3 integrantes
* **Área:** Ingeniería Mecatrónica / Estructuras
* **Ecuación del sistema:** $\mathbf{A}_{\theta} \mathbf{F} = \mathbf{P}$

#### 1. Descripción Física y Modelo
Un brazo articulado liviano soporta una carga vertical $P$ en su extremo. El balance de fuerzas en los nodos 2 y 3 genera un sistema de $4 \times 4$ para las tensiones internas $F_1, F_2, F_3, F_4$:

$$\begin{bmatrix}
\cos\alpha & 1 & \cos\beta & 0 \\
\sin\alpha & 0 & -\sin\beta & 0 \\
0 & -1 & 0 & \cos\gamma \\
0 & 0 & \sin\beta & \sin\gamma
\end{bmatrix}
\begin{bmatrix} F_1 \\ F_2 \\ F_3 \\ F_4 \end{bmatrix} =
\begin{bmatrix} 0 \\ P \\ 0 \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Asimétrica con ceros estratégicos en la diagonal.
* **Solver Ideal:** Eliminación Gaussiana con **Pivoteo Parcial por Renglón** obligatorio.
* **Análisis de Ingeniería:** Identificar qué barras están en tracción ($F_i > 0$) y compresión ($F_i < 0$), y evaluar cómo cambia $\text{Cond}(\mathbf{A}_{\theta})$ al variar los ángulos articulados.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

