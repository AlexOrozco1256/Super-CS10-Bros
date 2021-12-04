#To Start Game:
	#if in sublime
		# press ctrl + B
	#if in command prompt/terminal
		# write "python3 -i mario.py"
	#the space bar is to shoot the BJC Balls and the arrow keys are
	#for moving mario

import pygame 
import random
pygame.init()

#window
screen = pygame.display.set_mode((800, 600))

#title and icon
pygame.display.set_caption("Super CS10 Bros")
icon = pygame.image.load("project_logo.png")
pygame.display.set_icon(icon)

background = pygame.image.load("background.png")
game_over_background = pygame.image.load("game_over.png")

#clouds
cloud1 = pygame.image.load("cloud1.png")
cloud2 = pygame.image.load("cloud2.png")
cloud3 = pygame.image.load("cloud3.png")
cloud4 = pygame.image.load("cloud4.png")
cloud1x, cloud2x, cloud3x, cloud4x = 200, 400, 50, 700
cloud1y, cloud2y, cloud3y, cloud4y = 100, 150, 200, 100
cloudsx_change = -1

#bushes
bush1 = pygame.image.load("bush1.png")
bush2 = pygame.image.load("bush2.png")
bush3 = pygame.image.load("bush3.png")
bush1x, bush2x, bush3x = 50, 200, 450
bush1y, bush2y, bush3y = 450, 450, 450
bushx_change = -0.5

#mario player
mario_player = pygame.image.load("player.png")
mariox = 30
marioy = 450
mariospawny = 450
mariox_change = 0
mariojump = 0

#goomba
goomba = pygame.image.load("goomba.png")
goombax = 800
goombay = 515
goombax_change = -0.5

#bird
bird = pygame.image.load("bird.png")
birdx = 800
birdy = 350
birdspawny = 350
birdx_change = -0.5
birdy_change = 0

#fireball
fireball = pygame.image.load("bjc.png")
fireballx = 0
firebally = 460
fireballx_change = 5
#visible or not
fireball_state = "ready"

#pipe
pipe = pygame.image.load("pipe.png")
pipex = 800
pipey = 460
pipex_change = -0.5

goomba_life = 0

#above we were simply loading all of our images from our mario folder into this python file
#so that we can have graphics

#we then assigned x and y coordinates to variables associated with the images so that we can
#move the images rather than them being static

#score keeping
goombas_killed = 0
birds_killed = 0
enemies_killed = 0

#these are all of our score keeping variables

#draw score on screen fn
on_screen_score = pygame.font.Font("freesansbold.ttf", 32)
def show_score():
	score = on_screen_score.render("Score:" + str(goombas_killed + birds_killed), True, (255, 255, 255))
	screen.blit(score, (10, 10))

g_killed_font = pygame.font.Font("freesansbold.ttf", 32)
def print_goombas_killed():
	g_killed_text = g_killed_font.render("Goombas Killed: " + str(goombas_killed), True, (255, 255, 255))
	screen.blit(g_killed_text, (250, 225))

b_killed_font = pygame.font.Font("freesansbold.ttf", 32)
def print_birds_killed():
	b_killed_text = b_killed_font.render("Birds Killed: " + str(birds_killed), True, (255, 255, 255))
	screen.blit(b_killed_text, (275, 275))

#these functions don't take any inputs because when we show the score on the screen
#we want it to be static anyways 

#draw clouds fn
def cloud1_draw(x, y):
	screen.blit(cloud1, (x,y))
def cloud2_draw(x, y):
	screen.blit(cloud2, (x,y))
def cloud3_draw(x, y):
	screen.blit(cloud3, (x,y))
def cloud4_draw(x, y):
	screen.blit(cloud4, (x,y))

#draw bush fn
def bush1_draw(x, y):
	screen.blit(bush1, (x,y))
def bush2_draw(x, y):
	screen.blit(bush2, (x,y))
def bush3_draw(x, y):
	screen.blit(bush3, (x,y))

#draw mario fn
def mario_draw(x, y):
	screen.blit(mario_player, (x, y))

#draw goomba fn
def goomba_draw(x, y):
	screen.blit(goomba, (x, y))

#draw bird fn
def bird_draw(x, y):
	screen.blit(bird, (x, y))

#draw fireballs fn
def fireball_draw(x, y):
	global fireball_state
	fireball_state = "shoot"
	screen.blit(fireball, (x - 10, y + 60))

