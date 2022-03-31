'''
Module to run analysis

IMPORTANT INFO
GDAL paginate rasters number from 1 to n, NOT FROM 0 !
Agisoft exports channels with this order:
channel 1 - Blue
channel 2 - Green
channel 3 - Red
channel 5 - NIR
channel 6 - LWIR(thermal) wymagane jest jeszcze przekształcenie danych z kelwinów na st. celcujsza

1. W Workerze, najpierw pobieramy listę kanałów w zapisie bajtowym i listę poligonów
2. Sprawdzamy które poligony mają wartość "isChecked" == True i te bierzemy do analizy
3. Z tych poligonów robimy listę
4. Cropujemy bandy do kwadratu wymiaru poligonu, analizujemy je i docinamy do poligonu
5. Nakładamy kolorek na powstałą mapę
6. W zadanych współrzędnych mergujemy mapę orgynalną z tą z analizy
7. Wysyłamy sygnał do QML'a o reset parametru source z image providerem
8. W requstImage jeżeli przyjdzie pusty string onzacza to że to jest odswieżenie obrazu i wysyłamy
    nadpisany obraz do QML'a

'''
import cv2

import matplotlib.cm
import numpy as np
from torch import load
import random
from PySide2.QtCore import Slot, Signal, QObject, QThread
from deepforest import main

from analysisResult import AnalysisResult
from polygonMenager import PolygonMenager, CustomPolygon, PolygonCoords
from opencvImageProvider import OpencvImageProvider
from crop_img import *
from ALGORITHMS import *

COLOR_MAP = "Spectral"


# Todo zrobić warunek czy mamy chociaż jeden poligon czy nie
# Todo z importem nowego zdjęcia usunąć poligony z listy
# Todo KAŻDA Z ANALIZ ODDZIELNĄ KLASĄ!!


def index_calculation(index_threshold: float, index_map) -> float:
    index_sum = np.sum(index_map)
    print(f"WARTOŚC SUMY INDEKSU: {index_sum}")
    above_thresh_sum = np.sum(index_map >= index_threshold)
    print(f"WARTOŚC SUMY POWYŻEJ 0.4: {above_thresh_sum}")
    map_value = above_thresh_sum / index_sum
    print(f"WARTOŚ WSKAŹNIKA:{map_value}")

    return map_value


def is_correct(pt1: tuple, pt2: tuple, tan_thresh_val):
    '''

    :param pt1:
    :param pt2:
    :param tan_thresh_val:
    :return:
    '''

    width = pt2[0] - pt1[0]
    height = pt2[1] - pt1[1]

    long = 0
    short = 0

    if width > height:
        long = width
        short = height
    elif height > width:
        long = height
        short = width
    elif height == width:
        return True

    tan = short / long

    if tan < tan_thresh_val:
        return False

    return True


