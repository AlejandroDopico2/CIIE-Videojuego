import pygame
from gestorRecursos import *
from Personajes.personajes import MiSprite


class Dialogos(MiSprite):
    def __init__(self, img, coord, scale, despl, pos, active):
        super().__init__()
        self.img = img
        self.coord = coord
        self.rect = pygame.Rect(coord[0], coord[1], 0, 0)
        self.scale = scale
        self.despl = despl
        self.pos = pos
        self.active = active
        self.establecerPosicion(
            (self.rect.left + self.pos[0], self.rect.bottom + self.pos[1])
        )
        self.image = GestorRecursos.CargarImagen(self.img, -1)
        if scale > 1:
            self.image = pygame.transform.scale(
                self.image,
                (
                    self.image.get_width() * self.scale,
                    self.image.get_height() * self.scale,
                ),
            )

    def getCoord(self):
        return (self.coord[0], self.coord[1])

    def getDespl(self):
        return self.despl

    def setDespl(self, despl):
        self.despl = despl

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getActive(self):
        return self.active

    def setActive(self, active):
        self.active = active
    
    def updateDraw(self, coordJ):
        self.establecerPosicion(
            (coordJ[0] + self.pos[0], coordJ[1] + self.pos[1])
        )
