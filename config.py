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
    FROG_SPRITESHEET_IDLE = "sprites/frog_anim/BlueBlue/ToxicFrogBlueBlue_Idle.png"
    FROG_WIDTH = 24
    FROG_HEIGHT = 24
    FROG_SCALE = 2

    #ANIMATION
    ANIMATION_SPEED=0.1

    #Gameplay Frog
    GRAVITY = 700
    DRAG = 1/10
    FIXED_DRAG = 5
    FROG_SPEED = 100
    FROG_ACCELERATION = 700
    FROG_AIR_FORCE = 200
    JUMP_SPEED = 500
    TONGUE_CONTROL = 50
    TONGUE_ELASTIC_CONSTANT = 100

    MAX_TONGUE_LENGTH = 300
    TONGUE_VELOCITY = 1000