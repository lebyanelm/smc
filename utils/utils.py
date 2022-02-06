"""
'Short Morse Code' (TM) utilities script.

Under the courtesy of the Facecode.IO
"""

# Dependencies
import numpy as np
import utils.morse_encodings as m_e
import utils.guiders as guiders

"""Calculates the number of lines required for an encoding."""
# Helps with pre-determining the size of the encoding area, to set the image size


def calculate_required_no_lines(data: str) -> int:
    # The pointers added with the paddings from both sides
    current_line_size = (guiders._pointers * 2) + (guiders._padding * 2)
    maximum_line_size = 340
    no_lines = 1
    # Convert the text into all UPPERCASE
    data = data.upper()
    # Go through each character in the data to find the encodings
    for character_index, character in enumerate(data):
        if character_index + 1 == len(data):
            break
        else:
            character_encodings = m_e._encodings.get(character)
            if type(character_encodings) is int:
                character_encodings = [character_encodings]
            encoding_size = 0
            # Go through each character encoding and calculate it's size
            for encoding_index, character_encoding in enumerate(character_encodings):
                if character_encoding == 0:  # A Dash
                    encoding_size += guiders._dash
                else:
                    encoding_size += guiders._dot
                    # When the end of a character encoding is reached, add the spacings
                    if (encoding_index + 1) == len(character_encodings):
                        encoding_size += guiders._dot
                    # Check if there's space or a next line needs to be created
                    if (maximum_line_size - current_line_size) < 0:
                        current_line_size = encoding_size
                        no_lines += 1
                    else:
                        current_line_size += encoding_size
    return no_lines


def _get_required_morse_code_width(encodings: tuple, is_first_line: bool = False) -> int:
    required_morse_width = 0
    encodings = encodings if type(encodings) == tuple else [encodings]
    for encoding in encodings:
        space_width = guiders._space
        if encoding == 0:  # A dash
            encoding_width = guiders._dash
        else:
            encoding_width = guiders._dot
        required_morse_width += (encoding_width + space_width)
    return required_morse_width


"""Generates a base image, inverted=specifies whether or not to use black or white"""
# Should return a bool to define that the image is inverted or not


def _create_blank_image(height, width, is_inverted: bool = False) -> np.uint8:
    blank_img = np.zeros([height, width, 3], dtype=np.uint8)
    blank_img[:] = 255 if is_inverted == False else 0
    return blank_img


def create_base_image(no_lines: int = 1, is_inverted: bool = False) -> bool:
    _base_height = (guiders._padding * 2) + (no_lines * guiders._dot)
    _base_width = guiders._padding * 2 + guiders._max_width
    base_image = _create_blank_image(
        _base_height, _base_width, is_inverted=is_inverted)
    return is_inverted, add_image_border(base_image, is_inverted=is_inverted)


"""Adds a border around the edges of an image"""
# This helps with the detection of the box around the code when decoding


def add_image_border(image, thickness=5, is_inverted=False):
    img_height, img_width = len(image) + thickness, len(image[0]) + thickness
    border_image = _create_blank_image(
        img_height, img_width, is_inverted=True if not is_inverted else False)
    y_off = round((len(border_image) - len(image)) / 2)
    x_off = round((len(border_image[0]) - len(image[0])) / 2)
    border_image[y_off: (y_off + len(image)),
                 x_off: (x_off + len(image[0]))] = image
    return border_image


"""Draws the morse characters unto the base image"""

C_POS = 0
R_POS = 0


def _write_image_encodings(image: list, data: str, is_inverted: bool = False) -> list:
    # The global positions of the draw pointer
    global C_POS
    global R_POS

    # Draw the corner pointers
    image = _write_corner_pointers(image)

    # Set the start position from the first corner pointer
    C_POS = guiders._padding + (guiders._dot * 3)
    R_POS = guiders._padding

    # Make sure the data is always uppercase
    data = data.upper()

    for character_index, character in enumerate(data):
        character_morse_encodings = m_e._encodings[character]
        image = _draw_data(
            image=image, encodings=character_morse_encodings, is_inverted=is_inverted)

        if (character_index+1) == len(data):
            _fill_null(image=image)

    return image


def _draw_data(image: list, encodings: tuple, is_inverted=False, is_last_char=False) -> list:
    # The global positions of the draw pointer
    global C_POS
    global R_POS

    # Make sure the encodings are always iterable
    encodings = encodings if type(encodings) == tuple else [encodings]

    # Calculate the required width to encode the encodings
    # Checking if those encodings will fit in or not
    required_encodings_width = _get_required_morse_code_width(
        encodings=encodings)

    # Calculate the width on the row that's remaining
    # So the codes to overlap to the end of the encoding area
    remaining_encodings_width = (guiders._max_width) - C_POS

    # Check if we still at the first row or not
    # First row has two pointers that already take some of the space
    if R_POS == guiders._dot:
        print("Still on the first line")
        pointers_sizes = (guiders._dot * 3) * 2
        remaining_encodings_width -= pointers_sizes

    if required_encodings_width <= remaining_encodings_width:
        # Loop through every single encoding and draw the data on the image
        for encoding_index, encoding in enumerate(encodings):
            encoding_col_end = (
                C_POS + guiders._dot) if encoding == 1 else (C_POS + (guiders._dot * 2))
            encoding_row_end = R_POS + guiders._dot

            for row in range(R_POS, encoding_row_end):
                for col in range(C_POS, encoding_col_end):
                    image[row][col] = [
                        0, 0, 0] if not is_inverted else [255, 255, 255]

                    # Check when the end of the encoding has been reached
                    if (row + 1) == encoding_row_end and (col + 1) == encoding_col_end:
                        # Give in some space for the next code
                        C_POS += (guiders._dot + guiders._space) if encoding == 1 else (
                            (guiders._dot * 2) + guiders._space)

                        # Check if the whole morse encoding for a single character has been completed
                        # This is so to append another space, making it a double space
                        if (encoding_index + 1) == len(encodings):
                            C_POS += guiders._space
    else:
        print("Moving to a new line")
        # TODO: Fill up the remaining space in the row with the FILL NULL
        image = _fill_null(image=image)

        # Reset the current position of the draw cursor
        C_POS = guiders._padding
        R_POS += guiders._dot

        # Draw the data on that new row line
        _draw_data(image=image, encodings=encodings,
                   is_inverted=is_inverted, is_last_char=is_last_char)
    return image


def _fill_null(image: list) -> list:
    # The global positions of the draw pointer
    global C_POS
    global R_POS

    for row in range(R_POS, R_POS + guiders._dot):
        for col in range(C_POS, (guiders._max_width - (guiders._dot)) if R_POS == guiders._padding else guiders._max_width + 15):
            image[row][col] = [48, 33, 221]

    return image


"""Draws corner pointers that define the oriention of the code"""


def _write_corner_pointers(image: list) -> list:
    _base_pointer_width = guiders._dot * 3
    _base_pointer_height = guiders._dot
    # Positions that the pointers will be placed
    _pointer_1_pos = (guiders._padding, guiders._padding)
    _pointer_2_pos = (
        len(image[0]) - (guiders._padding + _base_pointer_width), guiders._padding)
    for _pointer in [_pointer_1_pos, _pointer_2_pos]:
        for row in range(guiders._dot, guiders._dot * 2):
            for col in range(_pointer[0], _pointer[0] + _base_pointer_width):
                image[row][col] = [0, 0, 217]
    return image
