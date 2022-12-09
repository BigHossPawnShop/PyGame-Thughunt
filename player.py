import pygame
from pygame.sprite import Sprite
from settings import Settings
from game_stats import GameStats

class Guy(Sprite):
    """A class to manage the guy."""

    def __init__(self):
        """Initialize the guy and set his starting position"""
        super().__init__()
        self.settings     = Settings()
        self.stats        = GameStats()
        self.attack_range = self.stats.whip_range

        # MATH - Define the face vector and set the homie's angle
        self.Face  = self.settings.Down
        self.angle = pygame.math.Vector2.angle_to(self.Face, self.settings.Up)

        # Load the image, align it, and get its rect.
        self.image = pygame.image.load('images/monkey.bmp')
        self.image = pygame.transform.scale(self.image, self.stats.DEFAULT_IMAGE_SIZE)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect  = self.image.get_rect()

        # Generate Relative Markers
        self.Face        = self.settings.Up
        self.angle       = pygame.math.Vector2.angle_to(self.Face, self.settings.Up)
        self.OK_Attack   = False
        self.Attack_init = pygame.time.get_ticks()  # Time of Last Attack
        self.Attack_trip = pygame.time.get_ticks()  # Time when called to Attack
        self.whipn_time  = 0

        # Start at the center of the screen.
        self.rect[0] = (self.settings.screen_rect.centerx - self.stats.DEFAULT_IMAGE_SIZE[0]/2)
        self.rect[1] = (self.settings.screen_rect.centery - self.stats.DEFAULT_IMAGE_SIZE[1]/2)

    def update(self, sm_game):
        """Runtime for the guy."""
        # Key inputs, movement is an illusion
        self.keys_control(sm_game)
        # Redraw guy.
        self.settings.screen.blit(self.image, self.rect)
        self.whip(sm_game)

    def _angle_shift(self, direct):
        """Update the angle and direction vector"""
        self.angle = pygame.math.Vector2.angle_to(self.Face, direct)
        self.Face  = direct

    def keys_control(self, sm_game):
        """input checks"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            self._angle_shift(self.settings.Up)
            sm_game.stats.actor_shift_y += self.stats.guy_speed
            for quarter, pos in sm_game.map.Grid.items():
                sm_game.map.Grid[quarter][1] += self.stats.guy_speed
            self._angler_pish(sm_game)
            sm_game.whip.rect.bottomright = self.settings.screen_rect.center
        if keys[pygame.K_s]:
            self._angle_shift(self.settings.Down)
            sm_game.stats.actor_shift_y -= self.stats.guy_speed
            for quarter, pos in sm_game.map.Grid.items():
                sm_game.map.Grid[quarter][1] -= self.stats.guy_speed
            self._angler_pish(sm_game)
            sm_game.whip.rect.topleft = self.settings.screen_rect.center
        if keys[pygame.K_a]:
            self._angle_shift(self.settings.Left)
            sm_game.stats.actor_shift_x += self.stats.guy_speed
            for quarter, pos in sm_game.map.Grid.items():
                sm_game.map.Grid[quarter][0] += self.stats.guy_speed
            self._angler_pish(sm_game)
            sm_game.whip.rect.topright = self.settings.screen_rect.center
        if keys[pygame.K_d]:
            self._angle_shift(self.settings.Right)
            sm_game.stats.actor_shift_x -= self.stats.guy_speed
            for quarter, pos in sm_game.map.Grid.items():
                sm_game.map.Grid[quarter][0] -= self.stats.guy_speed
            self._angler_pish(sm_game)
            sm_game.whip.rect.bottomleft = self.settings.screen_rect.center
        if keys[pygame.K_SPACE]:
            self._check_attack()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def attack(self):
        self.Attack_trip = pygame.time.get_ticks()
        self._check_attack()
        if self.OK_Attack:
            self.whipn_time = pygame.time.get_ticks()
            if self.whipn_time > self.Attack_trip + 150:
                self.Attack_init = pygame.time.get_ticks()
                self.OK_Attack   = False

    def _check_attack(self):
        self.Attack_trip = pygame.time.get_ticks()
        if (self.Attack_trip - self.Attack_init) > self.stats.whip_delay:
            self.OK_Attack = True

    def whip(self, sm_game):
        if self.OK_Attack:
            self.settings.screen.blit(sm_game.whip.img, sm_game.whip.rect)
            pygame.sprite.Sprite.add(sm_game.whip, pygame.sprite.GroupSingle(sm_game.whip))
            print(sm_game.whip.img)
            print(sm_game.whip.rect)
            self.whipn_time += 1
            if self.whipn_time >= 60:
                self.whipn_time  = 0
                self.Attack_init = pygame.time.get_ticks()
                pygame.sprite.Sprite.kill(sm_game.whip)
                self.OK_Attack   = False

    def _angler_pish(self, sm_game):
        self.image = pygame.transform.rotate(self.image, self.angle)
        sm_game.whip.img = pygame.transform.rotate(sm_game.whip.img, self.angle)
        sm_game.whip.rect = sm_game.whip.img.get_rect()

