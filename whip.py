import pygame
from pygame.sprite import Sprite


class Whip(Sprite):
    """This exists just because python is a pain in my derrier"""
    def __init__(self, sm_game):
        super().__init__()
        self.img              = pygame.image.load('images/Swoosh.png')
        self.img              = pygame.transform.rotate(self.img, sm_game.guy.angle / 2)
        self.whip_scale       = (sm_game.stats.whip_thickness, sm_game.stats.whip_range)
        self.img              = pygame.transform.scale(self.img, self.whip_scale)
        self.rect             = self.img.get_rect()
        self.rect.bottomright = sm_game.settings.screen_rect.center
