# -*- coding: utf-8 -*-

import os

import pygame
from pygame.locals import *

# -------------------------------------------------
# Clase GestorRecursos


# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}

    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join("Recursos", nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error:
                print("Cannot load image:", fullname)
                raise SystemExit
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0, 0))
                elif colorkey is 2:
                    colorkey = imagen.get_at((0, int(imagen.get_height() / 2)))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join("Recursos", nombre)
            pfile = open(fullname, "r")
            datos = pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

    @classmethod
    def load_sound(cls, nombre, dir_sonido):
        ruta = os.path.join(dir_sonido, nombre)
        # Intentar cargar el sonido
        try:
            sonido = pygame.mixer.Sound(ruta)
        except pygame.error as message:
            print("No se pudo cargar el sonido:", message)
            sonido = None
        return sonido

    @classmethod
    def getFont(cls, size):
        return pygame.font.Font("Recursos/font2.ttf", size)
