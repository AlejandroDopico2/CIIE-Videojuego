import pygame.mixer_music
from Niveles.nivel import *
from Niveles.nivelJungla import *
from Niveles.nivelPlaya import *
from Niveles.recursosMenu import *



class PantallaNiveles(Pantalla):
    def __init__(self, pantalla):
        Pantalla.__init__(self, pantalla)

        MENU_TEXT = self.get_font(100).render("SELECT LEVEL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        LEVEL_ONE_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 220),
            text_input="LEVEL 1",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"LEVEL_ONE": LEVEL_ONE_BUTTON})

        LEVEL_TWO_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 330),
            text_input="LEVEL 2",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"LEVEL_TWO": LEVEL_TWO_BUTTON})

        LEVEL_THREE_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 440),
            text_input="LEVEL 3",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"LEVEL_THREE": LEVEL_THREE_BUTTON})

        BACK = Button(
            image=None,
            pos=(640, 630),
            text_input="BACK",
            font=self.get_font(65),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"BACK": BACK})

    def get_font(self, size):
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):

        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None

                for button in self.screenButtons.items():
                    if button[1].checkForInput(event.pos):
                        self.elementoClic = button[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if self.screenButtons["LEVEL_ONE"]==self.elementoClic:
                    self.elementoClic = None
                    self.click.play()
                    self.menu.playLevel(1)
                if self.screenButtons["LEVEL_TWO"]==self.elementoClic:
                    self.elementoClic = None
                    self.click.play()
                    self.menu.playLevel(2)
                if self.screenButtons["LEVEL_THREE"]==self.elementoClic:
                    self.elementoClic = None
                    self.click.play()
                    print("level three")
                if self.screenButtons["BACK"]==self.elementoClic:
                    self.elementoClic = None
                    self.menu.pantallaActual = 0

    def draw(self, pantalla):
        self.pantalla.fill("black")

        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(
                self.screenButtons[button].text, self.screenButtons[button].text_rect
            )


class PantallaInicio(Pantalla):
    def __init__(self, pantalla):
        Pantalla.__init__(self, pantalla)

        MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        PLAY_BUTTON = Button(
            image=pygame.image.load("Recursos/Play Rect.png"),
            pos=(640, 250),
            text_input="PLAY",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"PLAY": PLAY_BUTTON})

        OPTIONS_BUTTON = Button(
            image=pygame.image.load("Recursos/Options Rect.png"),
            pos=(640, 400),
            text_input="OPTIONS",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"OPTIONS": OPTIONS_BUTTON})

        QUIT_BUTTON = Button(
            image=pygame.image.load("Recursos/Quit Rect.png"),
            pos=(640, 550),
            text_input="QUIT",
            font=self.get_font(75),
            base_color="#d7fcd4",
            hovering_color="White",
        )

        self.screenButtons.update({"QUIT": QUIT_BUTTON})

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):

        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None
                for button in self.screenButtons.items():
                    if button[1].checkForInput(event.pos):
                        self.elementoClic = button[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if self.screenButtons["PLAY"]==self.elementoClic:
                    self.elementoClic = None
                    self.click_simple.play()
                    self.menu.pantallaActual = 2
                if self.screenButtons["OPTIONS"]==self.elementoClic:
                    self.elementoClic = None
                    self.click_simple.play()
                    self.menu.pantallaActual = 1
                if self.screenButtons["QUIT"]==self.elementoClic:
                    self.elementoClic = None
                    self.click_simple.play()
                    self.menu.director.exitProgram()

    def draw(self, pantalla):
        self.pantalla.fill("black")

        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(
                self.screenButtons[button].text, self.screenButtons[button].text_rect
            )


class Menu(PygameScene):
    def __init__(self, director):
        PygameScene.__init__(self, director)

        self.initMixer()
        self.director = director

        self.listaPantallas = []

        self.listaPantallas.append(PantallaInicio(self))
        self.listaPantallas.append(PantallaOpciones(self))
        self.listaPantallas.append(PantallaNiveles(self))

        self.mostrarPantallaInicial()

    def initMixer(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        pygame.mixer.music.load("Recursos/Musica/UrbanTheme.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.02)

    def update(self, *args):
        return

    def setPantallaActual(self, numero):
        self.pantallaActual = numero

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def playLevel(self, level):
        if level == 1:
            nivel = NivelPlaya(self.director)
        elif level == 2:
            nivel = NivelJungla(self.director)
        self.director.stackScene(nivel)

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            
            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos)
