import pygame

from config import Config
from src.game_time import Time
from src.line import Line
from src.tilemap import GameMap
from src.vector2d import Vector2D

class GrapplingTongue:
    def __init__(self, parent) -> None:
        self.parent = parent

        self.is_launched: bool = False
        self.is_launching: bool = False
        self.is_retrieving: bool = False
        
        self.tongue_point: Vector2D = Vector2D(parent.position.x, parent.position.y)
        self.line: Line | None = None
        self.tongue_len = None

    def is_moving(self):
        return self.is_launching or self.is_retrieving
    
    def is_extended(self):
        return self.is_launched
    
    def apply_clockwise_force(self, flag_counterclock: int):
        tongue_direction = (Vector2D(*self.parent.rect.center) - self.line.end_point).normalize()

        if flag_counterclock == 1:
            force_direction = Vector2D(tongue_direction.y, -tongue_direction.x)
        else:
            force_direction = Vector2D(-tongue_direction.y, +tongue_direction.x)
        force = force_direction * Config.FROG_AIR_FORCE
        self.parent.physics.apply_force(force)

    def launch_tongue(self, direction: Vector2D):
        self.is_launching = True
        self.direction = direction.normalize()
        self.tongue_point = Vector2D(*self.parent.rect.center)
        self.line = Line(self.parent.position, self.tongue_point)

    def retrieve_tongue(self):
        self.is_retrieving = True
        self.is_launched = False

    def retract_tongue(self):
        if self.is_extended():
            tongue_change = Config.TONGUE_CONTROL * Time.delta_time
            self.tongue_len -= tongue_change
            line_direction = (Vector2D(*self.parent.rect.center) - self.line.end_point).normalize()
            self.parent.rect.center = (Vector2D(*self.parent.rect.center) - line_direction * tongue_change).as_tuple()

    def extend_tongue(self):
        if self.is_extended():
            tongue_change = Config.TONGUE_CONTROL * Time.delta_time
            self.tongue_len += tongue_change
            line_direction = (Vector2D(*self.parent.rect.center) - self.line.end_point).normalize()
            self.parent.rect.center = (Vector2D(*self.parent.rect.center) + line_direction * tongue_change).as_tuple()

    def fixed_update(self, level: GameMap):
        if self.is_launching:
            # Increase tongue length until limit
            self.line.start_point = Vector2D(*self.parent.rect.center)
            self.tongue_point += self.direction * (Config.TONGUE_VELOCITY * Time.fixed_delta_time)
            self.line.end_point = self.tongue_point
            
            # Check tongue collision with tilemap
            collision = level.detect_line_tile_collision(line=self.line)            
            if collision:
                self.is_launching = False
                self.is_launched = True
                self.line.end_point = collision
                self.tongue_len = self.line.length()
            elif self.line.length() > Config.MAX_TONGUE_LENGTH:
                self.is_launching = False
                self.is_retrieving = True
            # print(f"Tongue point: {self.direction * (Config.TONGUE_VELOCITY * Time.fixed_delta_time)} // Direction: {self.direction} // Config: {Config.TONGUE_VELOCITY} // Time: {Time.fixed_delta_time} // Tongue len: ", self.line.length())

            # Draw tongue
        elif self.is_retrieving:
            #Return tongue
            self.line.start_point = Vector2D(*self.parent.rect.center)
            self.tongue_point += (self.line.start_point - self.tongue_point).normalize() * (Config.TONGUE_VELOCITY * Time.fixed_delta_time)
            self.line.end_point = self.tongue_point

            if self.line.length() < 3:
                self.is_retrieving = False
                del(self.line)
                return
        elif self.is_launched:
            # Calculate the vector from the tongue's end point to the parent's position
            vector_to_parent = Vector2D(*self.parent.rect.center) - self.line.end_point
            distance = vector_to_parent.length()
            line_direction = vector_to_parent.normalize()
            tension_force = Vector2D(0,0)
            # Força de mola na lngua
            if distance > self.tongue_len:
                tension_force = -Config.TONGUE_ELASTIC_CONSTANT*(distance-self.tongue_len)*line_direction
                self.parent.physics.apply_force(tension_force)

            # Reduz componente da velocidade paralela à lingua
            self.parent.physics.velocity -= ((self.parent.physics.velocity.dot(line_direction)) * line_direction * Time.fixed_delta_time)*2

            self.line.start_point = Vector2D(*self.parent.rect.center)

    def draw(self, screen: pygame.Surface):
        if self.is_moving() or self.is_extended():
            self.line.draw(screen)