# This Python file uses the following encoding: utf-8
from PySide6 import QtCore


from projectMenager import ProjectMenager


class Appcore(QtCore.QObject):
    def __init__(self):
        super().__init__()

        self.projectMenager = ProjectMenager()

        pass

    @QtCore.Slot()
    def changeNameProject(self):

        self.projectMenager.projectName = "Papustka"

        print(self.projectMenager.projectName)
