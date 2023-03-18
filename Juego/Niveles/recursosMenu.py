import pygame
from escena import *
from gestorRecursos import GestorRecursos


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
    def checkForInput(self, posicion):
        (posicionx, posiciony) = posicion
        if (
            (posicionx >= self.rect.left)
            and (posicionx <= self.rect.right)
            and (posiciony >= self.rect.top)
            and (posiciony <= self.rect.bottom)
        ):
            return True
        else:
            return False

    # Si pasamos el raton pro encima del boton
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Pantalla:
    def __init__(self, menu):
        self.menu = menu
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.screenTexts = []
        self.screenButtons = {}
        self.click = GestorRecursos.load_sound("click.mp3", "Recursos/Sonidos/")
        self.click_simple = GestorRecursos.load_sound(
            "click_simple.mp3", "Recursos/Sonidos/"
        )
        self.elementoClic = None

    def update(self):
        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(
                self.screenButtons[button].text, self.screenButtons[button].text_rect
            )

    def changeColor(self, position):
        for button in self.screenButtons:
            value = self.screenButtons[button]
            if position[0] in range(value.rect.left, value.rect.right) and position[
                1
            ] in range(value.rect.top, value.rect.bottom):
                value.text = value.font.render(
                    value.text_input, True, value.hovering_color
                )
            else:
                value.text = value.font.render(value.text_input, True, value.base_color)

    def draw(self, pantalla):
        self.pantalla.fill("black")

        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(
                self.screenButtons[button].text, self.screenButtons[button].text_rect
            )


class PantallaOpciones(Pantalla):
    def __init__(self, menu):
        Pantalla.__init__(self, menu)

        OPTIONS_TEXT = GestorRecursos.getFont(45).render("Choose the difficulty:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))

        self.screenTexts.append((OPTIONS_TEXT, OPTIONS_RECT))

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 630),
            text_input="BACK",
            font=GestorRecursos.getFont(65),
            base_color="White",
            hovering_color="Green",
        )

        self.screenButtons.update({"OPTIONS_BACK": OPTIONS_BACK})

        RES1 = Button(
            image=None,
            pos=(640, 330),
            text_input="Medium",
            font=GestorRecursos.getFont(45),
            base_color="White",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES1": RES1})

        RES2 = Button(
            image=None,
            pos=(640, 440),
            text_input="Hard",
            font=GestorRecursos.getFont(45),
            base_color="White",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES2": RES2})

        RES3 = Button(
            image=None,
            pos=(640, 220),
            text_input="Easy",
            font=GestorRecursos.getFont(45),
            base_color="White",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES3": RES3})

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.screenButtons.items():
                    if button[1].checkForInput(event.pos):
                        self.elementoClic = button[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if self.screenButtons["OPTIONS_BACK"] == self.elementoClic:
                    self.elementoClic = None
                    self.menu.pantallaActual = 0
                if self.screenButtons["RES1"] == self.elementoClic:
                    self.elementoClic = None
                    print("one")
                if self.screenButtons["RES2"] == self.elementoClic:
                    self.elementoClic = None
                    print("chu")
                if self.screenButtons["RES3"] == self.elementoClic:
                    self.elementoClic = None
                    print("zree")

class Menu(PygameScene):
    def __init__(self,director):
        PygameScene.__init__(self,director)

        self.listaPantallas = []

        self.mostrarPrimeraPantalla()

    def update(self, *args):
        return
    
    def mostrarPrimeraPantalla(self):
        self.pantallaActual = 0

    def setPantallaActual(self, numero):
        self.pantallaActual = numero

    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla)

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            
            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos)
