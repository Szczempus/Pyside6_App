from PySide2.QtCore import QObject, Property, Signal, Slot
from select import select

minimum_distance = 0.5


class PolygonCoords(QObject):

    def __init__(self, x, y):
        super(PolygonCoords, self).__init__()
        self._x = x
        self._y = y
        self._hovered = False

    def x_get(self):
        return self._x

    def x_set(self, x_coord):
        self._x = x_coord

    @Signal
    def x_changed(self):
        pass

    def y_get(self):
        return self._y

    def y_set(self, y_coord):
        self._y = y_coord

    @Signal
    def y_changed(self):
        pass

    @Signal
    def hover_changed(self):
        pass

    @Property(bool, notify=hover_changed)
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, val):
        self._hovered = val

    x = Property(float, x_get, x_set, notify=x_changed)
    y = Property(float, y_get, y_set, notify=y_changed)


class CustomPolygon(QObject):

    def __init__(self, name):
        super(CustomPolygon, self).__init__()
        self._name = name

        pass

    @Signal
    def name_changed(self):
        pass

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    name = Property("QString", get_name, set_name, notify=name_changed)
    pointList = Property(list, )


class PolygonMenager(QObject):
    polygonListChanged = Signal()
    newPolygonCreated = Signal(CustomPolygon, arguments=["polygon"])

    def __init__(self):
        super(PolygonMenager, self).__init__()
        self._polygonList = []
        self._polygon_counter = 0
        self._last_polygon = None

        pass

    def get_polygon_list(self):
        return self._polygonList

    @Slot(str)
    def startNewPolygon(self, name):
        polygon_name = ""
        if name == "":
            polygon_name = "Poly " + str(self._polygon_counter + 1)
        else:
            polygon_name = name

        # Create new polygon of CustomPolygon class with name
        self._last_polygon = CustomPolygon(polygon_name)
        self._polygonList.append(self._last_polygon)
        
        # Todo obsłużyć nowy sposób zwracania poligonów
        self.newPolygonCreated.emit(self._last_polygon)

    polygonList = Property(list, get_polygon_list, notify=polygonListChanged)
