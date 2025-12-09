import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import os
import random

pygame.init()
pygame.mixer.init()

branco = (255,255,255)
largura_janela, altura_janela = 640, 480
velocidade = 5
obstaculoescolhido = 0
colidiu = False
pontos = 1
gravidade = 0.5
dificuldade = 1
mode = 0
num1 = 0
num2 = 0
tosdauj = 0
x= 1
dinolista = []
momento = 0
mortos = 0
melhoraleatorio = -1000000
melhoraleatorio2 = 0
FPS = 60

pygame.display.set_caption('Dino Game')
tela = pygame.display.set_mode((largura_janela, altura_janela))
clock = pygame.time.Clock()

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade, colidiu, obstaculoescolhido,dificuldade,mode,branco,num1,num2,tosdauj,mortos
    pontos = 1
    velocidade = 5
    colidiu = False
    dinoVoador.rect.x = largura_janela
    dinoVoador.rect.y = 300
    cacto.rect.x = largura_janela
    cacto2.rect.x = largura_janela +32
    obstaculoescolhido = 0
    dificuldade = 1
    mode = 0
    num1,num2 = 0,0
    tosdauj = 0
    branco = (255,255,255)
    mortos = 0
    #dinolista = []
    for i in range(50):
        (dinolista[i]).rect.x = 100
        (dinolista[i]).morreu = False
        (dinolista[i]).d3 = 0
        (dinolista[i]).d2 = 0
    if False:
        allsprites = pygame.sprite.Group()
        for i in range(50):
            dino = Dino()
            allsprites.add(dino)
            dinolista.append(dino)

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
        self.velocidade = 0
        self.morreu = False
        self.d2 = 0
        self.d3 = 0
        self.numeroaletorio = float(random.randint(-5,0))
        self.numeroaletorio2 = float(random.randint(0,10))
    

    def pular(self):
        if self.rect.y == self.posy:
            self.pulo = True
            self.d1 = 0
            self.som_pulo.play()

    def update(self):
        global mortos,melhoraleatorio,melhoraleatorio2
        if melhoraleatorio != -1000000 and self.d3 == 0:
            self.numeroaletorio = melhoraleatorio +(random.uniform(-1,1))
            if self.numeroaletorio > 0:
                self.numeroaletorio = 0
            self.numeroaletorio2 = melhoraleatorio2 +(random.uniform(-2,2))
            self.d3 = 1
        
        if momento == 1 and self.rect.y > 300:
            self.morreu = True
        if self.morreu == True:
            self.rect.x -= 5
            if self.d2 == 0:
                self.d2 = 1
                if mortos == 49:
                    melhoraleatorio = self.numeroaletorio
                    melhoraleatorio2 = self.numeroaletorio2
                mortos += 1
        if pontos <= 10:
            self.morreu = False
                
        if cacto.rect.x < cacto2.rect.x:
            cact = cacto.rect.x
        else:
            cact = cacto2.rect.x
        distanciacacto = cact-self.rect.x     
        if distanciacacto < 0:
            distanciacacto = 0
        
        if distanciacacto*self.numeroaletorio+velocidade*self.numeroaletorio2 >= 0:
            self.pular()

        if self.pulo == True and not(self.morreu):
                self.velocidade = -10
                self.pulo = False
                self.d1 = 1

        elif not(self.morreu):
            if self.rect.y >= self.posy:
                self.rect.y = self.posy
                self.d1 = 0
            else:
                self.rect.y += 0

        if self.d1 == 1:
            self.rect.y += self.velocidade
            self.velocidade += gravidade

        if self.indexsprite > 2 and not(self.morreu):
            self.indexsprite = 0
        if not(self.morreu):
            self.indexsprite += 0.12
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
        self.rect.x -= 5

class Cacto(pygame.sprite.Sprite):
    def __init__(self,num):
        pygame.sprite.Sprite.__init__(self)
        self.image = dinosheet.subsurface((5*32, 0), (32,32))  
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = obstaculoescolhido
        self.rect = self.image.get_rect()
        self.rect.center = (largura_janela, altura_janela-64)
        self.rect.x =  largura_janela +num*32

    def update(self):
        global momento
        if 100 <self.rect.x < 150:
            momento = 1
        else:
            momento = 0
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
        self.rect.center = (largura_janela, 320)
        self.rect.x = largura_janela
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura_janela
            self.rect.x -= velocidade

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.12
            self.image = self.imagens_dinossauro[int(self.index_lista)]

