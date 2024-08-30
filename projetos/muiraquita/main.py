
import sys
import math
import random
from time import time
import pygame
from src.tilemap import GameMap, TileList
from src.utils import load_img, polar2cart

# constantes
TILE_SIZE=16
SCALE = 2


pygame.init()


# inicializacao do pygame e da tela
pygame.init()
screen = pygame.display.set_mode((30 * TILE_SIZE*SCALE, 20 * TILE_SIZE*SCALE))

level = GameMap("projetos/muiraquita/maps/fase0.json")
tile_list = TileList("projetos/muiraquita/sprites/nature_elements/nature_tileset.png", TILE_SIZE, TILE_SIZE)
forest_background = load_img("projetos/muiraquita/sprites/nature_elements/forest_background.png", (480*SCALE*1.5, 270*SCALE*1.5))


# variaveis de estado para mostrar o tempo e a pontuacao na tela
font = pygame.font.SysFont(None, 48)
start = time()

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
    screen.fill((0, 0, 0))
    screen.blit(forest_background, (0,0))
    level.draw(screen, tile_list, scale=SCALE)
    pygame.display.flip()

    
    

    # atualiza a janela
    pygame.display.flip()