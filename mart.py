import pygame
import config

class PokeMart(object):

    def __init__(self, x_position, y_position):
        self.position = [x_position, y_position]
        self.image = pygame.image.load("sprites/poke_mart.png")
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)
        self.pokeballs_available = True

    def sell_pokeballs(self):
        self.pokeballs_available = False

    def render(self, screen):
        screen.blit(self.image, self.rect)