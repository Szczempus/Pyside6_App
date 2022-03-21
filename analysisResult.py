from PySide2.QtCore import QObject, Property, Signal, Slot


class AnalysisResult(QObject):
    """
    Analysis result class
    """

    # analysisDictChanged = Signal()
    analysisModelChanged = Signal()

    def __init__(self, analysis_type: int, **kwargs):
        super(AnalysisResult, self).__init__()

        self._fast_id = None  # 1 or 2 for index map or counting
        # Typ analizy
        self.analysis_type: str = self.analysis_type_to_string(analysis_type)
        # Współrzędne poligonu
        self.coordinates: tuple(float) = None
        # Ilość wszystkich próbek
        self.counting_total: int = None
        # Ilość chorych próbek
        self.sick: int = None
        # Ilość zdrowych próbek
        self.health: int = None
        # Wielkość wskaźnika
        self.map_calculus: float = None
        # Model listy do QML
        self.list_model = []

        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
            else:
                raise KeyError(key)


    def get_model(self):
        if self._fast_id == 1:
            self.list_model = [self.coordinates, self.map_calculus]
        else:
            self.list_model = [self.coordinates, self.counting_total, self.sick, self.health]
        return self.list_model

    # def create_analysis_model(self):
    #     print(self.__dict__)
    #     # In QML this is returned as QVariant
    #     return self.__dict__

    # dictonary = self.__dict__
    # model = []
    # for key, value in dictonary.items():
    #     if value is not None:
    #         model.append(value)
    # print(model)

    def analysis_type_to_string(self, analysis_type: int) -> str:
        if analysis_type == 1:
            self._fast_id = 1
            return "Wskaźnik NDVI"
        elif self._analysis == 2:
            self._fast_id = 1
            return "Wskaźnik BNDVI"
        elif self._analysis == 3:
            self._fast_id = 1
            return "Wskaźnik GNDVI"
        elif self._analysis == 4:
            self._fast_id = 1
            return "Wskaźnik LCI"
        elif self._analysis == 5:
            self._fast_id = 1
            return "Wskaźnik MCARI"
        elif self._analysis == 6 or self._analysis == 14 or self._analysis == 15 or self._analysis == 16 or self._analysis == 17:
            self._fast_id = 1
            return "Wskaźnik NDRE"
        elif self._analysis == 7:
            self._fast_id = 1
            return "Wskaźnik SIPI2"
        elif self._analysis == 8:
            self._fast_id = 1
            return "Wskaźnik OSAVI"
        elif self._analysis == 9:
            self._fast_id = 1
            return "Wskaźnik VARI"
        elif self._analysis == 10:
            self._fast_id = 1
            return "Wskaźnik Jemioły "
        elif self._analysis == 11:
            self._fast_id = 2
            return "Segemntacja"
        elif self._analysis == 12:
            self._fast_id = 2
            return "Detektor koron drzew"
        elif self._analysis == 13:
            self._fast_id = 2
            return "Detektor jemioły"

    # analysisResultList = Property(dict, create_analysis_model, notify=analysisDictChanged)


    analysisModel = Property(list, get_model, notify=analysisModelChanged)


if __name__ == "__main__":
    analysis = AnalysisResult(analysis_type=1, coordinates=(15.4505450934, 22.43984700), map_calculus=1.22)
    print(analysis.create_analysis_model())
    print(analysis.__doc__)
    print(analysis.__dir__())
    print(analysis.__str__())
