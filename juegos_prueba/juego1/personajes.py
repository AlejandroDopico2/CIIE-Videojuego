import pygame
from pygame.locals import *
from gestorRecursos import *

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2

# Velocidades
VELOCIDAD_JUGADOR = 0.2
VELOCIDAD_SALTO_JUGADOR = 0.3

GRAVEDAD = 0.0003

class MiSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0,0)
        self.velocidad = (0,0)
        self.scroll = (0,0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

class Personaje(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes):

        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()
        # self.hoja = pygame.transform.scale(self.hoja, (100,))
        

        self.movimiento = QUIETO
        self.mirando = IZQUIERDA

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 2):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4
        self.numPostura = QUIETO
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        self.actualizarPostura()
        # self.actualizarPostura()

    def actualizarPostura(self):

        # Si ha pasado, actualizamos la postura
        self.numImagenPostura += 1
        if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
            self.numImagenPostura = 0;
        if self.numImagenPostura < 0:
            self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

        # Si esta mirando a la izquiera, cogemos la porcion de la hoja
        if self.mirando == IZQUIERDA:
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
        #  Si no, si mira a la derecha, invertimos esa imagen
        elif self.mirando == DERECHA:
            self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def mover(self, movimiento):
        if movimiento == ARRIBA:
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        else:
            self.movimiento = movimiento

class Jugador(Personaje):
    def __init__(self):
        Personaje.__init__(self, 'homero_sprite.png', 'coordJugador.txt', [6,6,6])

    def mnover(self, teclasPulsadas, arriba, abajo, izquierda, derecha):
        if teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        else:
            Personaje.mover(self,QUIETO)