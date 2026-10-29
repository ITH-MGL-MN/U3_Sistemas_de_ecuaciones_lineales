# Referencias Cruzadas y Matriz Comparativa de Desempeño

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) | [README](../../README.md) | [Casos de estudio](../casos/casos_index.md) |

## 📑 Índice

1. [📌 Enlaces Relacionados en el Repositorio](#sec-enlaces)

| Método Numérico | Tipo de Algoritmo | Complejidad Temporal | Memoria Requerida | Requisito de Estabilidad / Convergencia | Caso de Uso Ideal en Ingeniería |
|---|---|:---:|:---:|---|---|
| **Eliminación Gaussiana** | Directo | $O(n^3)$ | $O(n^2)$ | Falla con $a_{kk}=0$; requiere **Pivoteo Parcial**. El error de redondeo se amplifica según el [número de condición](02_descomposicion_lu.md#sec-2-5) | Sistemas densos pequeños/medianos con un solo lado derecho $\mathbf{b}$. |
| **Descomposición LU** | Directo | $O(n^3)$ para factorizar, $O(n^2)$ por cada sustitución | $O(n^2)$ | Necesita **Pivoteo Parcial** ($\mathbf{P}\mathbf{A} = \mathbf{L}\mathbf{U}$) por la misma razón que Gauss | Sistemas con la misma matriz $\mathbf{A}$ y **múltiples vectores $\mathbf{b}$**; cálculo de $\mathbf{A}^{-1}$. |
| **Gauss-Seidel** | Iterativo | $O(n^2)$ **por iteración**; el total depende de cuántas haga falta | $O(n^2)$ si es densa, y ahí pierde el sentido | Converge seguro con **Dominancia Diagonal Estricta**; en general converge si el [radio espectral](03_metodos_iterativos.md#sec-3-6) es menor que $1$ | Matrices **dispersas** de gran escala ($n \ge 10{,}000$), donde una eliminación gastaría memoria en ceros. |
| **Algoritmo de Thomas** | Directo (LU Especial) | **$O(n)$** | **$O(n)$** | Sin pivoteo; es estable si la matriz es diagonalmente dominante | Sistemas **tridiagonales** (redes térmicas, diferencias finitas 1D). |
| **Factorización de Cholesky** | Directo | $\tfrac{1}{3}n^3$ ($O(n^3)$) | $O(n^2)$, y solo se guarda la mitad inferior | Exige matriz **Simétrica y Definida Positiva**; con eso **no necesita pivoteo** | Mecánica de estructuras, optimización de energía y ajuste por mínimos cuadrados. |

**Dos advertencias que la tabla no puede decir sola.**

1. Un método iterativo **no** está libre de error de redondeo: arrastra el suyo en cada iteración. Lo que no hace es acumular la transformación completa de la matriz, que es otra cosa. Su ventaja real es **memoria y estructura**, no precisión.
2. La dominancia diagonal es una condición **suficiente, no necesaria**: hay matrices que no la cumplen y convergen igual (ver el contraejemplo de la [sección 3.6](03_metodos_iterativos.md#sec-3-6)).

---

### <a id="sec-enlaces"></a>📌 Enlaces Relacionados en el Repositorio:
* 🌐 [Regresar al README Principal del Repositorio](../../README.md)
* 🧪 [Ejecutar Laboratorio de Álgebra Lineal en Colab (Notebook 01)](../../notebooks/U3_01_Algebra_Lineal.ipynb)
* 🏭 [Consultar Casos de Estudio de Ingeniería](../../docs/casos/)

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) | [README](../../README.md) | [Casos de estudio](../casos/casos_index.md) |

