from Niveles.nivel import *


class NivelTemplo(Nivel):
    def __init__(self, director):
        Nivel.__init__(self, director, "Recursos/level3.json")
