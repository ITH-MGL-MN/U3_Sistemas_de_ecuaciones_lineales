# 🌡️ Caso T16: Red de Intercambiadores de Calor Serie/Paralelo

> **# 🔹 BLOQUE D: Equipos de 5 Integrantes (Sistemas 3D y Mal Condicionados)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T16`
* **Tamaño de equipo:** 5 integrantes
* **Área:** Procesos Térmicos / Química
* **Ecuación del sistema:** $\mathbf{C}_{ter} \mathbf{T}_{out} = \mathbf{q}_{in}$

#### 1. Descripción Física y Modelo
Una red compleja de 6 a 8 intercambiadores de calor tubulares interconectados recupera energía de corrientes de proceso. El balance de energía por corriente con efectividad de intercambio $\epsilon_k$ conduce a un sistema lineal de $6 \times 6$:

$$\begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 \\
-\epsilon_1 & 1 & 0 & 0 & 0 & 0 \\
0 & -\epsilon_2 & 1 & 0 & 0 & 0 \\
0 & 0 & -\epsilon_3 & 1 & 0 & 0 \\
0 & 0 & 0 & -\epsilon_4 & 1 & 0 \\
0 & 0 & 0 & 0 & -\epsilon_5 & 1
\end{bmatrix}
\begin{bmatrix} T_1 \\ T_2 \\ T_3 \\ T_4 \\ T_5 \\ T_6 \end{bmatrix} = \mathbf{b}_{proceso}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Triangular inferior (o de banda si hay recirculación).
* **Solver Ideal:** Sustitución hacia adelante ($O(n^2)$) o Descomposición LU.
* **Análisis de Ingeniería:** Calcular la eficiencia global de recuperación térmica de la planta.

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

