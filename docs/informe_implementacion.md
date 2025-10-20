

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
![formula12](https://latex.codecogs.com/svg.image?{\color{white}$$F=\langle&space;T_0,T_1,\dots,T_{n-1}\rangle$$})

El objetivo es encontrar una **permutación óptima** ( \Pi ) que minimice el costo total:
![formula13](https://latex.codecogs.com/svg.image?{\color{white}$$CRF_{\Pi}=\sum_{i=0}^{n-1}p_i\cdot\max(0,(t_{\Pi_i}&plus;tr_i)-ts_i)$$})
donde (t_{\Pi_i}) representa el instante en que inicia el riego del tablón (i) según el orden ![formula14](https://latex.codecogs.com/svg.image?{\color{white}(\Pi)}).

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

La estrategia de **fuerza bruta (roFB)** consiste en probar **todas las permutaciones posibles** del orden de riego de los tablones y seleccionar aquella que minimice el costo total ![formula15](https://latex.codecogs.com/svg.image?{\color{white}(CRF_\Pi)}).

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

## 5. Idea de la solución — Programación Dinámica

La estrategia de **programación dinámica (`programacion_dinamica`)** construye la solución **de forma incremental**, evaluando todos los subconjuntos posibles de tablones y reutilizando los resultados parciales para evitar cálculos repetidos.

En lugar de probar todas las permutaciones como en la fuerza bruta, este método guarda en una tabla (`dp`) el costo mínimo asociado a cada subconjunto y el último tablón regado.

### 📘 Definición funcional

```python
def programacion_dinamica(finca):
    """
    Programación dinámica Bottom-Up (sin máscaras)
    Retorna el costo mínimo y el orden óptimo de riego.
    finca: lista de tuplas (ts, tr, p)
    """
    n = len(finca)
    dp = {}         
    parent = {}     

    # Casos base (subconjuntos de tamaño 1)
    for i in range(n):
        subset = (i,)
        ts, tr, p = finca[i]
        retraso = max(0, tr - ts)
        dp[subset] = {i: p * retraso}
        print("--------------------subset")
        print(dp)
        print("--------------------parent")
        parent[subset] = {i: None}
        print(parent)
        
    # Construcción Bottom-Up
    for k in range(2, n+1):
        for subset in combinations(range(n), k):
            dp[subset] = {}
            parent[subset] = {}

            for j in subset:
                prev_subset = tuple(x for x in subset if x != j)
                mejor = math.inf
                mejor_prev = None

                # tiempo acumulado previo
                tiempo_prev = sum(finca[x][1] for x in prev_subset)
                ts_j, tr_j, p_j = finca[j]
                fin_riego = tiempo_prev + tr_j
                retraso = max(0, fin_riego - ts_j)
                costo_extra = p_j * retraso

                # buscamos mejor previo
                for prev_last, costo_prev in dp[prev_subset].items():
                    total = costo_prev + costo_extra
                    if total < mejor:
                        mejor = total
                        mejor_prev = prev_last

                dp[subset][j] = mejor
                parent[subset][j] = mejor_prev

    # Solución óptima final
    full = tuple(range(n))
    mejor_tablon = min(dp[full], key=dp[full].get)
    mejor_costo = dp[full][mejor_tablon]

    # Reconstruir el orden óptimo
    orden = []
    subset = full
    actual = mejor_tablon
    while actual is not None:
        orden.append(actual)
        prev = parent[subset][actual]
        subset = tuple(x for x in subset if x != actual)
        actual = prev
    orden.reverse()

    return mejor_costo, orden
```


### 🧠 Descripción

* Usa un enfoque **Bottom-Up** con almacenamiento de subproblemas.
* Reduce cálculos redundantes y garantiza la **solución óptima**.
* Su complejidad es **exponencial optimizada**, ![formula16](https://latex.codecogs.com/svg.image?{\color{white}(O(n^2\cdot&space;2^n))}), mucho más eficiente que la fuerza bruta.

---

## 6. Idea de la solución — Algoritmo Voraz

La estrategia **voraz (`roV`)** busca una **aproximación rápida** al orden de riego ideal.
Ordena los tablones según criterios de prioridad y supervivencia sin explorar todas las combinaciones posibles.

### 📘 Definición funcional

```python
def roV(finca: List[Tuple[int, int, int]]):
    """
    Algoritmo voraz propuesto.
    Regla: EDD con prioridades -> ordenar por (ts asc, p desc, tr asc).

    Parámetros:
      finca: lista de n tuplas (ts_i, tr_i, p_i) para i=0..n-1

    Devuelve:
      (pi, costo)
        - pi: lista con la permutación (orden) de índices de tablones a regar.
        - costo: costo total CRF de la programación propuesta.
    """
    n = len(finca)
    indices = list(range(n))

    # Orden clave: primero ts asc, luego prioridad descendente (-p), y tr asc
    pi = sorted(indices, key=lambda i: (finca[i][0], -finca[i][2], finca[i][1]))

    # Calcula el costo asociado a ese orden
    _, _, costo = _calc_cost_and_starts(finca, pi)
    return pi, costo
```


### 🧠 Descripción

* **Ordena** los tablones de forma eficiente ![formula17](https://latex.codecogs.com/svg.image?{\color{white}((O(n\log&space;n)))}).
* Da prioridad a los tablones con **menos tiempo de supervivencia** y **mayor prioridad**.
* No garantiza la solución óptima, pero obtiene una **respuesta cercana** con tiempos muy bajos.

---
---

## 7. Pipeline de integración (GitHub Actions)

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

---

## 8. Sustentación del uso de `isinstance` en las pruebas

Durante las pruebas con **Pytest**, se utilizó la función `isinstance()` para validar que las salidas de los algoritmos tuvieran el **tipo de dato esperado**, garantizando la coherencia funcional sin necesidad de conocer valores exactos. Por ejemplo, se comprobó que `mejor_perm` fuera una lista y `mejor_costo` un número (`int` o `float`), asegurando así la correcta estructura de los resultados.

Este enfoque fue especialmente útil en pruebas de gran tamaño, donde ejecutar la fuerza bruta sería inviable. Con `isinstance()` se verificó que funciones como `calcular_costo` siguieran devolviendo tipos válidos, validando la **robustez y estabilidad del código** sin comprometer el tiempo de ejecución.


## 9. Conclusiones

El desarrollo del proyecto permitió analizar y comparar tres enfoques clásicos para resolver el **problema del riego óptimo**, evidenciando las diferencias entre exactitud, eficiencia y escalabilidad de cada técnica.

1. **Fuerza Bruta (`roFB`)**

   * Garantiza la **solución óptima**, ya que evalúa todas las permutaciones posibles.
   * Sin embargo, su **crecimiento factorial** ((O(n!))) hace que sea inviable para fincas con más de unos pocos tablones.
   * Resulta útil como **referencia teórica** y para validar otras soluciones en casos pequeños.

2. **Programación Dinámica (`programacion_dinamica`)**

   * Reduce el número de cálculos repetidos mediante el uso de subproblemas y almacenamiento parcial.
   * Mantiene la **exactitud de la fuerza bruta**, pero con una mejora significativa en rendimiento ![formula19](https://latex.codecogs.com/svg.image?{\color{white}$$((O(n^2\cdot&space;2^n)))$$}).
   * Su consumo de memoria es alto, pero logra un equilibrio razonable entre tiempo y precisión, siendo aplicable a **instancias medianas**.

3. **Algoritmo Voraz (`roV`)**

   * Utiliza criterios heurísticos (tiempo de supervivencia, prioridad y tiempo de riego) para obtener una **solución aproximada** de manera muy eficiente ![formula21](https://latex.codecogs.com/svg.image?{\color{white}$$((O(n\log&space;n)))$$}).
   * Aunque no siempre garantiza el costo mínimo global, produce resultados **prácticamente válidos** en fracciones de segundo.
   * Es la mejor alternativa para **instancias grandes o en tiempo real**.

### 💡 Conclusión general del proyecto

El proyecto demostró cómo los tres paradigmas de diseño de algoritmos —**exhaustivo**, **optimizado** y **heurístico**— pueden aplicarse a un mismo problema con resultados muy distintos.

* La **fuerza bruta** asegura exactitud pero no escala.
* La **dinámica** mantiene precisión con mejor desempeño.
* El **voraz** sacrifica exactitud en favor de velocidad.

En conjunto, la práctica permitió comprender de forma aplicada el impacto real de la **complejidad computacional** y la importancia de elegir el enfoque adecuado según el tamaño del problema y las restricciones del sistema.

---



