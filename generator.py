import numpy as np
from PIL import Image

reset_color = '\033[0m'
reset_foreground = '\033[39m'
reset_background = '\033[49m'


def get_color_escape(r, g, b, background=False):
    """ Given rgb values give the escape sequence for printing out the color"""
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


def get_magic_string(path):
    global last_foreground_color
    global last_background_color
    global is_last_bg_transparent
    # string to hold the color formatted string
    magic_string = ''

    # loading in image
    image = np.array(Image.open(path).convert('RGBA'))

    rows, columns, _ = image.shape
    if rows % 2 != 0:
        # Add a transparent row at the bottom
        transparent_row = np.zeros((1, columns, 4), dtype=np.uint8)
        transparent_row[:, :, 3] = 0  # Set alpha channel to 0 for transparency
        image = np.vstack((image, transparent_row))

    # generating the string
    for i in range(0, rows, 2):
        for j in range(columns):
            top = image[i, j, :]
            bottom = image[i + 1, j, :]
            magic_string += get_2pixel(top, bottom)

        magic_string += reset_color + '\n'

        # resetting values
        last_foreground_color = [-1, -1, -1, -1]
        last_background_color = [-1, -1, -1, -1]
        is_last_bg_transparent = True

    return magic_string


last_foreground_color = [-1, -1, -1, -1]
last_background_color = [-1, -1, -1, -1]
is_last_bg_transparent = True


def get_2pixel(top, bottom):
    global last_foreground_color
    global last_background_color
    global is_last_bg_transparent
    magic_string = ""

    is_top_transparent = top[3] == 0
    is_bottom_transparent = bottom[3] == 0

    if is_top_transparent or is_bottom_transparent:
        if is_last_bg_transparent:
            magic_string += reset_background
            is_last_bg_transparent = True

        if is_top_transparent and is_bottom_transparent:
            magic_string += " "
        elif is_top_transparent and not is_bottom_transparent:
            if np.any(bottom != last_foreground_color):
                magic_string += get_color_escape(bottom[0], bottom[1], bottom[2], background=False)
                last_foreground_color = bottom
            magic_string += "▄"
        elif not is_top_transparent and is_bottom_transparent:
            if np.any(top != last_foreground_color):
                magic_string += get_color_escape(top[0], top[1], top[2], background=False)
                last_foreground_color = top
            magic_string += "▀"

    else:
        if np.all(top == last_foreground_color) and np.all(bottom == last_background_color):
            magic_string += "▀"
        elif np.all(bottom == last_foreground_color) and np.all(top == last_background_color):
            magic_string += "▄"

        elif np.all(top == last_foreground_color):
            magic_string += get_color_escape(bottom[0], bottom[1], bottom[2], background=True)
            magic_string += "▀"
            last_background_color = bottom
        elif np.all(top == last_background_color):
            magic_string += get_color_escape(bottom[0], bottom[1], bottom[2], background=False)
            magic_string += "▄"
            last_foreground_color = bottom

        elif np.all(bottom == last_foreground_color):
            magic_string += get_color_escape(top[0], top[1], top[2], background=True)
            magic_string += "▀"
            last_background_color = top
        elif np.all(bottom == last_background_color):
            magic_string += get_color_escape(top[0], top[1], top[2], background=False)
            magic_string += "▄"
            last_foreground_color = top

        else:
            magic_string += get_color_escape(top[0], top[1], top[2], background=False)
            magic_string += get_color_escape(bottom[0], bottom[1], bottom[2], background=True)
            magic_string += "▀"
            last_foreground_color = top
            last_background_color = bottom

    return magic_string
