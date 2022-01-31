from PySide2.QtCore import QObject, Property, Signal, Slot, QPointF

minimum_distance = 0.5

'''
Polygon Coords Handler
'''


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


'''
Custom Polygon handler
'''


class CustomPolygon(QObject):
    nameChanged = Signal()
    pointListChanged = Signal()
    finishedChanged = Signal()
    hoveredChanged = Signal()
    polygonCenterChanged = Signal()


    def __init__(self, name):
        super(CustomPolygon, self).__init__()
        self._name = name
        self._finished = None
        self._hovered = None
        self._isChecked = None
        self._pointList = []
        self._polygonCenter = None
        pass

    # name property section
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # pointList property section
    def set_point(self, x, y):
        poly_coord = PolygonCoords()
        poly_coord.y_set(y)
        poly_coord.x_set(x)
        self._pointList.append(poly_coord)

    def get_point_list(self):
        return self._pointList

    # finished property section
    def get_finished(self):
        return self._finished

    def set_finished(self, val):
        self._finished = val

    # hovered property section
    def get_hoverd(self):
        return self._hovered

    def set_hovered(self, val):
        self._hovered = val

    # polygonCenter property section
    def get_polygon_center(self):
        x = 0
        y = 0
        for coords in range(0, len(self._pointList)):
            x = x + coords.x_get
            y = y + coords.y_get
        if len(self._pointList) > 0:
            x = x / len(self._pointList)
            y = y / len(self._pointList)
        return QPointF(x, y)

    name = Property("QString", get_name, set_name, notify=nameChanged)
    pointList = Property(list, get_point_list, notify=pointListChanged)
    finished = Property(bool, get_finished, set_finished, notify=finishedChanged)
    hovered = Property(bool, get_hoverd, set_hovered, notify=hoveredChanged)
    polygonCenter = Property(QPointF, get_polygon_center, notify=polygonCenterChanged)


'''
Polygons List Menager
'''


class PolygonMenager(QObject):
    polygonListChanged = Signal()
    newPolygonCreated = Signal(CustomPolygon, arguments=["poly"])

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

        # print("Nowy Poligon Python") #Działa

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
