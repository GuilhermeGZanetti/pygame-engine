from src.base_config import BaseConfig

class Config(BaseConfig):
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    TILE_SIZE = 16
    SCALE = 2

    #Images
    BACKGROUND_PATH = "sprites/nature_elements/forest_background.png"
    BACKGROUND_X = 480
    BACKGROUND_Y = 270
    FROG_SPRITESHEET_RUN = "sprites/frog_anim/ToxicFrogGreenBlue_Hop.png"
    FROG_WIDTH = 64
    FROG_HEIGHT = 64