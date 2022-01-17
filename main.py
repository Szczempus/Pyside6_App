# This Python file uses the following encoding: utf-8

import sys
from PySide6 import *
from __feature__ import snake_case
from __feature__ import true_property

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType

from appcore import Appcore
from projectMenager import ProjectMenager
from opencvImageProvider import OpencvImageProvider

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

opencv = OpencvImageProvider
prMang = ProjectMenager()

# qmlRegisterSingletonType(Appcore, "AppCore", 1, 0, "AppInfo")

appCore = Appcore(projectMenager=prMang, opencvMenager=opencv)

engine.root_context().set_context_property('appCore', appCore)

# engine.rootContext().setContextProperty('projectMenager', prMang)
# engine.rootContext().setContextProperty('projectMenager', pRojectMenager)
engine.quit.connect(app.quit)
engine.load('main.qml')

sys.exit(app.exec())
