from src.utils import Position, Velocity
import pygame as pg

class Ball:
    def __init__(self, position: Position, velocity: Velocity) -> None:
        self.position = position
        self.velocity = velocity


class Paddle:
    def __init__(self, position: Position, velocity_y: float, height: float, width: float) -> None:
        self.position = position
        self.velocity = Velocity(0, velocity_y)
        self.height = height
        self.width = width

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(
            self.position.x, self.position.y, self.width, self.height))