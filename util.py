def color_matches(pixel, color, tolerance=0):
    for i in range(3):
        if abs(pixel[i] - color[i]) > tolerance:
            return False
    return True


def color_matches_at_least_one(pixel, colors, tolerance=0):
    for color in colors:
        if color_matches(pixel, color, tolerance):
            return True
    return False