import pytest
import tempfile
from src.utils import calcular_costo, leer_finca, guardar_salida

def test_calcular_costo():
    """
    con este test se verifica que la funcion calcular_costo ubicadada en utils.py
    funcione y calcule correctamente el costo correctamente
    """
    finca = [(10, 3, 4), (5, 3, 3), (2, 2, 1), (8, 1, 1), (6, 4, 2)]
    perm = [0, 1, 4, 2, 3]  #permutacion del ejemplo 1 del enunciado

    costo = calcular_costo(finca, perm)

    #resultado esperado calculado manualmente en el documento (CRF = 26)
    assert costo == 26, f"se esperaba 26 pero se obtuvo {costo}"
    
def test_leer_finca(tmp_path):
    """
    con este test se verifica que la funcion leer_finca en utils.py lea el archivo de entrada correctamente
    """
    #crear archivo temporal de prueba
    file_path = tmp_path / "finca_test.txt"
    contenido = "5\n10,3,4\n5,3,3\n2,2,1\n8,1,1\n6,4,2\n"
    file_path.write_text(contenido)

    finca = leer_finca(str(file_path))

    esperado = [(10, 3, 4), (5, 3, 3), (2, 2, 1), (8, 1, 1), (6, 4, 2)]
    assert finca == esperado, f"Lectura incorrecta: se obtuvo {finca}"
    
    
def test_guardar_salida(tmp_path):
    """
    con este test se verifica que la funcio guardar_salida en utils.py escriba correctamente
    el costo y la permutacion en el archivo de salida.txt
    """
    #archivo de salida temporal
    file_path = tmp_path / "salida.txt"

    costo = 26
    perm = [0, 1, 4, 2, 3]

    guardar_salida(str(file_path), costo, perm)

    #leer archivo para verificar su contenido
    with open(file_path, "r") as f:
        lineas = [line.strip() for line in f.readlines()]

    assert lineas[0] == "26", "El costo no fue escrito correctamente"
    assert [int(x) for x in lineas[1:]] == perm, "La permutación escrita es incorrecta"
 
 
