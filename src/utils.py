import math
import pygame
from typing import Tuple, Optional


class Velocity:
    def __init__(self, vx, vy) -> None:
        self.x = vx
        self.y = vy

class Position:
    def __init__(self, px, py) -> None:
        self.x = px
        self.y = py

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

def load_img(caminho: str, size: Optional[Tuple[int, int]] = None):
    image = pygame.image.load(caminho)
    if size:
        image = pygame.transform.scale(image, size)
    image = image.convert_alpha()
    return image