# Métodos Iterativos: Gauss-Seidel y Relajación

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) | [README](../../README.md) | [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) |

## 📑 Índice

1. [3.1 Fundamento de los Métodos Iterativos](#sec-3-1)
2. [3.2 Algoritmo de Gauss-Seidel](#sec-3-2)
3. [3.3 Condición de Dominancia Diagonal Estricta](#sec-3-3)
4. [3.4 Mejoramiento de Convergencia con Relajación (SOR)](#sec-3-4)
5. [3.5 Criterio de Paro por Error Relativo](#sec-3-5)

### <a id="sec-3-1"></a>3.1 Fundamento de los Métodos Iterativos

**📘 Teoría.** Un método **directo** (Gauss, LU) transforma la matriz y entrega la solución en un número finito y predecible de pasos, con costo $O(n^{3})$. Un método **iterativo** hace lo contrario: parte de un vector inicial $\mathbf{x}^{(0)}$ y genera la sucesión

$$\mathbf{x}^{(0)},\ \mathbf{x}^{(1)},\ \mathbf{x}^{(2)},\ \dots,\ \mathbf{x}^{(k)},\ \dots$$

deteniéndose cuando la aproximación cumple una tolerancia de error. Cada iteración solo recorre los coeficientes de $\mathbf{A}$ para despejar cada incógnita de su propia ecuación:

$$x_i = \frac{b_i - \sum_{j \neq i} a_{ij}x_j}{a_{ii}}, \qquad a_{ii} \neq 0.$$

La ventaja aparece con **matrices dispersas y grandes**, donde casi todos los coeficientes son cero y una eliminación sería un desperdicio de memoria y tiempo. La desventaja es que la convergencia no está garantizada: depende de la matriz, del $\mathbf{x}^{(0)}$ y del criterio de paro.

**🧮 Ejemplo algebraico.** Para un sistema $2\times 2$ con letras,

$$\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} b_1 \\ b_2 \end{bmatrix},$$

el esquema iterativo despeja cada incógnita de su ecuación diagonal:

$$x_1^{(k+1)} = \frac{b_1 - a_{12}x_2^{(k)}}{a_{11}}, \qquad x_2^{(k+1)} = \frac{b_2 - a_{21}x_1^{(k)}}{a_{22}}.$$

Se ve de inmediato la condición mínima: $a_{11}$ y $a_{22}$ deben ser distintos de cero. El superíndice $(k)$ marca qué valores se usan en cada actualización.

**🔢 Versión con enteros (paso a paso).** Se usa en todo el documento

$$\mathbf{A} = \begin{bmatrix} 4 & 1 & -1 \\ 2 & 7 & 1 \\ 1 & -3 & 12 \end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 3 \\ 19 \\ 31 \end{bmatrix},$$

cuya solución exacta es $\mathbf{x} = [1,\ 2,\ 3]$.

1. Se verifica la solución sustituyendo en la primera ecuación: $4(1) + 1(2) - 1(3) = 3$, que es $b_1$.
2. Se elige el arranque $\mathbf{x}^{(0)}$, normalmente el vector de ceros.
3. Se itera hasta que el cambio entre iteraciones sea menor que la tolerancia.

---

### <a id="sec-3-2"></a>3.2 Algoritmo de Gauss-Seidel

**📘 Teoría.** De la ecuación $i$-ésima del sistema,

$$a_{i1}x_1 + \dots + a_{ii}x_i + \dots + a_{in}x_n = b_i,$$

se despeja la incógnita diagonal: $x_i = \left(b_i - \sum_{j \neq i} a_{ij}x_j\right)/a_{ii}$. La diferencia con el esquema ingenuo es que Gauss-Seidel **reutiliza de inmediato** cada valor recién calculado:

$$x_i^{(k+1)} = \frac{b_i - \displaystyle\sum_{j=1}^{i-1} a_{ij}x_j^{(k+1)} - \sum_{j=i+1}^{n} a_{ij}x_j^{(k)}}{a_{ii}}.$$

Es decir: para las incógnitas anteriores usa la iteración nueva (ya disponible) y para las posteriores, la vieja. El ciclo avanza en orden $i = 1, 2, \dots, n$; como aprovecha información recién actualizada, suele converger más rápido que retener todo el vector viejo.

**🧮 Ejemplo algebraico.** Para $n = 2$ el esquema se escribe completo, en orden:

$$x_1^{(k+1)} = \frac{b_1 - a_{12}x_2^{(k)}}{a_{11}}, \qquad x_2^{(k+1)} = \frac{b_2 - a_{21}x_1^{(k+1)}}{a_{22}}.$$

Nota el superíndice: en la segunda fórmula ya aparece $x_1^{(k+1)}$, no $x_1^{(k)}$. Esa sustitución inmediata es todo el algoritmo.

**🔢 Versión con enteros (paso a paso).** Con la matriz del subtema 3.1, $\mathbf{b} = [3,\ 19,\ 31]$ y $\mathbf{x}^{(0)} = [0,\ 0,\ 0]$, tolerancia $10^{-6}$:

1. **Iteración 1.**
   - $x_1 = 3/4 = 0.7500$ (renglón 1: $4x_1 = 3$).
   - $x_2 = 5/2 = 2.5000$ (usa el $x_1$ recién obtenido).
   - $x_3 = 151/48 \approx 3.1458$ (usa $x_1$ y $x_2$ nuevos).
   - Estado: $\mathbf{x}^{(1)} \approx [0.7500,\ 2.5000,\ 3.1458]$.
2. **Iteración 2.**
   - $x_1 = 175/192 \approx 0.9115$.
   - $x_2 = 449/224 \approx 2.0045$.
   - $x_3 = 48521/16128 \approx 3.0085$.
   - Estado: $\mathbf{x}^{(2)} \approx [0.9115,\ 2.0045,\ 3.0085]$.
3. **Iteración 3:** $\mathbf{x}^{(3)} \approx [1.0010,\ 1.9985,\ 2.9999]$.
4. Se observa el acercamiento a la solución exacta $[1,\ 2,\ 3]$; los errores relativos máximos fueron $0.1647$ en la iteración 2 y $0.0299$ en la 3.

---

### <a id="sec-3-3"></a>3.3 Condición de Dominancia Diagonal Estricta

**📘 Teoría.** La garantía de convergencia más usada es la **dominancia diagonal estricta por renglones**: en cada ecuación, el coeficiente de la incógnita despejada pesa más que la suma de los demás coeficientes de esa ecuación,

$$|a_{ii}| > \sum_{j=1,\, j \neq i}^{n} |a_{ij}|, \qquad \forall i \in \{1,\dots,n\}.$$

Si se cumple, Gauss-Seidel converge a la solución única para cualquier $\mathbf{x}^{(0)}$. La condición no es necesaria —hay matrices no dominantes que convergen—, pero sí es suficiente y fácil de verificar antes de programar.

Cuando un renglón no la cumple, reordenar las ecuaciones (intercambiar renglones) puede convertir la matriz en dominante; basta con emparejar cada incógnita con la ecuación donde tiene el coeficiente mayor.

**🧮 Ejemplo algebraico.** Para un sistema $3\times 3$ con letras, las tres condiciones son

$$|a_{11}| > |a_{12}| + |a_{13}|, \qquad |a_{22}| > |a_{21}| + |a_{23}|, \qquad |a_{33}| > |a_{31}| + |a_{32}|.$$

Si una falla, por ejemplo $|a_{11}| < |a_{12}| + |a_{13}|$, el método puede divergir; reordenando los renglones de modo que la diagonal acumule los coeficientes mayores se puede recuperar la condición.

**🔢 Versión con enteros (paso a paso).** Con la matriz del subtema 3.1:

$$\mathbf{A} = \begin{bmatrix} 4 & 1 & -1 \\ 2 & 7 & 1 \\ 1 & -3 & 12 \end{bmatrix}.$$

1. Renglón 1: $|4| > |1| + |-1|$, es decir $4 > 2$. Se cumple.
2. Renglón 2: $|7| > |2| + |1|$, es decir $7 > 3$. Se cumple.
3. Renglón 3: $|12| > |1| + |-3|$, es decir $12 > 4$. Se cumple.
4. La matriz es estrictamente dominante y por eso las iteraciones del subtema 3.2 avanzan hacia $[1,\ 2,\ 3]$.
5. **Contraejemplo:** con $\mathbf{A} = \begin{bmatrix} 1 & 3 \\ 4 & 1 \end{bmatrix}$ el primer renglón da $1 < 3$, la dominancia falla y el método diverge.

---

### <a id="sec-3-4"></a>3.4 Mejoramiento de Convergencia con Relajación (SOR)

**📘 Teoría.** La **sobrerrelajación sucesiva (SOR)** no toma el valor de Gauss-Seidel tal cual, sino un promedio ponderado con el valor de la iteración anterior:

$$x_i^{\text{nuevo}} = \lambda\, x_i^{\text{Gauss-Seidel}} + (1 - \lambda)\, x_i^{\text{anterior}}, \qquad \lambda \in (0, 2).$$

El factor $\lambda$ decide qué tanto se cree al valor nuevo:

- $0 < \lambda < 1$: **sub-relajación**, amortigua oscilaciones.
- $\lambda = 1$: recupera exactamente Gauss-Seidel.
- $1 < \lambda < 2$: **sobrerrelajación**, acelera sistemas que ya convergen pero avanzan lento.

Fuera del intervalo $(0,2)$ el esquema se vuelve inestable, de ahí la restricción.

**🧮 Ejemplo algebraico.** Para $n = 2$, aplicando la fórmula componente por componente,

$$x_1^{\text{nuevo}} = \lambda\,\frac{b_1 - a_{12}x_2^{\text{anterior}}}{a_{11}} + (1-\lambda)x_1^{\text{anterior}},$$
$$x_2^{\text{nuevo}} = \lambda\,\frac{b_2 - a_{21}x_1^{\text{nuevo}}}{a_{22}} + (1-\lambda)x_2^{\text{anterior}}.$$

Si $\lambda = 1$ ambas expresiones colapsan en las de Gauss-Seidel; si $\lambda > 1$ el término nuevo se amplifica y el viejo se resta parcialmente.

**🔢 Versión con enteros (paso a paso).** Misma matriz y mismo $\mathbf{x}^{(0)} = [0,0,0]$ del subtema 3.2, con $\lambda = 1.2$:

1. Se calcula primero el valor de Gauss-Seidel de cada componente, en orden.
2. Se pondera: $1.2$ veces el valor nuevo menos $0.2$ veces el anterior.
3. Tras la **iteración 1** el resultado es

$$\mathbf{x}^{(1)} = \left[\frac{9}{10},\ \frac{516}{175},\ \frac{13631}{3500}\right] \approx [0.9000,\ 2.9486,\ 3.8946].$$

4. Comparado con Gauss-Seidel puro, que en la iteración 1 daba $[0.7500,\ 2.5000,\ 3.1458]$, la sobrerrelajación avanza más hacia la solución $[1,\ 2,\ 3]$.

---

### <a id="sec-3-5"></a>3.5 Criterio de Paro por Error Relativo

**📘 Teoría.** Un método iterativo necesita una regla para detenerse. La más común compara, componente por componente, el valor nuevo contra el anterior:

$$\varepsilon_{a,i} = \left| \frac{x_i^{(k+1)} - x_i^{(k)}}{x_i^{(k+1)}} \right| \times 100\% < \varepsilon_s, \qquad \forall i = 1,\dots,n.$$

La norma práctica es el **máximo** de los $\varepsilon_{a,i}$: se detiene cuando la componente que más cambió ya cambió poco. Se usa error relativo y no absoluto para que el criterio no dependa de la escala de las incógnitas.

La división entre $x_i^{(k+1)}$ trae un detalle: si una componente vale cero, el error relativo no está definido y hay que tratarla aparte, por ejemplo esperando a que la componente sea distinta de cero o revisando el cambio absoluto.

**🧮 Ejemplo algebraico.** Para $n = 2$ el criterio exige las dos condiciones a la vez:

$$\left| \frac{x_1^{(k+1)} - x_1^{(k)}}{x_1^{(k+1)}} \right| \times 100 < \varepsilon_s
\quad \text{y} \quad
\left| \frac{x_2^{(k+1)} - x_2^{(k)}}{x_2^{(k+1)}} \right| \times 100 < \varepsilon_s.$$

Si una sola de las dos falla, la iteración continúa. El error reportado en la tabla de resultados es el máximo de las dos.

**🔢 Versión con enteros (paso a paso).** Con los resultados del subtema 3.2:

1. **Iteración 1:** no se puede calcular error relativo porque el vector anterior es $\mathbf{x}^{(0)} = [0,0,0]$ y la fórmula divide entre el valor nuevo. El error se reporta como "—".
2. **Iteración 2:** el error relativo máximo es $0.1647$ (un $16.47\%$), todavía lejos de la tolerancia de $10^{-6}$.
3. **Iteración 3:** el error relativo máximo baja a $0.0299$ (un $2.99\%$). Sigue siendo mayor que la tolerancia, así que el algoritmo continuaría.
4. La tendencia —de $0.1647$ a $0.0299$— muestra convergencia: el criterio de paro aún no se satisface en la iteración 3.

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Descomposición LU e Inversión de Matrices](02_descomposicion_lu.md) | [README](../../README.md) | [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) |

