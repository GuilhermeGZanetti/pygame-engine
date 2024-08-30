from abc import ABC, abstractmethod

class BaseScene():
    @abstractmethod
    def handle_events(self, events):
        """ handle pygame events """

    @abstractmethod
    def update_states(self):
        """ Update game state """
       
    @abstractmethod
    def draw(self, tela):
        """ draw the scene """

    