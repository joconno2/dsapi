import darksoulsapi
import random
import time

# Create game environment with your paths
env = darksoulsapi.create_game_state(
    game_directory="C:/Program Files (x86)/Steam/steamapps/common/DARK SOULS REMASTERED/",
    save_directory="C:/Users/username/Documents/NBGI/DARK SOULS REMASTERED/1638/"
)

# Pick scenario to load
env.set_scenario("asylum_demon")  # Example: Load the "Asylum Demon" boss fight

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