# 🚛 Caso T8: Repartición de Cargas en Suspensión Neumática Multieje

> **# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)** · [🗂️ Volver al índice](casos_index.md)

* **ID Tema:** `T8`
* **Tamaño de equipo:** 3 integrantes
* **Área:** Ingeniería Automotriz / Mecatrónica
* **Ecuación del sistema:** $\mathbf{A}_p \mathbf{P} = \mathbf{W}$

#### 1. Descripción Física y Modelo
Un vehículo de transporte pesado de 4 ejes cuenta con un sistema de nivelación neumática. El equilibrio de fuerzas verticales y momentos longitudinales/transversales conduce a:

$$\begin{bmatrix}
1 & 1 & 1 & 1 \\
-x_1 & -x_2 & x_3 & x_4 \\
-y_1 & y_2 & -y_3 & y_4 \\
k_1 & -k_2 & k_3 & -k_4
\end{bmatrix}
\begin{bmatrix} P_1 \\ P_2 \\ P_3 \\ P_4 \end{bmatrix} =
\begin{bmatrix} W_{total} \\ W \cdot e_x \\ W \cdot e_y \\ 0 \end{bmatrix}$$

#### 2. Propiedades Matriciales y Solver Recomendado
* **Tipo de Matriz:** Densa de $4 \times 4$.
* **Solver Ideal:** Descomposición LU con pivoteo parcial (Doolittle).
* **Análisis de Ingeniería:** Verificar que todas las presiones neumáticas $P_i$ resulten dentro del rango operativo de trabajo ($20\text{ psi} \le P_i \le 100\text{ psi}$).

---

> [🗂️ Volver al índice de casos](casos_index.md) · [📚 Métodos](../metodos/05_comparativa.md) · [🏠 README](../../README.md)

