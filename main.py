# This Python file uses the following encoding: utf-8

import sys
from PySide2 import *
# from __feature__ import snake_case
# from __feature__ import true_property

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType

from appcore import *

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    opencv = OpencvImageProvider()
    prMang = ProjectMenager()
    paintHan = PaintHandler()
    plgMenager = PolygonMenager()
    prcs = Processing(plgMenager, opencv)

    appCore = Appcore(projectMenager=prMang, opencvMenager=opencv, paintHandler=paintHan, polygonMenager=plgMenager,
                      processing=prcs)
    engine.addImageProvider("opencvImage", opencv)
    engine.rootContext().setContextProperty('appCore', appCore)

    engine.quit.connect(app.quit)
    engine.load('main.qml')

    sys.exit(app.exec_())
