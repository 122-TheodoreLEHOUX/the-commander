import math
import pygame


WHITE = (255, 255, 255)
BLUE = (255, 100, 0)

class Unit(pygame.sprite.Sprite):
    def __init__(self,coo):
        super().__init__()
        self.target=[100,300]
        self.direction=[0,0]
        self.coordinates = coo
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
 
        pygame.draw.polygon(self.image, BLUE, [0, 0, 10, 10])

        self.rect = self.image.get_rect()

    def setDirection(self):
        if self.rect.x == self.target[0] and self.rect.y == self.target[1]:
            self.direction[0] = 0
            self.direction[1] = 0
        else:
            angle = math.atan2((self.target[0] - self.rect.x),(self.target[1] - self.rect.y))
            self.direction[0] = math.cos(angle)
            self.direction[1] = math.sin(angle)

    def move(self):
        self.setDirection()
        self.rect.x += round(self.direction[0]*2)
        self.rect.y += round(self.direction[1]*2)

    def setTarget(self):
        print('target',self.target)
 
    def reverse(self):
        self.target[0] = (-1)* self.direction[0] + self.rect.x
        self.target[1] = (-1)*self.direction[1] + self.rect.y