from Niveles.recursosMenu import *
from escena import *

class PantallaTienda(Pantalla):
    def __init__(self, menu):
        Pantalla.__init__(self, menu)

        MENU_TEXT = self.get_font(100).render("MERCHANT", True, "#85bb65")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        self.screenTexts.append((MENU_TEXT, MENU_RECT))

        POCION_VIDA = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 220),
                            text_input="HEALTH POCION", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"POCION_VIDA":POCION_VIDA})
        
        CLOSE_BUTTON = Button(image=pygame.image.load("Recursos/Play Rect.png"), pos=(640, 660),
                            text_input="CLOSE", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        self.screenButtons.update({"CLOSE_BUTTON":CLOSE_BUTTON})

    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Recursos/font.ttf", size)

    def eventsLoop(self, lista_eventos):
        position = pygame.mouse.get_pos()
        self.changeColor(position)
        pygame.draw.circle(self.pantalla, (0, 255, 0),   position, 15, 1)
        for event in lista_eventos:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.screenButtons["CLOSE_BUTTON"].checkForInput(position):
                    self.menu.director.tienda = False
                    self.menu.director.exitScene()

    def draw(self, pantalla):
        self.pantalla.fill("black")
        for text in self.screenTexts:
            self.pantalla.blit(text[0], text[1])
        for button in self.screenButtons:
            self.pantalla.blit(self.screenButtons[button].text, self.screenButtons[button].text_rect)

class MenuTienda(PygameScene):
    def __init__(self, director):
        PygameScene.__init__(self, director)

        self.director = director
        self.listaPantallas = [PantallaTienda(self)]
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
                #TODO Aquí en vez de exit program haberia que facer algo en plan stop scene e desapilar de director
            
            self.listaPantallas[self.pantallaActual].eventsLoop(lista_eventos)
