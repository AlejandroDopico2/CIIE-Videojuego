from gestorRecursos import *
from Personajes.personajes import MiSprite


class Reliquia(MiSprite):
    def __init__(self):
        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen("Reliquia/reliquia.png", -1)
        self.hoja = self.hoja.convert_alpha()

        datos = GestorRecursos.CargarArchivoCoordenadas("Reliquia/coordReliquia.txt")
        datos = datos.split()

        self.numeroImagen = 0

        self.retardo = 0

        cont = 0
        self.coordenadasHoja = []

        for _ in range(0, 5):
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

        if self.retardo == 6:
            if self.numeroImagen < len(self.coordenadasHoja) - 1:
                self.numeroImagen += 1
            else:
                self.numeroImagen = 0

            self.retardo = 0

        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numeroImagen])