# -*- coding: utf-8 -*-
"""
voraz.py — Algoritmo voraz para el problema de riego óptimo.

Regla voraz implementada:
    EDD con prioridades:
      Ordenar los tablones por (ts ascendente, p descendente, tr ascendente).

Intuición de la regla:
- ts (tiempo de supervivencia) pequeño => más urgente: conviene regarlo antes.
- En empates de ts, priorizamos mayor p (más importante).
- Si aún hay empate, menor tr (para no bloquear el recurso con riegos largos si no hay diferencia en urgencia).

Formato de entrada (archivo de texto):
    n
    ts0,tr0,p0
    ts1,tr1,p1
    ...
    ts(n-1),tr(n-1),p(n-1)

Formato de salida (archivo de texto):
    Costo
    pi0
    pi1
    ...
    pi(n-1)

Uso desde consola (ejemplo):
    python src/voraz.py entrada.txt salida.txt

Complejidad:
- Ordenar n tablones: O(n log n).
- Calcular inicios y costo: O(n).
- Total: O(n log n).
"""

from typing import List, Tuple
import sys


# ============================
# Cálculo de costo y tiempos
# ============================
def _calc_cost_and_starts(
    finca: List[Tuple[int, int, int]], perm: List[int]
):
    """
    Dada una finca y una permutación perm (orden de riego),
    calcula:
      - start[i] = t*_i (instante de inicio del riego del tablón i)
      - completion[i] = C_i = t*_i + tr_i
      - costo_total = sum_i p_i * max(0, C_i - ts_i)

    Parámetros:
      finca: lista de tuplas (ts, tr, p) por índice de tablón i
      perm:  lista de índices de tablón en el orden de riego

    Retorna:
      (start, completion, costo_total)
    """
    n = len(finca)
    start = [0] * n
    completion = [0] * n

    # t acumula el tiempo corrido del recurso de riego
    t = 0
    for j, i in enumerate(perm):
        start[i] = t
        ts, tr, p = finca[i]
        t += tr
        completion[i] = start[i] + tr

    # costo por sufrimiento: p_i * max(0, C_i - ts_i)
    costo_total = 0
    for i, (ts, tr, p) in enumerate(finca):
        tardanza = completion[i] - ts
        if tardanza < 0:
            tardanza = 0
        costo_total += p * tardanza

    return start, completion, costo_total


# ============================
# Algoritmo voraz principal
# ============================
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


# ============================
# Entrada / salida de archivos
# ============================
def _leer_finca_desde_archivo(path: str) -> List[Tuple[int, int, int]]:
    """
    Lee el archivo de entrada con el formato especificado en el enunciado.
    Retorna una lista de tuplas (ts, tr, p).
    """
    with open(path, "r", encoding="utf-8") as f:
        lineas = [ln.strip() for ln in f if ln.strip() != ""]

    if not lineas:
        raise ValueError("Archivo de entrada vacío. Se esperaba al menos la línea con n.")

    # Primera línea: n
    try:
        n = int(lineas[0])
    except Exception as e:
        raise ValueError("La primera línea debe ser un entero n.") from e

    if len(lineas) - 1 < n:
        raise ValueError(f"Se esperaban {n} líneas de tablones; llegaron {len(lineas)-1}.")

    finca: List[Tuple[int, int, int]] = []
    for k in range(1, 1 + n):
        partes = lineas[k].split(",")
        if len(partes) != 3:
            raise ValueError(
                f"Línea {k+1}: se esperaban 3 valores separados por comas (ts,tr,p)."
            )
        try:
            ts = int(partes[0].strip())
            tr = int(partes[1].strip())
            p = int(partes[2].strip())
        except Exception as e:
            raise ValueError(f"Línea {k+1}: ts,tr,p deben ser enteros.") from e

        # Validaciones básicas sugeridas por el enunciado
        if p < 1 or p > 4:
            raise ValueError(f"Línea {k+1}: p debe estar en 1..4, recibido p={p}.")
        if ts < 0 or tr <= 0:
            raise ValueError(f"Línea {k+1}: ts >= 0 y tr > 0, recibido ts={ts}, tr={tr}.")

        finca.append((ts, tr, p))

    return finca


def _escribir_salida(path: str, costo: int, perm: List[int]) -> None:
    """
    Escribe el archivo de salida con el formato:
      Costo
      pi0
      pi1
      ...
      pi(n-1)
    """
    with open(path, "w", encoding="utf-8") as g:
        g.write(f"{costo}\n")
        for i in perm:
            g.write(f"{i}\n")


# ============================
# CLI (para correr desde terminal)
# ============================
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("Uso: python src/voraz.py <archivo_entrada> <archivo_salida>", file=sys.stderr)
        sys.exit(2)

    entrada, salida = argv
    finca = _leer_finca_desde_archivo(entrada)
    perm, costo = roV(finca)
    _escribir_salida(salida, costo, perm)


if __name__ == "__main__":
    main()
