from PySide2.QtCore import QObject, Property
import math


class PaintHandler(QObject):

    def __init__(self):
        super(PaintHandler, self).__init__()

        self.points_list = []
        self.lastX = 0
        self.lastY = 0
        self.firstX = 0
        self.firstY = 0

    def point(self, x, y):
        coords = [x, y]
        if self.lastX and self.lastY == 0:
            self.lastX = x
            self.lastY = y
            self.firstX = x
            self.firstY = y
            self.points_list.append(coords)
        else:
            if not (self.lastX == x and self.lastY == y):
                if math.abs(x - self.lastX) > 1 or math.abs(y - self.lastY) > 1:
                    self.lastX = x
                    self.lastY = y
                    self.points_list.append(coords)
                    print("Punkty dodane")
                else:
                    print("Punkty za blisko siebie")

    def get_points_list(self):
        return self.points_List

    pointsList = Property("QVariantList", get_points_list)
