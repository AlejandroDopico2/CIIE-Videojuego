#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Importar modulos

from Niveles.menu import Menu
from director import Director
from escena import *
from Niveles.menu import Menu


if __name__ == '__main__':

    director = Director()
    nivel = Menu(director)
    director.stackScene(nivel)
    director.execute()