def mistletone_detector(original_image, coords, cropped_bands):
    print("Analysis 13 - Mistletone detector")
    rgb, _ = crop_rgb(original_image[:, :, :3], coords)
    try:
        print("Loading model..")
        model = main.deepforest()
        print("Model loaded, loading weights...")
        # model.use_amp = True
        model.load_state_dict(load("weights/tuszyma19.pth"))
        print("Weights loaded, prediction...")

        predictions = model.predict_tile(image=rgb,
                                         return_plot=False,
                                         patch_size=1000,
                                         patch_overlap=0.1,
                                         iou_threshold=0.6,
                                         thresh=0.6)
    except Exception as e:
        return print(e)

    print("Prediction successful")

    numpy_pred = predictions.to_numpy()

    print("Pred. conv", numpy_pred)

    for index, predict in enumerate(numpy_pred):
        pt1 = (int(predict[0]), int(predict[1]))
        pt2 = (int(predict[2]), int(predict[3]))
        if predict[5] > 0.2 and is_correct(pt1, pt2, 0.5):
            # print("Drawing rec")
            # print(f"Pt1: {pt1}, pt2: {pt2}")
            # if sprawdzamy czy jest jemioła:
            #   rusujemy obwolutę na czerwono
            # else:

            coord1 = {
                "x": pt1[0],
                "y": pt1[1]
            }

            coord2 = {
                "x": pt2[0],
                "y": pt1[1]
            }

            coord3 = {
                "x": pt2[0],
                "y": pt2[1]
            }

            coord4 = {
                "x": pt1[0],
                "y": pt2[1]
            }

            bbox_coords = [coord1, coord2, coord3, coord4]

            try:
                roi_cropped_bands, crop_params = crop_band_list(cropped_bands, bbox_coords)

                # cv2.SimpleBlobDetector_Params
                image, int_mask = mistletone_analysis(cropped_rect=roi_cropped_bands, original_image=rgb, coords=bbox_coords)

                # TODO: Zbinaryzować, dylatacja, erozja, zamknięcie, regionproposal, blob
                # sqr = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
                # image = cv.dilate(image, sqr)
                cv.imwrite(f"kafelki_maski/kafelek_{index}.jpg", int_mask)
                cv.imwrite(f"kafelki_obrazu/kafelek_{index}.jpg", image)
                # print("image created")
                # mask = create_circular_mask(h=16, w=16)
                # print(f"Mask: {mask}")
                # template = np.dstack((np.zeros((16, 16), dtype=np.uint8),
                #                       np.ones((16, 16), dtype=np.uint8) * 255,
                #                       np.ones((16, 16), dtype=np.uint8) * 255))
                # print(f"Template: {template}")
                # template[~mask] = 0
                # print(f"Template after masking: {template}")
                # print(f"Time for template")
                # print(f"Is the same shape? {image.shape == template.shape}")
                # print(f"Image shape: {image.shape}, template shape: {template.shape}")
                # res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
                # print(f"Result{res}")
                # threshold = 0.4
                # print(f"Res > Threshold? : {np.any(res > threshold)}")
                #
                if np.any(image == [0, 255, 255]):
                    # if np.any(res > threshold):

                    # print(f"rysuje na czerwowono")
                    rgb = cv.rectangle(rgb, pt1, pt2, (0, 0, 255), thickness=1)
                else:
                    # print(f"rysuje na niebiesko")
                    rgb = cv.rectangle(rgb, pt1, pt2, (255, 0, 0), thickness=1)

                pt3 = (pt1[0], pt2[1] + 10)

                rgb = cv.putText(img=rgb,
                                 text=f"{predict[5]:.2f}",
                                 org=pt3,
                                 fontFace=cv.FONT_HERSHEY_SIMPLEX,
                                 fontScale=0.3,
                                 color=(255, 125, 255),
                                 thickness=1,
                                 lineType=cv.LINE_AA)

                print("Drawed")

            except Exception as e:
                return print(e)

    print("Draw edned")

    image = cv.cvtColor(rgb, cv.COLOR_BGR2BGRA)
    return numpy_pred, image


def tree_crown_detector(original_image, coords):
    '''

    :param original_image:
    :param coords:
    :return:
    '''

    print("Analysis 12 - Tree crown detector")
    rgb, _ = crop_rgb(original_image[:, :, :3], coords)
    model = main.deepforest()
    model.use_amp = True
    model.use_release()

    # # Pandas data frame boxes
    # for box in boxes:
    #     rgb = cv2.circle(rgb, (int((box[2] - box[0]) / 2), int((box[3] - box[1]) / 2)), radius=2,
    #                      color=(0, 0, 255), thickness=2)
    # image = rgb

    # img = model.predict_tile(image=rgb, return_plot=True, patch_size=1000, patch_overlap=0.1,
    #                          iou_threshold=0.4, thresh=0.2)

    try:
        pred = model.predict_tile(image=rgb, return_plot=False, patch_size=1000, patch_overlap=0.1,
                                  iou_threshold=0.4, thresh=0.2)

        for index, row in pred.iterrows():
            rgb = cv.rectangle(rgb, (int(row["xmin"]), int(row["ymin"])), (int(row["xmax"]), int(row["ymax"])),
                               color=(0, 165, 255), thickness=1, lineType=cv2.LINE_AA)

    except Exception as e:
        return print(e)

    # img = cv.cvtColor(rgb, cv.COLOR_RGB2BGR)
    image = cv.cvtColor(rgb, cv.COLOR_BGR2BGRA)

    return pred, image


def segmentaion_analysis(byte_band_list, coords):
    '''

    :param byte_band_list:
    :param coords:
    :return:
    '''

    print("Analysis 11 - Segmentation")

    index_image = osavi_map(byte_band_list)
    my_cmap = matplotlib.cm.get_cmap("Spectral")
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255
    print("Wielkośc obrazu", image.shape)
    rgb, _ = crop_rgb(image[:, :, :3], coords)
    print("Wielkość rgb ", rgb.shape)

    # cfg = config_init("", 4000, 8, 1)
    # image = prediction(cfg, rgb[:, :, ::-1],
    #                    model_path="weights/model_final.pth")

    return image


def mistletone_analysis(cropped_rect, original_image, coords):
    '''

    :param cropped_rect:
    :param original_image:
    :param coords:
    :return:
    '''

    try:

        print("Analysis 10 - Mistolete")
        mis_image = mis_map(cropped_rect)
        ndvi_image = ndvi_map(cropped_rect)
        mis_filtered = mis_filtration(mis_image, ndvi_image)
        int_mis = mis_filtered.astype(int) * 255

        image, crop_param = crop_rgb(original_image[:, :, :3], coords)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if int_mis[i, j] == 255:
                    image[i, j] = (0, 255, 255)


    except Exception as e:
        return print(e)


    return image, int_mis


