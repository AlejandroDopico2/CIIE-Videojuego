import pygame
from pygame.locals import *
from gestorRecursos import *
from Personajes.personajes import *
from escena import *
from Plataformas.plataformas import *
from Niveles.nivel import *


class NivelPlaya(Nivel):
    def __init__(self, director):
        Nivel.__init__(self, director,  'Recursos/level1.json')
