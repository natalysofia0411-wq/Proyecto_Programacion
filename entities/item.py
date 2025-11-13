import pygame
from os import path

from utils.helpers import scale_image_by_height
from config.settings import BASE_ITEM_SCORE

class Item(pygame.sprite.Sprite):
    """Represents an item in the game that can be collected by the player."""

    def __init__(self, x, y, item_type, height=30):
        """Initialize an Item object with position, type, and size.

        Args:
            x (int): The x-coordinate of the item's position.
            y (int): The y-coordinate of the item's position.
            item_type (int): The type of the item (e.g., 1 for radio, 2 for TV).
            height (int, optional): The height to scale the item's image. Defaults to 30.
        """
        super().__init__()
        self.load_images()
        self.item_type = item_type
        self.visible = True
        self.animation_time = 0

        # Set the item's image based on its type
        match item_type:
            case 1:
                self.image = scale_image_by_height(self.images["radio"], height)
            case 2:
                self.image = scale_image_by_height(self.images["tv"], height)
            case 3:
                self.image = scale_image_by_height(self.images["computer"], height)
            case 4:
                self.image = scale_image_by_height(self.images["painting"], height)
            case 5:
                self.image = scale_image_by_height(self.images["safe"], height)

        self.rect = self.image.get_rect(bottomright=(x, y))

        # Load the sound effect for item collection
        self.sound = pygame.mixer.Sound(path.join("assets", "sounds", "mappy_item_get.mp3"))

    def check_collision(self, player):
        """Check if the player collides with the item and handle the interaction.

        Args:
            player: The player object to check for collision.

        Returns:
            int: The score value of the item if collected, otherwise 0.
        """
        if self.rect.collidepoint(player.rect.center):
            self.sound.play()
            return self.item_type * BASE_ITEM_SCORE
        
        return 0
    
    def start_targeted_animation(self):
        """Start the targeted animation for the item, making it blink."""
        self.animation_time += 1
        
        if self.animation_time % 10 == 0:
            self.visible = not self.visible
            self.animation_time = 0

    def stop_targeted_animation(self):
        """Stop the targeted animation and make the item visible."""
        self.visible = True
        self.animation_time = 0

    def load_images(self):
        """Load all images for the different types of items."""
        base_path = path.join("assets", "sprites", "loot")

        self.images = {
            "radio": pygame.image.load(path.join(base_path, "radio.png")).convert_alpha(),
            "tv": pygame.image.load(path.join(base_path, "tv.png")).convert_alpha(),
            "computer": pygame.image.load(path.join(base_path, "computer.png")).convert_alpha(),
            "painting": pygame.image.load(path.join(base_path, "painting.png")).convert_alpha(),
            "safe": pygame.image.load(path.join(base_path, "safe.png")).convert_alpha(),
        }