import pygame
import sys
from audio_manager import AudioManager
from frog import Frog
from src.scene import BaseScene
from src.tilemap import GameMap, TileList
from src.utils import load_img
from config import Config

class GameScene(BaseScene):
    def __init__(self, screen: pygame.surface.Surface, audio_manager: AudioManager = AudioManager()):
        super().__init__(screen=screen)
        
        self.font = pygame.font.SysFont(None, 48)
        self.audio_manager = audio_manager



    def handle_events(self):
        """ handle pygame events """
        sair = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r]:
            self.exit_scene = True
            self.next_scene = GameScene(screen=self.screen, level="fase1.json")

        # termina o jogo se acabar o tempo ou se a pessoa clicar
        # no botao de sair
        if (sair):
            pygame.quit()
            sys.exit(0)
       
    def draw(self):
        """ draw the scene """
        # preenche a tela com branco
        self.screen.fill((0, 0, 0))
        pygame.display.flip()

