# Descomposición LU e Inversión de Matrices

### 2.1 Motivación e Idea Central
En muchas aplicaciones de ingeniería (ej. análisis de circuitos o estructuras sujetas a múltiples combinaciones de carga), es necesario resolver $\mathbf{A}\mathbf{x} = \mathbf{b}$ para **múltiples vectores independientes $\mathbf{b}$** manteniendo la misma matriz de estructura $\mathbf{A}$.

La Eliminación Gaussiana estándar repite el trabajo pesado $O(n^3)$ para cada nuevo vector $\mathbf{b}$. La **descomposición LU** separa el trabajo computacional:
1. **Factorización ($O(n^3)$):** Descompone la matriz $\mathbf{A}$ en dos matrices triangulares tal que $\mathbf{A} = \mathbf{L}\mathbf{U}$.
2. **Sustitución ($O(n^2)$):** Resuelve el sistema para cualquier vector $\mathbf{b}$ en tiempo cuadrático mediante sustituciones hacia adelante y hacia atrás.

---

### 2.2 Estrategia de Solución en Dos Pasos

Dado el sistema $\mathbf{A}\mathbf{x} = \mathbf{b}$ y la factorización $\mathbf{A} = \mathbf{L}\mathbf{U}$:

$$\mathbf{L}\mathbf{U}\mathbf{x} = \mathbf{b}$$

Definiendo un vector intermedio $\mathbf{d} = \mathbf{U}\mathbf{x}$:

1. **Paso 1: Sustitución Hacia Adelante (Forward Substitution)**
   Se resuelve el sistema triangular inferior $\mathbf{L}\mathbf{d} = \mathbf{b}$ para hallar $\mathbf{d}$:
   $$d_1 = \frac{b_1}{l_{11}}$$
   $$d_i = \frac{b_i - \sum_{j=1}^{i-1} l_{ij} d_j}{l_{ii}}, \quad \text{para } i = 2, \dots, n$$

2. **Paso 2: Sustitución Hacia Atrás (Back Substitution)**
   Se resuelve el sistema triangular superior $\mathbf{U}\mathbf{x} = \mathbf{d}$ para hallar la solución final $\mathbf{x}$:
   $$x_n = \frac{d_n}{u_{nn}}$$
   $$x_i = \frac{d_i - \sum_{j=i+1}^n u_{ij} x_j}{u_{ii}}, \quad \text{para } i = n-1, \dots, 1$$

---

### 2.3 Variantes de Factorización

#### A. Factorización de Doolittle
* La matriz $\mathbf{L}$ es triangular inferior con **unos en la diagonal principal** ($l_{ii} = 1$).
* La matriz $\mathbf{U}$ es triangular superior.
* Los elementos fuera de la diagonal de $\mathbf{L}$ son exactamente los **multiplicadores de eliminación de Gauss** $m_{ik} = \frac{a_{ik}}{a_{kk}}$ obtenidos durante la eliminación hacia adelante *(véase [Sección 1.2](./01_eliminacion_gaussiana.md))*.

$$\mathbf{L} = \begin{bmatrix}
1 & 0 & 0 \\
m_{21} & 1 & 0 \\
m_{31} & m_{32} & 1
\end{bmatrix}, \quad
\mathbf{U} = \begin{bmatrix}
u_{11} & u_{12} & u_{13} \\
0 & u_{22} & u_{23} \\
0 & 0 & u_{33}
\end{bmatrix}$$

#### B. Factorización de Crout
* La matriz $\mathbf{U}$ es triangular superior con **unos en la diagonal principal** ($u_{ii} = 1$).
* La matriz $\mathbf{L}$ es triangular inferior y contiene los coeficientes de escala.

Fórmulas de Crout para la columna $j$ y renglón $i$:
$$l_{ij} = a_{ij} - \sum_{k=1}^{j-1} l_{ik} u_{kj}, \quad \text{para } i = j, \dots, n$$
$$u_{jk} = \frac{a_{jk} - \sum_{i=1}^{j-1} l_{ji} u_{ik}}{l_{jj}}, \quad \text{para } k = j+1, \dots, n$$

---

### 2.4 Cálculo Eficiente de la Matriz Inversa $\mathbf{A}^{-1}$

La matriz inversa $\mathbf{X} = \mathbf{A}^{-1}$ satisface:

$$\mathbf{A}\mathbf{X} = \mathbf{I}$$

