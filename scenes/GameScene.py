import pygame
import sys
from audio_manager import AudioManager
from frog import Frog
from scenes.FinalScene import FinalScene
from src.scene import BaseScene
from src.tilemap import GameMap, TileList
from src.utils import load_img
from config import Config
from src.vector2d import Vector2D

class GameScene(BaseScene):
    def __init__(self, screen: pygame.surface.Surface, level: int = 1, audio_manager: AudioManager = AudioManager()):
        super().__init__(screen=screen)
        self.load_images()
        self._level_number = level
        tile_list = TileList("sprites/nature_elements/nature_tileset.png", Config.TILE_SIZE, Config.TILE_SIZE)
        self._level = GameMap(f"maps/fase{level}.json", tile_list=tile_list, scale=Config.SCALE)
        self.player = Frog(run_sprite_sheet=Config.FROG_SPRITESHEET_RUN, 
                           idle_sprite_sheet=Config.FROG_SPRITESHEET_IDLE,
                           px=self._level.player_initial_position()[0], py=self._level.player_initial_position()[1],
                           size=Config.FROG_SCALE, audio_manager=audio_manager)
        
        self.font = pygame.font.SysFont(None, 48)
        self.audio_manager = audio_manager


    def handle_events(self):
        """ handle pygame events """
        sair = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r]: # Apertar R para roubar e chegar perto das OCAs (para testes)
            self.player.position = Vector2D(100, 80)

        # termina o jogo se acabar o tempo ou se a pessoa clicar
        # no botao de sair
        if (sair):
            pygame.quit()
            sys.exit(0)

    def fixed_update(self):
        """ Update game state """
        self.player.fixed_update(self._level)
        if self._level.detect_goal_collision(self.player.rect):
            self.exit_scene = True
            next_level = self._level_number+1
            if next_level > Config.NUMBER_OF_LEVELS:
                self.next_scene = FinalScene(screen=self.screen, audio_manager=self.audio_manager)
            else:
                self.next_scene = GameScene(screen=self.screen, level=next_level, audio_manager=self.audio_manager)
        if self.player.is_dead():
            self.exit_scene = True
            self.next_scene = GameScene(screen=self.screen, level=self._level_number, audio_manager=self.audio_manager)
       
    def draw(self):
        """ draw the scene """
        # preenche a tela com branco
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img_forest_background, (0,0))
        self._level.draw(self.screen)
        self.player.update(self.screen, self._level)
        pygame.display.flip()


    def load_images(self):
        self.img_forest_background = load_img(Config.BACKGROUND_PATH, 
                                              (Config.SCREEN_WIDTH, Config.SCREEN_WIDTH*Config.BACKGROUND_Y/Config.BACKGROUND_X))

