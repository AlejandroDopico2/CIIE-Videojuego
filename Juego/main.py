#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Importar modulos
import pygame

from director import Director
from Niveles.menu import Menu
from Niveles.nivel import *
from escena import *


if __name__ == '__main__':

    director = Director()
    escena = Menu(director)

    director.stackScene(escena)
    director.execute()

