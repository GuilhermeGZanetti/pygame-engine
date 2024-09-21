import pygame
import sys
from audio_manager import AudioManager
from frog import Frog
from scenes.GameScene import GameScene
from src.scene import BaseScene
from src.tilemap import GameMap, TileList
from src.utils import load_img
from config import Config
from story_player import StoryPlayer

class InitialScene(BaseScene):
    def __init__(self, screen: pygame.surface.Surface, audio_manager: AudioManager = AudioManager()):
        super().__init__(screen=screen)
        self.audio_manager = audio_manager

        self.image1 = load_img("sprites/historia_inicio_1.png", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.image2 = load_img("sprites/historia_inicio_2.png", (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))

        story_texts = [
            """Uma pequena pedra jaz no fundo de um rio no meio da floresta Amazônica.
A princípio, apenas uma pedra comum: arredondada após os anos em contato com a água.
Entretanto, repentinamente ela começa a brilhar em um tom de azul,
assustando os animais que estavam por perto.
""",

            """A pedra, como um passe de mágica, se transforma em um pequeno sapinho azul.
Ele acorda confuso, exalando uma grande energia natural e mágica, até que percebe
um espírito da natureza surgindo do nada e tomando uma forma semelhante à sua.
 
O espírito explica que o sapinho é um amuleto Muiraquitã, um pingente em formato de sapo
que tem o dever de proteger uma índia Tapajó dos espíritos malignos. Em seu caso, o sapinho
deve procurar por Kauany, uma jovem Tapajó que é abençoada pelos espíritos.
 
Ajude o muiraquitã a percorrer a floresta até encontrar sua protegida!
""",

            """Instruções:
 
Ande para os lados com as setas <- e -> do teclado.
 
Pule com Z.
 
Jogue e solte sua língua na direção das setas do teclado com X.
 
Com a língua extendida, aperte a seta para cima e para baixo para aumentar e diminuir o comprimento da língua.
"""
        ]

        self.story_player: StoryPlayer = StoryPlayer(audio_manager=audio_manager, background_images=[self.image1, self.image2, self.image2], story_texts=story_texts)



    def handle_events(self):
        """ handle pygame events """
        sair = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if self.story_player.next():
                        self.exit_scene = True
                        self.next_scene = GameScene(screen=self.screen, level=1, audio_manager=self.audio_manager)
                        

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

