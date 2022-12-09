import pygame
from baddies import Baddy
from settings import Settings
from game_stats import GameStats
import random

class Gameday:
    def __init__(self, sm_game):
        self.run      = True
        self.settings = Settings()
        self.screen   = self.settings.screen_rect
        self.stats    = GameStats()

        # Enemy draw: Dictionary of enemies and the number to choose them
        self.en_number  = 0
        self.enemy_dict = {
            'Bat':    [sm_game, 'images/Bat.bmp', (50, 50), 5, 0, 100, 1],
            'Ghost':  [sm_game, 'images/Ghost.png', (75, 75), 4, 0, 200, 2],
            'Zombie': [sm_game, 'images/Zombie.png', (100, 100), 3, 0, 400, 2],
            'Taxes':  [sm_game, 'images/Taxes.png', (100, 100), 2, 0, 500, 3]
        }

        # Enemy draw: Spawn enablers
        self.spawn_init = pygame.time.get_ticks()  # Time of last spawn
        self.spawn_trip = pygame.time.get_ticks()  # Time when called to spawn
        self.spawnpos   = (0, 0)
        self.spawn_dict = {
            'Left Column': [(-self.screen.width, -self.screen.height), (0, 2*self.screen.height)],
            'Top': [(0, -self.screen.height), (self.screen.width, 0)],
            'Bottom': [(0, self.screen.height), (self.screen.width, 2*self.screen.height)],
            'Right Column': [(self.screen.width, -self.screen.height), (2*self.screen.width, 2*self.screen.height)]
        }

    def check_spawn(self, sm_game):
        self.spawn_trip = pygame.time.get_ticks()
        if len(sm_game.Enemies) < sm_game.stats.enemy_limit:
            if (self.spawn_trip - self.spawn_init) > (self.stats.spawn_buffer * 1000):
                self._spawn(sm_game)
                self.spawn_init = pygame.time.get_ticks()

    def _spawn(self, sm_game):
        self._get_randoms()
        self._choose_enemy()
        sm_game.Enemies.add(self.enemy)
        self.x        = self.screen.centerx
        self.y        = self.screen.centery
        self.spawnpos = (self.x, self.y)

    def _get_randoms(self):
        point         = random.choice(list(self.spawn_dict.values()))
        self.x        = random.randint(point[0][0], point[1][0])
        self.y        = random.randint(point[0][1], point[1][1])
        self.spawnpos = (self.x, self.y)

    def _choose_enemy(self):
        unit = random.choice(list(self.enemy_dict.values()))
        self._gennemy(unit)

    def _gennemy(self, unit):
        unit[4] = self.spawnpos
        self.enemy = Baddy(unit[0], unit[1], unit[2], unit[3], unit[4], unit[5], unit[6])

    def show_dam(self, dam):
        font = pygame.font.SysFont("bahnschrift", 18)
        self.showdam = pygame.font.Font.render(font, str(dam), True, (255, 0, 0))
        self.settings.screen.blit(self.showdam, (self.screen.centerx,
                                                 (self.screen.centery + self.stats.DEFAULT_IMAGE_SIZE[1]/2)))

