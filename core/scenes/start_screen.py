from core.scenes.scene import Scene
from config.settings import BLACK, GRAY, WHITE

class StartScreen(Scene):
    """
    Represents the start screen scene.
    Displays the welcome message and instructions to start the game.
    """

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
        instructions_text = self.text_font.render("Press SPACE to start", True, GRAY)
        instructions_rect = instructions_text.get_rect(center=(self.width // 2, self.height // 2))

        # Draw the texts onto the screen
        screen.blit(title_text, title_rect)
        screen.blit(instructions_text, instructions_rect)