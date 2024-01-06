from write_string_to_file import write_string_to_file
import generator
import argparse
import os.path
import sys

DESCRIPTION = 'Displays an image in terminal using Box-drawing characters and ANSI escape codes.'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('image', metavar='image-file', type=str, help='image to display')
    parser.add_argument('-o', metavar='example.txt', type=str, required=False,
                        help='write output into a file instead of printing it to the terminal')
    args = parser.parse_args()

    if not os.path.isfile(args.image):
        print(f"Provided file ({args.image}) does not exits.", file=sys.stderr)
        exit(-1)

    if args.o is None:
        generator.print_to_stdout(args.image)
    else:
        write_string_to_file(generator.get_magic_string(args.image), args.o)
    # print(args.image, args.output)
