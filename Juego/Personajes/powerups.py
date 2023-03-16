from Personajes.personajes import MiSprite
from gestorRecursos import *

class Powerup(MiSprite):
    def __init__(
            self,
            archivoImagen,
            archivoCoordenadas,
            numImagenes,
            tipo
    ):
        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()

        #self.numeroImagen = numImagenes
        self.type = tipo

        cont = 0
        self.coordenadasHoja = []

        self.coordenadasHoja.append([])
        tmp = self.coordenadasHoja[0]
        for _ in range(0, numImagenes[0]):
            tmp.append(
                pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3])),
                )
            )
            cont += 4

        self.rect = pygame.Rect(
            100, 100, self.coordenadasHoja[0][0][2], self.coordenadasHoja[0][0][3]
        )

        self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])


class Powerup_velocidad(MiSprite):
    def __init__(self):
        Powerup.__init__(
            self,
            "potions\Icon19.png",
            "potions\coordPotion19.txt",
            [1],
            "velocidad"
        )

class Powerup_vida(MiSprite):
    def __init__(self):
        Powerup.__init__(
            self,
            "potions\Icon1.png",
            "potions\coordPotion1.txt",
            [1],
            "vida"
        )