# This Python file uses the following encoding: utf-8

import sys
from PySide6 import *
from __feature__ import snake_case
from __feature__ import true_property

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType

from appcore import *

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

opencv = OpencvImageProvider
prMang = ProjectMenager()
paintHan = PaintHandler()

# qmlRegisterSingletonType(Appcore, "AppCore", 1, 0, "AppInfo")

appCore = Appcore(projectMenager=prMang, opencvMenager=opencv, paintHandler=paintHan)

engine.root_context().set_context_property('appCore', appCore)

engine.quit.connect(app.quit)
engine.load('main.qml')

sys.exit(app.exec())
