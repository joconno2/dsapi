<img src="grey_dsapi_logo.png" width=50%>

Dark Souls: Remastered API for Artificial Intelligence Research

# How To Run
1. First, update the [Game Settings](#game-settings).
2. Update your game and save paths in the `config.toml` file.
3. Look at `ds_environment_example_random.py` for usage instructions.
# Testing
- Run the tests to make sure that the environment is set up correctly and working.
  - Tests for game screen being obtained properly (run `show_visual_feed.py`)


# Game Settings
- Change resolution to 800x600, windowed.
- Make the following input changes in Key Settings, as Dark Souls may stop registering mouse input when training for extended periods of time:
  - "Right weapon action (attack)" to the key "t"
  - "Right weapon action (Strong Attack)" to the combination "Shift + t"
  - "Left weapon action (block)" to the key "y"
  - "Left weapon action (parry)" to the combination "Shift + y"
  - Additionaly, custom inputs can be defined in `gamestate.py`

Otherwise, default values remain for everything else.
