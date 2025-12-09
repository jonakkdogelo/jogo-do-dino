import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import os
import random

pygame.init()
pygame.mixer.init()

largura_janela, altura_janela = 640, 480
velocidade = 10
obstaculoescolhido = 0
colidiu = False
pontos = 1
FPS = 30

pygame.display.set_caption('Dino Game')
tela = pygame.display.set_mode((largura_janela, altura_janela))
clock = pygame.time.Clock()

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade, colidiu, obstaculoescolhido
    pontos = 0
    velocidade = 10
    colidiu = False
    dino.rect.y = altura_janela - 64 - 96//2
    dino.pulo = False
    dinoVoador.rect.x = largura_janela
    cacto.rect.x = largura_janela
    obstaculoescolhido = 0

pasta_principal = os.path.dirname(__file__)
pastasons = os.path.join(pasta_principal, 'sons')
som_colisao = pygame.mixer.Sound(os.path.join(pastasons, 'death_sound.wav'))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(pastasons, 'score_sound.wav'))
som_pontuacao.set_volume(1)


dinosheet = pygame.image.load(os.path.join(pasta_principal, 'dinoSpritesheet.png')).convert_alpha()
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(pastasons, 'jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.imagensdinossauro = []
        for i in range(3):
            img = dinosheet.subsurface((32*i,0), (32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.imagensdinossauro.append(img)

        self.indexsprite = 0
        self.image = self.imagensdinossauro[self.indexsprite]
        self.rect = self.image.get_rect()
        self.posy = altura_janela - 64 - 96//2
        self.rect.topleft = (100,self.posy)
        self.pulo = False


    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= self.posy - 150:
                self.pulo = False
            self.rect.y -= 15

        else:
            if self.rect.y >= self.posy:
                self.rect.y = self.posy
            else:
                self.rect.y += 15

        if self.indexsprite > 2:
            self.indexsprite = 0
        self.indexsprite += 0.25
        self.image = self.imagensdinossauro[int(self.indexsprite)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = dinosheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(50, 200, 50)
        self.rect.x = largura_janela - random.randrange(30, 300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura_janela
            self.rect.y = random.randrange(50, 200, 50)
        self.rect.x -= velocidade

class Chao(pygame.sprite.Sprite):
    def __init__(self,posx):
        pygame.sprite.Sprite.__init__(self)
        self.image = dinosheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.x =  posx * 64
        self.rect.y = altura_janela -64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura_janela
        self.rect.x -= 10

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = dinosheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = obstaculoescolhido
        self.rect = self.image.get_rect()
        self.rect.center = (largura_janela, altura_janela-64)
        self.rect.x =  largura_janela

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura_janela
            self.rect.x -= velocidade

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = dinosheet.subsurface((i*32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = obstaculoescolhido
        self.rect = self.image.get_rect()
        self.rect.center = (largura_janela, 300)
        self.rect.x = largura_janela
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura_janela
            self.rect.x -= velocidade

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_dinossauro[int(self.index_lista)]

allsprites = pygame.sprite.Group()
dino = Dino()
allsprites.add(dino)

for i in range(4):
    nuvens = Nuvens()
    allsprites.add(nuvens)

for i in range(altura_janela*2//64):
    chao  = Chao(i)
    allsprites.add(chao)

cacto = Cacto()
allsprites.add(cacto)

dinoVoador = DinoVoador()
allsprites.add(dinoVoador)

allobstaculos = pygame.sprite.Group()
allobstaculos.add(cacto)
allobstaculos.add(dinoVoador)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.posy:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colidiu == True:
                reiniciar_jogo()


    tela.fill((255,255,255))
    allsprites.draw(tela)

    colisoes = pygame.sprite.spritecollide(dino, allobstaculos, False, pygame.sprite.collide_mask)

    if cacto.rect.topright[0] <= 0 or dinoVoador.rect.topright[0] <= 0:
        obstaculoescolhido = random.randint(0, 9)
        if obstaculoescolhido == 9:
            obstaculoescolhido = 1
        else:
            obstaculoescolhido = 0
        cacto.rect.x = largura_janela
        dinoVoador.rect.x = largura_janela
        cacto.escolha = obstaculoescolhido
        dinoVoador.escolha = obstaculoescolhido

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        if int(pontos) % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
        tela.blit(game_over, (largura_janela//2, altura_janela//2))
        restart = exibe_mensagem('Pressione r para reiniciar', 20, (0,0,0))
        tela.blit(restart, (largura_janela//2, (altura_janela//2) + 60))

    else:
        pontos += 0.4
        allsprites.update()
        texto_pontos = exibe_mensagem(int(pontos), 40, (0,0,0))

    if int(pontos) % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 25:
            velocidade += 0
        else:
            velocidade += 1

    tela.blit(texto_pontos, (520, 30))

    clock.tick(FPS)
    pygame.display.flip()