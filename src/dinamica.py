from utils import leer_finca

def programacion_dinamica(finca):
    """
    Programación dinámica (bottom-up con bitmask)
    para minimizar el costo total de riego.
    finca: lista de tuplas (ts, tr, p)
    """
    n = len(finca)
    N = 1 << n  # Total de combinaciones posibles: 2^n

    # dp[mask][i] = costo mínimo si el conjunto de tablones regados es mask
    # y el último regado fue i
    dp = [[float('inf')] * n for _ in range(N)]

    # Casos base: regar solo un tablón i
    for i in range(n):
        ts, tr, p = finca[i]
        fin_riego = tr
        retraso = max(0, fin_riego - ts)
        dp[1 << i][i] = p * retraso

    # Recorremos todas las combinaciones posibles (máscaras)
    for mask in range(N):
        for ultimo in range(n):
            # Si el tablón 'ultimo' no está en la combinación actual, saltamos
            if not (mask & (1 << ultimo)):
                continue

            costo_actual = dp[mask][ultimo]
            if costo_actual == float('inf'):
                continue

            # Calcular el tiempo total actual (suma de duraciones en mask)
            tiempo_actual = sum(finca[k][1] for k in range(n) if mask & (1 << k))

            # Intentamos regar un tablón nuevo 'j' que aún no esté regado
            for j in range(n):
                if mask & (1 << j):  # ya regado
                    continue

                ts, tr, p = finca[j]
                fin_riego = tiempo_actual + tr
                retraso = max(0, fin_riego - ts)
                costo_extra = p * retraso

                nuevo_mask = mask | (1 << j)
                dp[nuevo_mask][j] = min(dp[nuevo_mask][j], costo_actual + costo_extra)

    # Costo mínimo al haber regado todos los tablones
    return min(dp[N - 1])


if __name__ == "__main__":
    # Leer finca desde archivo
    finca = leer_finca("ejemplo1.txt")
    print("Finca cargada:", finca)

    mejor_costo = programacion_dinamica(finca)
    print("Costo mínimo encontrado (DP):", mejor_costo)

