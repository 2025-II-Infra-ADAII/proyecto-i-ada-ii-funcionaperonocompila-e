import math
from itertools import combinations


def roPD(finca):
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
        parent[subset] = {i: None}
        
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