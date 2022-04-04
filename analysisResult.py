from PySide2.QtCore import QObject, Property, Signal, Slot


class AnalysisResult(QObject):
    """
    Analysis result class
    """

    # analysisDictChanged = Signal()
    analysisModelChanged = Signal()
    analTypeGet = Signal()
    predListGet = Signal()
    predictionListSet = Signal(list)

    def __init__(self, analysis_type=None, **kwargs):
        super(AnalysisResult, self).__init__()

        self._fast_id = None  # 1 or 2 for index map or counting
        # Typ analizy
        self.analysis_type: str = analysis_type
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
        # Model listy predykcji
        self.pred_lis_model = []
        self.accuracy: float = None

        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
            else:
                raise KeyError(key)

    def get_model(self):
        if self._fast_id == 1:
            self.list_model = [f"Współrzędne:\n{self.coordinates[0]} S; {self.coordinates[1]} N",
                               f"Wartość wskaźnika: {self.map_calculus:.2f}"]
        elif self._fast_id == 2:
            self.list_model = [f"Współrzędne:\n {self.coordinates[0]} S; {self.coordinates[1]} N",
                               f"Ilość predykcji: {self.counting_total}",
                               f"Ilość zainfekowanych drzew: {self.sick}",
                               f"Ilość zdrowych drzew: {self.counting_total - self.sick}"
                               ]

        return self.list_model

    def get_anal_type(self):
        return self.analysis_type

    @Slot()
    def get_prediction_list(self):
        return self.pred_lis_model

    def set_predictions(self, predicitons):
        self.counting_total = len(predicitons)

    def set_sick(self, num_of_sick):
        self.sick = num_of_sick

    def set_list_poligons(self, list_of_polygons):
        print(f"List: {list_of_polygons}")
        self.pred_lis_model = list_of_polygons
        self.predictionListSet.emit(self.pred_lis_model)
        print(f"sygnał listy wyemitowanty")

    def set_accuracy(self, val):
        self.accuracy = val

    def get_accuracy(self):
        return self.accuracy

    def set_fast_id(self, val):
        self._fast_id = val

    def get_fast_id(self):
        return self._fast_id

    def analysis_type_to_string(self, analysis_type: int) -> str:
        if analysis_type == 1:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik NDVI"

        elif analysis_type == 2:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik BNDVI"

        elif analysis_type == 3:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik GNDVI"

        elif analysis_type == 4:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik LCI"

        elif analysis_type == 5:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik MCARI"

        elif analysis_type == 6 or analysis_type == 14 or analysis_type == 15 or analysis_type == 16 or analysis_type == 17:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik NDRE"

        elif analysis_type == 7:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik SIPI2"

        elif analysis_type == 8:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik OSAVI"

        elif analysis_type == 9:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik VARI"

        elif analysis_type == 10:
            self._fast_id = 1
            self.analysis_type = "Wskaźnik Jemioły "

        elif analysis_type == 11:
            self._fast_id = 2
            self.analysis_type = "Segemntacja"

        elif analysis_type == 12:
            self._fast_id = 2
            self.analysis_type = "Detektor koron drzew"

        elif analysis_type == 13:
            self._fast_id = 2
            self.analysis_type = "Detektor jemioły"

    analysisModel = Property(list, get_model, notify=analysisModelChanged)
    analysisType = Property("QString", get_anal_type, notify=analTypeGet)
    predictionsList = Property(list, get_prediction_list, notify=predListGet)


if __name__ == "__main__":
    analysis = AnalysisResult(analysis_type=1, coordinates=(15.4505450934, 22.43984700), map_calculus=1.22)
    print(analysis.create_analysis_model())
    print(analysis.__doc__)
    print(analysis.__dir__())
    print(analysis.__str__())
