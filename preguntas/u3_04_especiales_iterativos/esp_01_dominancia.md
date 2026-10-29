---
id: esp_01
titulo: Qué garantiza la dominancia diagonal
---

Una matriz cumple **dominancia diagonal estricta por renglones** cuando, en cada
ecuación, el coeficiente de su propia incógnita pesa más que la suma de los
demás:

$$|a_{ii}| > \sum_{j \neq i} |a_{ij}| \qquad \text{para todo } i$$

**¿Qué se gana si la matriz cumple esa condición?**

- [x] Que Gauss-Seidel (y Jacobi) converjan a la solución para cualquier vector inicial
- [ ] Que la solución del sistema sea única
- [ ] Que el método termine en un número finito y conocido de iteraciones
- [ ] Que la matriz se pueda factorizar como $\mathbf{A} = \mathbf{L}\mathbf{U}$
