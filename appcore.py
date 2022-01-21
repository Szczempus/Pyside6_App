# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlSingleton

import os
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider
from paintHandler import PaintHandler


class Appcore(QObject):

    projectSignal = Signal()

    def __init__(self, projectMenager: ProjectMenager, opencvMenager: OpencvImageProvider, paintHandler: PaintHandler):
        super(Appcore, self).__init__()
        self.projectMenager = projectMenager
        self.opencvMenager = opencvMenager
        self.paintHandler = paintHandler

        print(self.projectMenager)

        pass

    @Property(ProjectMenager, notify=projectSignal)
    def prMeg(self):
        return self.projectMenager

    @prMeg.setter
    def prMeg(self, val):
        self.projectMenager = val
        # self.projectMenager.setParent(self)



    # @Slot()
    # def app_core_signal(self):
    #     self.projectMenager.project_menager_signal()
    #     print("appCore receive signal")

    """
    Property setters and getters
    """

    def get_project_menager(self):
        return self.projectMenager

    def get_opnecv_menager(self):
        return self.opencvMenager

    def get_paint_handler(self):
        return self.paintHandler

    """
    Properties seen by QML
    """
    # prMeg = Property(ProjectMenager, get_project_menager, notify=projectSignal)
    openCV = Property(OpencvImageProvider, get_opnecv_menager)
    paintHan = Property(PaintHandler, get_paint_handler)


