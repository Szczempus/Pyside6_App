import os
import time
import numpy as np
from sahi.slicing import slice_image
import cv2 as cv

# from deepforest import main
# from deepforest import get_data
# from deepforest import utilities
# from deepforest import preprocess

"""
Skrypt ponownie trenuje sieć RetinaNet na modelu deepforest.
Adnotacje pisane są w pliku .csv w formacie:
    path/to/image1.jpg, x1, y1, x2, y2, class_name
    path/to/image2.jpg, x1, y1, x2, y2, class_name
    ...
"""




if __name__ == "__main__":

    cwd = "C:/Users/quadro5000/Desktop/LAs18_sliced/"
    image = "Las18_oryginal_Rgb.png"

    path = cwd + image


    slice_image_result, num_total_invalid_segme = slice_image(image=path, output_dir=cwd + "sliced/", output_file_name="Las18_sliced", slice_width=400, slice_height=400)

    print(slice_image_result)
    print(num_total_invalid_segme)
    pass
