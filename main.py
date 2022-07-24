#Pixel Platformer by Kenney
#https://kenney.nl/assets/pixel-platformer

#Castle Background by Saphatthachat Sunchoote
#https://www.dreamstime.com/pixel-art-fantasy-castle-roof-image223418688

import pygame
from pygame.locals import *
from pygame import mixer
import math
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castleton')

#clock and frame rate
clock = pygame.time.Clock()
FPS = 60

#define font
font = pygame.font.SysFont('Banhaus 93', 70)
font_score = pygame.font.SysFont('Banhaus 93', 30)


#define game variables
tile_size = 40
game_over = 0
main_menu = True
level = 1
max_levels = 3
score = 0

#load images
title_img = pygame.image.load('imgs/title_img.png')
title_img = pygame.transform.scale(title_img, (800, 800))
castle_img = pygame.image.load('imgs/castle-1.png')
dirt_img = pygame.image.load('imgs/dirt.png')
ground_img = pygame.image.load('imgs/ground.png')
restart_img = pygame.image.load('imgs/restart_btn.png')
start_img = pygame.image.load('imgs/start_btn.png')
start_img = pygame.transform.scale(start_img, (270, 120))

#load sounds
gem_effect = pygame.mixer.Sound('Sounds/gem.wav')
'''
---grid to help place items in graphic window---
def draw_grid():
    for line in range(0, 20):
       pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (SCREEN_WIDTH, line * tile_size ))
       pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line*tile_size, SCREEN_HEIGHT))
'''

#define colors
blue = (157, 211, 255)   
white = (255, 255, 255)

#game backgrounds
def draw_bg():
    screen.fill(blue)

#draw text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


#reset function to reset level
def reset_level(level):
    player.reset(100, SCREEN_HEIGHT - 40)
    enemy_group.empty()
    flag_group.empty()

    #load on level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    return world


    
#buttons
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked position
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # 0: left mouse button 
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0]:
            self.clicked = False
            
        #draw button
        screen.blit(self.image, self.rect)
        return action


class Player():
    def __init__(self, x, y):
        self.reset(x,y)
         
    def update(self, game_over):
        #delta variables
        dx = 0
        dy = 0
        walk_cooldown = 5
        
        if game_over == 0:
            #keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jump == False and self.in_air == False:
                self.vel_y = -15 
                self.jump = True
            if key[pygame.K_SPACE] == False:
                self.jump = False
            if key[pygame.K_LEFT]:
                dx -= 2
                self.counter +=1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 2
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index= 0
            if self.direction == 1:
                    self.image = self.images_right[self.index]
            if self.direction == -1:
                    self.image = self.images_left[self.index]
    
            #animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            
            #gravity
            self.vel_y += 1
            if self.vel_y > 10: 
                self.vel_y = 10
            dy += self.vel_y
            
            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0    
                #check in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        
            #check collision with enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
            #check collision with flag
            if pygame.sprite.spritecollide(self, flag_group, False):
                game_over = 1
            
            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            
        elif game_over == -1:
            draw_text('GAME OVER!', font, white,(SCREEN_WIDTH // 2) - 200, SCREEN_HEIGHT // 2)
            self.image = self.death_image
        
        #draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        return game_over
    
    def reset(self, x, y): 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for i in range(1, 4):
            img_right = pygame.image.load(f'King/Walk/{i}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (38, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        for i in range(1,3):
            self.death_image = pygame.image.load(f'King/Death/{i}.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump = False
        self.direction = 0
        self.in_air = True
        
              
class World():
    def __init__(self, data):
        self.tile_list =[]
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(ground_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 8)
                    enemy_group.add(enemy)
                if tile == 4:
                    gem= Gem(col_count * tile_size, row_count * tile_size + 8)
                    gem_group.add(gem)
                if tile == 5:
                    flag = Flag(col_count * tile_size, row_count * tile_size + 8)
                    flag_group.add(flag) 
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (0, 0, 0), tile[1], 2)

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('imgs/flag.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('imgs/gem.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('imgs/enemy.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))       
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 15:
            self.move_direction *= -1
            self.move_counter *= -1
        
# 16 rows, 20 columns
#player
player = Player(100, SCREEN_HEIGHT - 40)
#enemy
enemy_group = pygame.sprite.Group()
#flag
flag_group = pygame.sprite.Group()
#gem
gem_group = pygame.sprite.Group()

#dummy gem for showing score
score_gem = Gem(tile_size //2, tile_size // 2)
gem_group.add(score_gem)

#load level data and create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#buttons
restart_button = Button(340, 0, restart_img)
start_button = Button(260, 375, start_img)


run = True
while run:
    
    #draw_grid()

    draw_bg()
    
    clock.tick(FPS)
    
    if main_menu == True:
        screen.blit(castle_img,(0,0))
        screen.blit(title_img,(54,-120))
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        if game_over == 0:
            enemy_group.update()
        #update score
            if pygame.sprite.spritecollide(player, gem_group, True):
                score += 1
            draw_text('X' + str(score), font_score, white, tile_size - 10, 10)

        enemy_group.draw(screen)
        flag_group.draw(screen)
        gem_group.draw(screen)
        
        game_over = player.update(game_over)
        
        #if player died
        if game_over == -1:
            if restart_button.draw():
                world_data =[]
                world = reset_level(level)
                game_over = 0
                score = 0

        #if player completes level
        if game_over == 1:
            #reset game and go to next level
            level += 1
            if level <= max_levels:
                #reset level
                world_data =[]
                world = reset_level(level)
                game_over = 0 
            else:
                draw_text('YOU WIN!', font, white, (SCREEN_WIDTH //2)- 140, SCREEN_HEIGHT //2)
                #restart game
                if restart_button.draw():
                    level = 1
                    world_data =[]
                    world = reset_level(level)
                    game_over = 0
                    score = 0


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
            
pygame.quit()