
class GameStats():
	'''Track statistics for Alien Invasion'''
	def __init__(self, ai_settings):
		'''initialize statistics.'''
		self.ai_settings= ai_settings
		self.reset_stats()
		
		#High score should never be reset
		filename= 'hs.txt'
		with open(filename, 'r') as f_obj:
			contents= f_obj.read()
		self.high_score= contents
		
		#start the game in an inactive state
		self.game_active= False
		
	def reset_stats(self):
		'''Initialize statistics that can change during the game'''
		self.ships_left= self.ai_settings.ship_limit
		self.score= 0
		self.level= 1
