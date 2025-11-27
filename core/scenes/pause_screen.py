from core.scenes.scene import Scene
from config.settings import WHITE

class PauseScreen(Scene):
    """
    Represents the pause screen scene.
    Displays the welcome message and instructions to pause the game.
    """

    def draw(self, screen):
        """
        Draw the pause screen elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """

        # Render and center the title text
        title_text = self.title_font.render("Game Paused", True, WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))

        # Render and center the instructions text
        instructions1_text = self.text_font.render("Press ESC to continue", True, WHITE)
        instructions1_rect = instructions1_text.get_rect(center=(self.width // 2, self.height // 2))

        # Render and center the instructions text
        instructions2_text = self.text_font.render("Press Q to save level and exit", True, WHITE)
        instructions2_rect = instructions2_text.get_rect(center=(self.width // 2, (self.height // 3) * 2))

        # Draw the texts onto the screen
        screen.blit(title_text, title_rect)
        screen.blit(instructions1_text, instructions1_rect)
        screen.blit(instructions2_text, instructions2_rect)