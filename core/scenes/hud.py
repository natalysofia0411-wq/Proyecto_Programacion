import pygame
from os import path

from core.scenes.scene import Scene
from config.settings import WHITE, RED, SCREEN_HEIGHT
from utils.helpers import load_scores

class HUD(Scene):
    """
    Heads-Up Display (HUD) for the game.
    Displays the current score, high score, and player lives.
    """

    def __init__(self, width, height):
        """
        Initialize the HUD with the given dimensions.

        Args:
            width (int): The width of the HUD.
            height (int): The height of the HUD.
        """
        super().__init__(width, height)

        self.load_images()
        self.current_score = 0
        self.high_score = self.get_high_score()

        self.player_lifes = 0

    def get_high_score(self):
        """
        Retrieve the highest score from the saved scores.

        Returns:
            int: The highest score, or 0 if no scores are available.
        """
        scores = load_scores()
        if not scores:
            return 0
        return max(score["score"] for score in scores)

    def add_score(self, new_score):
        """
        Add a new score to the current score and update the high score if necessary.

        Args:
            new_score (int): The score to add.
        """
        self.current_score += new_score

        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def draw(self, screen):
        """
        Draw the HUD elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        # Colores
        white = WHITE

        # Score actual - 1UP
        one_up_text = self.text_font.render("1UP", True, RED)
        score_text = self.text_font.render(str(self.current_score), True, white)
        screen.blit(one_up_text, (self.width // 4 - one_up_text.get_width() // 2, 20))
        screen.blit(score_text, (self.width // 4 - score_text.get_width() // 2, 50))

        # High Score
        high_text = self.text_font.render("HIGH SCORE", True, RED)
        high_score_text = self.text_font.render(str(self.high_score), True, white)
        screen.blit(high_text, (self.width // 2 - high_text.get_width() // 2, 20))
        screen.blit(high_score_text, (self.width // 2 - high_score_text.get_width() // 2, 50))

        # Extra lifes
        for i in range(self.player_lifes):
            screen.blit(self.hearth_image, (i * 40 + 5, SCREEN_HEIGHT - 50))

    def load_images(self):
        """
        Load the images required for the HUD, such as the heart icon.
        """
        base_path = path.join("assets", "sprites", "hud")
        self.hearth_image = pygame.image.load(path.join(base_path, "hearth_mappy.png"))