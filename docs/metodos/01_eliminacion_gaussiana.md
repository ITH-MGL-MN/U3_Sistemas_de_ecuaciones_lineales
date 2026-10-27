# Eliminación Gaussiana y Pivoteo Parcial

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| — | [README](../../README.md) | [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) |

## 📑 Índice

- [Eliminación Gaussiana y Pivoteo Parcial](#eliminación-gaussiana-y-pivoteo-parcial)
  - [📑 Índice](#-índice)
    - [1.1 Formulación Matricial del Sistema](#11-formulación-matricial-del-sistema)
    - [1.2 Eliminación Hacia Adelante (*Forward Elimination*)](#12-eliminación-hacia-adelante-forward-elimination)
    - [1.3 Estrategia de Pivoteo Parcial Por Renglón](#13-estrategia-de-pivoteo-parcial-por-renglón)
    - [1.4 Sustitución Hacia Atrás (*Back Substitution*)](#14-sustitución-hacia-atrás-back-substitution)
    - [1.5 Complejidad Computacional](#15-complejidad-computacional)

### <a id="sec-1-1"></a>1.1 Formulación Matricial del Sistema

**📘 Teoría.**

Un **sistema de ecuaciones lineales** es un conjunto de ecuaciones en el que cada
incógnita aparece elevada a la primera potencia y nunca multiplicada por otra
incógnita. *Resolver* el sistema significa encontrar un valor para cada incógnita
que satisfaga **todas** las ecuaciones al mismo tiempo.

#### Forma estándar: $n$ ecuaciones con $n$ incógnitas

Antes de escribir nada con matrices, el sistema se escribe completo, ecuación por
ecuación:

$$
\begin{aligned}
a_{11}x_1 + a_{12}x_2 + \cdots + a_{1n}x_n &= b_1 \\
a_{21}x_1 + a_{22}x_2 + \cdots + a_{2n}x_n &= b_2 \\
&\;\vdots \\
a_{n1}x_1 + a_{n2}x_2 + \cdots + a_{nn}x_n &= b_n
\end{aligned}
$$

Esta es la **forma estándar**. Hay $n$ ecuaciones y $n$ incógnitas, y cada símbolo
tiene un significado preciso:

| Símbolo | Qué es | Cuántos hay |
|---|---|---|
| $n$ | Número de ecuaciones = número de incógnitas (sistema *cuadrado*) | 1 valor |
| $x_1, x_2, \dots, x_n$ | Las **incógnitas**: lo que queremos calcular | $n$ |
| $a_{ij}$ | **Coeficiente**: el número que multiplica a $x_j$ en la ecuación $i$ | $n \times n$ |
| $b_i$ | **Término independiente**: el número conocido del lado derecho de la ecuación $i$ | $n$ |

El doble subíndice de $a_{ij}$ no es casual: el **primer** índice dice *en qué
ecuación* está (el renglón) y el **segundo**, *a qué incógnita* acompaña (la
columna). Así, $a_{23}$ es el coeficiente que multiplica a $x_3$ en la segunda
ecuación.

Un ejemplo con $n = 3$ para fijar ideas:

$$
\begin{aligned}
2x_1 + 1x_2 - 1x_3 &= 8 \\
-3x_1 - 1x_2 + 2x_3 &= -11 \\
-2x_1 + 1x_2 + 2x_3 &= -3
\end{aligned}
$$

Aquí $a_{11}=2$, $a_{12}=1$, $a_{13}=-1$, $b_1=8$, y así sucesivamente. Este
sistema de $3\times3$ se retomará en el subtema 1.2.

#### De la forma estándar a la forma matricial

Al escribir las ecuaciones una debajo de otra salta a la vista un patrón: las
incógnitas $x_1, x_2, \dots, x_n$ aparecen **en el mismo orden en todas las
ecuaciones**. Eso permite separar los datos (los números) de las incógnitas
(las letras) y escribir el sistema tres veces más compacto:

1. Se toman los coeficientes de cada ecuación, en orden, y se coloca cada
   ecuación en un renglón. Eso forma la **matriz de coeficientes** $\mathbf{A}$.
2. Las incógnitas se ponen en una sola columna: el **vector de incógnitas**
   $\mathbf{x}$.
3. Los términos independientes se ponen en otra columna: el **vector de términos
   independientes** $\mathbf{b}$.

$$
\underbrace{\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn}
\end{bmatrix}}_{\mathbf{A}\;(n\times n)}
\;
\underbrace{\begin{bmatrix}
x_1 \\ x_2 \\ \vdots \\ x_n
\end{bmatrix}}_{\mathbf{x}\;(n\times 1)}
=
\underbrace{\begin{bmatrix}
b_1 \\ b_2 \\ \vdots \\ b_n
\end{bmatrix}}_{\mathbf{b}\;(n\times 1)}
$$

es decir,

$$\mathbf{A}\mathbf{x} = \mathbf{b}.$$

#### ¿Por qué la forma matricial dice lo mismo?

Porque al multiplicar una matriz por un vector, **cada renglón produce una
ecuación**. Con un caso $2\times 2$ se ve sin lugar a dudas:

$$
\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
=
\begin{bmatrix}
a_{11}x_1 + a_{12}x_2 \\
a_{21}x_1 + a_{22}x_2
\end{bmatrix}
=
\begin{bmatrix} b_1 \\ b_2 \end{bmatrix}.
$$

El primer renglón del resultado es exactamente la primera ecuación de la forma
estándar y el segundo renglón es la segunda ecuación. En general, el renglón $i$
del producto $\mathbf{A}\mathbf{x}$ es

$$a_{i1}x_1 + a_{i2}x_2 + \cdots + a_{in}x_n,$$

que es justamente la ecuación $i$. Por eso $\mathbf{A}\mathbf{x} = \mathbf{b}$
y la forma estándar son **el mismo sistema**, solo escrito de otra manera.

> 💡 **Interpretación geométrica (interactiva).** En el [Cuaderno 01](../../notebooks/U3_01_Algebra_Lineal.ipynb), sección 7, puedes girar con el ratón dos rectas que se cruzan en un punto (2 ecuaciones, 2 incógnitas) y tres planos que se cruzan en un punto (3 ecuaciones, 3 incógnitas). Ahí se explica por qué con cientos o miles de ecuaciones ya no se puede dibujar.

#### La matriz aumentada

Resolver el sistema exige hacer **operaciones elementales de renglón**:
intercambiar dos renglones, o restar a un renglón un múltiplo de otro. Ninguna de
las dos cambia la solución, pero ambas afectan también al lado derecho. Para no
olvidar esa parte, se pega $\mathbf{b}$ a la derecha de $\mathbf{A}$, separado
por una línea vertical, y se forma la **matriz aumentada**:

$$
[\mathbf{A}\mid\mathbf{b}] = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} & \mid & b_1 \\
a_{21} & a_{22} & \cdots & a_{2n} & \mid & b_2 \\
\vdots & \vdots & \ddots & \vdots & \mid & \vdots \\
a_{n1} & a_{n2} & \cdots & a_{nn} & \mid & b_n
\end{bmatrix}.
$$

Todo el método de Gauss trabaja sobre esta matriz: los coeficientes a la
izquierda de la línea y los términos independientes a la derecha. De aquí en
adelante se opera siempre sobre $[\mathbf{A}\mid\mathbf{b}]$ y nunca sobre
$\mathbf{A}$ sola.

**🧮 Ejemplo algebraico.** Con un sistema $2\times 2$ genérico,

$$\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} =
\begin{bmatrix} b_1 \\ b_2 \end{bmatrix},$$

la matriz aumentada es

$$[\mathbf{A}\mid\mathbf{b}] = \begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}.$$

El renglón 1 representa $a_{11}x_1 + a_{12}x_2 = b_1$ y el renglón 2, $a_{21}x_1 + a_{22}x_2 = b_2$. Despejando la primera incógnita del primer renglón queda $x_1 = (b_1 - a_{12}x_2)/a_{11}$, válido solo si $a_{11} \neq 0$.

**🔢 Versión con enteros (paso a paso).** Para este primer ejemplo, un sistema
$2\times2$ sencillo:

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

