---
id: esp_02
titulo: Jacobi contra Gauss-Seidel
---

Los dos métodos despejan cada incógnita de su propia ecuación, pero no usan la
misma información dentro de la misma iteración.

**¿Cuál es la diferencia esencial?**

- [x] Gauss-Seidel usa de inmediato cada valor recién calculado; Jacobi usa el vector completo de la iteración anterior
- [ ] Jacobi converge siempre y Gauss-Seidel solo si la matriz es dominante
- [ ] Gauss-Seidel necesita calcular la matriz inversa en cada paso
- [ ] Jacobi hace una sola iteración y Gauss-Seidel itera hasta la tolerancia
