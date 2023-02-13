#https://coderslegacy.com/python/pygame-platformer-game-development/?utm_content=cmp-true

import pygame, sys
from pygame.locals import *
 
HEIGHT = 480
WIDTH = 480
ACC = 0.5
FRIC = -0.12
FPS = 60
CHARACT_SPRITE = pygame.transform.scale(pygame.image.load("homero.png"), [HEIGHT / 10, WIDTH / 5])
CHARACT_INIT_POS = (HEIGHT / 20, WIDTH / 4)
JUMP_LEN = -10

pygame.init()
vec = pygame.math.Vector2
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CIIE")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = CHARACT_SPRITE
        self.rect = self.surf.get_rect()
        self.pos = vec(CHARACT_INIT_POS)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #temporalmente limitado por la pantalla a izq. y der.
        if self.pos.x > WIDTH - CHARACT_INIT_POS[0]:
            self.pos.x = WIDTH - CHARACT_INIT_POS[0]
        if self.pos.x < CHARACT_INIT_POS[0]:
            self.pos.x = CHARACT_INIT_POS[0]
        if self.pos.y < HEIGHT / 5:
            self.pos.y = HEIGHT / 5
        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
    
    def jump(self):
        if self.pos.y == HEIGHT * 0.95625:
            self.vel.y = JUMP_LEN
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, HEIGHT / 20))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
PT1 = platform()
P1 = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
platforms = pygame.sprite.Group()
platforms.add(PT1)
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
     
    displaysurface.fill((100,100,255))
    P1.move()
    P1.update()
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(FPS)