import pygame
import config
from player import Player
from game_state import GameState
from game_state import PlayerOri

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []


    def set_up(self):
        player = Player(24, 19)
        self.player = player
        self.objects.append(player)
        print("Do set up")
        self.game_state = GameState.RUNNING

        self.load_map("01")

    def update(self):
        self.screen.fill(config.BLACK)
        print("update")
        self.handle_events()

        self.render_map(self.screen)

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        # HANDLE QUIT EVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            # HANDLE KEY EVENT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w: # WALK FORWARD
                    self.player.walk_forward()
                elif event.key == pygame.K_d: # TURN RIGHT
                    self.player.change_orientation(PlayerOri.TURN_RIGHT)
                elif event.key == pygame.K_a: # TURN LEFT
                    self.player.change_orientation(PlayerOri.TURN_LEFT)

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


map_tile_image = {
    "G" : pygame.transform.scale(pygame.image.load("sprites/grass.png"), (config.SCALE, config.SCALE)),
    "W" : pygame.transform.scale(pygame.image.load("sprites/water.png"), (config.SCALE, config.SCALE)),
    "M" : pygame.transform.scale(pygame.image.load("sprites/mountain.png"), (config.SCALE, config.SCALE)),
    "L" : pygame.transform.scale(pygame.image.load("sprites/lava.png"), (config.SCALE, config.SCALE)),
    "C" : pygame.transform.scale(pygame.image.load("sprites/cave.png"), (config.SCALE, config.SCALE))
}