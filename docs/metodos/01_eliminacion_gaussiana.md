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

**📘 Teoría.**

#### La idea: eliminar incógnitas una por una

En álgebra elemental un sistema se resuelve **eliminando** incógnitas: se toma
una ecuación, se multiplica por un número conveniente y se le resta a otra para
que una incógnita desaparezca. Con dos ecuaciones,

$$
\begin{aligned}
a_{11}x_1 + a_{12}x_2 &= b_1 &&\text{(ecuación 1)}\\
a_{21}x_1 + a_{22}x_2 &= b_2 &&\text{(ecuación 2)}
\end{aligned}
$$

si se multiplica la ecuación 1 por $\frac{a_{21}}{a_{11}}$ y se le resta a la
ecuación 2, la incógnita $x_1$ desaparece de la segunda:

$$\left(a_{21} - \frac{a_{21}}{a_{11}}a_{11}\right)x_1
+ \left(a_{22} - \frac{a_{21}}{a_{11}}a_{12}\right)x_2
= b_2 - \frac{a_{21}}{a_{11}}b_1,$$

es decir

$$0\cdot x_1 + a_{22}'\,x_2 = b_2',
\qquad a_{22}' = a_{22} - \frac{a_{21}}{a_{11}}a_{12},
\qquad b_2' = b_2 - \frac{a_{21}}{a_{11}}b_1.$$

La ecuación 2 quedó con **una sola incógnita** y ya se puede despejar.

#### Por qué esa resta es legal

Multiplicar una ecuación por una constante y restársela a otra **no cambia la
solución**: si un vector $\mathbf{x}$ cumple las dos ecuaciones originales,
también cumple cualquier combinación de ellas, y viceversa. Se reemplaza una
ecuación por otra equivalente, sin perder información. Es exactamente el mismo
argumento que se usa en álgebra elemental.

#### El pivote y el multiplicador

El número entre el que se divide, $a_{11}$ en el ejemplo, se llama **pivote**: es
el coeficiente de la incógnita que se va a eliminar. El factor que se resta se
llama **multiplicador**:

$$m_{ik} = \frac{a_{ik}^{(k)}}{a_{kk}^{(k)}}.$$

El subíndice $k$ dice **qué incógnita** se elimina en ese paso y la $i$,
**de qué renglón** se elimina. El pivote es entonces $a_{kk}$, el elemento de la
diagonal del renglón $k$. Debe cumplir $a_{kk} \neq 0$ porque está en un
denominador.

#### El algoritmo con $n$ ecuaciones

El mismo paso se repite para cada columna $k = 1, 2, \dots, n-1$:

1. **Tomar el pivote** $a_{kk}^{(k)}$ del renglón $k$.
2. Para cada renglón de abajo, $i = k+1, \dots, n$, calcular su multiplicador
   $m_{ik} = a_{ik}^{(k)}/a_{kk}^{(k)}$.
3. **Restar** $m_{ik}$ veces el renglón $k$ al renglón $i$, en **todos** los
   coeficientes desde la columna $k$ hasta la $n$, y también en $\mathbf{b}$:

$$a_{ij}^{(k+1)} = a_{ij}^{(k)} - m_{ik}\,a_{kj}^{(k)},
\qquad b_i^{(k+1)} = b_i^{(k)} - m_{ik}\,b_k^{(k)}.$$

El superíndice $(k)$ significa "el valor que tiene en el paso $k$": los números
van cambiando de un paso al siguiente.

#### Qué se logra: forma triangular

Al terminar, todo lo que está **debajo de la diagonal** quedó en cero:

$$
[\mathbf{U}\mid\mathbf{d}] = \begin{bmatrix}
u_{11} & u_{12} & \cdots & u_{1n} & \mid & d_1 \\
0 & u_{22} & \cdots & u_{2n} & \mid & d_2 \\
\vdots & \vdots & \ddots & \vdots & \mid & \vdots \\
0 & 0 & \cdots & u_{nn} & \mid & d_n
\end{bmatrix}.
$$

Eso es lo que se buscaba, porque la **última** ecuación ya tiene una sola
incógnita ($u_{nn}x_n = d_n$): se despeja de inmediato y luego se sube renglón
por renglón. De eso se encarga el subtema 1.4.

> ⚠️ En este subtema se supone que **todos los pivotes son distintos de cero**.
> Si alguno vale cero o es muy pequeño, hace falta lo del subtema 1.3 (pivoteo).

