###############################
# Programmer: Sam Raisbeck
# Date: May-June, 2014
# File name: main.py
# Description: Main game class which uses all other classes.
#              The game CAN run from this file as well.
###############################

## Imports ##
from localVariables import *
from plats import Plats, Wall
from character import Character
from block import Block
from powerBlock import PowerBlock, ItemBlock
from items import GravityBoost, Invincibility, Coin, Superjump, Health, \
     SwordIcon
from random import choice, randint
from enemies import Enemy, Boss
from door import Door
from button import Button
from sword import Sword
from arrow import Arrow
import math as m
import pygame, sys
pygame.init()

## BEGINNING OF THE CLASS ##
class Game(object):
    """ The main game class for the platformer """
    def __init__(self, fullscreen=False):
        self.gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
        self.inFullscreen = fullscreen
        self.inMainMenu = True
        self.bossKilled = False
        self.bossNumber = 0
        self.canClick = True
        self.musicSelected = False
        self.backgroundImage = None
        self.backgroundImage = None
        self.textGenerated = False
        self.wallsMoved = False

        self.level = 1
        self.volLevel = 1
        self.platforms = []
        self.otherMovableObjects = []
        self.pickedUpBlocks = []
        self.enemies = []
        self.staticTexts = []
        self.changingTexts = []
        self.lowestPlatIndex = 0

        self.char = Character(speed=8)
        self.char.sword = Sword(self.char.x+(self.char.w), self.char.y, (20, 70))
        self.clock = pygame.time.Clock()
        self.FPS = 70
        self.HUD = pygame.Surface((WIDTH, HEIGHT/8), pygame.SRCALPHA, 32)
        self.HUD.fill((255,255,255,100))

        self.menuPic = pygame.image.load(IMG_PATH_MAINMENU)
        self.instructionsPic = pygame.image.load(IMG_PATH_INSTRUCTIONS)
        self.storyPic = pygame.image.load(IMG_PATH_STORY)
        self.mechanicsPic = pygame.image.load(IMG_PATH_MECHANICS)
        self.lvlSelectionPic = pygame.image.load(IMG_PATH_LVLSELECT)
        self.transitionPic = pygame.image.load(IMG_PATH_TRANSITION)
        self.winPic = pygame.image.load(IMG_PATH_WIN)
        self.creditsPic = pygame.image.load(IMG_PATH_CREDITS)
        self.checkmark = pygame.image.load(IMG_PATH_CHECK)

        self.levelNames = ['"Through the first portal he goes!"', '"To the depths of Brinstar!"',
                           '"Next stop: Spiral Mountain."', '"A nice, pixelated view."',
                           '"The Maze of Mushroom Kingdom."', '"Bonus level! Your max health was increased!"',
                           '"The creepiest of them all."', '"This is it. Best of luck to you..."']

    def incrementScore(self):
        """ When called, increments the player's score """
        self.char.score += 5
        self.changingTexts[0] = self.renderText(str(self.char.score), COOL_FONT, (WIDTH/20*2.2, HEIGHT/10), BLACK, 25)

    def getDistance(self, x1, y1, x2, y2):
        """ Returns the distance between two sets of coordinates """
        return m.sqrt((x2-x1)**2 + (y2-y1)**2)

    def resetPowerups(self):
        """ Resets the powerups, including swords """
        if self.char.gravityBoosted:
            self.char.gravity /= 0.1
            self.char.jumpSpeed /= 0.35
        elif self.char.superjump:
            self.char.gravity /= 0.1
            self.char.jumpSpeed /= 0.7
        self.char.swordCount = 0
        self.char.gravityCount = 0
        self.char.invincibleCount = 0
        self.char.gravityBoosted = False
        self.char.superjump = False
        self.char.invincible = False
        self.char.sword.visible = False

    def resetTextValues(self):
        """ Method to reset the changing text values """
        self.changingTexts[0] = self.renderText(str(self.char.score), COOL_FONT, (WIDTH/20*2.2, HEIGHT/10), BLACK, 25)
        self.changingTexts[1] = self.renderText(str(len(self.pickedUpBlocks)), COOL_FONT, (WIDTH/11*10.1, HEIGHT/10), BLACK, 25)
        self.changingTexts[2] = self.renderText(str(self.char.gravityCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/30), BLACK, 20)
        self.changingTexts[3] = self.renderText(str(self.char.invincibleCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/2), BLACK, 20)
        self.changingTexts[4] = self.renderText(str(self.char.swordCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/3*2.2), BLACK, 20)

    def resetValues(self):
        """ Main reset method """
        if self.level >= 6:
            self.char.maxHealth = 80
        if self.char.levelCleared:
            self.char.prevLvlScore = self.char.score
        else:
            self.char.score = self.char.prevLvlScore
        self.pickedUpBlocks = []
        self.char.health = self.char.maxHealth
        self.platforms = []
        self.bossKilled = False
        self.bossNumber = 0
        self.otherMovableObjects = []
        self.wallsMoved = False
        self.char.inDoorway = False
        self.furthestPlatFound = False
        self.resetPowerups()
        self.resetTextValues()

    def constantEventChecks(self, keys):
        """ Takes pygame.key.get_pressed().
            Events to be checked all the time, like escape, and volume control """
        if keys[pygame.K_EQUALS] and self.volLevel < 1:
            self.volLevel += 0.01
            pygame.mixer.music.set_volume(self.volLevel)
        elif keys[pygame.K_MINUS] and self.volLevel > 0:
            self.volLevel -= 0.01
            pygame.mixer.music.set_volume(self.volLevel)
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and keys[pygame.K_f]:
            if self.inFullscreen:
                pygame.display.set_mode((WIDTH, HEIGHT))
                self.inFullscreen = False
            else:
                pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                self.inFullscreen = True

    def mainMenu(self):
        """ The main menu. Has it's own theme, and includes break-off menu loops """
        pygame.mixer.music.load(getFilepath("themeOther.mp3"))
        pygame.mixer.music.play(-1)
        playButton = Button("Play now!", WIDTH/10*7.3, HEIGHT/10, w=160, h=80, colorMouseOff=YELLOW, colorMouseOn=RED)
        selectionButton = Button("Level Selection", WIDTH/10*6.8, HEIGHT/10*2.7, w=250, h=80)
        instructionButton = Button("Instructions", WIDTH/10*7, HEIGHT/5*4, w=230, h=80)
        storyButton = Button("The Story", WIDTH/10*4.2, HEIGHT/5*4, w=170, h=80)
        mechanicsButton = Button("Mechanics",  WIDTH/10, HEIGHT/5*4, w=220, h=80)
        buttons = [playButton, selectionButton, instructionButton, storyButton,
                   mechanicsButton]
        while True:
            self.gameWindow.blit(self.menuPic, ORIGIN)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for button in buttons:
                button.checkState(events)
                button.draw(self.gameWindow)
            if playButton.pressed:
                self.inMainMenu = False
                pygame.mixer.music.fadeout(2000)
                self.gameWindow.blit(self.transitionPic, ORIGIN)
                self.drawText("Level "+str(self.level), COOL_FONT, (WIDTH/2, HEIGHT/2), GREEN, 70)
                self.drawText(str(self.levelNames[self.level-1]), COOL_FONT, (WIDTH/2, HEIGHT/5*3), GREEN, 35)
                pygame.display.update()
                pygame.time.delay(2000)
                break
            elif selectionButton.pressed:
                # Level Selection Menu
                lvl1Button = Button("Level 1", WIDTH/20*2, HEIGHT/20*7)
                lvl2Button = Button("Level 2", WIDTH/20*6, HEIGHT/20*7)
                lvl3Button = Button("Level 3", WIDTH/20*10, HEIGHT/20*7)
                lvl4Button = Button("Level 4", WIDTH/20*14, HEIGHT/20*7)
                lvl5Button = Button("Level 5", WIDTH/20*2, HEIGHT/20*14)
                lvl6Button = Button("Level 6", WIDTH/20*6, HEIGHT/20*14)
                lvl7Button = Button("Level 7", WIDTH/20*10, HEIGHT/20*14)
                lvl8Button = Button("Level 8", WIDTH/20*14, HEIGHT/20*14)
                backButton = Button("Back", WIDTH/10*7, HEIGHT/7*6, w=150, h=80, colorMouseOff=RED, colorMouseOn=YELLOW)
                lvlButtons = [lvl1Button, lvl2Button, lvl3Button, lvl4Button, lvl5Button,
                              lvl6Button, lvl7Button, lvl8Button]
                checkX = lvlButtons[self.level-1].x+20
                checkY = lvlButtons[self.level-1].y-100
                while True:
                    self.gameWindow.blit(self.lvlSelectionPic, ORIGIN)
                    events = pygame.event.get()
                    keys = pygame.key.get_pressed()
                    for button in lvlButtons:
                        button.checkState(events)
                        button.draw(self.gameWindow)
                        if button.pressed:
                            checkX, checkY = button.x+20, button.y-100
                            self.level = lvlButtons.index(button)+1
                    backButton.checkState(events)
                    backButton.draw(self.gameWindow)
                    self.gameWindow.blit(self.checkmark, (checkX, checkY))
                    if backButton.pressed:
                        break
                    self.constantEventChecks(keys)
                    pygame.display.update()
            elif instructionButton.pressed:
                # Instructions Menu
                backButton = Button("Back", WIDTH/10*7, HEIGHT/7*6, w=150, h=80, colorMouseOff=RED, colorMouseOn=YELLOW)
                while True:
                    self.gameWindow.blit(self.instructionsPic, ORIGIN)
                    events = pygame.event.get()
                    keys = pygame.key.get_pressed()
                    backButton.checkState(events)
                    backButton.draw(self.gameWindow)
                    if backButton.pressed:
                        break
                    self.constantEventChecks(keys)
                    pygame.display.update()
            elif storyButton.pressed:
                # The Story Page
                backButton = Button("Back", WIDTH/10*8, HEIGHT/13, w=150, h=80, colorMouseOff=RED, colorMouseOn=YELLOW)
                while True:
                    self.gameWindow.blit(self.storyPic, ORIGIN)
                    events = pygame.event.get()
                    keys = pygame.key.get_pressed()
                    backButton.checkState(events)
                    backButton.draw(self.gameWindow)
                    if backButton.pressed:
                        break
                    self.constantEventChecks(keys)
                    pygame.display.update()
            elif mechanicsButton.pressed:
                # Game Mechanics Menu
                backButton = Button("Back", WIDTH/10*8, HEIGHT/7*5.89, w=150, h=80, colorMouseOff=RED, colorMouseOn=YELLOW)
                while True:
                    self.gameWindow.blit(self.mechanicsPic, ORIGIN)
                    events = pygame.event.get()
                    keys = pygame.key.get_pressed()
                    backButton.checkState(events)
                    backButton.draw(self.gameWindow)
                    if backButton.pressed:
                        break
                    self.constantEventChecks(keys)
                    pygame.display.update()
            self.constantEventChecks(keys)
            pygame.display.update()

    def setMusic(self):
        """ Sets each level's theme and plays until that level is completed """
        if not self.musicSelected:
            pygame.mixer.music.load(getFilepath("theme"+str(self.level)+".mp3"))
            pygame.mixer.music.play(-1)
            self.musicSelected = True

    def setBackground(self):
        """ Sets the background for each level """
        self.backgroundImage = pygame.image.load(getFilepath("background"+str(self.level)+".jpg")).convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (WIDTH, HEIGHT)).convert()


    def readLevelData(self):
        """ Reads level data from text files based on the value of self.level,
            and places each feature into the right list based on the first
            string in each line """
        self.resetValues()
        levelData = open(getFilepath("lvl"+str(self.level)+".txt"))
        for line in levelData:
            arguments = line.split()
            if len(arguments) == 5:
                name, x, y, w, h = arguments[0], int(arguments[1]), \
                             int(arguments[2]), int(arguments[3]), \
                             int(arguments[4])
                if name == "platform":
                    self.platforms.append(Plats(IMG_PATH_PLATFORM, x, y, (w, h)))
                elif name == "platformLowest":
                    self.platforms.append(Plats(IMG_PATH_PLATFORM, x, y, (w, h)))
                    self.lowestPlatIndex = len(self.platforms)-1
                elif name == "block":
                    self.otherMovableObjects.append(Block(IMG_PATH_BLOCK, x, y, (w, h)))
                elif name == "powerBlock":
                    self.platforms.append(PowerBlock(x, y, (w, h)))
                elif name == "itemBlock":
                    self.platforms.append(ItemBlock(x, y, (w, h)))
                elif name == "coin":
                    self.otherMovableObjects.append(Coin(x, y, (w, h)))
                elif name == "heart":
                    self.otherMovableObjects.append(Health(x, y, (w, h)))
                elif name == "sword":
                    self.otherMovableObjects.append(SwordIcon(x, y, (w, h)))
                elif name == "superjump":
                    self.otherMovableObjects.append(Superjump(x, y, (w, h)))
                elif name == "gravBoost":
                    self.otherMovableObjects.append(GravityBoost(x, y, (w, h)))
                elif name == "invin":
                    self.otherMovableObjects.append(Invincibility(x, y, (w, h)))
                elif name == "arrow":
                    self.otherMovableObjects.append(Arrow(x, y, w)) # For arrow, w is angle
                elif name == "wall":
                    self.platforms.append(Wall(IMG_PATH_WALL, x, y))
                elif name == "door":
                    self.otherMovableObjects.append(Door(IMG_PATH_DOOR_CLOSED, x, y, (w, h)))
            elif len(arguments) == 6:
                # Here: s, d, h = speed, damage potential, health
                name, x, y, s, d, h = arguments[0], int(arguments[1]), \
                          int(arguments[2]), int(arguments[3]), \
                          int(arguments[4]), int(arguments[5])
                if name == "enemy":
                    if d <= 5:
                        self.enemies.append(Enemy(IMG_PATH_ENEMY1, x, y, s, d, h))
                        self.otherMovableObjects.append(Enemy(IMG_PATH_ENEMY1, x, y, s, d, h))
                    else:
                        self.enemies.append(Enemy(IMG_PATH_ENEMY2, x, y, s, d, h))
                        self.otherMovableObjects.append(Enemy(IMG_PATH_ENEMY2, x, y, s, d, h))
                elif name == "boss":
                    self.enemies.append(Boss(IMG_PATH_BOSS1, x, y, s, d, h))
                    self.otherMovableObjects.append(Boss(IMG_PATH_BOSS1, x, y, s, d, h))
                    self.bossNumber += 1
                    if self.bossNumber == 2:
                        self.otherMovableObjects[-1].healthPicX = WIDTH/10*7.3
                        self.otherMovableObjects[-1].healthBarX = WIDTH/10*8.3
                    # Sets the max speed of the boss to increase, the min speed
                    # to decrease, and the speed up interval to decrease with each level
                    self.otherMovableObjects[len(self.otherMovableObjects)-1].maxSpeed += self.level*2
                    self.otherMovableObjects[len(self.otherMovableObjects)-1].minSpeed += self.level*2
                    self.otherMovableObjects[len(self.otherMovableObjects)-1].speedInterval -= 55*self.level
            else:
                pass
        self.char.levelCleared = False
        self.char.hasDied = False

    def generateTexts(self):
        """ Generates the texts to be displayed on the main game window at all times """
        self.staticTexts = [self.renderText("Health: ", COOL_FONT, (WIDTH/17, HEIGHT/20), BLACK, 25),
                      self.renderText("Score: ", COOL_FONT, (WIDTH/20, HEIGHT/10), BLACK, 25),
                      self.renderText("Lives: ", COOL_FONT, (WIDTH/4*2.9, HEIGHT/20), BLACK, 25),
                      self.renderText("Spare Platforms: ", COOL_FONT, (WIDTH/10*7.95, HEIGHT/10), BLACK, 25),
                      self.renderText("1. Gravity Boosts: ", COOL_FONT, (WIDTH/20*8, HEIGHT/30), BLACK, 20),
                      self.renderText("2. Invincibilities: ", COOL_FONT, (WIDTH/20*8.1, HEIGHT/8/2), BLACK, 20),
                      self.renderText("3. Swords: ", COOL_FONT, (WIDTH/20*8.6, HEIGHT/8/3*2.2), BLACK, 20)]
