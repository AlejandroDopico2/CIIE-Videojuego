import pygame
from Personajes.personajes import MiSprite
from gestorRecursos import *

class Dialogos(MiSprite):
    def __init__(self, img, rect):
        super().__init__()
        self.img = img
        self.rect = rect
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        self.image = GestorRecursos.CargarImagen(self.img)
        if self.rect.width > 0 and self.rect.height > 0: 
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
# {
#   "img": 0,
#   "x": 548,
#   "y": 1276,
#   "width": 20,
#   "height": 20
# },