allsprites = pygame.sprite.Group()
for i in range(50):
    dino = Dino()
    allsprites.add(dino)
    dinolista.append(dino)

for i in range(4):
    nuvens = Nuvens()
    allsprites.add(nuvens)

for i in range(altura_janela*2//64):
    chao  = Chao(i)
    allsprites.add(chao)

dinoVoador = DinoVoador()
allsprites.add(dinoVoador)

cacto = Cacto(0)
cacto2 = Cacto(1)
allsprites.add(cacto)
allsprites.add(cacto2)

allobstaculos = pygame.sprite.Group()
allobstaculos.add(cacto)
allobstaculos.add(cacto2)
allobstaculos.add(dinoVoador)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and colidiu == False:
                for i in range (50):
                    if (dinolista[i]).rect.y != (dinolista[i]).posy:
                        pass
                    else:
                        (dinolista[i]).pular()

            if event.key == K_r:
                reiniciar_jogo()


    tela.fill(branco)
    allsprites.draw(tela)

    if (cacto.rect.topright[0] <= 0 or dinoVoador.rect.topright[0] <= 0) and mode == 0:
        obstaculoescolhido = random.randint(0, 9)
        print(obstaculoescolhido)
        if obstaculoescolhido == 9:
            obstaculoescolhido = 1
        else:
            obstaculoescolhido = 0
        cacto.rect.x = largura_janela 
        dinoVoador.rect.x = largura_janela
        cacto.escolha = obstaculoescolhido
        cacto2.escolha = obstaculoescolhido
        cacto2.rect.x = largura_janela +32*dificuldade
        dinoVoador.escolha = obstaculoescolhido
        if dificuldade == 3:
            dinoVoador.rect.y = random.randint(280,altura_janela-120)
            cacto.rect.x = random.choice([cacto2.rect.x-64,cacto2.rect.x+600])

    if (cacto.rect.topright[0] >= largura_janela+32 or dinoVoador.rect.topright[0] >= largura_janela+32) and mode == 1:
        obstaculoescolhido = random.randint(0, 9)
        #print(obstaculoescolhido)
        if obstaculoescolhido == 9:
            obstaculoescolhido = 1
        else:
            obstaculoescolhido = 0
        cacto.rect.x = 0 
        dinoVoador.rect.x = -96
        cacto.escolha = obstaculoescolhido
        cacto2.escolha = obstaculoescolhido
        cacto2.rect.x = 0 -32*dificuldade
        dinoVoador.escolha = obstaculoescolhido
        if dificuldade == 3:
            dinoVoador.rect.y = random.randint(280,altura_janela-120)
            cacto.rect.x = random.choice([cacto2.rect.x+64,cacto2.rect.x-600])

    #if colisoes and colidiu == False:
        #som_colisao.play()
        #colidiu = True

    if mortos == 50:
        if int(pontos) % 100 == 0:
            pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
        tela.blit(game_over, (largura_janela//2, altura_janela//2))
        restart = exibe_mensagem('Pressione r para reiniciar', 20, (0,0,0))
        tela.blit(restart, (largura_janela//2, (altura_janela//2) + 60))
    else:
        pontos += 0.2
        allsprites.update()
        texto_pontos = exibe_mensagem(int(pontos), 40, (0,0,0))

    if int(pontos) % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 120.5 or mode ==1:
            velocidade += 0
        else:
            velocidade += 0.2

    if int(pontos) % 400 == 0:
        pontos += 1
        dificuldade += 1
        dificuldade = min(dificuldade,3)

    print(melhoraleatorio)
    pygame.draw.rect(tela,(0,0,0),(100,300,50,5))
    tela.blit(texto_pontos, (largura_janela-120-tosdauj, 30))
    clock.tick(FPS)
    pygame.display.flip()