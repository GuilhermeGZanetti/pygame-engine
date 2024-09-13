from pygame import Rect, Surface
import pygame
from animator import Animator
from config import Config
from src.tilemap import GameMap, Tile
from src.utils import load_img
from src.vector2d import Vector2D
import time


class Frog:
    def __init__(self, run_sprite_sheet, idle_sprite_sheet, px: int, py: int, size: float = 1) -> None:
        self.last_time: float = time.time()
        self.delta_time: float = 0
        self.run_sprite_sheet: Surface = load_img(run_sprite_sheet)
        self.idle_sprite_sheet: Surface = load_img(idle_sprite_sheet)
        self.rect: Rect = pygame.rect.Rect(px, py, Config.FROG_WIDTH * size, Config.FROG_HEIGHT * size)
        self.velocity: Vector2D = Vector2D(0, 0)
        self.max_velocity = Config.FROG_SPEED
        self.position: Vector2D = Vector2D(px, py)

        # Animation
        self.run_frames = self.init_sprite_sheet(self.run_sprite_sheet, 7, size)
        self.idle_frames = self.init_sprite_sheet(self.idle_sprite_sheet, 8, size)
        self.jump_frames = self.init_sprite_sheet(self.run_sprite_sheet, 1, size, offset=3)

        self.animator = Animator(run_frames=self.run_frames, idle_frames=self.idle_frames, jump_frames=self.jump_frames, starting_animation="idle")


    def update(self, screen: Surface, level: GameMap) -> None:
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()

        self.handle_input(level)

        self.apply_physics(level=level)
        self.move_and_apply_collisions(level=level)
        self.verify_screen_bounds()

        self.animate(level=level)
        self.draw(screen)
    

    #### INPUT HANDLING ####

    def handle_input(self, level: GameMap) -> None:
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.command_move(right=False)
        elif pressed_keys[pygame.K_RIGHT]:
            self.command_move(right=True)
        else:
            self.is_moving = False

        if pressed_keys[pygame.K_UP]:
            if not self.is_jumping(level):
                self.start_jump()
    
    def command_move(self, right: bool):
        flag_sign = 1 if right else -1
        velocity = self.velocity.x + flag_sign * Config.FROG_ACCELERATION * self.delta_time
        if abs(velocity) < self.max_velocity:
            self.velocity.x = velocity
        self.is_moving = True

            
    def start_jump(self) -> None:
        self.velocity.y = -Config.JUMP_SPEED


    #### ANIMATION ####
    def animate(self, level: GameMap) -> None:
        self.animator.update(
            velocity=self.velocity, 
            is_jumping=self.is_jumping(level), 
            delta_time=self.delta_time, 
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
        screen.blit(self.animator.current_image, self.rect)
        # Draw red rectangle for debug
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)




    #### PHYSICS ####

    def apply_physics(self, level: GameMap) -> None:
        fixed_drag = Config.FIXED_DRAG if self.is_jumping(level) else Config.FIXED_DRAG * 50
        if self.velocity.x > 0:
            self.velocity.x -= (Config.DRAG * (self.velocity.x)/2 + fixed_drag) * self.delta_time
            if self.velocity.x < 0:
                self.velocity.x = 0
        elif self.velocity.x < 0:
            self.velocity.x += (Config.DRAG * (self.velocity.x)/2 + fixed_drag) * self.delta_time
            if self.velocity.x > 0:
                self.velocity.x = 0
        
        if self.velocity.y > 0:
            self.velocity.y -= (Config.DRAG * (self.velocity.y)/2 + fixed_drag) * self.delta_time
            if self.velocity.y < 0:
                self.velocity.y = 0
        elif self.velocity.y < 0:
            self.velocity.y += (Config.DRAG * (self.velocity.y)/2 + fixed_drag) * self.delta_time
            if self.velocity.y > 0:
                self.velocity.y = 0
        
        self.velocity.y += Config.GRAVITY * self.delta_time

    def move_and_apply_collisions(self, level: GameMap) -> None:
        # Move in x direction
        self.position.x += self.velocity.x * self.delta_time
        self.rect.x = int(self.position.x)  # Update rect x position

        collided_tile: Tile | None = level.detect_tile_collision(self.rect)
        if collided_tile:
            if self.velocity.x > 0:  # Moving right
                self.position.x = collided_tile.rect.left - self.rect.width
            elif self.velocity.x < 0:  # Moving left
                self.position.x = collided_tile.rect.right
            self.velocity.x = 0
        self.rect.x = int(self.position.x)  # Update rect after collision resolution

        # Move in y direction
        self.position.y += self.velocity.y * self.delta_time
        self.rect.y = int(self.position.y)  # Update rect y position

        collided_tile = level.detect_tile_collision(self.rect)
        if collided_tile:
            if self.velocity.y > 0:  # Moving down
                self.position.y = collided_tile.rect.top - self.rect.height
            elif self.velocity.y < 0:  # Moving up
                self.position.y = collided_tile.rect.bottom
            self.velocity.y = 0
            self.velocity.x -= self.velocity.x/2
        self.rect.y = int(self.position.y)  # Update rect after collision resolution


    def verify_screen_bounds(self) -> None:
        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x = 0
        if self.position.x > Config.SCREEN_WIDTH - self.rect.width:
            self.position.x = Config.SCREEN_WIDTH - self.rect.width
            self.velocity.x = 0
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y = 0
        if self.position.y > Config.SCREEN_HEIGHT - self.rect.height:
            self.position.y = Config.SCREEN_HEIGHT - self.rect.height
            self.velocity.y = 0
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)

    def is_jumping(self, level: GameMap) -> bool:
        collided_tile: Tile = level.detect_tile_collision(pygame.rect.Rect(self.rect.x, self.rect.y + 2, self.rect.width, self.rect.height))
        if collided_tile and collided_tile.rect.top < self.rect.bottom+2 and collided_tile.rect.top > self.rect.bottom-2:
            return False
        return True