**🧮 Ejemplo algebraico.** En un sistema $2\times2$ hay un solo paso. El pivote es
$a_{11}$ y el multiplicador $m_{21} = a_{21}/a_{11}$. Al restar
$R_2 \leftarrow R_2 - m_{21}R_1$ la matriz aumentada pasa de

$$
\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}
\quad\longrightarrow\quad
\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ 0 & a_{22}' & \mid & b_2' \end{bmatrix},
$$

donde $a_{22}' = a_{22} - m_{21}a_{12}$ y $b_2' = b_2 - m_{21}b_1$. La segunda
ecuación queda $a_{22}'x_2 = b_2'$, ya despejable.

**🔢 Versión con enteros (paso a paso).** Sistema

$$\mathbf{A} = \begin{bmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{bmatrix},
\qquad \mathbf{b} = \begin{bmatrix} 8 \\ -11 \\ -3 \end{bmatrix}.$$

1. **Matriz aumentada de partida:**

$$[\mathbf{A}\mid\mathbf{b}] = \begin{bmatrix}
2 & 1 & -1 & \mid & 8 \\
-3 & -1 & 2 & \mid & -11 \\
-2 & 1 & 2 & \mid & -3
\end{bmatrix}.$$

2. **Paso $k=1$: eliminar $x_1$ de los renglones 2 y 3.** El pivote es
   $a_{11} = 2 \neq 0$.

   - Renglón 2: $m_{21} = \dfrac{-3}{2}$. Como $R_2 - m_{21}R_1 = R_2 + \tfrac{3}{2}R_1$,
     se calcula primero $\tfrac{3}{2}R_1 = \left(3,\ \tfrac{3}{2},\ -\tfrac{3}{2} \mid 12\right)$
     y luego
     $$R_2 + \tfrac{3}{2}R_1 = \left(0,\ \tfrac{1}{2},\ \tfrac{1}{2} \mid 1\right).$$
   - Renglón 3: $m_{31} = \dfrac{-2}{2} = -1$. Como $R_3 - m_{31}R_1 = R_3 + R_1$,
     $$R_3 + R_1 = \left(0,\ 2,\ 1 \mid 5\right).$$

   La matriz queda

$$[\mathbf{A}^{(1)}\mid\mathbf{b}^{(1)}] = \begin{bmatrix}
2 & 1 & -1 & \mid & 8 \\
0 & \tfrac{1}{2} & \tfrac{1}{2} & \mid & 1 \\
0 & 2 & 1 & \mid & 5
\end{bmatrix}.$$

3. **Paso $k=2$: eliminar $x_2$ del renglón 3.** El pivote ahora es
   $a_{22} = \tfrac{1}{2} \neq 0$ y
   $m_{32} = \dfrac{2}{1/2} = 4$. Con $4R_2 = \left(0,\ 2,\ 2 \mid 4\right)$,

   $$R_3 - 4R_2 = \left(0,\ 0,\ -1 \mid 1\right).$$

4. **Resultado: la matriz quedó triangular superior.**

$$\mathbf{U} = \begin{bmatrix} 2 & 1 & -1 \\ 0 & \tfrac{1}{2} & \tfrac{1}{2} \\ 0 & 0 & -1 \end{bmatrix},
\qquad \mathbf{d} = \begin{bmatrix} 8 \\ 1 \\ 1 \end{bmatrix}.$$

5. **Comprobación:** los pivotes usados fueron $2$, $\tfrac{1}{2}$ y $-1$. Ninguno
   es cero, así que la eliminación corrió completa. La solución
   $\mathbf{x} = [2,\ 3,\ -1]$ se obtiene en el subtema 1.4.

---

### <a id="sec-1-3"></a>1.3 Estrategia de Pivoteo Parcial Por Renglón

**📘 Teoría.**

El subtema 1.2 supuso que todos los pivotes son distintos de cero. Eso no siempre
se cumple, y cuando falla el método se rompe. Hay dos maneras de fallar.

#### Falla 1: un pivote igual a cero

Recordemos que el multiplicador es $m_{ik} = a_{ik}/a_{kk}$. Si el pivote vale
cero, se divide entre cero y el método **no puede continuar**. Por ejemplo:

$$
\begin{aligned}
0\,x_1 + x_2 &= 1\\
x_1 + x_2 &= 3
\end{aligned}
\qquad\Longrightarrow\qquad
m_{21} = \frac{1}{0} \;\; \text{(no existe).}
$$

Lo importante es notar que **el sistema sí tiene solución** ($x_1 = 2$, $x_2 = 1$);
lo que falla es el **orden** en que se escribieron las ecuaciones. Si se
intercambian, el pivote pasa a ser $1$ y el método avanza sin problema.

#### Falla 2: un pivote muy pequeño (pero distinto de cero)

Este caso es más peligroso porque **no da error**: entrega un resultado creíble y
equivocado. Supongamos

$$
\begin{aligned}
10^{-18}\,x_1 + x_2 &= 1\\
x_1 + x_2 &= 2
\end{aligned}
$$

cuya solución verdadera es $x_1 \approx 1$, $x_2 \approx 1$. El pivote es
$a_{11} = 10^{-18}$, pequeño pero válido, así que el método procede:

$$m_{21} = \frac{1}{10^{-18}} = 10^{18}.$$

Un multiplicador **un billón de veces más grande** que los datos originales. Al
restar $R_2 \leftarrow R_2 - 10^{18}R_1$:

- coeficiente de $x_2$: $1 - 10^{18}(1) = -10^{18}$
- lado derecho: $2 - 10^{18}(1) = -10^{18}$

De ahí $x_2 = \dfrac{-10^{18}}{-10^{18}} = 1$, que sale bien. Pero al despejar
$x_1$:

$$x_1 = \frac{1 - x_2}{10^{-18}} = \frac{1 - 1}{10^{-18}} = \frac{0}{10^{-18}} = 0,$$

cuando debía dar $x_1 \approx 1$. **El resultado está completamente mal.**

El motivo es que al calcular $1 - x_2$ se restan dos números casi iguales: el
valor verdadero de la diferencia es del orden de $10^{-18}$, más pequeño que la
precisión con que se representan esos números. Se pierden **todos** los dígitos
significativos y la resta devuelve cero. Después, dividir ese cero entre
$10^{-18}$ no recupera nada.

Con pivoteo, en cambio, se intercambian los renglones, el pivote pasa a ser $1$,
los multiplicadores quedan pequeños y el resultado es $x_1 = x_2 = 1$: correcto.

#### La estrategia: elegir el mayor de la columna

El **pivoteo parcial** consiste en no aceptar el pivote que toca por posición,
sino **elegir el de mayor magnitud** de la columna. Antes de eliminar en el paso
$k$ se busca

$$p = \arg\max_{i = k,\, k+1,\, \dots,\, n} \left| a_{ik}^{(k)} \right|,$$

es decir, el renglón $p$ donde el coeficiente de la columna $k$ es el más grande
en valor absoluto. Si $p \neq k$, se intercambian los renglones completos:

$$R_k \longleftrightarrow R_p.$$

Recién entonces se calculan los multiplicadores.

#### Por qué esto resuelve el problema

Después del intercambio, el pivote es el mayor de su columna, así que para
cualquier otro renglón

$$|m_{ik}| = \left| \frac{a_{ik}}{a_{kk}} \right| \le 1.$$

Los multiplicadores ya **no amplifican** nada: restar $m_{ik}$ veces un renglón
resta una cantidad del mismo orden de magnitud que el renglón mismo, y los
errores de redondeo no se multiplican. Además, el intercambio garantiza que el
pivote no sea cero (salvo que la columna entera sea cero, y en ese caso el
sistema no tiene solución única).

> 💡 En la práctica **casi todos los programas hacen pivoteo siempre**, aunque el
> pivote parezca aceptable. Cuesta muy poco y evita los dos problemas a la vez.

#### Efecto sobre el determinante

Cada intercambio de renglones cambia el signo del determinante, pero no su valor
absoluto. Por eso, contando los intercambios $p_{\text{swaps}}$:

$$\det(\mathbf{A}) = (-1)^{p_{\text{swaps}}} \prod_{k=1}^{n} u_{kk}.$$

**🧮 Ejemplo algebraico.** Para una matriz $2\times2$ el criterio compara solo dos
candidatos. Si $|a_{21}| > |a_{11}|$ se elige $p = 2$ y se intercambian los
renglones:

$$
\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ a_{21} & a_{22} & \mid & b_2 \end{bmatrix}
\;\xrightarrow{R_1 \leftrightarrow R_2}\;
\begin{bmatrix} a_{21} & a_{22} & \mid & b_2 \\ a_{11} & a_{12} & \mid & b_1 \end{bmatrix}.
$$

El nuevo pivote es $a_{21}$ y el determinante cambia de signo una vez:
$\det(\mathbf{A}) = (-1)^{1} u_{11}u_{22}$.

**🔢 Versión con enteros (paso a paso).** Sistema

$$\mathbf{A} = \begin{bmatrix} 0 & 1 \\ 1 & 1 \end{bmatrix},
\qquad \mathbf{b} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}.$$

