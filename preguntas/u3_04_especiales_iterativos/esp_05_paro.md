---
id: esp_05
titulo: Cuándo se detiene un método iterativo
---

Un método iterativo no termina solo: hay que decirle cuándo parar. Se usa el
**error relativo** entre dos iteraciones seguidas,

$$\varepsilon_a = \max_i \left| \frac{x_i^{(k+1)} - x_i^{(k)}}{x_i^{(k+1)}} \right| \times 100\%,$$

y se para cuando $\varepsilon_a$ baja de una tolerancia.

**¿Por qué se compara contra la iteración anterior y no contra la solución exacta?**

- [x] Porque la solución exacta no se conoce: para eso se está iterando
- [ ] Porque el error relativo contra la solución exacta siempre vale cero
- [ ] Porque el criterio con la solución exacta nunca converge
- [ ] Porque así el método termina en un número fijo de iteraciones
