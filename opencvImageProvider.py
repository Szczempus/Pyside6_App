# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QSize, QByteArray
from PySide2.QtGui import QImage, QImageReader
from PySide2.QtQuick import QQuickImageProvider
import cv2 as cv


class OpencvImageProvider(QQuickImageProvider):
    def __init__(self):
        # QThread.__init__(self)
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image,
                                                  QQuickImageProvider.ForceAsynchronousImageLoading)
        self.image_file_path = None
        self.image = None


        pass

    def requestImage(self, path: str, size: QSize, req_size: QSize) -> QImage:
        img = self.image
        if img is None:
            self.image_file_path = path.split("///", 1)
            reader = QImageReader(path[1])
            print(path[1])
            img = cv.imread(path[1])

            # Todo załadowac obraz tiff, zrobić checking itp

            # cv.imshow("Załadowałe", img)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            # is_success, img_buf_array = cv.imencode(".png", img)
            # img_byte_array = img_buf_array.tobytes()
            #
            # bytearr = QByteArray(img_byte_array)
            # self.image = QImage()
            # self.image.loadFromData(bytearr, "PNG")

        # return self.image
        return reader.read()


