from PySide2.QtCore import QObject, Slot, Signal
from ALGORITHMS.maps import vari_map

class VARI(QObject):

    def __init__(self, cropped_bands):
        super().__init__()

        self._croopped_bands = cropped_bands


    @staticmethod
    def analysis(cropped_bands):
        index_image = vari_map(cropped_bands)
        pass
