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
        plataformaAire = Plataforma(pygame.Rect(500, 450, 300, 20), 'suelo.png')

        self.grupoPlataformas = pygame.sprite.Group(plataformaSuelo, plataformaAire)

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)
        self.grupoSprites = pygame.sprite.Group(self.jugador1, plataformaSuelo, plataformaAire)

    def actualizarScrollOrd(self, jugador):
        if jugador.rect.left < MINIMO_X_JUGADOR:
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            if self.scrollx <= 0:
                self.scrollx = 0
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
                return False
            
            else:
                self.scrollx = self.scrollx - desplazamiento
                return True

        if jugador.rect.right > MAXIMO_X_JUGADOR:
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
                jugador.establecerPosicion((self.scrollx +  MAXIMO_X_JUGADOR - jugador.rect.width, jugador.posicion[1]))
                
                return False
            
            elif jugador.rect.left - MINIMO_X_JUGADOR < desplazamiento:
                
                jugador.establecerPosicion((jugador.posicion[0] - desplazamiento, jugador.posicion[1]))
                return False
            else:
                self.scrollx = self.scrollx + desplazamiento
                return True
        
        return False

    def actualizarScroll(self, jugador):
        cambioScroll = self.actualizarScrollOrd(jugador)
        if cambioScroll:
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))

            self.decorado.update(self.scrollx)
            self.fondo.update(self.scrollx)

    def update(self, tiempo):

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        self.actualizarScroll(self.jugador1)
        # self.fondo.update(tiempo)

    def draw(self, pantalla):
        self.fondo.dibujar(pantalla, self.scrollx)
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
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA*2, ALTO_PANTALLA/4))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA*2, ALTO_PANTALLA/4)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = -scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class Cielo:
    def __init__(self,):
        self.cielo = GestorRecursos.CargarImagen('bg.png')
        self.cielo = pygame.transform.scale(self.cielo, (ANCHO_PANTALLA, 4*ALTO_PANTALLA/5))
        self.rect = self.cielo.get_rect()

        self.rect.left = 0 # El lado izquierdo de la subimagen que se esta visualizando
        # self.update(0)

    def update(self, scrollx):
        self.rect.left = scrollx
        
    def dibujar(self,pantalla, scrollx):
        # Dibujamos el color del cielo
        pantalla.fill("black")
        # pantalla.blit(self.cielo, self.rect)
        x = -scrollx % self.cielo.get_width()
        x2 = x - self.cielo.get_width() if x > 0 else x + self.cielo.get_width()

        pantalla.blit(self.cielo, (x, 0))
        pantalla.blit(self.cielo, (x2, 0))