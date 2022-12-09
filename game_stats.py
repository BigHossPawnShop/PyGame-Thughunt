import pygame
from settings import Settings


class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self):
        """Initialize statistics."""
        self.settings = Settings()
        self.reset_stats()

        # Start the game in its active state
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        # Guy Settings
        self.guy_speed          = 4
        self.DEFAULT_IMAGE_SIZE = (100, 100)
        self.player_health_max  = 500
        self.player_health      = self.player_health_max
        self.score              = 0

        # Whip Settings
        self.whip_length    = 50   # Range
        self.whip_delay     = 1000  # Attack Speed (inverse), lower = faster
        self.whip_range     = 300
        self.whip_thickness = 100
        self.whip_damage    = 100

        # Enemy Settings
        self.actor_shift_y    = 0  # Shift the actors with the screen (y)
        self.actor_shift_x    = 0  # Shift the actors with the screen (x)
        self.enemy_speed      = 0.8  # Modify enemy speed
        self.spawn_buffer     = 0.5  # Seconds between enemy spawns
        self.enemy_limit      = 120  # Max number of enemies on screen
        self.enemy_health_mod = 1
        self.enemy_damage_mod = 1




def PAUSE(sm_game):
    """Freeze the game in place"""
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                if sm_game.paused == False:
                    sm_game.paused = True
                    pygame.time.wait(50)
                elif sm_game.paused == True:
                    sm_game.paused = False
            if event.key == pygame.K_ESCAPE:
                quit()