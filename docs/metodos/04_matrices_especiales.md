# Matrices Especiales: Algoritmo de Thomas y Cholesky

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) | [README](../../README.md) | [Referencias Cruzadas y Matriz Comparativa de Desempeño](05_comparativa.md) |

## 📑 Índice

1. [4.1 Matrices Tridiagonales y el Algoritmo de Thomas](#sec-4-1)
2. [4.2 Factorización de Cholesky para Matrices Simétricas Definidas Positivas](#sec-4-2)

### <a id="sec-4-1"></a>4.1 Matrices Tridiagonales y el Algoritmo de Thomas

**📘 Teoría.** Un sistema tridiagonal tiene coeficientes no nulos solo en la diagonal principal ($f$) y en las dos diagonales adyacentes ($e$ abajo, $g$ arriba):

$$\begin{bmatrix}
f_1 & g_1 & 0 & \dots & 0 \\
e_2 & f_2 & g_2 & \dots & 0 \\
0 & e_3 & f_3 & \dots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \dots & f_n
\end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ \vdots \\ x_n \end{bmatrix}
=
\begin{bmatrix} r_1 \\ r_2 \\ r_3 \\ \vdots \\ r_n \end{bmatrix}.$$

El **algoritmo de Thomas** es una eliminación gaussiana sin pivoteo que aprovecha la estructura: nunca guarda los ceros, solo los tres vectores, así que baja de $O(n^{2})$ a $O(n)$ de memoria y de $O(n^{3})$ a $O(n)$ de tiempo.

Fase 1, descomposición ($k = 2,\dots,n$):

$$e_k' = \frac{e_k}{f_{k-1}'}, \qquad f_k' = f_k - e_k'\,g_{k-1}.$$

Fase 2, sustitución hacia adelante sobre el lado derecho ($k = 2,\dots,n$):

$$r_k' = r_k - e_k'\,r_{k-1}'.$$

Fase 3, sustitución hacia atrás ($k = n-1,\dots,1$):

$$x_n = \frac{r_n'}{f_n'}, \qquad x_k = \frac{r_k' - g_k\,x_{k+1}}{f_k'}.$$

Es la misma factorización LU del documento 02, solo que restringida a tres diagonales.

**🧮 Ejemplo algebraico.** Para $n = 2$ con letras,

$$\begin{bmatrix} f_1 & g_1 \\ e_2 & f_2 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} r_1 \\ r_2 \end{bmatrix},$$

las tres fases se escriben:

$$e_2' = \frac{e_2}{f_1}, \qquad f_2' = f_2 - e_2'g_1, \qquad r_2' = r_2 - e_2'r_1,$$

$$x_2 = \frac{r_2'}{f_2'}, \qquad x_1 = \frac{r_1 - g_1x_2}{f_1}.$$

