import pygame
import sys

from core.game import Game
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from utils.helpers import save_score

def main():
    pygame.init()
    pygame.display.set_caption("Mappy")
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen)

    # Main loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
