# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, QThread, QSize, Slot
from PySide2.QtGui import QImageReader, QImage
from PySide6.QtQml import QQmlImageProviderBase
from PySide2.QtQuick import QQuickImageProvider, QQuickAsyncImageProvider
import cv2 as cv


class OpencvImageProvider(QQuickAsyncImageProvider):
    def __init__(self):
        # QThread.__init__(self)
        QQuickAsyncImageProvider.__init__(self, QQuickAsyncImageProvider.Image)

        self.image_file_path = None
        self.image = None

        pass

    def requestImage(self, path: str, size: QSize, req_size: QSize) -> QImage:
        img = self.image
        if img is None:
            path = path.split("///", 1)
            print(path[1])

            # img = cv.imread(path[1])
            # h, w, _ = img.shape

            # qimage = QImage(img.data, w, h, QImage.Format_BGR888)
            # img = qimage

        return img
