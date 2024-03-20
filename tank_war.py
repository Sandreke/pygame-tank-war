import pygame
import time
import random

##################################################################
##### Este juego fue desarrollado por Sandreke (@sandreke99) #####
##################################################################

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
light_red = (255, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
green = (0, 155, 0)
light_green = (0, 255, 0)

display_width = 800
display_height = 750

tankHeight = 20
tankWidth = 40

ground_height = 45

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tank War by Sandreke")
fondo = pygame.image.load("images/fondo1.jpg")
fondo = pygame.transform.scale(fondo, (display_width, display_height))

fire_sound = pygame.mixer.Sound("sounds/misil.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosión.wav")

clock = pygame.time.Clock()

FPS = 10
direction = "right"

smallfont = pygame.font.SysFont("ematane", 25)
medfont = pygame.font.SysFont("ematane", 50)
largefont = pygame.font.SysFont("ematane", 80)

def tank(x, y, turPos):
	x = int(x)
	y = int(y)

	possibleTurrets = [(x-27, y - 2), 
						(x-26, y - 5),
						(x-25, y - 8),
						(x-23, y - 12),
						(x-20, y - 14),
						(x-18, y - 15),
						(x-15, y - 17),
						(x-13, y - 19),
						(x-11, y-21)]

	tank_image = pygame.image.load("images/peru.png").convert_alpha()
	tank_image = pygame.transform.scale(tank_image, (90, 40))
	gameDisplay.blit(tank_image, (x-30, y-10))
	pygame.draw.line(gameDisplay, white, (x, y), possibleTurrets[turPos], 5)

	return possibleTurrets[turPos]

def enemy_tank(x, y, turPos):
	x = int(x)
	y = int(y)

	possibleTurrets = [(x+27, y - 2), 
						(x+26, y - 5),
						(x+25, y - 8),
						(x+23, y - 12),
						(x+20, y - 14),
						(x+18, y - 15),
						(x+15, y - 17),
						(x+13, y - 19),
						(x+11, y-21)]

	enemy_tank_image = pygame.image.load("images/alemania.png").convert_alpha()
	enemy_tank_image = pygame.transform.scale(enemy_tank_image, (90, 40))
	gameDisplay.blit(enemy_tank_image, (x-60, y-10))
	pygame.draw.line(gameDisplay, white, (x, y), possibleTurrets[turPos], 5)

	return possibleTurrets[turPos]

def score(score):
	text = smallfont.render("Score: "+str(score), True, black)
	gameDisplay.blit(text, [0, 0])	

def ground(display_height, display_width, ground_height):
	gameDisplay.fill(black, rect=[0, display_height - ground_height, display_width, ground_height])
	pygame.draw.line(gameDisplay, white, (0, display_height - ground_height), (display_width, display_height - ground_height), 2)

def barrier(xlocation, randomHeight, barrier_width):
	pygame.draw.rect(gameDisplay, black,[xlocation, display_height-randomHeight, barrier_width, randomHeight], border_radius=5)
	pygame.draw.rect(gameDisplay, white, (xlocation, display_height-randomHeight-2, barrier_width, randomHeight), 2, border_radius=5)

def explosion(x, y, size=50):
	pygame.mixer.Sound.play(explosion_sound)
	explode = True

	while explode:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		startPoint = x, y
		colorChoices = [red, light_red, yellow, light_yellow]
		magnitude = 1

		while magnitude < size:
			exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
			exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)
			pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0, 4)],(exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
			magnitude += 1

			pygame.display.update()
			clock.tick(100)

		explode =False


def fireShell(xy, tankx, tanky, turPos, gun_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY):
	pygame.mixer.Sound.play(fire_sound)
	fire = True
	damage = 0
	startingShell = list(xy)

	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
		startingShell[0] -= (12 - turPos)*2
		startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(gun_power/30.0))**2) - (turPos + turPos/(12-turPos)))

		if startingShell[1] > display_height - ground_height:
			hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
			hit_y = int(display_height-ground_height)
			if enemyTankX + 10 > hit_x > enemyTankX - 10:
				damage = 25
			elif enemyTankX + 15 > hit_x > enemyTankX - 15:
				damage = 18
			elif enemyTankX + 25 > hit_x > enemyTankX - 25:
				damage = 10
			elif enemyTankX + 35 > hit_x > enemyTankX - 35:
				damage = 5

			explosion(hit_x, hit_y)
			fire = False

		check_x_1 = startingShell[0] <= xlocation + barrier_width
		check_x_2 = startingShell[0] >= xlocation
		check_y_1 = startingShell[1] <= display_height 
		check_y_2 = startingShell[1] >= display_height - randomHeight 

		if check_x_1 and check_x_2 and check_y_1 and check_y_2:
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])
			explosion(hit_x, hit_y)
			fire = False

		pygame.display.update()
		clock.tick(60)	

	return damage	


