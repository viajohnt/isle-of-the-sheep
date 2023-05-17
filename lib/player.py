import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['Jump'][self.frame_index]
        self.rect = self.image.get_rect(topleft= pos)
        self.hit_box = self.rect
        self.display_surface = display_surface
        
        #Player Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

    def import_character_assets(self):
        character_path = 'lib/assets/BlueWizard/'
        self.animations = {'Idle': [], 'Walk': [], 'Jump': [], 'Dash2': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations['Jump']
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        
        scale_factor = 0.25  # reduce the image size to 20%
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(topleft=self.rect.topleft)  # Update the rect

        hit_box_scale_factor = .5  # reduce the hit box size to 50% of the scaled image
        self.hit_box = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * hit_box_scale_factor), int(self.rect.height * hit_box_scale_factor))
        self.hit_box.center = self.rect.center  # Update the center based on the scaled rect


    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.animate()
        # Draw the hit box on the display_surface, not on the image
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.hit_box, 2)







        