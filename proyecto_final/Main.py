import sys
from BibliotecaLogica import crear_matriz_aleatoria, mostrar_matriz
from Game import calcular_posicion_centrada, dibujar_boton, dibujar_puntaje, dibujar_tablero, guardar_puntaje, manejar_clic, mostrar_mensaje_victoria, mostrar_puntajes, pedir_nombre, verificar_victoria
import pygame
from Config import * 

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
                 if 150 <= x <= 350:
                        if 200 <= y <= 250:
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
                        elif 300 <= y <= 350:
                                    mostrar_puntajes(pantalla,ANCHO,ALTO)
                        elif 400 <= y <= 450:
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


if __name__ == "__main__":
    main()