def e_fireShell(xy, tankx, tanky, turPos, gun_power, xlocation, barrier_width, randomHeight, ptankX, ptankY):
	pygame.mixer.Sound.play(fire_sound)
	damage = 0
	currentPower = 1
	power_found = False

	while not power_found:
		currentPower += 1
		if currentPower > 100:
			power_found = True

		fire = True
		startingShell = list(xy)

		while fire:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			startingShell[0] += (12 - turPos)*2
			startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(currentPower/50.0))**2) - (turPos + turPos/(12-turPos)))

			if startingShell[1] > display_height - ground_height:
				hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
				hit_y = int(display_height-ground_height)
				if ptankX + 15 > hit_x > ptankX - 15:
					power_found = True
				fire = False

			check_x_1 = startingShell[0] <= xlocation +  barrier_width
			check_x_2 = startingShell[0] >= xlocation
			check_y_1 = startingShell[1] <= display_height 
			check_y_2 = startingShell[1] >= display_height - randomHeight 

			if check_x_1 and check_x_2 and check_y_1 and check_y_2:
				hit_x = int(startingShell[0])
				hit_y = int(startingShell[1])
				fire = False

	fire = True
	startingShell = list(xy)

	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
		startingShell[0] += (12 - turPos)*2
		gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.10))
		startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(gun_power/50.0))**2) - (turPos + turPos/(12-turPos)))

		if startingShell[1] > display_height - ground_height:
			hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
			hit_y = int(display_height-ground_height)
			if ptankX + 10 > hit_x > ptankX - 10:
				damage = 25
			elif ptankX + 15 > hit_x > ptankX - 15:
				damage = 18
			elif ptankX + 25 > hit_x > ptankX - 25:
				damage = 10
			elif ptankX + 35 > hit_x > ptankX - 35:
				damage = 5
				
			explosion(hit_x, hit_y)
			fire = False

		check_x_1 = startingShell[0] <= xlocation + barrier_width
		check_x_2 = startingShell[0] >= xlocation
		check_y_1 = startingShell[1] <= display_height 
		check_y_2 = startingShell[1] >= display_height - randomHeight 

		if check_x_1 and check_x_2 and check_y_1 and check_y_2:
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])
			explosion(hit_x, hit_y)
			fire = False

		pygame.display.update()
		clock.tick(60)

	return damage


def power(level):
	text = smallfont.render("Power: "+str(level)+"%",True, black)
	gameDisplay.blit(text, [display_width/2, 0])


def game_over():
	game_over = True
	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(fondo, (0, 0))
		perdiste = pygame.image.load("images/perdiste.png").convert_alpha()
		perdiste = pygame.transform.scale(perdiste, (400, 400))
		gameDisplay.blit(perdiste, (200, 50))

		button("Jugar de nuevo", 325, 550, 150, 50, white, black, action="play")

		pygame.display.update()
		clock.tick(15)

def you_win():
	win = True
	while win:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(fondo, (0, 0))
		ganaste = pygame.image.load("images/ganaste.png").convert_alpha()
		ganaste = pygame.transform.scale(ganaste, (400, 400))
		gameDisplay.blit(ganaste, (200, 50))

		button("Jugar de nuevo", 325, 550, 150, 50, white, black, action="play")

		pygame.display.update()
		clock.tick(15)

def text_objects(text, color, size):
	if size == "small":	
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)
	return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight,size = "small"):
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
	gameDisplay.blit(textSurface, textRect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + width > cur[0] > x and y + height > cur[1] > y:
		pygame.draw.rect(gameDisplay, active_color, (x, y, width, height), border_radius=5)
		text_to_button(text, white, x, y, width, height)
		if click[0] == 1 and action != None:
			if action == "play":
				gameLoop()
			
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height), border_radius=5)
		text_to_button(text, black, x, y, width, height)

