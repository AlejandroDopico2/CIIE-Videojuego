import sys

import pygame

from Niveles.recursosMenu import *
from Niveles.nivel import Nivel


class PantallaNiveles(Pantalla):
    def __init__(self, pantalla):
        Pantalla.__init__(self,pantalla)

        MENU_TEXT = self.get_font(100).render("SELECT LEVEL", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        LEVEL_ONE_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 220),
                            text_input="LEVEL 1", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"LEVEL_ONE":LEVEL_ONE_BUTTON})
        
        LEVEL_TWO_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 330),
                    text_input="LEVEL 2", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"LEVEL_TWO":LEVEL_TWO_BUTTON})
        
        LEVEL_THREE_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 440),
                            text_input="LEVEL 3", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"LEVEL_THREE":LEVEL_THREE_BUTTON})

        BACK = Button(image=None, pos=(640, 630),
                        text_input="BACK", font=self.get_font(65), base_color="#d7fcd4", hovering_color="White")

        self.screenButtons.update({"BACK":BACK})

    def get_font(self,size):
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0),   position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screenButtons["LEVEL_ONE"].checkForInput(position):
                    self.menu.playLevel()
                if self.screenButtons["LEVEL_TWO"].checkForInput(position):
                    print('level chu')
                if self.screenButtons["LEVEL_THREE"].checkForInput(position):
                    print('level three')
                if self.screenButtons["BACK"].checkForInput(position):
                    self.menu.pantallaActual = 0   

    def draw(self, pantalla):
        self.pantalla.fill("black")

        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])

        for button in self.screenButtons:
            self.pantalla.blit(self.screenButtons[button].text, self.screenButtons[button].text_rect)

class PantallaInicio(Pantalla):
    def __init__(self, pantalla):
        Pantalla.__init__(self, pantalla)

        MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        PLAY_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

        self.screenButtons.update({"PLAY":PLAY_BUTTON})

        OPTIONS_BUTTON = Button(image=pygame.image.load("Recursos/Options Rect.png"), pos=(640, 400),
                            text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

        self.screenButtons.update({"OPTIONS":OPTIONS_BUTTON})

        QUIT_BUTTON = Button(image=pygame.image.load("Recursos/Quit Rect.png"), pos=(640, 550),
                            text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

        self.screenButtons.update({"QUIT":QUIT_BUTTON})
    
    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0),   position, 15, 1)
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
            self.pantalla.blit(self.screenButtons[button].text, self.screenButtons[button].text_rect)        


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


    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def playLevel(self):
        nivel = Nivel(self.director)
        self.director.stackScene(nivel)

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            
            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos)