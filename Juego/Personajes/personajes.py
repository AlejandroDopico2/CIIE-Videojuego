from escena import ANCHO_PANTALLA, ALTO_PANTALLA
from gestorRecursos import *

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
DISPARA = 5

# Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2
SPRITE_ATACANDO = 3

# Velocidades
VELOCIDAD_JUGADOR = 0.3
VELOCIDAD_SALTO_JUGADOR = 0.4

RETARDO_ANIMACION_JUGADOR = 5
GRAVEDAD = 0.0006

RECARGA_JUGADOR = 12
VELOCIDAD_BALA = 0.5

VELOCIDAD_ESPECTRO = 0.18
VELOCIDAD_DEMONIO = 0.15
VELOCIDAD_ESQUELETO = 0.22
VELOCIDAD_CANGREJO = 0.10
VELOCIDAD_PAJARO = 0.14

RETARDO_ANIMACION_JUGADOR = 5
RETARDO_ANIMACION_ESPECTRO = 7
RETARDO_ANIMACION_DEMONIO = 6
RETARDO_ANIMACION_CANGREJO = 4
RETARDO_ANIMACION_ESQUELETO = 4
RETARDO_ANIMACION_PAJARO = 4

GRAVEDAD = 0.0006


class MiSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx + incrementox, posy + incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0] * tiempo
        incrementoy = self.velocidad[1] * tiempo
        self.incrementarPosicion((incrementox, incrementoy))


class BarraSalud(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes):
        MiSprite.__init__(self)

        self.imagen = GestorRecursos.CargarImagen(archivoImagen)


class Personaje(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto,
                 retardoAnimacion):

        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()
        # self.hoja = pygame.transform.scale(self.hoja, (200, 200))

        self.movimientos = [QUIETO]
        self.mirando = DERECHA
        self.vuela = False

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        for linea in range(0, 3):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for _ in range(0, numImagenes[linea]):
                tmp.append(
                    pygame.Rect((int(datos[cont]), int(datos[cont + 1])), (int(datos[cont + 2]), int(datos[cont + 3]))))
                cont += 4

        self.retardoMovimiento = 0
        self.numPostura = QUIETO

        self.rect = pygame.Rect(100, 100, self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],
                                self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        self.actualizarPostura()

    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        if self.retardoMovimiento < 0:
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1
            if len(self.coordenadasHoja[1]) == 0:
                self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])
            else:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si es Demonio, el flip se hace al revés
            if isinstance(self, Pajaro):
                if self.mirando == DERECHA:
                    self.mirando = IZQUIERDA
                else:
                    self.mirando = DERECHA

            if self.mirando == DERECHA:
                if len(self.coordenadasHoja[1]) == 0:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])
                else:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                if len(self.coordenadasHoja[1]) == 0:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[0][0]), 1, 0)
                else:
                    self.image = pygame.transform.flip(
                        self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

    def mover(self, movimientos):
        self.movimientos = movimientos

    def update(self, grupoPlataformas, tiempo):
        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha        
        if (IZQUIERDA in self.movimientos) or (DERECHA in self.movimientos):
            # Esta mirando hacia ese lado
            if (IZQUIERDA in self.movimientos):
                self.mirando = IZQUIERDA
            else:
                self.mirando = DERECHA

            # Si vamos a la izquierda, le ponemos velocidad en esa dirección
            if IZQUIERDA in self.movimientos:
                velocidadx = -self.velocidadCarrera
            # Si vamos a la derecha, le ponemos velocidad en esa dirección
            else:
                velocidadx = self.velocidadCarrera

            # Si no estamos en el aire
            if self.numPostura != SPRITE_SALTANDO and not self.vuela:
                # La postura actual sera estar caminando
                self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                    self.numPostura = SPRITE_SALTANDO
                else:
                    self.numPostura = SPRITE_ANDANDO

        # Si queremos saltar
        if ARRIBA in self.movimientos:
            # La postura actual sera estar saltando
            self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        if DISPARA in self.movimientos:
            #Sprites no implementados asi que se queda quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO

        # Si no se ha pulsado ninguna tecla
        if QUIETO in self.movimientos:
            # Si no estamos saltando, la postura actual será estar quieto
            if not self.numPostura == SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO
            velocidadx = 0

        # Además, si estamos en el aire
        if self.numPostura == SPRITE_SALTANDO or self.numPostura == SPRITE_ANDANDO:
            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colision con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollide(self, grupoPlataformas, False)
            if len(plataforma) > 0:
                for i in range(len(plataforma)):
                    #  Ademas, esa colision solo nos interesa cuando estamos cayendo
                    #  y solo es efectiva cuando caemos encima, no de lado, es decir,
                    #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
                    if (plataforma[i] != None) and (velocidady > 0) and (plataforma[i].rect.top > self.rect.top):
                        # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                        #  para poder detectar cuando se cae de ella
                        self.establecerPosicion(
                            (self.posicion[0], plataforma[i].posicion[1] - plataforma[i].rect.height + 1))
                        # Lo ponemos como quieto
                        self.numPostura = SPRITE_QUIETO
                        # Y estará quieto en el eje y
                        velocidady = 0

                    elif (self.rect.bottom - 1 > plataforma[i].rect.top and self.rect.bottom < plataforma[i].rect.top +
                          plataforma[i].rect.height):
                        posicion = self.posicion[0] - 1 if (plataforma[i].rect.left > self.rect.left) else \
                        self.posicion[0] + 1
                        self.establecerPosicion((posicion, self.posicion[1]))
                        velocidadx = 0

            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad
            else:
                velocidady += GRAVEDAD * tiempo

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)

        return


