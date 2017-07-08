###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: enemies.py
# Description: Class for the enemies and boss of the game
###############################
import pygame
from localVariables import *
from movableObject import MovableObject
from random import choice, randint

class Enemy(MovableObject):
    """ The enemy class (all small enemies, not boss) """
    def __init__(self, imagePath, x, y, speed=1, damage=5, health=2):
        MovableObject.__init__(self, imagePath, x, y)
        self.imageRight = self.image.convert_alpha()
        self.imageRight.set_colorkey((255,255,255))
        self.imageLeft = pygame.transform.flip(self.imageRight, True, False).convert_alpha()
        self.images = [self.imageRight, self.imageLeft]
        self.imageIndex = 0
        self.speed = speed
        self.platIndex = 1     # Index of the platform the enemy is on
        self.platFound = False
        self.damage = damage   # Damage potential
        self.health = health
        self.direction = "right"
        self.bounds = 15       # The enemy's border on the platform

    def changeDirection(self):
        self.speed = -self.speed
        if self.direction == "right":
            self.direction = "left"
        else:
            self.direction = "right"
        # Changes the picture to match the direction
        self.imageIndex += 1
        self.imageIndex %= 2

    def updateSpeed(self, platforms):
        """ Updates the speed of the enemy based on its position """
        if not self.platFound:
            for platform in platforms:
                if self.getRect().colliderect(platform.getRect()):
                    self.platIndex = platforms.index(platform)
            self.platFound = True
        if self.x+self.w >= platforms[self.platIndex].getRect().right-self.bounds and \
           self.direction == "right" or self.x <= platforms[self.platIndex].x+self.bounds and \
           self.direction == "left":
            self.changeDirection()

    def draw(self, surface):
        """ Draws the enemy with correct picture """
        if self.visible:
            surface.blit(self.images[self.imageIndex], (self.x, self.y))

    def update(self, surface, characterObj):
        """ Enemy update method to be used in the game class """
        self.checkVisible()
        self.draw(surface)
        # Subtract the character's speed and add the enemy's own speed
        self.x -= characterObj.speedX
        self.x += self.speed
        self.y -= characterObj.speedY

class Boss(Enemy):
    """ Subclass of enemy, suited only for the boss """
    def __init__(self, imagePath, x, y, speed=2, damage=10, health=30):
        Enemy.__init__(self, imagePath, x, y, speed, damage, health)
        self.lastSpeedUp = 0
        self.speedInterval = 1000
        self.bounds = 40
        self.maxSpeed = 10
        self.minSpeed = 1

    def randomSpeed(self):
        """ Generate a random speed every speed interval """
        if pygame.time.get_ticks() - self.lastSpeedUp >= self.speedInterval:
            if self.direction == "right":
                self.speed = randint(self.minSpeed, self.maxSpeed)
            else:
                self.speed = -randint(self.minSpeed, self.maxSpeed)
            self.lastSpeedUp = pygame.time.get_ticks()

    def update(self, surface, characterObj):
        """ Same as enemy update except for the random speed method """
        self.checkVisible()
        self.randomSpeed()
        self.draw(surface)
        self.x -= characterObj.speedX
        self.x += self.speed
        self.y -= characterObj.speedY
        
        

        
        
