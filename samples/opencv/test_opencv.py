"""A simple script to demonstrate opencv-python."""

import os
import sys

sys.OpenCV_LOADER_DEBUG = True
import cv2  # noqa: E402


def find_data_file(filename) -> str:
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "share")
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


img_file = find_data_file("image.png")
img_file1 = find_data_file("image1.png")
img = cv2.imread(img_file)
if img is None:
    sys.exit("Could not read the image.")
cv2.imwrite(img_file1, img)
print("OpenCV generated a new png:", img_file1)
try:
    cv2.imshow("Display window from cx_Freeze", img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
except cv2.error:
    print("OpenCV headless mode does not implement 'imshow' function")
