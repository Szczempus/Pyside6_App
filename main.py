# This Python file uses the following encoding: utf-8

import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from appcore import Appcore

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
appCore = Appcore()
engine.rootContext().setContextProperty('appCore', appCore)
engine.quit.connect(app.quit)
engine.load('main.qml')

sys.exit(app.exec())
