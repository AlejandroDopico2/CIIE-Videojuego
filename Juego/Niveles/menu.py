import sys

import pygame

from Niveles.nivel import ANCHO_PANTALLA, ALTO_PANTALLA
from gestorRecursos import GestorRecursos


class Button():

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
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    # Si pasamos el raton pro encima del boton
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Menu():

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.imagen = pygame.transform.scale(self.pantalla, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.main_menu()


    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def play(self):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            self.pantalla.fill("black")

            PLAY_TEXT = self.get_font(45).render("This is the PLAY screen.", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
            self.pantalla.blit(PLAY_TEXT, PLAY_RECT)

            PLAY_BACK = Button(image=None, pos=(640, 460),
                               text_input="BACK", font=self.get_font(75), base_color="White", hovering_color="Green")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(self.pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.pantalla.fill("white")

            OPTIONS_TEXT = self.get_font(45).render("Choose the resolution:", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
            self.pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 630),
                                  text_input="BACK", font=self.get_font(65), base_color="Black", hovering_color="Green")

            RES1 = Button(image=None, pos=(640, 330),
                                  text_input="1280X720", font=self.get_font(45), base_color="Black", hovering_color="Green")

            RES2 = Button(image=None, pos=(640, 440),
                          text_input="700x500", font=self.get_font(45), base_color="Black", hovering_color="Green")

            RES3 = Button(image=None, pos=(640, 220),
                          text_input="1920x1080", font=self.get_font(45), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            RES1.changeColor(OPTIONS_MOUSE_POS)
            RES2.changeColor(OPTIONS_MOUSE_POS)
            RES3.changeColor(OPTIONS_MOUSE_POS)

            OPTIONS_BACK.update(self.pantalla)
            RES1.update(self.pantalla)
            RES2.update(self.pantalla)
            RES3.update(self.pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if RES1.checkForInput(OPTIONS_MOUSE_POS):
                        self.pantalla.blit(pygame.transform.scale(self.imagen, (1280, 720)),(0,0))
                        self.main_menu()
                    if RES2.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if RES3.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:

            self.pantalla.fill("black")

            # Pintamos el fondo del menu
            self.pantalla.blit(self.pantalla, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Ponemos el texto
            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("Recursos/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("Recursos/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.pantalla.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Si pulsamos un boton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return 0
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

