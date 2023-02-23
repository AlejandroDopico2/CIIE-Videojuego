import pygame
from pygame.locals import *
from gestorRecursos import *
from Personajes.personajes import *
from escena import *
from Plataformas.plataformas import *

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

class Nivel(PygameScene):
    def __init__(self, director):
        PygameScene.__init__(self, director)

        self.director = director

        self.decorado = Decorado()
        self.fondo = Cielo()
        self.scrollx = 0

       # Se crea personaje
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        self.jugador1.establecerPosicion((200, 541))

        plataformaSuelo = Plataforma(self.decorado.rect, 'suelo.png')
        plataformaAire = Plataforma(pygame.Rect(500, 400, 300, 100), 'suelo.png')

        self.grupoPlataformas = pygame.sprite.Group(plataformaSuelo, plataformaAire)

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)
        self.grupoSprites = pygame.sprite.Group(self.jugador1, plataformaSuelo, plataformaAire)

    def update(self, tiempo):
        # self.decorado.update(tiempo)

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        return False

    def draw(self, pantalla):
        self.fondo.dibujar(pantalla)
        self.decorado.dibujar(pantalla)
        self.grupoSprites.draw(pantalla)

    def eventsLoop(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                self.director.exitProgram()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('suelo.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA/4))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA/4)
        # self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class Cielo:
    def __init__(self):
        self.cielo = GestorRecursos.CargarImagen('sky.png')
        self.cielo = pygame.transform.scale(self.cielo, (ANCHO_PANTALLA, 4*ALTO_PANTALLA/5))
        self.rect = self.cielo.get_rect()

        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        # self.update(0)

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
        pantalla.fill("black")
        pantalla.blit(self.cielo, self.rect)
