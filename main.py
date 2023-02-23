#import pygame
from distutils.log import error
import pygame
import time
import pandas
import geopandas
import numpy as np
from numpy.linalg import norm 
from shapely.geometry import Polygon, LineString, Point, mapping

from polygon import Unit
#initialize game engine
pygame.init()




s1 = Polygon([(0, 0), (0, 100), (100, 100),(100,0)])
s2 = Polygon([(0, 0), (0,200), (200, 200),(200, 0)])
s3 = s1.difference(s2)
lis1 = list(s1.exterior.coords)
lis2 = list(s2.exterior.coords)
lis3 = list(s3.exterior.coords)
#Open a window
size = (800, 600)
screen = pygame.display.set_mode(size)

#Set title to the window
pygame.display.set_caption("Hello World")
dead=False

#Initialize values for color (RGB format)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0, 255, 0)
BLUE=(0,0,255)
BLACK=(0,0,0)


polist = []
poligaune1 = Unit([[0, 0], [100, 0], [200, 100]],BLUE,10000)
poligaune2 = Unit([[0, 400], [100, 400], [0, 500,],[100, 500,]],RED,100)
poligaune1.setTarget([[150, 120], [100, 0], [100, 100],[0, 100],[50, 50]])
print(len(poligaune1.coordinates))
print(len(poligaune1.target))
polist.append(poligaune2)
polist.append(poligaune1)

clock = pygame.time.Clock()
all_sprites_list = pygame.sprite.Group()

while(dead==False):
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            dead = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                dead = True
        

    
    screen.fill(WHITE)
    
    for i in polist:
        i.setVelocity()
        i.move()
        for j in polist : 
            if i != j : 
                i.transformation(j)
                pass
        pygame.draw.polygon(screen, i.color, i.coordinates,1)
    



    pygame.display.flip()
    clock.tick(60)
    
#Shutdown display module
pygame.display.quit()





