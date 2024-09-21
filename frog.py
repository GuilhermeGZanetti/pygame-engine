from pygame import Rect, Surface
import pygame
from animator import Animator
from config import Config
from grappling_tongue import GrapplingTongue
from physics import PhysicsComponent
from src.game_time import Time
from src.tilemap import GameMap, Tile
from src.utils import load_img
from src.vector2d import Vector2D
import time


class Frog:
    def __init__(self, run_sprite_sheet, idle_sprite_sheet, px: int, py: int, size: float = 1) -> None:
        self.run_sprite_sheet: Surface = load_img(run_sprite_sheet)
        self.idle_sprite_sheet: Surface = load_img(idle_sprite_sheet)
        self.rect: Rect = pygame.rect.Rect(px, py, Config.FROG_WIDTH * size, Config.FROG_HEIGHT * size)
        self.max_velocity = Config.FROG_SPEED
        self.position: Vector2D = Vector2D(px, py)
        self.physics: PhysicsComponent = PhysicsComponent(parent=self)

        self.grappling_tongue = GrapplingTongue(self)

        # Animation
        self.run_frames = self.init_sprite_sheet(self.run_sprite_sheet, 7, size)
        self.idle_frames = self.init_sprite_sheet(self.idle_sprite_sheet, 8, size)
        self.jump_frames = self.init_sprite_sheet(self.run_sprite_sheet, 1, size, offset=3)

        self.animator = Animator(run_frames=self.run_frames, idle_frames=self.idle_frames, jump_frames=self.jump_frames, starting_animation="idle")

    def fixed_update(self, level: GameMap) -> None:
        self.grappling_tongue.fixed_update(level=level)
        self.apply_physics(level=level)
        self.move_and_apply_collisions(level=level)
        self.verify_screen_bounds()


    def update(self, screen: Surface, level: GameMap) -> None:
        self.handle_input(level)        

        self.animate(level=level)
        self.draw(screen)
    

    #### INPUT HANDLING ####

    def handle_input(self, level: GameMap) -> None:
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.command_move(right=False, level=level)
        elif pressed_keys[pygame.K_RIGHT]:
            self.command_move(right=True, level=level)
        else:
            self.is_moving = False

        if pressed_keys[pygame.K_UP]:
            self.grappling_tongue.retract_tongue()
        elif pressed_keys[pygame.K_DOWN]:
            self.grappling_tongue.extend_tongue()

        if pressed_keys[pygame.K_z]:
            if self.pressed_tongue == False:
                self.pressed_tongue = True
                if not self.grappling_tongue.is_moving() and not self.grappling_tongue.is_extended():
                    direction = Vector2D(-int(pressed_keys[pygame.K_LEFT])+int(pressed_keys[pygame.K_RIGHT]),
                                         -int(pressed_keys[pygame.K_UP])+int(pressed_keys[pygame.K_DOWN]))
                    if direction.x == 0 and direction.y == 0:
                        direction.x = 1 if self.animator.facing_right else -1
                    self.grappling_tongue.launch_tongue(direction)
                elif not self.grappling_tongue.is_moving():
                    self.grappling_tongue.retrieve_tongue()
        else:
            self.pressed_tongue = False

        if pressed_keys[pygame.K_x]:
            if not self.is_jumping(level):
                self.start_jump()
    
    def command_move(self, right: bool, level: GameMap):
        flag_sign = 1 if right else -1
        if self.is_jumping(level) and self.grappling_tongue.is_extended():
            self.physics.apply_force(Vector2D(flag_sign * Config.FROG_AIR_FORCE, 0))
        else:
            velocity = self.physics.velocity.x + flag_sign * Config.FROG_ACCELERATION * Time.delta_time
            if abs(velocity) < self.max_velocity:
                self.physics.velocity.x = velocity
        self.is_moving = True

            
    def start_jump(self) -> None:
        self.physics.velocity.y = -Config.JUMP_SPEED


    #### ANIMATION ####
    def animate(self, level: GameMap) -> None:
        self.animator.update(
            velocity=self.physics.velocity, 
            is_jumping=self.is_jumping(level), 
            delta_time=Time.delta_time, 
            is_running=self.is_moving
        )
            

    def init_sprite_sheet(self, image: Surface, number_frames: int, size: float, offset: int = 0) -> list[Surface]:
        frames = [
            image.subsurface(((x * 2 * Config.FROG_WIDTH)+10, 10, Config.FROG_WIDTH, Config.FROG_HEIGHT))
            for x in range(offset, offset+number_frames) 
        ]
        frames = [pygame.transform.scale(frame, (Config.FROG_WIDTH * size, Config.FROG_HEIGHT * size)) for frame in frames]

        return frames


    #### DRAWING ####

    def draw(self, screen: Surface) -> None:
        self.grappling_tongue.draw(screen=screen)
        screen.blit(self.animator.current_image, self.rect)
        # Draw red rectangle for debug
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)




    #### PHYSICS ####

    def apply_physics(self, level: GameMap) -> None:
        fixed_drag = Config.FIXED_DRAG if self.is_jumping(level) else Config.FIXED_DRAG * 50
        if self.physics.velocity.x > 0:
            self.physics.velocity.x -= fixed_drag * Time.fixed_delta_time
            if self.physics.velocity.x < 0:
                self.physics.velocity.x = 0
        elif self.physics.velocity.x < 0:
            self.physics.velocity.x += fixed_drag * Time.fixed_delta_time
            if self.physics.velocity.x > 0:
                self.physics.velocity.x = 0
        
        if self.physics.velocity.y > 0:
            self.physics.velocity.y -= fixed_drag * Time.fixed_delta_time
            if self.physics.velocity.y < 0:
                self.physics.velocity.y = 0
        elif self.physics.velocity.y < 0:
            self.physics.velocity.y += fixed_drag * Time.fixed_delta_time
            if self.physics.velocity.y > 0:
                self.physics.velocity.y = 0
        
        drag_force = -(Config.DRAG * (self.physics.velocity)/2)
        self.physics.apply_force(drag_force)
        gravity_force = Vector2D(0, Config.GRAVITY)
        self.physics.apply_force(gravity_force)

        self.physics.update(delta_time=Time.fixed_delta_time)


    def move_and_apply_collisions(self, level: GameMap) -> None:
        # Move in x direction
        self.position.x += self.physics.velocity.x * Time.fixed_delta_time
        self.rect.x = int(self.position.x)  # Update rect x position

        collided_tile: Tile | None = level.detect_tile_collision(self.rect)
        if collided_tile:
            if self.physics.velocity.x > 0:  # Moving right
                self.position.x = collided_tile.rect.left - self.rect.width
            elif self.physics.velocity.x < 0:  # Moving left
                self.position.x = collided_tile.rect.right
            self.physics.velocity.x = 0
        self.rect.x = int(self.position.x)  # Update rect after collision resolution

        # Move in y direction
        self.position.y += self.physics.velocity.y * Time.fixed_delta_time
        self.rect.y = int(self.position.y)  # Update rect y position

        collided_tile = level.detect_tile_collision(self.rect)
        if collided_tile:
            if self.physics.velocity.y > 0:  # Moving down
                self.position.y = collided_tile.rect.top - self.rect.height
            elif self.physics.velocity.y < 0:  # Moving up
                self.position.y = collided_tile.rect.bottom
            self.physics.velocity.y = 0
            self.physics.velocity.x -= self.physics.velocity.x/2
        self.rect.y = int(self.position.y)  # Update rect after collision resolution


    def verify_screen_bounds(self) -> None:
        if self.position.x < 0:
            self.position.x = 0
            self.physics.velocity.x = 0
        if self.position.x > Config.SCREEN_WIDTH - self.rect.width:
            self.position.x = Config.SCREEN_WIDTH - self.rect.width
            self.physics.velocity.x = 0
        if self.position.y < 0:
            self.position.y = 0
            self.physics.velocity.y = 0
        if self.position.y > Config.SCREEN_HEIGHT - self.rect.height:
            self.position.y = Config.SCREEN_HEIGHT - self.rect.height
            self.physics.velocity.y = 0
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def is_jumping(self, level: GameMap) -> bool:
        collided_tile: Tile = level.detect_tile_collision(pygame.rect.Rect(self.rect.x, self.rect.y + 2, self.rect.width, self.rect.height))
        if collided_tile and collided_tile.rect.top < self.rect.bottom+2 and collided_tile.rect.top > self.rect.bottom-2:
            return False
        return True