El pivote de la fase 1 es $f_1$, por eso el algoritmo exige $f_1 \neq 0$ (en general, $f_k' \neq 0$).

**🔢 Versión con enteros (paso a paso).** Datos: $f = [2,\ 2,\ 2]$, $e = [0,\ -1,\ -1]$, $g = [-1,\ -1,\ 0]$, $r = [1,\ 0,\ 1]$.

1. **Inicio de la fase 1:** $f_1' = 2$ y $r_1' = 1$.
2. **$k = 2$:** $e_2' = (-1)/2$; entonces $f_2' = 3/2$ y $r_2' = 1/2$.
3. **$k = 3$:** $e_3' = -1/(3/2)$; entonces $f_3' = 4/3$ y $r_3' = 4/3$.
4. **Diagonales modificadas:** $f' = [2,\ 3/2,\ 4/3]$ y $r' = [1,\ 1/2,\ 4/3]$.
5. **Sustitución hacia atrás:** $x_3 = r_3'/f_3' = 1$; $x_2 = (r_2' - g_2x_3)/f_2' = 1$; $x_1 = (r_1 - g_1x_2)/f_1' = 1$.
6. **Solución:** $\mathbf{x} = [1,\ 1,\ 1]$ en tiempo $O(n)$.

---

### <a id="sec-4-2"></a>4.2 Factorización de Cholesky para Matrices Simétricas Definidas Positivas

**📘 Teoría.** Una matriz es **simétrica y definida positiva** si $\mathbf{A} = \mathbf{A}^{T}$ (es decir $a_{ij} = a_{ji}$) y además $\mathbf{x}^{T}\mathbf{A}\mathbf{x} > 0$ para todo $\mathbf{x} \neq \mathbf{0}$.

En ese caso la factorización LU se puede reducir a una sola matriz: existe $\mathbf{L}$ triangular inferior tal que

$$\mathbf{A} = \mathbf{L}\mathbf{L}^{T}.$$

Las recurrencias, renglón por renglón ($k = 1,\dots,n$), son

$$l_{kk} = \sqrt{a_{kk} - \sum_{j=1}^{k-1} l_{kj}^{2}}, \qquad
l_{ki} = \frac{a_{ki} - \sum_{j=1}^{i-1} l_{ij}l_{kj}}{l_{ii}}, \quad i < k.$$

La raíz cuadrada se calcula primero sobre la diagonal y luego se dividen las entradas del renglón. Tres consecuencias prácticas: cuesta $\tfrac{1}{3}n^{3}$ FLOPs (la mitad que LU), solo hay que guardar la mitad inferior y, por ser definida positiva, el radicando $a_{kk} - \sum l_{kj}^{2}$ es estrictamente positivo, así que **no requiere pivoteo**.

**🧮 Ejemplo algebraico.** Para $n = 2$, igualando entradas en $\mathbf{A} = \mathbf{L}\mathbf{L}^{T}$:

$$\begin{bmatrix} a_{11} & a_{21} \\ a_{21} & a_{22} \end{bmatrix} =
\begin{bmatrix} l_{11} & 0 \\ l_{21} & l_{22} \end{bmatrix}
\begin{bmatrix} l_{11} & l_{21} \\ 0 & l_{22} \end{bmatrix},$$

se obtiene

$$l_{11} = \sqrt{a_{11}}, \qquad l_{21} = \frac{a_{21}}{l_{11}}, \qquad l_{22} = \sqrt{a_{22} - l_{21}^{2}}.$$

Cada entrada de $\mathbf{L}$ necesita solo valores ya calculados de $\mathbf{L}$, y el orden obligatorio es diagonal y luego columna, renglón por renglón.

**🔢 Versión con enteros (paso a paso).** Matriz simétrica definida positiva

$$\mathbf{A} = \begin{bmatrix} 4 & 12 & -16 \\ 12 & 37 & -43 \\ -16 & -43 & 98 \end{bmatrix}.$$

1. **Diagonal $l_{11}$:** $l_{11} = \sqrt{4} = 2$.
2. **Columna 1:** $l_{21} = 12/2 = 6$ y $l_{31} = -16/2 = -8$.
3. **Diagonal $l_{22}$:** $l_{22} = \sqrt{37 - 6^{2}} = 1$.
4. **Columna 2:** $l_{32} = (-43 - (6)(-8))/1 = 5$.
5. **Diagonal $l_{33}$:** $l_{33} = \sqrt{98 - (-8)^{2} - 5^{2}} = 3$.
6. **Resultado:**

$$\mathbf{L} = \begin{bmatrix} 2 & 0 & 0 \\ 6 & 1 & 0 \\ -8 & 5 & 3 \end{bmatrix}.$$

7. **Verificación $\mathbf{L}\mathbf{L}^{T} = \mathbf{A}$:** la entrada $(1,1)$ da $2\cdot 2 = 4$; la $(2,2)$ da $36 + 1 = 37$; la $(3,3)$ da $64 + 25 + 9 = 98$. En las de fuera de la diagonal, $(1,2) = 2\cdot 6 = 12$ y $(2,3) = 6(-8) + 1\cdot 5 = -43$. Coincide con $\mathbf{A}$.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) | [README](../../README.md) | [Referencias Cruzadas y Matriz Comparativa de Desempeño](05_comparativa.md) |

