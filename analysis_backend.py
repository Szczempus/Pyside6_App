[from PySide2.QtCore import Slot, Signal, QObject, QThread
from matplotlib import pyplot as plt
from deepforest import main
import sys, time

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


# Todo: make a worker and controller class

class ThreadClass(QThread):
    signal = Signal(int)

    def __init__(self):
        super(ThreadClass, self).__init__()
        self._is_running = False

    def run(self):
        print("Strarting thread...")
        self._is_running = False



        # cnt = 0
        # while True:
        #     cnt += 1
        #     if cnt == 99:
        #         cnt = 0
        #         time.sleep(0.01)
        #         self.signal.emit(cnt)

    def stop(self):
        self._is_running = False
        print("Stopping thread...")
        self.terminate()


class Processing(QObject):
    isProcessing = Signal(bool, arguments=['val'])

    def __init__(self, polygon_manager: PolygonMenager, opencv: OpencvImageProvider):
        super(Processing, self).__init__()
        self._selected_analysis = None
        self._polygon_manager = polygon_manager
        self._image_provider = opencv
        self._working_thread = ThreadClass()
        self._working_thread.signal.connect(self.print_cnt)

        self.stop_timer = 0

    @Slot(int)
    def start_analysis(self, analysis):
        print("Zaczłąem analizę")
        self._working_thread.run()
        self.isProcessing.emit(True)

    # def print_cnt(self, cnt):
    #     print("Counter", cnt)
    #     self.stop_timer += 1
    #
    #     if self.stop_timer >= 20:
    #         self._working_thread.stop()