class Jugador(Personaje):
    def __init__(self):
        # Personaje.__init__(self, 'spritex2.png', 'coord2.txt', [12, 8, 4], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR,
        #    RETARDO_ANIMACION_JUGADOR)
        Personaje.__init__(self, 'Nera/NeraFull.png', 'Nera/coords.txt', [4, 8, 4], VELOCIDAD_JUGADOR,
                           VELOCIDAD_SALTO_JUGADOR,
                           RETARDO_ANIMACION_JUGADOR)
        self.vida = 3
        self.inmune = False
        self.ultimoGolpe = pygame.time.get_ticks()
        self.ticks = 0
        self.recarga = 0
        # self.barra = BarraSalud('health_bar1.png', 'coordBarraVida.txt', [1, 1, 1, 1, 1, 1])

    def reduce_recarga(self):
        self.recarga -= 1


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, dispara, bala):
        movimientos = []
        if teclasPulsadas[arriba] and self.numPostura != SPRITE_SALTANDO:
            movimientos.append(ARRIBA)
        if teclasPulsadas[derecha]:
            movimientos.append(DERECHA)
        if teclasPulsadas[izquierda]:
            movimientos.append(IZQUIERDA)
        if teclasPulsadas[dispara]:
            if self.recarga <= 0:
                self.recarga = RECARGA_JUGADOR
                movimientos.append(DISPARA)
                bala.vive(self.rect.left, self.rect.bottom, self.mirando)
        if len(movimientos) == 0:
            movimientos.append(QUIETO)
        Personaje.mover(self, movimientos)

    def dañarJugador(self):
        if not self.inmune:
            self.vida -= 1
            self.inmune = True
            self.ultimoGolpe = pygame.time.get_ticks()


class Bala(MiSprite):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, mirando):

        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 0
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []

        self.coordenadasHoja.append([])
        tmp = self.coordenadasHoja[0]
        for _ in range(0, numImagenes[0]):
            tmp.append(
                pygame.Rect((int(datos[cont]), int(datos[cont + 1])), (int(datos[cont + 2]), int(datos[cont + 3]))))
            cont += 4

        if mirando == 1:
            self.direccion = -1
            self.velocidad = (-velocidad, 0)
        else:
            self.direccion = 1
            self.velocidad = (velocidad, 0)

        self.alive = False

        self.rect = pygame.Rect(100, 100, self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],
                                self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])

        #self.rect = self.image.get_rect()
        #self.rect.center = (x, y)
        #self.direction = direction

    def muere(self):
        self.alive = False

    def vive(self, left, bottom, mirando):
        self.alive = True
        if mirando == 1:
            self.posicion = (left, bottom-50)
            self.direccion = -1
            self.velocidad = (-abs(self.velocidad[0]), 0)
        else:
            self.posicion = (left + 40, bottom - 50)
            self.direccion = 1
            self.velocidad = (abs(self.velocidad[0]), 0)
        self.establecerPosicion(self.posicion)

    def miraSiHaySignosVitales(self):
        return self.alive

    def update(self,tiempo):
        MiSprite.update(self, tiempo)

        #checkea off screen
        #if not self.game.screen.get_rect().contains(self.rect):
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:
            self.muere()


class Enemigo(Personaje):
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto,
                           retardoAnimacion)
        self.vida = 1

    def mover_cpu(self, jugador):
        # Por defecto un enemigo no hace nada
        return


