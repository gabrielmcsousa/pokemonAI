import pygame
import config
from game import Game
from game_state import GameState
from IPython.display import clear_output
from prologIntegration import BaseQuery

screen = pygame.display.set_mode(
    (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
game = Game(screen)
game.set_up()
base = BaseQuery(game.map, game.index_map)
print(game.map)
base.insert_map_facts()

base.run(game, True)

# while game.game_state == GameState.RUNNING:
