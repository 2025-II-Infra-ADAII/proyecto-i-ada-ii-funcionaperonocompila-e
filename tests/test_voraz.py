# -*- coding: utf-8 -*-
"""
test_voraz.py — pruebas automáticas para el algoritmo voraz de riego óptimo.

Estructura esperada:
  src/voraz.py   → contiene la función y CLI principal
  tests/test_voraz.py → este archivo (ejecutar con pytest o directamente)

Uso desde terminal:
    pytest tests/test_voraz.py
o simplemente:
    python tests/test_voraz.py
"""

import os
import subprocess
from pathlib import Path

# ----------------------------
# Rutas base
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SRC = BASE_DIR / "src" / "voraz.py"
TESTS_DIR = BASE_DIR / "tests"
ENTRADA = TESTS_DIR / "entrada.txt"
SALIDA = TESTS_DIR / "salida.txt"


# ----------------------------
# Función auxiliar para escribir un archivo de entrada
# ----------------------------
def crear_archivo_entrada():
    contenido = """5
10,3,4
5,3,3
2,2,1
8,1,1
6,4,2
"""
    with open(ENTRADA, "w", encoding="utf-8") as f:
        f.write(contenido)


# ----------------------------
# Prueba principal
# ----------------------------
def probar_algoritmo_voraz():
    """Ejecuta voraz.py sobre la entrada de ejemplo y valida la salida."""
    crear_archivo_entrada()

    # Ejecutar el script src/voraz.py desde consola
    subprocess.run(["python", str(SRC), str(ENTRADA), str(SALIDA)], check=True)

    # Leer la salida
    with open(SALIDA, "r", encoding="utf-8") as f:
        lineas = [ln.strip() for ln in f if ln.strip() != ""]

    costo = int(lineas[0])
    orden = list(map(int, lineas[1:]))

    print("Costo obtenido:", costo)
    print("Orden de riego:", orden)

    # Validar (según el resultado esperado del algoritmo voraz)
    assert costo == 11, "El costo total debería ser 11 para el ejemplo 1"
    assert orden == [2, 1, 4, 3, 0], "El orden de riego no coincide con el esperado"


# ----------------------------
# Ejecución directa
# ----------------------------
if __name__ == "__main__":
    probar_algoritmo_voraz()
    print("\n✅ Prueba completada correctamente.")
