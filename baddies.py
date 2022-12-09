import pygame
from pygame.sprite import Sprite
from settings import Settings
import math


class Baddy(Sprite):
    """Generic enemy class to then generate enemies"""
    def __init__(self, sm_game, picture, size, speed, spawn, health, damage):
        super().__init__()
        self.settings = Settings()
        self.stats    = sm_game.stats
        self.screen   = self.settings.screen
        self.speed    = speed
        self.size     = size
        self.health = health
        self.damage = damage

        # Perform relative vector maths
        self.dy       = 0
        self.dx       = 0
        self.vector   = [self.dx, self.dy]
        self.u_vector = [self.dx, self.dy]

        # Define the image
        self.image  = pygame.image.load(picture)
        self.image  = pygame.transform.scale(self.image, size)
        self.rect   = self.image.get_rect()
        self.rect.x = (spawn[0] - size[0]/2)
        self.rect.y = (spawn[1] - size[1] / 2)

        # Define hit buffer
        self.hit_buffer = 0
        self.hit_buffer2 = 0
        self.hit_buffer3 = 0
        self.hit_buffer4 = 0

    def update(self, sm_game):
        self.map_shift()
        self.move(sm_game)
        self.settings.screen.blit(self.image, (self.rect.centerx - self.size[0]/2, self.rect.centery - self.size[1]/2))
        self._check_collisions(sm_game)

    def map_shift(self):
        self.rect.x += self.stats.actor_shift_x
        self.rect.y += self.stats.actor_shift_y

    def move(self, sm_game):
        self.dx     = self.settings.screen_rect.center[0] - self.rect.center[0]
        self.dy     = self.settings.screen_rect.center[1] - self.rect.center[1]
        self.vector = [self.dx, self.dy]
        for i in range(0, 2):
            self.u_vector[i] = (self.vector[i])/(math.hypot(self.dx, self.dy)+1)
        self.rect.centerx += (self.u_vector[0] * sm_game.stats.enemy_speed * self.speed)
        self.rect.centery += (self.u_vector[1] * sm_game.stats.enemy_speed * self.speed)

    def _check_collisions(self, sm_game):
        if pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(sm_game.guy), False):
            self.hit_buffer = pygame.time.get_ticks()
            if self.hit_buffer - self.hit_buffer2 > 200:
                sm_game.stats.player_health -= self.damage
                sm_game.spawnner.show_dam(self.damage)
                self.hit_buffer2 = pygame.time.get_ticks()

        if sm_game.guy.OK_Attack and pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(sm_game.whip), False):
            self.hit_buffer3 = pygame.time.get_ticks()
            if self.hit_buffer3 - self.hit_buffer4 > 121:
                self.health -= sm_game.stats.whip_damage
                self.hit_buffer4 = pygame.time.get_ticks()

        if self.health <= 0:
            self.kill()
            sm_game.stats.score += 10


