import random
import pygame

from os import path

from entities.entity import Entity
from config.settings import MEOWKY_SCALE

class Meowky(Entity):
    """Represents the Meowky enemy character, inheriting from the Entity class."""

    def __init__(self, x, y):
        """Initialize Meowky with position and load its images.

        Args:
            x (int): Initial x-coordinate of Meowky.
            y (int): Initial y-coordinate of Meowky.
        """
        self.load_images()
        self.image = self.images["idle_1"]

        super().__init__(x, y)

        self.stun_counter = 0  # Counter for stun duration
        self.speed_x = 2  # Horizontal movement speed

    def update_on_level(self, level, player):
        """Update Meowky's behavior and interactions within the current level.

        Args:
            level: The current level object containing platforms, trampolines, and walls.
            player: The player object to interact with.
        """
        self.update()

        # Randomly decide Meowky's movement based on player's position
        if self.state not in ["jump", "down", "left", "right"]:
            if random.random() < 0.1:
                if player.rect.y > self.rect.y:
                    if player.rect < self.rect:
                        self.move_left(level.platforms)
                    elif player.rect > self.rect:
                        self.move_right(level.platforms)

        # Idle state random movement
        if self.state == "idle":
            self.move_right(level.platforms) if random.randint(0, 1) == 0 else self.move_left(level.platforms)

        collide_list = self.list_group_collisions(level.platforms)
        horizontal_match_trampoline = None

        # Check collisions with trampolines
        for trampoline in level.trampolines:
            if (
                ((trampoline.rect.left + 2 < self.rect.left < trampoline.rect.right - 2) or
                (trampoline.rect.left + 2 < self.rect.right < trampoline.rect.right - 2)) and
                (trampoline.rect.top > self.rect.top)
            ):
                horizontal_match_trampoline = trampoline
            
            if self.rect.colliderect(trampoline.rect) and not trampoline.broken:
                self.move_up()
                trampoline.start_animation()

        # Handle horizontal alignment with trampolines
        if horizontal_match_trampoline and self.state not in ["up", "jump"]:
            tr_centerx = horizontal_match_trampoline.rect.centerx
            pl_centerx = self.rect.centerx

            if len(collide_list) == 0:
                if pl_centerx >= (tr_centerx - 15) and pl_centerx <= (tr_centerx + 15):
                    self.stop()
                    self.move_down()

        # Check collisions with platforms
        for platform in level.platforms:
            if len(collide_list) == 1 and self.rect.colliderect(platform.rect):
                if horizontal_match_trampoline and self.state in ["right", "left"]:
                    if (platform.rect.bottomleft[0] > self.rect.bottomleft[0]) and self.state != "right":
                        self.jump_to(self.rect.centerx - 40, platform.rect.midtop[1] + 1, "down")
                    elif platform.rect.bottomright[0] < self.rect.bottomright[0] and self.state != "left":
                        self.jump_to(self.rect.centerx + 40, platform.rect.midtop[1] + 1, "down")
            
            if self.state == "up":
                vertically_close = 10 < platform.rect.bottom - self.rect.bottom <= 50

                if vertically_close:
                    self.platform_change = platform
                    break
            else:
                self.platform_change = None

        # Handle vertical alignment with platforms
        if len(collide_list) == 1 and self.state in ["up"]:
            self.stop()
            self.rect.midtop = (self.rect.centerx, collide_list[0].rect.midbottom[1] + 1)

        if len(collide_list) == 1 and self.state in ["down"]:
            self.stop()
            self.rect.midbottom = (self.rect.centerx, collide_list[0].rect.midtop[1] + 1)

        # Check collisions with walls
        for wall in level.walls:
            wall.check_collision(self)

    def animate_death(self):
        """Animate Meowky's death by setting its image to the 'dead' state."""
        self.image = self.images["dead"]

    def animate(self):
        """Animate Meowky based on its current state and direction."""
        if self.state in ["left", "right"]:
            if self.animation_frame <= 2:
                if self.animation_counter % 10 == 0:
                    self.animation_frame += 1
                else:
                    if self.state == "left":
                        self.image = self.images[f"moving_left_{self.animation_frame}"]
                    else:
                        self.image = self.images[f"moving_right_{self.animation_frame}"]

                self.animation_counter += 1
            else:
                self.animation_frame = 1
    
        elif self.state in ["idle", "up", "down"]: self.image = self.images["idle_1"]

        elif self.direction in ["left", "right"]:
            if self.direction == "left":
                self.image = self.images["moving_left_1"]
            else:
                self.image = self.images["moving_right_1"]

    def load_images(self):
        """Load all images for Meowky's animations and states."""
        base_path = path.join("assets", "sprites", "meowky")

        MEOWKY_IDLE_1 = pygame.transform.scale(pygame.image.load(path.join(base_path, "static_1_meowky.png")).convert_alpha(), MEOWKY_SCALE)
        MEOWKY_IDLE_2 = pygame.transform.scale(pygame.image.load(path.join(base_path, "static_2_meowky.png")).convert_alpha(), MEOWKY_SCALE)

        MEOWKY_MOVING_LEFT_1 = pygame.transform.scale(pygame.image.load(path.join(base_path, "moving_1_meowky.png")).convert_alpha(), MEOWKY_SCALE)
        MEOWKY_MOVING_LEFT_2 = pygame.transform.scale(pygame.image.load(path.join(base_path, "moving_2_meowky.png")).convert_alpha(), MEOWKY_SCALE)
        MEOWKY_MOVING_LEFT_3 = pygame.transform.scale(pygame.image.load(path.join(base_path, "moving_3_meowky.png")).convert_alpha(), MEOWKY_SCALE)
        MEOWKY_MOVING_RIGHT_1 = pygame.transform.flip(MEOWKY_MOVING_LEFT_1, True, False)
        MEOWKY_MOVING_RIGHT_2 = pygame.transform.flip(MEOWKY_MOVING_LEFT_2, True, False)
        MEOWKY_MOVING_RIGHT_3 = pygame.transform.flip(MEOWKY_MOVING_LEFT_3, True, False)

        MEOWKY_DEAD = pygame.transform.scale(pygame.image.load(path.join(base_path, "dead_meowky.png")).convert_alpha(), MEOWKY_SCALE)

        self.images = {
            "idle_1": MEOWKY_IDLE_1,
            "idle_2": MEOWKY_IDLE_2,
            "moving_left_1": MEOWKY_MOVING_LEFT_1,
            "moving_left_2": MEOWKY_MOVING_LEFT_2,
            "moving_left_3": MEOWKY_MOVING_LEFT_3,
            "moving_right_1": MEOWKY_MOVING_RIGHT_1,
            "moving_right_2": MEOWKY_MOVING_RIGHT_2,
            "moving_right_3": MEOWKY_MOVING_RIGHT_3,
            "dead": MEOWKY_DEAD,
        }