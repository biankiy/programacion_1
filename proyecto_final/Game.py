import pygame

import sys
import json

from BibliotecaLogica import crear_matriz_aleatoria, mostrar_matriz
from Config import *




'''
    Este metodo calcula la posicion  del tablero, para lñuego poder centrarlo

    Parámetros:

    filas (int): Número de filas del tablero.
    columnas (int): Número de columnas del tablero.
    Devuelve:

    (x_inicio, y_inicio) (tuple): Coordenadas (x, y) de la esquina superior izquierda donde se debe dibujar el tablero.
    Detalles:

    Utiliza constantes : TAM_CELDA (tamaño de cada celda) | dimensiones de la pantalla (ANCHO, ALTO) para calcular el espacio disponible y centrar el tablero horizontal y verticalmente.
'''

def calcular_posicion_centrada(filas, columnas):
    ancho_tablero = columnas * TAM_CELDA
    alto_tablero = filas * TAM_CELDA
    x_inicio = (ANCHO - ancho_tablero)//2 
    y_inicio = (ALTO - alto_tablero) //2
    return x_inicio, y_inicio

'''
Dibuja el tablero de juego en la pantalla según el estado actual de la partida.

Parámetros:

    matriz (list ): Representa el tablero con números o minas.
    -1: Indica una mina.
     0: Celda vacía sin minas cercanas.
    -8: Número de minas adyacentes.

    descubierto: Indica si cada celda ha sido descubierta (True) o no (False).
    banderas: Posiciones donde el jugador ha colocado banderas.
    x_inicio (int): Coordenada x inicial del tablero.
    y_inicio (int): Coordenada y inicial del tablero.
    Detalles:

    Pinta cada celda de manera diferente según su estado (descubierta, con mina, con bandera o cubierta).
    Muestra el número de minas adyacentes si la celda fue descubierta y no es una mina.
    Dibuja un borde en cada celda para crear una cuadrícula visible.

'''
def dibujar_tablero(pantalla, matriz, descubierto, banderas, x_inicio, y_inicio):
    filas, columnas = len(matriz), len(matriz[0])

    imagen_fondo = pygame.image.load("Assets/clean2.jpg")  
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
    #pantalla.fill(COLOR_FONDO)
    for i in range(filas):
        for j in range(columnas):
            x, y = x_inicio + j * TAM_CELDA, y_inicio + i * TAM_CELDA
            if descubierto[i][j]:
                if matriz[i][j] == -1:
                    pygame.draw.rect(pantalla, COLOR_MINA, (x, y, TAM_CELDA, TAM_CELDA))
                else:
                    pygame.draw.rect(pantalla, COLOR_FONDO, (x, y, TAM_CELDA, TAM_CELDA))
                    if matriz[i][j] > 0:
                        fuente = pygame.font.Font(None, 36)
                        texto = fuente.render(str(matriz[i][j]), True, COLOR_TEXTO)
                        pantalla.blit(texto, (x + 10, y + 5))
            elif (i, j) in banderas:
                pygame.draw.rect(pantalla, COLOR_BANDERA, (x, y, TAM_CELDA, TAM_CELDA))
            else:
                pygame.draw.rect(pantalla, COLOR_CUADRO, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(pantalla, COLOR_TEXTO, (x, y, TAM_CELDA, TAM_CELDA), 1)

'''
   LO que hace es revelar la celda seleccionada y, si es segura, descubre automáticamente las celdas adyacentes.

    Parámetros:

    fila (int): Fila de la celda a descubrir.
    columna (int): Columna de la celda a descubrir.
    Detalles:

    Si la celda contiene una mina (-1), el juego termina (game_over = True).
    Si la celda está vacía (0), se realiza una exploración recursiva para descubrir las celdas adyacentes seguras.
    Incrementa el puntaje cuando una celda segura es descubierta.
    Evita descubrir una celda ya revelada.
    Llama a funciones externas:

    mostrar_mensaje_perdida(): Muestra un mensaje cuando el jugador pierde al descubrir una mina.
'''
def descubrir_celda(fila, columna, descubierto, matriz, puntaje):
    if descubierto[fila][columna]:
        return puntaje
    
    descubierto[fila][columna] = True
    if matriz[fila][columna] == -1: 
        return puntaje 
    
    puntaje += 1
    
    if matriz[fila][columna] == 0:
        for x in range(max(0, fila - 1), min(len(matriz), fila + 2)):
            for y in range(max(0, columna - 1), min(len(matriz[0]), columna + 2)):
                if not descubierto[x][y]:
                    puntaje = descubrir_celda(x, y, descubierto, matriz, puntaje)
    
    return puntaje

'''
 Lo que hace es gestionar toda la logica de los cliks que se hacen en el tablero ,
  Tanto manejar la muestra de la celda, como la colocacion o eliminar una bandera 

    Parámetros:

    x (int): Coordenada horizontal del clic.
    y (int): Coordenada vertical del clic.
    boton (int): Botón del ratón presionado (1 para clic izquierdo, 3 para clic derecho).
    Detalles:

    Clic izquierdo (boton == 1): Descubre la celda seleccionada, llamando a la función descubrir_celda.
    Clic derecho (boton == 3): Coloca o elimina una bandera en la celda seleccionada. Si ya hay una bandera, la elimina; de lo contrario, la coloca.
    Comprueba si el juego ha terminado (game_over) antes de procesar el clic.
    Calcula la fila y columna del tablero según las coordenadas del clic y la posición inicial del tablero (x_inicio, y_inicio).
'''
def manejar_clic(x, y, boton, matriz, banderas, y_inicio, x_inicio, game_over, descubierto, puntaje):
    
    if game_over == False:
        
        fila, columna = (y - y_inicio) // TAM_CELDA, (x - x_inicio) // TAM_CELDA
        if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
            if boton == 1:
                if matriz[fila][columna] == -1:
                    game_over = True
                    mostrar_mensaje_perdida(pantalla, ANCHO, ALTO)
                else: 
                    puntaje = descubrir_celda(fila, columna, descubierto, matriz, puntaje)
            elif boton == 3:
                if (fila, columna) in banderas:
                    banderas.remove((fila, columna))
                else:
                    banderas.append((fila, columna))
    
    return game_over, puntaje

                
'''
    Dibuja y muestra el puntaje actual del jugador en la esquina superior izquierda de la pantalla.

    Parámetros:

    puntaje (int): Puntaje actual del jugador.
    Detalles:

    Muestra el puntaje con cuatro dígitos, rellenando con ceros a la izquierda si es necesario.
    Pinta el puntaje en la posición (10, 10) de la pantalla, utilizando una fuente estándar.
'''
def dibujar_puntaje(pantalla, puntaje):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntaje: {puntaje:04}", True, COLOR_TEXTO)
    pantalla.blit(texto, (10, 10))

'''
    Dibuja un botón en la pantalla con un texto especificado

    Parámetros:

    texto (str): Texto del boton.
    x (int): Coordenada x de la esquina superior izquierda del botón.
    y (int): Coordenada y de la esquina superior izquierda del botón.
    ancho (int): Ancho del botón.
    alto (int): Alto del botón.
    Detalles:

    Dibuja un rectángulo sólido para representar el botón.
    escribe el texto centrado dentro del botón.
    Usa colores definidos (COLOR_BOTON y COLOR_TEXTO_BOTON) .
'''
def dibujar_boton(texto, x, y, ancho, alto,pantalla):
    pygame.draw.rect(pantalla, COLOR_BOTON, (x, y, ancho, alto))
    fuente = pygame.font.Font(None, 36)
    texto_render = fuente.render(texto, True, COLOR_TEXTO_BOTON)
    pantalla.blit(texto_render, (x + 20, y + 10))
'''
    Muestra un mensaje en la pantalla cuando el jugador pierde la partida.

    Detalles:

    Muestra el texto "¡Perdiste!" en una fuente grande y de color rojo.
    Centra el texto en la pantalla.
    Actualiza la pantalla con pygame.display.flip() para mostrar el mensaje.
    Pausa el juego durante 2 segundos (pygame.time.delay(2000)) para que se pueda ver el mensaje antes de continuar o cerrar el juego.

'''
def mostrar_mensaje_perdida(pantalla, ANCHO, ALTO):
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("¡Perdiste!", True, (255, 0, 0)) 
    imagen_fondo = pygame.image.load("Assets/ganador.jpg")  
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
    
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))
    pygame.display.flip() 
    pygame.time.delay(2000) 





