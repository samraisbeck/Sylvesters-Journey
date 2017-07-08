###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: character.py
# Description: Class for the main character of the game
###############################

from localVariables import *
import pygame

class Character(object):
    """ The character class """
    def __init__(self, speed=1, speedX=0, speedY=0):
        # Left images
        self.imageLeft = pygame.image.load(IMG_PATH_CHARACTER).convert_alpha()
        self.imgRunL1 = pygame.image.load(IMG_PATH_CHARACTER1).convert_alpha()
        self.imgRunL2 = pygame.image.load(IMG_PATH_CHARACTER2).convert_alpha()
        self.imgRunL3 = pygame.image.load(IMG_PATH_CHARACTER3).convert_alpha()
        self.imgRunL4 = pygame.image.load(IMG_PATH_CHARACTER4).convert_alpha()
        self.imgRunL5 = pygame.image.load(IMG_PATH_CHARACTER5).convert_alpha()
        self.imgJumpL = pygame.image.load(IMG_PATH_CHARACTERJ).convert_alpha()
        self.imagesLeft = [self.imageLeft, self.imgRunL1, self.imgRunL2, self.imgRunL3,
                           self.imageLeft, self.imgRunL4, self.imgRunL5, self.imgRunL4]
        # Right images
        self.imageRight = pygame.transform.flip(self.imageLeft, True, False)
        self.imgRunR1 = pygame.transform.flip(self.imgRunL1, True, False)
        self.imgRunR2 = pygame.transform.flip(self.imgRunL2, True, False)
        self.imgRunR3 = pygame.transform.flip(self.imgRunL3, True, False)
        self.imgRunR4 = pygame.transform.flip(self.imgRunL4, True, False)
        self.imgRunR5 = pygame.transform.flip(self.imgRunL5, True, False)
        self.imgJumpR = pygame.transform.flip(self.imgJumpL, True, False)
        self.imagesRight = [self.imageRight, self.imgRunR1, self.imgRunR2, self.imgRunR3,
                            self.imageRight, self.imgRunR4, self.imgRunR5, self.imgRunR4]
        self.imageIndex = 0
        self.imageCounter = 0
        # Movement/position variables
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.w = self.imageLeft.get_width()
        self.h = self.imageLeft.get_height()
        self.speed = speed
        self.speedX = speedX
        self.speedY = speedY
        self.direction = "left"
        self.maxSpeed = 18
        self.jumpSpeed = 17
        self.onPlat = False
        self.canJump = True
        self.canGroundPound = False
        self.canMoveRight = True
        self.canMoveLeft = True
        self.gravity = 0.7
        # Health/score/attack settings
        self.maxHealth = 50
        self.health = 50
        self.lifeBarImage = pygame.transform.scale(self.imageLeft, (20, 25))
        self.lifeBarImgW = self.lifeBarImage.get_width()
        self.lifeBarImgH = self.lifeBarImage.get_height()
        self.hasDied = False
        self.lives = 5
        self.score = 0
        self.prevLvlScore = 0
        self.attackPoints = 5
        self.hitTime = 0
        self.underAttack = False
        self.hasAttacked = False
        self.hasAttackedTime = 0
        self.escapeTime = 2000
        # Invincible
        self.invincible = False
        self.invinBubble = pygame.image.load(IMG_PATH_BUBBLE)
        self.invincibleCount = 0
        self.bubbleW = self.invinBubble.get_width()
        self.bubbleH = self.invinBubble.get_height()
        # Gravity boost
        self.gravityBoosted = False
        self.gravityCount = 0
        self.superjump = False
        self.canBoostGravity = False
        self.activatedGravity = 0
        self.activatedInvincibility = 0
        self.powerTime = 10000
        # Level clear booleans
        self.inDoorway = False
        self.levelCleared = True

        self.swordCount = 0

    def getRect(self):
        """ Returns a rect object. Useful for collisions """
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def drawLives(self, surface, x, y, spacing=20):
        """ Draws how many lives the player has left """
        for i in range(self.lives):
            x_coord = spacing+x+i*(spacing+self.lifeBarImgW)
            y_coord = y
            surface.blit(self.lifeBarImage, (x_coord, y_coord))

    def counter(self):
        """ Takes care of looping through images for animation """ 
        self.imageCounter += 1
        # The number in place of 4 controls how fast to loop through images
        if self.imageCounter >= 4:
            self.imageCounter = 0
            self.imageIndex += 1
            if self.imageIndex == len(self.imagesRight):
                self.imageIndex = 0

    def jump(self):
        """ When called, the character jumps into the air """
        self.speedY = -self.jumpSpeed
        self.onPlat = False
        self.canJump = False
        self.canGroundPound = True

    def move(self, events):
        """ Takes in pygame.event.get() as argument, and
            moves character accordingly """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.canMoveLeft:
            self.speedX = -self.speed
            self.direction = "left"
            if self.onPlat:
                self.counter()
            if not self.canMoveRight:
                self.canMoveRight = True
        elif keys[pygame.K_RIGHT] and self.canMoveRight:
            self.speedX = self.speed
            self.direction = "right"
            if self.onPlat:
                self.counter()
            if not self.canMoveLeft:
                self.canMoveLeft = True
        else:
            self.speedX = 0
            self.imageIndex = 0
        if keys[pygame.K_UP] and self.onPlat and self.canJump and not self.inDoorway:
            self.jump()
        elif self.onPlat:
            self.speedY = 0
        elif keys[pygame.K_DOWN] and self.canGroundPound:
            self.speedY = self.maxSpeed
        else:
            if self.speedY <= self.maxSpeed:
                self.speedY += self.gravity
            
    def draw(self, surface):
        """ Draws the correct character images on the screen, and the
            invincibility bubble if needed """
        if self.direction == "right":
            if self.onPlat:
                surface.blit(self.imagesRight[self.imageIndex], (self.x, self.y))
            else:
                surface.blit(self.imgJumpR, (self.x, self.y)) 
        elif self.direction == "left":
            if self.onPlat:
                surface.blit(self.imagesLeft[self.imageIndex], (self.x, self.y))
            else:
                surface.blit(self.imgJumpL, (self.x, self.y))
        if self.invincible:
            surface.blit(self.invinBubble, (self.x-self.w/3, self.y-self.h/3))

    def update(self, surface, events):
        """ Character update to be used in the main game """
        self.draw(surface)
        self.move(events)

    def stopFalling(self):
        """ Changes booleans to indicate player is on platform """
        self.onPlat = True
        self.canJump = True
        self.canGroundPound = False
		
    def stopSideMotion(self):
        """ Player cannot move sideways """
        self.speedX = 0
