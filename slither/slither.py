##	Snake Game "Slither"
##	Braxton Gunter

import pygame as pyg, time, random
from colors import *

#initialize module
pyg.init()

display_width = 600
display_height = 400

#main display
game_display = pyg.display.set_mode((display_width,display_height)) #tuple
pyg.display.set_caption("Slither")

#fps
fps = 15
clock = pyg.time.Clock()

block_size = 10

#message display
font = pyg.font.SysFont(None, 25)
def text_objects(text, color):
	"""Passes text through and gets its text box"""
	text_surface = font.render(text,True,color)
	return (text_surface, text_surface.get_rect())

def display_message(msg,color):
	"""Sends a centered message to screen"""
	text_surface, text_rectangle = text_objects(msg,color)
	text_rectangle.center = (display_width/2),(display_height/2)
	game_display.blit(text_surface, text_rectangle)

#snake
def snake(block_size, snakeList):
	"""Creates a dynamic snake"""
	for element in snakeList:
		#element[0] = x, element[1] = y
		pyg.draw.rect(game_display,GREEN,[element[0],element[1],block_size,block_size])

#apple
def appleX(display_width,display_height,apple_thickness):
	"""Generate's an apple's random X coordinate"""
	apple_x = (random.randrange(0, display_width - apple_thickness))
	apple_x = (round(apple_x/apple_thickness)) * apple_thickness
	return apple_x
def appleY(display_width,display_height,apple_thickness):
	"""Generate's an apple's random Y coordinate"""
	apple_y = (random.randrange(0, display_height - apple_thickness))
	apple_y = (round(apple_y/apple_thickness)) * apple_thickness
	return apple_y

#main game function
def gameLoop():
	"""Plays main snake game"""
	#snake
	lead_x = display_width / 2
	lead_y = display_height / 2

	snakeList = []
	snakeLength = 1

	#snake movement
	lead_x_change = 0
	lead_y_change = 0

	#apple
	apple_thickness = 10
	apple_x = appleX(display_width,display_height,apple_thickness)
	apple_y = appleY(display_width,display_height,apple_thickness)

	gameExit = False
	gameOver = False

	#game loop
	while not gameExit:

		#game over loop
		while gameOver == True:
			game_display.fill(BLACK)
			display_message("You Lose! Press P to play again, or Q to quit.",WHITE)
			#update rendering
			pyg.display.update()

			for event in pyg.event.get():
				#window close
				if event.type == pyg.QUIT:
						gameExit = True
						gameOver = False
				if event.type == pyg.KEYDOWN:
					#press Q to quit
					if event.key == pyg.K_q:
						gameExit = True
						gameOver = False
					#press C to play again
					elif event.key == pyg.K_p:
						gameLoop()

		for event in pyg.event.get():
			print(event)
			if event.type == pyg.QUIT:
				gameExit = True
			if event.type == pyg.KEYDOWN:
				#x-axis
				if event.key == pyg.K_LEFT:
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pyg.K_RIGHT:
					lead_x_change = block_size
					lead_y_change = 0
				#y-axis
				elif event.key == pyg.K_UP:
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pyg.K_DOWN:
					lead_y_change = block_size
					lead_x_change = 0

		#boundaries
		if (lead_x >= display_width) or (lead_x < 0) or (lead_y >= display_height)\
		or (lead_y < 0):
			gameOver = True

		lead_x += lead_x_change
		lead_y += lead_y_change

		#background
		game_display.fill(WHITE)

		#apple
		pyg.draw.rect(game_display,RED,[apple_x,apple_y,apple_thickness,apple_thickness])

		#dynamic snake
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)

		#call snake function
		snake(block_size,snakeList)

		#manage length as snake moves
		if len(snakeList) > snakeLength:
			del snakeList[0]

		#snake self boundaries
		for segment in snakeList[:-1]:
			if segment == snakeHead:
				gameOver = True

		#update rendering
		pyg.display.update()

		#apple collision
		if (lead_x >= apple_x and lead_x <= apple_x + apple_thickness) and (lead_y >= apple_y and lead_y <= apple_y + apple_thickness):
			print("nom nom nom")
			#new apple
			apple_x = appleX(display_width,display_height,apple_thickness)
			apple_y = appleY(display_width,display_height,apple_thickness)
		 	#grow
			snakeLength += 1

		#fps
		clock.tick(fps)

	pyg.quit() #uninitialize
	quit()

gameLoop()
