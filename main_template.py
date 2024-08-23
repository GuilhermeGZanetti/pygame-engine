
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
    if (sair):
        pygame.quit()
        sys.exit(0)

    teclas_pressionadas = pygame.key.get_pressed()

    ######################################
    # ATUALIZACAO DO ESTADO DO JOGO
    ######################################

    

    ######################################
    # DESENHO NA TELA
    ######################################

    # preenche a tela com branco
    tela.fill("white")

    
    

    # atualiza a janela
    pygame.display.flip()