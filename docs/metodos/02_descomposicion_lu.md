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

**📘 Teoría.** El condicionamiento mide cuánto se amplifica en la solución $\mathbf{x}$ un error cometido en los datos ($\mathbf{A}$ o $\mathbf{b}$). Se cuantifica con el número de condición

$$\text{Cond}(\mathbf{A}) = \|\mathbf{A}\| \cdot \|\mathbf{A}^{-1}\|.$$

Con la **norma renglón-suma** ($\|\cdot\|_\infty$), que suma el valor absoluto de cada renglón y toma el máximo,

$$\|\mathbf{A}\|_\infty = \max_{1 \le i \le n} \sum_{j=1}^{n} |a_{ij}|,$$

la perturbación del lado derecho se acota por

$$\frac{\|\Delta\mathbf{x}\|}{\|\mathbf{x}\|} \le \text{Cond}(\mathbf{A})\,\frac{\|\Delta\mathbf{b}\|}{\|\mathbf{b}\|}.$$

Un sistema bien condicionado tiene $\text{Cond}(\mathbf{A}) \approx 1$; si $\text{Cond}(\mathbf{A}) \gg 10^{k}$ se pueden perder hasta $k$ dígitos de precisión.

**🧮 Ejemplo algebraico.** Para una matriz $2\times 2$ genérica,

$$\|\mathbf{A}\|_\infty = \max\left(|a_{11}| + |a_{12}|,\ |a_{21}| + |a_{22}|\right),$$

y con $\mathbf{A}^{-1} = \begin{bmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{bmatrix}$ se calcula igual, renglón por renglón. El número de condición es el producto de las dos normas; como $\text{Cond}(\mathbf{A}) = \text{Cond}(\mathbf{A}^{-1})$, la cifra no depende de cuál de las dos matrices se tome como referencia.

**🔢 Versión con enteros (paso a paso).** Con

$$\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}, \qquad \mathbf{A}^{-1} = \begin{bmatrix} 3/5 & -1/5 \\ -1/5 & 2/5 \end{bmatrix}.$$

1. Norma de $\mathbf{A}$: renglón 1 suma $2 + 1 = 3$; renglón 2 suma $1 + 3 = 4$. Por lo tanto $\|\mathbf{A}\|_\infty = 4$.
2. Norma de $\mathbf{A}^{-1}$: renglón 1 suma $3/5 + 1/5 = 4/5$; renglón 2 suma $1/5 + 2/5 = 3/5$. Por lo tanto $\|\mathbf{A}^{-1}\|_\infty = 4/5$.
3. Número de condición: $\text{Cond}(\mathbf{A}) = 4 \cdot \tfrac{4}{5} = \tfrac{16}{5} = 3.2$.
4. Interpretación: $3.2$ está cerca de $1$, así que el sistema está **bien condicionado** y un error relativo en $\mathbf{b}$ se amplifica poco más de tres veces.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Eliminación Gaussiana y Pivoteo Parcial](01_eliminacion_gaussiana.md) | [README](../../README.md) | [Métodos Iterativos: Gauss-Seidel y Relajación](03_metodos_iterativos.md) |

