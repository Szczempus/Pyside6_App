import matplotlib.pyplot as plt
import cv2 as cv
import numpy
import numpy as np

from PIL import Image

def run(image):

    image = numpy.asarray(image)

    plt.imshow(image)
    plt.show()

    x = [3580, 3200, 3100, 3780, 3880]
    y = [3668, 3450, 3950, 3680, 3621]

    poly = [(x, y) for x, y in zip(x, y)]

    polygon_pts = np.array(poly)

    copy_polygon_pts = polygon_pts
    # Cropping the bounding rect

    rect = cv.boundingRect(copy_polygon_pts)

    x_crop, y_crop, w, h = rect
    croped = image[y_crop:y_crop + h, x_crop:x_crop + w]

    croped = Image.fromarray(croped)
    croped = croped.convert("RGBA")
    croped = np.asarray(croped)

    plt.imshow(croped)
    plt.show()

    new_polygons = [(y - y_crop, x - x_crop) for x, y in zip(x, y)]

    new_polygons_pts = np.array(new_polygons)

    # Make mask
    new_polygons_pts = new_polygons_pts - new_polygons_pts.min(axis=0)

    copy_polygon_pts = copy_polygon_pts - copy_polygon_pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], dtype=numpy.uint8)
    cv.drawContours(mask, [copy_polygon_pts], -1, (255, 255, 255), -1, cv.LINE_AA)

    # Bit-op
    dst = cv.bitwise_and(croped, croped, mask=mask)

    # bg = np.ones_like(croped, np.uint8) * 255
    # cv.bitwise_not(bg, bg, mask=mask)
    #
    # dst = bg + dst

    plt.imshow(dst)
    plt.show()

    pil_image = Image.fromarray(dst)
    pil_image = pil_image.convert("RGBA")

    # alpha = np.sum(dst, axis=-1)>0
    # alpha = np.uint8(alpha*255)
    # dst = np.dstack((dst, alpha))
    # dst_alpa = np.concatenate([dst, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # white = np.all(dst_alpa == [255, 255, 255], axis=-1)
    # dst_alpa[white, -1] = 0
    # dst = dst_alpa

    plt.imshow(pil_image)
    plt.show()

    next = Image.open(r"C:\Users\quadro5000\Pictures\Prepar3D v5 Files\2021-7-9_21-43-41-599.jpg").convert("RGBA")

    next.paste(pil_image, (10, 10), pil_image)

    next = np.asarray(next)

    plt.imshow(next)
    plt.show()


if __name__ == "__main__":
    image = cv.imread(r"C:\Users\quadro5000\Pictures\rgb.tif")
    # image = Image.open(r"C:\Users\quadro5000\Pictures\rgb.tif").convert("RGBA")
    run(image)
