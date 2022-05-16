import pygame
import config

class Player(object):
    
    def __init__(self, x_position, y_position):
        print("Player Created")
        self.position = [x_position, y_position]
        self.orientation = PlayerOri.UP
        self.image = pygame.image.load("sprites/player.png")
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print("Player updated")

    def walk_forward(self):
        if self.orientation == PlayerOri.UP:
            self.position[0] += 0
            self.position[1] += -1
        elif self.orientation == PlayerOri.DOWN:
            self.position[0] += 0
            self.position[1] += 1
        elif self.orientation == PlayerOri.LEFT:
            self.position[0] += -1
            self.position[1] += 0
        elif self.orientation == PlayerOri.RIGHT:
            self.position[0] += 1
            self.position[1] += 0
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)


    def change_orientation(self, turn_rate):
        self.orientation += turn_rate
        self.normalizeOri()


    def render(self, screen):
        screen.blit(self.image, self.rect)
    
    def normalizeOri(self):
        if(self.orientation == 360):
            self.orientation = PlayerOri.UP
        elif(self.orientation == -90):
            self.orientation = PlayerOri.LEFT
        elif(self.orientation == -180):
            self.orientation = PlayerOri.DOWN
        elif(self.orientation == -270):
            self.orientation = PlayerOri.RIGHT


class PlayerOri():
    #TODO: FIX ORIENTATION ISSUE. ONLY TURNING CLOCKWISE AND NOT DOING FULL 360
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    TURN_LEFT = -90 #4
    TURN_RIGHT = 90 #5