donde $\mathbf{I}$ es la matriz identidad de $n \times n$. Denotando $\mathbf{x}^{(j)}$ como la $j$-ésima columna de $\mathbf{A}^{-1}$ y $\mathbf{e}^{(j)}$ como el $j$-ésimo vector canónico unitario de $\mathbf{I}$:

$$\mathbf{A}\mathbf{x}^{(j)} = \mathbf{e}^{(j)}, \quad \text{para } j = 1, \dots, n$$

#### Procedimiento:
1. Se descompone la matriz $\mathbf{A}$ en $\mathbf{L}\mathbf{U}$ una sola vez ($O(n^3)$).
2. Se realizan $n$ resoluciones independientes usando los vectores canónicos $\mathbf{e}^{(1)}, \mathbf{e}^{(2)}, \dots, \mathbf{e}^{(n)}$ como lados derechos.
3. Cada columna $\mathbf{x}^{(j)}$ toma $O(n^2)$ operaciones. El costo total para obtener $\mathbf{A}^{-1}$ es de $\frac{4}{3} n^3$ FLOPs.

---

### 2.5 Condicionamiento del Sistema y Normas Matriciales

#### Número de Condición $\text{Cond}(\mathbf{A})$
Mide la sensibilidad de la solución $\mathbf{x}$ ante pequeñas variaciones o errores en los datos de entrada ($\mathbf{A}$ o $\mathbf{b}$):

$$\text{Cond}(\mathbf{A}) = \|\mathbf{A}\| \cdot \|\mathbf{A}^{-1}\|$$

Usando la **norma renglón-suma ($\|\cdot\|_\infty$)**:

$$\|\mathbf{A}\|_\infty = \max_{1 \le i \le n} \sum_{j=1}^n |a_{ij}|$$

#### Cota de Error Relativo:
$$\frac{\|\Delta \mathbf{x}\|}{\|\mathbf{x}\|} \le \text{Cond}(\mathbf{A}) \cdot \frac{\|\Delta \mathbf{A}\|}{\|\mathbf{A}\|}$$

* **Sistema Bien Condicionado:** $\text{Cond}(\mathbf{A}) \approx 1$.
* **Sistema Mal Condicionado:** $\text{Cond}(\mathbf{A}) \gg 10^k$ (se pueden perder hasta $k$ dígitos de precisión por error de redondeo).

---

---

## 🔢 Ejemplo resuelto paso a paso

Factorizamos la misma matriz del ejemplo de Gauss por **Doolittle**:

$$\mathbf{A} = \begin{bmatrix} 3 & -0.1 & -0.2 \\ 0.1 & 7 & -0.3 \\ 0.3 & -0.2 & 10 \end{bmatrix}$$

**Paso $k=1$:** $U_{1,:} = [3,\ -0.1,\ -0.2]$. Los multiplicadores forman la columna de $\mathbf{L}$:

$$l_{21} = \frac{0.1}{3} = 0.0333, \qquad l_{31} = \frac{0.3}{3} = 0.1$$

**Paso $k=2$:** $U_{2,:} = [0,\ 7.00333,\ -0.29333]$ y $l_{32} = -0.19/7.00333 = -0.02713$.

**Paso $k=3$:** $U_{3,:} = [0,\ 0,\ 10.0120]$.

Resultado:

$$\mathbf{L} = \begin{bmatrix} 1 & 0 & 0 \\ 0.0333 & 1 & 0 \\ 0.1 & -0.02713 & 1 \end{bmatrix}, \qquad \mathbf{U} = \begin{bmatrix} 3 & -0.1 & -0.2 \\ 0 & 7.00333 & -0.29333 \\ 0 & 0 & 10.0120 \end{bmatrix}$$

Comprobamos $\mathbf{A} = \mathbf{L}\mathbf{U}$ multiplicando. Para resolver $\mathbf{A}\mathbf{x}=\mathbf{b}$:

**Sustitución hacia adelante** ($\mathbf{L}\mathbf{d}=\mathbf{b}$): $d_1 = 7.85$, $d_2 = -19.5617$, $d_3 = 70.0843$.

**Sustitución hacia atrás** ($\mathbf{U}\mathbf{x}=\mathbf{d}$): $\mathbf{x} = [3,\ -2.5,\ 7]^T$.

> 💡 **¿Para qué sirve?** Si tienes que resolver el sistema con **muchos** vectores $\mathbf{b}$ distintos (misma matriz $\mathbf{A}$), factorizas una sola vez ($O(n^3)$) y cada solución nueva cuesta solo $O(n^2)$.

---

> [📚 Volver al README](../../README.md) · [🏭 Casos de estudio](../casos/casos_index.md)

