from escena import ALTO_PANTALLA, ANCHO_PANTALLA
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
SPRITE_ATACANDO_QUIETO = 3
SPRITE_ATACANDO_ANDANDO = 4
SPRITE_ATACANDO_SALTANDO = 5

RECARGA_JUGADOR = 20
VELOCIDAD_BALA = 0.5

# Velocidades
VELOCIDAD_JUGADOR = 0.3
VELOCIDAD_SALTO_JUGADOR = 0.4
VELOCIDAD_ESPECTRO = 0.18
VELOCIDAD_DEMONIO = 0.15
VELOCIDAD_ESQUELETO = 0.22
VELOCIDAD_CANGREJO = 0.10
VELOCIDAD_PAJARO = 0.14

# Retardos
RETARDO_ANIMACION_JUGADOR = 5
RETARDO_ANIMACION_ESPECTRO = 7
RETARDO_ANIMACION_DEMONIO = 6
RETARDO_ANIMACION_CANGREJO = 4
RETARDO_ANIMACION_ESQUELETO = 4
RETARDO_ANIMACION_PAJARO = 4

DURACION_POWERUP = 200
GRAVEDAD = 0.0006


class MiSprite(pygame.sprite.Sprite):
    """
       Clase que representa cualquier objeto presente en el juego.

       ...

       Atributos
       ----------
       posicion: tupla
           posicion que ocupa en el eje x e y
       velocidad: tupla
           velocidad que adopta en el eje x e y
       scroll: tupla
           valor del scroll en el eje x e y

       Métodos
       -------
       establecerPosicion(posicion)
           Establece la posición del objeto en particular

       establecerPosicionPantalla(scrollDecorado)
           Establece la posición en pantalla del decorado

       incrementarPosicion(incremento)
           Incrementa la posición del objeto

       update(tiempo)
           Actualiza la posición del objeto en particular
    """

    def __init__(self):
        """
        Parámetros
        ----------
        """

        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll = (0, 0)

    def establecerPosicion(self, posicion):
        """Establece la posición del objeto en particular.

        Parámetros
        ----------
        posicion : tupla
            La posicion que se quiere establecer para el objeto

        """
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        """Establece la posición en pantalla del decorado

        Parámetros
        ----------
        scrollDecorado : tupla
            La posicion que se quiere establecer para el objet
        """
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        """Incrementa la posición del objeto.

        Parámetros
        ----------
        incremento : tupla
            La posicion que se quiere establecer para el objet
        """
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx + incrementox, posy + incrementoy))

    def update(self, tiempo):
        """Establece la posición del objeto en particular.

        Parámetros
        ----------
        tiempo : int
            Los milisegundos para la sincronización de cada frame.
        """
        incrementox = self.velocidad[0] * tiempo
        incrementoy = self.velocidad[1] * tiempo
        self.incrementarPosicion((incrementox, incrementoy))


