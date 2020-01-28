from io import BytesIO
from urllib.request import urlopen
from PIL import Image

print('Opening image with PIL')
filename = 'https://avatars3.githubusercontent.com/u/12752334?s=400&u=3ba7ed4b03221b76af248ff57b5f619d77b6021f&v=4'
fp = BytesIO(urlopen(filename).read())
with Image.open(fp) as im, open('test_pillow.pdf', 'w+b') as fp2:
	im.save(fp2, format='PDF')
print('OK')
