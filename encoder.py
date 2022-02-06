"""
'Short Morse Code' (TM) encoder script.

Under the courtesy of the Facecode.IO
"""

# Dependencies
import cv2
import numpy as np
import matplotlib.pyplot as plt
import utils.utils as utils


"""Encodes data to an image"""


def encode(data: str, is_inverted=False) -> bool:
    # Determine how many lines are required to encode the data
    no_lines_required = utils.calculate_required_no_lines(data)
    print(no_lines_required, "lines required")

    # Generate a blank image to fit the the no_lines_required to encode data unto
    is_inverted, base_img = utils.create_base_image(
        no_lines=no_lines_required, is_inverted=is_inverted)

    # Write the data as morse code onto the image
    image = utils._write_image_encodings(
        image=base_img, data=data, is_inverted=is_inverted)

    # Showing the image with OpenCV
    cv2.imwrite("encoded_image.png", image)
    # cv2.waitKey(0)

    # Showing the image with Matplot
    # plt.imshow(image)
    # plt.show()


encode("kendricklamar", is_inverted=False)
