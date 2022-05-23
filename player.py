import pygame
import config
from mon import Pokemon
from mart import PokeMart
from center import PokeCenter
from trainer import Trainer

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
        self.captured_pokemons = []
        self.visited_pokeMarts = []
        self.trainers_defeated = []

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
        #self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def change_orientation(self, turn_rate):
        self.orientation += turn_rate
        self.normalizeOri()

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * config.SCALE - (camera[0] * config.SCALE), self.position[1] * config.SCALE - (camera[1] * config.SCALE), config.SCALE, config.SCALE)
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
        # FIX SENSE WHEN UP/DOWN/LEFT/RIGHT IS on -1 or 43
        
        new_position = position
        
        up = new_position.copy()
        up[1] += -1
        
        down = new_position.copy()
        down[1] += 1
        
        left = new_position.copy()
        left[0] += -1
        
        right = new_position.copy()
        right[0] += 1

        # CHECK UP
        if(up[1] <= -1):
            self.obj_up = None
        elif(index_map[up[1]][up[0]] != None):
            self.obj_up = index_map[up[1]][up[0]]
        else:
            self.obj_up = None
        
        # CHECK DOWN
        if(down[1] >= 42):
            self.obj_down = None
        elif(index_map[down[1]][down[0]] != None):
            self.obj_down = index_map[down[1]][down[0]]
        else:
            self.obj_down = None

        # CHECK LEFT
        if(left[0] <= -1):
            self.obj_left = None
        elif(index_map[left[1]][left[0]] != None):
            self.obj_left = index_map[left[1]][left[0]]
        else:
            self.obj_left = None

        # CHECK RIGHT
        if(right[0] >= 42):
            self.obj_right = None
        elif(index_map[right[1]][right[0]] != None):
            self.obj_right = index_map[right[1]][right[0]]
        else:
            self.obj_right = None
    
    def interact(self, index_map, obj_list):
        print("What's here? pos_x: {}, pos_y: {} >> ".format(self.position[0], self.position[1]) + str(type(index_map[self.position[1]][self.position[0]])))       
        object_on_index = index_map[self.position[1]][self.position[0]]

        if(type(object_on_index) == Pokemon):
            self.catch_pokemon(object_on_index, index_map, obj_list)
            
        elif(type(object_on_index) == Trainer):
            self.begin_battle(object_on_index, index_map, obj_list)

        elif(type(object_on_index) == PokeCenter):
            self.heal_pokemons()

        elif(type(object_on_index) == PokeMart):
            self.buy_pokeballs(object_on_index, index_map, obj_list)

    def catch_pokemon(self, pokemon:Pokemon, index_map, obj_list):
        if(self.pokeballs > 0):
            self.captured_pokemons.append(pokemon)
            index_map[self.position[1]][self.position[0]] = None
            obj_list.remove(pokemon)
            self.pokeballs -= 1
            print("{} captured! Only {} pokeballs on invertory and {} pokemons left! Go catch'em all !!".format(pokemon.name, self.pokeballs, (150 - len(self.captured_pokemons))))
            # Remove 5 points from score
            if(pokemon.is_electric and self.can_pass_cave == False):
                self.can_pass_cave = True
                print("Electric type pokemon captured!! You can now enter caves!!")
            if(pokemon.is_fire and self.can_pass_lava == False):
                self.can_pass_lava = True
                print("Fire type pokemon captured!! You can now walk on lava!!")
            if(pokemon.is_flying and self.can_pass_mountain == False):
                self.can_pass_mountain = True
                print("Flying type pokemon captured!! You can now fly through mountains!!")
            if(pokemon.is_water and self.can_pass_water == False):
                self.can_pass_water = True
                print("Water type pokemon captured!! You can now swim on water!!")
        else:
            print("No pokeballs available!!")

    def begin_battle(self, trainer:Trainer, index_map, obj_list):
        if(len(self.captured_pokemons) == 0):
            print("You don't have any pokemon to use in this battle! Go capture some before comming back!!")
            return
        if(Pokemon.hurt == False): # == WIN
            self.trainers_defeated.append(trainer)
            index_map[self.position[1]][self.position[0]] = None
            Pokemon.hurt = True
            obj_list.remove(trainer)
            # Add 150 points from score
            print("You won the battle and gained 150 points!!")
        else:
            # Remove 1000 points from score
            print("You were defeated and lost 1000 points! Your pokemons are hurt, seek a PokeCenter to heal them!")

    def heal_pokemons(self):
        Pokemon.hurt = False
        print("Your pokemons are fully healed !!")

    def buy_pokeballs(self, pokemart:PokeMart, index_map, obj_list):
        if(pokemart.pokeballs_available == True):
            pokemart.sell_pokeballs()
            self.pokeballs = 25
            self.visited_pokeMarts.append(pokemart)
            index_map[self.position[1]][self.position[0]] = None
            obj_list.remove(pokemart)
            print("You've replenished your invetory and the pokeballs on this PokeMart are sold-out! Next time head to another!")
            # Remove 5 points from score
        else:
            print("No pokeballs available on this PokeMart!!!")

class PlayerOri():
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    TURN_LEFT = -90 #4
    TURN_RIGHT = 90 #5