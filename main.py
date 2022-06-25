import pygame
from pygame.locals import *
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('August')

#load background image
bg_img = pygame.image.load('imgs/castle.jpeg').convert()


#set framerate
clock = pygame.time.Clock()
FPS = 60
 
#define player action variables
moving_left = False
moving_right = False

class Knight(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'{self.char_type}/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0
        
        #assign movement variables if moving left or right
        if moving_left:
           dx = -self.speed 
           self.flip = True
           self.direction = -1
        if moving_right:
            dx = +self.speed
            self.flip = False
            self.direction = 1
            
            
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy
        
            
  
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
                  
#where player/enemy on appears on screen 
player = Knight('Player', 200, 200, 3, 5)
enemy = Knight('Enemy', 200, 200, 3, 5)




run = True
while run:
     
    screen.blit(bg_img, (0, 0))

     
    clock.tick(FPS)
    
    player.draw()
    enemy.draw()
    
    player.move(moving_left, moving_right)
    
    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
            
            
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True 
            if event.key == pygame.K_ESCAPE:
                run = False
                
                
        #keyboard button released 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False  
                
    #update display            
    pygame.display.update()
pygame.quit()
