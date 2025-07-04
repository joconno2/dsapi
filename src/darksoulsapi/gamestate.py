"""
Contains essential functions for interacting with the game and keeping the state.
"""
import cv2 as cv
import time
import keyboard
import random
import numpy as np
import threading
from pathlib import Path

from .windowcapture import WindowCapture
from . import key_output
from . import fitness_function
from . import feature_matching
from . import start_game
from . import game_save

_current_dir = Path(__file__).parent
_templates_dir = _current_dir / 'templates'

class GameState:
    def __init__(self, game_directory=None, executable_file=None, save_directory=None):
        """
        Initialize the GameState.
        
        Args:
            game_directory (str or Path, optional): Path to Dark Souls Remastered installation
            executable_file (str, optional): Name of the executable file
            save_directory (str or Path, optional): Path to Dark Souls save directory
        """
        self.game_directory = game_directory
        self.executable_file = executable_file
        
        # Set the save directory if provided
        if save_directory is not None:
            game_save.set_save_directory(save_directory)
        
        # Initialize the action space
        action_keys = [
            "w", "a", "s", "d", "attack", "backstep", "heal", "strong-attack", "front-roll", "left-roll", "back-roll", "right-roll"
        ]

        action_values = [
            key_output.w_char,
            key_output.a_char,
            key_output.s_char,
            key_output.d_char,
            key_output.t_char,
            key_output.space_char,
            key_output.r_char,
            [key_output.shift_char, key_output.t_char],
            [key_output.w_char, key_output.space_char],
            [key_output.a_char, key_output.space_char],
            [key_output.s_char, key_output.space_char],
            [key_output.d_char, key_output.space_char]
        ]
        
        self.action_space = dict(zip(action_keys, action_values))

        try:
            self.wincap = WindowCapture('DARK SOULS™: REMASTERED')
        except Exception as e:
            print(f'Game is not open. {e}. Opening Game.')
            self.start_program()
            self.wincap = WindowCapture('DARK SOULS™: REMASTERED')
            self.load_into_game_from_main_menu()

        self.start_time = time.time()

    def set_scenario(self, save_name):
        """
        Set the scenario by loading a specific save file.
        
        Args:
            save_name (str): Name of the save file to load
        """
        game_save.set_scenario(save_name)
        
    def step(self, action):
        # The length that an input is pressed can be modified through the key_delay parameter
        self.send_input(action)

        pixel_input = self.get_screenshot()

        terminal_state = self.stop_event.is_set()

        return pixel_input, terminal_state

    def reset(self):
        # open the game if not open already
        # navigate into the game
        # reset save file
        self.focus_on_screen()
        self.reset_gamestate_for_boss_battle()

        self.reset_monitor_external_state()
        
        pixel_input = self.get_screenshot()
        return pixel_input
    
    def start_program(self):
        start_game.start_game(
            game_directory=self.game_directory,
            executable_file=self.executable_file,
            start_delay=30
        )

    def is_terminal_state(self):
        try:
            pixel_input = self.get_screenshot()
        except Exception as e:
            print(f"Error getting screenshot: {e}")
            return False

        pixel_input_gray = cv.cvtColor(pixel_input, cv.COLOR_BGR2GRAY)

        player_dead_template = cv.imread(str(_templates_dir / 'is_dead.png'))
        player_dead_template = cv.cvtColor(player_dead_template, cv.COLOR_BGR2GRAY)
        boss_dead_template = cv.imread(str(_templates_dir / 'victory_achieved.png'))
        boss_dead_template = cv.cvtColor(boss_dead_template, cv.COLOR_BGR2GRAY)

        self.player_is_dead = feature_matching.template_matching(pixel_input_gray, player_dead_template, threshold=0.75)
        self.boss_is_dead = feature_matching.template_matching(pixel_input_gray, boss_dead_template, threshold=0.75)

        return self.player_is_dead or self.boss_is_dead
    
    def reset_monitor_external_state(self):
        if hasattr(self, 'monitor_thread') and self.monitor_thread.is_alive():
            self.stop_event.set()
            self.monitor_thread.join()

        self.player_is_dead = False
        self.boss_is_dead = False

        self.stop_event = threading.Event()
        self.monitor_thread = threading.Thread(target=self.monitor_external_state)

        self.monitor_thread.start()

    def monitor_external_state(self):
        while not self.stop_event.is_set():
            time.sleep(1.0/4)
            if self.check_external_condition():
                self.stop_event.set()

    def check_external_condition(self):
        if self.is_terminal_state():
            print("Terminal state reached.")
            return True
        return False

    # This exits out, resets the save, and then opens the game again with a fresh save
    # Only run this when in-game and not paused
    def reset_gamestate_for_boss_battle(self):
        print("Resetting gamestate for boss battle.")
        
        self.exit_to_main_menu_from_game()
        self.reset_save()
        success = self.load_into_game_from_main_menu(False)
        if not success:
            return False

        # Only press 'e' once 'traverse the white light' indication is on the screen
        template = cv.imread(str(_templates_dir / 'traverse_the_white_light.png'))
        self.press_key_on_repeat(template, 0.8, 'e', True, 0.25)
        print("Traversing light.")

        # fix to press esc to skip the boss cutscene after 4 seconds
        # time.sleep(4)
        # keyboard.press_and_release('esc')

        # Pause until loaded into the boss arena
        template = cv.imread(str(_templates_dir / 'health_bar.png'))
        self.pause_until_template_match(template, 0.95, 0.25)
        time.sleep(1.0/2)
        print('Entered boss battle.')
        return True
    
    def exit_to_main_menu_from_game(self):
        print("Exiting to main menu from in-game.")
        # small delay just to make sure all action is completed
        # before it presses escape and everything
        time.sleep(8)

        sleep_time = 0.75
        keys = ['e','esc', 'left', 'e', 'up', 'e', 'left', 'e']
        for key in keys:
            keyboard.press_and_release(key)
            time.sleep(sleep_time)
        print("(Likely) Exited to main menu")

    def reset_save(self):
        time.sleep(1)
        game_save.clear_save()
        game_save.load_save()
        print("Save reset.")

    # This presses 'e' until in-game
    def load_into_game_from_main_menu(self, wait_extra_time=True):
        print("Attempting to load into game.")
        template = cv.imread(str(_templates_dir / 'loading_into_game.png'))
        
        success = self.press_key_on_repeat(template, 0.9, 'e', sleep_time=0.1, timeout=60)

        if not success:
            return False
        
        # wait 20 seconds because sometimes
        # when you spawn in, you instantly die
        # even though you're not fighting the boss
        if wait_extra_time:
            time.sleep(20)
        print("Loading into game.")
        return True
    

    def restart_game(self):
        print("Restarting game (to prevent input issues).")
        # Close the game
        keyboard.press_and_release('alt+f4')
        time.sleep(5)  # Wait for the game to close
        # Start the game again
        self.start_program()
        self.load_into_game_from_main_menu()

    # this presses (or does not press) a key until a template is matched
    def press_key_on_repeat(self, template, threshold, key_to_press, press_at_end=False, sleep_time=0.01, timeout=0):
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

        full_screen = self.get_screenshot()
        full_screen_gray = cv.cvtColor(full_screen, cv.COLOR_BGR2GRAY)
        start_time = time.time()
        while not feature_matching.template_matching(full_screen_gray, template, threshold):
            if timeout > 0 and (time.time() - start_time) > timeout:
                print("Timeout reached.")
                return False
            full_screen = self.get_screenshot()
            full_screen_gray = cv.cvtColor(full_screen, cv.COLOR_BGR2GRAY)
            if key_to_press and not press_at_end:
                keyboard.press_and_release(key_to_press)
            time.sleep(sleep_time)
        if key_to_press and press_at_end:
            keyboard.press_and_release(key_to_press)
        return True
        

    def pause_until_template_match(self, template, threshold, sleep_time=0.01):
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

        full_screen = self.get_screenshot()
        full_screen_gray = cv.cvtColor(full_screen, cv.COLOR_BGR2GRAY)
        while not feature_matching.template_matching(full_screen_gray, template, threshold):
            full_screen = self.get_screenshot()
            full_screen_gray = cv.cvtColor(full_screen, cv.COLOR_BGR2GRAY)
            time.sleep(sleep_time)


    # Get a screenshot of the game window
    # By default, the screenshot is scaled down for the NEAT input
    def get_screenshot(self, scale=1):
        return self.wincap.get_screenshot(scale)
    
    # make windows focus on the game window
    def focus_on_screen(self):
        self.wincap.focus_on_screen()

    def send_input(self, selected_action, key_delay=1.0/4):
        if isinstance(selected_action, list):
            for action in selected_action:
                key_output.HoldKey(action)
        else:
            key_output.HoldKey(selected_action)

        time.sleep(key_delay)

        if isinstance(selected_action, list):
            for action in selected_action:
                key_output.ReleaseKey(action)
        else:
            key_output.ReleaseKey(selected_action)