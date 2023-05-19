import pygame
import sys
from settings import *
from models import Player, session 

def run_title_screen(screen, clock, font):
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Isle of the Sheep")

    grey = (50, 50, 50)
    white = (255, 255, 255)

    input_box_width = 250
    input_box_height = 80
    input_box_x = (screen_width - input_box_width) // 2  
    input_box_y = (screen_height - input_box_height) // 2 

    button_width = 140
    button_height = 80
    button_x = (screen_width - button_width) // 2 
    button_y = (screen_height + input_box_height) // 2 + 120

    username = ""
    is_typing = False
    start_clicked = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    is_typing = False
                    start_clicked = True
                else:
                    username += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if input_box_x <= mouse_pos[0] <= input_box_x + input_box_width and \
                    input_box_y <= mouse_pos[1] <= input_box_y + input_box_height:
                        is_typing = True
                    elif button_x <= mouse_pos[0] <= button_x + button_width and \
                        button_y <= mouse_pos[1] <= button_y + button_height:
                        start_clicked = True

        screen.fill(grey)

        welcome_text = font.render("Welcome to Isle of the Sheep", True, white)
        welcome_text_rect = welcome_text.get_rect(center=(screen_width // 2, input_box_y - 210))
        screen.blit(welcome_text, welcome_text_rect)

        instruction_text = font.render("enter username:", True, white)
        instruction_text_rect = instruction_text.get_rect(center=(screen_width // 2, input_box_y - 30))
        screen.blit(instruction_text, instruction_text_rect)

        pygame.draw.rect(screen, white, (input_box_x, input_box_y, input_box_width, input_box_height))
        if is_typing:
            pygame.draw.rect(screen, white, (input_box_x + 2, input_box_y + 2, input_box_width - 4, input_box_height - 4))
        username_text = font.render(username, True, 'black')
        screen.blit(username_text, (input_box_x + 10, input_box_y + 20))

        pygame.draw.rect(screen, 'green', (button_x, button_y, button_width, button_height))
        start_text = font.render("Start", True, white)
        start_text_rect = start_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(start_text, start_text_rect)

        pygame.display.flip()

        if start_clicked:
            player = get_player(username)
            break

    return player


def get_player(username):
    player = session.query(Player).filter_by(username=username).first()
    if player is None:
        player = Player(username=username)
        session.add(player)
        session.commit()
    return player

