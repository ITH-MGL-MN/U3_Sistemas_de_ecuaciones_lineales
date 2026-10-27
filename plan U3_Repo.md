# 🗺️ Plan — Repositorio U3: Sistemas de Ecuaciones Lineales

> Plan de trabajo por fases. Se ejecuta de forma incremental.

## Decisiones base
- **Ubicación:** carpeta nueva limpia `U3_Repo/` dentro de `U3 Sistemas de ecuaciones lineales algebráicas/`.
- **Cuadernos:** 4 (NB1 álgebra intro, NB2 laboratorios+teoría, NB3 selección de casos, NB4 análisis+reporte).
- **Casos:** 17 fichas individuales (`caso_t01.md` … `caso_t17.md`) + índice.
- **Métodos:** 4 documentos + 1 comparativa.
- **Helper:** un solo archivo `lib/` (fusión `matlab_like` + `robomat`).
- **Reporte:** reutilizar plantilla LaTeX de U2 y ajustar secciones.

---

## Fase 0 — Estructura y control de versiones ✅

- [x] Crear `U3_Repo/` con `docs/metodos/`, `docs/casos/`, `notebooks/`, `lib/`, `reporte/`.
- [x] `git init`.
- [x] `.gitignore` (`__pycache__/`, `.ipynb_checkpoints/`, `*.aux`, `build/`, `grader_ofuscado.txt`, temporales).
- [x] No tocar `U3_T1/` ni los borradores fuente.

## Fase 1 — Documentación markdown

- [ ] Partir `metodos_u3_completo.md` → `docs/metodos/` (5 archivos).
- [ ] Partir `casos_u3_completo.md` → `docs/casos/` (17 + índice).
  - ⚠️ Corregir corrupción de secuencias LaTeX (`\b`→0x08, `\t`→0x09, `\f`→0x0C, `\n`→0x0A, `\a`→0x07).
- [ ] Reescribir `README.md` (reconciliado con los 4 cuadernos).

## Fase 2 — Cuadernos Colab (los 4)

- [ ] `01_Algebra_Lineal.ipynb` — fusión `matlab_like` + `robomat`, intro práctica.
- [ ] `02_Laboratorios_Metodos.ipynb` — laboratorios + autograder (MCQ + numéricas), patrón U2_T3B.
- [ ] `03_Seleccion_Casos.ipynb` — registro equipos + asignación determinista por NC, patrón U2_T4_1.
- [ ] `04_Analisis_Casos.ipynb` — cada método en `.py`, comparación manual vs NumPy/SciPy, patrón U2_T4_2.

## Fase 3 — Plantilla de reporte LaTeX

- [ ] `reporte/main.tex`, `clases.cls`, `portada/`, `secciones/` (réplica de U2_T4_Reporte).

## Fase 4 — Integración Colab ↔ Google Sheets / Apps Script

- [ ] Insignias "Open in Colab" en `README.md`.
- [ ] Scripts Apps Script para calificaciones (NB2) y registro de equipos (NB3).
- [ ] Prueba end-to-end.

---

## Orden de ejecución y dependencias

```
Fase 0 ──► Fase 1 ──► Fase 2.1/2.2/2.3 ──► Fase 2.4 ──► Fase 4
        └─► Fase 3 (paralelo)
```
