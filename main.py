import pygame
from player import Guy
from whip import Whip
from mapC import Map
from game_stats import GameStats
from game_stats import PAUSE
from draw import Gameday
from draw import HUD
from draw import Menus
from settings import Settings




class Thughunt:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Thughunt")
        self.map      = Map()
        self.clock    = pygame.time.Clock()
        self.guy      = Guy()
        self.stats    = GameStats()
        self.Enemies  = pygame.sprite.Group()
        self.spawnner = Gameday(self)
        self.settings = Settings()
        self.HUD      = HUD(self)
        self.Menus    = Menus(self)
        self.whip = Whip(self)
        self.paused   = False
        self.game = True
        self.Start = False
        self.start_time = pygame.time.get_ticks()

    def run_game(self):
        """Code Mama - Master of All Code Bata"""
        while not self.Start:
            self.Menus.START_MENU(self)
            pygame.display.flip()
        self.start_time = pygame.time.get_ticks()
        while True:
            if self.game:
                PAUSE(self)
                if not self.paused:
                    self.map.scroll()
                    self.guy.update(self)
                    self.spawnner.check_spawn(self)
                    self.Enemies.update(self)
                    self.stats.actor_shift_x = 0
                    self.stats.actor_shift_y = 0
                    self.HUD.DrawHud(self)

                    pygame.display.flip()
                    self.clock.tick()
            elif not self.game:
                self.Menus.END_MENU(self)
                pygame.display.flip()

if __name__ == '__main__':
    sm = Thughunt()
    sm.run_game()
