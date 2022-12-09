import pygame
from settings import Settings
from game_stats import GameStats


class Map:
    """A class to manage the map"""

    def __init__(self):
        """Init"""
        self.settings = Settings()
        self.stats    = GameStats()
        self.screen   = self.settings.screen
        self.bg       = pygame.image.load('images/bg.png').convert()

        # Grid coordinates for 4 instances of the background image
        self.Grid = {
            'Q1': [-self.bg.get_width(), -self.bg.get_height()],
            'Q2': [0, -self.bg.get_height()],
            'Q3': [-self.bg.get_width(), 0],
            'Q4': [0, 0]
        }

    def scroll(self):
        """ILLUSORY MOVEMENT - SPOOKY"""
        if self.Grid['Q1'][0] < -self.bg.get_width():  # If our bg is at the -width then reset its position
            self.Grid['Q1'][0] = self.bg.get_width()
            self.Grid['Q3'][0] = self.bg.get_width()

        if self.Grid['Q4'][0] < -self.bg.get_width():
            self.Grid['Q2'][0] = self.bg.get_width()
            self.Grid['Q4'][0] = self.bg.get_width()

        if self.Grid['Q1'][0] > self.bg.get_width():  # If our bg is at the +width then reset its position
            self.Grid['Q1'][0] = -self.bg.get_width()
            self.Grid['Q3'][0] = -self.bg.get_width()

        if self.Grid['Q4'][0] > self.bg.get_width():
            self.Grid['Q2'][0] = -self.bg.get_width()
            self.Grid['Q4'][0] = -self.bg.get_width()

        if self.Grid['Q3'][1] < -self.bg.get_height():  # If our bg is at the -height (up) then reset its position
            self.Grid['Q3'][1] = self.bg.get_height()
            self.Grid['Q4'][1] = self.bg.get_height()

        if self.Grid['Q2'][1] < -self.bg.get_height():
            self.Grid['Q1'][1] = self.bg.get_height()
            self.Grid['Q2'][1] = self.bg.get_height()

        if self.Grid['Q3'][1] > self.bg.get_height():  # If our bg is at the +height (down) then reset its position
            self.Grid['Q3'][1] = -self.bg.get_height()
            self.Grid['Q4'][1] = -self.bg.get_height()

        if self.Grid['Q2'][1] > self.bg.get_height():
            self.Grid['Q1'][1] = -self.bg.get_height()
            self.Grid['Q2'][1] = -self.bg.get_height()

        for quarter, pos in self.Grid.items():
            self.screen.blit(self.bg, (self.Grid[quarter][0], self.Grid[quarter][1]))
