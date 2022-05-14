import pygame
import config
from game_state import PlayerOri

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


    def change_orientation(self, side):
        if side == PlayerOri.TURN_LEFT:
            self.orientation -= 90
        elif side == PlayerOri.TURN_RIGHT:
            self.orientation += 90


    def render(self, screen):
        screen.blit(self.image, self.rect)