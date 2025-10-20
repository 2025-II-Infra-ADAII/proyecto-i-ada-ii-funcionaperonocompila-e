import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import leer_finca, guardar_salida, medir_tiempo
from src.fuerza_bruta import roFB

def main():
    finca = leer_finca("data/ejemplo1.txt")
    
    print("calculando soluciones...\n")
    
    perm_fb, costo_fb, tiempo_fb = medir_tiempo(roFB, finca)
    
    print("RESULTADOS")
    print(f"fuera bruta: costo={costo_fb}, permutacion={perm_fb}, tiempo={tiempo_fb:.6f} seg")
    
    guardar_salida("data/salida_fb.txt", costo_fb, perm_fb)


if __name__ == "__main__":
    main()