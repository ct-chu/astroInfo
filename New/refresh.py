#mprof run ASC_mpl.py
#mprof plot

import time

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, ContentTooShortError
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
from matplotlib import collections as mc
import matplotlib.animation
import pandas
import numpy
import math
import ephem
from datetime import date, datetime, timedelta
import pathlib
from PIL import Image
import itertools
from sys import platform
import os
import gc
import feedparser
import re
import objgraph

######################
# initial parameters #
######################

count=0
T0 = time.time()

#####################################
# location information
#HKO
Trig_0 = ephem.Observer()
Trig_0.lon = str(114+10/60+27.6/3600)
Trig_0.lat = str(22+18/60+7.3/3600)
#Hokoon
hokoon = ephem.Observer()
hokoon.lon = str(114+6/60+29/3600)
hokoon.lat = str(22+23/60+1/3600)

Obs = hokoon #<= set your observatory
#####################################
# plot parameters
image_size = 1.6
side_space = 6
fig = plt.figure(figsize=(image_size*7.2*(1+1/side_space),image_size*4.8+1.2), facecolor='red')
fig.subplots_adjust(0,0,1,1,0,0)

gs = matplotlib.gridspec.GridSpec(6, 2, wspace=0, hspace=0, width_ratios=[1, side_space], height_ratios=[90,50,50,60,90,50])

ax0 = plt.subplot(gs[:5, 1])
ax0.set_facecolor('black')
ax0.set_aspect('equal', anchor='N')

ax1 = plt.subplot(gs[0, 0])
ax1.set_facecolor('red')
ax1.set_aspect('equal', anchor='NE')

ax2 = plt.subplot(gs[1, 0])
ax2.set_facecolor('green')
ax2.set_aspect('equal', anchor='NE')

ax3 = plt.subplot(gs[2, 0])
ax3.set_facecolor('blue')
ax3.set_aspect('equal', anchor='NE')

ax4 = plt.subplot(gs[3, 0])
ax4.set_facecolor('cyan')
ax4.set_aspect('equal', anchor='NE')

ax5 = plt.subplot(gs[4:, 0])
ax5.set_facecolor('yellow')
ax5.set_aspect('equal', anchor='SE')

ax6 = plt.subplot(gs[5, 1])
ax6.set_facecolor('black')
#ax6.set_aspect('equal', anchor='NW')

matplotlib.rcParams['savefig.facecolor'] = (0,0,0)


while True:
    ##############
    # time
    #Obs.date = datetime.utcnow().replace(second=0,microsecond=0)
    Obs.date = datetime.utcnow().replace(microsecond=0)
    ##############

    #clear the image because we didn't close it
    plt.clf()

    #show the image
#    plt.figure(figsize=(5, 5))
    plt.annotate('sky at HKT '+str(ephem.localtime(Obs.date).strftime('%d/%m/%Y %H:%M:%S')),(0.5,0.5),ha='right',color='c')
    print("Pausing...")
    plt.pause(2)
