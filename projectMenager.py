# This Python file uses the following encoding: utf-8
from PySide6 import QtCore


class ProjectMenager(QtCore.QObject):
    def __init__(self):

        self.projectName = "Cos"
        print(self.projectName)

        pass
