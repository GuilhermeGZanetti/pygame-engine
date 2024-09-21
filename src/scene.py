from abc import ABC, abstractmethod

import pygame

from src.game_time import Time

class BaseScene():
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.exit_scene: bool = False
        self.next_scene: BaseScene = None
        

    @abstractmethod
    def handle_events(self):
        """ handle pygame events """

    @abstractmethod
    def fixed_update(self):
        """ Update game state """
       
    @abstractmethod
    def draw(self):
        """ draw the scene """

    def _physics_step(self):
        while Time.has_physics_time():
            self.fixed_update()
            Time.fixed_update()

    def execute(self):
        """ execute scene """
        while True:
            Time.update()
            self.handle_events()
            self._physics_step()
            self.draw()
            Time.wait_fps()
            if self.exit_scene:
                break
        return self.next_scene


    