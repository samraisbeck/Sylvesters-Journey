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
        self.maxHealth = health
        self.direction = "right"
        self.bounds = 15       # The enemy's border on the platform
        self.inRange = False

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

    def drawHealth(self, surface):
        if self.inRange:
            pygame.draw.rect(surface, BLACK, (self.x-1-((48-self.w)/2), self.y-16, 49, 9), 1)
            pygame.draw.rect(surface, RED, (self.x-((47-self.w)/2), self.y-15, (float(self.health)/self.maxHealth)*47, 7))

    def update(self, surface, characterObj):
        """ Enemy update method to be used in the game class """
        if not self.inRange and abs(characterObj.x - self.x) <= 0.35*WIDTH:
            self.inRange = True
        elif self.inRange and abs(characterObj.x - self.x) > 0.35*WIDTH:
            self.inRange = False
        self.checkVisible()
        self.draw(surface)
        self.drawHealth(surface)
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
        self.hasBeenVisible = False
        self.healthPic = pygame.transform.scale(self.imageRight, (int(self.w*0.6),int(self.h*0.6)))
        self.healthPicX = WIDTH/10*0.6
        self.healthBarX = WIDTH/10*1.6

    def randomSpeed(self):
        """ Generate a random speed every speed interval """
        if pygame.time.get_ticks() - self.lastSpeedUp >= self.speedInterval:
            if self.direction == "right":
                self.speed = randint(self.minSpeed, self.maxSpeed)
            else:
                self.speed = -randint(self.minSpeed, self.maxSpeed)
            self.lastSpeedUp = pygame.time.get_ticks()

    def drawHealth(self, surface):
        if self.hasBeenVisible:
            pygame.draw.rect(surface,BLACK,(self.healthBarX,HEIGHT/5, 130, 20),2)
            pygame.draw.rect(surface,BLACK,(self.healthBarX,HEIGHT/5, (float(self.health)/self.maxHealth)*130, 20))
            pygame.draw.rect(surface,RED,(self.healthPicX-5,(HEIGHT/5-(0.5*(int(self.h*0.6)-20)))-5, (self.healthBarX-self.healthPicX+140),int(self.h*0.6)+10),2)
            surface.blit(self.healthPic,(self.healthPicX, (HEIGHT/5-(0.5*(int(self.h*0.6)-20)))))

    def draw(self, surface):
        """ Draws the enemy with correct picture """
        if self.visible:
            surface.blit(self.images[self.imageIndex], (self.x, self.y))
            if not self.hasBeenVisible:
                self.hasBeenVisible = True

    def runFromSword(self, characterObj):
        if (float(self.health)/self.maxHealth)*100 <= 50 and characterObj.sword.swinging and \
           abs((self.x+self.w/2) - (characterObj.x+characterObj.w/2)) <= self.w*2 + characterObj.w/2\
           and self.direction != characterObj.direction:
            self.changeDirection()

    def update(self, surface, characterObj):
        """ Same as enemy update except for the random speed method """
        self.checkVisible()
        self.randomSpeed()
        self.runFromSword(characterObj)
        self.draw(surface)
        self.drawHealth(surface)
        self.x -= characterObj.speedX
        self.x += self.speed
        self.y -= characterObj.speedY
