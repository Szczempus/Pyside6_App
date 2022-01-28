# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Slot, Property, QObject, Signal
# from PySide2.QtQml import QmlElement, QmlSingleton
from PySide2.QtWidgets import QFileDialog

# TODO zamienić Pyside6 na PyQt5

import os
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider
from paintHandler import PaintHandler
from polygonMenager import PolygonMenager


class Appcore(QObject):

    projectMenagerChanged = Signal()
    opencvImageProviderChanged = Signal()
    paintHandlerChanged = Signal()
    polygonMenagerChanged = Signal()

    def __init__(self, projectMenager: ProjectMenager, opencvMenager: OpencvImageProvider, paintHandler: PaintHandler,
                 polygonMenager: PolygonMenager):
        super(Appcore, self).__init__()
        self.projectMenager = projectMenager
        self.opencvMenager = opencvMenager
        self.paintHandler = paintHandler
        self.polygonMenager = polygonMenager

        print(self.projectMenager)

    """
    Property setters and getters
    """

    def get_project_menager(self):
        return self.projectMenager

    def get_opnecv_menager(self):
        return self.opencvMenager

    def get_paint_handler(self):
        return self.paintHandler

    def get_polygon_menager(self):
        return self.polygonMenager

    """
    Properties exposed to QML
    """
    prMeg = Property(ProjectMenager, get_project_menager, notify=projectMenagerChanged)
    openCV = Property(OpencvImageProvider, get_opnecv_menager, notify=opencvImageProviderChanged)
    paintHan = Property(PaintHandler, get_paint_handler, notify=paintHandlerChanged)
    polyMeg = Property(PolygonMenager, get_polygon_menager, notify=polygonMenagerChanged)

