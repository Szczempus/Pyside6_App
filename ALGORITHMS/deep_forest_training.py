import os
import time
import numpy as np
from deepforest import main
from deepforest import get_data
from deepforest import utilities
from deepforest import preprocess

"""
Skrypt ponownie trenuje sieć RetinaNet na modelu deepforest.
Adnotacje pisane są w pliku .csv w formacie:
    path/to/image1.jpg, x1, y1, x2, y2, class_name
    path/to/image2.jpg, x1, y1, x2, y2, class_name
    ...
"""


if __name__ == "__main__":
    pass