1. **Se revisa la columna 1.** Los candidatos son $|a_{11}| = 0$ y $|a_{21}| = 1$.
2. **Se elige el mayor:** $p = 2$, porque $1 > 0$. El pivote $a_{11} = 0$ haría
   imposible calcular $m_{21}$, así que hay que intercambiar.
3. **Se aplica $R_1 \leftrightarrow R_2$:**

$$\mathbf{A} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix},
\qquad \mathbf{b} = \begin{bmatrix} 3 \\ 1 \end{bmatrix}.$$

4. **Ahora el pivote es $1$**, distinto de cero, y se puede eliminar:
   $m_{21} = 0/1 = 0$. Restar cero veces el renglón 1 no cambia nada, así que la
   matriz ya quedó triangular.
5. **Solución** (se detalla en el subtema 1.4): de la última ecuación
   $1\cdot x_2 = 1$ se obtiene $x_2 = 1$; y del primer renglón,
   $x_1 + x_2 = 3 \Rightarrow x_1 = 2$.
6. **Comprobación:** $\mathbf{x} = [2,\ 1]$ satisface el sistema original
   ($0(2) + 1 = 1$ ✓ y $2 + 1 = 3$ ✓). Hubo un intercambio, así que
   $\det(\mathbf{A}) = (-1)^1 u_{11}u_{22} = -(1)(1) = -1$.

