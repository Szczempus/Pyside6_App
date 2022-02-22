# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Slot, Property, Signal, QObject

import os
import shutil
import pathlib


class ProjectMenager(QObject):
    fileExists = Signal()

    def __init__(self):
        QObject.__init__(self)
        self.projectName = "First Project"
        self.projectDescription = None
        self.projectLocation = None
        self.projectDate = None
        self.unixpath = None
        self.winpath = None

    @Slot("QString", "QString", "QString", "QString")
    def create_new_project(self, name, desc, loc, date):
        self.projectName = name
        self.projectDescription = desc
        self.projectLocation = loc
        self.projectDate = date

        # Get current working directory and create project directory
        self.winpath = os.getcwd()
        self.crete_directory()

    def crete_directory(self):
        directory = self.projectName
        parent_dir = self.winpath

        path = os.path.join(parent_dir, directory)
        winpath = path
        unixpath = path.replace("\\", "/")
        self.unixpath = unixpath
        self.winpath = winpath
        # print("WinPath: ", self.winpath)
        # print("UnixPath: ", self.unixpath)
        # Try to make project directory
        try:
            os.mkdir(path)
        except FileExistsError:
            # If exists emit signal to override
            self.fileExists.emit()

        except OSError as error:
            raise error
        else:
            # If not exists, current path is project path, project created
            self.project_created()

    def delete_project(self):
        path_cpy = self.winpath
        self.winpath = os.path.dirname(path_cpy)

        try:
            # os.close(path_cpy)
            # os.rmdir(path_cpy)
            # Removes all files in tree
            shutil.rmtree(path_cpy)
        except FileNotFoundError:
            raise FileNotFoundError("Nie znaleziono pliku")
        except OSError as error:
            raise error

    @Slot()
    def override_project(self):
        # If override delete existing project, create new one, and confirm it
        self.delete_project()
        self.crete_directory()
        self.project_created()

    def project_created(self):
        # Emit confirmation o creating project and change name in frontend
        self.projectNameChanged.emit(self.projectName)

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

    def get_project_unixpath(self):
        return self.unixpath

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
    project_path = Property(str, get_project_unixpath, notify=projectPathChanged)