#draw pipe fn
def pipe_draw(x, y):
	screen.blit(pipe, (x, y))

#all of these functions take in an x, y coordinate pair as an input and then 
#proceed to paste the image on the screen at those respective coordinates
#screen.blit is the function for drawing graphics on the screen that comes with pygames

#is fireball touching goomba?
def fireball_touching_goomba(fireballx, goombax, firebally, goombay):
	if fireballx - goombax > -27 and firebally - goombay == -65:
		return True
	else:
		return False

#is fireball touching bird?
def fireball_touching_bird(fireballx, birdx, firebally, birdy):
	if fireballx - birdx > -27 and (-85 < firebally - birdy < -45):
		return True
	else:
		return False

#is fireball touching pipe?
def fireball_touching_pipe(fireballx, pipex, firebally, pipey):
	if 50 > fireballx - pipex > 20 and firebally - pipey == -10:
		return True
	else:
		return False

#is goomba touching SuperDan?
def goomba_touching_SuperDan(mariox, goombax, marioy, goombay):
	if 50 > goombax - mariox > 0 and goombay - marioy == 65:
		return True
	else:
		return False

#all of these functions are responsible for the interactions that happen between
#our characters (a.k.a grahics) and they work by comparing the relative positions
#of the characters; if they are close enough to each other, an interaction is registered
#and the corresponing results ensue

#game condition
game_over = False
#this is ultimately what determines if you are still allowed to play the game

#game display loop
#the loop is constantly running, the only way to exit the game loop is by pressing 
#the x button on the window which sets running to false
#the graphics aren't actually moving in real time, they are just being pasted on
#different parts of the screen over and over again everytime the sceen refreshes

