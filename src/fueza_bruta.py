"""
Fuerza bruta.
src/utils.py contiene la función `calcular_costo(finca, orden)`.   
"""
import itertools
from typing import List, Tuple
from src.utils import calcular_costo  # usa la función centralizada en utils

def roFB_all(finca: List[Tuple[int,int,int]]):
    """
    Genera todas las permutaciones y retorna lista de (perm, costo).
    - finca: lista de tuplas (ts, tr, p)
    - perm: lista de índices
    """
    n = len(finca)
    resultados = []
    for perm in itertools.permutations(range(n)):
        costo = calcular_costo(finca, perm)
        resultados.append((list(perm), costo))
    return resultados

def roFB(finca: List[Tuple[int,int,int]]):
    """
    Retorna la mejor permutación y su costo (sin almacenar todas).
    Devuelve: (mejor_perm: List[int], mejor_costo: int)
    """
    n = len(finca)
    mejor_perm = None
    mejor_costo = float("inf")
    for perm in itertools.permutations(range(n)):
        costo = calcular_costo(finca, perm)
        if costo < mejor_costo:
            mejor_costo = costo
            mejor_perm = list(perm)
    return mejor_perm, mejor_costo
