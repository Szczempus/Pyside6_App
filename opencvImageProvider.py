# This Python file uses the following encoding: utf-8
import cv2
import matplotlib.pyplot
from PySide2.QtCore import QSize, QByteArray, Slot, QObject
from PySide2.QtGui import QImage, QImageReader
from PySide2.QtQuick import QQuickImageProvider
import cv2 as cv
import numpy as np
from osgeo import gdal
from tifffile import TiffFile

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

debug = False


def convert_from_cv_to_qimage(image: np.ndarray) -> QImage:
    is_succes, img_to_bytes = cv.imencode(".png", image)
    img_byte_array = img_to_bytes.tobytes()
    bytearr = QByteArray(img_byte_array)
    qimage = QImage()
    qimage.loadFromData(bytearr, "PNG")
    return qimage


class OpencvImageProvider(QQuickImageProvider, QObject):
    def __init__(self):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image,
                                                  QQuickImageProvider.ForceAsynchronousImageLoading)
        self._image_file_path = None
        self._image = None
        self._band_list = []
        self._byte_band_list = []
        self.colored_polygon = None
        self.polygon_params = None
        # print("Inicjalizacja OpencvImageProvider")

    def get_byte_band_list(self):
        return self._byte_band_list


    def requestImage(self, path: str, size: QSize, req_size: QSize) -> QImage:
        img = self._image

        # Reload image and clear everything
        if path == "reload":
            # print("Image reloading")
            qimage = convert_from_cv_to_qimage(self._image)
            return qimage

        _, parsed_path = path.split("///", 1)
        if img is None or parsed_path != self._image_file_path:

            self._byte_band_list.clear()
            self._band_list.clear()

            # Get file path
            self._image_file_path = parsed_path

            # reader = QImageReader(self._image_file_path)
            # return reader.read()

            # If it's tiff img
            if self._image_file_path.endswith(('.tiff', '.tif')):

                # Read dataset
                dataset = gdal.Open(self._image_file_path, gdal.GA_ReadOnly)

                # Check if dataset is valid
                if dataset is None:
                    raise TypeError("Image is None type. Check image source file")

                # Get rasters count
                rasters = dataset.RasterCount
                if debug:
                    print(rasters)

                # Calculate min and max value of rasters (raster num, val)
                mini = (0, 65535)
                maxi = (0, 0)

                # Loop over every band
                for i in range(1, rasters + 1):
                    band = dataset.GetRasterBand(i)
                    minimum = band.GetMinimum()
                    maximum = band.GetMaximum()
                    if not minimum or not maximum:
                        (minimum, maximum) = band.ComputeRasterMinMax(True)
                    if maximum > maxi[1]:
                        maxi = (i, maximum)
                    if minimum < mini[1]:
                        mini = (i, minimum)

                    # Append it to the list
                    self._band_list.append(band)
                    self._byte_band_list.append(band.ReadAsArray())

                # For debug purposes
                if debug:
                    print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
                                                 dataset.GetDriver().LongName))
                    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                                        dataset.RasterYSize,
                                                        dataset.RasterCount))
                    print("Projection is {}".format(dataset.GetProjection()))
                    geotransform = dataset.GetGeoTransform()
                    if geotransform:
                        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
                        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

                    band = dataset.GetRasterBand(1)
                    print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))

                    print("Min={:.3f}, Max={:.3f}".format(mini[1], maxi[1]))

                    if band.GetOverviewCount() > 0:
                        print("Band has {} overviews".format(band.GetOverviewCount()))

                    if band.GetRasterColorTable():
                        print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))

                    # Printing GEOTags
                    for page in TiffFile(self._image_file_path).pages:
                        for tag in page.tags.values():
                            print(tag.name, tag.code, tag.dtype, tag.count, tag.value)

                # Convert to rgb image
                rgb = rgb_image(self._byte_band_list)

                # Implementing color corection
                # Todo zrobić jakiś suwak żeby zmieniać wartość korekcji koloru
                # if rasters > 4:
                rgb = simplest_cb(rgb, 1)
                # alpha = np.array(np.ones(self._byte_band_list[1].shape) * 255)
                # rgba = np.dstack((rgb, alpha))
                rgba = cv.cvtColor(rgb, cv.COLOR_BGR2BGRA)
                self._image = rgba
                qimage = convert_from_cv_to_qimage(rgba)

                return qimage

            # Standard Reading
            else:

                img = cv.imread(self._image_file_path)
                # self._image = img
                qimage = convert_from_cv_to_qimage(image=img)

                return qimage


    def get_image(self):
        return self._image

    def write_image(self, image):
        self._image = image
