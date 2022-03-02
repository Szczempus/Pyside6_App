"""
Deepforest testing script
"""

from deepforest import main
from deepforest import get_data
from torch.cuda import empty_cache

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from maps import rgb_image
from PIL import Image

def fun(path):
    # bands_list = []
    # byte_band_list = []

    model = main.deepforest()
    model.use_amp = True
    model.use_release()

    # data = get_data(r"C:\Users\quadro5000\Desktop\BANDS.tif")
    # r = rasterio.open(data)
    # transform = r.transform
    # crs = r.crs
    # print(crs)
    # dataset = gdal.Open(data, gdal.GA_ReadOnly)
    # rasters = dataset.RasterCount
    # for i in range(0, rasters):
    #     bands_list.append(dataset.GetRasterBand(i + 1))
    #     byte_band_list.append(bands_list[i].ReadAsArray())

    # image = rgb_image(byte_band_list)

    img = model.predict_image(path=r"C:\Users\quadro5000\Desktop\sad_jablonie.tif", return_plot=True)

    image = cv2.imread(path)
    img = model.predict_tile(image=image,
                             return_plot=True, patch_size=800, patch_overlap=0.20)
    plt.imshow(img[:, :, ::-1])
    plt.show()

    cv2.rectangle()

if __name__ == "__main__":

    cwd = r"C:\anaconda3\envs\groot2.0\Lib\site-packages\deepforest\data"
    img = r"\SOAP_061.png"

    path = cwd + img

    fun(path)
