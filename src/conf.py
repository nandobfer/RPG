import pygame, random, init

# Background
background = pygame.image.load('background.jpg').convert()
background = pygame.transform.scale(background, init.resolution)
