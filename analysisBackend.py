import cv2
import matplotlib.cm
import pandas
import geopandas
from PySide2.QtCore import Slot, Signal, QObject, QThread
from deepforest import main

from polygonMenager import PolygonMenager
from opencvImageProvider import OpencvImageProvider
from crop_img import *
from ALGORITHMS.maps import *
from ALGORITHMS.detectron_prediction import *

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
# Todo z importem nowego zdjęcia usunąć poligony z listy

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


def proportion_is_ok(width, height, proportion):
    if width / height > proportion or width / height < 1 / proportion:
        return True
    else:
        return False


def mistleton_detector(original_image, coords):
    rgb, _ = crop_rgb(original_image[:, :, :3], coords)
    model = main.deepforest()
    model.use_amp = True
    model.use_release()

    predictions = model.predict_tile(image=rgb, return_plot=False, patch_size=800, patch_overlap=0.1,
                                     iou_threshold=0.4, thresh=0.8)



    pass


def tree_crown_detector(original_image, coords):
    print("Analysis 12 - Tree crown detector")
    rgb, _ = crop_rgb(original_image[:, :, :3], coords)
    model = main.deepforest()
    model.use_amp = True
    model.use_release()

    # boxes = model.predict_tile(image=rgb, return_plot=False, patch_size=800, patch_overlap=0.1,
    #                            iou_threshold=0.4, thresh=0.8)
    # print(type(boxes))
    # print(boxes)
    # boxes = boxes.to_numpy()
    # print(boxes)
    # # Pandas data frame boxes
    # for box in boxes:
    #     rgb = cv2.circle(rgb, (int((box[2] - box[0]) / 2), int((box[3] - box[1]) / 2)), radius=2,
    #                      color=(0, 0, 255), thickness=2)
    # image = rgb

    img = model.predict_tile(image=rgb, return_plot=True, patch_size=800, patch_overlap=0.1,
                             iou_threshold=0.4, thresh=0.8)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    image = cv.cvtColor(img, cv.COLOR_BGR2BGRA)

    return image


def segmentaion_analysis(byte_band_list, coords):
    print("Analysis 11 - Segmentation")

    index_image = osavi_map(byte_band_list)
    my_cmap = matplotlib.cm.get_cmap("Spectral")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255
    print("Wielkośc obrazu", image.shape)
    rgb, _ = crop_rgb(image[:, :, :3], coords)
    print("Wielkość rgb ", rgb.shape)

    cfg = config_init("", 4000, 8, 1)
    image = prediction(cfg, rgb[:, :, ::-1],
                       model_path="C:/Users/quadro5000/PycharmProjects/detectron2_training/detectron2/output/model_final.pth")

    return image


def mistletone_analysis(cropped_rect, original_image, coords):
    print("Analysis 10 - Mistolete")
    mis_image = mis_map(cropped_rect)
    ndvi_image = ndvi_map(cropped_rect)
    mis_filtered = mis_filtration(mis_image, ndvi_image)
    int_mis = mis_filtered.astype(int) * 255
    image, _ = crop_rgb(original_image[:, :, :3], coords)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if int_mis[i, j] == 255:
                image[i, j] = (0, 255, 255)

    return image


def vari_analysis(cropped_rect):
    print("Analysis 9 - seismic")
    index_image = vari_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("BrBG")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def osavi_analysis(cropped_rect):
    print("Analysis 8 - OSAVI")
    index_image = osavi_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("BrBG")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def sipi2_analysis(cropped_rect):
    print("Analysis 7 - SIPI2")
    index_image = sipi2_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("coolwarm")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def ndre_analysis(cropped_rect):
    print("Analysis 6 - NDRE")
    index_image = ndre_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("RdBu")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def mcar_analysis(cropped_rect):
    print("Analysis 5 - MCAR")
    index_image = mcar_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("BrBG")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def lci_analysis(cropped_rect):
    print("Analysis 4 - LCI")
    index_image = lci_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("PiYG")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def gndvi_analysis(cropped_rect):
    print("Analysis 3 - GNDVI")
    index_image = gndvi_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("RdYlGn")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def bndvi_analysis(cropped_rect):
    print("Analysis 2 - BNDVI")
    index_image = bndvi_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("RdYlBu")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


def ndvi_analysis(cropped_rect):
    print("Analysis 1 - NDVI")
    index_image = ndvi_map(cropped_rect)
    my_cmap = matplotlib.cm.get_cmap("Spectral")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return image


class Worker(QObject):
    workerFinished = Signal(str)
    workerInProgress = Signal()
    workerResult = Signal(object)
    workerException = Signal(Exception)

    def __init__(self, img_provider: OpencvImageProvider, polygon_provider: PolygonMenager, analysis: int):
        super(Worker, self).__init__()
        self._img_manager = img_provider
        self._polygon_manager = polygon_provider
        self._analysis = analysis

    def run(self):
        byte_band_list = []
        poligon_list = []
        checked_polygon_list = []

        original_image = self._img_manager.get_image()

        byte_band_list = self._img_manager.get_byte_band_list()
        poligon_list = self._polygon_manager.get_polygon_list()
        checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]

        if checked_polygon_list is None or len(checked_polygon_list) == 0:
            print("None polygon")
            self.workerFinished.emit("Fail")
            return

        for polygon in checked_polygon_list:
            coords = []
            for point in polygon.get_point_list():
                point = (point.x_get(), point.y_get())
                coords.append({"x": point[0], "y": point[1]})

            cropped_rect, params = crop_band_list(byte_band_list, coords)

            if self._analysis == 1:
                image = ndvi_analysis(cropped_rect)

            elif self._analysis == 2:
                image = bndvi_analysis(cropped_rect)

            elif self._analysis == 3:
                image = gndvi_analysis(cropped_rect)

            elif self._analysis == 4:
                image = lci_analysis(cropped_rect)

            elif self._analysis == 5:
                image = mcar_analysis(cropped_rect)

            elif self._analysis == 6:
                image = ndre_analysis(cropped_rect)

            elif self._analysis == 7:
                image = sipi2_analysis(cropped_rect)

            elif self._analysis == 8:
                image = osavi_analysis(cropped_rect)

            elif self._analysis == 9:
                image = vari_analysis(cropped_rect)

            elif self._analysis == 10:
                image = mistletone_analysis(cropped_rect, original_image=original_image, coords=coords)

            elif self._analysis == 11:
                image = segmentaion_analysis(byte_band_list, coords)

            elif self._analysis == 12:
                image = tree_crown_detector(original_image, coords)

            polygon, _, _ = poly_img(image, coords, params[0], params[1],
                                     original_image[params[1]: params[1] + params[3],
                                     params[0]:params[0] + params[2]])
            original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = polygon

            self._img_manager.write_image(original_image)

            print("Koniec procesu")
            self.workerFinished.emit("Success")
        return


class Processing(QObject):
    isProcessing = Signal(bool, str, arguments=['val', "status"])

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

        self.isProcessing.emit(True, "")

    def stop_analysis(self, status):
        print("Proces zakończony")
        self.isProcessing.emit(False, status)

    def print_exception(self, e):
        raise Exception(e)
        self.isProcessing.emit(False, staus)
        self._thread.quit()
        self._thread.deleteLater()
