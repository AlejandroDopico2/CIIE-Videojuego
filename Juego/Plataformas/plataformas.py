import pygame
from pygame.locals import *
from Personajes.personajes import MiSprite
from gestorRecursos import *

class Plataforma(MiSprite):
    def __init__(self, rectangulo, imagen = None, colorkey=None):
        MiSprite.__init__(self)
        self.rect = rectangulo
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        if imagen is not None:
            self.image = GestorRecursos.CargarImagen(imagen, colorkey)
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.Surface((0,0))