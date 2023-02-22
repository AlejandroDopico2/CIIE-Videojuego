import pygame

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720

class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def eventsLoop(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")

class PygameScene(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        # Inicializamos la libreria de pygame (si no esta inicializada ya)
        pygame.init()
        # Creamos la pantalla (si no esta creada ya)
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))


class PygletScene(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)
