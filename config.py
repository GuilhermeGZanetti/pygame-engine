from src.base_config import BaseConfig

class Config(BaseConfig):
    SCREEN_WIDTH = 1422
    SCREEN_HEIGHT = 800
    TILE_SIZE = 16
    SCALE = 2

    #Images
    BACKGROUND_PATH = "sprites/nature_elements/forest_background.png"
    BACKGROUND_X = 480
    BACKGROUND_Y = 270
    FROG_SPRITESHEET_RUN = "sprites/frog_anim/BlueBlue/ToxicFrogBlueBlue_Hop.png"
    FROG_WIDTH = 24
    FROG_HEIGHT = 24
    FROG_SCALE = 2

    #Gameplay Frog
    GRAVITY = 500
    DRAG = 1/100
    FIXED_DRAG = 100
    FROG_SPEED = 100
    JUMP_SPEED = 600