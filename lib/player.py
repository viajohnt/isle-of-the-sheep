import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['Idle'][self.frame_index][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = display_surface

        self.scale_factor = .223

        #Player Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'Idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False 

    def import_character_assets(self):
        character_path = 'lib/assets/BlueWizard/'
        self.animations = {'Idle': [], 'Walk': [], 'Jump': [], 'Dash2': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            temp_animations = import_folder(full_path)

            self.animations[animation] = [(image, image.get_width(), image.get_height()) for image in temp_animations]

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image, original_width, original_height = animation[int(self.frame_index)]
        new_width = int(original_width * self.scale_factor)
        new_height = int(original_height * self.scale_factor)
        scaled_image = pygame.transform.scale(image, (new_width, new_height))

        if self.facing_right:
            self.image = scaled_image
        else:
            flipped_image = pygame.transform.flip(scaled_image, True, False)
            self.image = flipped_image

        # Set Rect
        if self.on_ground and self.on_right: 
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft) 
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def draw_collision_box(self):
        pygame.draw.rect(self.display_surface, (255, 0, 0), self.collision_rect, 2)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        elif self.direction.x != 0:
            self.status = 'Dash2'
        else:
            self.status = 'Idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status ()
        self.animate()
 








        