class Personaje(MiSprite):
    """
    Clase que representa cualquier Personaje presente en el juego

    ..

    Atributos
    ----------
    hoja: Surface
        imagen que representa al Personaje
    movimientos: List[int]
        movimiento que está realizando (QUIETO, IZQUIERDA, DERECHA, ARRIBA)
    mirando: int
        dirección a la que está mirando
    vuela: bool
        atributo que le otorga la posibilidad de volar
    numPostura: int
        postura que toma el Personaje (SPRITE_QUIETO,SPRITE_ANDANDO,SPRITE_SALTANDO,SPRITE_ATACANDO_QUIETO,SPRITE_ATACANDO_SALTANDO,SPRITE_ATACANDO_ANDANDO)
    numImagenPostura: int
        fila que ocupan las imágenes que representan una postura
    coordenadasHoja: List[Rect]
        lista con coordenadas de imágenes
    retardoMovimiento: float
        retardo en el movimiento
    sonido_salto: Sound
        sonido que representa el salto
    velocidadCarrera: float
        velocidad a la hora de desplazarse
    velocidadSalto: float
        velocidad a la hora de saltar
    retardoAnimación: tupla
        retardo en la animación


    Métodos
    -------
    actualizarPostura()
        Carga la imagen correspondiente en función de a dónde esté mirando el Personaje
    mover(movimientos)
        Cambia el movimiento
    update(grupoPlataformas, tiempo)
        Cambia la postura del Personaje en funcion de sus movimientos y también lo deja mirando a donde corresponda
        """

    def __init__(
            self,
            archivoImagen,
            archivoCoordenadas,
            numImagenes,
            velocidadCarrera,
            velocidadSalto,
            retardoAnimacion,
    ):

        """Establece la creación de un Personaje.

        Parámetros
        ----------
        archivoImagen : str
            ruta de la imagen del Personaje.
        archivoCoordenadas : str
            ruta del archivo que contiene las coordenadas de cada imagen
        numImagenes : List[int]
            lista con numero de imagenes por fila del spritesheet
        velocidadCarrera : int
            velocidad a la hora de desplazarse
        velocidadSalto : int
            velocidad a la hora de saltar
        retardoAnimacion : int
            retardo en la animación
        """

        MiSprite.__init__(self)

        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)
        self.hoja = self.hoja.convert_alpha()

        self.movimientos = [QUIETO]
        self.mirando = DERECHA
        self.vuela = False

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1
        self.numImagenPostura = 0
        cont = 0
        self.coordenadasHoja = []
        for linea in range(0, len(numImagenes)):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for _ in range(0, numImagenes[linea]):
                tmp.append(
                    pygame.Rect(
                        (int(datos[cont]), int(datos[cont + 1])),
                        (int(datos[cont + 2]), int(datos[cont + 3])),
                    )
                )
                cont += 4

        self.retardoMovimiento = 0
        self.numPostura = QUIETO
        self.sonido_salto = GestorRecursos.load_sound("salto.mp3", "Recursos/Sonidos/")

        self.rect = pygame.Rect(
            100,
            100,
            self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],
            self.coordenadasHoja[self.numPostura][self.numImagenPostura][3],
        )

        self.velocidadCarrera = velocidadCarrera
        self.velocidadSalto = velocidadSalto
        self.retardoAnimacion = retardoAnimacion

        self.actualizarPostura()

    def actualizarPostura(self):
        """Carga la imagen correspondiente en función de a dónde esté mirando el Personaje

        Parámetros
        ----------
        """

        self.retardoMovimiento -= 1

        if self.retardoMovimiento < 0:
            self.retardoMovimiento = RETARDO_ANIMACION_JUGADOR
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1
            self.image = self.hoja.subsurface(
                self.coordenadasHoja[self.numPostura][self.numImagenPostura]
            )

            # Si el personaje es un Pájaro o un Cangrejo, invertimos su imagen.
            if isinstance(self, Pajaro) or isinstance(self, Cangrejo) and self.numPostura == SPRITE_ANDANDO:
                if self.mirando == DERECHA:
                    self.mirando = IZQUIERDA
                else:
                    self.mirando = DERECHA

            # Cargamos la imagen correspondiente
            if self.mirando == DERECHA:
                if len(self.coordenadasHoja) == 0:
                    self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])
                else:
                    self.image = self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura]
                    )
            # Si mira a la derecha, invertimos la imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(
                    self.hoja.subsurface(
                        self.coordenadasHoja[self.numPostura][self.numImagenPostura]
                    ),
                    1,
                    0,
                )

    def mover(self, movimientos):
        """Cambia el movimiento

        Parámetros
        ----------
         movimientos : List[int]
            movimiento a establecer.
        """

        self.movimientos = movimientos

    def update(self, grupoPlataformas, tiempo):
        """Cambia el movimiento

        Parámetros
        ----------
         grupoPlataformas : Group
            grupo de plataformas para comprobar colisiones
         tiempo : int
            milisegundos para la sincronización de cada frame.
        """

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        if (
                self.numPostura == SPRITE_SALTANDO
                or self.numPostura == SPRITE_ATACANDO_SALTANDO
        ):
            self.numPostura = (
                SPRITE_ATACANDO_SALTANDO
                if DISPARA in self.movimientos
                else SPRITE_SALTANDO
            )

        # En función del movimiento que adopte, se le pone mirando a un lado u a otro.
        if (IZQUIERDA in self.movimientos) or (DERECHA in self.movimientos):
            if IZQUIERDA in self.movimientos:
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
            if (
                    self.numPostura != SPRITE_SALTANDO
                    and self.numPostura != SPRITE_ATACANDO_SALTANDO
            ) and not self.vuela:
                # La postura actual sera estar caminando
                if DISPARA in self.movimientos:
                    self.numPostura = SPRITE_ATACANDO_ANDANDO
                else:
                    self.numPostura = SPRITE_ANDANDO
                # Ademas, si no estamos encima de ninguna plataforma, caeremos
                if pygame.sprite.spritecollideany(self, grupoPlataformas) is None:
                    if DISPARA in self.movimientos:
                        self.numPostura = SPRITE_ATACANDO_SALTANDO
                    else:
                        self.numPostura = SPRITE_SALTANDO

        # Si queremos saltar
        if ARRIBA in self.movimientos and (
                self.numPostura != SPRITE_SALTANDO
                and self.numPostura != SPRITE_ATACANDO_SALTANDO
        ):
            # La postura actual será estar saltando
            if DISPARA in self.movimientos:
                self.numPostura = SPRITE_ATACANDO_SALTANDO
            else:
                self.numPostura = SPRITE_SALTANDO
            # Le imprimimos una velocidad en el eje y
            velocidady = -self.velocidadSalto

        # Si no se ha pulsado ninguna tecla
        if QUIETO in self.movimientos:
            # Si no estamos saltando, la postura actual será estar quieto
            if (
                    not self.numPostura == SPRITE_SALTANDO
                    and not self.numPostura == SPRITE_ATACANDO_SALTANDO
            ):
                if DISPARA in self.movimientos:
                    self.numPostura = SPRITE_ATACANDO_QUIETO
                else:
                    self.numPostura = SPRITE_QUIETO

            velocidadx = 0

        # Además, si estamos en el aire
        if (
                self.numPostura != SPRITE_QUIETO
                and self.numPostura != SPRITE_ATACANDO_QUIETO
        ):
            # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
            #  Para ello, miramos si hay colisión con alguna plataforma del grupo
            plataforma = pygame.sprite.spritecollide(self, grupoPlataformas, False)
            if len(plataforma) > 0:
                for i in range(len(plataforma)):
                    #  Además, esa colisión solo nos interesa cuando estamos cayendo
                    #  y solo es efectiva cuando caemos encima, no de lado, es decir,
                    #  cuando nuestra posición inferior está por encima de la parte de abajo de la plataforma
                    if (
                            (plataforma[i] != None)
                            and (velocidady > 0)
                            and (plataforma[i].rect.top > self.rect.top)
                    ):
                        # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
                        #  para poder detectar cuando se cae de ella
                        self.establecerPosicion(
                            (
                                self.posicion[0],
                                plataforma[i].posicion[1]
                                - plataforma[i].rect.height
                                + 1,
                            )
                        )
                        # Lo ponemos como quieto
                        if DISPARA in self.movimientos:
                            self.numPostura = SPRITE_ATACANDO_QUIETO
                        else:
                            self.numPostura = SPRITE_QUIETO
                        # Y estará quieto en el eje y
                        velocidady = 0

                    elif (
                            self.rect.bottom - 1 > plataforma[i].rect.top
                            and self.rect.bottom
                            < plataforma[i].rect.top + plataforma[i].rect.height
                    ):
                        posicion = (
                            self.posicion[0] - 1
                            if (plataforma[i].rect.left > self.rect.left)
                            else self.posicion[0] + 1
                        )
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
    """
        Clase que representa al jugador que controla el usuario

        ..

        Atributos
        ----------
        vida: int
            numero de vidas del protagonista
        inmune: bool
            atributo acerca de si es inmune o no al daño enemigo
        money: int
            número de monedas que tiene
        ultimoGolpe: int
            imagen que representa al Personaje
        ticks: int
            imagen que representa al Personaje
        recarga: int
            balas por cargador
        tiempoRecarga: int
            tiempo que tarda en recargar
        cont_powerup: int
            numero de powerups que posee
        tipo_powerup: int
            tipo de powerup que posee
        sonido_disparo: Sound
            sonido de disparar
        sonido_recarga: Sound
            sonido de recargar
        sonido_dano: Sound
            sonido de recibir daño
        sonido_moneda: Sound
            sonido de coger una moneda

        Métodos
        -------
        reduce_recarga()
            Reduce la recarga en 1
        reduce_powerup()
            Reduce el numro de powerups en 1
        acaba_powerup()
            vuelve a la normalidad los atributos afectados por los powerups
        start_powerup(tipo)
            cambia el atributo que proceda afectado por los powerups
        has_powerup()
            aporta información sobre si tiene o no powerups
        cambia_velocidad(vel)
            establece la velocidad de carrera
        reset_velocidad()
            vuelve la velocidad de carrera del jugador a la original
        cambia_salto(vel)
            establece la velocidad de salto
        reset_salto()
            vuelve la velocidad de salto del jugador a la original
        cambia_tiempo_recarga(value)
            establece el numero de recargas
        reset_tiempo_recarga()
            vuelve el tiempo de recarga al original
        cura()
            aumenta 1 vida en caso de que falte alguna
        mover(teclasPulsadas, arriba, abajo, izquierda, derecha, dispara, bala)
            gestiona el movimiento el jugador
        dañarJugador()
            gestiona la acción de sufrir daño
        cogerMoneda()
            gestiona la acción de coger una moneda
        getMoney()
            devuelve el numero de monedas
        setMoney(saldo)
            establece el numero de monedas

        """

    def __init__(self):

        Personaje.__init__(
            self,
            "Nera/NeraFull.png",
            "Nera/coords.txt",
            [4, 8, 4, 4, 8, 4],
            VELOCIDAD_JUGADOR,
            VELOCIDAD_SALTO_JUGADOR,
            RETARDO_ANIMACION_JUGADOR,
        )
        self.vida = 3
        self.inmune = False
        self.money = 0
        self.ultimoGolpe = pygame.time.get_ticks()
        self.ticks = 0
        self.recarga = 1
        self.tiempoRecarga = RECARGA_JUGADOR
        self.cont_powerup = 0
        self.tipo_powerup = ""
        self.sonido_disparo = GestorRecursos.load_sound(
            "disparo.mp3", "Recursos/Sonidos/"
        )
        self.sonido_recarga = GestorRecursos.load_sound(
            "recarga.mp3", "Recursos/Sonidos/"
        )
        self.sonido_dano = GestorRecursos.load_sound("dano.mp3", "Recursos/Sonidos/")

        self.sonido_moneda = GestorRecursos.load_sound(
            "moneda.mp3", "Recursos/Sonidos/"
        )

    def reduce_recarga(self):
        """Reduce la recarga en 1

        Parámetros
        ----------
        """
        self.recarga -= 1

    def reduce_powerup(self):
        """Reduce el numero de powerups en 1

        Parámetros
        ----------
        """
        if self.cont_powerup > 0:
            self.cont_powerup -= 1
            if self.cont_powerup == 0:
                self.acaba_powerup()

    def acaba_powerup(self):
        """Vuelve a la normalidad los atributos afectados por los powerups

        Parámetros
        ----------
        """
        if self.tipo_powerup == "velocidad":
            self.reset_velocidad()
        if self.tipo_powerup == "salto":
            self.reset_salto()
        if self.tipo_powerup == "recarga":
            self.reset_tiempo_recarga()

    def start_powerup(self, tipo):
        """Cambia el atributo que proceda afectado por los powerups
        Parámetros
        ----------
        tipo : str
            tipo del powerup
        """
        self.tipo_powerup = tipo
        if tipo == "velocidad":
            self.cambia_velocidad(0.55)
            self.cont_powerup = 100
        if tipo == "salto":
            self.cambia_salto(0.65)
        if tipo == "recarga":
            self.cambia_tiempo_recarga(8)
        self.cont_powerup = DURACION_POWERUP

    def has_powerup(self):
        """Aporta información sobre si tiene o no powerups
        Parámetros
        ----------
        """
        if self.cont_powerup > 0:
            return True

    def cambia_velocidad(self, vel):
        """Establece la velocidad de carrera
        Parámetros
        ----------
        vel : str
            velocidad a establecer
        """
        self.velocidadCarrera = vel

    def reset_velocidad(self):
        """Vuelve la velocidad de carrera del jugador a la original
        Parámetros
        ---------
        """
        self.velocidadCarrera = VELOCIDAD_JUGADOR

    def cambia_salto(self, vel):
        """Establece la velocidad de salto
        Parámetros
        ----------
        vel : str
            velocidad a establecer
        """
        self.velocidadSalto = vel

    def reset_salto(self):
        """Vuelve la velocidad de salto del jugador a la original
        Parámetros
        ---------
        """
        self.velocidadSalto = VELOCIDAD_SALTO_JUGADOR

    def cambia_tiempo_recarga(self, value):
        """establece el numero de recargas
        Parámetros
        ----------
        value : int
            numero de recargas a establecer
        """
        self.tiempoRecarga = value

    def reset_tiempo_recarga(self):
        """Vuelve el tiempo de recarga al original
        Parámetros
        ---------
        """
        self.tiempoRecarga = RECARGA_JUGADOR

    def cura(self):
        """Aumenta 1 vida en caso de que falte alguna
        Parámetros
        ---------
        """
        if self.vida < 3:
            self.vida += 1

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, dispara, bala):
        """Gestiona el movimiento el jugador
        Parámetros
        ----------
        teclasPulsadas : List[int]
            teclas pulsads por el jugador
        arriba : int
            posicion
        abajo : int
            posicion
        izquierda : int
            posicion
        derecha : int
            posicion
        dispara : int
            posicion
        bala : Sprite
            bala
        """

        movimientos = []
        if teclasPulsadas[dispara]:
            self.sonido_disparo.play()
            movimientos.append(DISPARA)
            if self.recarga <= 0:
                self.recarga = self.tiempoRecarga
                self.sonido_recarga.play()
                bala.vive(self.rect.left, self.rect.bottom, self.mirando)
        if teclasPulsadas[arriba] and (
                self.numPostura != SPRITE_SALTANDO
                and self.numPostura != SPRITE_ATACANDO_SALTANDO
        ):
            self.sonido_salto.play()
            movimientos.append(ARRIBA)
        if teclasPulsadas[derecha]:
            movimientos.append(DERECHA)
        if teclasPulsadas[izquierda]:
            movimientos.append(IZQUIERDA)

        if len(movimientos) == 0 or (len(movimientos) == 1 and DISPARA in movimientos):
            movimientos.append(QUIETO)
        Personaje.mover(self, movimientos)

    def dañarJugador(self):
        """Gestiona la acción de sufrir daño
        Parámetros
        ----------
        """
        if not self.inmune:
            self.sonido_dano.play()
            self.vida -= 1
            self.inmune = True
            self.ultimoGolpe = pygame.time.get_ticks()

    def cogerMoneda(self):
        """Gestiona la acción de coger una moneda
        Parámetros
        ----------
        """
        self.sonido_moneda.play()
        self.money += 1

    def getMoney(self):
        """Devuelve el numero de monedas
        Parámetros
        ----------
        """
        return self.money

    def setMoney(self, saldo):
        """Establece el numero de monedas
        Parámetros
        ----------
        """
        self.money = saldo