running = True
while running:

	#sky background
	screen.fill((135, 206, 235))
	screen.blit(background, (0,11))

	#keyboard controls
	for event in pygame.event.get():

		#quitting the window
		if event.type == pygame.QUIT:
			running = False

		#right/left controls
		if event.type == pygame.KEYDOWN: 
			if event.key == pygame.K_LEFT:
				mariox_change -= 1
			if event.key == pygame.K_RIGHT:
				mariox_change += 1

			#fireball shooting
			if event.key == pygame.K_SPACE:
				if fireball_state is "ready":
					fireballx = mariox
					firebally = marioy
					fireball_draw(fireballx, firebally) 
					#we linked the fireball coordinates to the mario coordinates
					#the fireball is always on the screen but we only see it once it
					#moves away from mario

			#jumping up
			if event.key == pygame.K_UP:
				mariojump = -2

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				mariox_change = 0


	#background bushes
	bush1_draw(bush1x, bush1y)
	bush2_draw(bush2x, bush2y)
	bush3_draw(bush3x, bush3y)

	#coming down/ jump boundaries
	marioy += mariojump
	if marioy <= mariospawny - 100:
		mariojump = 2
	if marioy >= mariospawny:
		marioy = mariospawny
	#the way our jump function works is by setting an upper boundary for our marioy's
	#coordinate and once that boundary is reached, we reverse the direction of mariojump
	#which causes mario to come back down until he reaches his initial spawn value
	#a.k.a the floor

	#bird zig zag
	birdy += birdy_change
	if birdy == birdspawny:
		birdy_change = 0.5
	if birdy == birdspawny + 100:
		birdy_change = -0.5
	#this works very much like the mario jump feature, except that the bird is bouncing
	#between an upper and lower bound rather than waiting for a keyboard press to 
	#set it in motion like mario

	#mario jumping on pipe
	if 0 < mariox - pipex < 30 and marioy < mariospawny - 60:
		marioy = mariospawny - 60
		mariojump = 0

	if 130 > mariox - pipex > 120 and marioy == mariospawny - 60:
		mariojump = 2
	#the way our mario jumping on the pipe works is that if mario is at the height
	#of the top of the pipe, and near the pipe's x coordinate, mario's y lower boundary
	#is set to the top of the pipe and remains that way until mario's x coordinate
	#is past the width of the pipe

	#lateral movements
	mariox += mariox_change
	goombax += goombax_change
	pipex += pipex_change
	birdx += birdx_change
	cloud1x += cloudsx_change
	cloud2x += cloudsx_change
	cloud3x += cloudsx_change
	cloud4x += cloudsx_change
	bush1x += bushx_change
	bush2x += bushx_change
	bush3x += bushx_change
	#this is just adding constanly the value of the x_change to the x coordinate
	#of the respective objects while the game is running in the while loop

	#list requirements
	cloudx_positions = [cloud1x, cloud2x, cloud3x, cloud4x]
	cloudy_positions = [cloud1y, cloud2y, cloud3y, cloud4y]

	#display boundaries for mario
	if mariox <= 0:
		mariox = 0
	elif mariox >= 757:
		mariox = 757
	#this prevents mario from being taken off of the screen	

	#fireball movement
	if fireballx >= 800:
		fireballx = 30
		fireball_state = "ready"
	#this links the fireball coordinates back to mario so that it is out of sight and
	#appears to respawn when the space bar is pressed

	#shooting fireball
	if fireball_state is "shoot":
		fireball_draw(fireballx, firebally)
		fireballx += fireballx_change

	#is fireball touching goomba? 
	touching = fireball_touching_goomba(fireballx, goombax, firebally, goombay)
	if touching:
		fireballx = 0
		fireball_state = "ready"
		goomba_life += 1
		goombax_change -= 0.05

	#is fireball touching bird? 
	touching_bird = fireball_touching_bird(fireballx, birdx, firebally, birdy)
	if touching_bird:
		fireballx = 0
		fireball_state = "ready"
		birdx = random.randint(1100, 1200)
		birds_killed += 1

	#is fireball touching pipe? 
	touching_pipe = fireball_touching_pipe(fireballx, pipex, firebally, pipey)
	if touching_pipe:
		fireballx = 0
		fireball_state = "ready"
	#if the touching functions are true, we respawn the objects that were hit

	#goomba life
	if goomba_life == 3:
		goombax = random.randint(1000, 1200)
		goomba_life = 0
		goombax_change -= 0.05
		goombas_killed += 1
	#we gave the goomba extra health for the sake of difficulty

	#goomba respawn
	if goombax <= -100:
		goombax = random.randint(1000, 1200)
		goombax_change -= 0.05

	if birdx <= -200:
		birdx = random.randint(1100, 1200)

	#pipe regeneration
	if pipex <= -200:
		pipex = random.randint(1200, 1400)
		pipex_change -= 0.2

	#cloud regeneration
	cloudx_positions = [random.randint(800,2000) for x in cloudx_positions if x <= -200]
	if len(cloudx_positions) > 3:
		cloud1x = cloudx_positions[0]
		cloud2x = cloudx_positions[1]
		cloud3x = cloudx_positions[2]
		cloud4x = cloudx_positions[3]
		cloudy_positions = [random.randint(20,300) for x in cloudx_positions if x <= -200]
	if len(cloudy_positions) > 3:
		cloud1y = cloudy_positions[0]
		cloud2y = cloudy_positions[1]
		cloud3y = cloudy_positions[2]
		cloud4y = cloudy_positions[3]

	#bush regeneration
	if bush1x <= -200:
		bush1x = random.randint(800, 1000)
	if bush2x <= -200:
		bush2x = random.randint(800, 1000)
	if bush3x <= -200:
		bush3x = random.randint(800, 1000)

	#we give the x values random coordinates off of the screen to give the illusion
	#that there are many different bushes being drawn instead of the same 3
	#coming back over and over again


	#list requirement
	enemies_killed = ["birds killed = " + str(birds_killed), "goombas killed = " + str(goombas_killed), "total= " + str(birds_killed + goombas_killed)]
	print(enemies_killed)

	#drawing on game display
	cloud1_draw(cloud1x, cloud1y)
	cloud2_draw(cloud2x, cloud2y)
	cloud3_draw(cloud3x, cloud3y)
	cloud4_draw(cloud4x, cloud4y)
	bird_draw(birdx, birdy)
	pipe_draw(pipex, pipey)
	goomba_draw(goombax, goombay)
	mario_draw(mariox, marioy)
	#these functions are in the display loop and linked to the variables so that
	#the objects can be drawn at different spots every refresh

	#drawing score on screen
	show_score()

	#ending the game
	if goomba_touching_SuperDan(mariox, goombax, marioy, goombay) == True:
		game_over = True
	#we have to set a variable equal to true because since this is in the while loop
	#if we make our condition the function, it will be set back to false as soon as the mariox
	#coordinate is past the goomba's x coordinate
	if game_over:
		goombax = 2000
		birdx = 2000
		screen.blit(game_over_background, (0,0))
		print_birds_killed()
		print_goombas_killed()

	pygame.display.update()
