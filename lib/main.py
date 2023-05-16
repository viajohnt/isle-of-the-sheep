import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("lib/assets/images/characters/zarya-sprite.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (350, 250))
        self.rect = self.image.get_rect(midbottom=(200, 780))
        self.gravity = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        off_screen_allowance = 75
        if keys[pygame.K_SPACE] and self.rect.bottom >= 780:
            self.gravity = -20
        elif keys[pygame.K_d] and self.rect.right < screen.get_width() + off_screen_allowance:
            self.rect.x += 15
        elif keys[pygame.K_a] and self.rect.left > -off_screen_allowance:
            self.rect.x -= 15


    def get_collision_rect(self):
        return pygame.Rect(self.rect.left + 80, self.rect.top + 30, self.rect.width - 160, self.rect.height - 60)
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 780:
            self.rect.bottom = 780
        elif self.rect.left <= 0: 
            self.rect.left = 0

    def update(self):
        self.apply_gravity()
        self.player_input()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == 'flappy':
            self.image = pygame.image.load("lib/assets/images/characters/flappy-bird.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.image = pygame.transform.flip(self.image, True, False)
            y_pos = 550
        else:
            self.image = pygame.image.load("lib/assets/images/characters/derpy-bulbasaur.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (250, 250))
            self.image = pygame.transform.flip(self.image, True, False)
            y_pos = 820
        
        self.rect = self.image.get_rect(midbottom=(1400, y_pos))

    def get_collision_rect(self):
        if self.type == 'flappy':
            return pygame.Rect(self.rect.left + 10, self.rect.top + 10, self.rect.width - 10, self.rect.height - 20)
        else: 
            return pygame.Rect(self.rect.left + 75, self.rect.top + 75, self.rect.width - 140, self.rect.height - 150)

    def update(self):
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f"Score: {current_time}", False, 'White')
    score_rect = score_surf.get_rect(center=(700, 100))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_boxes(sprite1, sprite2):
    return sprite1.get_collision_rect().colliderect(sprite2.get_collision_rect())

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, collided=collision_boxes):
        obstacle_group.empty()
        return False
    else: 
        return True
    
pygame.init()
screen = pygame.display.set_mode((1400, 850))
pygame.display.set_caption("DerpyMon")
clock = pygame.time.Clock()
background_surf = pygame.image.load("lib/assets/images/background/background1.jpeg").convert_alpha()
text_font = pygame.font.Font('lib/assets/fonts/Pixeltype.ttf', 70)
game_active = True
start_time = 0
score = 0 

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

player_stand = pygame.image.load("lib/assets/images/characters/zarya-sprite.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (350, 250))
player_stand_rect = player_stand.get_rect(center=(700, 400))

game_name = text_font.render("DerpyMon", False, 'White')
game_name_rect = game_name.get_rect(center=(700, 100))

game_message =  text_font.render("Press SPACE to play", False, 'White')
game_message_rect = game_message.get_rect(center=(700, 700))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle = Obstacle('bulbasaur')
                else:
                    obstacle = Obstacle('flappy')
                obstacle_group.add(obstacle)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(background_surf, (0, -200))
        score = display_score()

        player.draw(screen)
        player.update()

        pygame.draw.rect(screen, (255, 0, 0), player.sprite.get_collision_rect(), 2)

        #Obstacle movement
        obstacle_group.draw(screen)
        obstacle_group.update()
        for obstacle in obstacle_group:
            pygame.draw.rect(screen, (255, 0, 0), obstacle.get_collision_rect(), 2)
        game_active = collision_sprite()
    else:
        obstacle_group.empty()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = text_font.render(f"Your score was: {score}", False, 'White')
        score_message_rect = score_message.get_rect(center=(700, 600))
        screen.blit(game_name, game_name_rect)

        if score == 0: 
            screen.blit(game_message, game_message_rect)
        else: 
            screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)

