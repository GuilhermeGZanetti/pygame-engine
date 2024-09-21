import pygame
import sys
from audio_manager import AudioManager
from frog import Frog
from src.scene import BaseScene
from src.tilemap import GameMap, TileList
from src.utils import load_img
from config import Config
from story_player import StoryPlayer

class FinalScene(BaseScene):
    def __init__(self, screen: pygame.surface.Surface, audio_manager: AudioManager = AudioManager()):
        super().__init__(screen=screen)
        self.audio_manager = audio_manager

        self.image1 = load_img("sprites/historia_final_1.png", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.image2 = load_img("sprites/historia_final_2.jpg", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

        story_texts = [
            """Após sua grande jornada e muitos desafios, o sapinho Muiraquitã avista uma vila Tapajó ao longe.
Ao se aproximar, ele sente que sua protegida está mais próxima que nunca, enchendo-se de alegria.
Parece que finalmente poderá cumprir o seu papel!""",

            """Guiado por seus instintos, o sapinho chega aos pés de Kauany, uma jovem Tapajó.
O reconhecimento é mútuo, tanto o sapo quanto a moça sentem a conexão entre eles e
sabem que foram unidos pelo destino, que nada irá separá-los. O sapo então pula no pescoço
da jovem e se transforma, com um intenso brilho azul, em um pequeno pingente muiraquitã.
 
Agora o sapinho está tranquilo, daqui ele seguirá protegendo Kauany e sua tribo, sabendo que
está apenas a um pulo de distância de sua protegida.
 
OBRIGADO POR AJUDAR O SAPINHO!
"""
        ]

        self.story_player: StoryPlayer = StoryPlayer(audio_manager=audio_manager, background_images=[self.image1, self.image2], story_texts=story_texts)



    def handle_events(self):
        """ handle pygame events """
        sair = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.story_player.next():
                        sair = True
                        

        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[pygame.K_r]:
        #     self.exit_scene = True
        #     self.next_scene = GameScene(screen=self.screen, level="fase1.json")

        # termina o jogo se acabar o tempo ou se a pessoa clicar
        # no botao de sair
        if (sair):
            pygame.quit()
            sys.exit(0)
       
    def draw(self):
        """ draw the scene """
        # preenche a tela com branco
        self.screen.fill((0, 0, 0))
        self.story_player.update(self.screen)
        pygame.display.flip()

