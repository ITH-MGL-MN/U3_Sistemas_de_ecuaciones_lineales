---
id: esp_03
titulo: Qué gana el algoritmo de Thomas
---

Una matriz **tridiagonal** solo tiene coeficientes distintos de cero en la
diagonal y en las dos diagonales vecinas. El algoritmo de Thomas aprovecha esa
estructura.

**¿Qué se gana frente a aplicarle eliminación gaussiana normal?**

- [x] Baja de $O(n^{3})$ a $O(n)$ en tiempo y de $O(n^{2})$ a $O(n)$ en memoria, porque nunca guarda los ceros
- [ ] Baja el costo de $O(n)$ a $O(\log n)$
- [ ] Permite usar pivoteo sin intercambiar renglones
- [ ] Calcula directamente la inversa de la matriz
