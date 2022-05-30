import pygame
import config
from game import Game
from game_state import GameState
from IPython.display import clear_output
from prologIntegration import BaseQuery

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

pygame.display.set_caption("PrologMon")

clock = pygame.time.Clock()

game = Game(screen)
game.set_up()
base = BaseQuery(game.map, game.index_map)
base.insert_map_facts()
base.run(True)
while game.game_state == GameState.RUNNING:
    clock.tick(50)
    game.update()
    pygame.display.flip()
