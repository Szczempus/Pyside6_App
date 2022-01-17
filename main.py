# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from appcore import Appcore
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

opencv = OpencvImageProvider
prMang = ProjectMenager()

appCore = Appcore(projectMenager=prMang, opencvMenager=opencv)

engine.rootContext().setContextProperty('appCore', appCore)
# engine.rootContext().setContextProperty('projectMenager', pRojectMenager)
engine.quit.connect(app.quit)
engine.load('main.qml')

sys.exit(app.exec())
