import random
import json
import os
import pygame
from config.settings import SCORES_FILE
from levels.levels_distribution import LEVELS_DISTRIBUTION

def get_level_matrix(level_number):
    """
    Retrieve the level matrix for a given level number.

    Args:
        level_number (int): The level number to retrieve the matrix for.

    Returns:
        list: The level matrix corresponding to the given level number.
    """
    # Determine the level index based on the level number
    if 1 <= level_number <= 2 or 16 <= level_number <= 18:
        level = 0
    elif 4 <= level_number <= 6 or 20 <= level_number <= 22:
        level = 1
    elif 8 <= level_number <= 10 or 24 <= level_number <= 26:
        level = 2
    elif 12 <= level_number <= 14 or 28 <= level_number <= 30:
        level = 3

    return LEVELS_DISTRIBUTION[level]

def generate_items_matrix(level_matrix):
    """
    Generate a matrix of items for a given level matrix.

    Args:
        level_matrix (list): The level matrix to generate items for.

    Returns:
        list: A matrix with items placed on valid positions.
    """
    # Initialize item matrix and item counts
    rows = len(level_matrix)
    cols = len(level_matrix[0])
    items_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    items = {item: 0 for item in range(1, 6)}

    filling_matrix = True
    while filling_matrix:
        for i in range(rows):
            for j in range(cols):
                if i == 0:
                    items_matrix[i][j] = 0
                elif (
                        (level_matrix[i][j] == 1) and
                        (random.random() < 0.2) and
                        (i != rows - 1 and j != cols - 2) and
                        (items_matrix[i][j] == 0)
                    ):

                    item = random.randint(1, 5)
                    if items[item] < 2:
                        items_matrix[i][j] = item
                        items[item] += 1

        filling_matrix = False if sum(items.values()) == 10 else True

    return items_matrix

def generate_doors_matrix(level_matrix):
    """
    Generate a matrix of doors for a given level matrix.

    Args:
        level_matrix (list): The level matrix to generate doors for.

    Returns:
        list: A matrix with doors placed on valid positions.
    """
    # Initialize door matrix and door counts
    rows = len(level_matrix)
    cols = len(level_matrix[0])
    doors_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    current_doors = 0
    min_doors = 5
    while current_doors < min_doors:
        for i in range(rows):
            for j in range(cols):
                if i != 0 and j != 0 and j != cols - 1:
                    if level_matrix[i][j] == 1 and random.random() < 0.1:
                        if random.random() < 0.2:
                            doors_matrix[i][j] = 2
                        else:
                            doors_matrix[i][j] = 1
                        current_doors += 1
                        break

    return doors_matrix
    
def load_scores():
    """
    Load scores from the JSON file.

    Returns:
        list: A list of dictionaries containing score data.
    """
    # Check if the scores file exists
    if not os.path.exists(SCORES_FILE):
        return []

    with open(SCORES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_score(name, score, round):
    """
    Save a new score to the JSON file.

    Args:
        name (str): The name of the player.
        score (int): The score achieved by the player.
        round (int): The round number associated with the score.
    """
    # Load existing scores and append the new score
    scores = load_scores()
    scores.append({"name": name, "score": score, "round": round})

    # Opcional: ordenarlos por score descendente
    scores.sort(key=lambda x: x["score"], reverse=True)

    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def scale_image_by_height(image, target_height):
    """
    Scale an image to a target height while maintaining its aspect ratio.

    Args:
        image (pygame.Surface): The image to scale.
        target_height (int): The desired height of the scaled image.

    Returns:
        pygame.Surface: The scaled image.
    """
    # Calculate the scale factor and new dimensions
    original_width, original_height = image.get_size()
    scale_factor = target_height / original_height
    new_width = int(original_width * scale_factor)
    return pygame.transform.scale(image, (new_width, target_height))