from pygame import Rect, Surface
import pygame
from config import Config
from src.utils import load_img
from src.vector2d import Vector2D


class Frog:
    def __init__(self, sprite_sheet, px: int, py: int, size: float = 1) -> None:
        self.sprite_sheet: Surface = load_img(sprite_sheet)
        self.rect: Rect = pygame.rect.Rect(px, py, Config.FROG_WIDTH*size, Config.FROG_HEIGHT*size)
        self.velocity: Vector2D = Vector2D(0, 0)

        self.current_image: Surface = self.sprite_sheet.subsurface(
            (0 * Config.FROG_WIDTH, 
             0 * Config.FROG_HEIGHT, 
             Config.FROG_WIDTH, 
             Config.FROG_HEIGHT)
        )
