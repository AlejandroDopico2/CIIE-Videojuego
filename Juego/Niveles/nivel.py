import json

import pygame
from Dialogos.dialogos import *
from escena import *
from gestorRecursos import *
from Mercader.mercader import *
from Mercader.señalMerc import *
from Niveles.menuPausa import MenuPausa
from Niveles.menuTienda import MenuTienda
from Personajes.moneda import *
from Personajes.personajes import *
from Personajes.playerState import *
from Personajes.powerups import *
from Personajes.reliquia import *
from Plataformas.plataformas import *
from pygame.locals import *

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 250
VELOCIDAD_BALA = 0.5


class Nivel(PygameScene):
    def __init__(self, director, cfg):
        PygameScene.__init__(self, director)

        with open(cfg, "r") as f:
            self.cfg = json.load(f)

        self.acabarPorFinal = True
        self.bossFinal = False
        self.reliquia = None

        self.director = director
        self.comprado = False
        self.set_music()
        self.decorado = Decorado(self.cfg["decoration"])
        self.fondo = Fondo(self.cfg["background"])
        self.vida = Vida()
        self.moneda = Moneda()
        self.scrollx = 0

        self.grupoSprites = pygame.sprite.Group()
        self.grupoJugadores = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoMisBalas = pygame.sprite.Group()
        self.grupoMisBalasActivas = pygame.sprite.Group()
        self.grupoBalasEnemigas = pygame.sprite.Group()
        self.grupoBalasEnemigasActivas = pygame.sprite.Group()

        self.grupoPowerups = pygame.sprite.Group()
        self.grupoPowerupsVelocidad = pygame.sprite.Group()
        self.grupoPowerupsVida = pygame.sprite.Group()
        self.grupoPowerupsSalto = pygame.sprite.Group()
        self.grupoPowerupsRecarga = pygame.sprite.Group()

        self.grupoMonedas = pygame.sprite.Group()

        # Se crea personaje
        self.jugador = Jugador()
        self.jugador.setMoney(self.director.playerState.getMoney())
        self.jugador.establecerPosicion((self.cfg["player"][0], self.cfg["player"][1]))
        self.grupoSprites.add(self.jugador)
        self.grupoJugadores.add(self.jugador)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador)

        # Se crean las balas del jugador y de los enemigos
        # se crean todas al inicio del nivel y luego se reutilizan durante toda la partida
        for i in range(0, 20):
            bala = Bala(
                "bullet.png", "coordBala.txt", [1], VELOCIDAD_BALA, self.jugador.mirando
            )
            self.grupoMisBalas.add(bala)
            bola = Bala("fireball1.png", "coordBolaFuego.txt", [1], VELOCIDAD_BALA, -1)
            self.grupoBalasEnemigas.add(bola)

        self.grupoPlataformas = pygame.sprite.Group()
        self.setPlatforms()
        self.setEnemies()

        # IMPORTANTE, DIALOGOS SIEMPRE EN ORDEN DE APARICION EN EL JSON
        self.listaDialog = []
        self.setDialogos()

        self.mercader = mercader()
        self.setMercader()
        self.setCoins()
        self.setPowerups()
        self.señalMerc = señalMerc("Mercader/señalMerc.png", (500, 30))
        self.game_over = GestorRecursos.load_sound("game_over.mp3", "Recursos/Sonidos/")

    def set_music(self):
        pygame.mixer.music.load(self.cfg["music"])
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)

    def setPlatforms(self):
        for pt in self.cfg["platforms"]:
            plataforma = Plataforma(
                pygame.Rect(pt["x"], pt["y"], pt["width"], pt["height"])
            )
            self.grupoPlataformas.add(plataforma)
            self.grupoSprites.add(plataforma)

    # NOTA: deben ponerse los dialogos en orden en el json
    def setDialogos(self):
        i = 0
        for d in self.cfg["dialogs"]:
            dialogo = Dialogos(
                d["img"], (d["x"], d["y"]), d["scale"], d["despl"], d["pos"], False
            )
            # self.grupoDialogos.add(dialogo)
            self.listaDialog.append(dialogo)
            i += 1
            # self.grupoSprites.add(dialogo)

    # Se cargan los enemigos desde el archivo json
    def setEnemies(self):
        for e in self.cfg["enemies"]:
            if e["name"] == "esqueleto":
                enemy = Esqueleto()
                enemy.establecerPosicion((e["pos"][0], e["pos"][1]))
            if e["name"] == "demonio":
                self.acabarPorFinal = False
                enemy = Demonio()
                self.bossFinal = enemy
                enemy.establecerPosicion((e["pos"][0], e["pos"][1]))
            if e["name"] == "espectro":
                enemy = Espectro()
                enemy.establecerPosicion((e["pos"][0], e["pos"][1]))
            if e["name"] == "cangrejo":
                enemy = Cangrejo()
                enemy.establecerPosicion((e["pos"][0], e["pos"][1]))
            if e["name"] == "pajaro":
                enemy = Pajaro()
                enemy.establecerPosicion((e["pos"][0], e["pos"][1]))

            self.grupoEnemigos.add(enemy)
            self.grupoSpritesDinamicos.add(enemy)
            self.grupoSprites.add(enemy)

    def setMercader(self):
        for m in self.cfg["merchant"]:
            self.mercader.establecerPosicion((m["x"], m["y"]))
            self.grupoSprites.add(self.mercader)

    def setCoins(self):
        for e in self.cfg["coins"]:
            coin = Moneda()
            coin.establecerPosicion((e["pos"][0], e["pos"][1]))

            self.grupoMonedas.add(coin)
            self.grupoSprites.add(coin)

    # Se crean los powerups indicados en el json
    def setPowerups(self):
        for e in self.cfg["powerups"]:
            if e["type"] == "velocidad":
                powerup = Powerup_velocidad()
                self.grupoPowerupsVelocidad.add(powerup)
                self.grupoPowerups.add(powerup)
            if e["type"] == "vida":
                powerup = Powerup_vida()
                self.grupoPowerupsVida.add(powerup)
            if e["type"] == "salto":
                powerup = Powerup_salto()
                self.grupoPowerupsSalto.add(powerup)
                self.grupoPowerups.add(powerup)
            if e["type"] == "recarga":
                powerup = Powerup_recarga()
                self.grupoPowerupsRecarga.add(powerup)
                self.grupoPowerups.add(powerup)

            powerup.establecerPosicion((e["pos"][0], e["pos"][1]))
            self.grupoSprites.add(powerup)

    def actualizarScrollOrd(self, jugador):
        if jugador.rect.left < MINIMO_X_JUGADOR:
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

            if self.scrollx <= 0:
                self.scrollx = 0
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
                return False

            else:
                self.scrollx = self.scrollx - desplazamiento
                return True
        if jugador.rect.right > MAXIMO_X_JUGADOR:
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR
            if self.decorado.rectSubImagen.right >= self.decorado.rect.right:
                self.acabarNivel()
                return True

            elif jugador.rect.left - MINIMO_X_JUGADOR < desplazamiento:
                jugador.establecerPosicion(
                    (jugador.posicion[0] - desplazamiento, jugador.posicion[1])
                )
                return False
            else:
                self.scrollx = self.scrollx + desplazamiento
                return True

        return False

    def acabarNivel(self):
        # Solo en caso de niveles 1 y 2, que el final de nivel es al limite.
        if self.acabarPorFinal:
            self.director.exitScene(playerState(self.jugador.getMoney()))
        else:
            # En caso de que se derrote al demonio, el boss final, se crea reliquia
            if not self.grupoEnemigos.has(self.bossFinal):
                if self.reliquia is None:
                    self.crearReliquia()
                else:
                    # Cuando toca la reliquia, se acaba el nivel
                    if pygame.sprite.collide_rect(self.jugador, self.reliquia):
                        self.director.exitScene(playerState(self.jugador.getMoney()))

    def crearReliquia(self):
        self.reliquia = Reliquia()
        self.reliquia.establecerPosicion((4709, 423))
        self.grupoSprites.add(self.reliquia)

    def actualizarScroll(self, jugador):
        cambioScroll = self.actualizarScrollOrd(jugador)
        added = False
        if cambioScroll:
            if not self.grupoSprites.has(self.jugador):
                added = True
                self.grupoSprites.add(self.jugador)
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla((self.scrollx, 0))

            if added:
                self.grupoSprites.remove(self.jugador)

            self.decorado.update(self.scrollx)
            self.fondo.update(self.scrollx)

    def update(self, tiempo):
        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        if not self.director.pause:
            # Si hay alguna bala inicializada por un personaje, esta se uno al grupo de sprites Balas Activas
            for bala in iter(self.grupoMisBalas):
                if bala.miraSiHaySignosVitales():
                    self.grupoMisBalasActivas.add(bala)
                else:
                    self.grupoMisBalasActivas.remove(bala)
            # Si la bala colisiona con un personaje o plataforma, se vuelve a marcar como "muerta" (no inicializada)
            for bala in iter(self.grupoMisBalasActivas):
                bala.update(tiempo)
                if pygame.sprite.spritecollideany(bala, self.grupoEnemigos):
                    bala.muere()
                if pygame.sprite.spritecollideany(bala, self.grupoPlataformas):
                    bala.muere()

            for bala in iter(self.grupoBalasEnemigas):
                if bala.miraSiHaySignosVitales():
                    self.grupoBalasEnemigasActivas.add(bala)
                else:
                    self.grupoBalasEnemigasActivas.remove(bala)

            for bala in iter(self.grupoBalasEnemigasActivas):
                bala.update(tiempo)
                if pygame.sprite.spritecollideany(bala, self.grupoJugadores):
                    bala.muere()
                if pygame.sprite.spritecollideany(bala, self.grupoPlataformas):
                    bala.muere()

            # Tras recibir daño, el jugador tiene unos instantes de inmunidad
            diference = pygame.time.get_ticks() - self.jugador.ultimoGolpe
            if self.jugador.inmune and diference > 3000:
                self.jugador.inmune = False
                self.grupoSprites.add(self.jugador)
            elif self.jugador.inmune:
                if diference % 2 == 0:
                    self.grupoSprites.remove(self.jugador)
                else:
                    self.grupoSprites.add(self.jugador)

            # Una de las balas que no esté en pantalla, se prepara por si el enemigo decide disparar
            bola_lista = 0
            for bala in iter(self.grupoBalasEnemigas):
                if not (bala in self.grupoBalasEnemigasActivas):
                    bola_lista = bala
                    break
            if bola_lista == 0:
                bola_lista = self.grupoBalasEnemigas.sprites()[
                    len(self.grupoBalasEnemigas.sprites()) - 1
                ]

            # detectamos las colisiones de las balas disparadas por el jugador con los enemigos y si suceden el enemigo sufre daño
            for enemigo in iter(self.grupoEnemigos):
                if pygame.sprite.spritecollideany(enemigo, self.grupoMisBalasActivas):
                    enemigo.dano.play()
                    enemigo.vida -= 1
                    if enemigo.vida <= 0:
                        enemigo.muerte.play()
                        pygame.sprite.Sprite.kill(enemigo)
                    # enemigo.numPostura = SPRITE_ATACANDO_SALTANDO
                if enemigo == self.bossFinal:
                    enemigo.mover_cpu(self.jugador, bola_lista)
                else:
                    enemigo.mover_cpu(self.jugador)

            # detectamos colisiones de las balas de los enemigos con el jugador, si suceden el jugador recibe daño
            if pygame.sprite.spritecollideany(
                self.jugador, self.grupoBalasEnemigasActivas
            ):
                self.jugador.dañarJugador()
                if self.jugador.vida <= 0:
                    self.game_over.play()
                    self.director.exitScene()

            for coin in iter(self.grupoMonedas):
                coin.update(tiempo)

            if self.reliquia:
                self.reliquia.update(tiempo)

            self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

            if self.jugador.posicion[1] - self.jugador.rect.height > ALTO_PANTALLA:
                self.director.exitScene()

            monedas_tocadas = pygame.sprite.spritecollide(
                self.jugador, self.grupoMonedas, True
            )

            for moneda in monedas_tocadas:
                self.jugador.cogerMoneda()
                self.grupoSprites.remove(moneda)

            if self.jugador.has_powerup():
                self.jugador.reduce_powerup()

            # detecta si el jugador recoge un powerup
            powerups_recogidos = pygame.sprite.spritecollide(
                self.jugador, self.grupoPowerups, False
            )
            # si se recoge un powerup mientras ya había uno activo, el primero se acaba y comienza el que acaba de recogerse.
            for power in powerups_recogidos:
                if self.jugador.has_powerup():
                    self.jugador.acaba_powerup()

                if self.grupoPowerupsVelocidad.has(power):
                    self.jugador.start_powerup("velocidad")
                if self.grupoPowerupsSalto.has(power):
                    self.jugador.start_powerup("salto")
                if self.grupoPowerupsRecarga.has(power):
                    self.jugador.start_powerup("recarga")
                power.kill()

            # El powerup de vida no termina ningún otro powerup activado previamente, es solo curarse al momento de recogerlo
            powerupVidaRecogido = pygame.sprite.spritecollide(
                self.jugador, self.grupoPowerupsVida, False
            )
            for power in powerupVidaRecogido:
                self.jugador.cura()
                power.kill()

            # colisiones entre jugador y enemigos, el jugador sufre daño
            if pygame.sprite.spritecollideany(self.jugador, self.grupoEnemigos) != None:
                self.jugador.dañarJugador()

                if self.jugador.vida <= 0:
                    self.game_over.play()
                    self.director.exitScene()
            for i in range(len(self.listaDialog)):
                if (not self.grupoEnemigos.has(self.bossFinal)) and (
                    len(self.listaDialog) == 1
                ):
                    self.listaDialog[i].setActive(True)
                    self.listaDialog[i].updateDraw(
                        (self.jugador.rect.x + self.scrollx, self.jugador.rect.y)
                    )
                    self.grupoSprites.add(self.listaDialog[i])
                    break
                # caso del primer dialogo
                if (
                    (
                        self.listaDialog[i].getCoord()[0]
                        - self.listaDialog[i].getDespl()
                        < self.jugador.rect.x
                        < self.listaDialog[i].getCoord()[0]
                        + self.listaDialog[i].getDespl()
                    )
                    and (
                        self.listaDialog[i].getCoord()[1]
                        - self.listaDialog[i].getDespl()
                        < self.jugador.rect.y
                        < self.listaDialog[i].getCoord()[1]
                        + self.listaDialog[i].getDespl()
                    )
                    and (not self.listaDialog[i].getActive())
                    and i == 0
                ):
                    self.listaDialog[i].updateDraw(
                        (self.jugador.rect.x + self.scrollx, self.jugador.rect.y)
                    )
                    self.grupoSprites.add(self.listaDialog[i])
                elif i == 0:
                    self.grupoSprites.remove(self.listaDialog[i])
                    self.listaDialog[i].setActive(True)
                # caso dialogos mercader
                else:
                    if (
                        self.listaDialog[i].getCoord()[0]
                        - self.listaDialog[i].getDespl()
                        < self.jugador.rect.x + self.scrollx
                        < self.listaDialog[i].getCoord()[0]
                        + self.listaDialog[i].getDespl()
                        and i == 1
                    ):
                        self.grupoSprites.add(self.listaDialog[i])
                        self.listaDialog[i].setActive(True)
                    else:
                        self.listaDialog[i].setActive(False)
                    if self.comprado and i == 2:
                        self.listaDialog[i].setActive(True)
                        self.grupoSprites.remove(self.listaDialog[i - 1])
                        self.grupoSprites.add(self.listaDialog[i])

            self.mercader.update(tiempo)
            self.jugador.reduce_recarga()
            self.actualizarScroll(self.jugador)

    def draw(self, pantalla):
        self.fondo.draw(pantalla, self.scrollx)
        self.decorado.draw(pantalla)
        self.vida.draw(pantalla, self.jugador.vida)
        self.moneda.draw(pantalla, self.jugador.money)
        if (len(self.listaDialog) > 1) and (self.listaDialog[1].getActive()):
            self.señalMerc.draw(pantalla)
        self.grupoSprites.draw(pantalla)
        self.grupoMisBalasActivas.draw(pantalla)
        self.grupoBalasEnemigasActivas.draw(pantalla)

    def eventsLoop(self, lista_eventos):
        for evento in lista_eventos:
            if self.director.pause:
                nivel = MenuPausa(self.director)
                self.director.stackScene(nivel)
                # GestorRecursos.CargarMenuPausa(self)
            if (
                not self.director.pause
                and self.director.tienda
                and (self.listaDialog[1].getActive() or self.listaDialog[2].getActive())
            ):
                self.comprado = True
                tienda = MenuTienda(self.director, self.jugador)
                self.director.stackScene(tienda)
            if evento.type == pygame.QUIT:
                self.director.exitProgram()

        # Una de las balas que no esté en pantalla, se prepara por si el jugador pulsa la tecla de disparar
        bala_lista = 0
        for bala in iter(self.grupoMisBalas):
            if not (bala in self.grupoMisBalasActivas):
                bala_lista = bala
                break
        if bala_lista == 0:
            bala_lista = self.grupoMisBalas.sprites()[
                len(self.grupoMisBalas.sprites()) - 1
            ]

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(
            teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_e, bala_lista
        )