class Espectro(Enemigo):
    def __init__(self):
        Enemigo.__init__(self, 'espectro.png', 'coord3.txt', [1, 0, 0], VELOCIDAD_ESPECTRO, 0,
                         RETARDO_ANIMACION_ESPECTRO)
        self.count = 0
        self.vuela = True
        self.vida = 1

    def mover_cpu(self, jugador):

        # Movemos solo a los enemigos que estén en la pantalla
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            # Si estamos en una plataforma quietos, el fantasma dará vueltas cerca nuestra
            if jugador.posicion[1] < self.posicion[
                1] and QUIETO in jugador.movimientos and jugador.numPostura != SPRITE_SALTANDO:
                if self.count < 90:
                    Personaje.mover(self, [IZQUIERDA])
                elif self.count == 180:
                    self.count = 0
                else:
                    Personaje.mover(self, [DERECHA])
                self.count += 1
            else:
                # Si estamos en suelo y miramos para él se queda quieto, si no miramos se acercará por nuestras espaldas
                if jugador.posicion[0] < self.posicion[0] and jugador.mirando == IZQUIERDA:
                    Personaje.mover(self, [IZQUIERDA])
                elif jugador.posicion[0] < self.posicion[0] and jugador.mirando == DERECHA:
                    Personaje.mover(self, [QUIETO])
                elif jugador.posicion[0] > self.posicion[0] and jugador.mirando == DERECHA:
                    Personaje.mover(self, [DERECHA])
                elif jugador.posicion[0] > self.posicion[0] and jugador.mirando == IZQUIERDA:
                    Personaje.mover(self, [QUIETO])

        # Si este personaje no está en pantalla, no hará nada
        else:
            Personaje.mover(self, [QUIETO])


class Demonio(Enemigo):
    def __init__(self):
        Enemigo.__init__(self, 'Demonio/demon__spritesheet.png', 'coordDiablo.txt', [6, 12, 5, 15, 17],
                         VELOCIDAD_DEMONIO, 0,
                         RETARDO_ANIMACION_DEMONIO)
        self.count = 0
        self.vuela = False
        self.vida = 3

    def mover_cpu(self, jugador):
        # Movemos solo a los enemigos que estén en la pantalla
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            if jugador.posicion[0] < self.posicion[0]:

                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:

                Personaje.mover(self, [DERECHA])
            else:
                Personaje.mover(self, [QUIETO])


class Cangrejo(Enemigo):
    def __init__(self):
        Enemigo.__init__(self, 'Cangrejo/cangrejo.png', 'coordCangrejo.txt', [4, 6, 0, 0], VELOCIDAD_CANGREJO, 0,
                         RETARDO_ANIMACION_CANGREJO)
        self.count = 0
        self.vuela = False

    def mover_cpu(self, jugador):
        # Movemos solo a los enemigos que estén en la pantalla
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            # Si estamos en una plataforma quietos, el fantasma dará vueltas cerca nuestra
            if jugador.posicion[0] < self.posicion[0]:
                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:
                Personaje.mover(self, [DERECHA])


class Esqueleto(Enemigo):
    def __init__(self):
        Enemigo.__init__(self, 'Esqueleto/esqueleto.png', 'coordEsqueleto.txt', [8, 6, 1, 0], VELOCIDAD_ESQUELETO, 0,
                         RETARDO_ANIMACION_ESQUELETO)
        self.count = 0
        self.vuela = False

    def mover_cpu(self, jugador):
        # Movemos solo a los enemigos que estén en la pantalla
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            # Si estamos en una plataforma quietos, el fantasma dará vueltas cerca nuestra
            if jugador.posicion[0] < self.posicion[0]:
                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:
                Personaje.mover(self, [DERECHA])


class Pajaro(Enemigo):
    def __init__(self):
        Enemigo.__init__(self, 'Bird Spritesheet.png', 'coordBird.txt', [2, 3, 8, 3], VELOCIDAD_PAJARO, 0,
                         RETARDO_ANIMACION_PAJARO)
        self.count = 0
        self.vuela = True

    def mover_cpu(self, jugador):
        # Movemos solo a los enemigos que estén en la pantalla
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            # Si estamos en una plataforma quietos, el fantasma dará vueltas cerca nuestra

            if self.count < 260:
                Personaje.mover(self, [DERECHA])
            elif self.rect.left == 70:
                self.count = 0
            else:
                Personaje.mover(self, [IZQUIERDA])
            self.count += 1
