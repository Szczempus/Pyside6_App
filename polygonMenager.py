from PySide2.QtCore import QObject, Property, Signal, Slot, QPointF
from math import sqrt

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
        self.hover_changed.emit()

    x = Property(float, x_get, x_set, notify=x_changed)
    y = Property(float, y_get, y_set, notify=y_changed)


'''
Custom Polygon handler
'''


class CustomPolygon(QObject):
    nameChanged = Signal()
    pointListChanged = Signal()
    finishedChanged = Signal(bool, arguments=['val'])
    hoveredChanged = Signal()
    polygonCenterChanged = Signal()
    isCheckedChanged = Signal()
    addPointResult = Signal(bool, arguments=['res'])

    def __init__(self, name):
        super(CustomPolygon, self).__init__()
        self._name = name
        self._finished = False
        self._hovered = False
        self._isChecked = False
        self._pointList = []
        self._polygonCenter = None
        pass

    @Slot(float, float)
    def addPoint(self, x, y):
        result = True
        distance = 0.0
        if len(self._pointList) == 0:
            for coords in self._pointList:
                distance = sqrt(((coords.x_get - x) ** 2) + ((coords.y_get - y) ** 2))
                if distance < minimum_distance:
                    result = False

        if result:
            poly_coords = PolygonCoords(x, y)
            self._pointList.append(poly_coords)
            self.pointListChanged.emit()
            self.polygonCenterChanged.emit()
            self.addPointResult.emit(result)

    @Slot(PolygonCoords)
    def removePoint(self, poly_coords):
        for cooord in self._pointList:
            if cooord == poly_coords:
                self._pointList.remove(cooord)
        self.pointListChanged.emit()
        self.polygonCenterChanged.emit()

    # name property section
    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    # pointList property section
    def set_point(self, x, y):
        poly_coord = PolygonCoords(x, y)
        self._pointList.append(poly_coord)

    def get_point_list(self):
        return self._pointList

    # finished property section
    def get_finished(self):
        return self._finished

    def set_finished(self, val):
        self._finished = val
        self.finishedChanged.emit(val)

    # hovered property section
    def get_hoverd(self):
        return self._hovered

    def set_hovered(self, val):
        self._hovered = val
        self.hoveredChanged.emit()

    # polygonCenter property section
    def get_polygon_center(self):
        x = 0
        y = 0
        for coords in self._pointList:
            x = x + coords.x_get()
            y = y + coords.y_get()
        if len(self._pointList) > 0:
            x = x / len(self._pointList)
            y = y / len(self._pointList)
        return QPointF(x, y)

    # isChecked property section
    def get_is_checked(self):
        return self._isChecked

    def set_is_checked(self, val):
        self._isChecked = val
        self.isCheckedChanged.emit()

    name = Property("QString", get_name, set_name, notify=nameChanged)
    pointList = Property(list, get_point_list, notify=pointListChanged)
    finished = Property(bool, get_finished, set_finished, notify=finishedChanged)
    hovered = Property(bool, get_hoverd, set_hovered, notify=hoveredChanged)
    polygonCenter = Property(QPointF, get_polygon_center, notify=polygonCenterChanged)
    isChecked = Property(bool, get_is_checked, set_is_checked, notify=isCheckedChanged)


'''
Polygons List Manager
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
        if name == "" or name == " ":
            polygon_name = "Poly " + str(self._polygon_counter + 1)
        else:
            polygon_name = name

        # Create new polygon of CustomPolygon class with name
        self._last_polygon = CustomPolygon(polygon_name)
        self._polygonList.append(self._last_polygon)
        self.newPolygonCreated.emit(self._last_polygon)
        self.polygonListChanged.emit()

    @Slot(CustomPolygon)
    def deletePolygon(self, polygon):
        for poly in self._polygonList:
            if poly == polygon:
                self._polygonList.remove(poly)
                self.polygonListChanged.emit()

    # Todo dokończyć sprawdzanie czy kursor jest w poligonie
    @Slot(float, float)
    def isPolygonHovered(self, x, y):
        for polygon in self._polygonList:
            pass

    def is_point_in_polygon(self, pkt: tuple, polygon: list) -> bool:
        inside = False

        minX = polygon[0].x_get()
        maxX = polygon[0].x_get()
        minY = polygon[0].y_get()
        maxY = polygon[0].y_get()

        for point in polygon:
            minX = min(point.x_get(), minX)
            maxX = max(point.x_get(), maxX)
            minY = min(point.y_get(), minY)
            maxY = max(point.y_get(), maxY)

        if pkt[0] < minX or pkt[0] > maxX or pkt[1] < minY or pkt[1] > maxY:
            return inside

        for point in polygon:
            pass

    polygonList = Property(list, get_polygon_list, notify=polygonListChanged)
