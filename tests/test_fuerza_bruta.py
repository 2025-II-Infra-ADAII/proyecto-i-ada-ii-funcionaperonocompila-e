import pytest
import random
import time
from src.fuerza_bruta import roFB
from src.utils import calcular_costo #funcion ubicada en utils

# ----------------------------------------------------------
# Función auxiliar: genera finca con n tablones aleatorios
# ----------------------------------------------------------
def generar_finca(n):
    finca = []
    for _ in range(n):
        ts = random.randint(5, 20)      # tiempo de supervivencia
        tr = random.randint(1, 5)       # tiempo de regado
        p = random.randint(1, 4)        # prioridad
        finca.append((ts, tr, p))
    return finca

# ----------------------------------------------------------
# Prueba (a): tamaño "juguete" - 10 elementos
# ----------------------------------------------------------
def test_fuerza_bruta_juguete():
    finca = generar_finca(5)  # menor que 10, para que no explote factorial
    start = time.time()
    mejor_perm, mejor_costo = roFB(finca)
    end = time.time()
    assert isinstance(mejor_perm, list)
    assert isinstance(mejor_costo, (int, float))
    assert len(mejor_perm) == len(finca)
    print(f"\n[JUGUETE] Tiempo: {end - start:.5f} s, n={len(finca)}")

# ----------------------------------------------------------
# Prueba (b): pequeño - 100 elementos (solo medir tiempo)
# ----------------------------------------------------------
def test_fuerza_bruta_pequeno():
    finca = generar_finca(100)
    start = time.time()
    # No ejecutamos roFB porque factorial(100) sería imposible
    # Solo validamos que calcular_costo funcione correctamente
    orden = list(range(100))
    costo = calcular_costo(finca, orden)
    end = time.time()
    assert isinstance(costo, (int, float))
    print(f"\n[PEQUEÑO] Tiempo: {end - start:.5f} s, n={len(finca)}")

# ----------------------------------------------------------
# Prueba (c): mediano - 1000 elementos
# ----------------------------------------------------------
def test_fuerza_bruta_mediano():
    finca = generar_finca(1000)
    start = time.time()
    orden = list(range(1000))
    costo = calcular_costo(finca, orden)
    end = time.time()
    assert isinstance(costo, (int, float))
    print(f"\n[MEDIANO] Tiempo: {end - start:.5f} s, n={len(finca)}")

# ----------------------------------------------------------
# Prueba (d): grande - 10 000 elementos
# ----------------------------------------------------------
def test_fuerza_bruta_grande():
    finca = generar_finca(10000)
    start = time.time()
    orden = list(range(10000))
    costo = calcular_costo(finca, orden)
    end = time.time()
    assert isinstance(costo, (int, float))
    print(f"\n[GRANDE] Tiempo: {end - start:.5f} s, n={len(finca)}")

# ----------------------------------------------------------
# Prueba (e): extra grande - 50 000 elementos
# ----------------------------------------------------------
def test_fuerza_bruta_extra_grande():
    finca = generar_finca(50000)
    start = time.time()
    orden = list(range(50000))
    costo = calcular_costo(finca, orden)
    end = time.time()
    assert isinstance(costo, (int, float))
    print(f"\n[EXTRA GRANDE] Tiempo: {end - start:.5f} s, n={len(finca)}")
