import pygame
import sys
from settings import *
from level import Level
from game_data import level1_1
import titlescreen
import gameover
from models import session, Score, Player, Attempts

def save_score(score, username):
    player = session.query(Player).filter_by(username=username).first()
    if player:
        score_entry = Score(score=score, player_id=player.id)
        session.add(score_entry)
        session.commit()
    else:
        print(f"Player with username '{username}' not found.")

def save_attempts(attempts_count, username):
    player = session.query(Player).filter_by(username=username).first()
    if player:
        attempts_entry = Attempts(count=attempts_count, player_id=player.id)
        session.add(attempts_entry)
        session.commit()  # Commit the session after adding the attempts entry
    else:
        print(f"Player with username '{username}' not found.")


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
username = titlescreen.run_title_screen()
level = Level(level1_1, screen, username=username)
game_over = False
restart_game = False
attempts = 0  # Initialize attempts counter to 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        level.run()

        if level.player.sprite.rect.bottom > screen_height:  # Check if player falls below the map
            save_score(level.player.sprite.score, username.username)
            attempts += 1  # Increment attempts counter
            save_attempts(attempts, username.username)
            game_over = True

        if level.player.sprite.health <= 0:  # Check if player's health reaches 0 or below
            save_score(level.player.sprite.score, username.username)
            attempts += 1  # Increment attempts counter
            save_attempts(attempts, username.username)
            game_over = True

        if pygame.sprite.spritecollide(level.player.sprite, level.goal, False):  # Check if player touches the hat
            save_score(level.player.sprite.score, username.username)
            attempts += 1  # Increment attempts counter
            save_attempts(attempts, username.username)
            game_over = True

    else:
        if gameover.show_game_over_screen(screen, clock, level.player.sprite.score):
            level = Level(level1_1, screen, username=username)
            game_over = False
            restart_game = True
            attempts = 0  # Reset attempts counter
        else:
            break
        
    if restart_game:
        restart_game = False
        continue

    pygame.display.update()
    clock.tick(60)
