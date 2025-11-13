import pygame
from os import path

class Platform(pygame.sprite.Sprite):
    """
    Represents a platform in the game. Platforms can either be regular or floor platforms,
    and they have a visual representation loaded from image files.
    """

    def __init__(self, x, y, width=100, height=25, floor=False):
        """
        Initializes the Platform object with its position, dimensions, and type.

        Args:
            x (int): The x-coordinate of the platform's top-left corner.
            y (int): The y-coordinate of the platform's top-left corner.
            width (int, optional): The width of the platform. Defaults to 100.
            height (int, optional): The height of the platform. Defaults to 25.
            floor (bool, optional): Whether the platform is a floor platform. Defaults to False.
        """
        super().__init__()
        self.load_images()  # Load the platform images from the assets folder.
        # Set the image based on whether the platform is a floor or not.
        self.image = pygame.transform.scale(self.platform, (width, height)) if floor else pygame.transform.scale(self.platform_floor, (width, height + 15))
        self.rect = self.image.get_rect(topleft=(x, y))  # Define the rectangle for collision detection.

    def load_images(self):
        """
        Loads the platform images from the assets folder.

        The images are expected to be located in the "assets/sprites/structures" directory.
        """
        base_path = path.join("assets", "sprites", "structures")
        self.platform = pygame.image.load(path.join(base_path, "platform.png"))  # Load the regular platform image.
        self.platform_floor = pygame.image.load(path.join(base_path, "platform_floor.png"))  # Load the floor platform image.