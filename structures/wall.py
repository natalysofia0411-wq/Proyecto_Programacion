import pygame
from os import path

class Wall(pygame.sprite.Sprite):
    """
    Represents a wall structure in the game. This class is a sprite that can detect collisions
    with other entities and has a visual representation loaded from an image file.
    """

    def __init__(self, x, y, width=8, height=75):
        """
        Initializes the Wall object with its position, dimensions, and image.

        Args:
            x (int): The x-coordinate of the wall's bottom-right corner.
            y (int): The y-coordinate of the wall's bottom-right corner.
            width (int, optional): The width of the wall. Defaults to 8.
            height (int, optional): The height of the wall. Defaults to 75.
        """
        super().__init__()
        self.load_images()  # Load the wall image from the assets folder.
        self.image = pygame.transform.scale(self.wall, (width, height))  # Scale the image to the specified dimensions.
        self.rect = self.image.get_rect(bottomright=(x, y))  # Set the rectangle for collision detection.

    def check_collision(self, entity):
        """
        Checks and handles collision with another entity.

        If the entity collides with the wall, its state and position are adjusted accordingly.

        Args:
            entity (pygame.sprite.Sprite): The entity to check collision with.
        """
        if self.rect.colliderect(entity.rect):
            if entity.state == "left":
                # Adjust the entity's position and change its state to "right".
                entity.rect.bottomleft = (self.rect.bottomright[0] + 4, self.rect.bottomleft[1])
                entity.state = "right"

            elif entity.state == "right":
                # Adjust the entity's position and change its state to "left".
                entity.rect.bottomright = (self.rect.bottomleft[0] - 4, self.rect.bottomright[1])
                entity.state = "left"

    def load_images(self):
        """
        Loads the wall image from the assets folder.

        The image is expected to be located in the "assets/sprites/structures" directory.
        """
        base_path = path.join("assets", "sprites", "structures")
        self.wall = pygame.image.load(path.join(base_path, "wall.png"))  # Load the wall image file.