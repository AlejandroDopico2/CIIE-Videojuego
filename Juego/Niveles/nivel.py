import pygame
from pygame.locals import *
from gestorRecursos import *
from Personajes.personajes import *
from escena import *
from Niveles.menuPausa import MenuPausa
from Niveles.menuTienda import MenuTienda
from Plataformas.plataformas import *
from Dialogos.dialogos import *
from Mercader.mercader import *
from Mercader.señalMerc import *

import json

ANCHO_PANTALLA = 1280
ALTO_PANTALLA = 720
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - 200
VELOCIDAD_BALA = 0.5

class Nivel(PygameScene):
    def __init__(self, director, cfg):
        PygameScene.__init__(self, director)

        with open(cfg, 'r') as f:
            self.cfg = json.load(f)

        self.director = director
        self.decorado = Decorado(self.cfg['decoration'])
        self.fondo = Fondo(self.cfg['background'])
        self.vida = Vida()
        self.scrollx = 0

        self.grupoSprites = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoMisBalas = pygame.sprite.Group()
        self.grupoMisBalasActivas = pygame.sprite.Group()


        # Se crea personaje
        self.jugador = Jugador()
        self.jugador.establecerPosicion((self.cfg['player'][0], self.cfg['player'][1]))
        self.grupoSprites.add(self.jugador)
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador)

        for i in range (0,20):
            bala = Bala("bullet.png", 'coordBala.txt', [1], VELOCIDAD_BALA, self.jugador.mirando)
            self.grupoMisBalas.add(bala)

        self.grupoPlataformas = pygame.sprite.Group()
        self.setPlatforms()
        self.setEnemies()

        #self.grupoDialogos = pygame.sprite.Group()
        #IMPORTANTE, DIALOGOS SIEMPRE EN ORDEN DE APARICION EN EL JSON
        self.listaDialog = []
        self.setDialogos()

        self.mercader = mercader()
        self.setMercader()
        self.señalMerc = señalMerc("../Mercader/señalMerc.png", (500, 30))
        # self.vida = self.jugador.barra
        # self.grupoSprites.add(self.vida)
        # self.grupoJugadores = pygame.sprite.Group(self.jugador)

    def setPlatforms(self):
            for pt in self.cfg['platforms']:
                plataforma = Plataforma(pygame.Rect(pt['x'], pt['y'], pt['width'], pt['height']))
                self.grupoPlataformas.add(plataforma)
                self.grupoSprites.add(plataforma)

    #NOTA: deben ponerse los dialogos en orden en el json
    def setDialogos(self):
        i = 0
        for d in self.cfg['dialogs']:
            dialogo = Dialogos(d['img'], (d['x'], d['y']), d['scale'], d['despl'], d['pos'], False)
            #self.grupoDialogos.add(dialogo)
            self.listaDialog.append(dialogo)
            i += 1
            #self.grupoSprites.add(dialogo)

    def setEnemies(self):
        for e in self.cfg['enemies']:
            if e['name'] == 'esqueleto':
                enemy = Esqueleto()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
            if e['name'] == 'demonio':
                enemy = Demonio()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
            if e['name'] == 'espectro':
                enemy = Espectro()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
            if e['name'] == 'cangrejo':
                enemy = Cangrejo()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
            if e['name'] == 'pajaro':
                enemy = Pajaro()
                enemy.establecerPosicion((e['pos'][0], e['pos'][1]))
                self.grupoEnemigos.add(enemy)
                self.grupoSprites.add(enemy)
                self.grupoSpritesDinamicos.add(enemy)

            if e['name'] != 'pajaro':
                self.grupoEnemigos.add(enemy)
                self.grupoSpritesDinamicos.add(enemy)
                self.grupoSprites.add(enemy)
    
    def setMercader(self):
        for m in self.cfg["merchant"]:
            self.mercader.establecerPosicion((m["x"], m["y"]))
            self.grupoSprites.add(self.mercader)


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
                
                self.director.exitScene()
            
            elif jugador.rect.left - MINIMO_X_JUGADOR < desplazamiento:
                
                jugador.establecerPosicion((jugador.posicion[0] - desplazamiento, jugador.posicion[1]))
                return False
            else:
                self.scrollx = self.scrollx + desplazamiento
                return True
        
        return False

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
            for bala in iter(self.grupoMisBalas):
                if bala.miraSiHaySignosVitales():
                    self.grupoMisBalasActivas.add(bala)
                else:
                    self.grupoMisBalasActivas.remove(bala)

            for bala in iter(self.grupoMisBalasActivas):
                bala.update(tiempo)

                if pygame.sprite.spritecollideany(bala, self.grupoEnemigos):
                    bala.muere()

                if pygame.sprite.spritecollideany(bala, self.grupoPlataformas):
                    bala.muere()


            diference = pygame.time.get_ticks() - self.jugador.ultimoGolpe
            if self.jugador.inmune and diference > 3000:
                print("Inmunidad acabada")
                self.jugador.inmune = False
                self.grupoSprites.add(self.jugador)
            elif self.jugador.inmune:
                if diference % 2 == 0:
                    self.grupoSprites.remove(self.jugador)
                else:
                    self.grupoSprites.add(self.jugador)

            for enemigo in iter(self.grupoEnemigos):
                if pygame.sprite.spritecollideany(enemigo, self.grupoMisBalasActivas):
                    enemigo.vida -= 1
                    if enemigo.vida <= 0:
                        pygame.sprite.Sprite.kill(enemigo)
                    #EFECTO DE ENEMIGO DE RECIBIR DAÑO
                enemigo.mover_cpu(self.jugador)

            self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

            if self.jugador.posicion[1] - self.jugador.rect.height > ALTO_PANTALLA:
                self.director.exitScene()

            if pygame.sprite.spritecollideany(self.jugador, self.grupoEnemigos) != None:
                self.jugador.dañarJugador()

                if self.jugador.vida == 0:
                    self.director.exitScene()
            for i in range(len(self.listaDialog)):
                #caso del primer dialogo
                if (self.listaDialog[i].getCoord()[0] - self.listaDialog[i].getDespl() < self.jugador.rect.x < self.listaDialog[i].getCoord()[0] + self.listaDialog[i].getDespl()) and (
                    self.listaDialog[i].getCoord()[1] - self.listaDialog[i].getDespl() < self.jugador.rect.y < self.listaDialog[i].getCoord()[1] + self.listaDialog[i].getDespl()) and (
                    not self.listaDialog[i].getActive()) and i == 0:
                    self.grupoSprites.add(self.listaDialog[i])
                elif i == 0:
                    self.grupoSprites.remove(self.listaDialog[i])
                    self.listaDialog[i].setActive(True)
                #caso dialogos mercader
                else:
                    if (self.listaDialog[i].getCoord()[0] - self.listaDialog[i].getDespl() < self.jugador.rect.x + self.scrollx < self.listaDialog[i].getCoord()[0] + self.listaDialog[i].getDespl()):
                        self.grupoSprites.add(self.listaDialog[i])
                        self.listaDialog[i].setActive(True)
                    else:
                        #self.grupoSprites.remove(self.listaDialog[i]) TODO pendiente pintar pos pantalla bien
                        self.listaDialog[i].setActive(False)
                    if self.director.tienda and i == 2:
                        print("gracias por venir")
                        self.listaDialog[i].setActive(True)
                        self.grupoSprites.add(self.listaDialog[i])
            
            self.mercader.update(tiempo)
            self.jugador.reduce_recarga()
            self.actualizarScroll(self.jugador)
        # self.fondo.update(tiempo)

    def draw(self, pantalla):
        self.fondo.draw(pantalla, self.scrollx)
        self.decorado.draw(pantalla)
        self.vida.draw(pantalla, self.jugador.vida)
        if (self.listaDialog[1].getActive()):
            self.señalMerc.draw(pantalla)
        self.grupoSprites.draw(pantalla)
        self.grupoMisBalasActivas.draw(pantalla)


    def eventsLoop(self, lista_eventos):
        for evento in lista_eventos:
            if self.director.pause:
                nivel = MenuPausa(self.director)
                self.director.stackScene(nivel)
                #GestorRecursos.CargarMenuPausa(self)
            if self.director.tienda and self.listaDialog[1].getActive():
                nivel = MenuTienda(self.director)
                self.director.stackScene(nivel)
            if evento.type == pygame.QUIT:
                self.director.exitProgram()

        bala_lista = 0
        for bala in iter(self.grupoMisBalas):
            if not(bala in self.grupoMisBalasActivas):
                bala_lista = bala
                break
        if bala_lista == 0:
            bala_lista = self.grupoMisBalas.sprites()[len(self.grupoMisBalas.sprites())-1]

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_e, bala_lista)

class Decorado:
    def __init__(self, img):
        # Cargar imagen fondo
        self.imagen = GestorRecursos.CargarImagen(img, -1)

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
        self.animated_bg = [i for i, bg in enumerate(bg_list) if bg['animated']]
        for bg in bg_list:
            img = GestorRecursos.CargarImagen(bg['img'], bg['colorKey'])
            self.bg.append((pygame.transform.scale(img, (ANCHO_PANTALLA, ALTO_PANTALLA)), bg['scroll']))
        
        self.rect = self.bg[0][0].get_rect()
        self.rect.left = 0 # El lado izquierdo de la subimagen que se esta visualizando
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
                self.drawLayer(pantalla, bg[0], (-scrollx + self.pos) * bg[1] % ANCHO_PANTALLA)
            else:
                self.drawLayer(pantalla, bg[0], -scrollx * bg[1] % ANCHO_PANTALLA)

class Vida:
    def __init__(self):
        self.image = GestorRecursos.CargarImagen('heart_pixel.png', -1)

        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.top = 30

    def draw(self, pantalla, nLifes):
        rect = self.rect.copy()
        for _ in range (0, nLifes):
            pantalla.blit(self.image, rect)
            rect.left += rect.width + 5
