import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self._jump_sound = pygame.mixer.Sound("sound/jump.mp3")
        self._song = pygame.mixer.music.load("sound/song.mp3")

        self._lingua1 = pygame.mixer.Sound("sound/lingua1.wav")
        self._lingua2 = pygame.mixer.Sound("sound/lingua2.wav")
        self._lingua3 = pygame.mixer.Sound("sound/lingua3.wav")

    def play_song(self):
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

    def play_jump_sound(self):
        self._jump_sound.play()

    def play_throw_tongue(self):
        self._lingua1.play()

    def play_retrieve_tongue(self):
        self._lingua2.play()
    
    def play_hit_tongue(self):
        self._lingua3.play()


