import sys

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


class Pantalla:
    def __init__(self, menu):
        self.menu = menu
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.screenTexts = []
        self.screenButtons = {}
        self.musica = GestorRecursos.load_sound("UrbanTheme.mp3", "Recursos/Musica/")
        self.click = GestorRecursos.load_sound("click.mp3", "Recursos/Sonidos/")
        self.click_simple = GestorRecursos.load_sound("click_simple.mp3", "Recursos/Sonidos/")
        self.musica.play(-1)

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


class PantallaOpciones(Pantalla):
    def __init__(self, menu):
        Pantalla.__init__(self, menu)

        OPTIONS_TEXT = self.get_font(45).render("Choose the resolution:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))

        self.screenTexts.append((OPTIONS_TEXT, OPTIONS_RECT))

        OPTIONS_BACK = Button(
            image=None,
            pos=(640, 630),
            text_input="BACK",
            font=self.get_font(65),
            base_color="Black",
            hovering_color="Green",
        )

        self.screenButtons.update({"OPTIONS_BACK": OPTIONS_BACK})

        RES1 = Button(
            image=None,
            pos=(640, 330),
            text_input="1280X720",
            font=self.get_font(45),
            base_color="Black",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES1": RES1})

        RES2 = Button(
            image=None,
            pos=(640, 440),
            text_input="700x500",
            font=self.get_font(45),
            base_color="Black",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES2": RES2})

        RES3 = Button(
            image=None,
            pos=(640, 220),
            text_input="1920x1080",
            font=self.get_font(45),
            base_color="Black",
            hovering_color="Green",
        )

        self.screenButtons.update({"RES3": RES3})

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0), position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screenButtons["OPTIONS_BACK"].checkForInput(position):
                    self.menu.pantallaActual = 0
                if self.screenButtons["RES1"].checkForInput(position):
                    print("one")
                if self.screenButtons["RES2"].checkForInput(position):
                    print("chu")
                if self.screenButtons["RES3"].checkForInput(position):
                    print("zree")

    def draw(self, pantalla):
        self.pantalla.fill("white")

        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(
                self.screenButtons[button].text, self.screenButtons[button].text_rect
            )
