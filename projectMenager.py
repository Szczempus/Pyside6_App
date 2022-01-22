# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, Signal, QObject

import os


class ProjectMenager(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.projectName = None
        self.projectDescription = None
        self.projectLocation = None
        self.projectDate = None
        self.path = None

    @Slot("QString", "QString", "QString", "QString")
    def create_new_project(self, name, desc, loc, date):
        self.projectName = name
        self.projectDescription = desc
        self.projectLocation = loc
        self.projectDate = date
        self.path = os.getcwd()

        # Change project name
        self.projectNameChanged.emit(self.projectName)

    # TODO Dokończyć tworzenie folderu nowego projektu w app dir.
    def crete_directory(self):
        directory = self.projectMenager.projectName
        parent_dir = self.projectMenager.path

        path = os.path.join(parent_dir, directory)

    """
    Creating getters to properties    
    """

    def get_project_name(self):
        return self.projectName

    def get_project_des(self):
        return self.projectDescription

    def get_project_loc(self):
        return self.projectLocation

    def get_project_date(self):
        return self.projectDate

    def get_project_path(self):
        return self.path

    """
    Signals of property change 
    """
    projectNameChanged = Signal(str)
    projectDescriptionChanged = Signal(str)
    projectLocationChanged = Signal(str)
    projectDateChanged = Signal(str)
    projectPathChanged = Signal(str)

    """
    Properties
    """
    project_name = Property(str, get_project_name, notify=projectNameChanged)
    project_desc = Property(str, get_project_des, notify=projectDescriptionChanged)
    project_loc = Property(str, get_project_loc, notify=projectLocationChanged)
    project_date = Property(str, get_project_date, notify=projectDateChanged)
    project_path = Property(str, get_project_path, notify=projectPathChanged)
