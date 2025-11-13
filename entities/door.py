import pygame
import random
from os import path
from config.settings import BROWN, CYAN, OPEN_DOOR_SCALE, CLOSED_DOOR_SCALE

class Door(pygame.sprite.Sprite):
    """Represents a door entity in the game, which can interact with other entities."""

    def __init__(self, x, y, width=10, height=60, direction=0, special=False):
        """Initialize a Door object with position, size, direction, and type.

        Args:
            x (int): The x-coordinate of the door's position.
            y (int): The y-coordinate of the door's position.
            width (int, optional): The width of the door. Defaults to 10.
            height (int, optional): The height of the door. Defaults to 60.
            direction (int, optional): The direction the door faces (-1 for left, 1 for right, 0 for random). Defaults to 0.
            special (bool, optional): Whether the door is a special type. Defaults to False.

        Raises:
            Exception: If the direction is not valid.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.special = special

        if direction == 0:
            self.state = -1 if random.randint(0, 1) == 0 else 1
        elif direction in [1, -1]:
            self.state = direction
        else:
            raise Exception("Not a valid direction")
        
        self.load_images()
        facing = "left" if self.state == -1 else "right"
        sp = "special_" if self.special else ""
        self.image = self.images[f"{sp}door_{facing}_closed"]

        self.rect = self.image.get_rect(midbottom=(x, y))
        
        self.direction = self.state

    def open(self, entity, new_width=50, enemy=False):
        """Open the door and adjust its size and position based on interactions.

        Args:
            entity: The entity interacting with the door.
            new_width (int, optional): The new width of the door. Defaults to 50.
            enemy (bool, optional): Whether the interaction is caused by an enemy. Defaults to False.
        """
        difference = new_width - self.width
        self.width = new_width

        sp = "special_" if self.special else ""
        self.image = self.images[f"{sp}open_door"]

        if self.state == -1:
            self.rect.bottomright = (self.rect.bottomright[0] - (difference), self.rect.midbottom[1])
            if entity.state == "right":
                new_state = "right" if not enemy else "stun"
                entity.jump_to(entity.rect.x - difference - 10, entity.rect.midbottom[1], new_state)
        elif self.state == 1:
            if entity.state == "left":
                new_state = "left" if not enemy else "stun"
                entity.jump_to(entity.rect.x + difference + 10, entity.rect.midbottom[1], new_state)

        self.state = 0

    def check_collision(self, entity, enemy=False):
        """Check if an entity collides with the door and handle the interaction.

        Args:
            entity: The entity to check for collision.
            enemy (bool, optional): Whether the entity is an enemy. Defaults to False.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        if self.rect.colliderect(entity.rect):
            if self.state in [-1, 1]:
                if entity.state in ["left", "right"]:
                    if not enemy:
                        self.open(entity)
                    else:
                        if not self.special:
                            if self.state == -1 and entity.state == "left": entity.state = "right"
                            elif self.state == 1 and entity.state == "right": entity.state = "left"
                            else: self.open(entity, enemy=True)
                        else:
                            if entity.state == "left": entity.state = "right"
                            elif entity.state == "right": entity.state = "left"
                    
                    return True

                elif entity.state == "jump":
                    if entity.direction == "left":
                        entity.jump_to(entity.rect.x + 40, entity.rect.midbottom[1], "down")
                    elif entity.direction == "right":
                        entity.jump_to(entity.rect.x - 40, entity.rect.midbottom[1], "down")

        return False
    
    def load_images(self):
        """Load all images for the door's states and types."""
        base_path = path.join("assets", "sprites", "doors")

        OPEN_DOOR = pygame.transform.scale(pygame.image.load(path.join(base_path, "open_door.png")).convert_alpha(), OPEN_DOOR_SCALE)
        DOOR_LEFT_CLOSED = pygame.transform.scale(pygame.image.load(path.join(base_path, "door_left_closed.png")).convert_alpha(), CLOSED_DOOR_SCALE)
        DOOR_RIGHT_CLOSED = pygame.transform.scale(pygame.image.load(path.join(base_path, "door_right_closed.png")).convert_alpha(), CLOSED_DOOR_SCALE)

        SPECIAL_OPEN_DOOR = pygame.transform.scale(pygame.image.load(path.join(base_path, "special_open_door.png")).convert_alpha(), OPEN_DOOR_SCALE)
        SPECIAL_DOOR_LEFT_CLOSED = pygame.transform.scale(pygame.image.load(path.join(base_path, "special_door_left_closed.png")).convert_alpha(), CLOSED_DOOR_SCALE)
        SPECIAL_DOOR_RIGHT_CLOSED = pygame.transform.scale(pygame.image.load(path.join(base_path, "special_door_right_closed.png")).convert_alpha(), CLOSED_DOOR_SCALE)

        self.images = {
            "open_door": OPEN_DOOR,
            "door_left_closed": DOOR_LEFT_CLOSED,
            "door_right_closed": DOOR_RIGHT_CLOSED,
            "special_open_door": SPECIAL_OPEN_DOOR,
            "special_door_left_closed": SPECIAL_DOOR_LEFT_CLOSED,
            "special_door_right_closed": SPECIAL_DOOR_RIGHT_CLOSED,
        }