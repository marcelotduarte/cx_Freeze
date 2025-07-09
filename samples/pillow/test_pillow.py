import sys
from pathlib import Path

from PIL import Image


def find_data_file(filename: str) -> Path:
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = Path(sys.prefix, "share")
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = Path(__file__).resolve().parent
    return datadir / filename


print("Hello from cx_Freeze")
print("Opening image with PIL")

filename_png = find_data_file("icon.png")
filename_pdf = filename_png.parent / "test_pillow.pdf"
with Image.open(filename_png) as im, filename_pdf.open("w+b") as fp:
    if im.mode == "RGBA":
        im2 = im.convert("RGB")
        im2.save(fp, format="PDF")
    else:
        im.save(fp, format="PDF")
print("OK")
