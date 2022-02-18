import numpy
import numpy as np
import cv2 as cv
import sys
from PIL import Image



def crop_band_list(band_list: list, coords: list):
    """
    This function crops the original sized bands to maximum sized rectangle
    to overfill polygon. With that to analyzis comes only selected area, not
    entire image.

    :param band_list:
    :param coords:
    :return:
    """

    cropped_band_list = []

    pts = [[int(coord["x"]), int(coord["y"])] for coord in coords]

    polygon_pts = np.array(pts)

    for band in band_list:
        copy_polygon_pts = polygon_pts
        # Cropping the bounding rect

        rect = cv.boundingRect(copy_polygon_pts)

        x, y, w, h = rect
        croped = band[y:y + h, x:x + w].copy()
        cropped_band_list.append(croped)

    return cropped_band_list, [x, y, w, h]

    # //// UNUSED

    # Make mask
    # copy_polygon_pts = copy_polygon_pts - copy_polygon_pts.min(axis=0)
    #
    # mask = np.zeros(croped.shape[:2], dtype=numpy.uint8)
    # cv.drawContours(mask, [copy_polygon_pts], -1, (255, 255, 255), -1, cv.LINE_AA)

    # plt.imshow(mask)
    # plt.title("Mask")
    # plt.show()

    # Bit-op
    # dst = cv.bitwise_and(croped, croped, mask=mask)
    #
    # bg = np.ones_like(croped, np.uint8) * 65535
    # cv.bitwise_not(bg, bg, mask=mask)
    # dst2 = bg + dst
    #
    # poly_band_list.append(dst2)


def crop_rgb(rgb, coords: list, x_new = None, y_new = None):
    """
    This function crops the original sized bands to maximum sized rectangle
    to overfill polygon. With that to analyzis comes only selected area, not
    entire image.

    :param rgb:
    :param coords:
    :return:
    """

    band = rgb
    print("1 badn", band.shape)
    if x_new or y_new is None:
        pts = [[int(coord["x"]), int(coord["y"])] for coord in coords]
    else:
        pts = [[int(coord["x"]) - x_new, int(coord["y"]) - y_new] for coord in coords]
    polygon_pts = np.array(pts)

    copy_polygon_pts = polygon_pts
    # Cropping the bounding rect

    rect = cv.boundingRect(copy_polygon_pts)

    x, y, w, h = rect
    cropped = band[y:y + h, x:x + w].copy()
    print("2 Cropped ", cropped.shape)

    return cropped, [x, y, w, h]


def poly_img(fgimage: np.ndarray, coords: list, x_new, y_new, bgimage: np.ndarray):
    """
    This function crops and overlays forground polygonal image above background cropped
    fragemnet od orygnal image

    :param fgimage: RGB foreground image as numpy array
    :param coords: dictionary of coordinates {x: float, y: float}
    :param x_new: x position of analyzed window
    :param y_new: y position of analyzed window
    :param bgimage: RGB background image as numpy array
    :return: cropped image with alpha channel
    """

    band = fgimage

    pts = [[int(coord["x"]) - x_new, int(coord["y"]) - y_new] for coord in coords]

    print("1")

    polygon_pts = np.array(pts)
    # Cropping the bounding rect

    rect = cv.boundingRect(polygon_pts)

    x, y, w, h = rect
    croped = band[y:y + h, x:x + w]
    _,_,channels = croped.shape

    print("2")
    print(type(croped))
    print(croped.shape)

    croped = Image.fromarray(croped.astype(np.uint8))


    print("2.1")

    if channels < 4:
        croped = croped.convert("RGBA")

    print("2.2")

    croped = np.asarray(croped)

    print("3")

    # Make mask
    copy_polygon_pts = polygon_pts - polygon_pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], dtype=numpy.uint8)
    cv.drawContours(mask, [copy_polygon_pts], -1, (255, 255, 255), -1, cv.LINE_AA)

    # Bit-op
    dst = cv.bitwise_and(croped, croped, mask=mask)

    print("4")

    fg_image = Image.fromarray(dst)
    fg_image = fg_image.convert("RGBA")

    print("5")

    bgimage = Image.fromarray(bgimage)
    bgimage = bgimage.convert("RGBA")

    print("6")

    bgimage.paste(fg_image, (0, 0), fg_image)

    print("7")

    bgimage = np.array(bgimage)

    print("8")

    print("Dst shape", dst.shape)

    return bgimage, [x, y, w, h], mask
