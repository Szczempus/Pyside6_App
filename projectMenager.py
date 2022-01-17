# This Python file uses the following encoding: utf-8
from PySide6.QtCore import Slot, Property, Signal, QObject

import os


class ProjectMenager(QObject):

    def __init__(self):
        super().__init__()
        self.projectName = None
        self.projectDescription = None
        self.projectLocation = None
        self.projectDate = None
        self.path = None

        pass

    @Slot(str, str, str, str)
    def create_new_project(self, name, desc, loc, date):
        self.projectName = name
        self.projectDescription = desc
        self.projectLocation = loc
        self.projectDate = date
        self.path = os.getcwd()

        # print(self.projectName,
        #       self.projectDescription,
        #       self.projectLocation, self.projectDate, self.path)

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
    Properties
    """
    project_name = Property(str, get_project_name)
    project_desc = Property(str, get_project_des)
    project_loc = Property(str, get_project_loc)
    project_date = Property(str, get_project_date)
    project_path = Property(str, get_project_path)
