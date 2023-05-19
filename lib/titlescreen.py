import pygame
import sys
from settings import *
from models import Player, session  # Import Player and session from models

def run_title_screen():
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Secret of the Sheep")

    font = pygame.font.Font(None, 36)

    black = (0, 0, 0)
    white = (255, 255, 255)

    input_box_width = 200
    input_box_height = 40
    input_box_x = (screen_width - input_box_width) // 2
    input_box_y = (screen_height - input_box_height) // 2

    button_width = 100
    button_height = 40
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height + input_box_height) // 2 + 20

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

        screen.fill(white)

        #Input box
        pygame.draw.rect(screen, black, (input_box_x, input_box_y, input_box_width, input_box_height))
        if is_typing:
            pygame.draw.rect(screen, white, (input_box_x + 2, input_box_y + 2, input_box_width - 4, input_box_height - 4))
        username_text = font.render(username, True, black) 
        screen.blit(username_text, (input_box_x + 10, input_box_y + 10))

        #Start button
        pygame.draw.rect(screen, black, (button_x, button_y, button_width, button_height))
        start_text = font.render("Start", True, white)
        screen.blit(start_text, (button_x + 25, button_y + 10))

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

