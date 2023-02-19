import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, size, center, color):
        super().__init__()
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center = center)
        self.color = color
        self.center = center
    
    def dibujar(self, pantalla):
        self.surf.fill(self.color)
        pantalla.blit(self.surf, self.center)
