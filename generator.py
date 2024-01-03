import numpy as np
from PIL import Image
from get_color_escape import get_color_escape


def get_magic_string(path):
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
        tmp = ''
        for j in range(columns):
            top = image[i, j, :]
            bottom = image[i + 1, j, :]
            #magic_string += get_2pixel(top, bottom)
            tmp += get_2pixel(top, bottom)

        magic_string += tmp
        print(tmp)
        magic_string += reset_all_color() + '\n'

    return magic_string


def is_transparent(color):
    return color[3] == 0


last_foreground_color = [-1, -1, -1, -1]
last_background_color = [-1, -1, -1, -1]
is_last_background_transparent = True


def reset_all_color():
    global last_foreground_color
    global last_background_color
    global is_last_background_transparent
    last_foreground_color = [-1, -1, -1, -1]
    last_background_color = [-1, -1, -1, -1]
    is_last_background_transparent = True
    return '\033[0m'


def reset_background_color():
    global last_background_color
    global is_last_background_transparent
    is_last_background_transparent = True
    # making sure bg is not a valid color so we dont need to chack if bg is transparent
    last_background_color = [-1, -1, -1, -1]
    return '\033[49m'


def set_background_color(color):
    if is_transparent(color):
        raise "given color is transparent"
    global last_background_color
    global is_last_background_transparent
    is_last_background_transparent = False
    last_background_color = color
    return get_color_escape(color[0], color[1], color[2], background=True)


def set_foreground_color(color):
    if is_transparent(color):
        raise "given color is transparent"
    global last_foreground_color
    last_foreground_color = color
    return get_color_escape(color[0], color[1], color[2], background=False)


def get_2pixel(top, bottom):
    global last_foreground_color
    global last_background_color
    global is_last_background_transparent
    magic_string = ""

    # top and bootom might be not equal but both are transparent
    if is_transparent(top) and is_transparent(bottom):
        if not is_last_background_transparent:
            magic_string += reset_background_color()
        magic_string += " "

    # top and bottom equal but not transparent
    elif np.all(top == bottom):
        if np.all(top == last_foreground_color):
            magic_string = "█"
        elif np.all(top == last_background_color):
            magic_string += " "
        else:
            magic_string += set_foreground_color(top)
            magic_string += "█"

    # top transparent, bottom not
    elif is_transparent(top) and not is_transparent(bottom):
        if not is_last_background_transparent:
            magic_string += reset_background_color()
        if np.any(bottom != last_foreground_color):
            magic_string += set_foreground_color(bottom)
        magic_string += "▄"

    # bottom transparent, top not
    elif not is_transparent(top) and is_transparent(bottom):
        if not is_last_background_transparent:
            magic_string += reset_background_color()
        if np.any(top != last_foreground_color):
            magic_string += set_foreground_color(top)
        magic_string += "▀"

    # neither transparent
    else:
        if np.all(top == last_foreground_color) and np.all(bottom == last_background_color):
            magic_string += "▀"
        elif np.all(top == last_background_color) and np.all(bottom == last_foreground_color):
            magic_string += "▄"
        elif np.all(top == last_foreground_color):
            magic_string += set_background_color(bottom)
            magic_string += "▀"
        elif np.all(top == last_background_color):
            magic_string += set_foreground_color(bottom)
            magic_string += "▄"
        elif np.all(bottom == last_foreground_color):
            magic_string += set_background_color(top)
            magic_string += "▄"
        elif np.all(bottom == last_background_color):
            magic_string += set_foreground_color(top)
            magic_string += "▀"
        else:
            magic_string += set_foreground_color(top)
            magic_string += set_background_color(bottom)
            magic_string += "▀"

    return magic_string































"""    if is_top_transparent or is_bottom_transparent:
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
            last_background_color = bottom"""