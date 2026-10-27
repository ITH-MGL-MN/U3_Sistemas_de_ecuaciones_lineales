# Eliminación Gaussiana y Pivoteo Parcial

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| — | [README](../../README.md) | [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) |

## 📑 Índice

1. [1.1 Formulación Matricial del Sistema](#sec-1-1)
2. [1.2 Eliminación Hacia Adelante (*Forward Elimination*)](#sec-1-2)
3. [1.3 Estrategia de Pivoteo Parcial Por Renglón](#sec-1-3)
4. [1.4 Sustitución Hacia Atrás (*Back Substitution*)](#sec-1-4)
5. [1.5 Complejidad Computacional](#sec-1-5)

### <a id="sec-1-1"></a>1.1 Formulación Matricial del Sistema

**📘 Teoría.** Un sistema de $n$ ecuaciones lineales con $n$ incógnitas se escribe en forma matricial como

$$\mathbf{A}\mathbf{x} = \mathbf{b}$$

donde $\mathbf{A} \in \mathbb{R}^{n \times n}$ es la matriz de coeficientes, $\mathbf{x} \in \mathbb{R}^{n}$ el vector de incógnitas y $\mathbf{b} \in \mathbb{R}^{n}$ el de términos independientes. Cada renglón de $\mathbf{A}$ guarda los coeficientes de una ecuación y cada columna los de una incógnita.

El método opera con **operaciones elementales de renglón**: intercambiar dos renglones y restar a un renglón un múltiplo de otro. Ninguna de las dos cambia el conjunto solución, pero sí obliga a arrastrar el lado derecho, así que se pega $\mathbf{b}$ a la derecha de $\mathbf{A}$ y se forma la **matriz aumentada**

$$[\mathbf{A}\mid\mathbf{b}] = \begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} & \mid & b_1 \\
a_{21} & a_{22} & \dots & a_{2n} & \mid & b_2 \\
\vdots & \vdots & \ddots & \vdots & \mid & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn} & \mid & b_n
\end{bmatrix}.$$

De aquí en adelante se trabaja siempre sobre $[\mathbf{A}\mid\mathbf{b}]$ y nunca sobre $\mathbf{A}$ sola.

**🧮 Ejemplo algebraico.** Con un sistema $2\times 2$ genérico,

$$\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} =
\begin{bmatrix} b_1 \\ b_2 \end{bmatrix},$$

la matriz aumentada es

$$[\mathbf{A}\mid\mathbf{b}] = \begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}.$$

El renglón 1 representa $a_{11}x_1 + a_{12}x_2 = b_1$ y el renglón 2, $a_{21}x_1 + a_{22}x_2 = b_2$. Despejando la primera incógnita del primer renglón queda $x_1 = (b_1 - a_{12}x_2)/a_{11}$, válido solo si $a_{11} \neq 0$.

**🔢 Versión con enteros (paso a paso).** Se usa en todo el documento

$$\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 4 \\ 7 \end{bmatrix}.$$

1. Se traducen los renglones a ecuaciones: $2x_1 + x_2 = 4$ y $x_1 + 3x_2 = 7$.
2. Se arma la matriz aumentada: $\begin{bmatrix} 2 & 1 & \mid & 4 \\ 1 & 3 & \mid & 7 \end{bmatrix}$.
3. Se revisa el pivote de la columna 1: $a_{11} = 2 \neq 0$, por lo que se puede eliminar hacia adelante sin intercambiar renglones.

---

### <a id="sec-1-2"></a>1.2 Eliminación Hacia Adelante (*Forward Elimination*)

**📘 Teoría.** Esta fase convierte $\mathbf{A}$ en una matriz **triangular superior** $\mathbf{U}$, es decir, deja ceros debajo de la diagonal. Para cada pivote $k = 1, 2, \dots, n-1$ y cada renglón $i = k+1, \dots, n$ se calcula el **multiplicador**

$$m_{ik} = \frac{a_{ik}^{(k)}}{a_{kk}^{(k)}}$$

y se actualizan el renglón y el lado derecho con

$$a_{ij}^{(k+1)} = a_{ij}^{(k)} - m_{ik}\,a_{kj}^{(k)}, \qquad b_i^{(k+1)} = b_i^{(k)} - m_{ik}\,b_k^{(k)}.$$

Al terminar el ciclo queda $[\mathbf{U}\mid\mathbf{d}]$ triangular superior. En esta sección **no hay pivoteo**: se supone que todos los pivotes son distintos de cero. Para la matriz de abajo los pivotes son $2$, $\tfrac{1}{2}$ y $-1$, todos $\neq 0$, así que la eliminación simple es válida.

**🧮 Ejemplo algebraico.** En un sistema $2\times 2$ solo hay un paso:

$$m_{21} = \frac{a_{21}}{a_{11}}, \qquad a_{22}' = a_{22} - m_{21}a_{12}, \qquad b_2' = b_2 - m_{21}b_1.$$

Aplicando $R_2 \leftarrow R_2 - m_{21}R_1$ la matriz aumentada pasa de

$$\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}
\quad\longrightarrow\quad
\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ 0 & a_{22}' & \mid & b_2' \end{bmatrix},$$

