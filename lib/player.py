import pygame
from support import import_folder
from models import Player, session
from pygame import Rect

class PlayerSprite(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index].convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.font = pygame.font.SysFont(None, 70)
		self.score = 0
		self.health = 100
		self.hit_cooldown = 0

		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16

		# player state
		self.state = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

	def import_character_assets(self):
		character_path = ('lib/assets/graphics/character/')
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('lib/assets/graphics/character/dust_particles/run')

	def animate(self):
		animation = self.animations[self.state]
	
		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		#rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def run_dust_animation(self):
		if self.state == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

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
			self.create_jump_particles(self.rect.midbottom)

	def get_state(self):
		if self.direction.y < 0:
			self.state = 'jump'
		elif self.direction.y > 1:
			self.state = 'fall'
		else:
			if self.direction.x != 0:
				self.state = 'run'
			else:
				self.state = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed
	
	def update_health(self, amount):
		if self.hit_cooldown <= 0:
			self.health -= amount
			self.hit_cooldown = 0.5

			if self.health <= 0:
				self.health = 0

			elif self.health > 100:
				self.health = 100

	def draw_health_bar(self, surface):
		bar_width = 100
		bar_height = 10
		bar_x = self.rect.centerx - bar_width // 2
		bar_y = self.rect.y - 20

		health_percentage = self.health / 100
		health_bar_width = int(bar_width * health_percentage)

		# Draw the background of the health bar
		bg_rect = Rect(bar_x, bar_y, bar_width, bar_height)
		pygame.draw.rect(surface, (255, 0, 0), bg_rect)

		# Draw the actual health bar
		health_rect = Rect(bar_x, bar_y, health_bar_width, bar_height)
		pygame.draw.rect(surface, (0, 255, 0), health_rect)

	def handle_enemy_collision(self, enemy):
		enemy_rect = enemy.rect

		if self.rect.colliderect(enemy_rect):
			if self.rect.bottom <= enemy_rect.top:  
				self.rect.bottom = enemy_rect.top
				self.velocity.y = -12 
				return True  

			self.update_health(20)  

		return False 
			
	def update(self):
		self.get_input()
		self.get_state()
		self.animate()
		self.run_dust_animation()
		if self.hit_cooldown > 0:
			self.hit_cooldown -= 0.01
