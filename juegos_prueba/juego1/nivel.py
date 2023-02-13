import pygame
from pygame.locals import *
from gestorRecursos import *
from personajes import *

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 500
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

class Nivel:
    def __init__(self):
        self.decorado = Decorado()
        self.scrollx = 0

       # Se crea personaje
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        self.jugador1.establecerPosicion((300, 320))

        self.grupoPlataformas = pygame.sprite.Group()

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)


    def update(self, tiempo):
        # self.decorado.update(tiempo)

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        return False

    def dibujar(self, pantalla):
        self.decorado.dibujar(pantalla)
        self.grupoJugadores.draw(pantalla)

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                return True

        teclasPulsadas = pygame.key.get_pressed()

        return False

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('decorado.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class Cielo:
    def __init__(self):
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def dibujar(self,pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
