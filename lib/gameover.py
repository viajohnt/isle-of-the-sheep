import pygame
import sys
from settings import *

def show_game_over_screen(screen, clock, score, font):
    pygame.init()

    white = (255, 255, 255)
    grey = (50, 50, 50)

    button_size = (240, 120)
    button_x = (screen_width - button_size[0]) // 2
    button_y = (screen_height // 2) + 50

    play_again_button = pygame.Rect(button_x, button_y, button_size[0], button_size[1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        screen.fill(grey)
        score_text = font.render("Your score: " + str(score), True, white)
        score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 170))
        screen.blit(score_text, score_text_rect)

        pygame.draw.ellipse(screen, 'pink', play_again_button)
        play_again_text = font.render("Play Again", True, white)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)

        pygame.display.flip()

        clock.tick(60)
