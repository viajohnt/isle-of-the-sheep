import pygame
import sys
from settings import *

def show_game_over_screen(screen, clock, score):
    pygame.init()

    font = pygame.font.Font(None, 36)
    white = (255, 255, 255)

    button_width = 140
    button_height = 40
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height // 2) + 50

    play_again_button = pygame.Rect(button_x, button_y, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    return True  # Signal to restart the game

        #Game over screen
        screen.fill(white)
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(score_text, score_text_rect)

        #"Play Again" button
        pygame.draw.rect(screen, (0, 255, 0), play_again_button)
        play_again_text = font.render("Play Again", True, (0, 0, 0))
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)

        pygame.display.flip()

        clock.tick(60)