#_---------------------------- GUARDAR NOMBRE PUNTAJE  --------------------------------------
'''
    Se le pide le nokmbre al jugador antes de comenzar o guardar su puntaje.

    Detalles:

    Muestra una pantalla negra con un mensaje que indica "Ingresa tu nombre".
    Captura la entrada de texto del teclado y muestra el nombre en tiempo real en la pantalla.
    Si el jugador presiona "Enter" (RETURN) y el nombre no está vacío, la función devuelve el nombre ingresado.
    
    Retorno:

    Devuelve el nombre del jugador como una cadena de texto.
'''
def pedir_nombre(pantalla):
    nombre = ""
    fuente = pygame.font.Font(None, 48)
    entrada_activa = True
    while entrada_activa:
        #pantalla.fill((0, 0, 0))  # Fondo negro
        imagen_fondo = pygame.image.load("Assets/ganador.jpg")  
        imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
        texto = fuente.render("Ingresa tu nombre:", True, (0, 128, 128))
        pantalla.blit(texto, (150, 200))
        nombre_texto = fuente.render(nombre, True, (255, 0, 255))
        pantalla.blit(nombre_texto, (150, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    return nombre.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode 



'''
    Guarda el puntaje del jugador en un archivo JSON, manteniendo una lista ordenada de los 10 mejores puntajes.

    Parámetros:

    nick (str): El nombre del jugador.
    puntaje (int): El puntaje obtenido en la partida.
    Detalles:

    Verifica que el nombre no esté vacío y que el puntaje sea válido.
    Carga los puntajes existentes desde puntajes.json.
    Agrega el nuevo puntaje y ordena la lista de mayor a menor, conservando solo los 10 mejores.
    Guarda la lista actualizada en el archivo puntajes.json.

'''
dato = ""

def guardar_puntaje(nick, puntaje):
    if nick != "" and puntaje > 0:
        puntajes = cargar_puntajes()
        puntajes.append({"nick": nick, "puntaje": puntaje})
        puntajes = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)[:10]

        with open("puntajes.txt", "w") as archivo:
            for puntaje in puntajes:
                archivo.write(f"{puntaje['nick']}: {puntaje['puntaje']}\n")
    
    else:
        print("Nombre o puntaje no válido. No se guardará el puntaje.")

'''
    Carga los puntajes almacenados en el archivo JSON.

    Retorno:

    Devuelve una lista de diccionarios con los puntajes, donde cada diccionario tiene las claves nick y puntaje.
    Si el archivo no existe, devuelve una lista vacía.

'''
def cargar_puntajes():
   
        with open("puntajes.json", "r") as archivo:
            return json.load(archivo)
    

'''
    Muestra los puntajes guardados en una pantalla de clasificación.

    Detalles:

    Crea una pantalla con fondo negro.
    Muestra el título "Puntajes" y una lista de los 10 mejores puntajes, ordenados de mayor a menor.
    Cada puntaje incluye el nombre del jugador y su puntaje.
    El jugador puede salir de la pantalla presionando cualquier tecla o clic del ratón.
    Eventos:

    Permite cerrar la pantalla de puntajes y volver al menú principal o al juego.

'''
def mostrar_puntajes(pantalla,ancho, alto):
    
    with open("puntajes.json", "r") as archivo:
        puntajes = json.load(archivo)

    puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
    pantalla_puntajes = True  

    while pantalla_puntajes:
        imagen_fondo = pygame.image.load("Assets/ganador.jpg") 
        imagen_fondo = pygame.transform.scale(imagen_fondo, (ancho, alto)) 
      
        letra_titulo = pygame.font.Font(None, 50)
        titulo = letra_titulo.render("Puntajes", True, (0, 0, 255))
        pantalla.blit(titulo, (250, 50))

        letra_puntaje = pygame.font.Font(None, 36)
        llenar = 150
        for idx, puntaje in enumerate(puntajes_ordenados[:10]):
            texto = f"{idx + 1}. {puntaje['nick']} - {puntaje['puntaje']}"
            render = letra_puntaje.render(texto, True, (100, 100, 255))
            pantalla.blit(render, (200, llenar))
            llenar += 40

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                pantalla_puntajes = False  

        pygame.display.flip()  
    puntajes = cargar_puntajes()  
    
    puntajes = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)
    
    pantalla.fill((0, 0, 0))

    fuente = pygame.font.Font(None, 48)
    llenar = 100 
    

    # TITULOS DE LAS COLUNAS ----------------------------------------------------
    texto_nick = fuente.render("Nick", True, (255, 255, 255))
    texto_puntaje = fuente.render("Puntaje", True, (255, 255, 255))
    pantalla.blit(texto_nick, (150, llenar))
    pantalla.blit(texto_puntaje, (400, llenar))
    llenar += 50  

    # mUESTRO TODOS LOS PUNTAJES--------------------------------------------------------
    for i, p in enumerate(puntajes):
        texto = fuente.render(f"{p['nick']}", True, (0, 0, 255))
        texto_punt = fuente.render(f"{p['puntaje']}", True, (255, 255, 255))
        pantalla.blit(texto, (150, llenar + i * 60))
        pantalla.blit(texto_punt, (400, llenar + i * 60))
    
   
    dibujar_boton("Volver", 150, llenar + len(puntajes) * 60 + 50, 200, 50,pantalla)
    pygame.display.flip()

