import os
import time
import cv2
import matplotlib.cm
from PySide2.QtCore import Slot, Signal, QObject, QThread
from deepforest import main

from polygonMenager import PolygonMenager
from opencvImageProvider import OpencvImageProvider
from crop_img import crop_band_list, poly_img
from ALGORITHMS.maps import *
from ALGORITHMS.color_corection import simplest_cb

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
# Todo zrobić obłsugę emita w sytuacji gdy nasz proces jest w trakcie a gdy już go kończysz.

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

    def run(self):

        if self._analysis == 1:
            print("Analysis 1 - NDVI")

            byte_band_list = []
            poligon_list = []
            checked_polygon_list = []

            original_image = self._img_manager.get_image()

            try:
                byte_band_list = self._img_manager.get_byte_band_list()
                poligon_list = self._polygon_manager.get_polygon_list()
                checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]

            except Exception as e:
                self.workerException.emit(e)

            for polygon in checked_polygon_list:
                coords = []
                for point in polygon.get_point_list():
                    point = (point.x_get(), point.y_get())
                    coords.append({"x": point[0], "y": point[1]})

                try:
                    cropped_rect, params = crop_band_list(byte_band_list, coords)
                except Exception as e:
                    self.workerException.emit(e)

                ndvi_image = ndvi_map(cropped_rect)

                my_cmap = matplotlib.cm.get_cmap("Spectral")
                color_array = my_cmap(ndvi_image)
                try:
                    image = np.asarray(color_array)
                    image = image * 255
                except Exception as e:
                    self.workerException.emit(e)

                try:
                    print("Type", type(image))
                    print("Shape", image.shape)

                    # image = cv.cvtColor(image[:, :, :3], cv.COLOR_BGR2RGB)
                    #
                    # polygon, _, _ = poly_img(image, coords, params[0], params[1],
                    #                          original_image[params[1]: params[1] + params[3],
                    #                          params[0]:params[0] + params[2]])
                    original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = image
                except Exception as e:
                    self.workerException.emit(e)

            self._img_manager.write_image(original_image)

            print("Koniec procesu")
            self.workerFinished.emit()

        if self._analysis == 2:
            print("Analysis 2 - LCI")

            byte_band_list = []
            poligon_list = []
            checked_polygon_list = []

            try:
                byte_band_list = self._img_manager.get_byte_band_list()
                # print("1")
                # print(byte_band_list)
                poligon_list = self._polygon_manager.get_polygon_list()
                # print("2")
                print(poligon_list)
                checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]
                # print("3")
                # print(checked_polygon_list)
                coords = []
                i = 0
            except Exception as e:
                self.workerException.emit(e)

            for polygon in checked_polygon_list:
                # print("3")
                for point in polygon.get_point_list():
                    # print("4")
                    point = (point.x_get(), point.y_get())
                    # print("5")
                    coords.append({"x": point[0], "y": point[1]})
                    # print("6")
                # print(coords)
                try:
                    cropped_rect, params = crop_band_list(byte_band_list, coords)
                except Exception as e:
                    self.workerException.emit(e)
                # print("7")
                # print(params)
                lci_image = lci_map(cropped_rect)

                my_cmap = matplotlib.cm.get_cmap("plasma")
                color_array = my_cmap(lci_image)
                try:
                    image = np.asarray(color_array)
                    image = image * 255
                except Exception as e:
                    print("Polygon error")
                    self.workerException.emit(e)

                original_image = self._img_manager.get_image()

                try:
                    original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = image
                except Exception as e:
                    print("Merging error")
                    self.workerException.emit(e)
                # print("Nadpisanie ")
                self._img_manager.write_image(original_image)

                # print("Wysłanie")

            print("Koniec procesu")

            self.workerFinished.emit()

        if self._analysis == 3:
            print("Analysis 3 - Segmentation")

            self.workerFinished.emit()

        if self._analysis == 4:
            print("Analysis 4 - Counting")

            byte_band_list = []
            poligon_list = []
            checked_polygon_list = []

            try:
                byte_band_list = self._img_manager.get_byte_band_list()
                # print("1")
                # print(byte_band_list)
                poligon_list = self._polygon_manager.get_polygon_list()
                # print("2")
                print(poligon_list)
                checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]
                # print("3")
                # print(checked_polygon_list)
                coords = []
                i = 0
            except Exception as e:
                self.workerException.emit(e)

            for polygon in checked_polygon_list:
                # print("3")
                for point in polygon.get_point_list():
                    # print("4")
                    point = (point.x_get(), point.y_get())
                    # print("5")
                    coords.append({"x": point[0], "y": point[1]})
                    # print("6")
                # print(coords)
                try:
                    cropped_rect, params = crop_band_list(byte_band_list, coords)
                except Exception as e:
                    self.workerException.emit(e)

            try:
                rgb = rgb_image(cropped_rect)
                rgb = simplest_cb(rgb, 1)
                model = main.deepforest()
                model.use_amp = True
                model.use_release()
            except Exception as e:
                print("Model prepaing problem")
                self.workerException.emit(e)

            try:
                img = model.predict_tile(image=rgb, return_plot=True, patch_size=800, patch_overlap=0.1,
                                         iou_threshold=0.4, thresh=0.8)
            except Exception as e:
                print("Model prediction problem")
                self.workerException.emit(e)

            original_image = self._img_manager.get_image()
            img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)

            try:
                polygon, _, _ = poly_img(img, coords, params[0], params[1],
                                         original_image[params[1]: params[1] + params[3],
                                         params[0]:params[0] + params[2]])
                original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = polygon
            except Exception as e:
                self.workerException.emit(e)

            self.workerFinished.emit()

        if self._analysis == 5:
            print("Analysis 5 - Mistolete")

            byte_band_list = []
            poligon_list = []
            checked_polygon_list = []

            original_image = self._img_manager.get_image()

            try:
                byte_band_list = self._img_manager.get_byte_band_list()
                poligon_list = self._polygon_manager.get_polygon_list()
                checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]

            except Exception as e:
                self.workerException.emit(e)

            for polygon in checked_polygon_list:
                coords = []
                for point in polygon.get_point_list():
                    point = (point.x_get(), point.y_get())
                    coords.append({"x": point[0], "y": point[1]})

                try:
                    cropped_rect, params = crop_band_list(byte_band_list, coords)
                except Exception as e:
                    self.workerException.emit(e)

                try:
                    mis_image = mis_map(cropped_rect)
                    print("Mis map", mis_image)
                    ndvi_image = ndvi_map(cropped_rect)
                    print("ndvi map", ndvi_image)
                except Exception as e:
                    print("Index Map creating error")
                    self.workerException.emit(e)
                    return

                try:
                    mis_filtered = mis_filtration(mis_image, ndvi_image)
                    print("mis_filtred", mis_filtered)
                except Exception as e:
                    print("Mist filter error")
                    self.workerException.emit(e)
                    return

                int_mis = mis_filtered.astype(int) * 255

                rgb = rgb_image(cropped_rect)
                rgb = simplest_cb(rgb, 1)

                try:
                    for i in range(rgb.shape[0]):
                        for j in range(rgb.shape[1]):
                            if int_mis[i, j] == 255:
                                rgb[i, j] = (0, 255, 255)

                except Exception as e:
                    self.workerException.emit(e)

                try:
                    polygon, _, _ = poly_img(rgb, coords, params[0], params[1],
                                             original_image[params[1]: params[1] + params[3],
                                             params[0]:params[0] + params[2]])

                    original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = polygon
                except Exception as e:
                    self.workerException.emit(e)

            self._img_manager.write_image(original_image)

            print("Koniec procesu")
            self.workerFinished.emit()

        else:
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
        raise Exception(e)
        self._thread.quit()
        self._thread.deleteLater()

    def print_restult(self, image):
        pass
