from __future__ import print_function

import numpy as np
import cv2 as cv

# built-in modules
import os
import sys
import glob
import argparse
from math import *

boxes = []
drag_start = None
sel = (0, 0, 0, 0)
img = None

def opencv_pain_loop(image):
    global img
    img = image
    cv.namedWindow("gray", 1)
    cv.setMouseCallback("gray", onmouse)
    sel = (0, 0, 0, 0)
    drag_start = None
    cv.imshow("gray", img)
    if cv.waitKey() == 27:
        cv.destroyAllWindows()


def onmouse(event, x, y, flags, param):
    global drag_start, sel, img
    if event == cv.EVENT_LBUTTONDOWN:
        drag_start = x, y
        sel = 0, 0, 0, 0
    elif event == cv.EVENT_LBUTTONUP:
        if sel[2] > sel[0] and sel[3] > sel[1]:
            patch = img[sel[1]:sel[3], sel[0]:sel[2]]
            result = cv.matchTemplate(img, patch, cv.TM_CCOEFF_NORMED)
            result = np.abs(result) ** 3
            _val, result = cv.threshold(result, 0.01, 0, cv.THRESH_TOZERO)
            result8 = cv.normalize(result, None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
            cv.imshow("gray", result8)
        drag_start = None
    elif drag_start:
        # print flags
        if flags & cv.EVENT_FLAG_LBUTTON:
            minpos = min(drag_start[0], x), min(drag_start[1], y)
            maxpos = max(drag_start[0], x), max(drag_start[1], y)
            sel = minpos[0], minpos[1], maxpos[0], maxpos[1]
            # img_copy = img
            cv.rectangle(img, (sel[0], sel[1]), (sel[2], sel[3]), (0, 255, 255), 1)
            cv.imshow("gray", img)
        else:
            print("selection is complete")
            drag_start = None
