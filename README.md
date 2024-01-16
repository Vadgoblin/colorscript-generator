# Colorscript generator

Display image in the terminal or generate colorscript.
Inspired by and based on [Phoney badger's pokemon-colorscripts ](https://gitlab.com/phoneybadger/pokemon-colorscripts)

## Description
Converts an image into a sequence of ANSI escape codes and [Block Elements](https://en.wikipedia.org/wiki/Block_Elements).
When rendered in a terminal emulator, it will display the image.
Keep in mind that the maximum image size a terminal can display is limited.
Maximum width is the terminal's width in characters and the maximum height terminal's height in characters times two.
Exceeding terminal's width results in improper rendering.
By default, when the program displays the image directly in the terminal, it will automatically downscale, if necessary, to fit inside the terminal window. 
However, note that there is no automatic downscaling if the output of the program is piped or used the `-o` flag.

## Usage
```plaintext
usage: main.py [-h] [-o example.txt] [--no-resize] [-s 123x123] image-file

Displays an image in terminal using Box-drawing characters and ANSI escape codes.

positional arguments:
  image-file      image to display

options:
  -h, --help      show this help message and exit
  -o example.txt  write output into a file instead of printing it to the terminal
  --no-resize     do not resize the image automatically; only have effect when image is
                  displayed directly in the terminal
  -s 123x123      resizes the image; if width or height is not provided (e.g., "x64" or "32x"),
                  it will be automatically calculated
```

### Requirements
The program was written in `python3`. It requires the following two python packages: `numpy` and `PIL`.<br />
The terminal emulator must be support true color, use monospace font and be able to display [Block Elements](https://en.wikipedia.org/wiki/Block_Elements) 

## License
The MIT License (MIT)
