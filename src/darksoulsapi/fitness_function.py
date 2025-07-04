"""
Functions to evaluate the fitness of an agent.
"""
import cv2 as cv
import numpy as np
import pytesseract
import random
from pathlib import Path

from . import feature_matching

tesseract_path = Path.home() / 'AppData' / 'Local' / 'Programs' / 'Tesseract-OCR' / 'tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)

_current_dir = Path(__file__).parent
_template_path = _current_dir / 'templates' / 'target_template1.png'
locked_on_marker = cv.cvtColor(cv.imread(str(_template_path)), cv.COLOR_BGR2GRAY)

def get_fitness(screenshot):
    fitness = 0
    # fitness += get_souls_number(screenshot) * 100
    # fitness += get_locked_in(screenshot)
    _, _, player_health_value = get_player_health(screenshot)
    fitness = player_health_value
    _, _, boss_health_value = get_boss_health(screenshot)
    fitness += (100 - boss_health_value)

    return fitness

def get_player_health(screenshot):
    cropped_screenshot = screenshot[48:55, 109:251]
    hsv_screenshot = cv.cvtColor(cropped_screenshot, cv.COLOR_BGR2HSV)
    upscaled_screenshot = cv.resize(cropped_screenshot, None, fx=5, fy=5, interpolation=cv.INTER_NEAREST)

    # Define range of color in HSV
    # Red color range can wrap around the hue values, so we need two ranges
    lower_red_1 = np.array([0, 80, 50])
    upper_red_1 = np.array([2, 255, 110])
    lower_red_2 = np.array([178, 80, 50])
    upper_red_2 = np.array([179, 255, 110])

    # Threshold the HSV image to get only red colors
    mask1 = cv.inRange(hsv_screenshot, lower_red_1, upper_red_1)
    mask2 = cv.inRange(hsv_screenshot, lower_red_2, upper_red_2)
    mask = cv.bitwise_or(mask1, mask2)
    # Close the mask to fill small holes
    kernel = np.ones((10, 10), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    
    # mask is 142x7
    # player_health_value = np.median(np.sum(mask==255, axis=1)) / mask.shape[1] * 100
    player_health_max_width = 142
    for i in range(mask.shape[1]):
        if np.all(mask[:, i] == 0):
            player_health_max_width = i
            break
    player_health_value = player_health_max_width/142*100

    upscaled_mask = cv.resize(mask, None, fx=5, fy=5, interpolation=cv.INTER_NEAREST)

    return upscaled_screenshot, upscaled_mask, player_health_value
    # return health_value

def get_boss_health(screenshot):
    screenshot_max_width = 415

    cropped_screenshot = screenshot[517:523, 246:246+screenshot_max_width]
    hsv_screenshot = cv.cvtColor(cropped_screenshot, cv.COLOR_BGR2HSV)
    upscaled_screenshot = cv.resize(cropped_screenshot, None, fx=2, fy=10, interpolation=cv.INTER_NEAREST)

    # Define range of color in HSV
    # Red color range can wrap around the hue values, so we need two ranges
    lower_red_1 = np.array([0, 140, 3])
    upper_red_1 = np.array([15, 255, 61])

    # Threshold the HSV image to get only red colors
    mask = cv.inRange(hsv_screenshot, lower_red_1, upper_red_1)
    # Close the mask to fill small holes
    kernel = np.ones((10, 10), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    # mask is 142x7
    upscaled_mask = cv.resize(mask, None, fx=2, fy=10, interpolation=cv.INTER_NEAREST)

    for i in range(mask.shape[1]):
        if np.all(mask[:, i] == 0):
            screenshot_max_width = i
            break
    
    boss_health_value = screenshot_max_width/415*100

    # cv.imshow('mask', upscaled_mask)

    return upscaled_screenshot, upscaled_mask, boss_health_value

def get_souls_number(screenshot):
    souls_number = 0

    # capture bottom right
    height, width, col = screenshot.shape

    h1 = 54
    h2 = 35
    w1 = 100
    w2 = 62

    bottom_right_img = screenshot[height-h1:height-h2, width-w1:width-w2]

    # saturation mask
    threshold_value = 90
    scale_factor = 4

    upscaled_screenshot = cv.resize(bottom_right_img, (bottom_right_img.shape[1] * scale_factor, bottom_right_img.shape[0] * scale_factor), interpolation=cv.INTER_CUBIC)
    hsv_img = cv.cvtColor(upscaled_screenshot, cv.COLOR_BGR2HSV)
    _, saturation_mask = cv.threshold(hsv_img[:, :, 1], threshold_value, 255, cv.THRESH_BINARY_INV)

    filtered_img = cv.bitwise_and(upscaled_screenshot, upscaled_screenshot, mask=saturation_mask)


    # Extract text using pytesseract with optimized configuration for numbers
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    souls_text = pytesseract.image_to_string(filtered_img, config=custom_config)
    # strip the text of any whitespaces
    souls_text = souls_text.strip()

    # Check if the extracted text is a valid integer
    if souls_text.isdigit():
        souls_number = int(souls_text)
    else:
        random_id = random.randint(10000, 99999)
        print(f'PARSE FAIL {random_id} - "{souls_text}"')

    return souls_number

def get_locked_on(screenshot):
    gray_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    locked_on = feature_matching.template_matching(gray_screenshot, locked_on_marker)
    if locked_on:
        return True
    return False
