import pygame
import config


class Pokemon(object):
    
    hurt = False

    def __init__(self, name, type, sprite):
        self.type = type
        self.name = name
        self.image = pygame.image.load(sprite)
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)
        self.is_flying = 'flying' in self.type
        self.is_fire = 'fire' in self.type
        self.is_water = 'water' in self.type
        self.is_electric = 'electric' in self.type


    def set_pos(self, pos):
        self.position = pos
        
    def render(self, screen):
        screen.blit(self.image, self.rect)