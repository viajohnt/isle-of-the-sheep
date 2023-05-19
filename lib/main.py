import pygame
import sys
from settings import *
from level import Level
from game_data import level1_1
import titlescreen
import gameover
from models import session, Score, Player

def save_score(score, username):
    player = session.query(Player).filter_by(username=username).first()
    if player:
        score_entry = Score(score=score, player_id=player.id)
        session.add(score_entry)
        session.commit()
    else:
        print(f"Player with username '{username}' not found.")

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
username = titlescreen.run_title_screen()
level = Level(level1_1, screen, username=username)
game_over = False
restart_game = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        level.run()
        if level.player.sprite.rect.bottom > screen_height:  # Check if player falls below the map
            save_score(level.player.sprite.score, username.username)
            game_over = True 

    else:
        if gameover.show_game_over_screen(screen, clock, level.player.sprite.score):
            level = Level(level1_1, screen, username=username)
            game_over = False
            restart_game = True
        else:
            break
        
    if restart_game:
        restart_game = False
        continue

    pygame.display.update()
    clock.tick(60)
