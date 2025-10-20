

# 💧 Informe de Implementación — Problema del Riego Óptimo

**Estudiantes:** Kevin Andrés Bejarano,Juan Jose millan, Harrison Valencia , Daniel Camelo
**Curso:** Análisis de Algoritmos II (ADA II)
**Periodo:** 2025-II
**Profesor:** Carlos Andrés Delgado Saavedra

---

## 0. Descripción del problema

El **problema del riego óptimo** consiste en determinar el **orden en que deben regarse los tablones** de una finca para minimizar el “sufrimiento” de los cultivos por falta de agua.

Cada tablón (T_i) tiene tres características:

* (ts_i): tiempo máximo que puede estar sin riego (supervivencia).
* (tr_i): tiempo que tarda en ser regado.
* (p_i): prioridad del tablón (1 = baja, 4 = alta).

La finca se modela como:
[
F = \langle T_0, T_1, \dots, T_{n-1} \rangle
]

El objetivo es encontrar una **permutación óptima** ( \Pi ) que minimice el costo total:

[
CRF_{\Pi} = \sum_{i=0}^{n-1} p_i \cdot \max(0, (t_{\Pi_i} + tr_i) - ts_i)
]

donde (t_{\Pi_i}) representa el instante en que inicia el riego del tablón (i) según el orden (\Pi).

---

## 1. Lenguaje y herramientas usadas

* **Lenguaje:** Python 3.10
* **Bibliotecas estándar:**

  * `time` — para medir tiempos de ejecución.
* **Dependencias externas:**

  * `pytest` — para pruebas unitarias.
  * `numpy` — para manejo de listas y cálculos simples.
* **Entorno:** entorno virtual `venv` para aislar dependencias.

**Motivación:**
Python ofrece una sintaxis clara para modelar algoritmos y facilita la construcción modular del proyecto, ideal para trabajo en equipo y validación de diferentes estrategias (fuerza bruta, dinámica, voraz).

---

## 2. Estructura del proyecto

El proyecto se organizó en módulos y carpetas siguiendo buenas prácticas de ingeniería de software.
La estructura propuesta fue:

```
proyecto_riego/
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada del proyecto
│   ├── utils.py             # Funciones auxiliares (lectura, cálculos)
│   ├── fuerza_bruta.py      # Implementación de la estrategia roFB
│   ├── dinamica.py          # Implementación de roPD (otro integrante)
│   └── voraz.py             # Implementación de roV (otro integrante)
│
├── tests/
│   ├── test_fuerza_bruta.py # Pruebas unitarias del método roFB
│   ├── test_utils.py
│   └── ...
│
├── data/
│   ├── ejemplo1.txt
│   └── ejemplo2.txt
│
├── docs/
│   ├── informe.md
│   └── imagenes/
│
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline de integración continua
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 3. Ejecución del proyecto

El punto de entrada está en `src/main.py`.
Para ejecutar desde consola:

```bash
python src/main.py
```

El script lee los datos de `data/ejemplo1.txt`, aplica las tres estrategias (si están implementadas) y muestra en pantalla el costo y la permutación óptima.

---

## 4. Idea de la solución — Fuerza Bruta

La estrategia de **fuerza bruta (roFB)** consiste en probar **todas las permutaciones posibles** del orden de riego de los tablones y seleccionar aquella que minimice el costo total (CRF_\Pi).

### 📘 Definición funcional

```python
def roFB(finca):
    mejor_perm = None
    mejor_costo = float("inf")
    for perm in itertools.permutations(range(len(finca))):
        costo = calcular_costo(finca, perm)
        if costo < mejor_costo:
            mejor_perm = list(perm)
            mejor_costo = costo
    return mejor_perm, mejor_costo
```

### 📄 Apoyo en módulo `utils.py`

La función `calcular_costo(finca, perm)` calcula el costo total para una permutación específica:

Esta función:

1. Calcula el tiempo acumulado de riego.
2. Evalúa el retraso de cada tablón.
3. Multiplica el retraso por su prioridad.
4. Suma los costos para obtener el total.

---


---

## 5. Pipeline de integración (GitHub Actions)

El archivo `.github/workflows/ci.yml` permite ejecutar automáticamente la verificación del proyecto en GitHub, sin correr las pruebas del docente (solo validación funcional).

```yaml
name: RiegoOptimo CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run project main script
        run: |
          python src/main.py
```

---


## 6. Conclusiones personales

(Kevin Bejarano)

* El enfoque de **fuerza bruta** permite validar la **exactitud de las soluciones** de los demás métodos.
* Su implementación es directa gracias a `itertools.permutations`, pero el costo computacional crece factorialmente con el número de tablones.
* La modularidad del proyecto permitió aislar esta técnica y mantener una arquitectura escalable para integrar las demás.
* La **estructura del proyecto** y la automatización mediante **GitHub Actions** garantizan un flujo de desarrollo limpio, reproducible y compatible entre los integrantes del equipo.

---

