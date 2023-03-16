from gestorRecursos import *
from Personajes.personajes import MiSprite


class mercader(MiSprite):
    def __init__(self):
        MiSprite.__init__(self)
        self.hoja = GestorRecursos.CargarImagen(
            "../Mercader/mercader.png", -1
        ).convert_alpha()
        self.numeroImagen = 0
        self.retardo = 0
        self.coordenadasHoja = []
        datos = GestorRecursos.CargarArchivoCoordenadas(
            "../Mercader/coordMerc.txt"
        ).split()
        cont = 0
        for _ in range(0, 7):
            self.coordenadasHoja.append(
                pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3])),
                )
            )
            cont += 4
        self.rect = pygame.Rect(
            self.coordenadasHoja[0][0],
            self.coordenadasHoja[0][1],
            self.coordenadasHoja[0][2],
            self.coordenadasHoja[0][3],
        )  # para que sirve ?
        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numeroImagen])

    def update(self, tiempo):
        incrementox = self.velocidad[0] * tiempo
        incrementoy = self.velocidad[1] * tiempo
        self.incrementarPosicion((incrementox, incrementoy))
        self.retardo += 1
        if self.retardo == 8:
            if self.numeroImagen < len(self.coordenadasHoja) - 1:
                self.numeroImagen += 1
            else:
                self.numeroImagen = 0
            self.retardo = 0
        self.image = pygame.transform.scale(
            self.hoja.subsurface(self.coordenadasHoja[self.numeroImagen]),
            (
                self.hoja.subsurface(
                    self.coordenadasHoja[self.numeroImagen]
                ).get_width()
                * 1.5,
                self.hoja.subsurface(
                    self.coordenadasHoja[self.numeroImagen]
                ).get_height()
                * 1.5,
            ),
        )
