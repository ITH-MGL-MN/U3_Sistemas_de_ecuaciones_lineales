# Descomposición LU e Inversión de Matrices

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Eliminación Gaussiana y Pivoteo Parcial](01_eliminacion_gaussiana.md) | [README](../../README.md) | [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) |

## 📑 Índice

1. [2.1 Motivación e Idea Central](#sec-2-1)
2. [2.2 Estrategia de Solución en Dos Pasos](#sec-2-2)
3. [2.3 Variantes de Factorización](#sec-2-3)
4. [2.4 Cálculo Eficiente de la Matriz Inversa $\mathbf{A}^{-1}$](#sec-2-4)
5. [2.5 Condicionamiento del Sistema y Normas Matriciales](#sec-2-5)

### <a id="sec-2-1"></a>2.1 Motivación e Idea Central

**📘 Teoría.** En muchas aplicaciones hay que resolver $\mathbf{A}\mathbf{x} = \mathbf{b}$ con la **misma** matriz $\mathbf{A}$ y muchos vectores $\mathbf{b}$ distintos (por ejemplo, varias combinaciones de carga sobre la misma estructura). Hacer eliminación gaussiana completa para cada $\mathbf{b}$ repite el trabajo pesado cada vez.

La descomposición LU separa ese trabajo en dos etapas mediante la factorización

$$\mathbf{A} = \mathbf{L}\mathbf{U},$$

con $\mathbf{L}$ triangular inferior y $\mathbf{U}$ triangular superior. Una vez factorizada la matriz, el costo es $O(n^{3})$ **una sola vez** y después $O(n^{2})$ por cada nuevo $\mathbf{b}$.

**🧮 Ejemplo algebraico.** Para una matriz $2\times 2$ la factorización tiene una forma cerrada: buscando $\mathbf{L}$ con unos en la diagonal,

$$\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} =
\begin{bmatrix} 1 & 0 \\ m_{21} & 1 \end{bmatrix}
\begin{bmatrix} u_{11} & u_{12} \\ 0 & u_{22} \end{bmatrix},$$

e igualando entrada por entrada se obtiene

$$u_{11} = a_{11}, \qquad u_{12} = a_{12}, \qquad m_{21} = \frac{a_{21}}{a_{11}}, \qquad u_{22} = a_{22} - m_{21}a_{12}.$$

Es decir: $u_{11}$ y $u_{12}$ son el primer renglón de $\mathbf{A}$, y $m_{21}$, $u_{22}$ son exactamente el multiplicador y el pivote actualizado de la eliminación. El sistema se resuelve luego como $\mathbf{L}(\mathbf{U}\mathbf{x}) = \mathbf{b}$, sin volver a tocar $\mathbf{A}$.

**🔢 Versión con enteros (paso a paso).** Se usa la misma matriz del documento anterior:

$$\mathbf{A} = \begin{bmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 8 \\ -11 \\ -3 \end{bmatrix}.$$

1. **Sin LU:** si aparecen dos vectores $\mathbf{b}$ distintos, se hacen **dos eliminaciones** completas, cada una de costo $O(n^{3})$.
2. **Con LU:** se factoriza una vez y se resuelven **dos sustituciones** por cada $\mathbf{b}$, de costo $O(n^{2})$ cada una.
3. Con $n=3$ la diferencia todavía no se nota, pero crece rápido. Tomando como medidas las multiplicaciones de la eliminación,
4. Si el segundo lado derecho es $\mathbf{b}^{(2)} = [1,\ 2,\ 3]$, al resolverlo con la **misma** $\mathbf{L}$ y $\mathbf{U}$ se obtiene $\mathbf{y}^{(2)} = [1,\ 7/2,\ -10]$ y $\mathbf{x}^{(2)} = [7,\ -3,\ 10]$, sin volver a tocar $\mathbf{A}$.
5. La cuenta del ahorro: hacer $k$ eliminaciones cuesta $k\,n^{3}/3$ multiplicaciones; factorizar una vez y sustituir $k$ veces cuesta $n^{3}/3 + k\,n^{2}$. Para $k=2$ la factorización empieza a ganar cuando $n > 6$: con $n=10$ son $667$ contra $533$, y con $n=100$, $666\,667$ contra $353\,333$.

En resumen: **LU no ahorra en un sistema pequeño ni en un solo lado derecho**. Ahorra cuando la matriz se reutiliza.

---

### <a id="sec-2-2"></a>2.2 Estrategia de Solución en Dos Pasos

**📘 Teoría.** Con $\mathbf{A} = \mathbf{L}\mathbf{U}$, el sistema $\mathbf{A}\mathbf{x} = \mathbf{b}$ se reescribe como

$$\mathbf{L}\mathbf{U}\mathbf{x} = \mathbf{b}.$$

Se introduce un vector intermedio $\mathbf{y} = \mathbf{U}\mathbf{x}$ y el problema se parte en dos sistemas triangulares:

$$\mathbf{L}\mathbf{y} = \mathbf{b} \qquad \text{(sustitución hacia adelante)},$$
$$\mathbf{U}\mathbf{x} = \mathbf{y} \qquad \text{(sustitución hacia atrás)}.$$

Como $\mathbf{L}$ es triangular inferior, $\mathbf{y}$ se obtiene de arriba hacia abajo con

$$y_1 = \frac{b_1}{l_{11}}, \qquad y_i = \frac{b_i - \sum_{j=1}^{i-1} l_{ij}y_j}{l_{ii}}, \quad i = 2, \dots, n,$$

y luego $\mathbf{x}$ se obtiene de abajo hacia arriba con

$$x_n = \frac{y_n}{u_{nn}}, \qquad x_i = \frac{y_i - \sum_{j=i+1}^{n} u_{ij}x_j}{u_{ii}}, \quad i = n-1, \dots, 1.$$

Cada sustitución cuesta $O(n^{2})$: eso es lo que se gana al no repetir la eliminación.

**🧮 Ejemplo algebraico.** Con $\mathbf{L} = \begin{bmatrix} 1 & 0 \\ m_{21} & 1 \end{bmatrix}$ y $\mathbf{U} = \begin{bmatrix} u_{11} & u_{12} \\ 0 & u_{22} \end{bmatrix}$:

$$y_1 = b_1, \qquad y_2 = b_2 - m_{21}y_1,$$

$$x_2 = \frac{y_2}{u_{22}}, \qquad x_1 = \frac{y_1 - u_{12}x_2}{u_{11}}.$$

Ninguna de las cuatro fórmulas toca la matriz $\mathbf{A}$ original: todo sale de entradas ya calculadas de $\mathbf{L}$ y $\mathbf{U}$.

**🔢 Versión con enteros (paso a paso).** Se factoriza la matriz del subtema 2.1 y se toma $\mathbf{b} = [8,\ -11,\ -3]$:

$$\mathbf{L} = \begin{bmatrix} 1 & 0 & 0 \\ -3/2 & 1 & 0 \\ -1 & 4 & 1 \end{bmatrix}.$$

1. Renglón 1: $y_1 = b_1 = 8$.
2. Renglón 2: $y_2 = -11 + 12 = 1$ (es $b_2 - l_{21}y_1$ con $l_{21} = -3/2$).
3. Renglón 3: $y_3 = -3 + 8 - 4 = 1$ (es $b_3 - l_{31}y_1 - l_{32}y_2$).
4. Resultado intermedio: $\mathbf{y} = [8,\ 1,\ 1]$.
5. Con $\mathbf{U}$ triangular superior, la sustitución hacia atrás sobre $\mathbf{y}$ entrega $\mathbf{x} = [2,\ 3,\ -1]$, la misma solución del método directo.

---

### <a id="sec-2-3"></a>2.3 Variantes de Factorización

**📘 Teoría.** La factorización $\mathbf{A} = \mathbf{L}\mathbf{U}$ no es única: hay $n^{2}+n$ incógnitas y solo $n^{2}$ ecuaciones, así que sobra libertad para fijar una diagonal. De ahí las dos convenciones usuales.

**Doolittle** fija $l_{ii} = 1$ y deja libre la diagonal de $\mathbf{U}$. Las entradas de $\mathbf{L}$ son los multiplicadores de Gauss y las de $\mathbf{U}$ son los pivotes ya actualizados:

$$u_{kj} = a_{kj} - \sum_{i=1}^{k-1} l_{ki}u_{ij}, \qquad l_{ik} = \frac{a_{ik} - \sum_{j=1}^{k-1} l_{ij}u_{jk}}{u_{kk}}.$$

**Crout** fija $u_{ii} = 1$; ahora la diagonal escala en $\mathbf{L}$:

$$l_{ik} = a_{ik} - \sum_{j=1}^{k-1} l_{ij}u_{jk}, \qquad u_{kj} = \frac{a_{kj} - \sum_{i=1}^{k-1} l_{ki}u_{ij}}{l_{kk}}.$$

Doolittle es la variante natural si ya se programó eliminación gaussiana; Crout evita divisiones al construir las columnas.

**🧮 Ejemplo algebraico.** Para $n = 2$ con Doolittle, las recurrencias se reducen a

$$u_{11} = a_{11}, \quad u_{12} = a_{12}, \quad l_{21} = \frac{a_{21}}{u_{11}}, \quad u_{22} = a_{22} - l_{21}u_{12},$$

mientras que con Crout ($u_{11} = u_{22} = 1$) se invierte el reparto:

$$l_{11} = a_{11}, \quad l_{21} = a_{21}, \quad u_{12} = \frac{a_{12}}{l_{11}}, \quad l_{22} = a_{22} - l_{21}u_{12}.$$

Ambas producen la misma $\mathbf{A}$; solo cambia qué matriz carga la escala.

**🔢 Versión con enteros (paso a paso).** Doolittle aplicado a

$$\mathbf{A} = \begin{bmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{bmatrix}.$$

1. Paso $k=1$: el primer renglón de $\mathbf{U}$ es $[2,\ 1,\ -1]$ y los multiplicadores forman la columna de $\mathbf{L}$: $l_{21} = -3/2$, $l_{31} = -1$.
2. Paso $k=2$: $u_{22} = 1/2$, $u_{23} = 1/2$ y $l_{32} = 4$.
3. Paso $k=3$: $u_{33} = -1$.
4. Resultado:

$$\mathbf{L} = \begin{bmatrix} 1 & 0 & 0 \\ -3/2 & 1 & 0 \\ -1 & 4 & 1 \end{bmatrix}, \qquad
\mathbf{U} = \begin{bmatrix} 2 & 1 & -1 \\ 0 & 1/2 & 1/2 \\ 0 & 0 & -1 \end{bmatrix}.$$

5. Verificación $k$-ésima renglón por renglón con $\mathbf{L}\mathbf{U} = \mathbf{A}$: la fila 1 da $[2,\ 1,\ -1]$; la fila 2 da $[-3,\ -1,\ 2]$; la fila 3 da $[-2,\ 1,\ 2]$. Coincide con $\mathbf{A}$.

---

### <a id="sec-2-4"></a>2.4 Cálculo Eficiente de la Matriz Inversa $\mathbf{A}^{-1}$

**📘 Teoría.** La inversa $\mathbf{X} = \mathbf{A}^{-1}$ es la matriz que satisface

$$\mathbf{A}\mathbf{X} = \mathbf{I}.$$

Vista por columnas, esa igualdad son $n$ sistemas independientes: si $\mathbf{x}^{(j)}$ es la columna $j$ de $\mathbf{X}$ y $\mathbf{e}^{(j)}$ es el $j$-ésimo vector canónico de la identidad, entonces

$$\mathbf{A}\mathbf{x}^{(j)} = \mathbf{e}^{(j)}, \qquad j = 1, \dots, n.$$

El procedimiento es: factorizar $\mathbf{A} = \mathbf{L}\mathbf{U}$ **una sola vez** ($O(n^{3})$) y resolver los $n$ sistemas con los vectores canónicos como lados derechos, a $O(n^{2})$ cada uno. El costo total de obtener $\mathbf{A}^{-1}$ es $\tfrac{4}{3}n^{3}$ FLOPs.

**🧮 Ejemplo algebraico.** Para $n = 2$ las dos columnas se resuelven por separado:

$$\mathbf{A}\mathbf{x}^{(1)} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \qquad \mathbf{A}\mathbf{x}^{(2)} = \begin{bmatrix} 0 \\ 1 \end{bmatrix},$$

y la inversa se arma pegando los resultados:

$$\mathbf{A}^{-1} = \begin{bmatrix} \mid & \mid \\ \mathbf{x}^{(1)} & \mathbf{x}^{(2)} \\ \mid & \mid \end{bmatrix}.$$

Cada columna usa la misma $\mathbf{L}$ y la misma $\mathbf{U}$; lo único que cambia es el lado derecho.

**🔢 Versión con enteros (paso a paso).** Con

$$\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}:$$

1. La inversa verificada es

$$\mathbf{A}^{-1} = \begin{bmatrix} 3/5 & -1/5 \\ -1/5 & 2/5 \end{bmatrix}.$$

2. Comprobación por columnas: la primera columna de $\mathbf{A}\mathbf{A}^{-1}$ es $2(3/5) + 1(-1/5) = 1$ y $1(3/5) + 3(-1/5) = 0$.
3. La segunda columna es $2(-1/5) + 1(2/5) = 0$ y $1(-1/5) + 3(2/5) = 1$.
4. Como $\mathbf{A}\mathbf{A}^{-1} = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = \mathbf{I}$, la inversa es correcta.

---

### <a id="sec-2-5"></a>2.5 Condicionamiento del Sistema y Normas Matriciales

**📘 Teoría.**

Hasta aquí está el método: cómo se calcula $\mathbf{x}$. Falta la otra mitad de
la pregunta, que en ingeniería pesa igual: **¿cuánto se puede confiar en el
resultado?** Un sistema puede resolverse sin un solo error de cuenta y aun así
dar una respuesta inútil, porque el problema mismo amplifica cualquier
imprecisión de los datos.

Para hablar del "tamaño" de un error hay que medir vectores. De eso se encarga
una **norma**: una función que asigna a cada vector un número no negativo y que
cumple tres propiedades.

$$\|\mathbf{x}\| \ge 0, \qquad \|\alpha\mathbf{x}\| = |\alpha|\,\|\mathbf{x}\|, \qquad \|\mathbf{x} + \mathbf{y}\| \le \|\mathbf{x}\| + \|\mathbf{y}\|$$

La primera dice que solo el vector nulo mide cero; la segunda, que al escalar un
vector su norma escala igual; la tercera es la desigualdad del triángulo. Lo
importante: **hay muchas normas válidas**. Cada una mide el tamaño a su manera y
todas sirven, mientras se use la misma en los dos lados de una comparación.

Las dos más fáciles de calcular a mano son

$$\|\mathbf{x}\|_1 = \sum_{i} |x_i| \qquad \text{y} \qquad \|\mathbf{x}\|_\infty = \max_{i} |x_i|,$$

es decir, la suma de los valores absolutos y la componente mayor en valor
absoluto. También existe la euclidiana $\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}$,
pero para matrices exige autovalores, así que en este curso se trabaja con la
$\infty$.

**La norma de una matriz** no se define aparte: se deduce de la del vector, como
el máximo estiramiento que la matriz puede producir,

$$\|\mathbf{A}\| = \max_{\|\mathbf{x}\| = 1} \|\mathbf{A}\mathbf{x}\|.$$

De esa definición salen dos fórmulas que sí se calculan sin optimizar nada:

$$\|\mathbf{A}\|_1 = \max_{j} \sum_{i} |a_{ij}| \qquad \text{y} \qquad \|\mathbf{A}\|_\infty = \max_{i} \sum_{j} |a_{ij}|.$$

Fíjate en el intercambio, que es la fuente de casi todos los errores: para un
**vector**, la $\infty$ toma el máximo de las **componentes**; para una
**matriz**, el máximo de las **sumas por renglón**. Y la norma $1$ de una matriz
suma por **columnas**, no por renglones.

**¿Por qué la $\infty$ y no otra?** Porque en el sistema
$\mathbf{A}\mathbf{x} = \mathbf{b}$ cada renglón es una ecuación. La norma
$\infty$ mide el error de la ecuación **peor**, que es la que arruina el
resultado. Es la norma natural para la pregunta "¿cuál es el peor error que
tengo?"

**Número de condición.** Con eso ya se puede medir la fragilidad del sistema:

$$\text{Cond}(\mathbf{A}) = \|\mathbf{A}\| \cdot \|\mathbf{A}^{-1}\| \;\ge\; 1.$$

Su sentido es el de un factor de amplificación. Si $\mathbf{b}$ trae un error
relativo $\delta$, la solución puede traer hasta

$$\frac{\|\Delta\mathbf{x}\|}{\|\mathbf{x}\|} \;\le\; \text{Cond}(\mathbf{A})\,\frac{\|\Delta\mathbf{b}\|}{\|\mathbf{b}\|}.$$

El mismo factor aplica a los errores en $\mathbf{A}$ y a los de redondeo que
introduce el propio algoritmo. Y como $\text{Cond}(\mathbf{A}) = \text{Cond}(\mathbf{A}^{-1})$, la cifra describe al sistema completo, no a una de las dos matrices.

**Cuántos dígitos se pierden.** Un `float64` guarda unos $16$ dígitos
($\varepsilon \approx 2.2\times 10^{-16}$). Cada factor de $10$ en el número de
condición se come un dígito:

$$\text{dígitos confiables} \approx 16 - \log_{10}\text{Cond}(\mathbf{A}).$$

Con $\text{Cond} \approx 10^{10}$ quedan $6$ dígitos: el programa puede estar
perfecto y la respuesta ya no servir.

> ⚠️ Este es el **mismo** fenómeno de la
> [sección 1.3](01_eliminacion_gaussiana.md#sec-1-3), donde un pivote diminuto
> amplificaba el error. La diferencia es de quién es la culpa: allá el problema
> estaba en el **algoritmo** y se arreglaba con pivoteo; aquí está en el
> **problema** y ningún pivoteo lo salva.

**🧮 Ejemplo algebraico.** Para una matriz $2\times 2$ genérica las dos normas son

$$\|\mathbf{A}\|_\infty = \max\left(|a_{11}| + |a_{12}|,\ |a_{21}| + |a_{22}|\right),$$

y con $\mathbf{A}^{-1} = \begin{bmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{bmatrix}$ se calcula igual, renglón por renglón. El número de condición es el producto de las dos.

**🔢 Versión con enteros (paso a paso).** Primero un sistema **bien** condicionado, con

$$\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}, \qquad \mathbf{A}^{-1} = \begin{bmatrix} 3/5 & -1/5 \\ -1/5 & 2/5 \end{bmatrix}.$$

1. Norma de $\mathbf{A}$: el renglón 1 suma $2 + 1 = 3$ y el 2 suma $1 + 3 = 4$. Entonces $\|\mathbf{A}\|_\infty = 4$.
2. Norma de $\mathbf{A}^{-1}$: el renglón 1 suma $3/5 + 1/5 = 4/5$ y el 2 suma $1/5 + 2/5 = 3/5$. Entonces $\|\mathbf{A}^{-1}\|_\infty = 4/5$.
3. Número de condición: $\text{Cond}(\mathbf{A}) = 4 \cdot \tfrac{4}{5} = \tfrac{16}{5} = 3.2$.
4. Interpretación: $3.2$ está cerca de $1$, el sistema está **bien condicionado** y un error relativo en $\mathbf{b}$ se amplifica poco más de tres veces.

Ahora uno **mal** condicionado, con entradas que parecen inofensivas:

$$\mathbf{B} = \begin{bmatrix} 10 & 7 \\ 7 & 5 \end{bmatrix}, \qquad \mathbf{B}^{-1} = \begin{bmatrix} 5 & -7 \\ -7 & 10 \end{bmatrix}, \qquad \det(\mathbf{B}) = 1.$$

1. $\|\mathbf{B}\|_\infty$: renglones $10 + 7 = 17$ y $7 + 5 = 12$. Toma el máximo, $17$.
2. $\|\mathbf{B}^{-1}\|_\infty$: renglones $5 + 7 = 12$ y $7 + 10 = 17$. También $17$.
3. $\text{Cond}(\mathbf{B}) = 17 \cdot 17 = 289$. Es $90$ veces peor que el anterior, y la matriz no tiene nada raro: determinante $1$, entradas de un dígito.
4. Para ver qué significa, se resuelve $\mathbf{B}\mathbf{x} = \mathbf{b}$ con $\mathbf{b} = [17,\ 12]$, cuya solución exacta es $\mathbf{x} = [1,\ 1]$.
5. Se perturba el lado derecho en una décima: $\mathbf{b}' = [17.1,\ 11.9]$, un cambio de $0.1/17 = 0.59\,\%$. La nueva solución es

$$\mathbf{x}' = \mathbf{B}^{-1}\begin{bmatrix} 17.1 \\ 11.9 \end{bmatrix} = \begin{bmatrix} 2.2 \\ -0.7 \end{bmatrix}.$$

6. El error relativo en $\mathbf{x}$ es $1.7/1 = 170\,\%$. **Un cambio del $0.59\,\%$ en los datos movió la solución un $170\,\%$**: se perdió el signo de la segunda incógnita. El cociente entre las dos cifras es $170/0.59 = 289$, exactamente el número de condición: la cota no era pesimista, era justa.

**📊 Para tener escala** (norma $\infty$, valores verificados):

| Matriz | $\text{Cond}_\infty$ | Lectura |
|---|---|---|
| $\begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}$ | $3.2$ | bien condicionada, no hay de qué preocuparse |
| $\begin{bmatrix} 10 & 7 \\ 7 & 5 \end{bmatrix}$ | $289$ | se pierden ~$2$ dígitos; ya se nota |
| Hilbert $3\times3$ | $748$ | matriz de interpolación, famosa por esto |
| $\begin{bmatrix} 1 & 1 \\ 1 & 1.0001 \end{bmatrix}$ | $4\times 10^{4}$ | se pierden ~$4$ dígitos |

La última es la trampa clásica: dos renglones **casi** iguales. Geométricamente
son dos rectas casi paralelas, y su punto de corte se mueve muchísimo si se
mueve una de las dos rectas.

**Cómo se calcula en la práctica.** A mano solo para matrices de $2\times2$ o
$3\times3$; en Python, `numpy.linalg.cond(A, numpy.inf)`. **Nunca** se calcula
invirtiendo la matriz a mano en un problema real: para eso existe la
descomposición LU, y el número de condición se estima sin invertir.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Eliminación Gaussiana y Pivoteo Parcial](01_eliminacion_gaussiana.md) | [README](../../README.md) | [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) |

