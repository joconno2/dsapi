"""
Standard computer vision functions for template matching and state detection.
"""

import numpy as np
import cv2 as cv

def template_matching(img, template, threshold=0.9, get_image=False):
    w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
                'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']
    # if changing the method, change the threshold
    meth = methods[3]
    method = getattr(cv, meth)

    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if not get_image:
        if max_val >= threshold:
            return True
        return False
    else:
        if max_val > threshold:
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv.rectangle(img,top_left, bottom_right, 255, 2)
        return img