y la segunda ecuación queda $a_{22}'x_2 = b_2'$, ya despejable.

**🔢 Versión con enteros (paso a paso).** Sistema

$$\mathbf{A} = \begin{bmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 8 \\ -11 \\ -3 \end{bmatrix}.$$

1. **Paso $k=1$.** Multiplicadores: $m_{21} = -3/2$ y $m_{31} = -1$.
2. Se aplican $R_2 \leftarrow R_2 - m_{21}R_1$ y $R_3 \leftarrow R_3 - m_{31}R_1$, con lo que la matriz aumentada queda

$$\begin{bmatrix} 2 & 1 & -1 & \mid & 8 \\ 0 & 1/2 & 1/2 & \mid & 1 \\ 0 & 2 & 1 & \mid & 5 \end{bmatrix}.$$

3. **Paso $k=2$.** Multiplicador: $m_{32} = 4$.
4. Se aplica $R_3 \leftarrow R_3 - m_{32}R_2$ y se llega a

$$\mathbf{U} = \begin{bmatrix} 2 & 1 & -1 \\ 0 & 1/2 & 1/2 \\ 0 & 0 & -1 \end{bmatrix}, \qquad \mathbf{d} = \begin{bmatrix} 8 \\ 1 \\ 1 \end{bmatrix}.$$

5. Los pivotes usados son $2$, $\tfrac{1}{2}$ y $-1$: ninguno es cero, la eliminación no se detuvo.

---

### <a id="sec-1-3"></a>1.3 Estrategia de Pivoteo Parcial Por Renglón

**📘 Teoría.** La eliminación simple falla de dos maneras: si $a_{kk}^{(k)} = 0$ el multiplicador $m_{ik}$ no existe, y si $|a_{kk}^{(k)}|$ es muy pequeño el multiplicador se vuelve enorme y amplifica los errores de redondeo de todo lo que sigue.

El **pivoteo parcial** evita ambas cosas eligiendo como pivote el elemento de mayor magnitud en la columna $k$, desde el renglón $k$ hasta el $n$:

$$p = \arg\max_{i = k, \dots, n} \left| a_{ik}^{(k)} \right|.$$

Si $p \neq k$ se intercambia el renglón $k$ completo con el renglón $p$, es decir $R_k \leftrightarrow R_p$, y recién entonces se calculan los multiplicadores.

Cada intercambio cambia el signo del determinante, de modo que

$$\det(\mathbf{A}) = (-1)^{p_{\text{swaps}}} \prod_{k=1}^{n} u_{kk},$$

donde $p_{\text{swaps}}$ es el número total de intercambios realizados.

**🧮 Ejemplo algebraico.** Para una matriz $2\times 2$ el criterio compara solo dos candidatos. Si $|a_{21}| > |a_{11}|$ se elige $p = 2$ y se intercambian los renglones:

$$\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}
\;\xrightarrow{R_1 \leftrightarrow R_2}\;
\begin{bmatrix} a_{21} & a_{22} & \mid & b_2 \\ a_{11} & a_{12} & \mid & b_1 \end{bmatrix}.$$

El nuevo pivote es $a_{21}$ y el determinante cambia de signo una vez: $\det(\mathbf{A}) = (-1)^{1} u_{11}u_{22}$.

**🔢 Versión con enteros (paso a paso).** Sistema

$$\mathbf{A} = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}.$$

1. Se revisa la columna 1: los candidatos son $|a_{11}| = 0$ y $|a_{21}| = 1$.
2. Como $p = 2 \neq 1$, el pivote $a_{11} = 0$ obliga a intercambiar.
3. Se aplica $R_1 \leftrightarrow R_2$ y queda

