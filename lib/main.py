import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1400, 850))
pygame.display.set_caption("DerpyMon")
clock = pygame.time.Clock()

test_font = pygame.font.Font('lib/assets/fonts/Pixeltype.ttf', 70)

background_surface = pygame.image.load("lib/assets/images/background/background1.jpeg")
text_surface = test_font.render("DerpyMon: Adventure of the Derp", False, 'White')


bulbasaur = pygame.image.load("lib/assets/images/characters/derpy-bulbasaur.png")
smaller_bulbasaur = pygame.transform.scale(bulbasaur, (250, 250))
bulbs_x_position = 100


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(background_surface, (0,-200))
    screen.blit(text_surface, (400,100))
    bulbs_x_position += 1
    screen.blit(smaller_bulbasaur, (bulbs_x_position,550))

    pygame.display.update()
    clock.tick(60)