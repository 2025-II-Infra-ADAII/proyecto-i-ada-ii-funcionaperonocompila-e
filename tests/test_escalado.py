# -*- coding: utf-8 -*-
"""
Pruebas de escalado y tiempos (Requisito 10):
- Tamaños: 10, 100, 1_000, 10_000, 50_000
- 5 repeticiones por tamaño
- Validación entrada ↔ salida
- Medición de tiempo y registro a CSV por tamaño
- Un test adicional n=7 con fuerza bruta (control de calidad)
"""

from pathlib import Path
import csv
import random
import time
import subprocess
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "src" / "voraz.py"
TESTS_DIR = BASE_DIR / "tests"
ENTRADA = TESTS_DIR / "entrada_escalado.txt"
SALIDA = TESTS_DIR / "salida_escalado.txt"
BM_DIR = TESTS_DIR / "benchmarks"
BM_DIR.mkdir(exist_ok=True, parents=True)


def _generar_finca(n: int, seed: int):
    """
    Genera n tablones (ts, tr, p) válidos y variados.
    - p ∈ {1,2,3,4}
    - tr ∈ [1, 10]
    - ts ∈ [0, 8*prom_tr] con algo de dispersión relativa a n para meter presión variable
    """
    rnd = random.Random(seed)
    finca = []
    # Promedio de tr esperado ~5.5; usamos un rango para ts que genera casos con y sin tardanza.
    for _ in range(n):
        tr = rnd.randint(1, 10)
        p = rnd.randint(1, 4)
        # ts: escogemos una ventana que no dependa linealmente de n para evitar explotar tiempos óptimos triviales
        # y permitir tardanzas; centramos en ~30 con dispersión.
        ts = max(0, int(rnd.gauss(mu=30, sigma=15)))
        finca.append((ts, tr, p))
    return finca


def _escribir_entrada(path: Path, finca):
    n = len(finca)
    lines = [str(n)] + [f"{ts},{tr},{p}" for (ts, tr, p) in finca]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _leer_salida(path: Path):
    lineas = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    costo = int(lineas[0])
    perm = list(map(int, lineas[1:]))
    return costo, perm, lineas


def _recalcular_costo(finca, perm):
    n = len(finca)
    # inicios
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


def _validar_perm(perm, n):
    assert len(perm) == n, f"La permutación debe tener {n} elementos."
    assert sorted(perm) == list(range(n)), "La permutación debe contener 0..n-1 sin repetir."


def _registrar_benchmark_csv(n, rep, elapsed_sec):
    csv_path = BM_DIR / f"bench_{n}.csv"
    new_file = not csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as g:
        w = csv.writer(g)
        if new_file:
            w.writerow(["n", "repeticion", "tiempo_segundos"])
        w.writerow([n, rep, f"{elapsed_sec:.6f}"])


# ---------------------------
# Test de control (óptimo por fuerza bruta con n pequeño)
# ---------------------------

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
    """Control de calidad: para n=7 comparamos voraz vs óptimo (solo 1 repetición)."""
    n = 7
    finca = _generar_finca(n, seed=12345)
    # Ejecutar CLI para validar I/O también
    _escribir_entrada(ENTRADA, finca)
    subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)
    costo_cli, perm_cli, _ = _leer_salida(SALIDA)
    _validar_perm(perm_cli, n)
    assert costo_cli == _recalcular_costo(finca, perm_cli)

    # Comparar contra fuerza bruta (n=7 es manejable)
    costo_opt, perm_opt = _fuerza_bruta_optimo(finca)
    assert costo_cli >= costo_opt  # el voraz no es necesariamente óptimo; al menos no debe ser menor que el óptimo
    # (Opcional) dejamos un mensaje útil
    print(f"[n=7] costo_voraz={costo_cli} vs costo_optimo={costo_opt}")


# ---------------------------
# Pruebas por tamaño (5 repeticiones cada una)
# ---------------------------

@pytest.mark.parametrize("n", [10])
def test_escalado_tamano_juguete(n):
    _test_escalado_generic(n, reps=5, seed_base=1000)


@pytest.mark.parametrize("n", [100])
def test_escalado_tamano_pequeno(n):
    _test_escalado_generic(n, reps=5, seed_base=2000)


@pytest.mark.parametrize("n", [1000])
def test_escalado_tamano_mediano(n):
    _test_escalado_generic(n, reps=5, seed_base=3000)


@pytest.mark.slow
@pytest.mark.parametrize("n", [10_000])
def test_escalado_tamano_grande(n):
    _test_escalado_generic(n, reps=5, seed_base=4000)


@pytest.mark.slow
@pytest.mark.parametrize("n", [50_000])
def test_escalado_tamano_extra_grande(n):
    _test_escalado_generic(n, reps=5, seed_base=5000)


def _test_escalado_generic(n: int, reps: int, seed_base: int):
    """
    Núcleo de la prueba por tamaño:
      - Genera datos, corre CLI, valida salida, mide y registra tiempo.
      - 5 repeticiones como exige el enunciado.
    """
    for rep in range(1, reps + 1):
        finca = _generar_finca(n, seed=seed_base + rep)

        # Escribir entrada
        _escribir_entrada(ENTRADA, finca)

        # Medir tiempo total (I/O + algoritmo) usando el CLI (entrada→salida)
        t0 = time.perf_counter()
        subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)
        elapsed = time.perf_counter() - t0

        # Leer y validar salida
        costo, perm, lineas = _leer_salida(SALIDA)
        assert len(lineas) == 1 + n, "La salida debe tener exactamente n+1 líneas."
        _validar_perm(perm, n)
        costo_recalc = _recalcular_costo(finca, perm)
        assert costo == costo_recalc, "El costo reportado debe coincidir con el recalculado."

        # Registrar benchmark
        _registrar_benchmark_csv(n, rep, elapsed)

        # Mensaje informativo en salida de test
        print(f"[n={n} rep={rep}] tiempo={elapsed:.6f}s costo={costo}")
