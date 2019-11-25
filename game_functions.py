import sys

import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	'''Respond to key presses'''
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_p:
			start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets) 
		elif event.key == pygame.K_RIGHT:
			ship.moving_right= True
		elif event.key == pygame.K_LEFT:
			ship.moving_left= True
		elif event.key == pygame.K_SPACE:
			fire_bullets(ai_settings, screen, ship, bullets)
		elif event.key == pygame.K_q:
			filename= 'hs.txt'
			with open(filename, 'w') as f_obj:
				f_obj.write(str(stats.high_score))
			sys.exit()
def check_keyup_events(event, ship):
	'''Respond to key releases'''	
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RIGHT:
			ship.moving_right= False
		elif event.key == pygame.K_LEFT:
			ship.moving_left= False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
	bullets):
	'''Respond to key presses and mouth events'''
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			filename= 'hs.txt'
			with open(filename, 'w') as f_obj:
				f_obj.write(str(stats.high_score))
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats, sb, 
				play_button, ship, aliens, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
		'''elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y= pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, 
				ship, aliens, bullets, mouse_x, mouse_y)'''
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
	aliens, bullets):
	'''Start a new game when a player clicks play'''
	#button_clicked= play_button.rect.collidepoint(mouse_x, mouse_y)
	if not stats.game_active:
		#Hide the mouse cursor
		pygame.mouse.set_visible(False)
		
		#Initialize the game speeds
		ai_settings.initialize_dynamic_settings()
		
		#Reset  game statistics
		stats.reset_stats()
		stats.game_active= True
		
		#Reset scoreboard stats
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
	
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	'''start the game if button is pressed'''
	check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
	play_button):
	'''update images on the screen and flip to new screen'''
	#redraw the screen on each pass through the loop
	screen.fill(ai_settings.bg_color)
	
	#redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	
	#Draw the scoreboard to the screen
	sb.show_score()
	
	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
	
	#make the most recently drawn screen visible
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	'''update the position of bullets and get rid of old bullets'''
	bullets.update()
	
	# Get rid of bullets that have disappeared.
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, 
		bullets)
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, 
	bullets):
	'''Respond to bullet-alien collisions in the game'''		
	#check for bullets that have hit aliens
	#if so, get rid of alien and bullet
	collisions= pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#if the entire fleet is destroyed, start a new level
		#destroy existing bullets, speed up the game and create a new fleet of aliens
		bullets.empty()
		ai_settings.increase_speed()
		
		#increase the level
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)
			
def fire_bullets(ai_settings, screen, ship, bullets):
	'''fire a new bullet if limit not reached yet'''
	# Create a new bullet and add it to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet= Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	'''Determine the number of aliens that fit in a row'''
	available_space_x= ai_settings.screen_width - 2*alien_width
	number_aliens_x= int(available_space_x / (2*alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	'''Determine the number of aliens that fit on the screen'''
	available_space_y= (ai_settings.screen_height - (3 * alien_height)
			- ship_height)
	number_rows= int(available_space_y/ (2 * alien_height))
	return number_rows
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	'''create an alien and place it in the row'''
	alien= Alien(ai_settings, screen)
	alien_width= alien.rect.width
	alien.x= alien_width + 2*alien_width*alien_number
	alien.rect.x= alien.x
	alien.rect.y= alien.rect.height + 2* alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	'''create an entire fleet of aliens'''
	# Create an alien and find the number of aliens in a row.    
	# Spacing between each alien is equal to one alien width.
	alien= Alien(ai_settings, screen)
	number_aliens_x= get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows= get_number_rows(ai_settings, ship.rect.height, 
			alien.rect.height)
	 
	#create the fleet of aliens
	for row_number in range(number_rows):	
		for alien_number in range(number_aliens_x):
			#create an alien and place it in the row
			create_alien(ai_settings, screen, aliens, alien_number, 
				row_number)
				
def check_fleet_edges(ai_settings, aliens):
	'''respond appropriately if any aliens have reached the edge'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	'''drop the entire fleet and change the fleet's direction'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''check if any aliens have reached the bottom of the screen and respond appropriately'''
	screen_rect= screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#Treat this the same as if a ship got hit
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break
		
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''Respond to ship being hit by alien.'''
	if stats.ships_left > 0:
		#Decrement ships left
		stats.ships_left -= 1
	
		#Update scoreboard
		sb.prep_ships()
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
	
		#create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#Pause.
		sleep(0.5)
	else:
		#pygame.mouse.set_visible(True)
		stats.game_active= False

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	'''check if the fleet is at an edge then update the position of each alien in the fleet'''
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#detecting collisions between ship and aliens
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
	#look for aliens that hit the bottom of the screen
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens,bullets)
	
def check_high_score(stats, sb):
	'''check if there is a new high score'''
	if stats.score > int(stats.high_score):
		stats.high_score= stats.score
		sb.prep_high_score()