class Bala(MiSprite):
    """
    Clase que representa cualquier Personaje presente en el juego

    ..

    Atributos
    ----------
    hoja: Surface
        imagen que representa al Personaje
    mirando: int
        dirección a la que está mirando
    numPostura: int
        postura que toma la Bala
    numImagenPostura: int
        fila que ocupan las imágenes que representan una postura
    coordenadasHoja: List[Rect]
        lista con coordenadas de imágenes
    direccion: int
        direccion de la bala
    velocidad: float
        velocidad de la bala
    alive: bool
        indica si la bala existe o no
    image: Surface
        imagen de la bala
    Métodos
    -------
    muere()
        JORGE
    vive(movimientos)
        JORGE
    miraSiHaySignosVitales(movimientos)
        JORGE
    update(tiempo)
        JORGE
        """
    def __init__(
            self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, mirando
    ):
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
                pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3])),
                )
            )
            cont += 4

        if mirando == 1:
            self.direccion = -1
            self.velocidad = (-velocidad, 0)
        else:
            self.direccion = 1
            self.velocidad = (velocidad, 0)

        self.alive = False

        self.rect = pygame.Rect(
            100,
            100,
            self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],
            self.coordenadasHoja[self.numPostura][self.numImagenPostura][3],
        )

        self.image = self.hoja.subsurface(self.coordenadasHoja[0][0])

    def muere(self):
        self.alive = False

    def vive(self, left, bottom, mirando):
        self.alive = True
        if mirando == 1:
            self.posicion = (left, bottom - 60)
            self.direccion = -1
            self.velocidad = (-abs(self.velocidad[0]), 0)
        else:
            self.posicion = (left + 40, bottom - 60)
            self.direccion = 1
            self.velocidad = (abs(self.velocidad[0]), 0)
        self.establecerPosicion(self.posicion)

    def miraSiHaySignosVitales(self):
        return self.alive

    def update(self, tiempo):
        MiSprite.update(self, tiempo)

        # checkea off screen
        # if not self.game.screen.get_rect().contains(self.rect):
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:
            self.muere()


