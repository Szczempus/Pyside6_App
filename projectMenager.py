# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, Signal, QObject


class ProjectMenager(QObject):
    # projectNameChanged = Signal()

    def __init__(self, projectNameInit = "Papustka"):
        super().__init__()
        self.projectName = projectNameInit
        self._projectDescription = None
        self._projectLocation = None
        self._projectDate = None

        self.path = None

        pass

    # @Property(str)
    # def project_name(self):
    #     return self.projectName
    #
    # @project_name.setter
    # def set_project_name(self, name):
    #     self.projectName = name
    #     self.project_name_changed
    #     print(self.project_name)
    #
    # @Signal
    # def project_menager_glos(self):
    #     print("Daje glos")
    #     print(self.project_name)

    # def _name(self):
    #     return self._projectName
    #
    # @Signal
    # def name_changed(self):
    #     print(self._projectName)
    #     pass

    # @Slot(str)
    # def set_project_name(self, string):
    #     self.projectName = string
    #     print(self.projectName)

    # def _project_name(self):
    #     return self.projectName
    #
    # @Signal
    # def project_name_changed(self):
    #     pass
    #
    # @Slot(str)
    # def set_project_name(self, string):
    #     self.projectName = string
    #     self.project_name_changed.emit()
    #

    def get_project_name(self):
        return self.projectName

    def set_project_name(self, name):
        self.projectName = name
        print(self.projectName)


