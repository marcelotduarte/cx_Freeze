import os.path
import sys

from PIL import Image

print("Opening image with PIL")

if getattr(sys, "frozen", False):
    filename_png = os.path.join(os.path.dirname(sys.executable), "favicon.png")
else:
    filename_png = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "favicon.png"
    )
filename_pdf = os.path.join(os.path.dirname(filename_png), "test_pillow.pdf")
with Image.open(filename_png) as im, open(filename_pdf, "w+b") as fp:
    if im.mode == "RGBA":
        im = im.convert("RGB")
    im.save(fp, format="PDF")
print("OK")