# This is a list of texts that need to be "re-rendered" with certain events, like grabbing a block
# or gaining/losing score.
        self.changingTexts = [self.renderText(str(self.char.score), COOL_FONT, (WIDTH/20*2.2, HEIGHT/10), BLACK, 25),
                              self.renderText(str(len(self.pickedUpBlocks)), COOL_FONT, (WIDTH/11*10.1, HEIGHT/10), BLACK, 25),
                              self.renderText(str(self.char.gravityCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/30), BLACK, 20),
                              self.renderText(str(self.char.invincibleCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/2), BLACK, 20),
                              self.renderText(str(self.char.swordCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/3*2.2), BLACK, 20)]
        self.textGenerated = True

    def redrawGameWindow(self):
        """ Redraw the main game window """
        self.gameWindow.blit(self.backgroundImage, ORIGIN)
        events = pygame.event.get()
        wallCount = 0
        for platform in self.platforms:
            if isinstance(platform, Wall) and self.bossKilled and not self.wallsMoved:
                wallCount += 1
                # Moves last 2 walls up when boss is killed (these are always the ones blocking the portal)
                if wallCount == 3 or wallCount == 4:
                    platform.y -= 200
                    self.wallsMoved = True
            platform.update(self.gameWindow, self.char)
        for obj in self.otherMovableObjects:
            # Only be able to use superjump when boss is killed
            if isinstance(obj, Superjump) and self.bossKilled:
                obj.canBeUsed = True
            if isinstance(obj, Enemy) or isinstance(obj, Boss):
                obj.updateSpeed(self.platforms)
            obj.update(self.gameWindow, self.char)
        self.gameWindow.blit(self.HUD, ORIGIN)
        self.drawTimers()
        if self.char.sword.visible:
            self.char.sword.update(self.gameWindow, self.char, events)
        self.char.update(self.gameWindow, events)
        for text in self.staticTexts:
            font, coords = text
            self.gameWindow.blit(font, coords)
        for text in self.changingTexts:
            font, coords = text
            self.gameWindow.blit(font, coords)
        pygame.draw.rect(self.gameWindow, BLACK, (WIDTH/9, HEIGHT/28, 100, 20), 1)
        pygame.draw.rect(self.gameWindow, BLACK,
                         (WIDTH/9, HEIGHT/28, (float(self.char.health)/self.char.maxHealth)*100, 20))
        self.char.drawLives(self.gameWindow, WIDTH/4*3, HEIGHT/20-13)
        pygame.display.update()

    def keyEvents(self):
        """ Checks for key events like using items """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.char.inDoorway or keys[pygame.K_LSHIFT] and keys[pygame.K_s] \
           and keys[pygame.K_a] and keys[pygame.K_m]:
            # Win screen sequence (the part after the 'or' above is a cheat code. Shhh...)
            if self.level == 8:
                pygame.time.delay(1000)
                while True:
                    self.gameWindow.blit(self.winPic, ORIGIN)
                    self.drawText("Your final score: "+str(self.char.score), COOL_FONT, (WIDTH/2, HEIGHT/10*6.4), GREEN, 40)
                    events = pygame.event.get()
                    keys = pygame.key.get_pressed()
                    self.constantEventChecks(keys)
                    if keys[pygame.K_RETURN]:
                        self.creditScreen()
                    pygame.display.update()
            else:
                pygame.time.delay(500)
                self.level += 1
                self.char.levelCleared = True
                self.gameWindow.blit(self.transitionPic, ORIGIN)
                self.drawText("Level "+str(self.level), COOL_FONT, (WIDTH/2, HEIGHT/2), GREEN, 70)
                self.drawText(str(self.levelNames[self.level-1]), COOL_FONT, (WIDTH/2, HEIGHT/5*3), GREEN, 35)
                self.musicSelected = False
                pygame.mixer.music.fadeout(2000)
                pygame.display.update()
                pygame.time.delay(2000)
        elif keys[pygame.K_1] and not self.char.gravityBoosted and \
             not self.char.superjump and self.char.gravityCount > 0:
            self.char.gravityBoosted = True
            self.char.canBoostGravity = True
            self.char.activatedGravity = pygame.time.get_ticks()
            self.char.gravityCount -= 1
            self.changingTexts[2] = self.renderText(str(self.char.gravityCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/30), BLACK, 20)
        elif keys[pygame.K_2] and not self.char.invincible and self.char.invincibleCount > 0:
            self.char.invincible = True
            self.char.activatedInvincibility = pygame.time.get_ticks()
            self.char.invincibleCount -= 1
            self.changingTexts[3] = self.renderText(str(self.char.invincibleCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/2), BLACK, 20)
        elif keys[pygame.K_3] and not self.char.sword.visible and self.char.swordCount > 0:
            self.char.sword = Sword(self.char.x+(self.char.w), self.char.y, (20, 70))
            self.char.swordCount -= 1
            self.char.sword.visible = True
            self.changingTexts[4] = self.renderText(str(self.char.swordCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/3*2.2), BLACK, 20)
        self.constantEventChecks(keys)

    def renderText(self, text, font, coordinates, color, size):
        """ First text function: returns coordinates and rect (only renders once)
            For text that needs to be displayed most of the game """
        font = pygame.font.Font(font, size)
        text = str(text)
        surface_font = font.render(text, True, color)
        fontrect = surface_font.get_rect()
        fontrect.center = coordinates
        return surface_font, fontrect

    def drawText(self, text, font, coordinates, color, size):
        """ Second text function: draws text on screen (renders everytime it has to blit)
            For menu screen, between levels screen, etc. """
        font = pygame.font.Font(font, size)
        text = str(text)
        surface_font = font.render(text, True, color)
        fontrect = surface_font.get_rect()
        fontrect.center = coordinates
        self.gameWindow.blit(surface_font, fontrect)

    def generatePower(self, platform):
        """ Takes a platform as parameter and generates power/sword \
            objects and randomly chooses one to use """
        gravityItem = GravityBoost(platform.x+platform.w/2-15, platform.y-50, (30, 30))
        invincibleItem = Invincibility(platform.x+platform.w/2-15, platform.y-50, (30, 30))
        swordItem = SwordIcon(platform.x+platform.w/2-5, platform.y-80, (25, 65))
        self.otherMovableObjects.append(choice([swordItem, gravityItem, invincibleItem]))

    def generateItem(self, platform):
        """ Takes platform as parameter and generates item objects
            and randomly chooses one to use """
        blockItem = Block(IMG_PATH_BLOCK, platform.x+platform.w/2-15, platform.y-50, (30, 30))
        healthItem = Health(platform.x+platform.w/2-15, platform.y-50, (30, 30))
        coinItem = Coin(platform.x+platform.w/2-15, platform.y-50, (30, 30))
        self.otherMovableObjects.append(choice([healthItem, coinItem, blockItem]))

    def checkSideCollide(self):
        """ Checks collisions with the side of the platform """
        for platform in self.platforms:
            if self.char.getRect().colliderect(platform.getRect()) and \
               self.char.getRect().right < platform.getRect().left + 9 and \
               self.char.direction == "right" and self.char.getRect().bottom > platform.y+2 \
               or self.char.getRect().colliderect(platform.getRect()) \
               and self.char.getRect().left > platform.getRect().right - 9 and \
               self.char.direction == "left" and self.char.getRect().bottom > platform.y+2:
                self.char.stopSideMotion()

    def checkOtherCollide(self):
        """ Checks top/bottom collisions of platforms """
        for platform in self.platforms:
            if self.char.getRect().colliderect(platform.getRect()) and \
                 self.char.getRect().top > platform.getRect().bottom - 20 and \
                 self.char.getRect().left < platform.getRect().right-3 and \
                 self.char.getRect().right > platform.getRect().left+3 and self.char.speedY < 0:
                self.char.speedY = 1
                if isinstance(platform, PowerBlock) and not platform.hit:
                    platform.hit = True
                    if not isinstance(platform, ItemBlock):
                        self.generatePower(platform)
                    else:
                        self.generateItem(platform)
            elif self.char.getRect().colliderect(platform.getRect()) and \
               self.char.getRect().bottom < platform.y+25 and \
               self.char.x < platform.x+platform.w-7 and self.char.x+self.char.w-7 \
               > platform.x:
                # Makes sure the character is always right on the platform (no overlaps)
                overlap = self.char.y+self.char.h-1 > platform.y
                if overlap:
                    platCharOverlap = (self.char.y+self.char.h) - platform.y-1
                    self.char.speedY = -platCharOverlap
                self.char.stopFalling()
                # No need to check other platforms after character is found on one
                break
            self.char.onPlat = False

    def checkObjectCollide(self):
        """ Checks collisions with items/enemies/interactable objects.
            Each time score, pickedUpPlatforms, etc increases/decreases,
            new font has to be rendered """
        for obj in self.otherMovableObjects:
            if self.char.getRect().colliderect(obj.getRect()):
                if isinstance(obj, Block) and not obj.placed:
                    self.pickedUpBlocks.append(obj)
                    self.changingTexts[1] = self.renderText(str(len(self.pickedUpBlocks)), COOL_FONT, (WIDTH/11*10.1, HEIGHT/10), BLACK, 25)
                    self.otherMovableObjects.remove(obj)
                elif isinstance(obj, SwordIcon):
                    self.char.swordCount += 1
                    self.changingTexts[4] = self.renderText(str(self.char.swordCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/3*2.2), BLACK, 20)
                    self.otherMovableObjects.remove(obj)
                elif isinstance(obj, Coin):
                    self.incrementScore()
                    self.otherMovableObjects.remove(obj)
                elif isinstance(obj, Health):
                    if self.char.maxHealth-self.char.health >= 5:
                        self.char.health += 5
                    else:
                        self.char.health = self.char.maxHealth
                    self.otherMovableObjects.remove(obj)
                elif isinstance(obj, GravityBoost) or isinstance(obj, Superjump) and \
                     obj.canBeUsed:
                    if not self.char.superjump and isinstance(obj, Superjump):
                        self.char.superjump = True
                        self.char.activatedGravity = pygame.time.get_ticks()
                        self.char.canBoostGravity = True
                        self.otherMovableObjects.remove(obj)
                    else:
                        self.char.gravityCount += 1
                        self.changingTexts[2] = self.renderText(str(self.char.gravityCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/30), BLACK, 20)
                        self.otherMovableObjects.remove(obj)
                elif isinstance(obj, Invincibility):
                    self.char.invincibleCount += 1
                    self.changingTexts[3] = self.renderText(str(self.char.invincibleCount), COOL_FONT, (WIDTH/20*9.8, HEIGHT/8/2), BLACK, 20)
                    self.otherMovableObjects.remove(obj)
                elif isinstance(obj, Door):
                    obj.opened = True
                    self.char.inDoorway = True
                elif isinstance(obj, Enemy) or isinstance(obj, Boss):
                    if obj.getRect().colliderect(self.char.getRect()) and \
                       self.char.getRect().bottom <= obj.y+19 and self.char.speedY > 0:
                        obj.health -= self.char.attackPoints
                        temp = randint(1,20)
                        if (isinstance(obj, Boss) and temp <= 9) or (isinstance(obj, Enemy) and temp <= 4):
                            obj.changeDirection()
                        self.char.hasAttacked = True
                        self.char.hasAttackedTime = pygame.time.get_ticks()
                        self.incrementScore()
                        if self.char.gravityBoosted:
                            self.char.speedY = -3
                        else:
                            self.char.speedY = -10
                        self.char.canGroundPound = False
                    if obj.getRect().colliderect(self.char.getRect()) and not self.char.underAttack \
                         and not self.char.hasAttacked:
                        if not self.char.invincible:
                            self.char.health -= obj.damage
                            self.char.underAttack = True
                            self.char.hitTime = pygame.time.get_ticks()
                        elif self.char.invincible and isinstance(obj, Boss):
                            self.char.health -= obj.damage-5
                            self.char.underAttack = True
                            self.char.hitTime = pygame.time.get_ticks()
                        else:
                            pass
            # These are if the character isn't colliding with the object
            elif isinstance(obj, Door):
                obj.opened = False
                self.char.inDoorway = False
            if self.char.sword.visible and obj.getRect().colliderect(self.char.sword.rect) and \
               self.char.sword.swinging and self.char.sword.canHit:
                if isinstance(obj, Enemy) or isinstance(obj, Boss):
                    obj.health -= 10
                    if obj.direction != self.char.direction:
                        obj.changeDirection()
                    self.incrementScore()
                    self.char.sword.canHit = False
            if isinstance(obj, Enemy) and obj.health <= 0 or isinstance(obj, Boss) and obj.health <= 0:
                obj.visible = False
                self.otherMovableObjects.remove(obj)
                temp2 = randint(1,20)
                if (float(self.char.health)/self.char.maxHealth)*100 <= 50 and temp2 <= 6:
                    self.otherMovableObjects.append(Health(self.char.x-60, self.char.y-20, (30,30)))
                    self.otherMovableObjects.append(Health(self.char.x+self.char.w+30, self.char.y-20, (30,30)))
                    if temp2 <= 3:
                        self.otherMovableObjects.append(Health(self.char.x-60, self.char.y+15, (30,30)))
                        self.otherMovableObjects.append(Health(self.char.x+self.char.w+30, self.char.y+15, (30,30)))
                        print temp2
                self.incrementScore()
                if isinstance(obj, Boss):
                    self.bossNumber -= 1
                    if self.bossNumber == 0:
                        self.bossKilled = True

    def allCollision(self):
        """ Groups all collision methods """
        self.checkObjectCollide()
        self.checkOtherCollide()
        self.checkSideCollide()

    def characterPowers(self):
        """ Checks for the use of superjump or gravity boost """
        if self.char.gravityBoosted and self.char.onPlat and self.char.canBoostGravity:
            self.char.gravity *= 0.1
            self.char.jumpSpeed *= 0.35
            self.char.canBoostGravity = False
        elif self.char.superjump and self.char.onPlat and self.char.canBoostGravity:
            self.char.gravity *= 0.1
            self.char.jumpSpeed *= 0.7
            self.char.canBoostGravity = False

    def drawTimers(self):
        """ Draws the timers if needed """
        if self.char.gravityBoosted or self.char.superjump:
            self.drawText("Gravity Boost: "+str((self.char.activatedGravity+self.char.powerTime+1000 - \
                                            pygame.time.get_ticks())/1000), \
                          COOL_FONT, (WIDTH/2, HEIGHT/20*3), RED, 30)
        if self.char.invincible:
            self.drawText("Invincibility: "+str((self.char.activatedInvincibility+self.char.powerTime+1000 - \
                                            pygame.time.get_ticks())/1000), \
                          COOL_FONT, (WIDTH/2, HEIGHT/20*4), RED, 30)
        if self.char.underAttack:
            self.drawText("Escape: "+str((self.char.hitTime+self.char.escapeTime+1000 - \
                                          pygame.time.get_ticks())/1000), \
                          COOL_FONT, (WIDTH/2, HEIGHT/20*5), RED, 30)

    def timeEvents(self):
        """ Time events like powers and escape time """
        if self.char.gravityBoosted and \
           pygame.time.get_ticks() - self.char.activatedGravity >= self.char.powerTime \
           or self.char.superjump and \
           pygame.time.get_ticks() - self.char.activatedGravity >= self.char.powerTime:
            self.char.gravity /= 0.1
            if self.char.gravityBoosted:
                self.char.jumpSpeed /= 0.35
                self.char.gravityBoosted = False
            else:
                self.char.jumpSpeed /= 0.7
                self.char.superjump = False
        if self.char.invincible and \
           pygame.time.get_ticks() - self.char.activatedInvincibility >= self.char.powerTime:
            self.char.invincible = False
        if self.char.underAttack and \
           pygame.time.get_ticks() - self.char.hitTime >= self.char.escapeTime:
            self.char.underAttack = False
        if self.char.hasAttacked and \
           pygame.time.get_ticks() - self.char.hasAttackedTime >= 200:
            self.char.hasAttacked = False

    def placeBlock(self):
        """ Checks for mouse clicks to place blocks """
        mousex, mousey = pygame.mouse.get_pos()
        events = pygame.event.get()
        if pygame.mouse.get_pressed()[0] and len(self.pickedUpBlocks) > 0 and self.canClick:
            placedBlock = Block(IMG_PATH_BLOCK, mousex, mousey, (100, 20))
            self.platforms.append(placedBlock)
            self.pickedUpBlocks.remove(self.pickedUpBlocks[0])
            self.changingTexts[1] = self.renderText(str(len(self.pickedUpBlocks)), COOL_FONT, (WIDTH/11*10.1, HEIGHT/10), BLACK, 25)
            placedBlock.placed = True
            self.canClick = False
        elif not pygame.mouse.get_pressed()[0]:
            self.canClick = True

    def checkDead(self):
        """ Checks if the character has died """
        if self.char.y > self.platforms[self.lowestPlatIndex].y + 1000 or \
           self.char.health <= 0:
            self.char.lives -= 1
            self.char.hasDied = True
            self.gameWindow.fill(BLACK)
            lifeWord = ""
            # Grammar for the win
            if self.char.lives == 1:
                lifeWord = "life"
            else:
                lifeWord = "lives"
            if self.char.lives == 0:
                pygame.mixer.music.fadeout(2000)
            self.drawText(str(self.char.lives)+" "+lifeWord+" remaining.", COOL_FONT,
                          (WIDTH/2, HEIGHT/2), RED, 70)
            pygame.display.update()
            pygame.time.delay(2000)

    def gameOver(self):
        """ Game over screen """
        pygame.mixer.music.load(getFilepath("gameOver.mp3"))
        pygame.mixer.music.play(-1)
        while True:
            self.gameWindow.fill(BLACK)
            self.drawText("Game over!", COOL_FONT, (WIDTH/2, HEIGHT/4), RED, 70)
            self.drawText("Your final score: "+str(self.char.score), COOL_FONT, (WIDTH/2, HEIGHT/4*2), WHITE, 40)
            self.drawText("Hit enter to see the credits. Thanks for playing!", COOL_FONT, (WIDTH/2, HEIGHT/4*3), WHITE, 40)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            self.constantEventChecks(keys)
            if keys[pygame.K_RETURN]:
                self.creditScreen()
            pygame.display.update()

    def creditScreen(self):
        """ Screen that displays the credits """
        while True:
            self.gameWindow.blit(self.creditsPic, ORIGIN)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            self.constantEventChecks(keys)
            pygame.display.update()



    def execute(self):
        """ Main execute method """
        self.clock.tick(self.FPS)
        if not self.textGenerated:
            self.generateTexts()
        if self.inMainMenu:
            self.mainMenu()
        self.setMusic()
        if self.char.levelCleared or self.char.hasDied:
            if self.char.levelCleared:
                self.setBackground()
            self.readLevelData()
        self.redrawGameWindow()
        self.keyEvents()
        self.allCollision()
        self.characterPowers()
        self.checkDead()
        self.placeBlock()
        self.timeEvents()
        if self.char.lives <= 0:
            self.gameOver()
            pygame.quit()
            sys.exit(0)

# You can start the game from this file as well as runGame.py.
g = Game()
while True:
    g.execute()
