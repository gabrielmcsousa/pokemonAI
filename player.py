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
        
        self.can_pass_water = False
        self.can_pass_cave = False
        self.can_pass_mountain = False
        self.can_pass_lava = False
        
        self.obj_left = None
        self.obj_right = None
        self.obj_up = None
        self.obj_down = None

        self.pokeballs = 25

    def update(self):
        print("Player updated")

    def walk_forward(self, map, index_map):
        new_position = self.position.copy()

        if self.orientation == PlayerOri.UP:
            new_position[0] += 0
            new_position[1] += -1
        elif self.orientation == PlayerOri.DOWN:
            new_position[0] += 0
            new_position[1] += 1
        elif self.orientation == PlayerOri.LEFT:
            new_position[0] += -1
            new_position[1] += 0
        elif self.orientation == PlayerOri.RIGHT:
            new_position[0] += 1
            new_position[1] += 0

        if new_position[0] < 0 or new_position[0] > (len(map[0]) - 1):
            return
        if new_position[1] < 0 or new_position[1] > (len(map) - 1):
            return

        if map[new_position[1]][new_position[0]] == "W" and self.can_pass_water == False:
            return
        if map[new_position[1]][new_position[0]] == "C" and self.can_pass_cave == False:
            return
        if map[new_position[1]][new_position[0]] == "M" and self.can_pass_mountain == False:
            return
        if map[new_position[1]][new_position[0]] == "L" and self.can_pass_lava == False:
            return
        
        self.sense(new_position.copy(), index_map)

        self.position = new_position.copy()
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

    def sense(self, position, index_map):
        
        new_position = position
        
        up = new_position.copy()
        up[1] += -1
        
        down = new_position.copy()
        down[1] += 1
        
        left = new_position.copy()
        left[0] += -1
        
        right = new_position.copy()
        right[0] += 1

        if(index_map[up[1]][up[0]] != None):
            self.obj_up = index_map[up[1]][up[0]]
        else:
            self.obj_up = None
        if(index_map[down[1]][down[0]] != None):
            self.obj_down = index_map[down[1]][down[0]]
        else:
            self.obj_down = None
        if(index_map[left[1]][left[0]] != None):
            self.obj_left = index_map[left[1]][left[0]]
        else:
            self.obj_left = None
        if(index_map[right[1]][right[0]] != None):
            self.obj_right = index_map[right[1]][right[0]]
        else:
            self.obj_right = None
    
    def interact(self, map):
        pass


class PlayerOri():
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    TURN_LEFT = -90 #4
    TURN_RIGHT = 90 #5