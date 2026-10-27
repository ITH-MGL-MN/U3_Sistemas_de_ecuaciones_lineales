# 🏭 Casos de Estudio de Ingeniería — Unidad 3: Sistemas de Ecuaciones Lineales ($\mathbf{A}\mathbf{x} = \mathbf{b}$)
### *Materia: Métodos Numéricos para Ingeniería (TecNM / ITH)*

Este documento contiene el catálogo oficial de los **17 Casos de Estudio de Ingeniería** organizados por nivel de complejidad y tamaño de equipo (**de 2 a 6 integrantes**). Cada caso presenta el modelo físico, la formulación matricial $\mathbf{A}\mathbf{x} = \mathbf{b}$, las propiedades de la matriz de coeficientes, el solver numérico recomendado y las métricas de análisis de ingeniería (número de condición $\text{Cond}(\mathbf{A})$, determinantes y estabilidad).

---

## 📊 Resumen General del Catálogo por Tamaño de Equipo

| Bloque | Integrantes | Casos | Rango | Complejidad / Propiedad Matricial |
| :---: | :---: | :---: | :---: | :--- |
| **Bloque A** | **2** | 4 | **T1 – T4** | Sistemas $3 \times 3$ bien condicionados, matrices simétricas y tridiagonales. |
| **Bloque B** | **3** | 5 | **T5 – T9** | Sistemas $4 \times 4$, geometría 2D, pivoteo parcial y dominancia diagonal. |
| **Bloque C** | **4** | 5 | **T10 – T14** | Sistemas $5 \times 5$ a $6 \times 6$, matrices de banda, balances multivariable. |
| **Bloque D** | **5** | 2 | **T15 – T16** | Sistemas 3D y de proceso $6 \times 6$ a $8 \times 8$, mal condicionados ($\text{Cond}(\mathbf{A}) > 10^3$). |
| **Bloque E** | **6** | 1 | **T17** | Redes de potencia $8 \times 8$, matriz de admitancia dispersa e inversión $\mathbf{A}^{-1}$. |

---

## 🗂️ Lista de Casos

# 🔹 BLOQUE A: Equipos de 2 Integrantes (Sistemas $3 \times 3$)

- **T1** · [Análisis de Corrientes de Malla en Circuito de CD](caso_t1.md)
- **T2** · [Análisis de Nodos de Voltaje con Fuentes de Corriente](caso_t2.md)
- **T3** · [Red de Filtros Pasivos RC en Escalera de 3 Etapas](caso_t3.md)
- **T4** · [Conducción Térmica 1D en Barra Discretizada](caso_t4.md)

# 🔹 BLOQUE B: Equipos de 3 Integrantes (Sistemas $4 \times 4$)

- **T5** · [Cercha Plana 2D de Brazo Robótico (4 Nodos / 5 Barras)](caso_t5.md)
- **T6** · [Sistema Masa-Resorte de 4 Masas Acopladas](caso_t6.md)
- **T7** · [Deflexión de Viga Continua sobre Múltiples Apoyos](caso_t7.md)
- **T8** · [Repartición de Cargas en Suspensión Neumática Multieje](caso_t8.md)
- **T9** · [Balance de Materia en 4 Reactores CSTR Acoplados](caso_t9.md)

# 🔹 BLOQUE C: Equipos de 4 Integrantes (Sistemas $5 \times 5$ a $6 \times 6$)

- **T10** · [Conducción Térmica 2D en Placa Rectangular](caso_t10.md)
- **T11** · [Distribución de Caudales en Red de Tuberías Linealizada](caso_t11.md)
- **T12** · [Estequiometría de Combustión Compleja](caso_t12.md)
- **T13** · [Modelo Insumo-Producto de Leontief](caso_t13.md)
- **T14** · [Separación por Etapas en Columna de Destilación](caso_t14.md)

# 🔹 BLOQUE D: Equipos de 5 Integrantes (Sistemas 3D y Mal Condicionados)

- **T15** · [Cercha Espacial 3D para Brazo/Torre de Soporte](caso_t15.md)
- **T16** · [Red de Intercambiadores de Calor Serie/Paralelo](caso_t16.md)

# 🔹 BLOQUE E: Equipos de 6 Integrantes (Reto Integrador $8 \times 8$)

- **T17** · [Flujo de Carga Linealizado (DC Power Flow) en Red de Potencia](caso_t17.md)
