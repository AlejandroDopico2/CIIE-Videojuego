import pygame
from pygame.locals import *
from Personajes.personajes import MiSprite
from gestorRecursos import *

class Plataforma(MiSprite):
    def __init__(self, rectangulo, imagen):
        MiSprite.__init__(self)
        self.rect = rectangulo
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        self.image = GestorRecursos.CargarImagen(imagen, -1)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))