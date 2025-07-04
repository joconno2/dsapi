"""
Run this file to make sure that the Dark Souls Feed is being captured correctly
"""

import cv2 as cv
from time import time, sleep

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gamestate import GameState
from datetime import datetime

def show_visual_feed(save_image=False):
    screenshot = env.get_screenshot()
    
    cv.imshow("Game feed", screenshot)
    cv.waitKey(1)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    print(timestamp)
    
    if save_image:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        cv.imwrite(f"screenshots/screenshot_{timestamp}.png", screenshot)
        
if __name__ == "__main__":
    env = GameState()
    count = 0
    while True:
        count += 1
        show_visual_feed()
        
