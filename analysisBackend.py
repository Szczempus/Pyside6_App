import matplotlib.cm
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
        byte_band_list = []
        poligon_list = []
        checked_polygon_list = []

        original_image = self._img_manager.get_image()

        byte_band_list = self._img_manager.get_byte_band_list()
        poligon_list = self._polygon_manager.get_polygon_list()
        checked_polygon_list = [polygon for polygon in poligon_list if polygon.get_is_checked()]

        for polygon in checked_polygon_list:
            coords = []
            for point in polygon.get_point_list():
                point = (point.x_get(), point.y_get())
                coords.append({"x": point[0], "y": point[1]})

            cropped_rect, params = crop_band_list(byte_band_list, coords)

            if self._analysis == 1:
                print("Analysis 1 - NDVI")
                index_image = ndvi_map(cropped_rect)
                my_cmap = matplotlib.cm.get_cmap("Spectral")
                color_array = my_cmap(index_image)
                image = np.asarray(color_array)
                image = image * 255

            elif self._analysis == 2:
                print("Analysis 2 - LCI")
                index_image = lci_map(cropped_rect)
                my_cmap = matplotlib.cm.get_cmap("plasma")
                color_array = my_cmap(index_image)
                image = np.asarray(color_array)
                image = image * 255

            elif self._analysis == 3:
                print("Analysis 3 - Segmentation")
                try:
                    index_image = osavi_map(byte_band_list)
                    my_cmap = matplotlib.cm.get_cmap("Spectral")
                    color_array = my_cmap(index_image)
                    image = np.asarray(color_array)
                    image = image * 255
                    print("Wielkośc obrazu", image.shape)
                except Exception as e:
                    print("Index map error")
                    self.workerException.emit(e)

                try:
                    rgb, _ = crop_rgb(image[:, :, :3], coords)
                    print("Wielkość rgb ", rgb.shape)
                except Exception as e:
                    print("Kurwa to tu")
                    self.workerException.emit(e)
                try:
                    cfg = config_init("", 4000, 8, 1)
                    image = prediction(cfg, rgb[:, :, ::-1],
                                       model_path="C:/Users/quadro5000/PycharmProjects/detectron2_training/detectron2/output/model_final.pth")
                except Exception as e:
                    print("Kurwa to jednak tu")
                    self.workerException.emit(e)

            elif self._analysis == 4:
                print("Analysis 4 - Counting")
                rgb, _ = crop_rgb(original_image[:, :, :3], coords)
                model = main.deepforest()
                model.use_amp = True
                model.use_release()
                try:
                    img = model.predict_tile(image=rgb, return_plot=True, patch_size=800, patch_overlap=0.1,
                                             iou_threshold=0.4, thresh=0.8)
                    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
                    image = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
                except Exception as e:
                    self.workerException.emit(e)

            if self._analysis == 5:
                print("Analysis 5 - Mistolete")
                mis_image = mis_map(cropped_rect)
                ndvi_image = ndvi_map(cropped_rect)
                mis_filtered = mis_filtration(mis_image, ndvi_image)
                int_mis = mis_filtered.astype(int) * 255
                image, _ = crop_rgb(original_image[:, :, :3], coords)

                for i in range(image.shape[0]):
                    for j in range(image.shape[1]):
                        if int_mis[i, j] == 255:
                            image[i, j] = (0, 255, 255)

            polygon, _, _ = poly_img(image, coords, params[0], params[1],
                                     original_image[params[1]: params[1] + params[3],
                                     params[0]:params[0] + params[2]])
            original_image[params[1]: params[1] + params[3], params[0]:params[0] + params[2]] = polygon

            self._img_manager.write_image(original_image)

            print("Koniec procesu")
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
        self.isProcessing.emit(False)
        self._thread.quit()
        self._thread.deleteLater()

    def print_restult(self, image):
        pass
