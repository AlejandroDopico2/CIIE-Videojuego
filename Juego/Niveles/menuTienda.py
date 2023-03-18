from Niveles.recursosMenu import *
from escena import *
from gestorRecursos import *

class PantallaTienda(Pantalla):
    def __init__(self, menu, jugador):
        Pantalla.__init__(self, menu)

        self.MENU_TEXT = GestorRecursos.getFont(100).render("MERCHANT: " + str(jugador.money) + "$", True, "#85bb65")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((self.MENU_TEXT, self.MENU_RECT))

        POCION_VIDA = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 220),
                            text_input="HEALTH POCION", font=GestorRecursos.getFont(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"POCION_VIDA":POCION_VIDA})

        POCION_VELOCIDAD = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 330),
                            text_input="SPEED POCION", font=GestorRecursos.getFont(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"POCION_VELOCIDAD":POCION_VELOCIDAD})
        
        CLOSE_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 660),
                            text_input="CLOSE", font=GestorRecursos.getFont(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"CLOSE_BUTTON":CLOSE_BUTTON})

    def eventsLoop(self, lista_eventos, jugador):
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0),   position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.elementoClic = None

                for button in self.screenButtons.items():
                    if button[1].checkForInput(event.pos):
                        self.elementoClic = button[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if self.screenButtons["CLOSE_BUTTON"] == self.elementoClic:
                    self.elementoClic = None
                    self.menu.director.tienda = False
                    self.menu.director.exitScene()
                if self.screenButtons["POCION_VELOCIDAD"] == self.elementoClic and jugador.money >= 1:
                    jugador.money -= 1
                    jugador.start_powerup('velocidad')
                    self.draw(Pantalla, jugador)
                if self.screenButtons["POCION_VIDA"] == self.elementoClic and jugador.money >= 2:
                    jugador.money -= 2
                    jugador.cura()
                    self.draw(Pantalla, jugador)
                

    def draw(self, pantalla, jugador):
        self.pantalla.fill("black")
        self.screenTexts[0] = (GestorRecursos.getFont(100).render("MERCHANT: " + str(jugador.money) + "$", True, "#85bb65"), self.MENU_RECT)
        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])
        for button in self.screenButtons:
            self.pantalla.blit(self.screenButtons[button].text, self.screenButtons[button].text_rect)

class MenuTienda(PygameScene):
    def __init__(self, director, jugador):
        PygameScene.__init__(self, director)

        self.director = director
        self.listaPantallas = [PantallaTienda(self, jugador)]
        self.mostrarPantallaPausa()
        self.jugador = jugador
    
    def update(self, *args):
        return
    
    def draw(self, pantalla):
        self.listaPantallas[self.pantallaActual].draw(pantalla, self.jugador)

    def mostrarPantallaPausa(self):
        self.pantallaActual = 0

    def eventsLoop(self, lista_eventos):
        for event in lista_eventos:
            if event.type == pygame.QUIT:
                self.director.exitProgram()
                #TODO Aquí en vez de exit program haberia que facer algo en plan stop scene e desapilar de director
            
            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos, self.jugador)
