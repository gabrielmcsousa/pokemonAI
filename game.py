import random
import pygame
import config
import requests
from center import PokeCenter
from mart import PokeMart
from trainer import Trainer
from mon import Pokemon
from player import Player, PlayerOri
from game_state import GameState

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []
        self.poke_centers = []
        self.poke_marts = []
        self.poke_trainers = []             
        

    def set_up(self):
        self.load_map("01")
        self.player = Player(24, 19)
        self.objects.append(self.player)
        self.pokemons = self.request_pokemons()
        self.load_assets()
        print("Do set up")
        self.game_state = GameState.RUNNING
        


    def update(self):
        self.screen.fill(config.BLACK)
        #print(self.player.position)
        self.handle_events()

        self.render_map(self.screen)

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            # HANDLE QUIT EVENT
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # HANDLE KEY EVENT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w: # WALK FORWARD
                    self.player.walk_forward(self.map)
                elif event.key == pygame.K_d: # TURN RIGHT
                    self.player.change_orientation(PlayerOri.TURN_RIGHT)
                elif event.key == pygame.K_a: # TURN LEFT
                    self.player.change_orientation(PlayerOri.TURN_LEFT)
                elif event.key == pygame.K_z: # INTERACT
                    self.player.interact(self.map)

        #TODO: Handle prolog events

    def load_map(self, file_name):
        with open('maps/' + file_name + ".txt") as map_file:
            for line in map_file:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.map.append(tiles)

            #print(self.map)

    def load_assets(self):
        print("Loading Assets...")
        centers = 20
        marts = 15
        trainers = 50
        mons = 150
        count = 0

        poke_list = list(self.pokemons.values()).copy()
        random.shuffle(poke_list)

        for i in range(len(self.map[0])):
            for j in range(len(self.map[1])):
                dice = random.randint(0,8)

                if(dice == 0):
                    continue
                elif(dice == 2 and centers > 0 and count <= 0):
                    self.poke_centers.append(PokeCenter(j, i))
                    self.objects.append(self.poke_centers[-1])
                    centers -= 1
                    count = 5
                elif(dice == 4 and marts > 0 and count <= 0):
                    self.poke_marts.append(PokeMart(j, i))
                    self.objects.append(self.poke_marts[-1])
                    marts -= 1
                    count = 5
                elif(dice == 6 and trainers > 0 and count <= 0):
                    self.poke_trainers.append(Trainer(j, i))
                    self.objects.append(self.poke_trainers[-1])
                    trainers -= 1
                    count = 5
                elif(dice == 8 and mons > 0):
                    poke_name = poke_list[mons-1].name
                    self.pokemons[poke_name].set_pos(j, i)
                    self.objects.append(self.pokemons[poke_name])
                    mons -= 1
                count -= 1
        print("Assets Loaded!")

    def render_map(self, screen):
        y_pos = 0
        for line in self.map:
            x_pos = 0
            for tile in line:
                image = map_tile_image[tile]
                rect = pygame.Rect(x_pos * config.SCALE, y_pos * config.SCALE, config.SCALE, config.SCALE)
                screen.blit(image, rect)
                x_pos = x_pos + 1

            y_pos = y_pos + 1

    def request_pokemons(self):
        print("Loading Pokemons...")
        poke_dict = {}
        for i in range(1,151):
            #REQUESTS POKEMON DETAILS FROM API
            poke_details = 'https://pokeapi.co/api/v2/pokemon/' + str(i)
            poke_res = requests.get(poke_details)
            pj = poke_res.json()
            
            # GET POKEMON NAME AND TYPES
            name = pj['name']
            poke_types = [x['type']['name'] for x in pj['types']]
            
            # DOWNLOAD POKEMON SPRITES (UNCOMMENT IF NEEDED)
            # sprite_url = pj['sprites']['front_default']
            # img_data = requests.get(sprite_url).content
            # with open('sprites/pokemon/' + name + ".png", 'wb') as handler:
            #     handler.write(img_data)
            
            sprite_file = 'sprites/pokemon/' + name + ".png"

            poke_dict[name] = Pokemon(name, poke_types, sprite_file)
            print("Pokemon: {} created!".format(name))
            #self.objects.append(poke_dict[name])
            
        print("Pokemons Loaded!")
        
        return poke_dict



map_tile_image = {
    "G" : pygame.transform.scale(pygame.image.load("sprites/grass.png"), (config.SCALE, config.SCALE)),
    "W" : pygame.transform.scale(pygame.image.load("sprites/water.png"), (config.SCALE, config.SCALE)),
    "M" : pygame.transform.scale(pygame.image.load("sprites/mountain.png"), (config.SCALE, config.SCALE)),
    "L" : pygame.transform.scale(pygame.image.load("sprites/lava.png"), (config.SCALE, config.SCALE)),
    "C" : pygame.transform.scale(pygame.image.load("sprites/cave.png"), (config.SCALE, config.SCALE))
}