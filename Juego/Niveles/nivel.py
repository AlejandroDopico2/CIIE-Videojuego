import pygame
from pygame.locals import *
from gestorRecursos import *
from Personajes.personajes import *
from escena import *
from Plataformas.plataformas import *


ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 200

class Nivel(PygameScene):
    def __init__(self, director):
        PygameScene.__init__(self, director)

        self.director = director

        self.decorado = Decorado()

        self.fondo = Cielo()
        self.scrollx = 0

        # Se crea personaje
        self.jugador = Jugador()
        self.vida = self.jugador.barra
        self.grupoJugadores = pygame.sprite.Group(self.jugador)

        self.jugador.establecerPosicion((300, 541))
        # plataformaSuelo = Plataforma(pygame.Rect(0, 550, 8500, 20))
        # plataformaSuelo = Plataforma(pygame.Rect(250, 540, 2560, 180), 'suelo.png')
        plataformaAire = Plataforma(pygame.Rect(500, 450, 300, 20), 'suelo.png')

        self.grupoPlataformas = pygame.sprite.Group(plataformaAire)
        self.grupoSprites = pygame.sprite.Group(self.jugador, plataformaAire)
        self.splitCoords()
        for platRect in self.plataformasRect:
            print(platRect)
            plat = Plataforma(platRect) #, 'prueba.png')
            self.grupoPlataformas.add(plat)
            self.grupoSprites.add(plat)

        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador)
        enemigo1 = Espectro()
        enemigo1.establecerPosicion((600, 535))

        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group(enemigo1)

        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador,enemigo1)
        self.grupoSprites = pygame.sprite.Group(self.jugador, plataformaAire,enemigo1)

    def splitCoords(self):
        self.plataformasRect = []
        datos = GestorRecursos.CargarArchivoCoordenadas('plataforma.txt')
        datos = datos.split()
        nDatos = int(len(datos)/4)

        for i in range(0, nDatos):
            self.plataformasRect.append(pygame.Rect(int(datos[i*4]), int(datos[i*4+1]), int(datos[i*4+2]), int(datos[i*4+3])))
        

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
        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover_cpu(self.jugador)

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        if self.jugador.posicion[1] - self.jugador.rect.height > ALTO_PANTALLA:
            self.director.exitScene()

        self.actualizarScroll(self.jugador)
        # self.fondo.update(tiempo)

    def draw(self, pantalla):
        self.fondo.dibujarMulti(pantalla, self.scrollx)
        self.decorado.dibujar(pantalla)
        self.grupoSprites.draw(pantalla)

    def eventsLoop(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                self.director.exitProgram()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('level1.png', -1)

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        # self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA*2, ALTO_PANTALLA/6)
        # self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        # self.rectSubimagen.left = -scrollx
        self.rect.left = -scrollx

    def dibujar(self, pantalla):
        # pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
        pantalla.blit(self.imagen, self.rect)

class Cielo:
    def __init__(self,):
        self.bg = GestorRecursos.CargarImagen('bg.png')
        self.bg = pygame.transform.scale(self.bg, (ANCHO_PANTALLA, ALTO_PANTALLA))

        self.bg1 = GestorRecursos.CargarImagen('bg1.png', 2)
        self.bg1 = pygame.transform.scale(self.bg1, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.bg2 = GestorRecursos.CargarImagen('bg2.png', 2)
        self.bg2 = pygame.transform.scale(self.bg2, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.bg3 = GestorRecursos.CargarImagen('bg3.png', 2)
        self.bg3 = pygame.transform.scale(self.bg3, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.bg4 = GestorRecursos.CargarImagen('bg4.png', 2)
        self.bg4 = pygame.transform.scale(self.bg4, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.rect = self.bg.get_rect()

        self.rect.left = 0 # El lado izquierdo de la subimagen que se esta visualizando

    def update(self, scrollx):
        self.rect.left = scrollx
        
    def dibujar(self, pantalla, layer, scrollx):
        pantalla.blit(layer, (scrollx - pantalla.get_width(), 0))
        pantalla.blit(layer, (scrollx, 0))

    def dibujarMulti(self, pantalla, scrollx):

        pantalla.fill("black")
        self.dibujar(pantalla, self.bg,  -scrollx % ANCHO_PANTALLA)
        self.dibujar(pantalla, self.bg1, -scrollx % ANCHO_PANTALLA)
        self.dibujar(pantalla, self.bg2, -scrollx * 0.75 % ANCHO_PANTALLA)
        self.dibujar(pantalla, self.bg3, -scrollx * 0.5 % ANCHO_PANTALLA)
        self.dibujar(pantalla, self.bg4, -scrollx* 0.25 % ANCHO_PANTALLA)

        