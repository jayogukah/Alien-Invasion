
class Settings():
	'''a class to store all settings for the game, Alien Invasion'''
	def __init__(self):
		'''Initialize the game's settings'''
		#screen settings
		self.screen_width= 1200
		self.screen_height= 800
		self.bg_color= (230, 230, 230)
		
		#ship settings
		self.ship_limit = 3
		
		#Bullet Settings
		self.bullet_width= 3
		self.bullet_height= 15
		self.bullet_color= 60, 60, 60
		self.bullets_allowed= 4
		
		#alien settings
		self.alien_speed_factor= 1
		self.fleet_drop_speed= 10
		
		#How quickly the game speeds up
		self.speedup_scale= 1.2
		
		#How quickly the alien point values increase
		self.score_scale= 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		'''initialize settings that change through the game'''
		self.bullet_speed_factor= 3
		self.ship_speed_factor = 1.5
		self.alien_speed_factor= 1
		#fleet direction, right or left, -1 for left and 1 for right
		self.fleet_direction= 1
		
		#Alien points
		self.alien_points= 50

	def increase_speed(self):
		'''increase the speed of the game and alien points values as the level goes up'''
		self.bullet_speed_factor *= self.speedup_scale
		self.ship_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
