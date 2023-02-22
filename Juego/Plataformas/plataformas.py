import pygame
from pygame.locals import *
from Personajes.personajes import MiSprite

class Plataforma(MiSprite):
    def __init__(self, rectangulo):
        MiSprite.__init__(self)
        self.rect = rectangulo
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        self.image = pygame.Surface((0,0))