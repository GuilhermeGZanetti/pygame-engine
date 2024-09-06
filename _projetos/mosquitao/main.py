
import sys
import math
import random
from time import time
import pygame
from src.utils import ler_imagem, polar2cart

# constantes
HEALTHY_MAGNITUDE = 0.2
PUNHO_SPEED_MAGNITUDE = 0.1
total_time = 20



# inicializacao do pygame e da tela
pygame.init()
tela = pygame.display.set_mode((700, 700))

# leitura das imagens
punho = ler_imagem('sprites/fist.png', (80, 80))
healthy = ler_imagem('sprites/mosquito-saudavel.png', (80, 80))
hit = ler_imagem('sprites/mosquito-morto.png', (80, 80))

# variaveis de estado da mosca
healthy_x = 320
healthy_y = 240
healthy_angulo = random.uniform(-math.pi, math.pi)

# variaveis de estado do punho
punho_x = 320
punho_y = 240
punho_vx = 0
punho_vy = 0

# em caso de colisao, mostra a mosca morta por este tempo
frames_hit = 0

# variaveis de estado para mostrar o tempo e a pontuacao na tela
font = pygame.font.SysFont(None, 48)
pontuacao = 0
start = time()
time_left = total_time

while True:
    ######################################
    # TRATAMENTO DE EVENTOS
    ######################################
    sair = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True

    # termina o jogo se acabar o tempo ou se a pessoa clicar
    # no botao de sair
    if (sair) or (time_left <= 0):
        pygame.quit()
        sys.exit(0)

    teclas_pressionadas = pygame.key.get_pressed()

    # movimento na horizontal
    punho_vx = 0.0
    if teclas_pressionadas[pygame.K_a]:
        punho_vx = -PUNHO_SPEED_MAGNITUDE
    elif teclas_pressionadas[pygame.K_d]:
        punho_vx = PUNHO_SPEED_MAGNITUDE

    # movimento na vertical
    punho_vy = 0.0
    if teclas_pressionadas[pygame.K_s]:
        punho_vy = PUNHO_SPEED_MAGNITUDE
    elif teclas_pressionadas[pygame.K_w]:
        punho_vy = -PUNHO_SPEED_MAGNITUDE

    # verifica se o jogador atacou
    ataque_realizado = False
    if teclas_pressionadas[pygame.K_j]:
        ataque_realizado = True

    ######################################
    # ATUALIZACAO DO ESTADO DO JOGO
    ######################################

    # atualiza posicao da mosca com base na velocidade
    healthy_vx, healthy_vy = polar2cart(HEALTHY_MAGNITUDE, healthy_angulo)
    healthy_x += healthy_vx
    healthy_y += healthy_vy

    # se a mosca tocar os limites da tela, inverte seleciona uma nova
    # direcao aleatoria de movimento
    if (healthy_x < 0) or (healthy_x + healthy.get_width() > tela.get_width()) or \
            (healthy_y < 0) or (healthy_y + healthy.get_height() > tela.get_height()):
        healthy_angulo = random.uniform(-math.pi, math.pi)

    # atualiza posicao do punho com base na velocidade
    punho_x += punho_vx
    punho_y += punho_vy

    # restringe o movimento do punho para ficar na tela
    if punho_x < 0:
        punho_x = 0
    if punho_y < 0:
        punho_y = 0
    if punho_x + punho.get_width() > tela.get_width():
        punho_x = tela.get_width() - punho.get_width()
    if punho_y + punho.get_height() > tela.get_height():
        punho_y = tela.get_height() - punho.get_height()

    # processa o ataque
    if frames_hit > 0:
        frames_hit -= 1
        # reamostra a posicao e direcao de movimento da mosca quando o tempo
        # de morto terminar
        if frames_hit == 0:
            healthy_x = random.randint(0, tela.get_width() - healthy.get_width())
            healthy_y = random.randint(0, tela.get_height() - healthy.get_height())
            healthy_angulo = random.uniform(-math.pi, math.pi)

    if ataque_realizado:
        # obtem o retangulo ao redor do punho na posicao atual do punho
        punho_rect = punho.get_rect(x=punho_x, y=punho_y)
        # obtem o retangulo ao redor do rosto healthy na posicao atual do rosto healthy
        healthy_rect = healthy.get_rect(x=healthy_x, y=healthy_y)
        # verifca se houve colisao entre os dois retangulos (e a mosca estava viva)
        if punho_rect.colliderect(healthy_rect) and (frames_hit == 0):
            frames_hit = 500
            pontuacao += 1

    # atualiza o tempo de partida
    time_left = total_time - (time() - start)

    ######################################
    # DESENHO NA TELA
    ######################################

    # preenche a tela com branco
    tela.fill("white")

    # desenha a mosca viva ou morta
    if frames_hit == 0:
        tela.blit(healthy, (healthy_x, healthy_y))
    else:
        tela.blit(hit, (healthy_x, healthy_y))

    # desenha o punho
    tela.blit(punho, (punho_x, punho_y))

    # desenha a pontuacao e o tempo de partida
    img = font.render(
        f'Time: {time_left:.0f} Pontos: {pontuacao:03d}', True, (0, 0, 0))
    px = tela.get_width() * 0.25
    py = tela.get_height() * 0.1
    tela.blit(img, (px, py))

    # atualiza a janela
    pygame.display.flip()