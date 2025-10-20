# -*- coding: utf-8 -*-
"""
Pruebas integradas (todo en un solo archivo):

1) Correctitud e I/O (F1, F2).
2) Validación de errores de formato (líneas > n).
3) Control de calidad con óptimo por fuerza bruta (n=7).
4) Escalado con tiempos y 5 repeticiones por tamaño:
   - Siempre: 10, 100, 1_000
   - Opcional (si RUN_SLOW=1): 10_000, 50_000

Los resultados de tiempos se guardan en tests/benchmarks/bench_<n>.csv
"""

from pathlib import Path
import csv
import os
import random
import subprocess
import time
import pytest

# ----------------------------
# Rutas base
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "src" / "voraz.py"
TESTS_DIR = BASE_DIR / "tests"
ENTRADA = TESTS_DIR / "entrada.txt"
SALIDA = TESTS_DIR / "salida.txt"
BM_DIR = TESTS_DIR / "benchmarks"
BM_DIR.mkdir(exist_ok=True, parents=True)


# ----------------------------
# Utilidades comunes
# ----------------------------
def _escribir(path: Path, contenido: str):
    path.write_text(contenido, encoding="utf-8")


def _leer_salida(path: Path):
    lineas = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    costo = int(lineas[0])
    orden = list(map(int, lineas[1:]))
    return costo, orden, lineas


def _validar_perm(perm, n):
    assert len(perm) == n, f"La permutación debe tener {n} elementos."
    assert sorted(perm) == list(range(n)), "La permutación debe contener 0..n-1 sin repetir."


def _recalcular_costo(finca, perm):
    n = len(finca)
    start = [0] * n
    t = 0
    for i in perm:
        start[i] = t
        t += finca[i][1]  # tr

    costo = 0
    for i, (ts, tr, p) in enumerate(finca):
        C = start[i] + tr
        R = C - ts
        if R < 0:
            R = 0
        costo += p * R
    return costo


def _registrar_benchmark_csv(n, rep, elapsed_sec):
    csv_path = BM_DIR / f"bench_{n}.csv"
    new_file = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        if new_file:
            w.writerow(["n", "repeticion", "tiempo_segundos"])
        w.writerow([n, rep, f"{elapsed_sec:.6f}"])


def _generar_finca(n: int, seed: int):
    """
    Genera datos sintéticos válidos:
    - p ∈ {1..4}
    - tr ∈ [1..10]
    - ts ~ N(30, 15) truncado a >=0
    """
    rnd = random.Random(seed)
    finca = []
    for _ in range(n):
        tr = rnd.randint(1, 10)
        p = rnd.randint(1, 4)
        ts = max(0, int(rnd.gauss(mu=30, sigma=15)))
        finca.append((ts, tr, p))
    return finca


def _escribir_entrada_finca(path: Path, finca):
    n = len(finca)
    lines = [str(n)] + [f"{ts},{tr},{p}" for (ts, tr, p) in finca]
    _escribir(path, "\n".join(lines) + "\n")


# ----------------------------
# 1) Correctitud e I/O (F1, F2)
# ----------------------------
def test_cli_F1_formato_y_valores():
    """Entrada F1 del enunciado: costo=20, orden=[2,1,4,3,0]."""
    entrada = """5
10,3,4
5,3,3
2,2,1
8,1,1
6,4,2
"""
    _escribir(ENTRADA, entrada)
    subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)

    costo, orden, lineas = _leer_salida(SALIDA)
    assert len(lineas) == 6, "La salida debe tener exactamente n+1 líneas (6)."
    assert costo == 20
    assert orden == [2, 1, 4, 3, 0]


def test_cli_F2_formato_y_valores():
    """Entrada F2: costo=24, orden=[2,1,4,3,0]."""
    entrada = """5
9,3,4
5,3,3
2,2,1
8,1,1
6,4,2
"""
    _escribir(ENTRADA, entrada)
    subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)

    costo, orden, lineas = _leer_salida(SALIDA)
    assert len(lineas) == 6
    assert costo == 24
    assert orden == [2, 1, 4, 3, 0]


# ----------------------------
# 2) Validación de errores (líneas > n)
# ----------------------------
def test_error_si_archivo_tiene_mas_de_n_filas_de_datos():
    """Debe fallar si hay más datos que n."""
    entrada = """3
5,1,2
4,1,1
6,2,3
7,2,2
"""
    _escribir(ENTRADA, entrada)
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)


# ----------------------------
# 3) Control de calidad (óptimo por fuerza bruta con n=7)
# ----------------------------
def _fuerza_bruta_optimo(finca):
    from itertools import permutations
    mejor = None
    mejor_pi = None
    idxs = list(range(len(finca)))
    for pi in permutations(idxs):
        c = _recalcular_costo(finca, pi)
        if mejor is None or c < mejor:
            mejor = c
            mejor_pi = pi
    return mejor, list(mejor_pi)


def test_control_bruteforce_n7():
    """Para n=7, comparamos voraz vs óptimo (una instancia)."""
    n = 7
    finca = _generar_finca(n, seed=12345)
    _escribir_entrada_finca(ENTRADA, finca)

    subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)
    costo_cli, perm_cli, _ = _leer_salida(SALIDA)
    _validar_perm(perm_cli, n)
    assert costo_cli == _recalcular_costo(finca, perm_cli)

    costo_opt, perm_opt = _fuerza_bruta_optimo(finca)
    # El voraz no debe ser mejor que el óptimo; lo normal es que sea >=
    assert costo_cli >= costo_opt
    print(f"[n=7] costo_voraz={costo_cli} vs costo_optimo={costo_opt}")


# ----------------------------
# 4) Escalado con tiempos (5 repeticiones por tamaño)
#    RUN_SLOW=1 en el entorno para incluir 10k y 50k.
# ----------------------------
def _sizes_for_scaling():
    sizes = [10, 100, 1_000]
    if os.environ.get("RUN_SLOW", "0") == "1":
        sizes += [10_000, 50_000]
    return sizes


@pytest.mark.parametrize("n", _sizes_for_scaling())
def test_escalado_con_tiempos(n):
    reps = 5
    seed_base = {10: 1000, 100: 2000, 1000: 3000, 10_000: 4000, 50_000: 5000}.get(n, 9999)

    for rep in range(1, reps + 1):
        finca = _generar_finca(n, seed=seed_base + rep)
        _escribir_entrada_finca(ENTRADA, finca)

        t0 = time.perf_counter()
        subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)
        elapsed = time.perf_counter() - t0

        costo, perm, lineas = _leer_salida(SALIDA)
        assert len(lineas) == 1 + n, "La salida debe tener exactamente n+1 líneas."
        _validar_perm(perm, n)

        costo_recalc = _recalcular_costo(finca, perm)
        assert costo == costo_recalc, "El costo reportado debe coincidir con el recalculado."

        _registrar_benchmark_csv(n, rep, elapsed)
        print(f"[n={n} rep={rep}] tiempo={elapsed:.6f}s costo={costo}")
