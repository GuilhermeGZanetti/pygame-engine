import pygame

from src.vector2d import Vector2D

class PhysicsComponent:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.velocity: Vector2D = Vector2D(0, 0)
        self.resulting_force: Vector2D = Vector2D(0, 0)

    def update(self, delta_time: float):
        # Run physics
        self.velocity.x = self.velocity.x + (self.resulting_force.x * delta_time)
        self.velocity.y = self.velocity.y + (self.resulting_force.y * delta_time)

        self.resulting_force = Vector2D(0, 0)

    def apply_force(self, force: Vector2D):
        self.resulting_force += force