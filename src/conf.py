import pygame, random, init

# Player
player_img = "assets/player/man.png"
IMAGE_INTERVAL = 4000  # This is the amount of miliseconds that will represent the time to change the picture.

# Fonts
small_text = pygame.font.Font('assets/cthulus_calling.otf', int(0.02 * init.resolution[0]))
text = pygame.font.Font('assets/cthulus_calling.otf', int(0.04 * init.resolution[0]))
big_text = pygame.font.Font('assets/cthulus_calling.otf', int(0.08 * init.resolution[0]))

