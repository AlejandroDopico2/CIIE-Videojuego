import os
import sys

import pygame
import pyglet
from escena import *
from pygame.locals import *

FPS = 60


class Director:
    def __init__(self):
        # Pila de escenas
        self.stack = []
        self.pause = False
        # Flag que nos indica cuando quieren salir de la escena de pygame
        self.exit_pygame_scene = False

    def pygameLoop(self, scene):
        clock = pygame.time.Clock()

        self.exit_pygame_scene = False

        pygame.event.clear()

        while not self.exit_pygame_scene:
            tiempo_pasado = clock.tick(FPS)

            # Definir interfaz para escena con métodos característicos de cada escena

            # escena.bucle de eventos (for de eventos)
            scene.eventsLoop(pygame.event.get())

            teclas_pulsadas = pygame.key.get_pressed()
            if teclas_pulsadas[K_p]:
                self.pause = True

            # Os movimientos do personaje por ejemplo
            scene.update(tiempo_pasado)

            # Os blit dos sprites por ejemplo
            scene.draw(scene.pantalla)
            pygame.display.flip()  # o comando de siempre de pygame

    def execute(self):
        while len(self.stack) > 0:
            escena = self.stack[len(self.stack) - 1]

            if isinstance(escena, PygameScene):
                self.pygameLoop(escena)

            elif isinstance(escena, PygletScene):
                pyglet.app.run()
                escena.close()

            else:
                raise Exception("No se que tipo de escena es")

        pygame.quit()

    def stopScene(self):
        if len(self.stack) > 0:
            escena = self.stack[len(self.stack) - 1]
            # Si la escena es de pygame
            if isinstance(escena, PygameScene):
                # Indicamos en el flag que se quiere salir de la escena
                self.exit_pygame_scene = True
            else:
                raise Exception("No se que tipo de escena es")

    def exitScene(self):
        self.exit_pygame_scene = True
        # Eliminamos la escena actual de la pila (si la hay)
        if len(self.stack) > 0:
            self.stack.pop()
            print(self.stack)

    def exitProgram(self):
        self.stopScene()
        # Vaciamos la lista de escenas pendientes
        self.stack = []

    def changeScene(self, escena):
        self.stopScene()
        # Eliminamos la escena actual de la pila (si la hay)
        if len(self.stack) > 0:
            self.stack.pop()
        # Ponemos la escena pasada en la cima de la pila
        self.stack.append(escena)

    def stackScene(self, escena):
        self.stopScene()
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.stack.append(escena)
        print(self.stack)
