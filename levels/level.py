import pygame
from os import path

from structures.trampoline import Trampoline
from structures.platform import Platform
from structures.wall import Wall

from entities.item import Item
from entities.meowky import Meowky
from entities.door import Door
from entities.wave import Wave

from utils.helpers import get_level_matrix, generate_items_matrix, generate_doors_matrix
from config.settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, TRAMPOLINE_HEIGHT, TRAMPOLINE_WIDTH, FLOOR_HEIGHT, SCREEN_WIDTH, FPS

class Level:
    """
    Represents a game level, including its platforms, trampolines, items, walls, enemies, doors, and waves.
    Handles the generation, updating, and rendering of these elements.
    """

    def __init__(self, level_number):
        """
        Initialize the level with the given level number.

        Args:
            level_number (int): The number of the level to load.
        """
        self.platforms = pygame.sprite.Group()
        self.trampolines = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.meowkies = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.waves = pygame.sprite.Group()

        # Group all sprite groups for easier management
        self.groups = [self.platforms, self.trampolines, self.items, self.walls, self.meowkies, self.doors, self.waves]

        # Level dimensions and offset for scrolling
        self.offset = 0
        self.width = 0
        self.height = 0

        # Generate matrices for level layout, items, and doors
        level_matrix = get_level_matrix(level_number)
        items_matrix = generate_items_matrix(level_matrix)
        doors_matrix = generate_doors_matrix(level_matrix)

        # Load roof sprite
        self.roof = pygame.image.load(path.join("assets", "sprites", "structures", "roof.png")).convert_alpha()
        self.roof_rect = self.roof.get_rect()

        # Build the level layout
        self.build_level(level_matrix, items_matrix, doors_matrix)

        # Initialize gameplay variables
        self.targeted_item = -1
        self.streak = True
        self.pairs_collected = 0

        self.total_meowkies = level_number
        self.current_meowkies = 0
        self.meowkies_delay_counter = 0

    def build_level(self, level_matrix, items_matrix, door_matrix, start_x=60, start_y=210):
        """
        Build the level layout based on the provided matrices.

        Args:
            level_matrix (list): Matrix representing the level structure.
            items_matrix (list): Matrix representing item placements.
            door_matrix (list): Matrix representing door placements.
            start_x (int): Starting x-coordinate for level elements.
            start_y (int): Starting y-coordinate for level elements.
        """
        increment = 0
        y = start_y

        for r_index, row in enumerate(level_matrix):
            x = start_x
            for c_index, cell in enumerate(row):
                # Wall generation
                if c_index == 0:
                    if r_index == 0:
                        wall = Wall(x + 2, y, height=20)
                    else:
                        wall = Wall(x + 2, y)
                    self.walls.add(wall)
                if c_index == len(row) - 1:
                    if r_index == 0:
                        wall = Wall(x + TRAMPOLINE_WIDTH, y, height=20)
                    else:
                        wall = Wall(x + TRAMPOLINE_WIDTH, y)
                    self.walls.add(wall)

                # Void
                if cell == 0:
                    x += TRAMPOLINE_WIDTH
                    increment = abs(PLATFORM_WIDTH - TRAMPOLINE_WIDTH)

                # Platform generation
                elif cell == 1:
                    is_floor = False if r_index == len(level_matrix) - 1 else True
                    platform = Platform(x, y, PLATFORM_WIDTH + increment, PLATFORM_HEIGHT, floor=is_floor)
                    self.platforms.add(platform)
                    x += PLATFORM_WIDTH + increment

                    # Items generation
                    if items_matrix[r_index][c_index] != 0:
                        item = Item(x - 10, y, items_matrix[r_index][c_index])
                        self.items.add(item)

                    # Doors generation
                    if door_matrix[r_index][c_index] in [1, 2] and c_index not in [0, len(row) - 1]:
                        special = True if door_matrix[r_index][c_index] == 2 else False

                        if level_matrix[r_index][c_index - 1] == 0:
                            door = Door(x + 5 - PLATFORM_WIDTH - increment, y, direction=1, special=special)
                        elif level_matrix[r_index][c_index + 1] == 0:
                            door = Door(x - 5, y, direction=-1, special=special)
                        else:
                            door = Door(x - 5, y, special=special)
                        self.doors.add(door)

                    # Reset increment
                    if increment > 0:
                        increment = 0

                # Trampoline generation
                elif cell == 2:
                    if c_index < len(row) - 2:
                        if level_matrix[r_index][c_index + 1] == 1:
                            increment = abs(PLATFORM_WIDTH - TRAMPOLINE_WIDTH)

                    trampoline = Trampoline(x, y + (PLATFORM_HEIGHT - TRAMPOLINE_HEIGHT), TRAMPOLINE_WIDTH, TRAMPOLINE_HEIGHT)
                    self.trampolines.add(trampoline)
                    x += TRAMPOLINE_WIDTH

            y += FLOOR_HEIGHT

        self.width = x
        self.height = y - FLOOR_HEIGHT
        self.roof = pygame.transform.scale(self.roof, (x - TRAMPOLINE_WIDTH + 10, self.roof.get_height()))
        self.roof_rect.bottomleft = (start_x, start_y)
        self.scroll(-self.width + SCREEN_WIDTH - 60)

    def generate_enemies(self, delay=2):
        """
        Generate enemies (Meowkies) at regular intervals.

        Args:
            delay (int): Delay in seconds between enemy generation.
        """
        if self.current_meowkies < self.total_meowkies:
            if self.meowkies_delay_counter > FPS * delay:
                meowky = Meowky(self.width // 2 - abs(self.offset) + 40, 100)
                meowky.move_down()
                self.meowkies.add(meowky)
                self.meowkies_delay_counter = 0
                self.current_meowkies += 1
            else:
                self.meowkies_delay_counter += 1

    def reset_meowkies(self):
        """
        Reset all Meowkies in the level.
        """
        self.meowkies.empty()
        self.current_meowkies = 0

    def reset_trampolines(self):
        """
        Reset all trampolines in the level to their initial state.
        """
        for trampoline in self.trampolines:
            trampoline.reset()
            trampoline.broken = False

    def check_collision(self, player):
        """
        Check for collisions between the player and Meowkies.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        for meowky in self.meowkies:
            if player.state not in ["jump", "up", "down"] and meowky.state not in ["jump", "up", "down"]:
                if meowky.rect.collidepoint(player.rect.center):
                    if player.state == meowky.state or player.state == "idle":
                        return True

        return False

    def check_fall(self, player):
        """
        Check if the player has fallen off the level.

        Args:
            player (Player): The player object.

        Returns:
            bool: True if the player has fallen, False otherwise.
        """
        if player.rect.y > self.height:
            return True

        return False

    def update(self, player):
        """
        Update the level state, including player interactions and enemy behavior.

        Args:
            player (Player): The player object.

        Returns:
            int: The score gained during this update.
        """
        score = 0
        score += player.update_on_level(self)

        for meowky in self.meowkies:
            meowky.update_on_level(self, player)

            # Logic with meowkies and doors
            for door in self.doors:
                door.check_collision(meowky, enemy=True)

            # Stun after door collision logic
            if meowky.state == "stun":
                if meowky.stun_counter < FPS * 2:
                    meowky.stun_counter += 1
                    meowky.animate_death()
                else:
                    score += 50
                    self.meowkies.remove(meowky)
                    self.current_meowkies -= 1

            # Logic with meowkies and waves
            for wave in self.waves:
                wave.check_collision(meowky)

            # Check if meowky fell
            if meowky.rect.y > self.height:
                self.meowkies.remove(meowky)
                self.current_meowkies -= 1

        for door in self.doors:
            if door.check_collision(player):
                if door.special:
                    wave = Wave(door.rect.centerx, door.rect.centery, door.direction)
                    self.waves.add(wave)

        for wave in self.waves:
            wave.update()

        for trampoline in self.trampolines:
            trampoline.update()

        self.generate_enemies()

        return score

    def scroll(self, dx):
        """
        Scroll the level horizontally by a given amount.

        Args:
            dx (int): The amount to scroll.
        """
        self.offset += dx

        for group in self.groups:
            for sprite in group:
                sprite.rect.x += dx

        self.roof_rect.x += dx

    def draw(self, screen):
        """
        Draw the level elements onto the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        # The order determines the layers
        self.platforms.draw(screen)
        self.doors.draw(screen)
        self.walls.draw(screen)
        self.trampolines.draw(screen)

        for sprite in self.items:
            if sprite.visible:
                screen.blit(sprite.image, sprite.rect.topleft)

        self.meowkies.draw(screen)
        self.waves.draw(screen)

        screen.blit(self.roof, self.roof_rect)