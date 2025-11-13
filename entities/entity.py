import pygame

class Entity(pygame.sprite.Sprite):
    """Base class for all game entities, providing movement, collision detection, and animation capabilities."""

    def __init__(self, x, y):
        """Initialize the entity with position, speed, and state.

        Args:
            x (int): The x-coordinate of the entity's initial position.
            y (int): The y-coordinate of the entity's initial position.
        """
        super().__init__()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed_x = 3  # Horizontal movement speed
        self.speed_y = 5  # Vertical movement speed

        self.direction = ""  # Current movement direction
        self.state = "idle"  # Current state of the entity
        self.platform_change = None  # Platform the entity is interacting with

        self.jump_start = None  # Starting position of a jump
        self.jump_end = None  # Ending position of a jump
        self.jump_frame = 0  # Current frame of the jump animation
        self.jump_duration = 20  # Total duration of the jump animation

        self.animation_counter = 1  # Counter for animation frames
        self.animation_frame = 1  # Current animation frame

    def move_left(self, platforms):
        """Move the entity to the left and handle platform interactions.

        Args:
            platforms (pygame.sprite.Group): Group of platforms to check for interactions.
        """
        if self.state in ["idle", "left", "right"]:
            self.state = "left"

        if self.platform_change and self.rect_on_left(platforms):
            self.jump_to(self.rect.centerx - 50, self.platform_change.rect.midtop[1] + 1, "left")

    def move_right(self, platforms):
        """Move the entity to the right and handle platform interactions.

        Args:
            platforms (pygame.sprite.Group): Group of platforms to check for interactions.
        """
        if self.state in ["idle", "left", "right"]:
            self.state = "right"

        if self.platform_change and self.rect_on_right(platforms):
            self.jump_to(self.rect.centerx + 50, self.platform_change.rect.midtop[1] + 1, "right")

    def move_up(self):
        """Move the entity upward."""
        if self.state in ["idle", "up", "down"]:
            self.state = "up"

    def move_down(self):
        """Move the entity downward."""
        if self.state in ["idle", "up", "down"]:
            self.state = "down"

    def stop(self):
        """Stop the entity's movement and set its state to idle."""
        self.state = "idle"

    def jump_to(self, x_obj, y_obj, direction):
        """Initiate a jump to a specific position.

        Args:
            x_obj (int): Target x-coordinate.
            y_obj (int): Target y-coordinate.
            direction (str): Direction of the jump (e.g., "left" or "right").
        """
        self.direction = direction
        self.state = "jump"
        self.jump_start = self.rect.center
        self.jump_end = (x_obj, y_obj)

    def follow_parabolic_trajectory(self, start_pos, end_pos, duration, current_frame):
        """Move the entity along a parabolic trajectory.

        Args:
            start_pos (tuple): Starting position of the trajectory.
            end_pos (tuple): Ending position of the trajectory.
            duration (int): Total duration of the trajectory in frames.
            current_frame (int): Current frame of the trajectory.
        """
        if current_frame >= duration:
            self.jump_frame = 0
            self.rect.midbottom = end_pos
            self.state = self.direction
            return

        # Interpolate horizontal position
        t = current_frame / duration
        x = (1 - t) * start_pos[0] + t * end_pos[0]

        # Maximum height of the parabola
        peak_height = -20

        # Interpolate vertical position with a parabolic curve
        y = (1 - t)**2 * start_pos[1] + 2 * (1 - t) * t * (start_pos[1] + peak_height) + t**2 * end_pos[1]

        self.rect.midbottom = (x, y)

    def list_group_collisions(self, group):
        """Check for collisions with a group of sprites.

        Args:
            group (pygame.sprite.Group): Group of sprites to check for collisions.

        Returns:
            list: List of sprites that collide with the entity.
        """
        li = list()
        for item in group:
            if self.rect.colliderect(item.rect):
                li.append(item)

        return li
    
    def rect_on_left(self, sprite_group):
        """Check if there are sprites to the left of the entity.

        Args:
            sprite_group (pygame.sprite.Group): Group of sprites to check.

        Returns:
            bool: True if there are sprites to the left, False otherwise.
        """
        for sprite in sprite_group:
            if sprite.rect.centerx < self.rect.centerx:
                return True
            
        return False
    
    def rect_on_right(self, sprite_group):
        """Check if there are sprites to the right of the entity.

        Args:
            sprite_group (pygame.sprite.Group): Group of sprites to check.

        Returns:
            bool: True if there are sprites to the right, False otherwise.
        """
        for sprite in sprite_group:
            if self.rect.centerx < sprite.rect.centerx:
                return True
            
        return False

    def update(self):
        """Update the entity's position and state based on its current behavior."""
        if self.state != "stun":
            self.animate()

        if self.state != "jump":
            if self.state in ["left", "left_stun"]:
                self.rect.x -= self.speed_x
            elif self.state in ["right", "right_stun"]:
                self.rect.x += self.speed_x
            elif self.state == "up":
                self.rect.y -= self.speed_y
            elif self.state == "down":
                self.rect.y += self.speed_y

        else:
            self.follow_parabolic_trajectory(self.jump_start, self.jump_end, self.jump_duration, self.jump_frame)
            self.jump_frame += 1

        if self.rect.y < 80:
            self.state = "down"
