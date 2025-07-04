"""
Dark Souls: Remastered API for AI research
"""

from .gamestate import GameState
from .game_save import set_save_directory
from . import start_game

__version__ = "0.0.7"

def create_game_state(game_directory, save_directory, executable_file="DarkSoulsRemastered.exe"):
    """
    Create a GameState with the specified paths.
    
    Args:
        game_directory (str or Path): Path to Dark Souls Remastered installation directory
        save_directory (str or Path): Path to Dark Souls save files directory  
        executable_file (str): Name of the executable file (default: "DarkSoulsRemastered.exe")
    
    Returns:
        GameState: Configured GameState instance
        
    Example:
        game = darksoulsapi.create_game_state(
            game_directory="C:/Program Files (x86)/Steam/steamapps/common/Dark Souls Remastered/",
            save_directory="C:/Users/username/Documents/NBGI/DARK SOULS REMASTERED/1638/"
        )
    """
    return GameState(
        game_directory=game_directory,
        executable_file=executable_file,
        save_directory=save_directory
    )