import pygame
#_---------------------------- CONFIGURACION DEL JUEGO --------------------------------------

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bianca_Gimenes_2_parcial")
iconoMargenSuperior = pygame.image.load("Assets/png-transparent-utn-hd-logo.png")
pygame.display.set_icon(iconoMargenSuperior)


imagen_fondo = pygame.image.load("Assets/clean2.jpg")
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))


pygame.mixer.music.load("Assets/arcade-70780.mp3") 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.)

COLOR_FONDO = (200, 200, 100)
COLOR_CUADRO = (150, 150, 150)
COLOR_TEXTO = (0, 0, 0)
COLOR_MINA = (255, 0, 0)
COLOR_BOTON = (100, 100, 250)
COLOR_TEXTO_BOTON = (255, 255, 255)
COLOR_BANDERA = (0, 255, 0)

TAM_CELDA = 30
nivel = "FACIL"



niveles_config = {
    "FACIL": {"filas": 8, "columnas": 8, "minas": 10},
    "MEDIO": {"filas": 16, "columnas": 16, "minas": 40},
    "DIFICIL": {"filas": 16, "columnas": 30, "minas": 100},
}
