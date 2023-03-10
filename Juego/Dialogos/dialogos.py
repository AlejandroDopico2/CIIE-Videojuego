import pygame
from Personajes.personajes import MiSprite
from gestorRecursos import *

class Dialogos(MiSprite):
    def __init__(self, img, rect, scale):
        super().__init__()
        self.img = img
        self.rect = rect
        self.scale = scale
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        self.image = GestorRecursos.CargarImagen(self.img, -1)
        if scale > 1: 
            self.image = pygame.transform.scale(self.image, 
                (self.image.get_width() * self.scale, self.image.get_height() * self.scale))