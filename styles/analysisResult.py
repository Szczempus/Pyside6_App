from PySide2.QtCore import QObject, Property, Signal, Slot
from polygonMenager import CustomPolygon

class AnalysisResult(QObject):

    def __init__(self, polygon: CustomPolygon):
        super(AnalysisResult, self).__init__()

        # Poligon (obiekt)
        self._polygon = polygon
        # Nazwa poligonu
        self._polygon_name = None
        # Typ analizy
        self._analysis_type = None
        # Współrzędne poligonu
        self._coordinates = None
        # Ilość wszystkich próbek
        self._counting_total = None
        # Ilość chorych próbek
        self._sick = None
        # Ilość zdrowych próbek
        self._health = None
        # Wielkość wskaźnika
        self._map_calulus = None

    @staticmethod
    def process_polygon(polygon):
        pass





class AnalysisManager(QObject):

    def __init__(self):
        super(AnalysisManager, self).__init__()

        self._analysis_list: list(AnalysisResult) = []

    def append_analysis(self, analysis: AnalysisResult):
        self._analysis_list.append(analysis)

    def get_analysis_list(self):
        return self._analysis_list

    def get_analysis(self, polygon:CustomPolygon):
        for analysis in self._analysis_list:
            pass

