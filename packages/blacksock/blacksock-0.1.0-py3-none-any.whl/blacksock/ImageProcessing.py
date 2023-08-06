import numpy as np

def area_is_active(area, frame):
    """Decide if a given area is active.

    For now, an area is consideren active if there are
    enough black pixels inside."""
    # These contants are likely to be calibrated later on
    NR_REQUIRED_PIXELS = 1
    THERESHOLD = 30
    STEP_SIZE = 5
    TARGET_COLOR = np.array([0, 0, 0])
    x_min, x_max = sorted([area.corner_1[0], area.corner_2[0]])
    y_min, y_max = sorted([area.corner_1[1], area.corner_2[1]])
    pixels_found = 0
    # STEP_SIZE -> skip some pixels for checking to
    # improve performance
    for x in range(x_min, x_max, STEP_SIZE):
        for y in range(y_min, y_max, STEP_SIZE):
            value = np.linalg.norm(frame[y, x]-TARGET_COLOR)
            if value < THERESHOLD:
                pixels_found += 1
    return pixels_found >= NR_REQUIRED_PIXELS
