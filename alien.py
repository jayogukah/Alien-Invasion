import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	'''a class to draw a single alien in a fleet of aliens'''
	def __init__(self, ai_settings, screen):
		'''initialize the alien and set its starting position'''
		super().__init__()
		self.screen= screen
		self.ai_settings= ai_settings
	
		#load the alien image and define its position
		self.image= pygame.image.load('images/alien.bmp')
		self.rect= self.image.get_rect()
		#set its position at the top left
		self.rect.x= self.rect.width
		self.rect.y= self.rect.height
	
		#store the alien's exact position
		self.x= float(self.rect.x)
	
	def blitme(self):
		'''draw the alien at its current location'''
		self.screen.blit(self.image, self.rect)
		
	def check_edges(self):
		'''check if an alien has hit the edge of the screen and return True'''
		screen_rect= self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		

	def update(self):
		'''update each aliens location by a defined speed and move right'''
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x= self.x
