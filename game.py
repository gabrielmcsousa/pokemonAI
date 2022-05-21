from urllib.request import urlopen
import pygame
import config
import requests
import io
from mon import Pokemon
from player import Player, PlayerOri
from game_state import GameState

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []
        #self.request_pokemons()
        self.pokemons = self.request_pokemons()
        
        


    def set_up(self):
        self.player = Player(24, 19)
        self.objects.append(self.player)
        print("Do set up")
        self.game_state = GameState.RUNNING

        self.load_map("01")

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
        poke_dict = {}
        for i in range(1,151):
            #REQUESTS POKEMON DETAILS FROM API
            poke_details = 'https://pokeapi.co/api/v2/pokemon/' + str(i)
            poke_res = requests.get(poke_details)
            pj = poke_res.json()
            
            # GET POKEMON NAME AND TYPES
            name = pj['name']
            poke_types = [x['type']['name'] for x in pj['types']]
            
            # GET POKEMON SPRITE AND TURN IT INTO A FILE ON MEMORY
            sprite_url = pj['sprites']['front_default']
            sprite_str = urlopen(sprite_url).read()
            sprite_file = io.BytesIO(sprite_str)

            poke_dict[name] = Pokemon(name, poke_types, sprite_file)
            self.objects.append(poke_dict[name])



map_tile_image = {
    "G" : pygame.transform.scale(pygame.image.load("sprites/grass.png"), (config.SCALE, config.SCALE)),
    "W" : pygame.transform.scale(pygame.image.load("sprites/water.png"), (config.SCALE, config.SCALE)),
    "M" : pygame.transform.scale(pygame.image.load("sprites/mountain.png"), (config.SCALE, config.SCALE)),
    "L" : pygame.transform.scale(pygame.image.load("sprites/lava.png"), (config.SCALE, config.SCALE)),
    "C" : pygame.transform.scale(pygame.image.load("sprites/cave.png"), (config.SCALE, config.SCALE))
}