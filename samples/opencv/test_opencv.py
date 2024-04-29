"""A simple script to demonstrate opencv-python."""

import os
import sys

sys.OpenCV_LOADER_DEBUG = True
import cv2 as cv  # noqa: E402


def find_data_file(filename) -> str:
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "share")
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


img = cv.imread(find_data_file("image.png"))
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(15000)
if k == ord("s"):
    cv.imwrite("image1.png", img)
