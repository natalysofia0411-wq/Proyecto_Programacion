import pygame
from os import path

from config.settings import BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, FPS

from entities.mappy import Mappy

from levels.level import Level

from core.scenes.hud import HUD
from core.scenes.start_screen import StartScreen
from core.scenes.transition_screen import TransitionScene
from core.scenes.game_over_screen import GameOverScreen
from core.scenes.scores_screen import ScoresScreen
from core.scenes.pause_screen import PauseScreen

from utils.helpers import save_score, save_progress, load_progress

class Game:
    """
    Initialize the Game class.

    Args:
        screen (pygame.Surface): The screen surface where the game will be drawn.
    """
    def __init__(self, screen):
        # Initialize sprite group and screen dimensions
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.transition_scene = TransitionScene(self.width, self.height)
        self.start_screen = StartScreen(self.width, self.height)
        self.game_over_screen = GameOverScreen(self.width, self.height)
        self.scores_screen = ScoresScreen(self.width, self.height - 150)
        self.pause_screen = PauseScreen(self.width, self.height)
        self.scene = "start"

        self.initial_level_score = 0
        self.level_number = 1
        self.level = None

        self.block_count = 0
        self.controls = False

        self.player = Mappy(self.width - 170, self.height - 119)
        self.all_sprites.add(self.player)

        self.HUD = HUD(SCREEN_WIDTH, 60)
        self.HUD.player_lifes = self.player.lifes

        self.load_sounds()
        self.is_music = False

    def load_level(self):
        """
        Load the current level based on the level number.
        """
        # Create a new Level instance
        self.level = Level(self.level_number)

    def handle_event(self, event):
        """
        Handle user input events based on the current game scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """

        # Handle events for different scenes
        if self.scene == "start":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scene = "change"
                    self.sounds["game_start"].play()

                if event.key == pygame.K_l:
                    prev_save = load_progress()
                    if prev_save["level"] != -1:
                        self.level_number = prev_save["level"]
                        self.HUD.current_score = prev_save["score"]
                        self.player.lifes = prev_save["lifes"]
                        self.HUD.player_lifes = prev_save["lifes"]
                        self.scene = "change"
                        self.sounds["game_start"].play()

        elif self.scene == "level" and self.controls == True:
            if event.type == pygame.KEYDOWN:
                if self.player.state in ["idle", "left", "right", "up"]:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(self.level.platforms)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(self.level.platforms)
                
                if self.player.state in ["up"]:
                    if event.key == pygame.K_DOWN:
                        self.player.move_down()

                if event.key == pygame.K_ESCAPE:
                    self.scene = "pause"

            if event.type == pygame.KEYUP:
                if self.player.state in ["left", "right"]:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.stop()
        
        elif self.scene == "scores":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scores_screen.change_selection("left")
                elif event.key == pygame.K_RIGHT:
                    self.scores_screen.change_selection("right")
                elif event.key == pygame.K_UP:
                    self.scores_screen.change_letter("up")
                    self.scores_screen.generate_top_5_with_status()
                elif event.key == pygame.K_DOWN:
                    self.scores_screen.change_letter("down")
                    self.scores_screen.generate_top_5_with_status()
                elif event.key == pygame.K_SPACE:
                    if "." not in self.scores_screen.current_name:
                        save_score(self.scores_screen.current_name, self.scores_screen.current_score, self.scores_screen.current_round)
                        self.scene = "start"
                        self.level_number = 1
                        self.scores_screen.current_name = "..."
                        self.HUD.current_score = 0
                        self.player.state = "idle"
                        self.player.lifes = 4

        elif self.scene == "pause":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene = "level"
                if event.key == pygame.K_q:
                    save_progress(self.level_number, self.initial_level_score, self.player.lifes)
                    self.start_screen.load_level()
                    self.scene = "start"
                    self.level_number = 1
                    self.scores_screen.current_name = "..."
                    self.HUD.current_score = 0
                    self.player.state = "idle"
                    self.player.lifes = 4
                    self.HUD.player_lifes = 4
                    self.level = None
                    self.block_count = 0

    def scroll_screen(self):
        """
        Scroll the screen horizontally based on the player's position.
        """

        # Adjust screen offset for scrolling
        screen_mid = self.width // 2

        if self.level.width > self.width:
            if self.player.rect.centerx > screen_mid:
                if ((self.width - 60) - self.level.offset) < self.level.width:
                    movement = self.player.speed_x if self.player.state in ["right"] else self.player.speed_x - 1
                    self.player.rect.centerx = screen_mid
                    self.level.scroll(-movement)

            if self.player.rect.centerx < screen_mid:
                if -self.level.offset > 0:
                    movement = self.player.speed_x if self.player.state in ["left"] else self.player.speed_x - 1
                    self.player.rect.centerx = screen_mid
                    self.level.scroll(movement)

    def update(self, dt):
        """
        Update the game state based on the current scene and elapsed time.

        Args:
            dt (float): The time elapsed since the last update.
        """
        # Update game state for different scenes
        self.all_sprites.update()

        if self.scene == "level":
            self.update_level()
            
        elif self.scene == "block":
            self.block_level()

        elif self.scene == "change":
            self.change_level()

        elif self.scene == "reset":
            self.reset_level()

        elif self.scene == "game_over":
            self.game_over()

        elif self.scene == "game_over_screen":
            self.game_over_transition()

    def update_level(self, inital_block: int = 2):
        """
        Update the level state, including player actions and level transitions.

        Args:
            inital_block (int): The initial block duration before enabling controls.
        """

        # Update level logic and handle transitions
        if self.block_count > FPS * inital_block:
            if not self.is_music:
                pygame.mixer.music.play(-1)
                self.is_music = True

            self.controls = True
            score = self.level.update(self.player)
            self.HUD.add_score(score)
            self.scroll_screen()

            # Verifies end game conditions
            if len(self.level.items) == 0:
                pygame.mixer.music.stop()
                self.is_music = False
                self.sounds["level_clear"].play()

                self.block_count = 0
                self.scene = "block"
                self.player.stop()

            if self.level.check_collision(self.player) or self.level.check_fall(self.player):
                pygame.mixer.music.stop()
                self.is_music = False
                self.sounds["miss"].play()

                self.block_count = 0
                self.player.stop()
                self.player.lifes -= 1
                
                self.scene = "reset" if self.player.lifes + 1 > 0 else "game_over"
                self.level.scroll(-(abs(self.level.width - (SCREEN_WIDTH + abs(self.level.offset) - 60)))) # Resets the camera position
                self.level.reset_meowkies()
                self.level.reset_trampolines()
        else:
            self.controls = False
            self.block_count += 1

    def block_level(self, duration: int = 3):
        """
        Handle the block level state, which is a pause between levels.

        Args:
            duration (int): The duration of the block state in seconds.
        """

        # Manage block level state
        self.controls = False
        if self.block_count > FPS * duration:
            self.level_number = (self.level_number + 1) % 30  # Always loop between 1 and 30

            # Bonus levels logic (not implemented)
            if self.level_number not in [3, 7, 11, 15, 19, 23, 27]:
                self.scene = "change"
                self.block_count = 0
        else:
            self.block_count += 1

    def change_level(self, duration: int = 2):
        """
        Transition to the next level after a delay.

        Args:
            duration (int): The duration of the transition state in seconds.
        """

        # Handle level transition logic
        if self.block_count > FPS * duration:
            self.scene = "level"
            self.load_level()
            self.player.rect.topleft = (self.width - 170, self.height - 119)
            self.player.level = self.level
            self.block_count = 0
            self.initial_level_score = self.HUD.current_score
        else:
            self.block_count += 1

    def reset_level(self, duration = 4):
        """
        Reset the current level after the player loses a life.

        Args:
            duration (int): The duration of the reset state in seconds.
        """

        # Reset level state and player position
        if self.block_count > FPS * duration:
            self.HUD.player_lifes = self.player.lifes
            self.player.death_animation_counter, self.player.death_animation_frame = 0, 0
            self.player.state = "idle"
            self.player.rect.topleft = (self.width - 170, self.height - 119)
            self.block_count = 0
            self.scene = "level"
        else:
            self.player.animate_death()
            self.block_count += 1

    def game_over(self, duration = 4):
        """
        Handle the game over state, transitioning to the game over screen.

        Args:
            duration (int): The duration of the game over state in seconds.
        """

        # Manage game over logic
        if self.block_count > FPS * duration:
            self.sounds["game_over"].play(maxtime=10*1000)

            self.scene = "game_over_screen"
            self.block_count = 0
        else:
            self.player.animate_death()
            self.block_count += 1

    def game_over_transition(self, duration = 10):
        """
        Transition from the game over screen to the scores screen.

        Args:
            duration (int): The duration of the game over transition in seconds.
        """

        # Handle game over to scores transition
        if self.block_count > FPS * duration:
            self.sounds["name_entry"].play()

            self.scene = "scores"
            self.scores_screen.current_round = self.level_number
            self.scores_screen.current_score = self.HUD.current_score
            self.scores_screen.generate_top_5_with_status()
            self.block_count = 0
        else:
            self.block_count += 1

    def draw(self):
        """
        Draw the current game scene to the screen.
        """

        # Render the appropriate scene based on the current state
        if self.scene == "start":
            self.start_screen.draw(self.screen)

        elif self.scene == "level" or self.scene == "block":
            self.screen.fill(BLACK)
            self.level.draw(self.screen)
            self.HUD.draw(self.screen)
            self.all_sprites.draw(self.screen)
        
        elif self.scene == "reset" or self.scene == "game_over":
            self.screen.fill(BLACK)
            self.HUD.draw(self.screen)
            self.all_sprites.draw(self.screen)

        elif self.scene == "change":
            self.transition_scene.draw(self.screen, self.level_number)

        elif self.scene == "game_over_screen":
            self.game_over_screen.draw(self.screen)
            self.HUD.draw(self.screen)

        elif self.scene == "scores":
            self.scores_screen.draw(self.screen)
            self.HUD.draw(self.screen)

        elif self.scene == "pause":
            self.pause_screen.draw(self.screen)

    def load_sounds(self):
        """
        Load game sounds and music from the assets directory.
        """

        # Initialize sound effects and music
        base_bath = path.join("assets", "sounds")

        self.sounds = {
            "main_theme": pygame.mixer.music.load(path.join(base_bath, "mappy_main_theme.mp3")),
            "credit": pygame.mixer.Sound(path.join(base_bath, "mappy_credit_sound.mp3")),
            "game_over": pygame.mixer.Sound(path.join(base_bath, "mappy_game_over.mp3")),
            "game_start": pygame.mixer.Sound(path.join(base_bath, "mappy_game_start.mp3")),
            "miss": pygame.mixer.Sound(path.join(base_bath, "mappy_miss.mp3")),
            "level_clear": pygame.mixer.Sound(path.join(base_bath, "mappy_level_clear.mp3")),
            "name_entry": pygame.mixer.Sound(path.join(base_bath, "mappy_name_entry.mp3")),
        }