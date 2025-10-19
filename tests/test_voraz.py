# -*- coding: utf-8 -*-
"""
Pruebas automáticas para el algoritmo voraz de riego óptimo.

Se prueba:
- Formato I/O exigido (n+1 líneas).
- Valores esperados para F1 y F2 con la regla (ts asc, -p desc, tr asc).
- El test usa el CLI, verificando que el pipeline de "compilar" sea coherente con la entrega.
"""

from pathlib import Path
import subprocess
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "src" / "voraz.py"
TESTS_DIR = BASE_DIR / "tests"
ENTRADA = TESTS_DIR / "entrada.txt"
SALIDA = TESTS_DIR / "salida.txt"


def _escribir(path: Path, contenido: str):
    path.write_text(contenido, encoding="utf-8")


def _leer_salida():
    lineas = [ln.strip() for ln in SALIDA.read_text(encoding="utf-8").splitlines() if ln.strip()]
    costo = int(lineas[0])
    orden = list(map(int, lineas[1:]))
    return costo, orden, lineas


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

    costo, orden, lineas = _leer_salida()
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

    costo, orden, lineas = _leer_salida()
    assert len(lineas) == 6
    assert costo == 24
    assert orden == [2, 1, 4, 3, 0]


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
