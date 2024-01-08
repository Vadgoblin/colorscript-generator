from write_string_to_file import write_string_to_file
import generator
import argparse
import os.path
import sys

DESCRIPTION = 'Displays an image in terminal using Box-drawing characters and ANSI escape codes.'


def die(message):
    print(message, file=sys.stderr)
    exit(-1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('image', metavar='image-file', type=str, help='image to display')

    parser.add_argument('-o', metavar='example.txt', type=str, required=False,
                        help='write output into a file instead of printing it to the terminal')

    parser.add_argument('--no-resize', action='store_true', required=False,
                        help='do not resize the image automatically;'
                             ' only have effect when image is displayed directly in the terminal')

    parser.add_argument('-s', metavar='123x123', type=str, required=False,
                        help='resizes the image; if width or height is not provided (e.g., "x64" or "32x"),'
                             ' it will be automatically calculated')

    args = parser.parse_args()

    if not os.path.isfile(args.image):
        die(f"Provided file ({args.image}) does not exits.")

    if args.s and args.no_resize:
        die("The --no-resize and -s cannot be used together.")

    size = None

    if args.s:
        try:
            width, height = str.split(args.s.lower(), 'x')

            width = int(width) if width != "" else -1
            height = int(height) if height != "" else -1

            if width == 0 or height == 0:
                raise Exception
            if width == height == -1:
                raise Exception

            size = (width, height)

        except:
            die(f"\"{args.s}\" is an invalid size.")

    if args.o:
        write_string_to_file(generator.get_magic_string(args.image, size), args.o)
    else:
        if sys.stdout.isatty() and not args.s and not args.no_resize:
            size = "auto"
        generator.print_to_stdout(args.image, size)
