import random
from gamestate import GameState
import time

if __name__ == "__main__":
    env = GameState()
    pixel_input = env.reset()

    terminated = False
    while not terminated:
        action_key, action_value = random.choice(list(env.action_space.items()))
        print("Performing", action_key)
        pixel_input, terminated = env.step(action_value)
        time.sleep(1.0)
    print("Terminated")