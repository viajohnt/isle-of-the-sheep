import pygame 
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect

class Level:
	def __init__(self,level_data,surface, username):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.username = username

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# grass setup 
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# sheeps 
		sheep_layout = import_csv_layout(level_data['sheep'])
		self.sheep_sprites = self.create_tile_group(sheep_layout,'sheep')

		# coins 
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		# foreground palms 
		tree_layout = import_csv_layout(level_data['trees'])
		self.tree_sprites = self.create_tile_group(tree_layout,'trees')

		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

		# constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

		# decoration 
		self.sky = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 20,level_width)
		self.clouds = Clouds(400,level_width,30)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('lib/assets/Tiny Swords/Terrain/Ground/Tilemap_Elevation.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					if type == 'grass':
						grass_tile_list = import_cut_graphics('lib/assets/Tiny Swords/Terrain/Ground/Tilemap_Flat.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
					
					if type == 'sheep':
						sheep_tile_list = import_cut_graphics('lib/assets/Tiny Swords/Resources/Sheep/HappySheep_All.png')
						tile_surface = sheep_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'coins':
						if val == '0': sprite = Coin(tile_size,x,y,'lib/assets/graphics/coins/gold')
						if val == '1': sprite = Coin(tile_size,x,y,'lib/assets/graphics/coins/silver')

					if type == 'trees':
						terrain_tile_list = import_cut_graphics('lib/assets/Tiny Swords/Resources/Trees/Tree.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)

					if type == 'enemies':
						sprite = Enemy(tile_size,x,y)

					if type == 'constraint':
						sprite = Tile(tile_size,x,y)
					sprite_group.add(sprite)
					
		return sprite_group

	def player_setup(self,layout):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('lib/assets/graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(tile_size,x,y,hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.sheep_sprites.sprites() + self.tree_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites() + self.sheep_sprites.sprites() + self.tree_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def run(self):
		# sky 
		self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)

		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# sheep
		self.sheep_sprites.update(self.world_shift)
		self.sheep_sprites.draw(self.display_surface)

		# coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

		# foreground palms
		self.tree_sprites.update(self.world_shift)
		self.tree_sprites.draw(self.display_surface)

		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		player = self.player.sprite
		for coin in pygame.sprite.spritecollide(player, self.coin_sprites, True):
			player.score += 1
		
		score_text = self.player.sprite.font.render("Score: " + str(self.player.sprite.score), True, (0, 0, 0))
		self.display_surface.blit(score_text, (20, 20))

		username_font = pygame.font.Font(None, 36)  
		username_text = username_font.render("User: " + self.username, True, (0, 0, 0))
		self.display_surface.blit(username_text, (20, 60))
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		
		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		# water 
		self.water.draw(self.display_surface,self.world_shift)