$$\mathbf{A} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 3 \\ 1 \end{bmatrix}.$$

4. Ahora el pivote es $1$, distinto de cero, y hubo un intercambio, así que el determinante lleva factor $(-1)^1$.

---

### <a id="sec-1-4"></a>1.4 Sustitución Hacia Atrás (*Back Substitution*)

**📘 Teoría.** Con el sistema ya triangular $\mathbf{U}\mathbf{x} = \mathbf{d}$, la última ecuación contiene una sola incógnita y se resuelve de inmediato:

$$x_n = \frac{d_n}{u_{nn}}.$$

Las demás se despejan en orden descendente, porque al llegar a $x_i$ todas las incógnitas $x_{i+1}, \dots, x_n$ ya son conocidas:

$$x_i = \frac{d_i - \sum_{j=i+1}^{n} u_{ij}x_j}{u_{ii}}, \qquad i = n-1, n-2, \dots, 1.$$

El costo de esta fase es $n^2 + O(n)$ FLOPs, mucho menor que el de la eliminación.

**🧮 Ejemplo algebraico.** Para un sistema $2\times 2$ ya triangular,

$$\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ 0 & a_{22}' & \mid & b_2' \end{bmatrix},$$

se aplica la fórmula dos veces:

$$x_2 = \frac{b_2'}{a_{22}'}, \qquad x_1 = \frac{b_1 - a_{12}x_2}{a_{11}}.$$

La división solo es válida si $a_{11} \neq 0$ y $a_{22}' \neq 0$.

**🔢 Versión con enteros (paso a paso).** Se parte de la forma triangular del subtema 1.2:

$$\mathbf{U} = \begin{bmatrix} 2 & 1 & -1 \\ 0 & 1/2 & 1/2 \\ 0 & 0 & -1 \end{bmatrix}, \qquad \mathbf{d} = \begin{bmatrix} 8 \\ 1 \\ 1 \end{bmatrix}.$$

1. Renglón 3: $x_3 = d_3/u_{33} = 1/(-1) = -1$.
2. Renglón 2: $x_2 = \left(d_2 - u_{23}x_3\right)/u_{22} = 3$.
3. Renglón 1: $x_1 = \left(d_1 - u_{12}x_2 - u_{13}x_3\right)/u_{11} = 2$.
4. Solución verificada del sistema: $\mathbf{x} = [2,\ 3,\ -1]$.

---

### <a id="sec-1-5"></a>1.5 Complejidad Computacional

**📘 Teoría.** Un FLOP es una operación de punto flotante (una suma o una multiplicación). Contar FLOPs es la forma estándar de comparar el costo de dos métodos.

La eliminación hacia adelante necesita

$$\frac{2}{3}n^{3} + O(n^{2}) \ \text{FLOPs},$$

la sustitución hacia atrás solo $n^{2} + O(n)$ FLOPs, y el costo total del método es $O(n^{3})$. El término cúbico domina: duplicar $n$ multiplica aproximadamente por ocho el trabajo de eliminación, mientras que la sustitución se multiplica por cuatro.

**🧮 Ejemplo algebraico.** Para $n$ genérico, en el paso $k$ se actualizan $n-k$ renglones y cada uno cuesta cerca de $2(n-k+1)$ FLOPs (un multiplicador, $n-k+1$ productos y otras tantas restas). Sumando sobre todos los pasos:

$$\sum_{k=1}^{n-1}\sum_{i=k+1}^{n} 2(n-k+1) \;=\; \frac{2}{3}n^{3} + O(n^{2}),$$

mientras que la sustitución hacia atrás, que solo recorre una vez los renglones, aporta $n^{2} + O(n)$. La razón entre ambos costos crece con $n$: para $n$ grande la eliminación es quien manda.

**🔢 Versión con enteros (paso a paso).** Con $n = 3$:

1. Se evalúa el término cúbico de la eliminación: $\tfrac{2}{3}n^{3} = \tfrac{2}{3}(27) = 18$ FLOPs.
2. Ese valor es un **orden de magnitud**, no un conteo exacto: los términos $O(n^{2})$ y las operaciones sobre $\mathbf{b}$ ajustan la cifra.
3. Para comparar, la sustitución hacia atrás aporta del orden de $n^{2} = 9$ FLOPs.
4. Conclusión para $n=3$: el total lo domina la eliminación, con cerca de 18 FLOPs frente a unos 9 de la sustitución.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| — | [README](../../README.md) | [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) |

