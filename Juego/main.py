#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Importar modulos

from director import Director
from escena import *
from Niveles.menu import MenuInicio

if __name__ == "__main__":
    director = Director()
    nivel = MenuInicio(director)
    director.stackScene(nivel)
    director.execute()
