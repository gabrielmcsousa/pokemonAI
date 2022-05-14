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


    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print("Do set up")
        self.game_state = GameState.RUNNING

    def update(self):
        self.screen.fill(config.BLACK)
        print("update")
        self.handle_events()

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