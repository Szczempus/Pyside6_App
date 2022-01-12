# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, QThread, QSize
from PySide6.QtGui import QImageReader, QImage
from PySide6.QtQml import QQmlImageProviderBase
from PySide6.QtQuick import QQuickImageProvider


class OpencvImageProvider(QQuickImageProvider):
    def __init__(self):
        # QThread.__init__(self)
        QQuickImageProvider.__init__(self, QQmlImageProviderBase.Image,
                                     )

        self.image_file_path = None
        self.image = None

        pass

    def requestImage(self, str: str, size: QSize, req_size: QSize) -> QImage:
        image = self.image
        if image is None:
            return QQuickImageProvider.requestImage(self, str, size)


        return img

