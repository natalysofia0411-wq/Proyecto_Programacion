from core.scenes.scene import Scene
from config.settings import BLACK, GRAY, WHITE

from utils.helpers import load_progress

class StartScreen(Scene):
    """
    Represents the start screen scene.
    Displays the welcome message and instructions to start the game.
    """
    def __init__(self, width, height):
        """
        Initialize the scores screen with the given dimensions.

        Args:
            width (int): The width of the screen.
            height (int): The height of the screen.
        """
        super().__init__(width, height)
        self.prev_save = load_progress()

    def draw(self, screen):
        """
        Draw the start screen elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        # Fill the background with a solid color
        screen.fill(BLACK)

        # Render and center the title text
        title_text = self.title_font.render("¡Welcome to MAPPY!", True, WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))

        # Render and center the instructions text
        instructions1_text = self.text_font.render("Press SPACE to start", True, GRAY)
        instructions1_rect = instructions1_text.get_rect(center=(self.width // 2, self.height // 2))

        # Render and center the instructions text

        if self.prev_save["level"] != -1:
            instructions2_text = self.text_font.render(f"Press L to continue level {self.prev_save["level"]}", True, GRAY)
            instructions2_rect = instructions2_text.get_rect(center=(self.width // 2, (self.height // 3) * 2))
        else:
            instructions2_text = self.text_font.render("No current level progress detected", True, GRAY)
            instructions2_rect = instructions2_text.get_rect(center=(self.width // 2, (self.height // 3) * 2))

        # Draw the texts onto the screen
        screen.blit(title_text, title_rect)
        screen.blit(instructions1_text, instructions1_rect)
        screen.blit(instructions2_text, instructions2_rect)

    def load_level(self):
        self.prev_save = load_progress()