---

### <a id="sec-1-4"></a>1.4 Sustitución Hacia Atrás (*Back Substitution*)

**📘 Teoría.**

#### La forma triangular ya casi está resuelta

Después de la eliminación el sistema quedó así:

$$
\begin{aligned}
u_{11}x_1 + u_{12}x_2 + \cdots + u_{1n}x_n &= d_1\\
u_{22}x_2 + \cdots + u_{2n}x_n &= d_2\\
&\;\;\vdots\\
u_{nn}x_n &= d_n
\end{aligned}
$$

Fíjate en la **última** ecuación: aparece una sola incógnita, $x_n$. No hay
sistema que resolver ahí, solo una división. Y en cuanto $x_n$ es un número
conocido, la **penúltima** ecuación queda con una sola incógnita ($x_{n-1}$),
porque $x_n$ ya se calculó. Y así hacia arriba.

Ese es el motivo del nombre **sustitución hacia atrás**: se empieza por el último
renglón y se sube, renglón por renglón.

#### Las dos fórmulas

**1. La última incógnita.** Del renglón $n$:

$$u_{nn}x_n = d_n \qquad\Longrightarrow\qquad x_n = \frac{d_n}{u_{nn}}.$$

Requiere $u_{nn} \neq 0$; si el pivoteo se hizo bien, lo es.

**2. Las demás, de abajo hacia arriba.** Para $i = n-1, n-2, \dots, 1$:

$$x_i = \frac{d_i - \sum_{j=i+1}^{n} u_{ij}x_j}{u_{ii}}.$$

La suma $\sum_{j=i+1}^{n}$ recorre **solo las incógnitas a la derecha de la
diagonal** en el renglón $i$, que son justamente las que ya se calcularon. Por eso
en cada paso no queda ninguna incógnita desconocida.

Por ejemplo, en el renglón $n-1$ la suma tiene **un solo término**:

$$x_{n-1} = \frac{d_{n-1} - u_{n-1,\,n}\,x_n}{u_{n-1,\,n-1}}.$$

En el renglón $n-2$ tiene dos, y así sucesivamente hasta el primer renglón, donde
la suma recorre todas las incógnitas ya conocidas.

#### Por qué no se puede empezar por arriba