class HUD:
    def __init__(self, sm_game):
        self.HUD_Rect = [0, 0, 1920, 150]
        self.HUD_Back = (sm_game.settings.screen, (40, 40, 40), self.HUD_Rect)

        self.Health_Bar_Rect = [20, 80, 420, 50]
        self.Health_Bar = (sm_game.settings.screen, (180, 0, 0), self.Health_Bar_Rect)

        self.Health_Bar_BG_Rect = [18, 78, 424, 54]
        self.Health_Bar_BG = (sm_game.settings.screen, (0, 0, 0), self.Health_Bar_BG_Rect)

    def DrawHud(self, sm_game):
        Health_Ratio = sm_game.stats.player_health / sm_game.stats.player_health_max
        self.Health_Bar_Rect[2] = 420*Health_Ratio
        pygame.draw.rect(sm_game.settings.screen, (40, 40, 40), self.HUD_Rect)
        pygame.draw.rect(sm_game.settings.screen, (0, 0, 0), self.Health_Bar_BG_Rect)
        pygame.draw.rect(sm_game.settings.screen, (180, 0, 0), self.Health_Bar_Rect)
        font = pygame.font.SysFont("bahnschrift", 40)
        HEALTH = pygame.font.Font.render(font, "HEALTH", True, (180, 0, 0))
        sm_game.settings.screen.blit(HEALTH, (self.Health_Bar_BG_Rect[0] + 140, self.Health_Bar_BG_Rect[1] - 50))

        self.Counter(sm_game)
        self.Score(sm_game)

        if Health_Ratio <= 0:
            sm_game.game = False

    def Counter(self, sm_game):
        counting_time = pygame.time.get_ticks() - sm_game.start_time

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(counting_time // 60000).zfill(2)
        counting_seconds = str((counting_time % 60000) // 1000).zfill(2)
        counting_string = "%s:%s" % (counting_minutes, counting_seconds)
        font = pygame.font.SysFont("bahnschrift", 40)
        counting_text = font.render(str(counting_string), True, (255, 255, 255))
        self.counting_rect = counting_text.get_rect(center=sm_game.settings.screen.get_rect().center)
        self.counting_rect.top = sm_game.settings.screen.get_rect().top
        sm_game.settings.screen.blit(counting_text, self.counting_rect)

    def Score(self, sm_game):
        font = pygame.font.SysFont("bahnschrift", 40)
        scoretext = str(sm_game.stats.score)
        SCORE = pygame.font.Font.render(font, f"SCORE: {scoretext}", True, (240, 240, 240))
        sm_game.settings.screen.blit(SCORE, (self.counting_rect[0] - 30, self.Health_Bar_BG_Rect[1] - 25))

class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.size = (self.text.get_size()[0] + 30, self.text.get_size()[1] + 30)
        self.surface = pygame.Surface(self.size)
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.text, (15, 15))
        self.rect = pygame.Rect(self.x - self.size[0]/2, self.y - self.size[1]/2, self.size[0], self.size[1])

    def show(self, sm_game, button):
        sm_game.settings.screen.blit(button.surface, (self.x - self.size[0]/2, self.y - self.size[1]/2))   #____.surface

    def _click(self, sm_game, event, func):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    if func == 'QUIT':
                        quit()
                    elif func == 'START':
                        sm_game.Start = True
                    elif func == 'RESTART':
                        sm_game.stats.reset_stats()
                        sm_game.Enemies.empty()
                        sm_game.start_time = pygame.time.get_ticks()
                        sm_game.game = True


class Menus:
    def __init__(self, sm_game):
        y = sm_game.settings.screen_rect.centery
        x = sm_game.settings.screen_rect.centerx
        cen = sm_game.settings.screen_rect.center
        size = sm_game.settings.screen_rect.width, sm_game.settings.screen_rect.height
        self.Start_BG = pygame.image.load("images/MAIN_MENU.jfif").convert()
        self.Start_BG = pygame.transform.scale(self.Start_BG, size)
        self.End_BG = pygame.image.load("images/END.jpg").convert()
        self.button1 = Button("Start", (x + 600, y), 70)
        self.button2 = Button("Restart", cen, 70)
        self.button3 = Button("Quit", (x, y + 110), 40)
        self.button4 = Button("Quit", (x + 600, y + 110), 40)

    def START_MENU(self, sm_game):
        sm_game.settings.screen.blit(self.Start_BG, (0, 0))
        for event in pygame.event.get():
            self.button1._click(sm_game, event, "START")
            self.button4._click(sm_game, event, "QUIT")
        self.button1.show(sm_game, self.button1)
        self.button4.show(sm_game, self.button4)

    def END_MENU(self, sm_game):
        sm_game.settings.screen.blit(self.End_BG, (0, 0))
        for event in pygame.event.get():
            self.button2._click(sm_game, event, "RESTART")
            self.button3._click(sm_game, event, "QUIT")
        self.button2.show(sm_game, self.button2)
        self.button3.show(sm_game, self.button3)
        self._Score(sm_game)


    def _Score(self, sm_game):
        font = pygame.font.SysFont("bahnschrift", 40)
        scoretext = str(sm_game.stats.score)
        SCORE = pygame.font.Font.render(font, f"FINAL SCORE: {scoretext}", True, (0, 0, 0))
        SCORE_Rect = SCORE.get_rect(center=sm_game.settings.screen.get_rect().center)
        SCORE_Rect.y -= 200
        sm_game.settings.screen.blit(SCORE, SCORE_Rect)

