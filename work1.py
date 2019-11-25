import sys
import pygame
from work import Star
from pygame.sprite import Group

def displaystar():
	pygame.init()
	screen= pygame.display.set_mode((1200, 800))
	pygame.display.set_caption('Display a grid of stars')
	star= Star(screen)
	color= (255, 255, 255)
	
	while True:
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				sys.exit()
		screen.fill(color)
		star.blitme()
		pygame.display.flip()
displaystar()
