# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, QObject, Signal

from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider


class Appcore(QObject):

    def __init__(self, project_menager: ProjectMenager, parent=None):
        QObject.__init__(self, parent)

        self.projectMenager = project_menager
        # self._opencvImageProvider = OpencvImageProvider()

        pass

    @Signal
    def app_core_signal(self):
        print("appCore signal")

    # @Property(ProjectMenager, notify=projectMenagerChanged)
    # def project_menager(self):
    #     return self.projectMenager
    #
    # @project_menager.setter
    # def set_project_menager(self, project_menager):
    #     self.projectMenager = project_menager
    #     self.projectMenagerChanged.emit()

    # def _project_menager(self):
    #     return self._projectMenager
    #
    # @Signal
    # def project_menager_changed(self):
    #     pass


    # project_menager = Property(ProjectMenager, _project_menager, notify=project_menager_changed)

    # @Slot()
    # def changeNameProject(self):
    #
    #     self._projectMenager.projectName = "Papustka"
    #
    #     print(self._projectMenager.projectName)