'''
    Verifica si el jugador ha ganado la partida.

    Parámetros:

    matriz (list): Matriz del tablero de juego, que contiene minas ('M') y números.
    descubierto (list): Matriz booleana que indica qué celdas han sido descubiertas.
    Retorno:

    Devuelve True si todas las celdas sin minas han sido descubiertas; de lo contrario, devuelve False.
'''
def verificar_victoria(matriz, descubierto):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            # Solo chequea si todas las celdas no-mina están descubiertas
            if matriz[i][j] != -1 and not descubierto[i][j]:
                return False
    return True


'''
    Muestra un mensaje en la pantalla cuando el jugador gana la partida.

    Detalles:

    Muestra el texto "¡Ganaste!" en color verde en el centro de la pantalla.
    Actualiza la pantalla para mostrar el mensaje.
    Mantiene el mensaje visible durante 3 segundos antes de continuar (pygame.time.delay(3000)).
'''    
def mostrar_mensaje_victoria(pantalla, ancho, alto):
    pantalla.fill((0, 0, 0))

    imagen_fondo = pygame.image.load("Assets/ganador.jpg")  
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ancho, alto))
    
    pantalla.blit(imagen_fondo, (0, 0))
    
    font_victoria = pygame.font.Font(None, 72)
    mensaje = font_victoria.render("¡Ganaste!", True, (255, 255, 255))
    
    rect_ancho = mensaje.get_width() + 40
    rect_alto = mensaje.get_height() + 20
    ancho__x = (ancho - rect_ancho) // 2
    alto_y = (alto - rect_alto) // 2

    pantalla.blit(mensaje, (ancho__x + 20, alto_y + 10))
    
    pygame.display.flip()
    pygame.time.delay(3000)



