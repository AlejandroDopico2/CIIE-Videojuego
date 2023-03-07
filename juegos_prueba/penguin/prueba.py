import pygame

# ----------------------------------------------
# Constantes, como anchos y largo de pantalla, etc.
# ----------------------------------------------


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# ----------------------------------------------
# Clases y Funciones utilizadas (lo explicare en la siguiente parte)
# ----------------------------------------------

def main():
    pygame.init()
    
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("club penguin")

    fondo = pygame.image.load("fondo.jpg").convert()
    tux = pygame.image.load("tux.png").convert_alpha()

    tux_pos_x = 550
    tux_pos_y = 200

    screen.blit(fondo, (0, 0))
    screen.blit(tux, (tux_pos_x, tux_pos_y))

    pygame.display.flip()

    while True:
        # Posibles entradas del teclado y mouse

        tux_pos_x = tux_pos_x - 1

        if tux_pos_x < 1:
            tux_pos_x = 550

        screen.blit(fondo, (0, 0))
        screen.blit(tux, (tux_pos_x, tux_pos_y))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()