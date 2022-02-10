import numpy
import numpy as np
import cv2 as cv
import sys


def crop_img(band_list: list, coords: list):
    poly_band_list = []
    cropped_band_list = []

    pts = [[int(coord["x"]), int(coord["y"])] for coord in coords]

    polygon_pts = np.array(pts)

    # print("6.1")
    # print(band_list)
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
    # print("6.9")
    # print("polyband list", poly_band_list)
    # print("cropped_band", cropped_band_list)
    # print("coords", [x, y, w, h])
    return poly_band_list, cropped_band_list, [x, y, w, h]

def poly_img(image: np.ndarray, coords: list, x_new, y_new):

    band = image

    pts = [[int(coord["x"]) - x_new, int(coord["y"]) - y_new] for coord in coords]

    polygon_pts = np.array(pts)

    # print("6.1")
    # print(band_list)
    copy_polygon_pts = polygon_pts
    # Cropping the bounding rect

    rect = cv.boundingRect(copy_polygon_pts)

    print(copy_polygon_pts)
    print(band.shape)
    print(rect)

    x, y, w, h = rect
    croped = band[y:y + h, x:x + w]


    print(croped.shape)

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
    dst = cv.cvtColor(dst, cv.COLOR_BGR2BGRA)

    print("Dst shape", dst.shape)

    # plt.imshow(dst)
    # plt.title("Black bg")

    # bg = np.ones_like(croped, np.uint8) * 65535
    # cv.bitwise_not(bg, bg, mask=mask)
    # dst2 = bg + dst

    # plt.imshow(dst2)
    # plt.title("White bg")
    # plt.show()

    # dst2 = cv.cvtColor(dst2, cv.COLOR_BGR2BGRA)

    # print("6.9")
    # print("polyband list", poly_band_list)
    # print("cropped_band", cropped_band_list)
    # print("coords", [x, y, w, h])
    return  dst, [x, y, w, h], croped