import pygame
import sys
from src.scene import BaseScene
from src.tilemap import GameMap, TileList
from src.utils import load_img
from config import Config

class GameScene(BaseScene):
    def __init__(self, screen: pygame.surface.Surface, level: str = "fase0.json"):
        super().__init__(screen=screen)
        self.load_images()
        tile_list = TileList("sprites/nature_elements/nature_tileset.png", Config.TILE_SIZE, Config.TILE_SIZE)
        self._level = GameMap(f"maps/{level}", tile_list=tile_list, scale=Config.SCALE)
        

        self.font = pygame.font.SysFont(None, 48)


    def handle_events(self):
        """ handle pygame events """
        sair = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True

        # termina o jogo se acabar o tempo ou se a pessoa clicar
        # no botao de sair
        if (sair):
            pygame.quit()
            sys.exit(0)

        teclas_pressionadas = pygame.key.get_pressed()

    def update_states(self):
        """ Update game state """
       
    def draw(self):
        """ draw the scene """
        # preenche a tela com branco
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.img_forest_background, (0,0))
        self._level.draw(self.screen)
        pygame.display.flip()


    def load_images(self):
        self.img_forest_background = load_img(Config.BACKGROUND_PATH, 
                                              (Config.SCREEN_WIDTH, Config.SCREEN_WIDTH*Config.BACKGROUND_Y/Config.BACKGROUND_X))

