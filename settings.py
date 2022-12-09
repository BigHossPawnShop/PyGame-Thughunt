import pygame

class Settings:
    """A class to store all settings for ALien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""

        #Screen Settings
        self.screen_width  = 1200
        self.screen_height = 800
        self.bg_color      = (55, 0, 55)
        self.screen        = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect   = self.screen.get_rect()

        #VECTORS
        self.Right = pygame.math.Vector2((self.screen_rect.right - self.screen_rect.centerx), 0)
        self.Left  = pygame.math.Vector2((self.screen_rect.left - self.screen_rect.centerx), 0)
        self.Up    = pygame.math.Vector2(0, -(self.screen_rect.top - self.screen_rect.centery))
        self.Down  = pygame.math.Vector2(0, -(self.screen_rect.bottom - self.screen_rect.centery))




