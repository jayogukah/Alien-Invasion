import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
	#initialize game and create a screen update
	pygame.init()
	ai_settings= Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, 
		ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	pygame.mouse.set_visible(False)
	#Make Play Button instance
	play_button= Button(ai_settings, screen, 'Play(p), Quit(q)')
	
	#Create an instance to store  game stats and scoreboard
	stats= GameStats(ai_settings)
	sb= ScoreBoard(ai_settings, screen, stats)
	
	#Make a ship, a group of bullets and a group of aliens
	ship= Ship(ai_settings, screen)
	bullets= Group()
	aliens= Group()
	
	#create a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#the main loop for the game
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
			aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, 
				bullets)

		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
			bullets, play_button)
				
run_game()
