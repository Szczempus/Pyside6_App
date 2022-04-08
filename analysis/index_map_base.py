import numpy as np
import matplotlib
from PySide2.QtCore import QObject, Slot, Signal, Property
from ALGORITHMS.maps import index_calculation


class IndexMap(QObject):
    mapThresholdChanged = Signal()
    indexValueChanged = Signal()
    analysisNameChanged = Signal()

    def __init__(self, croopped_bands: list = None,
                 analysis_name: str = None,
                 color_map: str = "Spectral",
                 threshold_of_index: float = None):

        self.croopped_bands: list = croopped_bands
        self.index_value: float = None
        self.analysis_name: str = analysis_name
        self.index_image: np.ndarray = None
        self.color_map: str = color_map
        self.threshold_of_index: float = threshold_of_index

    def calculate_index(self, threshold_value: float = None, normalize: bool = False) -> float:
        """
        Function calulation of map index. According to type of index, it can be normalized or not. Default it is not.
        Available is also setting custom threshold value, above witch index will be valid.

        :param threshold_value: threshold value of cut off values in index, typically between -1 and 1
        :param normalize: set the values between 0 and 1, default False
        :return: value of custom index.
        """
        try:
            if threshold_value is None:
                index_value = index_calculation(self.threshold_of_index, self.index_image, normalize)
            else:
                index_value = index_calculation(threshold_value, self.index_image, normalize)
            return index_value

        except Exception as e:
            print(f"Error: {e}")
            return None

    def create_cmapped_image(self, color_map=None) -> np.ndarray:
        """
        Function make colour image from index map in grayscale . Default is 'Spectral' cmap,
        but user can define other than that, which is valid with matplotlib specification.
        https://matplotlib.org/stable/tutorials/colors/colormaps.html

        :param color_map: Color map valid with matplotlib specification
        :return: image as numpy array full of color
        """
        try:
            if color_map is not None:
                my_cmap = matplotlib.cm.get_cmap(color_map)
                if my_cmap is not None:
                    self.color_map = color_map
                else:
                    print("Color map invalid, using default")
            my_cmap = matplotlib.cm.get_cmap(self.color_map)
            color_mapped_image = my_cmap(self.index_image)
            image = np.asarray(color_mapped_image)
            numpy_image = image * 255

            return numpy_image

        except Exception as e:
            print(f"Error: {e}")
            return None

    def set_threshold(self, val):
        self.threshold_of_index = val

    def get_threshold(self):
        return self.threshold_of_index

    def get_index_value(self):
        return self.index_value

    def get_analysis_name(self):
        return self.analysis_name

    threshold = Property(float, get_threshold, set_threshold, notify=mapThresholdChanged)
    indexValue = Property(float, get_index_value, notify=indexValueChanged)
    analysisName = Property(str, get_analysis_name, notify=analysisNameChanged)
