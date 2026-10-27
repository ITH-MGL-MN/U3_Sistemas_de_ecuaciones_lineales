# Matrices Especiales: Algoritmo de Thomas y Cholesky

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) | [README](../../README.md) | [Referencias Cruzadas y Matriz Comparativa de Desempeño](05_comparativa.md) |

## 📑 Índice

1. [4.1 Matrices Tridiagonales y el Algoritmo de Thomas](#sec-4-1)
2. [4.2 Factorización de Cholesky para Matrices Simétricas Definidas Positivas](#sec-4-2)
3. [🔢 Ejemplo resuelto: Algoritmo de Thomas](#sec-ej-thomas)
4. [🔢 Ejemplo resuelto: Cholesky](#sec-ej-cholesky)

### <a id="sec-4-1"></a>4.1 Matrices Tridiagonales y el Algoritmo de Thomas

#### Estructura del Sistema
Un sistema tridiagonal surge de la discretización por diferencias finitas en sistemas continuos (redes térmicas, vigas y difusión) y tiene coeficientes no nulos **exclusivamente en la diagonal principal y en las dos subdiagonales adyacentes**:

$$\begin{bmatrix}
f_1 & g_1 & 0 & \dots & 0 & 0 \\
e_2 & f_2 & g_2 & \dots & 0 & 0 \\
0 & e_3 & f_3 & \dots & 0 & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & \dots & e_n & f_n
\end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ \vdots \\ x_n \end{bmatrix}
=
\begin{bmatrix} r_1 \\ r_2 \\ r_3 \\ \vdots \\ r_n \end{bmatrix}$$

#### Algoritmo de Thomas ($O(n)$)
Es una versión altamente optimizada de la Descomposición LU *(véase [Sección 2](./02_descomposicion_lu.md))* que opera únicamente sobre los tres vectores $e, f, g$, reduciendo la memoria de $O(n^2)$ a **$O(n)$** y el tiempo de cómputo de $O(n^3)$ a **$O(n)$**:

1. **Fase 1: Descomposición LU y Modificación de Diagonales ($k = 2, \dots, n$)**:
   $$e_k' = \frac{e_k}{f_{k-1}'}$$
   $$f_k' = f_k - e_k' \cdot g_{k-1}$$

2. **Fase 2: Sustitución Hacia Adelante sobre el Lado Derecho ($k = 2, \dots, n$)**:
   $$r_k' = r_k - e_k' \cdot r_{k-1}'$$

3. **Fase 3: Sustitución Hacia Atrás ($k = n-1, n-2, \dots, 1$)**:
   $$x_n = \frac{r_n'}{f_n'}$$
   $$x_k = \frac{r_k' - g_k \cdot x_{k+1}}{f_k'}$$

---

### <a id="sec-4-2"></a>4.2 Factorización de Cholesky para Matrices Simétricas Definidas Positivas

#### Propiedades
Una matriz cuadrada $\mathbf{A}$ es **simétrica y definida positiva** si:
1. $\mathbf{A} = \mathbf{A}^T$ ($a_{ij} = a_{ji}$).
2. $\mathbf{x}^T \mathbf{A} \mathbf{x} > 0$ para cualquier vector no nulo $\mathbf{x} \in \mathbb{R}^n$.

#### Factorización $\mathbf{A} = \mathbf{L} \mathbf{L}^T$
En lugar de calcular dos matrices distintas $\mathbf{L}$ y $\mathbf{U}$, la simetría permite factorizar la matriz como el producto de una matriz triangular inferior $\mathbf{L}$ y su propia transpuesta $\mathbf{L}^T$:

$$\mathbf{A} = \mathbf{L} \mathbf{L}^T$$

$$\begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}
=
\begin{bmatrix}
l_{11} & 0 & 0 \\
l_{21} & l_{22} & 0 \\
l_{31} & l_{32} & l_{33}
\end{bmatrix}
\begin{bmatrix}
l_{11} & l_{21} & l_{31} \\
0 & l_{22} & l_{32} \\
0 & 0 & l_{33}
\end{bmatrix}$$

#### Fórmulas de Recurrencia de Cholesky:
Para el renglón $k \in \{1, 2, \dots, n\}$:

1. **Elementos fuera de la diagonal ($i = 1, \dots, k-1$)**:
   $$l_{ki} = \frac{a_{ki} - \sum_{j=1}^{i-1} l_{ij} l_{kj}}{l_{ii}}$$

2. **Elemento diagonal ($i = k$)**:
   $$l_{kk} = \sqrt{a_{kk} - \sum_{j=1}^{k-1} l_{kj}^2}$$

#### Ventajas del Método de Cholesky:
* **Costo Computacional Reducido:** Requiere $\frac{1}{3} n^3$ FLOPs (la mitad de operaciones que la descomposición LU estándar).
* **Ahorro de Memoria:** Solo requiere almacenar la mitad inferior de la matriz.
* **Estabilidad Numérica:** **No requiere pivoteo parcial** cuando la matriz es definida positiva, garantizando que el término dentro de la raíz cuadrada siempre sea estrictamente positivo ($a_{kk} - \sum l_{kj}^2 > 0$).

---

---

### <a id="sec-ej-thomas"></a>🔢 Ejemplo resuelto: Algoritmo de Thomas

Sistema tridiagonal (p. ej. conducción térmica 1D o masa-resorte):

$$\begin{bmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}$$

con diagonal $f=[2,2,2]$, subdiagonal $e=[\cdot,-1,-1]$, superdiagonal $g=[-1,-1,\cdot]$.

**Fase 1 (descomposición + sustitución adelante):**

$$k=1:\quad f_2' = 2 - \tfrac{-1}{2}(-1) = 1.5, \quad r_2' = 0 - \tfrac{-1}{2}(1) = 0.5$$

$$k=2:\quad f_3' = 2 - \tfrac{-1}{1.5}(-1) = 1.3333, \quad r_3' = 1 - \tfrac{-1}{1.5}(0.5) = 1.3333$$

**Fase 2 (sustitución hacia atrás):**

$$x_3 = \frac{1.3333}{1.3333} = 1, \quad x_2 = \frac{0.5 - (-1)(1)}{1.5} = 1, \quad x_1 = \frac{1 - (-1)(1)}{2} = 1$$

**Solución:** $\mathbf{x} = [1,\ 1,\ 1]^T$ en $O(n)$ operaciones. ✅

### <a id="sec-ej-cholesky"></a>🔢 Ejemplo resuelto: Cholesky

Para una matriz **simétrica definida positiva** $\mathbf{A} = \begin{bmatrix} 4 & 2 \\ 2 & 3 \end{bmatrix}$:

$$l_{11} = \sqrt{4} = 2, \qquad l_{21} = \frac{2}{2} = 1, \qquad l_{22} = \sqrt{3 - 1^2} = \sqrt{2}$$

$$\mathbf{L} = \begin{bmatrix} 2 & 0 \\ 1 & \sqrt{2} \end{bmatrix}, \qquad \mathbf{A} = \mathbf{L}\mathbf{L}^T$$

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) | [README](../../README.md) | [Referencias Cruzadas y Matriz Comparativa de Desempeño](05_comparativa.md) |

