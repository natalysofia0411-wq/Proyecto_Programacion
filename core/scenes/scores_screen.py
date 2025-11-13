import pygame
import string
from os import path

from core.scenes.scene import Scene
from config.settings import BLACK, WHITE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT

from utils.helpers import load_scores

class ScoresScreen(Scene):
    """
    Represents the scores screen scene.
    Displays the top 5 scores, allows the player to input their name, and highlights their score.
    """

    def __init__(self, width, height):
        """
        Initialize the scores screen with the given dimensions.

        Args:
            width (int): The width of the screen.
            height (int): The height of the screen.
        """
        super().__init__(width, height)
        self.load_images(width, height)

        self.current_score = 0
        self.current_round = 0
        self.current_name = "..."
        self.prev_scores = load_scores()
        self.top_5 = None
        self.is_current_in_top = False

        self.selected_letter_index = 0

    def generate_top_5_with_status(self):
        """
        Generate the top 5 scores, including the current player's score.
        Updates the status of whether the current player is in the top 5.
        """
        self.prev_scores = load_scores()

        # Combine the current score with previous scores
        combined = self.prev_scores + [{
            "name": self.current_name,
            "score": self.current_score,
            "round": self.current_round
        }]

        # Sort by score (descending) and then by round (descending)
        combined.sort(key=lambda x: (x["score"], x["round"]), reverse=True)

        # Get the top 5 scores
        self.top_5 = combined[:5]

        # Check if the current player is in the top 5
        self.is_current_in_top = any(entry["name"] == self.current_name and entry["score"] == self.current_score for entry in self.top_5)

    def change_selection(self, direction):
        """
        Change the selected letter index for the player's name.

        Args:
            direction (str): The direction to move the selection ("left" or "right").
        """
        if direction == "left":
            self.selected_letter_index = (self.selected_letter_index - 1) % 3
        elif direction == "right":
            self.selected_letter_index = (self.selected_letter_index + 1) % 3

    def change_letter(self, direction):
        """
        Change the letter at the selected index in the player's name.

        Args:
            direction (str): The direction to change the letter ("up" or "down").
        """
        alphabet = list(string.ascii_uppercase)

        # Convert the current name to a list of characters
        name_chars = list(self.current_name)

        # Get the current letter's index in the alphabet
        current_char = name_chars[self.selected_letter_index]
        if current_char not in alphabet:
            current_index = 0
        else:
            current_index = alphabet.index(current_char)

        # Calculate the new index based on the direction
        if direction == "up":
            new_index = (current_index + 1) % len(alphabet)
        elif direction == "down":
            new_index = (current_index - 1) % len(alphabet)
        else:
            return  # Invalid direction

        # Replace the selected letter with the new one
        name_chars[self.selected_letter_index] = alphabet[new_index]
        self.current_name = "".join(name_chars)

    def draw(self, screen):
        """
        Draw the scores screen elements onto the provided screen.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
        """
        title_y = 200
        line_height = 30
        start_x = 100  # Initial horizontal position
        start_y = title_y + line_height

        # Fill the background with a solid color
        screen.fill(BLACK)

        # Draw the background image
        image_rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(self.image, image_rect)

        # Draw the headers
        headers = ["Name", "Score", "Round"]
        header_text = f"{headers[0]:<15}{headers[1]:<10}{headers[2]:<6}"
        header_surface = self.text_font.render(header_text, True, WHITE)
        screen.blit(header_surface, (start_x, title_y))

        # Draw the top 5 scores
        for i, entry in enumerate(self.top_5):
            color = YELLOW if entry["name"] == self.current_name else WHITE
            line_text = f"{entry['name']:<18}{entry['score']:<10}{entry['round']:<6}"
            line_surface = self.text_font.render(line_text, True, color)
            screen.blit(line_surface, (start_x, start_y + i * line_height))

        # Draw the current player's score if not in the top 5
        if not self.is_current_in_top:
            line_text = f"{self.current_name:<18}{self.current_score:<10}{self.current_round:<6}"
            line_surface = self.text_font.render(line_text, True, YELLOW)
            screen.blit(line_surface, (start_x, self.height - 80))

        # Draw the confirmation text
        confirm_text = self.text_font.render("Press SPACE to continue", True, WHITE)
        confirm_text_rect = confirm_text.get_rect(center=(self.width // 2, self.height - 30))
        screen.blit(confirm_text, confirm_text_rect)

        # Draw the instruction text
        inst_text = self.text_font.render("No (.) in name", True, WHITE)
        inst_text_rect = inst_text.get_rect(center=(self.width // 2, self.height))
        screen.blit(inst_text, inst_text_rect)

    def load_images(self, width, height):
        """
        Load the images required for the scores screen.

        Args:
            width (int): The width of the screen.
            height (int): The height of the screen.
        """
        base_path = path.join("assets", "sprites", "structures")
        self.image = pygame.transform.scale(pygame.image.load(path.join(base_path, "goro_house.png")), (width, height))