def vari_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 9 - seismic")
    index_image = vari_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def osavi_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 8 - OSAVI")
    index_image = osavi_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def sipi2_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 7 - SIPI2")
    index_image = sipi2_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def ndre_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 6 - NDRE")
    index_image = ndre_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)
    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def mcar_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 5 - MCAR")
    index_image = mcar_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def lci_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 4 - LCI")
    index_image = lci_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def gndvi_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 3 - GNDVI")
    index_image = gndvi_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def bndvi_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 2 - BNDVI")
    index_image = bndvi_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


def ndvi_analysis(cropped_rect):
    '''

    :param cropped_rect:
    :return:
    '''

    print("Analysis 1 - NDVI")
    index_image = ndvi_map(cropped_rect)
    map_value = index_calculation(0.4, index_map=index_image)
    my_cmap = matplotlib.cm.get_cmap(COLOR_MAP)

    color_array = my_cmap(index_image)
    image = np.asarray(color_array)
    image = image * 255

    return map_value, image


class Worker(QObject):
    """
    Worker docstring
    """

    workerFinished = Signal(str)
    workerInProgress = Signal()
    workerResult = Signal(object)
    workerException = Signal(Exception)

    def __init__(self,
                 img_provider: OpencvImageProvider,
                 polygon_provider: PolygonMenager,
                 analysis: int):
        super(Worker, self).__init__()
        self._img_manager: OpencvImageProvider = img_provider
        self._polygon_manager: PolygonMenager = polygon_provider
        self._analysis_number = analysis

    def calculate_geolocation(self, params: list):
        x = params[0] + params[2] / 2
        y = params[1] + params[3] / 2

        posX = self._img_manager.get_pixel_size()[0] * x + self._img_manager.get_geolocation()[0]
        posY = self._img_manager.get_pixel_size()[1] * y + self._img_manager.get_geolocation()[1]

        posX += self._img_manager.get_pixel_size()[0] / 2
        posY += self._img_manager.get_pixel_size()[1] / 2

        print(f"Coordinates: {posX, posY}")

        return posX, posY

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
        # Polygon declaring type
        polygon: CustomPolygon
        for polygon in checked_polygon_list:
            coords = []
            map_value = None
            pred = None
            # Point declaring type
            point: PolygonCoords
            for point in polygon.get_point_list():
                point = (point.x_get(), point.y_get())
                coords.append({"x": point[0], "y": point[1]})

            cropped_rect, params = crop_band_list(byte_band_list, coords)

            if self._analysis_number == 1:
                map_value, image = ndvi_analysis(cropped_rect)

            elif self._analysis_number == 2:
                map_value, image = bndvi_analysis(cropped_rect)

            elif self._analysis_number == 3:
                map_value, image = gndvi_analysis(cropped_rect)

            elif self._analysis_number == 4:
                map_value, image = lci_analysis(cropped_rect)

            elif self._analysis_number == 5:
                map_value, image = mcar_analysis(cropped_rect)

            elif self._analysis_number == 6 or self._analysis_number == 14 or self._analysis_number == 15 or self._analysis_number == 16 or self._analysis_number == 17:
                map_value, image = ndre_analysis(cropped_rect)

            elif self._analysis_number == 7:
                map_value, image = sipi2_analysis(cropped_rect)

            elif self._analysis_number == 8:
                map_value, image = osavi_analysis(cropped_rect)

            elif self._analysis_number == 9:
                map_value, image = vari_analysis(cropped_rect)

            elif self._analysis_number == 10:
                image, _ = mistletone_analysis(cropped_rect,
                                            original_image=original_image,
                                            coords=coords)

            elif self._analysis_number == 11:
                pass
                # Pyinstaller ma problem z detectron2
                # Nie możliwe jest wykonywanie detekcji bez skompilowanej CUD'Y

                # try:
                #     image = segmentaion_analysis(cropped_rect, coords)
                # except Exception as e:
                #     self.workerException.emit(e)

            elif self._analysis_number == 12:
                pred, image = tree_crown_detector(original_image, coords)

            elif self._analysis_number == 13:
                pred, image = mistletone_detector(original_image, coords, cropped_rect)

            poly, _, _ = poly_img(image, coords, params[0], params[1],
                                  original_image[params[1]: params[1] + params[3],
                                  params[0]:params[0] + params[2]])
            original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = poly

            geolocation = self.calculate_geolocation(params)
            try:
                analysis_result = AnalysisResult(self._analysis_number, coordinates=geolocation, map_calculus=map_value)
                # TODO Czemu zwraca null ?? Return self?
                if analysis_result._fast_id == 2:
                    analysis_result.set_predictions(pred)
                polygon.set_analysis_result(analysis_result)
            except Exception as e:
                self.workerException.emit(e)

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
