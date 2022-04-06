from PySide2.QtCore import QObject, Slot, Signal
from ALGORITHMS.maps import vari_map

class VARI(QObject):

    def __init__(self, **kwargs):
        super().__init__()

        self._croopped_bands: list = None
        self._index_value: float = None
        self._analysis_name: str = "Wskaźnik VARI"


    @staticmethod
    def analysis(cropped_bands: list):
        index_image = vari_map(cropped_bands)
        pass