def message_to_screen(msg, color, y_displace=0, size="small"):
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = display_width/2, display_height/2 + y_displace
	gameDisplay.blit(textSurface, textRect)


def health_bars(player_health, enemy_health):
	if player_health > 75:
		player_health_color = green
	elif player_health > 50:
		player_health_color = yellow
	else:
		player_health_color = red

	if enemy_health > 75:
		enemy_health_color = green
	elif enemy_health > 50:
		enemy_health_color = yellow
	else:
		enemy_health_color = red
		
	pygame.draw.rect(gameDisplay, black, (675, 20, 110, 35), 5, border_radius=5)
	pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
	pygame.draw.line(gameDisplay, black, (680 + player_health, 20), (680 + player_health, 50), 3)

	pygame.draw.rect(gameDisplay, black, (15, 20, 110, 35), 5, border_radius=5)
	pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))
	pygame.draw.line(gameDisplay, black, (20 + enemy_health, 20), (20 + enemy_health, 50), 3)


def gameLoop():
	global direction
	direction = "right"

	gameExit = False
	gameOver = False

	player_health = 100
	enemy_health = 100

	mainTankX = display_width*0.9
	mainTankY = display_height*0.9

	enemyTankX = display_width*0.1
	enemyTankY = display_height*0.9

	tankMove = 0

	currentTurPos = 0
	changeTur = 0

	fire_power = 50
	power_change = 0

	xlocation = (display_width/2)+random.randint(-0.1*display_width,0.1*display_width)
	randomHeight = random.randrange(display_height*0.1, display_height*0.6)

	barrier_width = 50

	while not gameExit:
		if gameOver == True:
			message_to_screen("Game over.", red, y_displace=-50, size="large")
			pygame.display.update()

		while gameOver == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameLoop()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					tankMove = -5
				elif event.key == pygame.K_RIGHT:
					tankMove = +5
				elif event.key == pygame.K_UP:
					changeTur = 1
				elif event.key == pygame.K_DOWN:
					changeTur = -1
				elif event.key == pygame.K_SPACE:
					damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY)
					enemy_health -= damage
					possibleMovement = ['f', 'r']
					moveIndex = random.randrange(0, 2)
					for x in range(random.randrange(0,10)):
						if display_width*0.3 > enemyTankX > display_width*0.03:
							if possibleMovement[moveIndex] == 'f':
								enemyTankX += 5
							elif possibleMovement[moveIndex] == 'r':
								enemyTankX -= 5

							gameDisplay.blit(fondo, (0, 0))
							health_bars(player_health, enemy_health)
							gun = tank(mainTankX, mainTankY, currentTurPos)
							enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

							fire_power += power_change
							power(fire_power)
							barrier(xlocation, randomHeight, barrier_width)
							ground(display_height, display_width, ground_height)
							pygame.display.update()
							clock.tick(FPS)

					damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, xlocation, barrier_width, randomHeight,mainTankX, mainTankY )
					player_health -= damage

				elif event.key == pygame.K_a:
					power_change = -1
				elif event.key == pygame.K_d:
					power_change = 1

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					tankMove = 0
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					changeTur = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					power_change = 0

		mainTankX += tankMove
		currentTurPos += changeTur

		if currentTurPos > 8:
			currentTurPos = 8
		elif currentTurPos < 0:
			currentTurPos = 0

		if mainTankX - (tankWidth/2)  < xlocation + barrier_width:
			mainTankX += 5

		gameDisplay.blit(fondo, (0, 0))
		health_bars(player_health, enemy_health)
		gun = tank(mainTankX, mainTankY, currentTurPos)
		enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

		fire_power += power_change

		if fire_power > 100:
			fire_power = 100
		elif fire_power < 1:
			fire_power = 1

		power(fire_power)
		barrier(xlocation, randomHeight, barrier_width)
		ground(display_height, display_width, ground_height)
		pygame.display.update()

		if player_health < 1:
			game_over()
		elif enemy_health < 1:
			you_win()

		clock.tick(FPS)

	pygame.quit()
	quit()

gameLoop()