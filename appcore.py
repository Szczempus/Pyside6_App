# This Python file uses the following encoding: utf-8
import cv2
from PySide2.QtCore import Slot, Property, QObject, Signal
# from PySide2.QtQml import QmlElement, QmlSingleton
from PySide2.QtWidgets import QFileDialog

import os
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider
from paintHandler import PaintHandler
from polygonMenager import PolygonMenager
from analysisBackend import Processing


class Appcore(QObject):
    projectMenagerChanged = Signal()
    opencvImageProviderChanged = Signal()
    paintHandlerChanged = Signal()
    polygonMenagerChanged = Signal()
    procesManagerChanged = Signal()

    def __init__(self, projectMenager: ProjectMenager, opencvMenager: OpencvImageProvider, paintHandler: PaintHandler,
                 polygonMenager: PolygonMenager, processing: Processing):
        super(Appcore, self).__init__()
        self.projectMenager = projectMenager
        self.opencvMenager = opencvMenager
        self.paintHandler = paintHandler
        self.polygonMenager = polygonMenager
        self.processingManager = processing

        print(self.projectMenager)

    @Slot("QString")
    def save_image(self, path_to_save_image: str):
        print("Otrzymana ścieżka", path_to_save_image)
        # Split file and desired path
        _, path = path_to_save_image.split("///")
        # TODO Check if path has correct format

        img = self.opencvMenager.get_image()
        # TODO Check if image is not none

        # TODO Write in correct file format
        cv2.imwrite(path, img)

    def save_project(self):
        pass

    def create_report(self):
        pass

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

    def get_proces_menager(self):
        return self.processingManager

    """
    Properties exposed to QML
    """
    prMeg = Property(ProjectMenager, get_project_menager, notify=projectMenagerChanged)
    openCV = Property(OpencvImageProvider, get_opnecv_menager, notify=opencvImageProviderChanged)
    paintHan = Property(PaintHandler, get_paint_handler, notify=paintHandlerChanged)
    polyMeg = Property(PolygonMenager, get_polygon_menager, notify=polygonMenagerChanged)
    proces = Property(Processing, get_proces_menager, notify=procesManagerChanged)