def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Bianca_Gimenes_2_parcial")
    

    iconoMargenSuperior = pygame.image.load("Assets/png-transparent-utn-hd-logo.png")
    pygame.display.set_icon(iconoMargenSuperior)
    
    imagen_fondo = pygame.image.load("Assets/clean2.jpg")
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

    en_juego = False
    mostrar_niveles = False
    matriz = []
    descubierto = []
    banderas = []
    puntaje = 0
    game_over = False
    x_inicio, y_inicio = 0, 0

    nivel = "FACIL"
    config = niveles_config[nivel.upper()]


    run = True
    while run:
        pantalla.blit(imagen_fondo, (0, 0))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos 
                
               # print(f"Botón presionado: {evento.button}")
                if en_juego and not game_over:
                    
                    game_over, puntaje = manejar_clic(x, y, evento.button, matriz, banderas, y_inicio, x_inicio, game_over, descubierto, puntaje)

                    if verificar_victoria(matriz, descubierto):
                         print("¡Victoria detectada!")
                         mostrar_mensaje_victoria(pantalla, ANCHO, ALTO)
                         guardar_puntaje(nick, puntaje)
                         en_juego = False
                                        
                if en_juego:
                    if 10 <= x <= 100 and 550 <= y <= 590:
                        guardar_puntaje(nick, puntaje)
                        nick = pedir_nombre(pantalla)
                        config = niveles_config[nivel.upper()]
                        filas, columnas, minas = config["filas"], config["columnas"], config["minas"]
                        matriz = crear_matriz_aleatoria(filas, columnas, minas)
                        mostrar_matriz(matriz)
                        print("----------------------------")
                        descubierto = [[False] * columnas for _ in range(filas)]
                        banderas = []
                        puntaje = 0
                        game_over = False
                
                    elif 650 <= x <= 750 and 550 <= y <= 590:
                        print("Botón 'Volver' presionado")
                        guardar_puntaje(nick, puntaje) 
                        en_juego = False
                
                elif mostrar_niveles:
                    if 150 <= x <= 350:
                        if 100 <= y <= 150:
                            nivel = "FACIL"
                            mostrar_niveles = False
                        elif 200 <= y <= 250:
                            nivel = "MEDIO"
                            mostrar_niveles = False
                        elif 300 <= y <= 350:
                            nivel = "DIFICIL"
                            mostrar_niveles = False
                        elif 400 <= y <= 450:
                            print("Botón 'Volver' presionado en niveles")
                            mostrar_niveles = False
              
                
                else:
                    if 150 <= x <= 350:  # Verifica si el clic está en el rango de botones
                        if 100 <= y <= 150:  # Botón "Niveles"
                            mostrar_niveles = True
                        elif 200 <= y <= 250:  # Botón "Jugar"
                            nick = pedir_nombre(pantalla)
                            en_juego = True
                            config = niveles_config[nivel.upper()]
                            filas, columnas, minas = config["filas"], config["columnas"], config["minas"]
                            matriz = crear_matriz_aleatoria(filas, columnas, minas)
                            mostrar_matriz(matriz)
                            descubierto = [[False] * columnas for _ in range(filas)]
                            banderas = []
                            puntaje = 0
                            game_over = False
                            x_inicio, y_inicio = calcular_posicion_centrada(filas, columnas)
                        elif 300 <= y <= 350:  # Botón "Ver Puntajes"
                            mostrar_puntajes(pantalla, ANCHO, ALTO)
                        elif 400 <= y <= 450:  # Botón "Salir"
                            run = False


        if en_juego:
            dibujar_tablero(pantalla, matriz, descubierto, banderas, x_inicio, y_inicio)
            dibujar_puntaje(pantalla, puntaje)
            dibujar_boton("Reiniciar", 10, 550, 150, 40, pantalla)
            dibujar_boton("Volver", 650, 550, 120, 40, pantalla)
        elif mostrar_niveles:
            dibujar_boton("Fácil", 150, 100, 200, 50, pantalla)
            dibujar_boton( "Medio", 150, 200, 200, 50, pantalla)
            dibujar_boton( "Difícil", 150, 300, 200, 50, pantalla)
            dibujar_boton( "Volver", 150, 400, 200, 50, pantalla)
        else:
            dibujar_boton( "Nivel", 150, 100, 200, 50, pantalla)
            dibujar_boton( "Jugar", 150, 200, 200, 50, pantalla)
            dibujar_boton( "Ver Puntajes", 150, 300, 200, 50, pantalla)
            dibujar_boton( "Salir", 150, 400, 200, 50, pantalla)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()