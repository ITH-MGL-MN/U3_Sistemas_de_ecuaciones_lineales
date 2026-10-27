# Métodos Iterativos: Gauss-Seidel y Relajación

### 3.1 Fundamento de los Métodos Iterativos
A diferencia de los métodos directos (Gauss y LU) que modifican la matriz completa mediante eliminaciones $O(n^3)$, los **métodos iterativos** parten de un vector estimado inicial $\mathbf{x}^{(0)}$ y generan una secuencia de aproximaciones $\mathbf{x}^{(1)}, \mathbf{x}^{(2)}, \dots, \mathbf{x}^{(k)}$ hasta satisfacer una tolerancia de error.

**Ventajas clave:**
* Ideales para **matrices dispersas de gran escala** ($n \ge 10,000$), donde la memoria para guardar ceros no utilizados es crítica.
* Inmunes a la acumulación desastrosa de errores de redondeo, ya que el error depende exclusivamente de la tolerancia especificada para detener la iteración.

---

### 3.2 Algoritmo de Gauss-Seidel

Dada la ecuación $i$-ésima del sistema $\mathbf{A}\mathbf{x} = \mathbf{b}$:

$$a_{i1}x_1 + a_{i2}x_2 + \dots + a_{ii}x_i + \dots + a_{in}x_n = b_i$$

Despejando la variable diagonal $x_i$:

$$x_i = \frac{b_i - \sum_{j=1, j \neq i}^n a_{ij} x_j}{a_{ii}}$$

#### Regla de Actualización Inmediata de Gauss-Seidel:
Al calcular $x_i^{(k+1)}$ en la iteración $(k+1)$, Gauss-Seidel utiliza **inmediatamente los valores más recientes recién calculados** ($x_1^{(k+1)}, \dots, x_{i-1}^{(k+1)}$) para los componentes previos, y los valores de la iteración anterior ($x_{i+1}^{(k)}, \dots, x_n^{(k)}$) para los componentes restantes:

$$x_i^{(k+1)} = \frac{b_i - \sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)} - \sum_{j=i+1}^n a_{ij} x_j^{(k)}}{a_{ii}}$$

*(A diferencia de la **iteración de Jacobi**, que retiene todos los valores antiguos $\mathbf{x}^{(k)}$ hasta completar el ciclo entero, Gauss-Seidel acelera substancialmente la velocidad de convergencia).*

---

### 3.3 Condición de Dominancia Diagonal Estricta

Para garantizar que el método de Gauss-Seidel converja a la solución única sin importar el vector inicial $\mathbf{x}^{(0)}$, la matriz $\mathbf{A}$ debe ser **estrictamente diagonalmente dominante por renglones**:

$$|a_{ii}| > \sum_{j=1, j \neq i}^n |a_{ij}|, \quad \forall i \in \{1, 2, \dots, n\}$$

* **Significado físico/geométrico:** El elemento diagonal de cada fila tiene mayor magnitud que la suma de todos los demás coeficientes de esa misma fila.
* **Nota:** Si la matriz no es diagonalmente dominante, reordenar los renglones (intercambiar ecuaciones) puede convertirla en dominante.

---

### 3.4 Mejoramiento de Convergencia con Relajación (SOR)

La técnica de **Sobrerrelajación Sucesiva (SOR)** modifica el valor recién calculado por Gauss-Seidel mediante un promedio ponderado con la iteración anterior:

$$x_i^{\text{nuevo}} = \lambda x_i^{\text{Gauss-Seidel}} + (1 - \lambda) x_i^{\text{anterior}}$$

donde $\lambda \in (0, 2)$ es el factor de ponderación:

1. **Sub-relajación ($0 < \lambda < 1$):**  
   Pondera el valor anterior. Se emplea para amortiguar oscilaciones violentas y lograr convergencia en sistemas no diagonalmente dominantes o altamente no lineales.
2. **Sin Relajación ($\lambda = 1$):**  
   Coincide con el algoritmo estándar de Gauss-Seidel.
3. **Sobre-relajación ($1 < \lambda < 2$):**  
   Acelera la velocidad de convergencia en sistemas que ya son convergentes pero avanzan muy lentamente.

---

### 3.5 Criterio de Paro por Error Relativo
La computación se detiene cuando el error relativo aproximado máximo entre todas las componentes sea menor que la tolerancia porcentual $\varepsilon_s$:

$$\varepsilon_{a, i} = \left| \frac{x_i^{(k+1)} - x_i^{(k)}}{x_i^{(k+1)}} \right| \times 100\% < \varepsilon_s, \quad \forall i = 1, \dots, n$$

---

---

## 🔢 Ejemplo resuelto paso a paso

Resolvamos el sistema (diagonal dominante) partiendo de $\mathbf{x}^{(0)} = [0,0,0]^T$:

$$\begin{bmatrix} 3 & -0.1 & -0.2 \\ 0.1 & 7 & -0.3 \\ 0.3 & -0.2 & 10 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 7.85 \\ -19.3 \\ 71.4 \end{bmatrix}$$

**Iteración 1** (despejando y usando los valores recién calculados):

$$x_1 = \frac{7.85}{3} = 2.6167$$

$$x_2 = \frac{-19.3 - 0.1(2.6167)}{7} = -2.7945$$

$$x_3 = \frac{71.4 - 0.3(2.6167) + 0.2(-2.7945)}{10} = 7.0056$$

**Iteración 2:**

$$x_1 = \frac{7.85 + 0.1(-2.7945) + 0.2(7.0056)}{3} = 2.9906$$

$$x_2 = \frac{-19.3 - 0.1(2.9906) + 0.3(7.0056)}{7} = -2.4996$$

$$x_3 = \frac{71.4 - 0.3(2.9906) + 0.2(-2.4996)}{10} = 7.0003$$

| Iteración | $x_1$ | $x_2$ | $x_3$ | Error relativo máx. |
|---|---:|---:|---:|---:|
| 1 | 2.6167 | -2.7945 | 7.0056 | — |
| 2 | 2.9906 | -2.4996 | 7.0003 | 13.1% |
| 3 | 3.0000 | -2.5000 | 7.0000 | 0.02% |

Converge a $\mathbf{x} = [3,\ -2.5,\ 7]^T$ en pocas iteraciones gracias a la **dominancia diagonal**. ✅

> ⚠️ Si la matriz **no** es diagonal dominante, Gauss-Seidel puede **divergir**. Reordena los renglones o usa un método directo.

---

> [📚 Volver al README](../../README.md) · [🏭 Casos de estudio](../casos/casos_index.md)

