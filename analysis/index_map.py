import numpy as np
import matplotlib
from PySide2.QtCore import QObject, Slot, Signal
from ALGORITHMS.maps import index_calculation


class IndexMap(QObject):

    def __init__(self, **kwargs):
        super().__init__()

        self._croopped_bands: list = None
        self._index_value: float = None
        self._analysis_name: str = None
        self._index_image: np.ndarray = None
        self._index_value: float = None
        self._color_map = "Spectral"

    def index_calculus(self, threshold_value: float) -> float:
        index_value = index_calculation(threshold_value, self._index_image)
        return index_value

    def create_cmapped_image(self, color_map=None):
        if color_map is not None:
            # Todo check is color_map is valid
            self._color_map = color_map
        my_cmap = matplotlib.cm.get_cmap(self._color_map)
        color_mapped_image = my_cmap(self._index_image)
        numpy_image = np.asarray(color_mapped_image)

        pass
