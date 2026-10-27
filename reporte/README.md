# 📄 Plantilla de Reporte (LaTeX)

Plantilla para el reporte del **Caso de Estudio** de la Unidad 3. Réplica de la
estructura de `U2_T4_Reporte`, adaptada a **sistemas de ecuaciones lineales**.

## Estructura

```text
reporte/
├── main.tex                  <- documento principal (compila todo)
├── clases.cls                <- clase/estilo del documento (no modificar)
├── fuentes.bib               <- bibliografía (opcional)
├── portada/
│   └── portada.tex           <- portada (nombre, caso, integrantes)
├── secciones/
│   ├── 01_introduccion.tex
│   ├── 02_modelo.tex
│   ├── 03_metodologia.tex
│   ├── 04_resultados.tex
│   └── 05_conclusion.tex
└── img/                      <- figuras del Monte Carlo (boxplot, histogramas)
```

## Cómo compilar

```bash
# En la carpeta reporte/ (con un LaTeX completo, p. ej. TeX Live / MiKTeX):
pdflatex main.tex     # (2 veces para referencias)
# o con latexmk:
latexmk -pdf main.tex
```

En [Overleaf](https://overleaf.com) basta con subir la carpeta `reporte/` y compilar `main.tex`.

## Qué reemplazar

1. **`portada/portada.tex`**: nombre del caso, integrantes y **foto** (`perfil1.jpg`).
2. **`secciones/*.tex`**: el contenido guiado de cada sección (sigue los comentarios `%`).
3. **`secciones/04_resultados.tex`**: pega los resultados que exporta el **Cuaderno 04**
   (`resultados.tex`) y las figuras de `img/`.

> 💡 El Cuaderno 04 genera `resultados.tex` con la matriz, el vector y la tabla de
> métodos. Cópialo a esta carpeta y descomenta `\input{resultados}`.