class Enemigo(Personaje):
    """
           Clase que representa a los enemigos que atacan al Jugador

           ..

           Atributos
           ----------
           Todos los heredados de Personaje

           Métodos
           -------

           Todos los heredados de Personaje
            mover_cpu(jugador)
                se encarga de implementar la estrategia de IA de los enemigos
           """

    def __init__(
            self,
            archivoImagen,
            archivoCoordenadas,
            numImagenes,
            velocidad,
            velocidadSalto,
            retardoAnimacion,
    ):
        """Establece la creación del Enemigo.

                Parámetros
                ----------
                archivoImagen : str
                    ruta de la imagen del Enemigo.
                archivoCoordenadas : str
                    ruta del archivo que contiene las coordenadas de cada imagen
                numImagenes : List[int]
                    lista con numero de imagenes por fila del spritesheet
                velocidadCarrera : int
                    velocidad a la hora de desplazarse
                velocidadSalto : int
                    velocidad a la hora de saltar
                retardoAnimacion : int
                    retardo en la animación
                """

        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(
            self,
            archivoImagen,
            archivoCoordenadas,
            numImagenes,
            velocidad,
            velocidadSalto,
            retardoAnimacion,
        )

        self.vida = 1

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        """
        # Por defecto un enemigo no hace nada
        return


class Espectro(Enemigo):
    """
        Clase que representa al Espectro en el juego.

        ...

        Atributos
        ----------
        vuela: bool
            indica si vuela o no
        dano: Sound
            sonido que produce al recibir daño
        muerte: Sound
            sonido que produce al morir
        Métodos
        -------
        mover_cpu(jugador)
            se encarga de implementar la estrategia de IA de los enemigos
       """

    def __init__(self):
        """Establece la creación del Espectro.

        Parámetros
        ----------
        """
        Enemigo.__init__(
            self,
            "espectro_4.png",
            "coord3.txt",
            [1, 1, 1, 1],
            VELOCIDAD_ESPECTRO,
            0,
            RETARDO_ANIMACION_ESPECTRO,
        )
        self.vuela = True
        self.dano = GestorRecursos.load_sound("fantasma.mp3", "Recursos/Sonidos/")
        self.muerte = GestorRecursos.load_sound("muerte.mp3", "Recursos/Sonidos/")

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        jugador : Jugador
            jugador principal
        """

        # Movemos solo a los enemigos que estén en la pantalla
        if (
                self.rect.left > 0
                and self.rect.right < ANCHO_PANTALLA
                and self.rect.bottom > 0
                and self.rect.top < ALTO_PANTALLA
        ):
            # Si estamos por encima de él, el espectro se queda quieto porque el Jugador no entra en su campo de visión
            if self.posicion[1] - jugador.posicion[1] > 80:
                Personaje.mover(self, [QUIETO])
            else:
                # Si no miramos para él se acercará por nuestras espaldas.
                if (
                        jugador.posicion[0] < self.posicion[0]
                        and jugador.mirando == IZQUIERDA
                ):
                    Personaje.mover(self, [IZQUIERDA])
                # Si estamos en suelo y miramos para él se queda quieto
                elif (
                        jugador.posicion[0] < self.posicion[0]
                        and jugador.mirando == DERECHA
                ):
                    Personaje.mover(self, [QUIETO])
                # Si no miramos para él se acercará por nuestras espaldas.
                elif (
                        jugador.posicion[0] > self.posicion[0]
                        and jugador.mirando == DERECHA
                ):
                    Personaje.mover(self, [DERECHA])
                # Si estamos en suelo y miramos para él se queda quieto
                elif (
                        jugador.posicion[0] > self.posicion[0]
                        and jugador.mirando == IZQUIERDA
                ):
                    Personaje.mover(self, [QUIETO])

        # Si este personaje no está en pantalla, no hará nada
        else:
            Personaje.mover(self, [QUIETO])


