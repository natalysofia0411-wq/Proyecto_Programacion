import pygame
from os import path

from entities.entity import Entity
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAPPY_SCALE

class Mappy(Entity):
    """Represents the main character, Mappy, inheriting from the Entity class."""

    def __init__(self, x, y, lifes=4):
        """Initialize Mappy with position, lifes, and load its images.

        Args:
            x (int): Initial x-coordinate of Mappy.
            y (int): Initial y-coordinate of Mappy.
            lifes (int, optional): Number of lives Mappy starts with. Defaults to 4.
        """
        self.load_images()
        self.image = self.images["idle"]

        super().__init__(x, y)

        self.lifes = lifes

        self.death_animation_counter = 0
        self.death_animation_frame = 1

    def update(self):
        """Update Mappy's position and ensure it stays within screen bounds."""
        super().update()
        self.rect.clamp_ip(pygame.Rect(60, 0, SCREEN_WIDTH - 120, SCREEN_HEIGHT))

    def update_on_level(self, level):
        """Update Mappy's interactions with the current level, including platforms, trampolines, items, and walls.

        Args:
            level: The current level object containing platforms, trampolines, items, and walls.

        Returns:
            int: The score accumulated from interactions in the level.
        """
        score = 0
        trampoline_score = 0
        item_score = 0

        collide_list = self.list_group_collisions(level.platforms)
        player_rect = self.rect
        horizontal_match_trampoline = None

        # Check collisions with trampolines
        for trampoline in level.trampolines:
            if (
                ((trampoline.rect.left + 2 < player_rect.left < trampoline.rect.right - 2) or
                (trampoline.rect.left + 2 < player_rect.right < trampoline.rect.right - 2)) and
                (trampoline.rect.top > player_rect.top)
            ):
                horizontal_match_trampoline = trampoline
            
            trampoline_score = trampoline.check_collision(self)
            score += trampoline_score

            if trampoline_score:
                trampoline.start_animation()

            if trampoline != horizontal_match_trampoline:
                trampoline.reset()

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
            if len(collide_list) == 1 and player_rect.colliderect(platform.rect):
                if horizontal_match_trampoline and self.state in ["right", "left"]:
                    if (platform.rect.bottomleft[0] > player_rect.bottomleft[0]) and self.state != "right":
                        self.jump_to(self.rect.centerx - 50, platform.rect.midtop[1] + 1, "down")
                    if platform.rect.bottomright[0] < player_rect.bottomright[0] and self.state != "left":
                        self.jump_to(self.rect.centerx + 50, platform.rect.midtop[1] + 1, "down")
            
            if self.state == "up":
                vertically_close = 0 < platform.rect.bottom - player_rect.bottom <= 25

                if vertically_close:
                    self.platform_change = platform
                    break
            else:
                self.platform_change = None

        # Handle vertical alignment with platforms
        if len(collide_list) == 1 and self.state in ["up"]:
            self.stop()
            player_rect.midtop = (player_rect.centerx, collide_list[0].rect.midbottom[1] + 1)

        if len(collide_list) == 1 and self.state in ["down"]:
            self.stop()
            player_rect.midbottom = (player_rect.centerx, collide_list[0].rect.midtop[1] + 1)

        # Check collisions with items
        for item in level.items:
            if self.state not in ["jump", "up", "down", "idle"]:
                item_score += item.check_collision(self)

                if item_score:
                    level.items.remove(item)

                    if level.targeted_item == item.item_type:
                        level.streak = True
                        level.pairs_collected += 1
                    else:
                        level.targeted_item = item.item_type
                        level.streak = False

                    score += item_score * (level.pairs_collected + 1) if level.streak else item_score
                    break

        # Animate targeted items
        for item in level.items:
            if item.item_type == level.targeted_item:
                item.start_targeted_animation()
            else:
                item.stop_targeted_animation()

        # Check collisions with walls
        for wall in level.walls:
            wall.check_collision(self)
                
        return score

    def animate_death(self):
        """Animate Mappy's death sequence."""
        self.state = "stun"
        if self.death_animation_frame < 7:
            if self.death_animation_counter % 15 == 0:
                self.death_animation_frame += 1

            self.death_animation_counter += 1

        self.image = self.images[f"death_animation_{self.death_animation_frame}"]

    def animate(self):
        """Animate Mappy based on its current state and direction."""
        if self.state in ["left", "right"]:
            self.animation_counter += 1

            if self.animation_counter % 10 == 0:
                self.image = self.images["idle"]
            else:
                if self.state == "left":
                    self.image = self.images["moving_left"]
                else:
                    self.image = self.images["moving_right"]
    
        elif self.state == "idle": self.image = self.images["idle"]

        elif self.direction in ["left", "right"]:
            if self.direction == "left":
                self.image = self.images["jumping_left"]
            else:
                self.image = self.images["jumping_right"]

    def load_images(self):
        """Load all images for Mappy's animations and states."""
        base_path = path.join("assets", "sprites", "mappy")

        MAPPY_IDLE = pygame.transform.scale(pygame.image.load(path.join(base_path, "static_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_MOVING_LEFT = pygame.transform.scale(pygame.image.load(path.join(base_path, "moving_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_MOVING_RIGHT = pygame.transform.flip(MAPPY_MOVING_LEFT, True, False)
        MAPPY_JUMPING_LEFT = pygame.transform.scale(pygame.image.load(path.join(base_path, "jumping_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_JUMPING_RIGHT = pygame.transform.flip(MAPPY_JUMPING_LEFT, True, False)

        MAPPY_DEATH_ANIMATION_1 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_1_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_2 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_2_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_3 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_3_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_4 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_4_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_5 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_5_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_6 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_6_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_7 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_7_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_8 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_8_mappy.png")).convert_alpha(), MAPPY_SCALE)
        MAPPY_DEATH_ANIMATION_9 = pygame.transform.scale(pygame.image.load(path.join(base_path, "death_animation_9_mappy.png")).convert_alpha(), MAPPY_SCALE)

        self.images = {
            "idle": MAPPY_IDLE,
            "moving_left": MAPPY_MOVING_LEFT,
            "moving_right": MAPPY_MOVING_RIGHT,
            "jumping_left": MAPPY_JUMPING_LEFT,
            "jumping_right": MAPPY_JUMPING_RIGHT,
            "death_animation_1": MAPPY_DEATH_ANIMATION_1,
            "death_animation_2": MAPPY_DEATH_ANIMATION_2,
            "death_animation_3": MAPPY_DEATH_ANIMATION_3,
            "death_animation_4": MAPPY_DEATH_ANIMATION_4,
            "death_animation_5": MAPPY_DEATH_ANIMATION_5,
            "death_animation_6": MAPPY_DEATH_ANIMATION_6,
            "death_animation_7": MAPPY_DEATH_ANIMATION_7,
            "death_animation_8": MAPPY_DEATH_ANIMATION_8,
            "death_animation_9": MAPPY_DEATH_ANIMATION_9,
        }