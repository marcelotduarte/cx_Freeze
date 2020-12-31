import os.path

from PIL import Image

print("Opening image with PIL")
filename = os.path.join("..", "icon", "favicon.png")
with Image.open(filename) as im, open("test_pillow.pdf", "w+b") as fp:
    if im.mode == "RGBA":
        im = im.convert("RGB")
    im.save(fp, format="PDF")
print("OK")
