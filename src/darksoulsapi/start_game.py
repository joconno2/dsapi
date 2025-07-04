"""
Helper method for starting the game when it is not running
"""

from pathlib import Path
from subprocess import run
import time
import tomllib

def start_game(start_delay=0):
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    home_path = Path.home()

    game_directory = home_path / config["paths"]["game_directory"]
    executable_file = config["paths"]["executable_file"]

    run(["start", "/d", game_directory, executable_file], shell=True)


    # wait for program to finish loading into the intro screen
    time.sleep(start_delay)

    print("Game started.")

if __name__ == "__main__":
    start_game()