Si se intentara despejar $x_1$ del primer renglón, aparecerían $x_2, \dots, x_n$:
un problema con $n-1$ incógnitas, es decir, el mismo problema otra vez. Solo al
empezar por abajo se tiene **una** incógnita por ecuación.

#### Costo

Esta fase requiere del orden de $n^2$ operaciones, mucho menos que las
$\tfrac{2}{3}n^3$ de la eliminación. El detalle está en el subtema 1.5.

**🧮 Ejemplo algebraico.** Para un sistema $2\times2$ ya triangular,

$$
\begin{bmatrix} a_{11} & a_{12} & \mid & b_1 \\ 0 & a_{22}' & \mid & b_2' \end{bmatrix},
$$

se aplica la fórmula dos veces, de abajo hacia arriba:

$$x_2 = \frac{b_2'}{a_{22}'}, \qquad x_1 = \frac{b_1 - a_{12}x_2}{a_{11}}.$$

La primera división exige $a_{22}' \neq 0$ y la segunda, $a_{11} \neq 0$.

**🔢 Versión con enteros (paso a paso).** Se parte de la forma triangular
obtenida en el subtema 1.2:

$$\mathbf{U} = \begin{bmatrix} 2 & 1 & -1 \\ 0 & \tfrac{1}{2} & \tfrac{1}{2} \\ 0 & 0 & -1 \end{bmatrix},
\qquad \mathbf{d} = \begin{bmatrix} 8 \\ 1 \\ 1 \end{bmatrix}.$$

1. **Renglón 3.** Tiene una sola incógnita: $-1\,x_3 = 1$, entonces
   $$x_3 = \frac{d_3}{u_{33}} = \frac{1}{-1} = -1.$$

2. **Renglón 2.** Ya se conoce $x_3$, así que
   $$\tfrac{1}{2}x_2 + \tfrac{1}{2}x_3 = 1
   \qquad\Longrightarrow\qquad
   x_2 = \frac{d_2 - u_{23}x_3}{u_{22}} = \frac{1 - \tfrac{1}{2}(-1)}{\tfrac{1}{2}}
   = \frac{1 + \tfrac{1}{2}}{\tfrac{1}{2}} = \frac{\tfrac{3}{2}}{\tfrac{1}{2}} = 3.$$

3. **Renglón 1.** Ya se conocen $x_2$ y $x_3$:
   $$2x_1 + x_2 - x_3 = 8
   \qquad\Longrightarrow\qquad
   x_1 = \frac{d_1 - u_{12}x_2 - u_{13}x_3}{u_{11}}
   = \frac{8 - (1)(3) - (-1)(-1)}{2} = \frac{8 - 3 - 1}{2} = \frac{4}{2} = 2.$$

4. **Solución:** $\mathbf{x} = [2,\ 3,\ -1]$.

5. **Comprobación en el sistema original** (no en el triangular, para detectar
   errores arrastrados desde la eliminación):

   - $2(2) + (3) - (-1) = 4 + 3 + 1 = 8$ ✓
   - $-3(2) - (3) + 2(-1) = -6 - 3 - 2 = -11$ ✓
   - $-2(2) + (3) + 2(-1) = -4 + 3 - 2 = -3$ ✓

   Las tres ecuaciones se cumplen, así que la solución es correcta.

---

### <a id="sec-1-5"></a>1.5 Complejidad Computacional

**📘 Teoría.**

#### Qué es un FLOP y para qué contarlos

Un **FLOP** (*floating point operation*) es una operación aritmética entre
números reales: una suma, una resta, una multiplicación o una división. Contarlos
sirve para dos cosas:

1. **Comparar algoritmos** sin depender de la computadora: el método con menos
   FLOPs será más rápido.
2. **Predecir cómo crece el tiempo** al aumentar el tamaño $n$ del sistema.

Se adopta la convención habitual: cada multiplicación, división, suma o resta
cuenta como **1 FLOP**. Una operación combinada del tipo $a - m\cdot c$ cuenta
como **2 FLOPs** (una multiplicación y una resta).

#### Cuánto cuesta la eliminación

En el paso $k$ hay $n-k$ renglones por eliminar. Cada uno cuesta:

| Concepto | FLOPs |
|---|---|
| Calcular el multiplicador $m_{ik} = a_{ik}/a_{kk}$ | $1$ |
| Actualizar los coeficientes de las columnas $k+1$ a $n$ ($n-k$ productos y $n-k$ restas) | $2(n-k)$ |
| Actualizar el lado derecho $b_i$ (un producto y una resta) | $2$ |
| **Total por renglón** | $2(n-k)+3$ |

