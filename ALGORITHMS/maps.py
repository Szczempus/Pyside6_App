import numpy as np
from numpy import inf
import cv2 as cv

'''
Band_list must be in Agisoft order standard and must represent numpy byte arrays.
Agisoft exports channels with this order: 
channel 1 - Blue
channel 2 - Green
channel 3 - Red 
channel 4 - Red edge
channel 5 - NIR
'''


def index_calculation(index_threshold: float, index_map, normalize=False) -> float:
    # Todo dockstring
    if normalize:
        index_map[index_map < 0] = 0
    index_sum = np.sum(index_map)
    print(f"WARTOŚC SUMY INDEKSU: {index_sum}")
    above_thresh_sum = np.sum(index_map >= index_threshold)
    print(f"WARTOŚC SUMY POWYŻEJ 0.4: {above_thresh_sum}")
    map_value = above_thresh_sum / index_sum
    print(f"WARTOŚ WSKAŹNIKA:{map_value}")

    return map_value


def rgb_image(band_list, max_val: list = None, min_val: list = None):
    r = band_list[2]
    g = band_list[1]
    b = band_list[0]

    if max_val and min_val is not None:
        print("Typy danych: ", type(max_val[1]))
        print("Zawarte dane: ", max_val)

        r = (r < int(max_val[2])) * r
        g = (g < int(max_val[1])) * g
        b = (b < int(max_val[0])) * b

        r = (r > int(min_val[2])) * r
        g = (g > int(min_val[1])) * g
        b = (b > int(min_val[0])) * b

    r = np.array(r / 256).astype("uint8")
    g = np.array(g / 256).astype("uint8")
    b = np.array(b / 256).astype("uint8")

    img = np.dstack((b, g, r))  # Stack band for RGB image

    return img


'''
Blue Normalized Difference Vegetation Index
'''


def bndvi_map(band_list):
    # Getting bands
    nir = band_list[4]
    vis = band_list[0]

    # Calculations
    image = (nir - vis) / (nir + vis)  # NDVI

    # Preventing from inf and -inf values
    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Green Normalized Difference Vegetation Index
'''


def gndvi_map(band_list):
    # Getting bands
    nir = band_list[4]
    vis = band_list[1]

    # Calculations
    image = (nir - vis) / (nir + vis)  # NDVI

    # Preventing from inf and -inf values
    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Normalized Difference Vegetation Index
'''


def ndvi_map(band_list):
    # Getting bands
    nir = band_list[4]
    vis = band_list[2]

    # Calculations
    image = (nir - vis) / (nir + vis)  # NDVI

    # Preventing from inf and -inf values
    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Leaf Chlorophyll Index
'''


def lci_map(band_list):
    nir = band_list[4]
    rededge = band_list[3]
    red = band_list[2]

    # Calculations
    image = (nir - rededge) / (nir + red)  # LCI

    # Preventing from inf and -inf values
    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Modified Chlorophyll Absorption in Reflective Index
'''


def mcar_map(band_list):
    nir = band_list[4]
    red = band_list[2]
    green = band_list[1]

    image = (1.2 * (2.5 * (nir - red) - 1.3 * (nir - green))) / ((nir + red))

    return image


'''
Normalized Difference Red Edge
'''


def ndre_map(band_list):
    nir = band_list[4]
    rededge = band_list[3]

    image = (nir - rededge) / (nir + rededge)

    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Structure Intensive Pigment Index 2
'''


def sipi2_map(band_list):
    nir = band_list[4]
    green = band_list[1]
    red = band_list[2]

    image = (nir - green) / (nir - red)

    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Triangular Greenness Index
'''


def tgi_map(band_list):
    return


'''
Optimized Soil-Adjusted Vegetation Index
'''


def osavi_map(band_list):
    nir = band_list[4]
    red = band_list[2]

    image = (nir - red) / (nir + red + 0.16)

    return image


'''
Visible Atmospherically Resistant Index
'''


def vari_map(band_list):
    green = band_list[1]
    red = band_list[2]
    blue = band_list[0]

    image = (green - red) / (green + red - blue)

    image[image == inf] = 1
    image[image == -inf] = -1

    return image


'''
Mistletoe index
'''


def mis_map(band_list):
    green = band_list[1]
    red = band_list[2]
    blue = band_list[0]

    image = np.divide(red - blue + green, red + blue, out=np.zeros_like(red, dtype=float), where=(red + blue) != 0)

    image[image > 3] = 0
    image[image < 0] = 0
    return image


'''
Filtration for mistletoe index
'''


def mis_filtration(mis, ndvi, mis_thresh=[1.5, 2.5], ndvi_thresh=[0.75, 0.85]):
    statement_1 = np.logical_and(mis >= mis_thresh[0], mis <= mis_thresh[1])
    print("statement_1 passed")
    statement_2 = np.logical_and(ndvi >= ndvi_thresh[0], ndvi <= ndvi_thresh[1])
    print("statement_2 passed")
    image = np.bitwise_and(statement_1, statement_2)
    print("image passed")
    return image
