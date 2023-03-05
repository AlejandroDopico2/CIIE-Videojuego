#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Importar modulos

from Niveles.menu import Menu
from director import Director

if __name__ == '__main__':

    director = Director()
    escena = Menu(director)

    director.stackScene(escena)
    director.execute()