class Decorado:
    def __init__(self, cfg):
        # Cargar imagen fondo
        self.imagen = GestorRecursos.CargarImagen(cfg["image"], cfg["colorKey"])

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        self.rectSubImagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubImagen.left = 0

    def update(self, scrollx):
        self.rectSubImagen.left = scrollx
        # self.rect.left = -scrollx

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubImagen)
        # pantalla.blit(self.imagen, self.rect)


class Fondo:
    def __init__(self, bg_list):
        self.bg = []
        self.animated_bg = [i for i, bg in enumerate(bg_list) if bg["animated"]]
        for bg in bg_list:
            img = GestorRecursos.CargarImagen(bg["img"], bg["colorKey"])
            self.bg.append(
                (
                    pygame.transform.scale(img, (ANCHO_PANTALLA, ALTO_PANTALLA)),
                    bg["scroll"],
                )
            )

        self.rect = self.bg[0][0].get_rect()
        self.rect.left = 0  # El lado izquierdo de la subimagen que se esta visualizando
        self.pos = 0

    def update(self, scrollx):
        self.rect.left = scrollx

    def drawLayer(self, pantalla, layer, scrollx):
        pantalla.blit(layer, (scrollx - pantalla.get_width(), 0))
        pantalla.blit(layer, (scrollx, 0))

    def draw(self, pantalla, scrollx):
        self.pos += 2
        pantalla.fill("black")

        for i, bg in enumerate(self.bg):
            if i in self.animated_bg:
                self.drawLayer(
                    pantalla, bg[0], (-scrollx + self.pos) * bg[1] % ANCHO_PANTALLA
                )
            else:
                self.drawLayer(pantalla, bg[0], -scrollx * bg[1] % ANCHO_PANTALLA)


class Vida:
    def __init__(self):
        self.image = GestorRecursos.CargarImagen("heart_pixel.png", -1)

        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.top = 30

    def draw(self, pantalla, nLifes):
        rect = self.rect.copy()
        for _ in range(0, nLifes):
            pantalla.blit(self.image, rect)
            rect.left += rect.width + 5
