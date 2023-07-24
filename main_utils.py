import time
import math
import numpy as np

def rgb_to_hex(rgb):
    return ("#%02x%02x%02x%02x" % rgb).upper()

def image_to_npy(img):
    
    return np.asarray(img).transpose((1, 0, 2))

def closest_color(target_rgb, rgb_colors_array_in):
    # function to find the closest rgb color from palette to a target rgb color
    r, g, b, a = target_rgb
    color_diffs = []
    for color in rgb_colors_array_in:
        cr, cg, cb, _ = color
        color_diff = math.sqrt((float(r) - cr) ** 2 + (float(g) - cg) ** 2 + (float(b) - cb) ** 2)
        color_diffs.append((color_diff, color))
    return min(color_diffs, key=lambda x: x[0])[1]


def get_time_passed(start_time):
    time_passed = time.time() - start_time
    h, remainder = divmod(time_passed, 3600)
    m, s = divmod(remainder, 60)
    ms = int((s % 1) * 1000)  # Getting milliseconds part

    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}.{ms:03d}"