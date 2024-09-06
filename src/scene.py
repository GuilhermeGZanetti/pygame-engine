from abc import ABC, abstractmethod

import pygame

class BaseScene():
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.exit_scene: bool = False
        self.next_scene: BaseScene = None
        

    @abstractmethod
    def handle_events(self):
        """ handle pygame events """

    @abstractmethod
    def update_states(self):
        """ Update game state """
       
    @abstractmethod
    def draw(self):
        """ draw the scene """

    def execute(self):
        """ execute scene """
        while True:
            self.handle_events()
            self.update_states()
            self.draw()
            if self.exit_scene:
                break
        return self.next_scene


    