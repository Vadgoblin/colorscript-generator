import PIL
import numpy as np
from PIL import Image
import sys
from main import die
import os


def print_to_stdout(path_to_image, size):
    image, rows, columns = prepare_image(path_to_image, size)

    for i in range(0, rows, 2):
        tmp_string = ""

        for j in range(columns):
            top = image[i, j, :]
            bottom = image[i + 1, j, :]
            tmp_string += get_2pixel(top, bottom)

        tmp_string += reset_all_color()
        print(tmp_string)


def get_magic_string(path_to_image, size):
    magic_string = ''

    image, rows, columns = prepare_image(path_to_image, size)

    for i in range(0, rows, 2):
        for j in range(columns):
            top = image[i, j, :]
            bottom = image[i + 1, j, :]
            magic_string += get_2pixel(top, bottom)

        magic_string += reset_all_color() + '\n'

    return magic_string


def prepare_image(path_to_image, size):
    try:
        image = Image.open(path_to_image).convert('RGBA')

        if size is not None:
            image = resize_image(image, size)

        image = np.array(image)
        rows, columns, _ = image.shape
        if rows % 2 != 0:
            # Add a transparent row at the bottom
            transparent_row = np.zeros((1, columns, 4), dtype=np.uint8)
            transparent_row[:, :, 3] = 0  # Set alpha channel to 0 for transparency
            image = np.vstack((image, transparent_row))
        return image, rows, columns

    except PIL.UnidentifiedImageError:
        die(f"Provided file ({path_to_image}) is not an image.")


def resize_image(image, size):
    width, height = image.size
    aspect_ratio = width / height

    new_width, new_height = -1, -1

    if size == "auto":
        terminal_size = os.get_terminal_size()

        max_width = terminal_size.columns
        max_height = terminal_size.lines * 2

        if max_width < width or max_height < height:
            if aspect_ratio > max_width/max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:
            new_width = width
            new_height = height

    else:
        if size[0] == -1:
            new_height = size[1]
            new_width = int(new_height * aspect_ratio)
        elif size[1] == -1:
            new_width = size[0]
            new_height = int(new_width / aspect_ratio)

        else:
            new_width = size[0]
            new_height = size[1]

    resized_image = image.resize((new_width, new_height))
    return resized_image


def is_transparent(color):
    return color[3] == 0


def get_color_escape(r, g, b, background=False):
    """ Given rgb values give the escape sequence for printing out the color"""
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


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