class Demonio(Enemigo):
    """
        Clase que representa al Demonio en el juego.

        ...

        Atributos
        ----------
        vuela: bool
            indica si vuela o no
        vida: int
            indica el número de vidas que tiene
        dano: Sound
            sonido que produce al recibir daño
        muerte: Sound
            sonido que produce al morir
        Métodos
        -------
        mover_cpu(jugador)
            se encarga de implementar la estrategia de IA de los enemigos
        """
    def __init__(self):
        """Establece la creación del Demonio.

        Parámetros
        ----------
        """
        Enemigo.__init__(
            self,
            "Demonio/demon__spritesheet2.png",
            "coordDiablo.txt",
            [6, 12, 15, 5, 16],
            VELOCIDAD_DEMONIO,
            0,
            RETARDO_ANIMACION_DEMONIO,
        )
        self.vuela = False
        self.vida = 3
        self.dano = GestorRecursos.load_sound("demonio.mp3", "Recursos/Sonidos/")
        self.muerte = GestorRecursos.load_sound("muerte_demonio.mp3", "Recursos/Sonidos/")

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        jugador : Jugador
            jugador principal
        """

        # Movemos solo a los enemigos que estén en la pantalla
        if (
                self.rect.left > 0
                and self.rect.right < ANCHO_PANTALLA
                and self.rect.bottom > 0
                and self.rect.top < ALTO_PANTALLA
        ):
            # Si no estamos en su campo de visión vertical, se queda quieto
            if abs(jugador.posicion[0] - self.posicion[0]) < 50:
                Personaje.mover(self, [QUIETO])
                self.numPostura = SPRITE_ATACANDO_SALTANDO
            # Si estamos en su campo de visión vertical, viene a por nosotros
            elif jugador.posicion[0] < self.posicion[0]:
                self.numPostura = SPRITE_ANDANDO
                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:
                self.numPostura = SPRITE_ANDANDO
                Personaje.mover(self, [DERECHA])
            else:
                Personaje.mover(self, [QUIETO])


class Cangrejo(Enemigo):
    """
    Clase que representa al Cangrejo en el juego

    ...

    Atributos
    ----------
    vuela: bool
        indica si vuela o no
    dano: Sound
        sonido que produce al recibir daño

    Métodos
    -------
    mover_cpu(jugador)
        se encarga de implementar la estrategia de IA de los enemigos
    """

    def __init__(self):
        Enemigo.__init__(
            self,
            "Cangrejo/cangrejo.png",
            "coordCangrejo.txt",
            [4, 6, 1],
            VELOCIDAD_CANGREJO,
            0,
            RETARDO_ANIMACION_CANGREJO,
        )
        self.vuela = False
        self.dano = GestorRecursos.load_sound("fantasma.mp3", "Recursos/Sonidos/")

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        jugador : Jugador
            jugador principal
        """
        # Movemos solo a los enemigos que estén en la pantalla
        if (
                self.rect.left > 0
                and self.rect.right < ANCHO_PANTALLA
                and self.rect.bottom > 0
                and self.rect.top < ALTO_PANTALLA
        ):
            if abs(jugador.posicion[1] - self.posicion[1]) > 20 and abs(jugador.posicion[0] - self.posicion[0]) < 10:
                Personaje.mover(self, [QUIETO])
            elif jugador.posicion[0] < self.posicion[0]:
                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:
                Personaje.mover(self, [DERECHA])


