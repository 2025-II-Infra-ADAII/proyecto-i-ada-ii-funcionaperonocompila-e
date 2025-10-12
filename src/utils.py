
def calcular_costo(finca, permutacion):
    
    """
    con esta funcion calcularemos el costo total que tarda una finca en regarse
    se espera la lista de tuplas finca: (ts, tr, p) y la
    permutacion: lista con el orden de los tablones [0, 1, 2]
    """
    
    tiempo_actual = 0
    costo_total = 0
    
    for i in permutacion:
        ts, tr, p = finca[i]
        fin_riego = tiempo_actual + tr
        retraso = max(0, fin_riego - ts)
        costo_total += p * retraso
        tiempo_actual += tr  
    
    return costo_total


def tiempos_inicio(finca, permutacion):
    """
    con esta funcion calcularemos en que momento se debe iniciar a regar cada tablon
    """
    tiempos = [0] * len(finca)
    tiempo_actual = 0
    
    for idx, i in enumerate(permutacion):
        tiempos[i] = tiempo_actual
        tiempo_actual += finca[i][1]  
    
    return tiempos


def leer_finca(ruta_archivo):
    """
    con esta funcion leemos el archivo de entrada la cual debe estar en un orden especifico
    """
    with open(ruta_archivo, 'r') as f:
        lineas = [line.strip() for line in f.readlines()]
    
    n = int(lineas[0])
    finca = [tuple(map(int, linea.split(','))) for linea in lineas[1:n+1]]
    return finca
    