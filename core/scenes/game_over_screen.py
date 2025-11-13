from core.scenes.scene import Scene
from config.settings import BLACK, GREEN

class GameOverScreen(Scene):
    """
    Represents the game over screen scene.
    Handles the rendering of the game over message and player information.
    """

    def draw(self, screen):
        """
        Draw the game over screen elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        # Fill the background with a solid color
        screen.fill(BLACK)

        # Render and center the "Player 1" text
        p1_text = self.title_font.render("Player 1", True, GREEN)
        p1_rect = p1_text.get_rect(center=(self.width // 2, self.height // 3))

        # Render and center the "Game over" text
        game_over_text = self.text_font.render("Game over", True, GREEN)
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))

        # Draw the texts onto the screen
        screen.blit(p1_text, p1_rect)
        screen.blit(game_over_text, game_over_rect)