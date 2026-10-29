---
id: lu_03
titulo: Cuándo conviene factorizar LU
---

Factorizar cuesta lo mismo que una eliminación gaussiana, $O(n^3)$. Resolver
después cada sistema triangular cuesta $O(n^2)$.

**¿En cuál de estos casos LU ahorra trabajo de verdad?**

- [x] Cuando hay que resolver muchos sistemas con la **misma** $\mathbf{A}$ y distintos $\mathbf{b}$
- [ ] Cuando hay que resolver un solo sistema y no se vuelve a usar $\mathbf{A}$
- [ ] Cuando la matriz es de $2\times2$ o $3\times3$
- [ ] Cuando la matriz $\mathbf{A}$ es simétrica
