from gestorRecursos import *
from Personajes.personajes import MiSprite


class Moneda(MiSprite):
    def __init__(self):
        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen("moneda/mayan_golden_token.png", -1)
        self.hoja = self.hoja.convert_alpha()

        datos = GestorRecursos.CargarArchivoCoordenadas("moneda/coordMonedaAux.txt")
        datos = datos.split()

        self.numeroImagen = 0

        self.retardo = 0

        cont = 0
        self.coordenadasHoja = []

        for _ in range(0, 24):
            self.coordenadasHoja.append(
                pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3])),
                )
            )
            cont += 4

        self.rect = pygame.Rect(
            100, 100, self.coordenadasHoja[0][2], self.coordenadasHoja[0][3]
        )

        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numeroImagen])

    def update(self, tiempo):
        incrementox = self.velocidad[0] * tiempo
        incrementoy = self.velocidad[1] * tiempo
        self.incrementarPosicion((incrementox, incrementoy))

        self.retardo += 1

        if self.retardo == 3:
            if self.numeroImagen < len(self.coordenadasHoja) - 1:
                self.numeroImagen += 1
            else:
                self.numeroImagen = 0

            self.retardo = 0

        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numeroImagen])

    def draw(self, pantalla, nMonedas):
        nMonedas_string = "x" + str(nMonedas)

        MONEY_TEXT = GestorRecursos.getFont(50).render(nMonedas_string, True, "#b68f40")
        MONEY_RECT = MONEY_TEXT.get_rect(center=(1130, 50))

        pantalla.blit(MONEY_TEXT, MONEY_RECT)

        rect = pygame.Rect(
            1050, 30, self.coordenadasHoja[0][2], self.coordenadasHoja[0][3]
        )

        pantalla.blit(self.image, rect)
