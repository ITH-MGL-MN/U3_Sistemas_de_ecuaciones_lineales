# Referencias Cruzadas y Matriz Comparativa de Desempeño

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) | [README](../../README.md) | [Casos de estudio](../casos/casos_index.md) |

## 📑 Índice

1. [📌 Enlaces Relacionados en el Repositorio](#sec-enlaces)

| Método Numérico | Tipo de Algoritmo | Complejidad Temporal | Memoria Requerida | Requisito de Estabilidad / Convergencia | Caso de Uso Ideal en Ingeniería |
|---|---|:---:|:---:|---|---|
| **Eliminación Gaussiana** | Directo | $O(n^3)$ | $O(n^2)$ | Sensible a $a_{kk}=0$; requiere **Pivoteo Parcial** | Sistemas densos pequeños/medianos con un solo lado derecho $\mathbf{b}$. |
| **Descomposición LU** | Directo | $O(n^3)$ decomp. / $O(n^2)$ sust. | $O(n^2)$ | Requiere Pivoteo Parcial ($P A = L U$) | Sistemas con la misma matriz $\mathbf{A}$ y **múltiples vectores $\mathbf{b}$**; cálculo de $\mathbf{A}^{-1}$. |
| **Gauss-Seidel** | Iterativo | $O(k \cdot n^2)$ | $O(n)$ (dispersas) | Requiere **Dominancia Diagonal Estricta** | Matrices dispersas de gran escala ($n \ge 10,000$); libre de error de redondeo acumulado. |
| **Algoritmo de Thomas** | Directo (LU Especial) | **$O(n)$** | **$O(n)$** | Sin pivoteo si es diagonalmente dominante | Sistemas **tridiagonales** (redes térmicas, diferencias finitas 1D). |
| **Factorización de Cholesky** | Directo | $\frac{1}{3} n^3$ ($O(n^3)$) | $\frac{1}{2} O(n^2)$ | Matriz **Simétrica y Definida Positiva** | Mecánica de estructuras, optimización de energía y ajuste por mínimos cuadrados. |

---

### <a id="sec-enlaces"></a>📌 Enlaces Relacionados en el Repositorio:
* 🌐 [Regresar al README Principal del Repositorio](../../README.md)
* 🧪 [Ejecutar Laboratorio de Álgebra Lineal en Colab (Notebook 01)](../../notebooks/01_Algebra_Lineal.ipynb)
* 🏭 [Consultar Casos de Estudio de Ingeniería](../../docs/casos/)

---

| ⬅️ Anterior | 🏠 Inicio | Siguiente ➡️ |
|:---|:---:|---:|
| [Matrices Especiales: Algoritmo de Thomas y Cholesky](04_matrices_especiales.md) | [README](../../README.md) | [Casos de estudio](../casos/casos_index.md) |

