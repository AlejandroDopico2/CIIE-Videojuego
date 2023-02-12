import sys, pygame
import numpy as np
pygame.init()

size = width, height = 640, 480
speedSP = [0, -1]
speedA = [-1, 0]
speedD = [1, 0]
black = 0, 0, 0

#activamos repeticion de teclas
pygame.key.set_repeat(5, 5)
#creamos ventana del juego
screen = pygame.display.set_mode(size)
#cargamos imagen y la escalamos para hacerla mas grande
character = pygame.transform.scale(pygame.image.load("homero.png"), [48, 111])
#nos da la area rect. de la superficie. Empieza en las coord. (0,0) (esquina sup. izq.)
characterRect = character.get_rect()
#desplazamos personaje hacia la esquina inferior izq
characterRect.bottom = height

while True:
    for event in pygame.event.get():
        #evento salir del juego (X)
        if event.type == pygame.QUIT: 
            sys.exit()

        #eventos pulsar A, D, SPACE
        keys = pygame.key.get_pressed()
        movement = np.array([0, 0])
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_a]:
                movement += np.array(speedA)
            if keys[pygame.K_d]:
                movement += np.array(speedD)
            if keys[pygame.K_SPACE]:#TODO crear salto
                movement += np.array(speedSP)
            characterRect = characterRect.move(movement)

            #comprobamos que no el personaje no se salga de la ventana
            if characterRect.left < 0:
                characterRect.left = 0
            if characterRect.right > width:
                characterRect.right = width
            if characterRect.top < 0:
                characterRect.top = 0
            if characterRect.bottom > height:
                characterRect.bottom = height

    #pintamos de negro toda la ventana
    screen.fill(black)
    #pintamos nueva pos. del personaje
    screen.blit(character, characterRect)
    #mostramos lo pintado en el buffer
    pygame.display.flip()