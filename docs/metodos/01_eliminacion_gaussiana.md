# Eliminación Gaussiana y Pivoteo Parcial

### 1.1 Formulación Matricial del Sistema
Un sistema simultáneo de $n$ ecuaciones lineales algebraicas con $n$ incógnitas se expresa como:

$$\mathbf{A}\mathbf{x} = \mathbf{b}$$

donde $\mathbf{A} \in \mathbb{R}^{n \times n}$ es la matriz de coeficientes, $\mathbf{x} \in \mathbb{R}^n$ es el vector de variables desconocidas y $\mathbf{b} \in \mathbb{R}^n$ es el vector de términos independientes:

$$\begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\
a_{21} & a_{22} & \dots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn}
\end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}
=
\begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_n \end{bmatrix}$$

Para manipular el sistema mediante operaciones elementales de renglón, se define la **matriz aumentada**:

$$\tilde{\mathbf{A}} = [\mathbf{A} \mid \mathbf{b}] = \begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} & \mid & b_1 \\
a_{21} & a_{22} & \dots & a_{2n} & \mid & b_2 \\
\vdots & \vdots & \ddots & \vdots & \mid & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn} & \mid & b_n
\end{bmatrix}$$

---

### 1.2 Eliminación Hacia Adelante (*Forward Elimination*)
El objetivo de esta fase es transformar la matriz de coeficientes $\mathbf{A}$ en una matriz **triangular superior** $\mathbf{U}$.

Para cada pivote $k \in \{1, 2, \dots, n-1\}$:
1. **Multiplicador / Factor de eliminación** para el renglón $i \in \{k+1, \dots, n\}$:
   $$m_{ik} = \frac{a_{ik}^{(k)}}{a_{kk}^{(k)}}$$

2. **Actualización de elementos del renglón $i$**:
   $$a_{ij}^{(k+1)} = a_{ij}^{(k)} - m_{ik} \cdot a_{kj}^{(k)}, \quad \text{para } j = k, \dots, n$$
   $$b_i^{(k+1)} = b_i^{(k)} - m_{ik} \cdot b_k^{(k)}$$

Al finalizar el bucle externo $k$, la matriz aumentada adopta la forma triangular superior:

$$[\mathbf{U} \mid \mathbf{d}] = \begin{bmatrix}
a_{11} & a_{12} & a_{13} & \dots & a_{1n} & \mid & b_1 \\
0 & a_{22}' & a_{23}' & \dots & a_{2n}' & \mid & b_2' \\
0 & 0 & a_{33}'' & \dots & a_{3n}'' & \mid & b_3'' \\
\vdots & \vdots & \vdots & \ddots & \vdots & \mid & \vdots \\
0 & 0 & 0 & \dots & a_{nn}^{(n-1)} & \mid & b_n^{(n-1)}
\end{bmatrix}$$

---

### 1.3 Estrategia de Pivoteo Parcial Por Renglón

#### Diagnóstico de Fallas
La eliminación Gaussiana simple presenta dos limitaciones severas:
* **División entre cero:** Si $a_{kk}^{(k)} = 0$, el multiplicador $m_{ik}$ no puede calcularse.
* **Amplificación de errores de redondeo:** Si $|a_{kk}^{(k)}| \ll 1$, el multiplicador $m_{ik}$ se vuelve extremadamente grande, amplificando el error flotante en todos los términos subsiguientes.

#### Criterio de Selección de Pivote
Antes de eliminar los elementos debajo de la diagonal en el paso $k$, se busca el elemento con el mayor valor absoluto en la columna $k$, desde el renglón $k$ hasta el renglón $n$:

$$p = \arg\max_{i = k, \dots, n} |a_{ik}^{(k)}|$$

Si $p \neq k$, se intercambia el renglón $k$ completo por el renglón $p$:

$$R_k \longleftrightarrow R_p$$

