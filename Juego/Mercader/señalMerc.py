import pygame
from gestorRecursos import *
from Personajes.personajes import MiSprite


class señalMerc(MiSprite):
    def __init__(self, img, coord):
        super().__init__()
        self.img = img
        self.rect = pygame.Rect(coord[0], coord[1], 0, 0)
        self.image = GestorRecursos.CargarImagen(self.img, -1)

    def draw(self, pantalla):
        rect = self.rect.copy()
        pantalla.blit(self.image, rect)
