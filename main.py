"""
Main app runfile
"""
# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from appcore import *

if __name__ == "__main__":

    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    opencv = OpencvImageProvider()
    prMang = ProjectMenager()
    paintHan = PaintHandler()
    plgMenager = PolygonMenager()
    prcs = Processing(plgMenager, opencv)

    appCore = Appcore(projectMenager=prMang,
                      opencvMenager=opencv,
                      paintHandler=paintHan,
                      polygonMenager=plgMenager,
                      processing=prcs)
    engine.addImageProvider("opencvImage", opencv)
    engine.rootContext().setContextProperty('appCore', appCore)

    engine.quit.connect(app.quit)
    engine.load('main.qml')

    sys.exit(app.exec_())
