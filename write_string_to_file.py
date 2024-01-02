def write_string_to_file(magic_string, output_path):
    with open(output_path, 'w') as file:
        file.write(magic_string)
