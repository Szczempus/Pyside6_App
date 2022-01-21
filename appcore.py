# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlSingleton

import os
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider


class Appcore(QObject):

    projectMenagerSignal = Signal(ProjectMenager)

    def __init__(self, projectMenager: ProjectMenager, opencvMenager: OpencvImageProvider):
        super(Appcore, self).__init__()
        self.projectMenager = projectMenager
        self.opencvMenager = opencvMenager

        print(self.projectMenager)

        pass

    # @Slot()
    # def app_core_signal(self):
    #     self.projectMenager.project_menager_signal()
    #     print("appCore receive signal")

    def get_project_menager(self):
        return self.projectMenager

    def get_opnecv_menager(self):
        return self.opencvMenager

    prMeg = Property(ProjectMenager, get_project_menager, notify=projectMenagerSignal)
    openCV = Property(OpencvImageProvider, get_opnecv_menager)
