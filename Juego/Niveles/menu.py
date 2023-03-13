from Niveles.nivel import *
from Niveles.nivelPlaya import *
from Niveles.nivelJungla import *
from Niveles.recursosMenu import *


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Inicializacion de propiedades
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # Actualizacion
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # Si clickamos
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # Si pasamos el raton pro encima del boton
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


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
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0), position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screenButtons["LEVEL_ONE"].checkForInput(position):
                    self.menu.playLevel(1)
                if self.screenButtons["LEVEL_TWO"].checkForInput(position):
                    self.menu.playLevel(2)
                if self.screenButtons["LEVEL_THREE"].checkForInput(position):
                    print("level three")
                if self.screenButtons["BACK"].checkForInput(position):
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
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0), position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screenButtons["PLAY"].checkForInput(position):
                    self.menu.pantallaActual = 2
                if self.screenButtons["OPTIONS"].checkForInput(position):
                    self.menu.pantallaActual = 1
                if self.screenButtons["QUIT"].checkForInput(position):
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

        self.director = director

        self.listaPantallas = []

        self.listaPantallas.append(PantallaInicio(self))
        self.listaPantallas.append(PantallaOpciones(self))
        self.listaPantallas.append(PantallaNiveles(self))

        self.mostrarPantallaInicial()

    def update(self, *args):
        return

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
