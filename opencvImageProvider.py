"""
IMPORTANT INFO
GDAL paginate rasters number from 1 to n, NOT FROM 0 !
Agisoft exports channels with this order:
channel 1 - Blue
channel 2 - Green
channel 3 - Red
channel 5 - NIR
channel 6 - LWIR(thermal) wymagane jest jeszcze przekształcenie danych z kelwinów na st. celcujsza
"""

# This Python file uses the following encoding: utf-8
import platform
import time

from PySide2.QtCore import QSize, QByteArray, QObject, Slot
from PySide2.QtGui import QImage
from PySide2.QtQuick import QQuickImageProvider
import cv2 as cv
import numpy as np

if platform.system() == 'Windows':
    from osgeo import gdal
else:
    import gdal

from tifffile import TiffFile

from ALGORITHMS import rgb_image, simplest_cb

Debug = True


def convert_from_cv_to_qimage(image: np.ndarray) -> QImage:
    """

    :param image:
    :return:
    """
    _, img_to_bytes = cv.imencode(".png", image)
    img_byte_array = img_to_bytes.tobytes()
    bytearr = QByteArray(img_byte_array)
    qimage = QImage()
    qimage.loadFromData(bytearr, "PNG")
    return qimage


class OpencvImageProvider(QQuickImageProvider, QObject):
    """
    QML Image Provider class
    """

    def __init__(self):
        super(OpencvImageProvider, self).__init__(QQuickImageProvider.Image,
                                                  QQuickImageProvider.ForceAsynchronousImageLoading)
        self._image_file_path = None
        self._image = None
        self._band_list = []
        self._byte_band_list = []
        self.colored_polygon = None
        self.polygon_params = None
        self._image_params = []
        self._dataset = None
        self._geolocation = None
        self._pixel_size = None
        self._dem_model = None

    def get_geolocation(self):
        return self._geolocation

    def get_pixel_size(self):
        return self._pixel_size

    def get_byte_band_list(self):
        return self._byte_band_list

    def get_image(self):
        return self._image

    def write_image(self, image):
        self._image = image

    def set_image_params(self, params: list):
        # In BGR order
        self._image_params = params

    def requestImage(self, path: str, size: QSize, req_size: QSize) -> QImage:
        start = time.time()
        img = self._image

        # Reload image and clear everything
        if path == "reload":
            # print("Image reloading")
            qimage = convert_from_cv_to_qimage(self._image)
            return qimage

        if path == "reload_with_params":
            rgb = rgb_image(self._byte_band_list,
                            min_val=self._image_params[0],
                            max_val=self._image_params[1])
            rgb = simplest_cb(rgb, int(self._image_params[2]))
            rgba = cv.cvtColor(rgb, cv.COLOR_BGR2BGRA)
            self._image = rgba
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

                if gdal.GetConfigOption("GDAL_NUM_THREADS") is None:
                    gdal.SetConfigOption('GDAL_NUM_THREADS', 'ALL_CPUS')
                    print("Wszystkie rdzenie na pełną moc")
                checkpoint_1 = time.time()

                # Read dataset
                self._dataset = gdal.Open(self._image_file_path, gdal.GA_ReadOnly)
                geotransform = self._dataset.GetGeoTransform()
                self._geolocation = (geotransform[0], geotransform[3])  # Xp[0], Yp[1]
                self._pixel_size = (geotransform[1], geotransform[5])  # W-E pix. res, N-S pix. res. (neg. for N)

                # TODO Pomyśleć nad optymalizacją
                checkpoint_2 = time.time()

                # Check if dataset is valid
                if self._dataset is None:
                    raise TypeError("Image is None type. Check image source file")
                    return None

                # Get rasters count
                rasters = self._dataset.RasterCount
                if Debug:
                    print(rasters)

                # Calculate min and max value of rasters (raster num, val)
                mini = (0, 65535)
                maxi = (0, 0)

                # Loop over every band
                for i in range(1, rasters + 1):
                    band = self._dataset.GetRasterBand(i)
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

                checkpoint_3 = time.time()

                # For debug purposes
                if Debug:
                    print("Driver: {}/{}".format(self._dataset.GetDriver().ShortName,
                                                 self._dataset.GetDriver().LongName))
                    print("Size is {} x {} x {}".format(self._dataset.RasterXSize,
                                                        self._dataset.RasterYSize,
                                                        self._dataset.RasterCount))
                    print("Projection is {}".format(self._dataset.GetProjection()))
                    if geotransform:
                        print("Origin = ({} E, {} N)".format(self._geolocation[0], self._geolocation[1]))
                        print("Pixel Size = ({}, {})".format(self._pixel_size[0], self._pixel_size[1]))

                    band = self._dataset.GetRasterBand(1)
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

                checkpoint_4 = time.time()

                # Implementing color corection
                rgb = simplest_cb(rgb, 1)

                checkpoint_5 = time.time()

                # alpha = np.array(np.ones(self._byte_band_list[1].shape) * 255)
                # rgba = np.dstack((rgb, alpha))
                rgba = cv.cvtColor(rgb, cv.COLOR_BGR2BGRA)

                checkpoint_6 = time.time()

                self._image = rgba
                qimage = convert_from_cv_to_qimage(rgba)

                checkpoint_7 = time.time()

                print("Czas działania: \n"
                      f"Ustawienie skryptu: {start - checkpoint_1} \n"
                      f"Wczytanie datasetu: {checkpoint_2 - checkpoint_1} \n"
                      f"Pobranie metadanych: {checkpoint_3 - checkpoint_2} \n"
                      f"Konwersja warstw na RGB: {checkpoint_4 - checkpoint_3} \n"
                      f"Kolorkorekcja: {checkpoint_5 - checkpoint_4} \n"
                      f"Konwersja na RGBA: {checkpoint_6 - checkpoint_5} \n"
                      f"Konwersja na QImage: {checkpoint_7 - checkpoint_6} \n "
                      f"Całość trwania skrypytu: {checkpoint_7 - start}")

            # Standard Reading
            else:

                img = cv.imread(self._image_file_path)
                # self._image = img
                qimage = convert_from_cv_to_qimage(image=img)

        return qimage

    @Slot(str)
    def read_dem(self, path: str):

        _, parsed_path = path.split("///", 1)