class Esqueleto(Enemigo):
    def __init__(self):
        """Establece la creación del Esqueleto.

        Parámetros
        ----------
        """
        Enemigo.__init__(
            self,
            "Esqueleto/esqueleto.png",
            "coordEsqueleto.txt",
            [8, 6, 1],
            VELOCIDAD_ESQUELETO,
            0,
            RETARDO_ANIMACION_ESQUELETO,
        )
        self.vuela = False
        self.dano = GestorRecursos.load_sound("esqueleto.mp3", "Recursos/Sonidos/")

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        jugador : Jugador
            jugador principal
        """
        # Movemos solo a los enemigos que estén en la pantalla
        if (
                self.rect.left > 0
                and self.rect.right < ANCHO_PANTALLA
                and self.rect.bottom > 0
                and self.rect.top < ALTO_PANTALLA
        ):
            # Si no estamos en su campo de visión vertical, se queda quieto
            if abs(jugador.posicion[1] - self.posicion[1]) > 20 and abs(jugador.posicion[0] - self.posicion[0]) < 10:
                self.numPostura = SPRITE_QUIETO
                Personaje.mover(self, [QUIETO])
            # Si estamos en su campo de visión vertical, nor persigue
            elif jugador.posicion[0] < self.posicion[0]:
                Personaje.mover(self, [IZQUIERDA])
            elif jugador.posicion[0] > self.posicion[0]:
                Personaje.mover(self, [DERECHA])
            else:
                self.numPostura = SPRITE_QUIETO
                Personaje.mover(self, [QUIETO])


class Pajaro(Enemigo):
    """
    Clase que representa al Pájaro en el juego

    ...

    Atributos
    ----------
    count: int
        contador para su movimiento
    vuela: bool
        indica si vuela o no
    dano: Sound
        sonido que produce al recibir daño
    Métodos
    -------
    mover_cpu(jugador)
        se encarga de implementar la estrategia de IA de los enemigos
    """
    def __init__(self):
        Enemigo.__init__(
            self,
            "Bird Spritesheet.png",
            "coordBird.txt",
            [2, 3, 8, 3],
            VELOCIDAD_PAJARO,
            0,
            RETARDO_ANIMACION_PAJARO,
        )
        self.count = 0
        self.vuela = True
        self.dano = GestorRecursos.load_sound("pajaro.mp3", "Recursos/Sonidos/")

    def mover_cpu(self, jugador):
        """Se encarga de implementar la estrategia de IA de los enemigos

        Parámetros
        ----------
        jugador : Jugador
            jugador principal
        """
        # Movemos solo a los enemigos que estén en la pantalla
        if (
                self.rect.left > 0
                and self.rect.right < ANCHO_PANTALLA
                and self.rect.bottom > 0
                and self.rect.top < ALTO_PANTALLA
        ):
            # Este se mueve de izquierda a derecha en bucle
            if self.count < 260:
                Personaje.mover(self, [DERECHA])
            elif self.rect.left == 70:
                self.count = 0
            else:
                Personaje.mover(self, [IZQUIERDA])
            self.count += 1
