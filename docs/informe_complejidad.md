
# 🧮 Informe de Complejidad — Proyecto de Riego Óptimo

**Estudiante:** Kevin Andrés Bejarano
**Curso:** Análisis de Algoritmos II (ADA II)
**Periodo:** 2025-II
**Profesor:** Carlos Andrés Delgado Saavedra

---

## 🧩 Contexto general

El **problema del riego óptimo** busca determinar el orden ideal en el que deben regarse los **tablones de cultivo** para minimizar el sufrimiento de las plantas por falta de agua.
Cada tablón posee tres características:

* ( ts_i ): tiempo máximo que puede permanecer sin riego (supervivencia),
* ( tr_i ): tiempo que toma regarlo,
* ( p_i ): prioridad del tablón (1 a 4).

La solución se basa en encontrar la **permutación óptima** ( \Pi ) de los tablones que minimice el costo total:

[
CRF_{\Pi} = \sum_{i=0}^{n-1} p_i \cdot \max(0, (t_{\Pi_i} + tr_i) - ts_i)
]

donde (t_{\Pi_i}) representa el instante en el que comienza el riego del tablón (i) según la permutación seleccionada.

---

## ⚙️ Implementación: Fuerza Bruta (`roFB`)

### Descripción general

El método **fuerza bruta (roFB)** genera **todas las permutaciones posibles** del conjunto de tablones y calcula el **costo total de riego** para cada una, seleccionando la de menor costo.

El cálculo del costo total se apoya en la función auxiliar `calcular_costo(finca, perm)`, la cual:

1. Calcula los tiempos de inicio de riego acumulados.
2. Evalúa el retraso de cada tablón respecto a su tiempo de supervivencia.
3. Suma las penalizaciones ponderadas por la prioridad (p_i).

### código

```python
def roFB(finca):
    mejor_perm = None
    mejor_costo = ∞
    for perm in todas_las_permutaciones(finca):
        costo = calcular_costo(finca, perm)
        if costo < mejor_costo:
            mejor_perm = perm
            mejor_costo = costo
    return mejor_perm, mejor_costo
```

---

## ⏱️ Complejidad temporal

La función `roFB` recorre **todas las permutaciones posibles** de los (n) tablones:

[
n!
]

Para cada permutación, la función auxiliar `calcular_costo` evalúa los (n) tablones, realizando operaciones constantes en cada iteración.
Por tanto, el costo total en tiempo es:

[
T(n) = O(n \cdot n!) = O(n!)
]

> 🔹 **Interpretación:**
> El algoritmo explora exhaustivamente todo el espacio de búsqueda.
> Para valores pequeños (ej. (n \le 8)), es viable;
> pero el tiempo crece de forma explosiva a medida que se agregan tablones.

| n (tablones) | Permutaciones (n!) | Escalamiento aproximado |
| ------------ | ------------------ | ----------------------- |
| 3            | 6                  | Rápido                  |
| 5            | 120                | Aceptable               |
| 8            | 40,320             | Muy lento               |
| 10           | 3,628,800          | Prácticamente inviable  |

---

## 💾 Complejidad espacial

El algoritmo mantiene:

* La lista original de tablones: (O(n))
* Una variable para la mejor permutación: (O(n))
* Una permutación temporal generada por `itertools.permutations` (iterador interno): (O(n))

Por tanto:

[
S(n) = O(n)
]

> El consumo de memoria crece linealmente con el número de tablones, ya que solo se almacena una permutación a la vez y el costo actual.

---

## 📊 Resumen analítico

| Estrategia            | Complejidad temporal | Complejidad espacial | Viabilidad práctica        |
| --------------------- | -------------------- | -------------------- | -------------------------- |
| Fuerza bruta (`roFB`) | (O(n!))              | (O(n))               | Solo viable para (n \le 8) |

---

## 📈 Interpretación teórica

La fuerza bruta garantiza encontrar la **solución óptima exacta**, pero **sacrifica eficiencia**:

* Escala factorialmente: cada tablón adicional multiplica las permutaciones por un nuevo factor.
* No reutiliza resultados ni aplica podas, a diferencia de métodos dinámicos o voraces.
* Es ideal para **validar** resultados de otras estrategias más eficientes (sirve como referencia exacta para comparar la precisión de algoritmos aproximados).

---

## 🧠 Conclusiones personales

* La creación de una **estructura modular del proyecto** (carpetas `src`, `tests`, `data`, `docs`, etc.) permitió una organización clara del código, separando las implementaciones de cada técnica.
* La implementación del algoritmo **fuerza bruta** refleja la esencia del análisis de algoritmos: garantiza la solución exacta, pero muestra el impacto directo del crecimiento factorial en la práctica.
* Este método, aunque poco escalable, es **fundamental como referencia de verificación** para las estrategias **dinámica y voraz**, que sacrifican exactitud por eficiencia.

---

---

