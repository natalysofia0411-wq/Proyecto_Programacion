import pygame
from os import path

from config.settings import TEXT_FONT_SIZE, TITLE_FONT_SIZE

"""
This module defines the Scene class, which serves as a base class for different game scenes.
"""

class Scene:
    """
    Initialize the Scene class.

    Args:
        width (int): The width of the scene.
        height (int): The height of the scene.
    """
    def __init__(self, width, height):
        # Store the dimensions of the scene
        self.width = width
        self.height = height

        # Load the font for titles and text from the assets directory
        font_path = path.join("assets", "fonts", "Jersey25-Regular.ttf")
        self.title_font = pygame.font.Font(font_path, TITLE_FONT_SIZE)
        self.text_font = pygame.font.Font(font_path, TEXT_FONT_SIZE)