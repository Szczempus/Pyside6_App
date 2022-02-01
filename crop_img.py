import numpy
from osgeo import gdal
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv


def crop_img(band_list, coords):
    pts = []
    poly_band_list = []
    cropped_band_list = []

    for coord in coords:
        pts.append([int(coord["x"]), int(coord["y"])])

    polygon_pts = np.array(pts)

    for band in band_list:
        copy_polygon_pts = polygon_pts
        # Cropping the bounding rect
        rect = cv.boundingRect(copy_polygon_pts)
        x, y, w, h = rect
        croped = band[y:y + h, x:x + w].copy()
        cropped_band_list.append(croped)

        # plt.imshow(croped)
        # plt.title("Cropped")
        # plt.show()

        # Make mask
        copy_polygon_pts = copy_polygon_pts - copy_polygon_pts.min(axis=0)

        mask = np.zeros(croped.shape[:2], dtype=numpy.uint8)
        cv.drawContours(mask, [copy_polygon_pts], -1, (255, 255, 255), -1, cv.LINE_AA)

        # plt.imshow(mask)
        # plt.title("Mask")
        # plt.show()

        # Bit-op
        dst = cv.bitwise_and(croped, croped, mask=mask)

        # plt.imshow(dst)
        # plt.title("Black bg")

        bg = np.ones_like(croped, np.uint8) * 65535
        cv.bitwise_not(bg, bg, mask=mask)
        dst2 = bg + dst

        # plt.imshow(dst2)
        # plt.title("White bg")
        # plt.show()

        poly_band_list.append(dst2)

    return poly_band_list, cropped_band_list, [x, y, w, h]
