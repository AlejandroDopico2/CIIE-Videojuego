from Niveles.nivel import *


class NivelPlaya(Nivel):
    def __init__(self, director):
        Nivel.__init__(self, director, "Recursos/level1.json")
