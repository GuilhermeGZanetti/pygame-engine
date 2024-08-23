import sys
import math
import random
from time import time
import pygame

# funcao para ler imagens com transparencia
def ler_imagem(caminho, tamanho):
    image = pygame.image.load(caminho)
    image = pygame.transform.scale(image, tamanho)
    image = image.convert_alpha()
    return image

# funcao para converter o vetor de coordenadas polares para cartesianas
def polar2cart(magnitude: float, angulo: float):
    x = magnitude * math.cos(angulo)
    y = magnitude * math.sin(angulo)
    return x, y