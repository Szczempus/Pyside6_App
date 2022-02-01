"""
Deepforest testing script
"""

from deepforest import main
from deepforest import get_data
from torch.cuda import empty_cache

import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from osgeo import gdal
from maps import rgb_image

bands_list = []
byte_band_list = []

model = main.deepforest()
model.use_release()

data = get_data(r"C:\Users\quadro5000\Desktop\BANDS.tif")
r = rasterio.open(data)
transform = r.transform
crs = r.crs
print(crs)
dataset = gdal.Open(data, gdal.GA_ReadOnly)
rasters = dataset.RasterCount
for i in range(0, rasters):
    bands_list.append(dataset.GetRasterBand(i + 1))
    byte_band_list.append(bands_list[i].ReadAsArray())

image = rgb_image(byte_band_list)

# img = model.predict_image(path=r"C:\Users\quadro5000\Desktop\sad_jablonie.tif", return_plot=True)
img = model.predict_tile(raster_path=r"C:\Users\quadro5000\PycharmProjects\groot-the-tree\AI\webgis-rgb.tif", return_plot= True, patch_size= 800, patch_overlap= 0.20)
plt.imshow(img[:, :, ::-1])
plt.show()
