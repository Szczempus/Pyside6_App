from PySide6.QtCore import QObject, Property, Signal


class PolygonCoords(QObject):
    hoveredChanged = Signal()

    def __init__(self):
        super(PolygonCoords, self).__init__()
        self._x = None
        self._y = None

    hovered = Property(bool, notify=hoveredChanged)
    x = Property(float,)


class CustomPolygon(QObject):

    def __init__(self):
        super(CustomPolygon, self).__init__()

        pass


class PolygonMenager(QObject):

    def __init__(self):
        super(PolygonMenager, self).__init__()

        pass
