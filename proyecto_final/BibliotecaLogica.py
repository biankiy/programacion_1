


import random


def mostrar_matriz(matriz:list):
    '''
    Muestra una matriz por consola.

    Parámetros:
        matriz (list): La matriz a mostrar.

    Retorna:
        None
    '''
    
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
          print( f"{matriz[i][j]:3}", end=" ")
        print(" ")  


'''
Inicializa la matriz en NONE
'''
def inicializar_matriz(cant_filas, cant_columnas):
    '''
    Crea una matriz con todas las celdas inicializadas en None.

    Parámetros:
        cant_filas (int): Número de filas.
        cant_columnas (int): Número de columnas.

    Retorna:
        list: Matriz inicializada.
    '''
    matriz = []
    for _ in range(cant_filas):
        matriz += [[None] * cant_columnas]
    return matriz    

'''
    Crea una matriz de dimensiones especificas pasada s por parametro y coloca minas aleatoriamente en ella.

    Parámetros:
    cant_filas: Número de filas de la matriz.
    cant_columnas: Número de columnas de la matriz.
    total_minas: Número total de minas a colocar en la matriz.
'''
def crear_matriz_aleatoria(cant_filas, cant_columnas, total_minas):
    '''
    Crea una matriz con minas colocadas aleatoriamente.

    Parámetros:
        cant_filas (int): Número de filas.
        cant_columnas (int): Número de columnas.
        total_minas (int): Número de minas a colocar.

    Retorna:
        list: Matriz con minas y números de minas adyacentes.
    '''
    matriz = inicializar_matriz(cant_filas,cant_columnas)
    
    minas_colocadas = 0
    while minas_colocadas < total_minas:
        fila = random.randint(0, cant_filas - 1)
        columna = random.randint(0, cant_columnas - 1)
        if matriz[fila][columna] != -1:
            matriz[fila][columna] = -1 
            minas_colocadas += 1
    matriz_actualziada =actualizar_matriz_juego(matriz)
    return matriz_actualziada


'''
   Esta funcion se encarga de calcular y actualizar el valor de cada celda de la matriz, representando el número de minas adyacentes a esa celda.

Pasos ...
    Recorre cada celda de la matriz.
    Detección de minas: Si la celda actual contiene una mina (valor -1), la función salta a la siguiente celda sin hacer cambios.
    Contar minas adyacentemos: Para cada celda que no es una mina:
     Revisa las ocho celdas que la rodean (arriba, abajo, izquierda, derecha y diagonales).
     Utiliza un bucle para asegurarse de no salir de los límites de la matriz.
     Suma cuántas de las celdas vecinas contienen minas (-1).
    Actualizar el valor de la celda: y lo guarda  en cada celda el número total de minas que se encontraron de manera adyacentes.

'''
def actualizar_matriz_juego(matriz):
    '''
    Calcula y actualiza el valor de cada celda con el número de minas adyacentes.

    Parámetros:
        matriz (list): Matriz con minas.

    Retorna:
        list: Matriz actualizada.
    '''
    filas = len(matriz)
    columnas = len(matriz[0])

    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == -1:
                continue
            minas_adyacentes = 0
        
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):

                    if 0 <= x < filas and 0 <= y < columnas:
                        if matriz[x][y] == -1:
                            minas_adyacentes += 1
            matriz[i][j] = minas_adyacentes

    return matriz