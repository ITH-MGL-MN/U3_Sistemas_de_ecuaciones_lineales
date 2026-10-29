---
id: lu_02
titulo: Por qué L lleva unos en la diagonal
---

La factorización $\mathbf{A} = \mathbf{L}\mathbf{U}$ **no es única**: hay $n^2+n$
incógnitas y solo $n^2$ ecuaciones. Para que quede determinada se fija una de las
dos diagonales.

En la variante de **Doolittle** se impone $l_{ii} = 1$.

**¿Qué se gana con esa elección?**

- [x] Que $\mathbf{L}$ guarde tal cual los multiplicadores y $\mathbf{U}$ cargue los pivotes actualizados, sin mezclar escalas
- [ ] Que $\mathbf{A}$ quede simétrica
- [ ] Que $\mathbf{U}$ sea siempre la matriz identidad
- [ ] Que el determinante de $\mathbf{A}$ valga 1
