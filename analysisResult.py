import numpy
from PySide2.QtCore import QObject, Property, Signal, Slot


class AnalysisResult(QObject):
    """
    Analysis result class
    """

    # analysisDictChanged = Signal()
    analysisModelChanged = Signal()
    analTypeGet = Signal()

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
            self.list_model = [f"Współrzędne: \n{self.coordinates[0]} S; {self.coordinates[1]} N",
                               f"Wartość wskaźnika: {self.map_calculus:.2f}"]
        else:
            self.list_model = [f"Współrzędne: \n {self.coordinates[0]} S; {self.coordinates[1]} N",
                               f"Ilość predykcji {self.counting_total}", self.sick, self.health]
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

    def set_predictions(self, predicitons):
        self.counting_total = len(predicitons)

    def analysis_type_to_string(self, analysis_type: int) -> str:
        if analysis_type == 1:
            self._fast_id = 1
            return "Wskaźnik NDVI"
        elif analysis_type == 2:
            self._fast_id = 1
            return "Wskaźnik BNDVI"
        elif analysis_type == 3:
            self._fast_id = 1
            return "Wskaźnik GNDVI"
        elif analysis_type == 4:
            self._fast_id = 1
            return "Wskaźnik LCI"
        elif analysis_type == 5:
            self._fast_id = 1
            return "Wskaźnik MCARI"
        elif analysis_type == 6 or analysis_type == 14 or analysis_type == 15 or analysis_type == 16 or analysis_type == 17:
            self._fast_id = 1
            return "Wskaźnik NDRE"
        elif analysis_type == 7:
            self._fast_id = 1
            return "Wskaźnik SIPI2"
        elif analysis_type == 8:
            self._fast_id = 1
            return "Wskaźnik OSAVI"
        elif analysis_type == 9:
            self._fast_id = 1
            return "Wskaźnik VARI"
        elif analysis_type == 10:
            self._fast_id = 1
            return "Wskaźnik Jemioły "
        elif analysis_type == 11:
            self._fast_id = 2
            return "Segemntacja"
        elif analysis_type == 12:
            self._fast_id = 2
            return "Detektor koron drzew"
        elif analysis_type == 13:
            self._fast_id = 2
            return "Detektor jemioły"

    # analysisResultList = Property(dict, create_analysis_model, notify=analysisDictChanged)

    def get_anal_type(self):
        return self.analysis_type

    analysisModel = Property(list, get_model, notify=analysisModelChanged)
    analysisType = Property("QString", get_anal_type, notify=analTypeGet)


if __name__ == "__main__":
    analysis = AnalysisResult(analysis_type=1, coordinates=(15.4505450934, 22.43984700), map_calculus=1.22)
    print(analysis.create_analysis_model())
    print(analysis.__doc__)
    print(analysis.__dir__())
    print(analysis.__str__())
