#level editor by Coding with Russ
#this was edited for 'Castleton' 

import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

#define colors
color = (157, 211, 255)   

#game backgrounds
def draw_bg():
    screen.fill(color)
    
#game window
tile_size = 40
cols = 20
margin = 100
SCREEN_WIDTH = tile_size * cols
SCREEN_HEIGHT = (tile_size * cols) + margin

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption('Level Editor')

#load images
castle_img = pygame.image.load('imgs/castle-1.png')
dirt_img = pygame.image.load('imgs/dirt.png')
ground_img = pygame.image.load('imgs/ground.png')
gem_img = pygame.image.load('imgs/gem.png')
save_img = pygame.image.load('imgs/save_btn.png')
load_img = pygame.image.load('imgs/load_btn.png')
door_img = pygame.image.load('imgs/crown.png')
spikes_img = pygame.image.load('imgs/spikes.png')
water_img = pygame.image.load('imgs/water.png')

#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)
font = pygame.font.SysFont('Futura', 14)

#create empty tile list
world_data = []
for row in range(20):
	r = [0] * 20
	world_data.append(r)

#create boundary
for tile in range(0, 20):
	world_data[19][tile] = 2
	world_data[0][tile] = 1
	world_data[tile][0] = 1
	world_data[tile][19] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(0, 20):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, SCREEN_HEIGHT - margin))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (SCREEN_WIDTH, c * tile_size))

def draw_world():
	for row in range(16):
		for col in range(20):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#ground blocks
					img = pygame.transform.scale(ground_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#gem
					img = pygame.transform.scale(gem_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 4:
					#door
					img = pygame.transform.scale(door_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 5:
					#spikes
					img = pygame.transform.scale(spikes_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 6:
					#water
					img = pygame.transform.scale(water_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
		

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))
		return action

#create load and save buttons
save_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 80, save_img)
load_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT - 80, load_img)

#main game loop
run = True
while run:
	clock.tick(fps)
	draw_bg()

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)

	#show the grid and draw the level tiles
	draw_grid()
	draw_world()

	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, SCREEN_HEIGHT - 40)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, SCREEN_HEIGHT - 60)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 20 and y < 16:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 6:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 6
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()
pygame.quit()