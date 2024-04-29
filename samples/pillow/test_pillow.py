import os.path
import sys

from PIL import Image


def find_data_file(filename) -> str:
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.join(os.path.dirname(sys.executable), "share")
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


print("Opening image with PIL")

filename_png = find_data_file("favicon.png")
filename_pdf = os.path.join(os.path.dirname(filename_png), "test_pillow.pdf")
with Image.open(filename_png) as im, open(filename_pdf, "w+b") as fp:
    if im.mode == "RGBA":
        im2 = im.convert("RGB")
        im2.save(fp, format="PDF")
    else:
        im.save(fp, format="PDF")
print("OK")
