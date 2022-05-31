import math
import random
import pygame
import config
import requests
import json
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
        self.camera = [0, 0]

    def set_up(self):
        self.load_map("01")
        self.player = Player(24, 19)
        self.objects.append(self.player)
        self.pokemons = self.request_pokemons()
        self.load_assets()
        print("Gotta catch'em all !!")
        self.game_state = GameState.RUNNING

    def update(self):
        self.screen.fill(config.BLACK)
        # print(self.player.position)
        # self.handle_events()

        self.render_map(self.screen)

        for object in self.objects:
            object.render(self.screen, self.camera)

    def handle_events(self):
        for event in pygame.event.get():
            # HANDLE QUIT EVENT
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # HANDLE KEY EVENT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w:  # WALK FORWARD
                    self.player.walk_forward(self.map, self.index_map)
                elif event.key == pygame.K_d:  # TURN RIGHT
                    self.player.change_orientation(PlayerOri.TURN_RIGHT)
                elif event.key == pygame.K_a:  # TURN LEFT
                    self.player.change_orientation(PlayerOri.TURN_LEFT)
                elif event.key == pygame.K_z:  # INTERACT
                    self.player.interact(self.index_map, self.objects)
                    # if(len(self.player.captured_pokemons) == 150):
                    #     self.game_state = GameState.WIN # TODO: Implement winning screen

        # TODO: Handle prolog events

    def load_map(self, file_name):
        with open('maps/' + file_name + ".txt") as map_file:
            for line in map_file:
                tiles = []
                for i in range(0, len(line) - 1, 2):
                    tiles.append(line[i])
                self.map.append(tiles)

            # print(self.map)

    def load_assets(self):
        print("Loading Assets...")
        centers = 20
        marts = 15
        trainers = 50
        mons = 150

        rows, cols = 42, 42
        self.index_map = [([None]*cols) for i in range(rows)]
        self.index_map[self.player.position[1]
                       ][self.player.position[0]] = self.player

        poke_list = list(self.pokemons.values()).copy()
        random.shuffle(poke_list)

        # TODO: Improve spawning rules (e.g: No water pokemons, trainers, centers or marts on lava, no fire pokemons on water)
        while(centers + marts + trainers + mons > 0):
            i = random.randint(0, 41)
            j = random.randint(0, 41)
            if(self.index_map[i][j] == None):
                dice = random.randint(0, 3)

                if(dice == 0 and centers > 0):
                    self.poke_centers.append(PokeCenter(j, i))
                    self.objects.append(self.poke_centers[-1])
                    centers -= 1
                    self.index_map[i][j] = self.poke_centers[-1]
                elif(dice == 1 and marts > 0):
                    self.poke_marts.append(PokeMart(j, i))
                    self.objects.append(self.poke_marts[-1])
                    marts -= 1
                    self.index_map[i][j] = self.poke_marts[-1]
                elif(dice == 2 and trainers > 0):
                    self.poke_trainers.append(Trainer(j, i))
                    self.objects.append(self.poke_trainers[-1])
                    trainers -= 1
                    self.index_map[i][j] = self.poke_trainers[-1]
                elif(dice == 3 and mons > 0):
                    poke_name = poke_list[mons-1].name
                    self.pokemons[poke_name].set_pos(j, i)
                    self.objects.append(self.pokemons[poke_name])
                    mons -= 1
                    self.index_map[i][j] = self.pokemons[poke_name]

        if(centers == marts == trainers == mons == 0):
            print("NO MISSING ASSETS!!")
        print("Assets Loaded!")

    def render_map(self, screen):
        self.determine_camera()

        y_pos = 0
        for line in self.map:
            x_pos = 0
            for tile in line:
                image = map_tile_image[tile]
                rect = pygame.Rect(x_pos * config.SCALE - (self.camera[0] * config.SCALE), y_pos * config.SCALE - (
                    self.camera[1] * config.SCALE), config.SCALE, config.SCALE)
                screen.blit(image, rect)
                x_pos = x_pos + 1

            y_pos = y_pos + 1

    def request_pokemons(self):
        print("Loading Pokemons...")
        poke_dict = {}
        #self.poke_data = {}
        for i in range(1, 151):

            ''' # REQUESTS POKEMON DETAILS FROM API AND SAVES BOTH SIMPLIFIED JSON AND SPRITES
                # UNCOMMENT THIS IF RUNNING FOR THE FIRTS TIME
            pj = self.get_api_json('https://pokeapi.co/api/v2/pokemon/' + str(i))
            self.save_poke_json(pj, self.poke_data, i)
            self.download_pokemon_sprite(pj, name)
            '''

            # READ FROM JSON FOLDER
            name, poke_types = self.read_poke_json(
                'jsons/names_and_types.json', i)
            sprite_file = 'sprites/pokemon/' + name + ".png"

            poke_dict[name] = Pokemon(name, poke_types, sprite_file)
            #print("Pokemon: {} created!".format(name))

        print("Pokemons Loaded!")

        return poke_dict

    def get_api_json(self, url):
        poke_details = url
        poke_res = requests.get(poke_details)
        pj = poke_res.json()
        return pj

    def save_poke_json(self, poke_json, poke_data, index):
        poke_data[index] = {'name': poke_json['name']}
        poke_data[index].update({'types': [x['type']['name']
                                for x in poke_json['types']]})
        # TODO: This could be optimized. As of now it re-writes the whole file on every loop.
        with open('jsons/names_and_types.json', 'w') as f:
            json.dump(poke_data, f)
        #print("Json Saved: {}".format(poke_data))

    def read_poke_json(self, json_file, index):
        with open(json_file, 'r') as f:
            poke_data = json.load(f)
            name = poke_data[str(index)]['name']
            types = poke_data[str(index)]['types'].copy()
            return name, types

    def download_pokemon_sprite(self, json, pokemon):
        sprite_url = json['sprites']['front_default']
        img_data = requests.get(sprite_url).content
        with open('sprites/pokemon/' + pokemon + ".png", 'wb') as handler:
            handler.write(img_data)

    def determine_camera(self):
        # DETERMINE Y POSITION
        max_y_position = len(self.map) - config.SCREEN_HEIGHT / config.SCALE
        y_position = self.player.position[1] - \
            math.ceil(round(config.SCREEN_HEIGHT / config.SCALE / 2))

        if(y_position <= max_y_position and y_position >= 0):
            self.camera[1] = y_position
        elif(y_position < 0):
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_position

        # DETERMINE X POSITION
        max_x_position = len(self.map[0]) - config.SCREEN_WIDTH / config.SCALE
        x_position = self.player.position[0] - \
            math.ceil(round(config.SCREEN_WIDTH / config.SCALE / 2))

        if(x_position <= max_x_position and x_position >= 0):
            self.camera[0] = x_position
        elif(x_position < 0):
            self.camera[0] = 0
        else:
            self.camera[0] = max_x_position


map_tile_image = {
    "G": pygame.transform.scale(pygame.image.load("sprites/grass.png"), (config.SCALE, config.SCALE)),
    "W": pygame.transform.scale(pygame.image.load("sprites/water.png"), (config.SCALE, config.SCALE)),
    "M": pygame.transform.scale(pygame.image.load("sprites/mountain.png"), (config.SCALE, config.SCALE)),
    "L": pygame.transform.scale(pygame.image.load("sprites/lava.png"), (config.SCALE, config.SCALE)),
    "C": pygame.transform.scale(pygame.image.load("sprites/cave.png"), (config.SCALE, config.SCALE))
}
