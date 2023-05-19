import pygame
import sys
from settings import *
from level import Level
from game_data import level1_1, level1_2  
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
        session.commit() 
    else:
        print(f"Player with username '{username}' not found.")


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Load the custom font
font_path = "lib/assets/fonts/Pixeltype.ttf"
font_size = 72
font = pygame.font.Font(font_path, font_size)

username = titlescreen.run_title_screen(screen, clock, font) 
level_data = [level1_1, level1_2]  
current_level_index = 0
level = Level(level_data[current_level_index], screen, username=username)
game_over = False
restart_game = False
attempts = 0  
cumulative_score = 0  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        level.run()

        if level.player.sprite.rect.bottom > screen_height:  # Check if player falls below the map
            save_score(level.player.sprite.score + cumulative_score, username.username)  
            attempts += 1  
            save_attempts(attempts, username.username)
            game_over = True

        if level.player.sprite.health <= 0:  # Check if player's health reaches 0 or below
            save_score(level.player.sprite.score + cumulative_score, username.username) 
            attempts += 1  
            save_attempts(attempts, username.username)
            game_over = True

        if pygame.sprite.spritecollide(level.player.sprite, level.goal, False):  # Check if player touches the hat
            cumulative_score += level.player.sprite.score 
            save_score(level.player.sprite.score + cumulative_score, username.username)  
            attempts += 1  
            if current_level_index < len(level_data) - 1:  # Check if there is another level
                current_level_index += 1 
                level = Level(level_data[current_level_index], screen, username=username)
                level.player.sprite.score = cumulative_score  
                game_over = False
            else:
                current_level_index = 0  
                game_over = True
                

    else:
        if gameover.show_game_over_screen(screen, clock, level.player.sprite.score + cumulative_score, font):  
            current_level_index = 0 
            cumulative_score = 0 
            level = Level(level_data[current_level_index], screen, username=username)
            game_over = False
            restart_game = True
            attempts = 0  
        else:
            break

    if restart_game:
        current_level_index = 0  
        cumulative_score = 0  
        level = Level(level_data[current_level_index], screen, username=username)
        level.player.sprite.score = cumulative_score 
        game_over = False
        restart_game = False
        attempts = 0  

    pygame.display.update()
    clock.tick(60)
