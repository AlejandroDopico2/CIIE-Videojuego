from escena import *
from Niveles.recursosMenu import *


class PantallaPausa(Pantalla):
    def __init__(self, menu):
        Pantalla.__init__(self, menu)

        MENU_TEXT = GestorRecursos.getFont(100).render("PAUSE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        RESUME_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 220),
            text_input="RESUME",
            font=GestorRecursos.getFont(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"RESUME_BUTTON": RESUME_BUTTON})

        OPTIONS_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 330),
            text_input="OPTIONS",
            font=GestorRecursos.getFont(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"OPTIONS_BUTTON": OPTIONS_BUTTON})

        EXIT_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 440),
            text_input="EXIT",
            font=GestorRecursos.getFont(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"EXIT_BUTTON": EXIT_BUTTON})

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None
                for button in self.screenButtons.items():
                    if button[1].checkForInput(event.pos):
                        self.elementoClic = button[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if self.screenButtons["RESUME_BUTTON"] == self.elementoClic:
                    self.elementoClic = None
                    # TODO desapilar en vez de cambiar a pantalla 0
                    self.menu.director.pause = False
                    self.menu.director.exitScene()
                if self.screenButtons["OPTIONS_BUTTON"] == self.elementoClic:
                    self.elementoClic = None
                    self.menu.pantallaActual = 1
                if self.screenButtons["EXIT_BUTTON"] == self.elementoClic:
                    self.elementoClic = None
                    self.menu.director.exitProgram()


class MenuPausa(PygameScene):
    def __init__(self, director):
        PygameScene.__init__(self, director)

        self.director = director

        self.listaPantallas = []

        self.listaPantallas.append(PantallaPausa(self))
        self.listaPantallas.append(PantallaOpciones(self))

        self.mostrarPantallaPausa()

    def update(self, *args):
        return

    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla)

    def mostrarPantallaPausa(self):
        self.pantallaActual = 0

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.exitProgram()
                # TODO Aquí en vez de exit program haberia que facer algo en plan stop scene e desapilar de director

            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos)
