import pygame
from pygame.locals import *
from gestorRecursos import *
from Personajes.personajes import *
from escena import *
from Plataformas.plataformas import *

import json

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 200
class Nivel(PygameScene):
    def __init__(self, director, cfg):
        PygameScene.__init__(self, director)

        with open(cfg, 'r') as f:
            self.cfg = json.load(f)

        self.director = director
        self.decorado = Decorado(self.cfg['decoration'])
        self.fondo = Fondo(self.cfg['background'])
        self.scrollx = 0

        self.grupoSprites = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()

        # Se crea personaje
        self.jugador = Jugador()
        self.jugador.establecerPosicion((self.cfg['player'][0], self.cfg['player'][1]))
        self.grupoSprites.add(self.jugador)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador)

        self.grupoPlataformas = pygame.sprite.Group()
        self.setPlatforms()
        self.setEnemies()

        # self.vida = self.jugador.barra
        # self.grupoSprites.add(self.vida)
        # self.grupoJugadores = pygame.sprite.Group(self.jugador)

    def setPlatforms(self):
            for pt in self.cfg['platforms']:
                plataforma = Plataforma(pygame.Rect(pt['x'], pt['y'], pt['width'], pt['height']))
                self.grupoPlataformas.add(plataforma)
                self.grupoSprites.add(plataforma)

    def setEnemies(self):
        for e in self.cfg['enemies']:
            if e['name'] == 'espectro':
                enemy = Espectro()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
                self.grupoEnemigos.add(enemy)
                self.grupoSpritesDinamicos.add(enemy)
                self.grupoSprites.add(enemy)

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

        if (self.jugador.posicion[1] - self.jugador.rect.height > ALTO_PANTALLA
            or pygame.sprite.spritecollideany(self.jugador, self.grupoEnemigos) != None):
            self.director.exitScene()

        self.actualizarScroll(self.jugador)
        # self.fondo.update(tiempo)

    def draw(self, pantalla):
        self.fondo.draw(pantalla, self.scrollx)
        self.decorado.draw(pantalla)
        self.grupoSprites.draw(pantalla)

    def eventsLoop(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                self.director.exitProgram()

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

class Decorado:
    def __init__(self, img):
        # Cargar imagen fondo
        self.imagen = GestorRecursos.CargarImagen(img, -1)

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

    def update(self, scrollx):
        # self.rectSubimagen.left = -scrollx
        self.rect.left = -scrollx

    def draw(self, pantalla):
        # pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
        pantalla.blit(self.imagen, self.rect)

class Fondo:
    def __init__(self, bg_list):
        self.bg = []
        self.animated_bg = [i for i, bg in enumerate(bg_list) if bg['animated']]
        for bg in bg_list:
            img = GestorRecursos.CargarImagen(bg['img'], bg['colorKey'])
            self.bg.append((pygame.transform.scale(img, (ANCHO_PANTALLA, ALTO_PANTALLA)), bg['scroll']))
        
        self.rect = self.bg[0][0].get_rect()
        self.rect.left = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.pos = 0

    def update(self, scrollx):
        self.rect.left = scrollx
        
    def drawLayer(self, pantalla, layer, scrollx):
        pantalla.blit(layer, (scrollx - pantalla.get_width(), 0))
        pantalla.blit(layer, (scrollx, 0))

    def draw(self, pantalla, scrollx):
        self.pos += 2
        pantalla.fill("black")
        
        for i, bg in enumerate(self.bg):
            if i in self.animated_bg:
                self.drawLayer(pantalla, bg[0], (-scrollx + self.pos) * bg[1] % ANCHO_PANTALLA)
            else:
                self.drawLayer(pantalla, bg[0], -scrollx * bg[1] % ANCHO_PANTALLA)

        