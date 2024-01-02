import numpy as np
from PIL import Image


def write_pokemon_to_file(pokemon_art, output_path):
    with open(output_path, 'w') as file:
        file.write(pokemon_art)


def get_pokemon_art(path):
    # string to hold the color formatted string
    magic_string = ''

    # loading in image
    image = np.array(Image.open(path).convert('RGBA'))

    rows, columns, _ = image.shape
    if rows % 2 != 0:
        raise "image height must be devideable by 2"

    # generating the string
    for i in range(0, rows, 2):
        for j in range(columns):
            top = image[i, j, :]
            bottom = image[i+1, j, :]

            magic_string += get_color_escape(top[0], top[1], top[2], background=False)
            magic_string += get_color_escape(bottom[0], bottom[1], bottom[2], background=True)
            magic_string += "▀"

        magic_string += '\033[0m\n'

    return magic_string


def get_color_escape(r, g, b, background=False):
    """ Given rgb values give the escape sequence for printing out the color"""
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


#get_pokemon_art("DSC00928.png")
write_pokemon_to_file(get_pokemon_art("mama.png"),"mama.txt")
#print( get_pokemon_art("DSC00928.png"))