import pygame
from config.settings import CYAN

class Wave(pygame.sprite.Sprite):
    """Represents a wave entity that moves horizontally and can interact with other entities."""

    def __init__(self, x, y, direction, width=5, height=70):
        """Initialize the Wave object with position, direction, and size.

        Args:
            x (int): The x-coordinate of the wave's initial position.
            y (int): The y-coordinate of the wave's initial position.
            direction (int): The direction of the wave's movement (-1 for left, 1 for right).
            width (int, optional): The width of the wave. Defaults to 5.
            height (int, optional): The height of the wave. Defaults to 70.
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed_x = 4  # Horizontal movement speed
        self.direction = direction  # Direction of movement (-1 for left, 1 for right)

    def check_collision(self, entity):
        """Check if the wave collides with an entity and apply effects.

        Args:
            entity: The entity to check for collision.
        """
        if self.rect.colliderect(entity.rect):
            entity.speed_x = self.speed_x
            if self.direction == -1:
                entity.state = "left_stun"
            elif self.direction == 1:
                entity.state = "right_stun"

    def update(self):
        """Update the wave's position based on its direction."""
        if self.direction == -1:
            self.rect.x -= self.speed_x
        elif self.direction == 1:
            self.rect.x += self.speed_x
