import pygame
from os import path
from config.settings import GRAY, CYAN, TRAMPOLINE_SCORE

class Trampoline(pygame.sprite.Sprite):
    """
    Represents a trampoline in the game. The trampoline can interact with the player, change its state based on usage,
    and display animations. It also plays a sound when the player bounces on it.
    """

    def __init__(self, x, y, width=75, height=10):
        """
        Initializes the trampoline with its position, dimensions, and initial state.

        Args:
            x (int): The x-coordinate of the trampoline's top-left corner.
            y (int): The y-coordinate of the trampoline's top-left corner.
            width (int, optional): The width of the trampoline. Defaults to 75.
            height (int, optional): The height of the trampoline. Defaults to 10.
        """
        super().__init__()
        self.load_images(width, height)  # Load trampoline images for different states and animations.
        self.image = self.images["green_trampoline"]  # Set the initial image.
        self.rect = self.image.get_rect(topleft=(x, y))  # Define the rectangle for collision detection.

        self.bounce_counter = 0  # Tracks the number of bounces on the trampoline.
        self.broken = False  # Indicates whether the trampoline is broken.
        self.color = "green"  # Initial color of the trampoline.

        self.animation = False  # Indicates whether the trampoline is animating.
        self.animation_counter = 1  # Counter for animation frames.
        self.animation_frame = 0  # Current frame in the animation sequence.
        self.animation_sequence = [1, 2, 3, 2, 1, 4, 5, 4]  # Sequence of animation frames.

        self.sound = pygame.mixer.Sound(path.join("assets", "sounds", "mappy_trampoline_jump.mp3"))  # Load the trampoline sound.

    def reset(self):
        """
        Resets the trampoline to its initial state.
        """
        self.bounce_counter = 0
        self.image = self.images["green_trampoline"]

    def check_collision(self, player):
        """
        Checks for collision with the player and handles the bounce logic.

        Args:
            player (pygame.sprite.Sprite): The player sprite to check collision with.

        Returns:
            int: The score awarded for bouncing on the trampoline, or 0 if no collision occurs.
        """
        if self.broken:
            return 0

        if player.rect.colliderect(self.rect) and player.state == "down":
            player.move_up()  # Make the player bounce upward.
            self.bounce_counter += 1

            if self.bounce_counter >= 3:
                self.broken = True  # Break the trampoline after 3 bounces.

            return TRAMPOLINE_SCORE
        else:
            return 0

    def start_animation(self):
        """
        Starts the trampoline's animation and plays the bounce sound.
        """
        self.sound.play()
        self.animation_counter = 1
        self.animation_frame = 0
        self.animation = True

    def stop_animation(self):
        """
        Stops the trampoline's animation.
        """
        self.animation = False

    def animate(self):
        """
        Handles the trampoline's animation logic based on the bounce counter and animation sequence.
        """
        match self.bounce_counter:
            case 0: self.color = "green"
            case 1: self.color = "blue"
            case 2: self.color = "pink"
            case 3: self.color = "red"

        if self.animation_frame < 7:
            if self.animation_counter % 3 == 0:
                self.animation_frame += 1

            frame = self.animation_sequence[self.animation_frame]
            self.image = self.images[f"{self.color}_trampoline_moving_{frame}"]

            self.animation_counter += 1
        else:
            self.image = self.images[f"{self.color}_trampoline"]
            self.animation_frame = 0
            self.animation_counter = 1
            self.stop_animation()

    def update(self):
        """
        Updates the trampoline's state, handling animations and broken state.
        """
        if self.animation:
            self.animate()

        if self.broken:
            self.image = self.images["broken_trampoline"]

    def load_images(self, width, height):
        """
        Loads the trampoline images for different states and animations.

        Args:
            width (int): The width to scale the images to.
            height (int): The height to scale the images to.
        """
        base_path = path.join("assets", "sprites", "trampolines")

        self.images = {
            "green_trampoline": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline.png")), (width, height)),
            "green_trampoline_moving_1": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline_moving_1.png")), (width, height)),
            "green_trampoline_moving_2": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline_moving_2.png")), (width, height)),
            "green_trampoline_moving_3": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline_moving_3.png")), (width, height)),
            "green_trampoline_moving_4": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline_moving_4.png")), (width, height)),
            "green_trampoline_moving_5": pygame.transform.scale(pygame.image.load(path.join(base_path, "green_trampoline_moving_5.png")), (width, height)),

            "blue_trampoline": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline.png")), (width, height)),
            "blue_trampoline_moving_1": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline_moving_1.png")), (width, height)),
            "blue_trampoline_moving_2": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline_moving_2.png")), (width, height)),
            "blue_trampoline_moving_3": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline_moving_3.png")), (width, height)),
            "blue_trampoline_moving_4": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline_moving_4.png")), (width, height)),
            "blue_trampoline_moving_5": pygame.transform.scale(pygame.image.load(path.join(base_path, "blue_trampoline_moving_5.png")), (width, height)),

            "pink_trampoline": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline.png")), (width, height)),
            "pink_trampoline_moving_1": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline_moving_1.png")), (width, height)),
            "pink_trampoline_moving_2": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline_moving_2.png")), (width, height)),
            "pink_trampoline_moving_3": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline_moving_3.png")), (width, height)),
            "pink_trampoline_moving_4": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline_moving_4.png")), (width, height)),
            "pink_trampoline_moving_5": pygame.transform.scale(pygame.image.load(path.join(base_path, "pink_trampoline_moving_5.png")), (width, height)),

            "red_trampoline": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline.png")), (width, height)),
            "red_trampoline_moving_1": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline_moving_1.png")), (width, height)),
            "red_trampoline_moving_2": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline_moving_2.png")), (width, height)),
            "red_trampoline_moving_3": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline_moving_3.png")), (width, height)),
            "red_trampoline_moving_4": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline_moving_4.png")), (width, height)),
            "red_trampoline_moving_5": pygame.transform.scale(pygame.image.load(path.join(base_path, "red_trampoline_moving_5.png")), (width, height)),

            "broken_trampoline": pygame.transform.scale(pygame.image.load(path.join(base_path, "broken_trampoline.png")), (width, height)),
        }