import pygame
import sys
from settings import *
from level import Level
from game_data import level1_1
import titlescreen

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Call the title screen and get the username
username = titlescreen.run_title_screen()

# Create the level instance after the title screen is done
level = Level(level1_1, screen, username=username)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    level.run()

    pygame.display.update()
    clock.tick(60)
