"""
File for managing game saves. Provided save files consist of the Knight class with default gear and attributes.
"""

from pathlib import Path
import shutil
import tomllib

_user_save_directory = None

def _get_save_directory():
    """Get the save directory from user setting or config file."""
    global _user_save_directory
    if _user_save_directory is not None:
        return _user_save_directory
    
    # Fall back to config file
    _current_dir = Path(__file__).parent
    _config_path = _current_dir / "config.toml"
    
    with open(_config_path, "rb") as f:
        config = tomllib.load(f)
    
    return Path.home() / config["paths"]["game_save_directory"]

def set_save_directory(save_directory):
    """
    Set the game save directory.
    
    Args:
        save_directory (str or Path): Path to your Dark Souls save directory
    """
    global _user_save_directory
    _user_save_directory = Path(save_directory)

# Package save files location
_package_dir = Path(__file__).parent
save_file_location = _package_dir / "Dark Souls Save Files"

save_files = {
    "newgame": "Beginning",
    "asylum_demon": "Asylum Demon",
    "taurus_demon": "Taurus Demon",
    "bell_gargoyles": "Bell Gargoyles",
    "moonlight_butterfly": "Moonlight Butterfly",
    "capra_demon": "Capra Demon",
    "gaping_dragon": "Gaping Dragon",
    "chaos_witch_quelaag": "Chaos Witch Quelaag",
    "great_grey_wolf_sif": "Great Grey Wolf Sif",
    "iron_golem": "Iron Golem"
}

# Select a save file
current_save = save_file_location / save_files["bell_gargoyles"] / "DRAKS0005.sl2"

def set_scenario(save_name):
    """
    Pick a save file by name.
    
    Args:
        save_name (str): Name of the save file to load
    """
    global current_save
    if save_name in save_files:
        current_save = save_file_location / save_files[save_name] / "DRAKS0005.sl2"
    else:
        raise ValueError(f"Save file '{save_name}' does not exist. Available saves: {list(save_files.keys())}")

# deletes the 'DRAKS0005.sl2' file in the '1638' folder
# There may be other save files generated later
def clear_save():
    save_dir = _get_save_directory()
    delete_files_in_folder(save_dir)

def load_save():
    save_dir = _get_save_directory()
    shutil.copy(current_save, save_dir)

def list_files_in_folder(folder_path): 
    return [f for f in folder_path.glob("*") if f.is_file()]

def delete_files_in_folder(folder_path):
    [f.unlink() for f in folder_path.glob("*") if f.is_file()]

def main():
    clear_save()
    load_save()
    print("Save reloaded!")

# wipes the save file and loads a new one
if __name__ == "__main__":
    main()