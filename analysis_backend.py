import cv2
import matplotlib.cm
import numpy as np
from PySide2.QtCore import Slot, Signal, QObject, QThread
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from deepforest import main
import sys, time
from tqdm import tqdm
from numpy import ndarray

from polygonMenager import PolygonMenager
from opencvImageProvider import OpencvImageProvider
from jsonparser import parse_json
from crop_img import crop_img
# from save_polygon import save_polygon
from ALGORITHMS.watershed import watershed
from ALGORITHMS.maps import *

'''
IMPORTANT INFO 
GDAL paginate rasters number from 1 to n, NOT FROM 0 !
Agisoft exports channels with this order: 
channel 1 - Blue
channel 2 - Green
channel 3 - Red 
channel 5 - NIR
channel 6 - LWIR(thermal) wymagane jest jeszcze przekształcenie danych z kelwinów na st. celcujsza  
'''

# Todo zrobić warunek czy mamy chociaż jeden poligon czy nie
# Todo zrobić obłsugę emita w sytuacji gdy masz proces w trakcie a gdy już go skńczysz.

"""
1. W Workerze, najpierw pobieramy listę kanałów w zapisie bajtowym i listę poligonów
2. Sprawdzamy które poligony mają wartość "isChecked" == True i te bierzemy do analizy
3. Z tych poligonów robimy listę
4. Cropujemy bandy do kwadratu wymiaru poligonu, analizujemy je i docinamy do poligonu
5. Nakładamy kolorek na powstałą mapę 
6. W zadanych współrzędnych mergujemy mapę orgynalną z tą z analizy 
7. Wysyłamy sygnał do QML'a o reset parametru source z image providerem
8. W requstImage jeżeli przyjdzie pusty string onzacza to że to jest odswieżenie obrazu i wysyłamy
    nadpisany obraz do QML'a  
"""


class Worker(QObject):
    workerFinished = Signal()
    workerInProgress = Signal()
    workerResult = Signal(object)
    workerException = Signal(Exception)

    def __init__(self, img_provider: OpencvImageProvider, polygon_provider: PolygonMenager, analysis: int):
        super(Worker, self).__init__()
        self._img_manager = img_provider
        self._polygon_manager = polygon_provider
        self._analysis = analysis

    def create_colorfull_map(self):
        pass

    def run(self):
        if self._analysis == 1:
            print("Analysis 1 - NDVI")

            byte_band_list = self._img_manager.get_byte_band_list()
            poligon_list = self._polygon_manager.get_polygon_list()
            checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]
            coords = []
            i = 0

            for polygon in checked_polygon_list:
                for point in polygon.get_point_list():
                    point = (point.x_get(), point.y_get())
                    coords.append({"x": point[0], "y": point[1]})
                _, cropped_rect, params = crop_img(byte_band_list, coords)
                print(params)
                ndvi_image = ndvi_map(cropped_rect)

                my_cmap = matplotlib.cm.get_cmap("Spectral")
                color_array = my_cmap(ndvi_image)

                x = np.asarray(color_array)
                try:
                    x = np.asarray(color_array)
                    x = int(x * 255)
                    polygon, _, _ = crop_img(x, coords)
                except Exception as e:
                    self.workerException.emit(e)
                # pts = []
                #
                # for coord in coords:
                #     pts.append([int(coord["x"]), int(coord["y"])])
                #
                # polygon_pts = np.array(pts)
                # copy_polygon_pts = polygon_pts
                #
                # copy_polygon_pts = copy_polygon_pts - copy_polygon_pts.min(axis=0)

                print("Map generated sucessfull")
                print("Zdjęcie", polygon)
                print("Wymiary anlizy", polygon.shape)
                original_image = self._img_manager.get_image()
                print("Kopiowanie zdjecia")

                try:
                    original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = polygon[:, :, :4]
                except Exception as e:
                    self.workerException.emit(e)
                print("Nadpisanie ")
                self._img_manager.write_image(original_image)

                print("Wysłanie")

            print("Koniec procesu")
            self.workerFinished.emit()

        if self._analysis == 2:
            print("Analysis 2 - LCI")

            self.workerFinished.emit()

        if self._analysis == 3:
            print("Analysis 3 - Segmentation")

            self.workerFinished.emit()

        if self._analysis == 4:
            print("Analysis 4 - Counting")

            self.workerFinished.emit()


class Processing(QObject):
    isProcessing = Signal(bool, arguments=['val'])

    def __init__(self, polygon_manager: PolygonMenager, opencv: OpencvImageProvider):
        super(Processing, self).__init__()
        self._polygon_manager = polygon_manager
        self._image_provider = opencv
        self._analysis = None
        self._worker = None
        self._thread = None

    @Slot(int)
    def start_analysis(self, analysis):
        print("Zacząłem analizę")
        self._analysis = analysis
        # Creating Worker and new Thread
        self._thread = QThread()
        self._worker = Worker(self._image_provider, self._polygon_manager, self._analysis)
        # Moving Worker to Thread
        self._worker.moveToThread(self._thread)
        # Connecting signals and slots to run and terminate Thread and Worker
        self._thread.started.connect(self._worker.run)
        self._worker.workerFinished.connect(self.stop_analysis)
        self._worker.workerFinished.connect(self._thread.quit)
        self._worker.workerFinished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._worker.workerException.connect(self.print_exception)

        self._thread.start()

        self.isProcessing.emit(True)

    def stop_analysis(self):
        print("Proces zakończony")
        self.isProcessing.emit(False)

    def print_exception(self, e):
        print(e)
        self._thread.quit
        self._thread.deleteLater

    def print_restult(self, image):
        pass
        # print("Slot received")
        # img = self._image_provider.get_image()
        # print(type(image))
        # print(type(img))

        # px = 1 / plt.rcParams['figure.dpi']
        # print("Slot received1")
        # if imaghe.shape == 3:
        #     x_size, y_size, _ = imaghe.shape
        # else:
        #     x_size, y_size = imaghe.shape
        # print("Slot received2")
        # plt.ioff()
        # print("Slot received3")
        # fig, ax = plt.subplots(figsize=(x_size * px, y_size * px))
        # print("Slot received4")
        # plot_image = plt.imshow(imaghe, cmap=plt.get_cmap("Spectral"), vmin=0, vmax=1, resample=True)
        # print("Slot received5")
        # ax.axis('off')
        # canvas = FigureCanvasAgg(fig)
        # print("Slot received6")
        # canvas.draw()
        # print("Slot received7")
        # buf = canvas.buffer_rgba()
        # print("Slot received8")
        # x = np.asarray(buf)
        # print("Slot received9")
        # plt.imsave("TO_TO_ZDJECIE.png", x)
        # print("Slot received10")
