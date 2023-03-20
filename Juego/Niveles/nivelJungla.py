from Niveles.nivel import Nivel


class NivelJungla(Nivel):
    def __init__(self, director):
        Nivel.__init__(self, director, "Recursos/level2.json")
