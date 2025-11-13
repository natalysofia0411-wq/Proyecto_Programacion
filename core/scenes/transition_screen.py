from core.scenes.scene import Scene
from config.settings import BLACK, GRAY

class TransitionScene(Scene):
    """
    Represents a transition scene between game rounds.
    Displays the current round number on the screen.
    """

    def draw(self, screen, number):
        """
        Draw the transition screen elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            number (int): The current round number to display.
        """
        # Fill the background with a solid color
        screen.fill(BLACK)

        # Render and center the round number text
        round_text = self.text_font.render(f"Round {number}", True, GRAY)
        instructions_rect = round_text.get_rect(center=(self.width // 2, self.height // 2))

        # Draw the round number text onto the screen
        screen.blit(round_text, instructions_rect)