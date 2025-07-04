"""
Helper method for starting the game when it is not running
"""

from pathlib import Path
from subprocess import run
import time
import tomllib

def start_game(game_directory=None, executable_file=None, start_delay=0):
    """
    Start the Dark Souls game.
    
    Args:
        game_directory (str or Path, optional): Path to Dark Souls Remastered installation directory
        executable_file (str, optional): Name of the executable file (default: "DarkSoulsRemastered.exe")
        start_delay (int): Delay in seconds after starting the game
    """
    if game_directory is None or executable_file is None:
        # Fall back to config file if paths not provided
        _current_dir = Path(__file__).parent
        _config_path = _current_dir / "config.toml"
        
        with open(_config_path, "rb") as f:
            config = tomllib.load(f)
        
        if game_directory is None:
            game_directory = Path.home() / config["paths"]["game_directory"]
        if executable_file is None:
            executable_file = config["paths"]["executable_file"]
    
    game_directory = Path(game_directory)
    
    run(["start", "/d", str(game_directory), executable_file], shell=True)


    # Wait for program to finish loading into the intro screen
    time.sleep(start_delay)

    print("Game started.")

if __name__ == "__main__":
    start_game()