Multiplicando por los $n-k$ renglones y sumando sobre todos los pasos:

$$C_{\text{elim}} = \sum_{k=1}^{n-1}(n-k)\left[2(n-k)+3\right]
= \frac{n(n-1)(4n+7)}{6}.$$

#### Cuánto cuesta la sustitución hacia atrás

La última incógnita cuesta **1** FLOP (una división). Cada una de las demás
cuesta $2(n-i)$ FLOPs por los productos y restas de la suma, más $1$ por la
división final, es decir $2(n-i)+1$. Sumando:

$$C_{\text{sust}} = 1 + \sum_{i=1}^{n-1}\left[2(n-i)+1\right] = n^{2}.$$

Sencillo y exacto: la sustitución cuesta exactamente $n^2$ FLOPs.

#### Por qué el término cúbico es el que manda

Para $n$ grande, $\dfrac{n(n-1)(4n+7)}{6} \approx \dfrac{2}{3}n^{3}$, mientras que
la sustitución se queda en $n^{2}$. El cociente entre ambos crece sin límite, así
que el costo total es $O(n^{3})$ y lo aporta casi todo la eliminación.

Con números concretos:

| $n$ | Eliminación (exacta) | $\approx\frac{2}{3}n^{3}$ | Sustitución ($n^2$) |
|---:|---:|---:|---:|
| 3 | 19 | 18 | 9 |
| 10 | 645 | 667 | 100 |
| 1\,000 | 667\,165\,500 | 666\,666\,667 | 1\,000\,000 |

La consecuencia práctica: **duplicar** $n$ multiplica el trabajo de eliminación
por $\approx 8$ (porque $2^3 = 8$), mientras que la sustitución solo se
multiplica por $4$. Por eso, cuando $n$ crece, lo único que importa es reducir el
número de operaciones de la eliminación; ahí está el interés de los métodos
especializados (LU, Thomas, Cholesky) que vienen en los subtemas siguientes.

**🧮 Ejemplo algebraico.** La cuenta anterior ya está hecha para $n$ genérico: las
fórmulas $C_{\text{elim}} = \frac{n(n-1)(4n+7)}{6}$ y $C_{\text{sust}} = n^2$ valen
para cualquier tamaño. Si se abre el numerador de la primera,

$$C_{\text{elim}} = \frac{4n^{3} + 3n^{2} - 7n}{6}
= \frac{2}{3}n^{3} + \frac{1}{2}n^{2} - \frac{7}{6}n,$$

se ve de dónde salen los dos términos: el cúbico $\frac{2}{3}n^3$ y el cuadrático
$O(n^2)$, que para $n$ grande queda opacado por el primero.

**🔢 Versión con enteros (paso a paso).** Con $n = 3$ se puede contar a mano,
usando el mismo sistema del subtema 1.2:

1. **Paso $k=1$:** hay $n-k = 2$ renglones por eliminar. Cada uno cuesta
   $2(2)+3 = 7$ FLOPs (1 del multiplicador, $2\cdot2 = 4$ de los coeficientes y 2
   del lado derecho). Total: $2 \times 7 = 14$ FLOPs.
2. **Paso $k=2$:** queda $n-k = 1$ renglón, que cuesta $2(1)+3 = 5$ FLOPs.
3. **Eliminación completa:** $14 + 5 = 19$ FLOPs. La fórmula da
   $\frac{(3)(2)(12+7)}{6} = \frac{3\cdot2\cdot19}{6} = 19$ ✓
4. **Sustitución hacia atrás:** $x_3$ cuesta $1$ FLOP; $x_2$ cuesta
   $2(1)+1 = 3$; $x_1$ cuesta $2(2)+1 = 5$. Total: $1+3+5 = 9$ FLOPs, que es
   $n^{2} = 9$ ✓
5. **Total del método:** $19 + 9 = 28$ FLOPs.
6. **Comparación con la cota:** $\frac{2}{3}n^{3} = 18$ frente al valor exacto
   $19$; la diferencia ($1$ FLOP) viene del término cuadrático que la cota
   desprecia. Para $n = 3$ pesa, pero para $n$ grande deja de importar.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| — | [README](../../README.md) | [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) |