#### Determinante mediante Eliminación Gaussiana
El determinante de la matriz $\mathbf{A}$ equivale al producto de los elementos diagonales de la matriz triangular superior $\mathbf{U}$, corregido por el número total de intercambios de renglón $p_{\text{swaps}}$ realizados durante el pivoteo:

$$\det(\mathbf{A}) = (-1)^{p_{\text{swaps}}} \prod_{k=1}^n u_{kk}$$

*(Para profundizar en la relación con la factorización $PLU$, véase la [Sección 2](./02_descomposicion_lu.md)).*

---

### 1.4 Sustitución Hacia Atrás (*Back Substitution*)
Con el sistema en forma triangular superior $\mathbf{U}\mathbf{x} = \mathbf{d}$, las incógnitas se despejan iterativamente desde la última ($x_n$) hasta la primera ($x_1$):

1. **Última incógnita**:
   $$x_n = \frac{d_n}{u_{nn}}$$

2. **Incógnitas generales ($i = n-1, n-2, \dots, 1$)**:
   $$x_i = \frac{d_i - \sum_{j=i+1}^n u_{ij} x_j}{u_{ii}}$$

---

### 1.5 Complejidad Computacional
* **Fase de eliminación:** $\frac{2}{3} n^3 + O(n^2)$ FLOPs (operaciones de punto flotante).
* **Fase de sustitución hacia atrás:** $n^2 + O(n)$ FLOPs.
* **Costo Total:** $O(n^3)$.

---

---

## 🔢 Ejemplo resuelto paso a paso

Resolvamos el sistema clásico de Chapra (Ejemplo 9.5):

$$\mathbf{A} = \begin{bmatrix} 3 & -0.1 & -0.2 \\ 0.1 & 7 & -0.3 \\ 0.3 & -0.2 & 10 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 7.85 \\ -19.3 \\ 71.4 \end{bmatrix}$$

**1) Matriz aumentada** $[\mathbf{A}\mid\mathbf{b}]$:

$$\begin{bmatrix} 3 & -0.1 & -0.2 & \mid & 7.85 \\ 0.1 & 7 & -0.3 & \mid & -19.3 \\ 0.3 & -0.2 & 10 & \mid & 71.4 \end{bmatrix}$$

**2) Eliminación hacia adelante.** Pivote $k=1$: el mayor $|a|$ de la columna 1 es $3$ (renglón 1), no hay intercambio. Multiplicadores:

$$m_{21} = \frac{0.1}{3} = 0.0333, \qquad m_{31} = \frac{0.3}{3} = 0.1$$

Aplicando $R_2 \leftarrow R_2 - m_{21}R_1$ y $R_3 \leftarrow R_3 - m_{31}R_1$:

$$\begin{bmatrix} 3 & -0.1 & -0.2 & \mid & 7.85 \\ 0 & 7.00333 & -0.29333 & \mid & -19.5617 \\ 0 & -0.19 & 10.02 & \mid & 70.615 \end{bmatrix}$$

Pivote $k=2$: mayor $|a|$ de la columna 2 (desde el renglón 2) es $7.00333$. Multiplicador $m_{32} = -0.19/7.00333 = -0.02713$:

$$\begin{bmatrix} 3 & -0.1 & -0.2 & \mid & 7.85 \\ 0 & 7.00333 & -0.29333 & \mid & -19.5617 \\ 0 & 0 & 10.0120 & \mid & 70.0843 \end{bmatrix}$$

**3) Sustitución hacia atrás:**

$$x_3 = \frac{70.0843}{10.0120} = 7$$

$$x_2 = \frac{-19.5617 - (-0.29333)(7)}{7.00333} = -2.5$$

$$x_1 = \frac{7.85 - (-0.1)(-2.5) - (-0.2)(7)}{3} = 3$$

**Solución:** $\mathbf{x} = [3,\ -2.5,\ 7]^T$. ✅ *Verifícalo en el [Cuaderno 04](../../notebooks/04_Analisis_Casos.ipynb) con `np.linalg.solve(A, b)`.*

---

> [📚 Volver al README](../../README.md) · [🏭 Casos de estudio](../casos/casos_index.md)

