from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError
import matplotlib.pyplot as plt
import numpy
import math
from datetime import date, datetime
from matplotlib.figure import Figure
import pathlib
from PIL import Image
import cv2

##try:
##    urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
##    asc = Image.open('asc.jpg')
##except HTTPError:
##    urlretrieve('https://www.hko.gov.hk/gts/astronomy/image/asc_hokoon0.jpg?1541472934785', 'asc.jpg')
##    asc = Image.open('asc.jpg')
##except:
##    asc = Image.open(pathlib.Path.cwd().joinpath('ASC','serverdead.jpg'))

asc = Image.open(pathlib.Path.cwd().joinpath('ASIM','hkneac_asc (5).jpg'))

# cloud coverage
mask_source = Image.open(pathlib.Path.cwd().joinpath('ASC','mask_source.jpg'))
mask_source_rgb = mask_source.convert('RGB')

# mask
hokoon = numpy.arange(480*720).reshape(480,720) # (row,col)
hokoon_mask = numpy.ma.make_mask(hokoon,copy=True,shrink=True,dtype=numpy.bool)

for row in range(480):
    hokoon_mask_row = []
    for col in range(720):
        r, g, b = mask_source_rgb.getpixel((col, row)) # (x,y)
        if r+g+b > 200:
            hokoon_mask_row.append(False)
        else:
            hokoon_mask_row.append(True)

    hokoon_mask[row] = hokoon_mask_row

hokoon_mask[0:34+1,:] = True # mask rim, last item is not included
hokoon_mask[453:480+1,:] = True
hokoon_mask[:,0:120+1] = True
hokoon_mask[:,569:720+1] = True

hokoon_mask[257:395+1,236:405+1] = False # unmask dark cloud

# sun mask
asc_rgb = asc.convert('RGB')
sun_raw = numpy.arange(480*720).reshape(480,720) # (row,col)
sun_mask = numpy.ma.make_mask(sun_raw,copy=False,shrink=False,dtype=numpy.bool)        

for row in range(480):
    sun_mask_row = []
    for col in range(720):
        r, g, b = asc_rgb.getpixel((col, row)) # (x,y)
        if r+g+b > 700:
            sun_mask_row.append(True)
        else:
            sun_mask_row.append(False)

    sun_mask[row] = sun_mask_row
            
# save mask
#cv2.imwrite('hokoon_mask.png', hokoon_mask.astype('uint8') * 255)

# mask for inspection
real_mask = hokoon_mask + sun_mask
real_mask_check = real_mask.astype(numpy.float)
real_mask_check[numpy.where(real_mask_check==0)]=numpy.nan
hokoon_mask_check = hokoon_mask.astype(numpy.float)
hokoon_mask_check[numpy.where(hokoon_mask_check==0)]=numpy.nan
sun_mask_check = sun_mask.astype(numpy.float)
sun_mask_check[numpy.where(sun_mask_check==0)]=numpy.nan
plt.imshow(asc)
plt.imshow(real_mask_check)

plt.show()
