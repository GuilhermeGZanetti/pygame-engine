import pygame
from pygame.surface import Surface

from config import Config
import time

from src.vector2d import Vector2D

class Animator:
    def __init__(self, idle_frames: list[Surface], run_frames: list[Surface], jump_frames: list[Surface], starting_animation: str = "idle") -> None:
        self.facing_right = True
        self.frame_index = 0
        self.current_animation = starting_animation
        self.animation_speed = Config.ANIMATION_SPEED  # Adjust the speed of the animation
        self.time_since_last_frame = 0

        self.idle_frames = idle_frames
        self.run_frames = run_frames
        self.jump_frames = jump_frames

        self.frames = idle_frames

        # Set the current image
        self.current_image: Surface = self.run_frames[0]

    def update(self, velocity: Vector2D, is_jumping: bool, delta_time: float, is_running: bool) -> None:
        if is_jumping:
            if self.current_animation != "jump":
                self.current_animation = "jump"
                self.frame_index = 0
                self.frames = self.jump_frames
                self.time_since_last_frame = 1
        elif is_running: 
            if self.current_animation != "run":
                self.current_animation = "run"
                self.frame_index = 0
                self.frames = self.run_frames
                self.time_since_last_frame = 1
        else:
            if self.current_animation != "idle":
                self.current_animation = "idle"
                self.frame_index = 0
                self.frames = self.idle_frames
                self.time_since_last_frame = 1

        # Flip the image if moving left/right
        if velocity.x < -0.5 and self.facing_right:
            self.facing_right = False
        elif velocity.x > 0.5 and not self.facing_right:
            self.facing_right = True            

        self.time_since_last_frame += delta_time
        if self.time_since_last_frame > self.animation_speed:
            # Update the frame index
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.current_image = self.frames[self.frame_index]
            if not self.facing_right:
                self.current_image = pygame.transform.flip(self.current_image, True, False)
            self.time_since_last_frame = 0

        