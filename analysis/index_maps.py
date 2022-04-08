from .index_map_base import IndexMap
from ALGORITHMS import vari_map


class Vari(IndexMap):

    def __init__(self, **kwargs):
        super(Vari, self).__init__(**kwargs)

        self.result_image = None
        self.analysis_name = "Vari"

    def analysis(self, cropped_rect_band_list: list = None):
        if cropped_rect_band_list is not None:
            self.croopped_bands = cropped_rect_band_list
        if self.croopped_bands is None:
            raise TypeError(f"None cropped bands passed in object {self}")
            return None

        try:
            self.index_image = vari_map(self.croopped_bands)
            self.result_image = self.create_cmapped_image()
            self.index_value = self.calculate_index()

            return self.result_image

        except Exception as e:
            print(f"Error: {e}")
            return None

