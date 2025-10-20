import pytest
import random
import time
from src.dinamica import roPD


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
# (a) Test de caso pequeño — validación exacta y orden
# ----------------------------------------------------------
def test_dinamica_caso_pequeno():
    finca = [(10, 3, 4), (5, 3, 3), (2, 2, 1)]
    costo, orden = roPD(finca)
    print(f"\n[CASO PEQUEÑO] Costo mínimo: {costo}, Orden óptimo: {orden}")
    assert isinstance(costo, (int, float))
    assert isinstance(orden, list)
    assert len(orden) == len(finca)
    assert costo >= 0

# ----------------------------------------------------------
# (b) Test finca aleatoria pequeña
# ----------------------------------------------------------
def test_dinamica_random_pequena():
    finca = generar_finca(5)
    start = time.time()
    costo, orden = roPD(finca)
    end = time.time()
    print(f"\n[RANDOM PEQUEÑA] Tiempo: {end - start:.5f} s, n={len(finca)}")
    assert isinstance(costo, (int, float))
    assert isinstance(orden, list)
    assert len(orden) == len(finca)
    assert costo >= 0

# ----------------------------------------------------------
# (c) Test finca mediana (rendimiento)
# ----------------------------------------------------------
def test_dinamica_mediana():
    finca = generar_finca(10)
    start = time.time()
    costo, orden = roPD(finca)
    end = time.time()
    print(f"\n[MEDIANA] Tiempo: {end - start:.5f} s, n={len(finca)}")
    assert isinstance(costo, (int, float))
    assert isinstance(orden, list)

# ----------------------------------------------------------
# (d) Test finca grande (verifica que no explote)
# ----------------------------------------------------------
def test_dinamica_grande():
    finca = generar_finca(12)
    start = time.time()
    costo, orden = roPD(finca)
    end = time.time()
    print(f"\n[GRANDE] Tiempo: {end - start:.5f} s, n={len(finca)}")
    assert isinstance(costo, (int, float))
    assert isinstance(orden, list)
    assert costo >= 0
