import pygame

from config import Config
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

    def launch_tongue(self, direction: Vector2D):
        self.is_launching = True
        self.direction = direction.normalize()
        self.tongue_point = Vector2D(*self.parent.rect.center)
        self.line = Line(self.parent.position, self.tongue_point)

    def retrieve_tongue(self):
        self.is_retrieving = True
        self.is_launched = False

    def update(self, screen: pygame.Surface, level: GameMap):
        if self.is_launching:
            # Increase tongue length until limit
            self.line.start_point = Vector2D(*self.parent.rect.center)
            self.tongue_point += self.direction * (Config.TONGUE_VELOCITY * self.parent.delta_time)
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
            # print(f"Tongue point: {self.direction * (Config.TONGUE_VELOCITY * self.parent.delta_time)} // Direction: {self.direction} // Config: {Config.TONGUE_VELOCITY} // Time: {self.parent.delta_time} // Tongue len: ", self.line.length())

            # Draw tongue
            self.line.draw(screen)
        elif self.is_retrieving:
            #Return tongue
            self.line.start_point = Vector2D(*self.parent.rect.center)
            self.tongue_point += (self.line.start_point - self.tongue_point).normalize() * (Config.TONGUE_VELOCITY * self.parent.delta_time)
            self.line.end_point = self.tongue_point

            if self.line.length() < 3:
                self.is_retrieving = False
                del(self.line)
                return
            self.line.draw(screen)
        elif self.is_launched:
            # Calculate the vector from the tongue's end point to the parent's position
            vector_to_parent = Vector2D(*self.parent.rect.center) - self.line.end_point
            distance = vector_to_parent.length()
            tension_force = Vector2D(0,0)
            # Check if the parent is beyond the maximum tongue length
            # if distance > self.tongue_len:
            # Get the line direction (from start to end point)
            line_direction = vector_to_parent.normalize()
            # Calculate tongue tension (component of gravity in the direction of line_direction)
            # T = Fcp + Py
            tangent_velocity = self.parent.physics.velocity.dot(Vector2D(line_direction.y, -line_direction.x).normalize())
            centripetal_force = (tangent_velocity**2)/distance
            tension_force = (centripetal_force + Vector2D(0,Config.GRAVITY).dot(-line_direction))*line_direction
            #Apply force parent
            self.parent.physics.apply_force(tension_force)

            # Força de mola na lngua
            if distance > self.tongue_len:
                K = 10
                spring_force = -K*(distance-self.tongue_len)*line_direction
                self.parent.physics.apply_force(spring_force)

            self.line.start_point = Vector2D(*self.parent.rect.center)
            self.line.draw(screen)                
            Line(self.line.start_point, self.line.start_point+tension_force*1/10).draw(screen, color=(0,255,0), width=2)

