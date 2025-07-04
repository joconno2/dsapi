# Dark Souls: Remastered API

<img src="https://github.com/joconno2/dsapi/raw/main/grey_dsapi_logo.png" width=50%>

**A Dark Souls: Remastered Python API, enabling the development of real-time AI agents.**

## About
This repository provides an API for Dark Souls: Remastered, enabling the development of AI agents to interact with and play the game. The API handles game state detection, action execution, and provides a simple interface for training agents. Currently, the API exists to simulate boss fight scenarios.

### Features

- **Ability to simulate various boss scenarios**
- **Real-time game screen capture for visual input**
- **Easy framework for training artificial intelligence agents**

## Requirements

- **Operating System**: Windows only (due to `win32api` dependency)
- **Python**: 3.12 or higher
- **Game**: Dark Souls: Remastered must be installed already

## Installation

Install from PyPI:

```bash
pip install darksoulsapi
```

## Usage
### 1. Configure Game Settings

Before using the API, configure Dark Souls: Remastered with these settings:

- **Resolution**: Set to 800x600, windowed mode
- **Key Bindings**: Update the following in Key Settings:
  - "Right weapon action (attack)" → `t`
  - "Right weapon action (Strong Attack)" → `Shift + t`
  - "Left weapon action (block)" → `y`
  - "Left weapon action (parry)" → `Shift + y`

> **Note**: Custom key bindings help prevent mouse input issues.

### 2. Obtain Game Paths

The API requires two main paths:

1. **Game Directory**: Path to your Dark Souls: Remastered installation
   ```
   Example: "C:/Program Files (x86)/Steam/steamapps/common/DARK SOULS REMASTERED/"
   ```

2. **Save Directory**: Path to your Dark Souls save files
   ```
   Example: "C:/Users/username/Documents/NBGI/Dark Souls Remastered/1638/"
   ```


### 3. Basic usage (more examples in /examples folder)
```python
import darksoulsapi
import random
import time

# Create game environment with your paths
env = darksoulsapi.create_game_state(
    game_directory="C:/Program Files (x86)/Steam/steamapps/common/DARK SOULS REMASTERED/",
    save_directory="C:/Users/username/Documents/NBGI/DARK SOULS REMASTERED/1638/"
)

# Reset the game state and obtain pixel input
pixel_input = env.reset()

# Main game loop
terminated = False
while not terminated:
  # Choose a random action from the action space
  action_key, action_value = random.choice(list(env.action_space.items()))
  print("Performing", action_key)
  # Execute action and get new state
  pixel_input, terminated = env.step(action_value)
  # Pause to allow action to be followed through
  time.sleep(1.0)
print("Game Session Terminated")
```




## Testing
- Run the tests to make sure that the environment is set up correctly and working.
  - Tests for game screen being obtained properly (run `show_visual_feed.py`)
