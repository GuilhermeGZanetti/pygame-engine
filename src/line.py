import math
import pygame

from src.vector2d import Vector2D

class Line:
    def __init__(self, start_point: Vector2D, end_point: Vector2D) -> None:
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, screen: pygame.Surface, color = (255, 0, 0), width = 5):
        pygame.draw.line(screen, color, self.start_point.as_tuple(), self.end_point.as_tuple(), width)

    def length(self):
        vector = self.end_point - self.start_point
        return vector.tamanho()