import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import leer_finca, guardar_salida, medir_tiempo
from src.fuerza_bruta import roFB
from src.voraz import roV 
from src.dinamica import roPD

def main():
    finca = leer_finca("data/ejemplo1.txt")
    
    print("calculando soluciones...\n")
    
    perm_fb, costo_fb, tiempo_fb = medir_tiempo(roFB, finca)
    perm_v, costo_v, tiempo_v = medir_tiempo(roV, finca)
    costo_pd, perm_pd, tiempo_pd = medir_tiempo(roPD, finca)
    
    print("RESULTADOS")
    print(f"fuera bruta: costo={costo_fb}, permutacion={perm_fb}, tiempo={tiempo_fb:.6f} seg")
    print(f"Voraz: costo={costo_v}, permutacion={perm_v}, tiempo={tiempo_v:.6f} seg")
    print(f"Dinamica: costo={costo_pd}, permutacion={perm_pd}, tiempo={tiempo_pd:.6f} seg")
    
    guardar_salida("data/salida_fb.txt", costo_fb, perm_fb)
    guardar_salida("data/salida_v.txt", costo_v, perm_v)
    guardar_salida("data/salida_pd.txt", costo_pd, perm_pd)


if __name__ == "__main__":
    main()