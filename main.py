import pygame
from audio_manager import AudioManager
from src.scene import BaseScene
from scenes.GameScene import GameScene
from config import Config


if __name__ == "__main__":
    pygame.init()
# create a surface on screen that has the size of 700 x 200
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    audio_manager = AudioManager()
    audio_manager.play_song()
    current_scene: BaseScene = GameScene(screen=screen, level=2, audio_manager=audio_manager)
    while True:
        current_scene = current_scene.execute()
