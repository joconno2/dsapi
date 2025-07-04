"""
File for managing game saves. Provided save files consist of the Knight class with default gear and attributes.
"""

from pathlib import Path
import shutil
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

home_path = Path.home()

game_save_directory = home_path / config["paths"]["game_save_directory"]

save_file_location = Path("Dark Souls Save Files")

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

# deletes the 'DRAKS0005.sl2' file in the '1638' folder
# There may be other save files generated later
def clear_save():
    delete_files_in_folder(game_save_directory)

def load_save():
    shutil.copy(current_save, game_save_directory)

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