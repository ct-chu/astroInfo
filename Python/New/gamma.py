import time
from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import collections as mc
import pylab as pl
import pandas
import numpy
import math
import ephem
from datetime import date, datetime
from matplotlib.figure import Figure
import pathlib
from PIL import Image
import itertools

gamma_0FGL      = numpy.zeros(shape=(205,7))
gamma_0FGL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','0FGL.csv'))
gamma_1FGL      = numpy.zeros(shape=(1451,9))
gamma_1FGL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','1FGL.csv'))
gamma_2FGL      = numpy.zeros(shape=(1873,10))
gamma_2FGL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','2FGL.csv'))
gamma_3FGL      = numpy.zeros(shape=(3034,10))
gamma_3FGL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','3FGL.csv'))
gamma_1FHL      = numpy.zeros(shape=(515,7))
gamma_1FHL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','1FHL.csv'))
gamma_2FHL      = numpy.zeros(shape=(360,7))
gamma_2FHL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','2FHL.csv'))
gamma_3FHL      = numpy.zeros(shape=(1556,10))
gamma_3FHL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','3FHL.csv'))
gamma_FL8Y      = numpy.zeros(shape=(5523,10))
gamma_FL8Y      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','FL8Y.csv'))
gamma_1SC       = numpy.zeros(shape=(102,8))
gamma_1SC       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','1SC.csv'))
gamma_2PC       = numpy.zeros(shape=(117,7))
gamma_2PC       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','2PC.csv'))
gamma_GRB1      = numpy.zeros(shape=(146,8))
gamma_GRB1      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','LAT_GRB1.csv'))
gamma_GRB2      = numpy.zeros(shape=(493,7))
gamma_GRB2      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','LAT_GRB2.csv'))
gamma_2FAV      = numpy.zeros(shape=(518,7))
gamma_2FAV      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','2FAV.csv'))
gamma_PSR       = numpy.zeros(shape=(234,7))
gamma_PSR       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','PSR.csv'))

plot_scale = 100

transform_l = lambda x,y: math.degrees(math.atan2(math.sin(math.radians(y))*math.cos(math.radians(27.12825))-math.cos(math.radians(y))*math.cos(math.radians(x-192.85948))*math.sin(math.radians(27.12825)),math.cos(math.radians(y))*math.sin(math.radians(x-192.85948)))+math.radians(122.93192))
transform_b = lambda x,y: math.degrees(math.asin(math.sin(math.radians(y))*math.sin(math.radians(27.12825))+math.cos(math.radians(y))*math.cos(math.radians(x-192.85948))*math.cos(math.radians(27.12825))))

gamma_0FGL.l = list(map(transform_l, gamma_0FGL.RA, gamma_0FGL.Dec))
gamma_0FGL.b = list(map(transform_b, gamma_0FGL.RA, gamma_0FGL.Dec))
gamma_1FGL.l = list(map(transform_l, gamma_1FGL.RA, gamma_1FGL.Dec))
gamma_1FGL.b = list(map(transform_b, gamma_1FGL.RA, gamma_1FGL.Dec))
gamma_2FGL.l = list(map(transform_l, gamma_2FGL.RA, gamma_2FGL.Dec))
gamma_2FGL.b = list(map(transform_b, gamma_2FGL.RA, gamma_2FGL.Dec))
gamma_3FGL.l = list(map(transform_l, gamma_3FGL.RA, gamma_3FGL.Dec))
gamma_3FGL.b = list(map(transform_b, gamma_3FGL.RA, gamma_3FGL.Dec))
gamma_1FHL.l = list(map(transform_l, gamma_1FHL.RA, gamma_1FHL.Dec))
gamma_1FHL.b = list(map(transform_b, gamma_1FHL.RA, gamma_1FHL.Dec))
gamma_2FHL.l = list(map(transform_l, gamma_2FHL.RA, gamma_2FHL.Dec))
gamma_2FHL.b = list(map(transform_b, gamma_2FHL.RA, gamma_2FHL.Dec))
gamma_3FHL.l = list(map(transform_l, gamma_3FHL.RA, gamma_3FHL.Dec))
gamma_3FHL.b = list(map(transform_b, gamma_3FHL.RA, gamma_3FHL.Dec))
gamma_FL8Y.l = list(map(transform_l, gamma_FL8Y.RA, gamma_FL8Y.Dec))
gamma_FL8Y.b = list(map(transform_b, gamma_FL8Y.RA, gamma_FL8Y.Dec))
gamma_GRB1.l = list(map(transform_l, gamma_GRB1.RA, gamma_GRB1.Dec))
gamma_GRB1.b = list(map(transform_b, gamma_GRB1.RA, gamma_GRB1.Dec))
gamma_GRB2.l = list(map(transform_l, gamma_GRB2.RA, gamma_GRB2.Dec))
gamma_GRB2.b = list(map(transform_b, gamma_GRB2.RA, gamma_GRB2.Dec))
gamma_2FAV.l = list(map(transform_l, gamma_2FAV.RA, gamma_2FAV.Dec))
gamma_2FAV.b = list(map(transform_b, gamma_2FAV.RA, gamma_2FAV.Dec))
gamma_PSR.l  = list(map(transform_l, gamma_PSR.RA, gamma_PSR.Dec))
gamma_PSR.b  = list(map(transform_b, gamma_PSR.RA, gamma_PSR.Dec))

l0 = 180
b0 = -90
    
transform_x = lambda x,y: plot_scale\
              *(-2/(1+math.sin(math.radians(b0))*math.sin(math.radians(y))+math.cos(math.radians(b0))*math.cos(math.radians(y))*math.cos(math.radians(x-l0))))\
              *math.cos(math.radians(y))*math.sin(math.radians(x-l0))
transform_y = lambda x,y: plot_scale\
              *(2/(1+math.sin(math.radians(b0))*math.sin(math.radians(y))+math.cos(math.radians(b0))*math.cos(math.radians(y))*math.cos(math.radians(x-l0))))\
              *(math.cos(math.radians(b0))*math.sin(math.radians(y))-math.sin(math.radians(b0))*math.cos(math.radians(y))*math.cos(math.radians(x-l0)))

gamma_0FGL.x = list(map(transform_x, gamma_0FGL.l, gamma_0FGL.b))
gamma_0FGL.y = list(map(transform_y, gamma_0FGL.l, gamma_0FGL.b))
gamma_1FGL.x = list(map(transform_x, gamma_1FGL.l, gamma_1FGL.b))
gamma_1FGL.y = list(map(transform_y, gamma_1FGL.l, gamma_1FGL.b))
gamma_2FGL.x = list(map(transform_x, gamma_2FGL.l, gamma_2FGL.b))
gamma_2FGL.y = list(map(transform_y, gamma_2FGL.l, gamma_2FGL.b))
gamma_3FGL.x = list(map(transform_x, gamma_3FGL.l, gamma_3FGL.b))
gamma_3FGL.y = list(map(transform_y, gamma_3FGL.l, gamma_3FGL.b))
gamma_1FHL.x = list(map(transform_x, gamma_1FHL.l, gamma_1FHL.b))
gamma_1FHL.y = list(map(transform_y, gamma_1FHL.l, gamma_1FHL.b))
gamma_2FHL.x = list(map(transform_x, gamma_2FHL.l, gamma_2FHL.b))
gamma_2FHL.y = list(map(transform_y, gamma_2FHL.l, gamma_2FHL.b))
gamma_3FHL.x = list(map(transform_x, gamma_3FHL.l, gamma_3FHL.b))
gamma_3FHL.y = list(map(transform_y, gamma_3FHL.l, gamma_3FHL.b))
gamma_FL8Y.x = list(map(transform_x, gamma_FL8Y.l, gamma_FL8Y.b))
gamma_FL8Y.y = list(map(transform_y, gamma_FL8Y.l, gamma_FL8Y.b))
gamma_1SC.x  = list(map(transform_x, gamma_1SC.l, gamma_1SC.b))
gamma_1SC.y  = list(map(transform_y, gamma_1SC.l, gamma_1SC.b))
gamma_2PC.x  = list(map(transform_x, gamma_2PC.l, gamma_2PC.b))
gamma_2PC.y  = list(map(transform_y, gamma_2PC.l, gamma_2PC.b))
gamma_GRB1.x = list(map(transform_x, gamma_GRB1.l, gamma_GRB1.b))
gamma_GRB1.y = list(map(transform_y, gamma_GRB1.l, gamma_GRB1.b))
gamma_GRB2.x = list(map(transform_x, gamma_GRB2.l, gamma_GRB2.b))
gamma_GRB2.y = list(map(transform_y, gamma_GRB2.l, gamma_GRB2.b))
gamma_2FAV.x = list(map(transform_x, gamma_2FAV.l, gamma_2FAV.b))
gamma_2FAV.y = list(map(transform_y, gamma_2FAV.l, gamma_2FAV.b))
gamma_PSR.x  = list(map(transform_x, gamma_PSR.l, gamma_PSR.b))
gamma_PSR.y  = list(map(transform_y, gamma_PSR.l, gamma_PSR.b))

fig, ax0 = plt.subplots(figsize=(7.2,4.8), facecolor='black')
fig.subplots_adjust(0,0,1,1)
ax0.set_facecolor('black')
ax0.set_aspect('equal')
ax0.set_xlim((-60,40))
ax0.set_ylim((-75,0))

# galatic grid
equator     = pandas.DataFrame(0,index=range(360),columns=['l','b','x','y']).apply(pandas.to_numeric)
meridian    = pandas.DataFrame(0,index=range(86),columns=['l','b','x','y']).apply(pandas.to_numeric)

time0 = time.time()

equator['l'] = numpy.arange(len(equator))
b05 = equator+[0,-5,0,0]
b10 = equator+[0,-10,0,0]
b15 = equator+[0,-15,0,0]
b20 = equator+[0,-20,0,0]
b25 = equator+[0,-25,0,0]
b30 = equator+[0,-30,0,0]
b35 = equator+[0,-35,0,0]
b40 = equator+[0,-40,0,0]
b45 = equator+[0,-45,0,0]
b50 = equator+[0,-50,0,0]
b55 = equator+[0,-55,0,0]
b60 = equator+[0,-60,0,0]
b65 = equator+[0,-65,0,0]
b70 = equator+[0,-70,0,0]
b75 = equator+[0,-75,0,0]
b80 = equator+[0,-80,0,0]
b85 = equator+[0,-85,0,0]

meridian['b'] = -numpy.arange(len(meridian))
l10 = meridian+[10,0,0,0]
l20 = meridian+[20,0,0,0]
l30 = meridian+[30,0,0,0]
l40 = meridian+[40,0,0,0]
l50 = meridian+[50,0,0,0]
l60 = meridian+[60,0,0,0]
l70 = meridian+[70,0,0,0]
l80 = meridian+[80,0,0,0]
l90 = meridian+[90,0,0,0]
l100 = meridian+[100,0,0,0]
l110 = meridian+[110,0,0,0]
l120 = meridian+[120,0,0,0]
l130 = meridian+[130,0,0,0]
l140 = meridian+[140,0,0,0]
l150 = meridian+[150,0,0,0]
l160 = meridian+[160,0,0,0]
l170 = meridian+[170,0,0,0]
l180 = meridian+[180,0,0,0]
l190 = meridian+[190,0,0,0]
l200 = meridian+[200,0,0,0]
l210 = meridian+[210,0,0,0]
l220 = meridian+[220,0,0,0]
l230 = meridian+[230,0,0,0]
l240 = meridian+[240,0,0,0]
l250 = meridian+[250,0,0,0]
l260 = meridian+[260,0,0,0]
l270 = meridian+[270,0,0,0]
l280 = meridian+[280,0,0,0]
l290 = meridian+[290,0,0,0]
l300 = meridian+[300,0,0,0]
l310 = meridian+[310,0,0,0]
l320 = meridian+[320,0,0,0]
l330 = meridian+[330,0,0,0]
l340 = meridian+[340,0,0,0]
l350 = meridian+[350,0,0,0]

time1 = time.time()

grid_list = [equator,b05,b10,b15,b20,b25,b30,b35,b40,b45,b50,b55,b60,b65,b70,b75,b80,b85,\
             meridian,l10,l20,l30,l40,l50,l60,l70,l80,l90,l100,l110,l120,l130,l140,l150,l160,l170,l180,\
             l190,l200,l210,l220,l230,l240,l250,l260,l270,l280,l290,l300,l310,l320,l330,l340,l350]

for df in grid_list:
    df.x = list(map(transform_x, df.l, df.b))
    df.y = list(map(transform_y, df.l, df.b))

time2 = time.time()

equator_pt = []
for i in range(len(equator)):
    equator_pt.append([equator['x'].tolist()[i],equator['y'].tolist()[i]])
b05_pt = []
for i in range(len(b05)):
    b05_pt.append([b05['x'].tolist()[i],b05['y'].tolist()[i]])
b10_pt = []
for i in range(len(b10)):
    b10_pt.append([b10['x'].tolist()[i],b10['y'].tolist()[i]])
b15_pt = []
for i in range(len(b15)):
    b15_pt.append([b15['x'].tolist()[i],b15['y'].tolist()[i]])
b20_pt = []
for i in range(len(b20)):
    b20_pt.append([b20['x'].tolist()[i],b20['y'].tolist()[i]])
b25_pt = []
for i in range(len(b25)):
    b25_pt.append([b25['x'].tolist()[i],b25['y'].tolist()[i]])
b30_pt = []
for i in range(len(b30)):
    b30_pt.append([b30['x'].tolist()[i],b30['y'].tolist()[i]])
b35_pt = []
for i in range(len(b35)):
    b35_pt.append([b35['x'].tolist()[i],b35['y'].tolist()[i]])
b40_pt = []
for i in range(len(b40)):
    b40_pt.append([b40['x'].tolist()[i],b40['y'].tolist()[i]])
b45_pt = []
for i in range(len(b45)):
    b45_pt.append([b45['x'].tolist()[i],b45['y'].tolist()[i]])
b50_pt = []
for i in range(len(b50)):
    b50_pt.append([b50['x'].tolist()[i],b50['y'].tolist()[i]])
b55_pt = []
for i in range(len(b55)):
    b55_pt.append([b55['x'].tolist()[i],b55['y'].tolist()[i]])
b60_pt = []
for i in range(len(b60)):
    b60_pt.append([b60['x'].tolist()[i],b60['y'].tolist()[i]])
b65_pt = []
for i in range(len(b65)):
    b65_pt.append([b65['x'].tolist()[i],b65['y'].tolist()[i]])
b70_pt = []
for i in range(len(b70)):
    b70_pt.append([b70['x'].tolist()[i],b70['y'].tolist()[i]])
b75_pt = []
for i in range(len(b75)):
    b75_pt.append([b75['x'].tolist()[i],b75['y'].tolist()[i]])
b80_pt = []
for i in range(len(b80)):
    b80_pt.append([b80['x'].tolist()[i],b80['y'].tolist()[i]])
b85_pt = []
for i in range(len(b85)):
    b85_pt.append([b85['x'].tolist()[i],b85['y'].tolist()[i]])
meridian_pt = []
for i in range(len(meridian)):
    meridian_pt.append([meridian['x'].tolist()[i],meridian['y'].tolist()[i]])
l10_pt = []
for i in range(len(l10)):
    l10_pt.append([l10['x'].tolist()[i],l10['y'].tolist()[i]])
l20_pt = []
for i in range(len(l20)):
    l20_pt.append([l20['x'].tolist()[i],l20['y'].tolist()[i]])
l30_pt = []
for i in range(len(l30)):
    l30_pt.append([l30['x'].tolist()[i],l30['y'].tolist()[i]])
l40_pt = []
for i in range(len(l40)):
    l40_pt.append([l40['x'].tolist()[i],l40['y'].tolist()[i]])
l50_pt = []
for i in range(len(l50)):
    l50_pt.append([l50['x'].tolist()[i],l50['y'].tolist()[i]])
l60_pt = []
for i in range(len(l60)):
    l60_pt.append([l60['x'].tolist()[i],l60['y'].tolist()[i]])
l70_pt = []
for i in range(len(l70)):
    l70_pt.append([l70['x'].tolist()[i],l70['y'].tolist()[i]])
l80_pt = []
for i in range(len(l80)):
    l80_pt.append([l80['x'].tolist()[i],l80['y'].tolist()[i]])
l90_pt = []
for i in range(len(l90)):
    l90_pt.append([l90['x'].tolist()[i],l90['y'].tolist()[i]])
l100_pt = []
for i in range(len(l100)):
    l100_pt.append([l100['x'].tolist()[i],l100['y'].tolist()[i]])
l110_pt = []
for i in range(len(l110)):
    l110_pt.append([l110['x'].tolist()[i],l110['y'].tolist()[i]])
l120_pt = []
for i in range(len(l120)):
    l120_pt.append([l120['x'].tolist()[i],l120['y'].tolist()[i]])
l130_pt = []
for i in range(len(l130)):
    l130_pt.append([l130['x'].tolist()[i],l130['y'].tolist()[i]])
l140_pt = []
for i in range(len(l140)):
    l140_pt.append([l140['x'].tolist()[i],l140['y'].tolist()[i]])
l150_pt = []
for i in range(len(l150)):
    l150_pt.append([l150['x'].tolist()[i],l150['y'].tolist()[i]])
l160_pt = []
for i in range(len(l160)):
    l160_pt.append([l160['x'].tolist()[i],l160['y'].tolist()[i]])
l170_pt = []
for i in range(len(l170)):
    l170_pt.append([l170['x'].tolist()[i],l170['y'].tolist()[i]])
l180_pt = []
for i in range(len(l180)):
    l180_pt.append([l180['x'].tolist()[i],l180['y'].tolist()[i]])
l190_pt = []
for i in range(len(l190)):
    l190_pt.append([l190['x'].tolist()[i],l190['y'].tolist()[i]])
l200_pt = []
for i in range(len(l200)):
    l200_pt.append([l200['x'].tolist()[i],l200['y'].tolist()[i]])
l210_pt = []
for i in range(len(l210)):
    l210_pt.append([l210['x'].tolist()[i],l210['y'].tolist()[i]])
l220_pt = []
for i in range(len(l220)):
    l220_pt.append([l220['x'].tolist()[i],l220['y'].tolist()[i]])
l230_pt = []
for i in range(len(l230)):
    l230_pt.append([l230['x'].tolist()[i],l230['y'].tolist()[i]])
l240_pt = []
for i in range(len(l240)):
    l240_pt.append([l240['x'].tolist()[i],l240['y'].tolist()[i]])
l250_pt = []
for i in range(len(l250)):
    l250_pt.append([l250['x'].tolist()[i],l250['y'].tolist()[i]])
l260_pt = []
for i in range(len(l260)):
    l260_pt.append([l260['x'].tolist()[i],l260['y'].tolist()[i]])
l270_pt = []
for i in range(len(l270)):
    l270_pt.append([l270['x'].tolist()[i],l270['y'].tolist()[i]])
l280_pt = []
for i in range(len(l280)):
    l280_pt.append([l280['x'].tolist()[i],l280['y'].tolist()[i]])
l290_pt = []
for i in range(len(l290)):
    l290_pt.append([l290['x'].tolist()[i],l290['y'].tolist()[i]])
l300_pt = []
for i in range(len(l300)):
    l300_pt.append([l300['x'].tolist()[i],l300['y'].tolist()[i]])
l310_pt = []
for i in range(len(l310)):
    l310_pt.append([l310['x'].tolist()[i],l310['y'].tolist()[i]])
l320_pt = []
for i in range(len(l320)):
    l320_pt.append([l320['x'].tolist()[i],l320['y'].tolist()[i]])
l330_pt = []
for i in range(len(l330)):
    l330_pt.append([l330['x'].tolist()[i],l330['y'].tolist()[i]])
l340_pt = []
for i in range(len(l340)):
    l340_pt.append([l340['x'].tolist()[i],l340['y'].tolist()[i]])
l350_pt = []
for i in range(len(l350)):
    l350_pt.append([l350['x'].tolist()[i],l350['y'].tolist()[i]])

time3 = time.time()

equator_line = plt.Polygon(equator_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b05_line = plt.Polygon(b05_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b10_line = plt.Polygon(b10_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b15_line = plt.Polygon(b15_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b20_line = plt.Polygon(b20_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b25_line = plt.Polygon(b25_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b30_line = plt.Polygon(b30_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b35_line = plt.Polygon(b35_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b40_line = plt.Polygon(b40_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b45_line = plt.Polygon(b45_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b50_line = plt.Polygon(b50_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b55_line = plt.Polygon(b55_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b60_line = plt.Polygon(b60_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b65_line = plt.Polygon(b65_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b70_line = plt.Polygon(b70_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b75_line = plt.Polygon(b75_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b80_line = plt.Polygon(b80_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
b85_line = plt.Polygon(b85_pt, closed=True, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
meridian_line = plt.Polygon(meridian_pt, closed=False, fill=None, edgecolor=(1,0.5,0.5,0.5), zorder=1+2.5)
l10_line = plt.Polygon(l10_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l20_line = plt.Polygon(l20_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l30_line = plt.Polygon(l30_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l40_line = plt.Polygon(l40_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l50_line = plt.Polygon(l50_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l60_line = plt.Polygon(l60_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l70_line = plt.Polygon(l70_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l80_line = plt.Polygon(l80_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l90_line = plt.Polygon(l90_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l100_line = plt.Polygon(l100_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l110_line = plt.Polygon(l110_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l120_line = plt.Polygon(l120_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l130_line = plt.Polygon(l130_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l140_line = plt.Polygon(l140_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l150_line = plt.Polygon(l150_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l160_line = plt.Polygon(l160_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l170_line = plt.Polygon(l170_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l180_line = plt.Polygon(l180_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l190_line = plt.Polygon(l190_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l200_line = plt.Polygon(l200_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l210_line = plt.Polygon(l210_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l220_line = plt.Polygon(l220_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l230_line = plt.Polygon(l230_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l240_line = plt.Polygon(l240_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l250_line = plt.Polygon(l250_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l260_line = plt.Polygon(l260_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l270_line = plt.Polygon(l270_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l280_line = plt.Polygon(l280_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l290_line = plt.Polygon(l290_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l300_line = plt.Polygon(l300_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l310_line = plt.Polygon(l310_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l320_line = plt.Polygon(l320_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l330_line = plt.Polygon(l330_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l340_line = plt.Polygon(l340_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)
l350_line = plt.Polygon(l350_pt, closed=False, fill=None, edgecolor=(1,0,0,0.5), zorder=1+2.5)

grid_line_list = [equator_line,b05_line,b10_line,b15_line,b20_line,b25_line,b30_line,b35_line,b40_line,b45_line,b50_line,b55_line,b60_line,b65_line,b70_line,b75_line,b80_line,b85_line,\
                  meridian_line,l10_line,l20_line,l30_line,l40_line,l50_line,l60_line,l70_line,l80_line,l90_line,l100_line,l110_line,l120_line,l130_line,l140_line,l150_line,l160_line,l170_line,l180_line,\
                  l190_line,l200_line,l210_line,l220_line,l230_line,l240_line,l250_line,l260_line,l270_line,l280_line,l290_line,l300_line,l310_line,l320_line,l330_line,l340_line,l350_line]

for i in grid_line_list:
    ax0.add_patch(i)

time4 = time.time()

# milkyway
MW_southernedge = numpy.zeros(shape=(263,6))
MW_southernedge = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_southernedge.csv'))
MW_MonPer       = numpy.zeros(shape=(71,6))
MW_MonPer       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_MonPer.csv'))
MW_CamCas       = numpy.zeros(shape=(13,6))
MW_CamCas       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_CamCas.csv'))
MW_Cep          = numpy.zeros(shape=(13,6))
MW_Cep          = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_Cep.csv'))
MW_CygOph       = numpy.zeros(shape=(40,6))
MW_CygOph       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_CygOph.csv'))
MW_OphSco       = numpy.zeros(shape=(17,6))
MW_OphSco       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_OphSco.csv'))
MW_LupVel       = numpy.zeros(shape=(78,6))
MW_LupVel       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LupVel.csv'))
MW_VelMon       = numpy.zeros(shape=(34,6))
MW_VelMon       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_VelMon.csv'))
dark_PerCas     = numpy.zeros(shape=(35,6))
dark_PerCas     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_PerCas.csv'))
dark_CasCep     = numpy.zeros(shape=(28,6))
dark_CasCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CasCep.csv'))
dark_betaCas    = numpy.zeros(shape=(20,6))
dark_betaCas    = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_betaCas.csv'))
dark_CygCep     = numpy.zeros(shape=(22,6))
dark_CygCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CygCep.csv'))
dark_CygOph     = numpy.zeros(shape=(197,6))
dark_CygOph     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CygOph.csv'))
dark_thetaOph   = numpy.zeros(shape=(28,6))
dark_thetaOph   = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_thetaOph.csv'))
dark_lambdaSco  = numpy.zeros(shape=(17,6))
dark_lambdaSco  = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_lambdaSco.csv'))
dark_ScoNor     = numpy.zeros(shape=(31,6))
dark_ScoNor     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_ScoNor.csv'))
dark_Coalsack   = numpy.zeros(shape=(32,6))
dark_Coalsack   = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_Coalsack.csv'))
dark_Vel        = numpy.zeros(shape=(22,6))
dark_Vel        = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_Vel.csv'))
MW_LMC1         = numpy.zeros(shape=(34,6))
MW_LMC1         = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LMC1.csv'))
MW_LMC2         = numpy.zeros(shape=(12,6))
MW_LMC2         = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LMC2.csv'))
MW_SMC          = numpy.zeros(shape=(14,6))
MW_SMC          = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_SMC.csv'))

MW_list = [MW_southernedge,MW_MonPer,MW_CamCas,MW_Cep,MW_CygOph,MW_OphSco,MW_LupVel,MW_VelMon,\
           dark_PerCas,dark_CasCep,dark_betaCas,dark_CygCep,dark_CygOph,dark_thetaOph,dark_lambdaSco,dark_ScoNor,dark_Coalsack,dark_Vel,\
           MW_LMC1,MW_LMC2,MW_SMC]

for df in MW_list:
    df.l = list(map(transform_l, df.RA, df.Dec))
    df.b = list(map(transform_b, df.RA, df.Dec))    
    df.x = list(map(transform_x, df.l, df.b))
    df.y = list(map(transform_y, df.l, df.b))
    for i in range(len(df)-1):
        ax0.plot([df.x[i],df.x[i+1]],[df.y[i],df.y[i+1]],'b-',alpha=0.5,zorder=1+2.5)

#ax0.scatter(gamma_0FGL.x,gamma_0FGL.y, 10, c='magenta', zorder=3+2.5)
#ax0.scatter(gamma_1FGL.x,gamma_1FGL.y, gamma_1FGL.Flux_Density*5*100000000000, c='white', zorder=3+2.5)
#ax0.scatter(gamma_2FGL.x,gamma_2FGL.y, gamma_2FGL.Flux_Density*5*100000000000, c='yellow', zorder=3+2.5)
#ax0.scatter(gamma_3FGL.x,gamma_3FGL.y, gamma_3FGL.Flux_Density*5*100000000000, c='orange', zorder=3+2.5)
#ax0.scatter(gamma_1FHL.x,gamma_1FHL.y, 10, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_2FHL.x,gamma_2FHL.y, 10, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_3FHL.x,gamma_3FHL.y, gamma_3FHL.Flux_Density*5*100000000000000, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_FL8Y.x,gamma_FL8Y.y, gamma_FL8Y.Flux_Density*5*1000000000000, c='green', zorder=3+2.5)
#ax0.scatter(gamma_1SC.x,gamma_1SC.y, 10, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_2PC.x,gamma_2PC.y, 10, c='cyan', zorder=3+2.5)
ax0.scatter(gamma_GRB1.x,gamma_GRB1.y, 10, c='magenta', zorder=3+2.5)
ax0.scatter(gamma_GRB2.x,gamma_GRB2.y, 10, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_2FAV.x,gamma_2FAV.y, 10, c='cyan', zorder=3+2.5)
#ax0.scatter(gamma_PSR.x,gamma_PSR.y, 10, c='cyan', zorder=3+2.5)

Black_Widow_Spider = [((gamma_3FGL.x[453],gamma_3FGL.y[453]),(gamma_3FGL.x[454],gamma_3FGL.y[454])),\
                      ((gamma_3FGL.x[454],gamma_3FGL.y[454]),(gamma_3FGL.x[1686],gamma_3FGL.y[1686])),\
                      ((gamma_3FGL.x[581],gamma_3FGL.y[581]),(gamma_3FGL.x[584],gamma_3FGL.y[584])),\
                      ((gamma_3FGL.x[581],gamma_3FGL.y[581]),(gamma_3FGL.x[1750],gamma_3FGL.y[1750])),\
                      ((gamma_3FGL.x[583],gamma_3FGL.y[583]),(gamma_3FGL.x[584],gamma_3FGL.y[584])),\
                      ((gamma_3FGL.x[583],gamma_3FGL.y[583]),(gamma_3FGL.x[600],gamma_3FGL.y[600])),\
                      ((gamma_3FGL.x[584],gamma_3FGL.y[584]),(gamma_3FGL.x[614],gamma_3FGL.y[614])),\
                      ((gamma_3FGL.x[584],gamma_3FGL.y[584]),(gamma_3FGL.x[766],gamma_3FGL.y[766])),\
                      ((gamma_3FGL.x[600],gamma_3FGL.y[600]),(gamma_3FGL.x[2210],gamma_3FGL.y[2210])),\
                      ((gamma_3FGL.x[614],gamma_3FGL.y[614]),(gamma_3FGL.x[1729],gamma_3FGL.y[1729])),\
                      ((gamma_3FGL.x[764],gamma_3FGL.y[764]),(gamma_3FGL.x[770],gamma_3FGL.y[770])),\
                      ((gamma_3FGL.x[764],gamma_3FGL.y[764]),(gamma_3FGL.x[873],gamma_3FGL.y[873])),\
                      ((gamma_3FGL.x[765],gamma_3FGL.y[765]),(gamma_3FGL.x[934],gamma_3FGL.y[934])),\
                      ((gamma_3FGL.x[765],gamma_3FGL.y[765]),(gamma_3FGL.x[767],gamma_3FGL.y[767])),\
                      ((gamma_3FGL.x[765],gamma_3FGL.y[765]),(gamma_3FGL.x[770],gamma_3FGL.y[770])),\
                      ((gamma_3FGL.x[765],gamma_3FGL.y[765]),(gamma_3FGL.x[2309],gamma_3FGL.y[2309])),\
                      ((gamma_3FGL.x[766],gamma_3FGL.y[766]),(gamma_3FGL.x[767],gamma_3FGL.y[767])),\
                      ((gamma_3FGL.x[767],gamma_3FGL.y[767]),(gamma_3FGL.x[1300],gamma_3FGL.y[1300])),\
                      ((gamma_3FGL.x[934],gamma_3FGL.y[934]),(gamma_3FGL.x[2633],gamma_3FGL.y[2633])),\
                      ((gamma_3FGL.x[1232],gamma_3FGL.y[1232]),(gamma_3FGL.x[1233],gamma_3FGL.y[1233])),\
                      ((gamma_3FGL.x[1232],gamma_3FGL.y[1232]),(gamma_3FGL.x[1522],gamma_3FGL.y[1522])),\
                      ((gamma_3FGL.x[1233],gamma_3FGL.y[1233]),(gamma_3FGL.x[1234],gamma_3FGL.y[1234])),\
                      ((gamma_3FGL.x[1300],gamma_3FGL.y[1300]),(gamma_3FGL.x[1680],gamma_3FGL.y[1680])),\
                      ((gamma_3FGL.x[1473],gamma_3FGL.y[1473]),(gamma_3FGL.x[1474],gamma_3FGL.y[1474])),\
                      ((gamma_3FGL.x[1473],gamma_3FGL.y[1473]),(gamma_3FGL.x[2309],gamma_3FGL.y[2309])),\
                      ((gamma_3FGL.x[1474],gamma_3FGL.y[1474]),(gamma_3FGL.x[1522],gamma_3FGL.y[1522])),\
                      ((gamma_3FGL.x[1662],gamma_3FGL.y[1662]),(gamma_3FGL.x[2211],gamma_3FGL.y[2211])),\
                      ((gamma_3FGL.x[1680],gamma_3FGL.y[1680]),(gamma_3FGL.x[1722],gamma_3FGL.y[1722])),\
                      ((gamma_3FGL.x[1681],gamma_3FGL.y[1681]),(gamma_3FGL.x[1682],gamma_3FGL.y[1682])),\
                      ((gamma_3FGL.x[1681],gamma_3FGL.y[1681]),(gamma_3FGL.x[2855],gamma_3FGL.y[2855])),\
                      ((gamma_3FGL.x[1682],gamma_3FGL.y[1682]),(gamma_3FGL.x[1936],gamma_3FGL.y[1936])),\
                      ((gamma_3FGL.x[1720],gamma_3FGL.y[1720]),(gamma_3FGL.x[1722],gamma_3FGL.y[1722])),\
                      ((gamma_3FGL.x[1728],gamma_3FGL.y[1728]),(gamma_3FGL.x[1729],gamma_3FGL.y[1729])),\
                      ((gamma_3FGL.x[1728],gamma_3FGL.y[1728]),(gamma_3FGL.x[1730],gamma_3FGL.y[1730])),\
                      ((gamma_3FGL.x[1730],gamma_3FGL.y[1730]),(gamma_3FGL.x[1731],gamma_3FGL.y[1731])),\
                      ((gamma_3FGL.x[1731],gamma_3FGL.y[1731]),(gamma_3FGL.x[2908],gamma_3FGL.y[2908])),\
                      ((gamma_3FGL.x[1750],gamma_3FGL.y[1750]),(gamma_3FGL.x[1752],gamma_3FGL.y[1752])),\
                      ((gamma_3FGL.x[1751],gamma_3FGL.y[1751]),(gamma_3FGL.x[1752],gamma_3FGL.y[1752])),\
                      ((gamma_3FGL.x[1936],gamma_3FGL.y[1936]),(gamma_3FGL.x[1938],gamma_3FGL.y[1938])),\
                      ((gamma_3FGL.x[1937],gamma_3FGL.y[1937]),(gamma_3FGL.x[1938],gamma_3FGL.y[1938])),\
                      ((gamma_3FGL.x[2210],gamma_3FGL.y[2210]),(gamma_3FGL.x[2211],gamma_3FGL.y[2211])),\
                      ((gamma_3FGL.x[2633],gamma_3FGL.y[2633]),(gamma_3FGL.x[2634],gamma_3FGL.y[2634])),\
                      ((gamma_3FGL.x[2908],gamma_3FGL.y[2908]),(gamma_3FGL.x[2910],gamma_3FGL.y[2910])),\
                      ((gamma_3FGL.x[2910],gamma_3FGL.y[2910]),(gamma_3FGL.x[2911],gamma_3FGL.y[2911]))]
                      #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[2855],gamma_3FGL.y[2855])),\

Colosseum = [((gamma_3FGL.x[565],gamma_3FGL.y[565]),(gamma_3FGL.x[586],gamma_3FGL.y[586])),\
             ((gamma_3FGL.x[565],gamma_3FGL.y[565]),(gamma_3FGL.x[945],gamma_3FGL.y[945])),\
             ((gamma_3FGL.x[565],gamma_3FGL.y[565]),(gamma_3FGL.x[1533],gamma_3FGL.y[1533])),\
             ((gamma_3FGL.x[586],gamma_3FGL.y[586]),(gamma_3FGL.x[699],gamma_3FGL.y[699])),\
             ((gamma_3FGL.x[586],gamma_3FGL.y[586]),(gamma_3FGL.x[2886],gamma_3FGL.y[2886])),\
             ((gamma_3FGL.x[696],gamma_3FGL.y[696]),(gamma_3FGL.x[699],gamma_3FGL.y[699])),\
             ((gamma_3FGL.x[696],gamma_3FGL.y[696]),(gamma_3FGL.x[2481],gamma_3FGL.y[2481])),\
             ((gamma_3FGL.x[945],gamma_3FGL.y[945]),(gamma_3FGL.x[1950],gamma_3FGL.y[1950])),\
             ((gamma_3FGL.x[1494],gamma_3FGL.y[1494]),(gamma_3FGL.x[2477],gamma_3FGL.y[2477])),\
             ((gamma_3FGL.x[1494],gamma_3FGL.y[1494]),(gamma_3FGL.x[2558],gamma_3FGL.y[2558])),\
             ((gamma_3FGL.x[1494],gamma_3FGL.y[1494]),(gamma_3FGL.x[2873],gamma_3FGL.y[2873])),\
             ((gamma_3FGL.x[1533],gamma_3FGL.y[1533]),(gamma_3FGL.x[1534],gamma_3FGL.y[1534])),\
             ((gamma_3FGL.x[1534],gamma_3FGL.y[1534]),(gamma_3FGL.x[2523],gamma_3FGL.y[2523])),\
             ((gamma_3FGL.x[1874],gamma_3FGL.y[1874]),(gamma_3FGL.x[2457],gamma_3FGL.y[2457])),\
             ((gamma_3FGL.x[1874],gamma_3FGL.y[1874]),(gamma_3FGL.x[2465],gamma_3FGL.y[2465])),\
             ((gamma_3FGL.x[1890],gamma_3FGL.y[1890]),(gamma_3FGL.x[1950],gamma_3FGL.y[1950])),\
             ((gamma_3FGL.x[1890],gamma_3FGL.y[1890]),(gamma_3FGL.x[2467],gamma_3FGL.y[2467])),\
             ((gamma_3FGL.x[2367],gamma_3FGL.y[2367]),(gamma_3FGL.x[2532],gamma_3FGL.y[2532])),\
             ((gamma_3FGL.x[2367],gamma_3FGL.y[2367]),(gamma_3FGL.x[2558],gamma_3FGL.y[2558])),\
             ((gamma_3FGL.x[2457],gamma_3FGL.y[2457]),(gamma_3FGL.x[2873],gamma_3FGL.y[2873])),\
             ((gamma_3FGL.x[2465],gamma_3FGL.y[2465]),(gamma_3FGL.x[2466],gamma_3FGL.y[2466])),\
             ((gamma_3FGL.x[2466],gamma_3FGL.y[2466]),(gamma_3FGL.x[2467],gamma_3FGL.y[2467])),\
             ((gamma_3FGL.x[2467],gamma_3FGL.y[2467]),(gamma_3FGL.x[2886],gamma_3FGL.y[2886])),\
             ((gamma_3FGL.x[2477],gamma_3FGL.y[2477]),(gamma_3FGL.x[2481],gamma_3FGL.y[2481])),\
             ((gamma_3FGL.x[2481],gamma_3FGL.y[2481]),(gamma_3FGL.x[2886],gamma_3FGL.y[2886])),\
             ((gamma_3FGL.x[2523],gamma_3FGL.y[2523]),(gamma_3FGL.x[2532],gamma_3FGL.y[2532]))]

Eiffel_Tower = [((gamma_3FGL.x[689],gamma_3FGL.y[689]),(gamma_3FGL.x[690],gamma_3FGL.y[690])),\
                ((gamma_3FGL.x[689],gamma_3FGL.y[689]),(gamma_3FGL.x[691],gamma_3FGL.y[691])),\
                ((gamma_3FGL.x[689],gamma_3FGL.y[689]),(gamma_3FGL.x[1463],gamma_3FGL.y[1463])),\
                ((gamma_3FGL.x[689],gamma_3FGL.y[689]),(gamma_3FGL.x[2505],gamma_3FGL.y[2505])),\
                ((gamma_3FGL.x[689],gamma_3FGL.y[689]),(gamma_3FGL.x[2506],gamma_3FGL.y[2506])),\
                ((gamma_3FGL.x[690],gamma_3FGL.y[690]),(gamma_3FGL.x[1883],gamma_3FGL.y[1883])),\
                ((gamma_3FGL.x[691],gamma_3FGL.y[691]),(gamma_3FGL.x[1487],gamma_3FGL.y[1487])),\
                ((gamma_3FGL.x[691],gamma_3FGL.y[691]),(gamma_3FGL.x[2507],gamma_3FGL.y[2507])),\
                ((gamma_3FGL.x[798],gamma_3FGL.y[798]),(gamma_3FGL.x[800],gamma_3FGL.y[800])),\
                ((gamma_3FGL.x[798],gamma_3FGL.y[798]),(gamma_3FGL.x[2434],gamma_3FGL.y[2434])),\
                ((gamma_3FGL.x[800],gamma_3FGL.y[800]),(gamma_3FGL.x[911],gamma_3FGL.y[911])),\
                ((gamma_3FGL.x[911],gamma_3FGL.y[911]),(gamma_3FGL.x[916],gamma_3FGL.y[916])),\
                ((gamma_3FGL.x[916],gamma_3FGL.y[916]),(gamma_3FGL.x[2686],gamma_3FGL.y[2686])),\
                ((gamma_3FGL.x[1445],gamma_3FGL.y[1445]),(gamma_3FGL.x[1876],gamma_3FGL.y[1876])),\
                ((gamma_3FGL.x[1445],gamma_3FGL.y[1445]),(gamma_3FGL.x[2731],gamma_3FGL.y[2731])),\
                ((gamma_3FGL.x[1463],gamma_3FGL.y[1463]),(gamma_3FGL.x[1876],gamma_3FGL.y[1876])),\
                ((gamma_3FGL.x[1463],gamma_3FGL.y[1463]),(gamma_3FGL.x[1883],gamma_3FGL.y[1883])),\
                ((gamma_3FGL.x[1487],gamma_3FGL.y[1487]),(gamma_3FGL.x[1883],gamma_3FGL.y[1883])),\
                ((gamma_3FGL.x[1488],gamma_3FGL.y[1488]),(gamma_3FGL.x[1487],gamma_3FGL.y[1487])),\
                ((gamma_3FGL.x[1488],gamma_3FGL.y[1488]),(gamma_3FGL.x[2332],gamma_3FGL.y[2332])),\
                ((gamma_3FGL.x[1514],gamma_3FGL.y[1514]),(gamma_3FGL.x[1971],gamma_3FGL.y[1971])),\
                ((gamma_3FGL.x[1514],gamma_3FGL.y[1514]),(gamma_3FGL.x[2122],gamma_3FGL.y[2122])),\
                ((gamma_3FGL.x[1971],gamma_3FGL.y[1971]),(gamma_3FGL.x[2687],gamma_3FGL.y[2687])),\
                ((gamma_3FGL.x[2122],gamma_3FGL.y[2122]),(gamma_3FGL.x[2332],gamma_3FGL.y[2332])),\
                ((gamma_3FGL.x[2432],gamma_3FGL.y[2432]),(gamma_3FGL.x[2433],gamma_3FGL.y[2433])),\
                ((gamma_3FGL.x[2433],gamma_3FGL.y[2433]),(gamma_3FGL.x[2434],gamma_3FGL.y[2434])),\
                ((gamma_3FGL.x[2432],gamma_3FGL.y[2432]),(gamma_3FGL.x[2613],gamma_3FGL.y[2613])),\
                ((gamma_3FGL.x[2505],gamma_3FGL.y[2505]),(gamma_3FGL.x[2506],gamma_3FGL.y[2506])),\
                ((gamma_3FGL.x[2506],gamma_3FGL.y[2506]),(gamma_3FGL.x[2507],gamma_3FGL.y[2507])),\
                ((gamma_3FGL.x[2612],gamma_3FGL.y[2612]),(gamma_3FGL.x[2613],gamma_3FGL.y[2613])),\
                ((gamma_3FGL.x[2612],gamma_3FGL.y[2612]),(gamma_3FGL.x[2731],gamma_3FGL.y[2731])),\
                ((gamma_3FGL.x[2686],gamma_3FGL.y[2686]),(gamma_3FGL.x[2687],gamma_3FGL.y[2687])),\
                ((gamma_3FGL.x[911],gamma_3FGL.y[911]),(gamma_3FGL.x[1481],gamma_3FGL.y[1481])),\
                ((gamma_3FGL.x[1481],gamma_3FGL.y[1481]),(gamma_3FGL.x[1883],gamma_3FGL.y[1883]))]
                #((gamma_3FGL.x[1],gamma_3FGL.y[1]),(gamma_3FGL.x[1876],gamma_3FGL.y[1876])),\
                #((gamma_3FGL.x[1],gamma_3FGL.y[1]),(gamma_3FGL.x[2332],gamma_3FGL.y[2332]))]

Einstein = [((gamma_3FGL.x[594],gamma_3FGL.y[594]),(gamma_3FGL.x[2666],gamma_3FGL.y[2666])),\
            ((gamma_3FGL.x[594],gamma_3FGL.y[594]),(gamma_3FGL.x[2856],gamma_3FGL.y[2856])),\
            ((gamma_3FGL.x[866],gamma_3FGL.y[866]),(gamma_3FGL.x[867],gamma_3FGL.y[867])),\
            ((gamma_3FGL.x[866],gamma_3FGL.y[866]),(gamma_3FGL.x[2669],gamma_3FGL.y[2669])),\
            ((gamma_3FGL.x[867],gamma_3FGL.y[867]),(gamma_3FGL.x[868],gamma_3FGL.y[868])),\
            ((gamma_3FGL.x[868],gamma_3FGL.y[868]),(gamma_3FGL.x[869],gamma_3FGL.y[869])),\
            ((gamma_3FGL.x[869],gamma_3FGL.y[869]),(gamma_3FGL.x[2632],gamma_3FGL.y[2632])),\
            ((gamma_3FGL.x[1327],gamma_3FGL.y[1327]),(gamma_3FGL.x[2652],gamma_3FGL.y[2652])),\
            ((gamma_3FGL.x[1327],gamma_3FGL.y[1327]),(gamma_3FGL.x[2926],gamma_3FGL.y[2926])),\
            ((gamma_3FGL.x[1677],gamma_3FGL.y[1677]),(gamma_3FGL.x[1678],gamma_3FGL.y[1678])),\
            ((gamma_3FGL.x[1677],gamma_3FGL.y[1677]),(gamma_3FGL.x[2629],gamma_3FGL.y[2629])),\
            ((gamma_3FGL.x[1678],gamma_3FGL.y[1678]),(gamma_3FGL.x[2906],gamma_3FGL.y[2906])),\
            ((gamma_3FGL.x[1704],gamma_3FGL.y[1704]),(gamma_3FGL.x[1705],gamma_3FGL.y[1705])),\
            ((gamma_3FGL.x[1704],gamma_3FGL.y[1704]),(gamma_3FGL.x[1968],gamma_3FGL.y[1968])),\
            ((gamma_3FGL.x[1705],gamma_3FGL.y[1705]),(gamma_3FGL.x[1941],gamma_3FGL.y[1941])),\
            ((gamma_3FGL.x[1705],gamma_3FGL.y[1705]),(gamma_3FGL.x[1960],gamma_3FGL.y[1960])),\
            ((gamma_3FGL.x[1939],gamma_3FGL.y[1939]),(gamma_3FGL.x[1941],gamma_3FGL.y[1941])),\
            ((gamma_3FGL.x[1939],gamma_3FGL.y[1939]),(gamma_3FGL.x[2662],gamma_3FGL.y[2662])),\
            ((gamma_3FGL.x[1958],gamma_3FGL.y[1958]),(gamma_3FGL.x[1959],gamma_3FGL.y[1959])),\
            ((gamma_3FGL.x[1958],gamma_3FGL.y[1958]),(gamma_3FGL.x[2253],gamma_3FGL.y[2253])),\
            ((gamma_3FGL.x[1959],gamma_3FGL.y[1959]),(gamma_3FGL.x[1960],gamma_3FGL.y[1960])),\
            ((gamma_3FGL.x[1968],gamma_3FGL.y[1968]),(gamma_3FGL.x[1969],gamma_3FGL.y[1969])),\
            ((gamma_3FGL.x[1968],gamma_3FGL.y[1968]),(gamma_3FGL.x[2538],gamma_3FGL.y[2538])),\
            ((gamma_3FGL.x[1969],gamma_3FGL.y[1969]),(gamma_3FGL.x[2650],gamma_3FGL.y[2650])),\
            ((gamma_3FGL.x[2251],gamma_3FGL.y[2251]),(gamma_3FGL.x[2252],gamma_3FGL.y[2252])),\
            ((gamma_3FGL.x[2251],gamma_3FGL.y[2251]),(gamma_3FGL.x[2254],gamma_3FGL.y[2254])),\
            ((gamma_3FGL.x[2252],gamma_3FGL.y[2252]),(gamma_3FGL.x[2456],gamma_3FGL.y[2456])),\
            ((gamma_3FGL.x[2253],gamma_3FGL.y[2253]),(gamma_3FGL.x[2254],gamma_3FGL.y[2254])),\
            ((gamma_3FGL.x[2454],gamma_3FGL.y[2454]),(gamma_3FGL.x[2455],gamma_3FGL.y[2455])),\
            ((gamma_3FGL.x[2454],gamma_3FGL.y[2454]),(gamma_3FGL.x[2858],gamma_3FGL.y[2858])),\
            ((gamma_3FGL.x[2455],gamma_3FGL.y[2455]),(gamma_3FGL.x[2456],gamma_3FGL.y[2456])),\
            ((gamma_3FGL.x[2538],gamma_3FGL.y[2538]),(gamma_3FGL.x[2539],gamma_3FGL.y[2539])),\
            ((gamma_3FGL.x[2539],gamma_3FGL.y[2539]),(gamma_3FGL.x[2643],gamma_3FGL.y[2643])),\
            ((gamma_3FGL.x[2540],gamma_3FGL.y[2540]),(gamma_3FGL.x[2905],gamma_3FGL.y[2905])),\
            ((gamma_3FGL.x[2540],gamma_3FGL.y[2540]),(gamma_3FGL.x[2926],gamma_3FGL.y[2926])),\
            ((gamma_3FGL.x[2629],gamma_3FGL.y[2629]),(gamma_3FGL.x[2641],gamma_3FGL.y[2641])),\
            ((gamma_3FGL.x[2632],gamma_3FGL.y[2632]),(gamma_3FGL.x[2864],gamma_3FGL.y[2864])),\
            ((gamma_3FGL.x[2641],gamma_3FGL.y[2641]),(gamma_3FGL.x[2643],gamma_3FGL.y[2643])),\
            ((gamma_3FGL.x[2641],gamma_3FGL.y[2641]),(gamma_3FGL.x[2865],gamma_3FGL.y[2865])),\
            ((gamma_3FGL.x[2650],gamma_3FGL.y[2650]),(gamma_3FGL.x[2651],gamma_3FGL.y[2651])),\
            ((gamma_3FGL.x[2651],gamma_3FGL.y[2651]),(gamma_3FGL.x[2652],gamma_3FGL.y[2652])),\
            ((gamma_3FGL.x[2659],gamma_3FGL.y[2659]),(gamma_3FGL.x[2856],gamma_3FGL.y[2856])),\
            ((gamma_3FGL.x[2659],gamma_3FGL.y[2659]),(gamma_3FGL.x[2857],gamma_3FGL.y[2857])),\
            ((gamma_3FGL.x[2660],gamma_3FGL.y[2660]),(gamma_3FGL.x[2661],gamma_3FGL.y[2661])),\
            ((gamma_3FGL.x[2660],gamma_3FGL.y[2660]),(gamma_3FGL.x[2845],gamma_3FGL.y[2845])),\
            ((gamma_3FGL.x[2661],gamma_3FGL.y[2661]),(gamma_3FGL.x[2662],gamma_3FGL.y[2662])),\
            ((gamma_3FGL.x[2666],gamma_3FGL.y[2666]),(gamma_3FGL.x[2668],gamma_3FGL.y[2668])),\
            ((gamma_3FGL.x[2668],gamma_3FGL.y[2668]),(gamma_3FGL.x[2669],gamma_3FGL.y[2669])),\
            ((gamma_3FGL.x[2845],gamma_3FGL.y[2845]),(gamma_3FGL.x[2864],gamma_3FGL.y[2864])),\
            ((gamma_3FGL.x[2857],gamma_3FGL.y[2857]),(gamma_3FGL.x[2858],gamma_3FGL.y[2858])),\
            ((gamma_3FGL.x[2864],gamma_3FGL.y[2864]),(gamma_3FGL.x[2865],gamma_3FGL.y[2865])),\
            ((gamma_3FGL.x[2905],gamma_3FGL.y[2905]),(gamma_3FGL.x[2906],gamma_3FGL.y[2906]))]

Fermi_Satellite = [((gamma_3FGL.x[579],gamma_3FGL.y[579]),(gamma_3FGL.x[598],gamma_3FGL.y[598])),\
                   ((gamma_3FGL.x[579],gamma_3FGL.y[579]),(gamma_3FGL.x[1618],gamma_3FGL.y[1618])),\
                   ((gamma_3FGL.x[595],gamma_3FGL.y[595]),(gamma_3FGL.x[983],gamma_3FGL.y[983])),\
                   ((gamma_3FGL.x[595],gamma_3FGL.y[595]),(gamma_3FGL.x[598],gamma_3FGL.y[598])),\
                   ((gamma_3FGL.x[595],gamma_3FGL.y[595]),(gamma_3FGL.x[1268],gamma_3FGL.y[1268])),\
                   ((gamma_3FGL.x[596],gamma_3FGL.y[596]),(gamma_3FGL.x[598],gamma_3FGL.y[598])),\
                   ((gamma_3FGL.x[597],gamma_3FGL.y[597]),(gamma_3FGL.x[598],gamma_3FGL.y[598])),\
                   ((gamma_3FGL.x[721],gamma_3FGL.y[721]),(gamma_3FGL.x[722],gamma_3FGL.y[722])),\
                   ((gamma_3FGL.x[831],gamma_3FGL.y[831]),(gamma_3FGL.x[985],gamma_3FGL.y[985])),\
                   ((gamma_3FGL.x[831],gamma_3FGL.y[831]),(gamma_3FGL.x[996],gamma_3FGL.y[996])),\
                   ((gamma_3FGL.x[982],gamma_3FGL.y[982]),(gamma_3FGL.x[983],gamma_3FGL.y[983])),\
                   ((gamma_3FGL.x[982],gamma_3FGL.y[982]),(gamma_3FGL.x[987],gamma_3FGL.y[987])),\
                   ((gamma_3FGL.x[983],gamma_3FGL.y[983]),(gamma_3FGL.x[984],gamma_3FGL.y[984])),\
                   ((gamma_3FGL.x[984],gamma_3FGL.y[984]),(gamma_3FGL.x[985],gamma_3FGL.y[985])),\
                   ((gamma_3FGL.x[996],gamma_3FGL.y[996]),(gamma_3FGL.x[999],gamma_3FGL.y[999])),\
                   ((gamma_3FGL.x[999],gamma_3FGL.y[999]),(gamma_3FGL.x[1015],gamma_3FGL.y[1015])),\
                   ((gamma_3FGL.x[1015],gamma_3FGL.y[1015]),(gamma_3FGL.x[1269],gamma_3FGL.y[1269])),\
                   ((gamma_3FGL.x[1268],gamma_3FGL.y[1268]),(gamma_3FGL.x[1269],gamma_3FGL.y[1269])),\
                   ((gamma_3FGL.x[2545],gamma_3FGL.y[2545]),(gamma_3FGL.x[2547],gamma_3FGL.y[2547]))]
                   #((gamma_3FGL.x[1618],gamma_3FGL.y[1618]),(gamma_3FGL.x[],gamma_3FGL.y[])),\
                   #((gamma_3FGL.x[721],gamma_3FGL.y[721]),(gamma_3FGL.x[],gamma_3FGL.y[])),\
                   #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[722],gamma_3FGL.y[722])),\
                   #((gamma_3FGL.x[987],gamma_3FGL.y[987]),(gamma_3FGL.x[],gamma_3FGL.y[])),\
                                                                                                   
Godzilla = [((gamma_3FGL.x[38],gamma_3FGL.y[38]),(gamma_3FGL.x[959],gamma_3FGL.y[959])),\
            ((gamma_3FGL.x[38],gamma_3FGL.y[38]),(gamma_3FGL.x[2303],gamma_3FGL.y[2303])),\
            ((gamma_3FGL.x[534],gamma_3FGL.y[534]),(gamma_3FGL.x[2149],gamma_3FGL.y[2149])),\
            ((gamma_3FGL.x[534],gamma_3FGL.y[534]),(gamma_3FGL.x[2567],gamma_3FGL.y[2567])),\
            ((gamma_3FGL.x[607],gamma_3FGL.y[607]),(gamma_3FGL.x[608],gamma_3FGL.y[608])),\
            ((gamma_3FGL.x[607],gamma_3FGL.y[607]),(gamma_3FGL.x[1739],gamma_3FGL.y[1739])),\
            ((gamma_3FGL.x[608],gamma_3FGL.y[608]),(gamma_3FGL.x[1740],gamma_3FGL.y[1740])),\
            ((gamma_3FGL.x[632],gamma_3FGL.y[632]),(gamma_3FGL.x[633],gamma_3FGL.y[633])),\
            ((gamma_3FGL.x[632],gamma_3FGL.y[632]),(gamma_3FGL.x[634],gamma_3FGL.y[634])),\
            ((gamma_3FGL.x[633],gamma_3FGL.y[633]),(gamma_3FGL.x[639],gamma_3FGL.y[639])),\
            ((gamma_3FGL.x[634],gamma_3FGL.y[634]),(gamma_3FGL.x[635],gamma_3FGL.y[635])),\
            ((gamma_3FGL.x[635],gamma_3FGL.y[635]),(gamma_3FGL.x[636],gamma_3FGL.y[636])),\
            ((gamma_3FGL.x[636],gamma_3FGL.y[636]),(gamma_3FGL.x[1437],gamma_3FGL.y[1437])),\
            ((gamma_3FGL.x[639],gamma_3FGL.y[639]),(gamma_3FGL.x[1467],gamma_3FGL.y[1467])),\
            ((gamma_3FGL.x[684],gamma_3FGL.y[684]),(gamma_3FGL.x[685],gamma_3FGL.y[685])),\
            ((gamma_3FGL.x[684],gamma_3FGL.y[684]),(gamma_3FGL.x[1414],gamma_3FGL.y[1414])),\
            ((gamma_3FGL.x[685],gamma_3FGL.y[685]),(gamma_3FGL.x[1417],gamma_3FGL.y[1417])),\
            ((gamma_3FGL.x[686],gamma_3FGL.y[686]),(gamma_3FGL.x[1437],gamma_3FGL.y[1437])),\
            ((gamma_3FGL.x[686],gamma_3FGL.y[686]),(gamma_3FGL.x[2448],gamma_3FGL.y[2448])),\
            ((gamma_3FGL.x[692],gamma_3FGL.y[692]),(gamma_3FGL.x[1001],gamma_3FGL.y[1001])),\
            ((gamma_3FGL.x[692],gamma_3FGL.y[692]),(gamma_3FGL.x[2334],gamma_3FGL.y[2334])),\
            ((gamma_3FGL.x[959],gamma_3FGL.y[959]),(gamma_3FGL.x[960],gamma_3FGL.y[960])),\
            ((gamma_3FGL.x[960],gamma_3FGL.y[960]),(gamma_3FGL.x[1626],gamma_3FGL.y[1626])),\
            ((gamma_3FGL.x[1000],gamma_3FGL.y[1000]),(gamma_3FGL.x[1001],gamma_3FGL.y[1001])),\
            ((gamma_3FGL.x[1000],gamma_3FGL.y[1000]),(gamma_3FGL.x[1468],gamma_3FGL.y[1468])),\
            ((gamma_3FGL.x[1112],gamma_3FGL.y[1112]),(gamma_3FGL.x[1113],gamma_3FGL.y[1113])),\
            ((gamma_3FGL.x[1112],gamma_3FGL.y[1112]),(gamma_3FGL.x[2239],gamma_3FGL.y[2239])),\
            ((gamma_3FGL.x[1113],gamma_3FGL.y[1113]),(gamma_3FGL.x[1395],gamma_3FGL.y[1395])),\
            ((gamma_3FGL.x[1131],gamma_3FGL.y[1131]),(gamma_3FGL.x[1133],gamma_3FGL.y[1133])),\
            ((gamma_3FGL.x[1131],gamma_3FGL.y[1131]),(gamma_3FGL.x[1396],gamma_3FGL.y[1396])),\
            ((gamma_3FGL.x[1133],gamma_3FGL.y[1133]),(gamma_3FGL.x[1422],gamma_3FGL.y[1422])),\
            ((gamma_3FGL.x[1135],gamma_3FGL.y[1135]),(gamma_3FGL.x[1137],gamma_3FGL.y[1137])),\
            ((gamma_3FGL.x[1135],gamma_3FGL.y[1135]),(gamma_3FGL.x[1830],gamma_3FGL.y[1830])),\
            ((gamma_3FGL.x[1137],gamma_3FGL.y[1137]),(gamma_3FGL.x[2334],gamma_3FGL.y[2334])),\
            ((gamma_3FGL.x[1140],gamma_3FGL.y[1140]),(gamma_3FGL.x[1141],gamma_3FGL.y[1141])),\
            ((gamma_3FGL.x[1140],gamma_3FGL.y[1140]),(gamma_3FGL.x[1400],gamma_3FGL.y[1400])),\
            ((gamma_3FGL.x[1141],gamma_3FGL.y[1141]),(gamma_3FGL.x[1142],gamma_3FGL.y[1142])),\
            ((gamma_3FGL.x[1142],gamma_3FGL.y[1142]),(gamma_3FGL.x[1145],gamma_3FGL.y[1145])),\
            ((gamma_3FGL.x[1143],gamma_3FGL.y[1143]),(gamma_3FGL.x[1144],gamma_3FGL.y[1144])),\
            ((gamma_3FGL.x[1144],gamma_3FGL.y[1144]),(gamma_3FGL.x[1145],gamma_3FGL.y[1145])),\
            ((gamma_3FGL.x[1351],gamma_3FGL.y[1351]),(gamma_3FGL.x[1787],gamma_3FGL.y[1787])),\
            ((gamma_3FGL.x[1351],gamma_3FGL.y[1351]),(gamma_3FGL.x[2448],gamma_3FGL.y[2448])),\
            ((gamma_3FGL.x[1394],gamma_3FGL.y[1394]),(gamma_3FGL.x[1400],gamma_3FGL.y[1400])),\
            ((gamma_3FGL.x[1394],gamma_3FGL.y[1394]),(gamma_3FGL.x[1602],gamma_3FGL.y[1602])),\
            ((gamma_3FGL.x[1395],gamma_3FGL.y[1395]),(gamma_3FGL.x[1396],gamma_3FGL.y[1396])),\
            ((gamma_3FGL.x[1414],gamma_3FGL.y[1414]),(gamma_3FGL.x[1415],gamma_3FGL.y[1415])),\
            ((gamma_3FGL.x[1416],gamma_3FGL.y[1416]),(gamma_3FGL.x[1418],gamma_3FGL.y[1418])),\
            ((gamma_3FGL.x[1417],gamma_3FGL.y[1417]),(gamma_3FGL.x[1418],gamma_3FGL.y[1418])),\
            ((gamma_3FGL.x[1422],gamma_3FGL.y[1422]),(gamma_3FGL.x[1143],gamma_3FGL.y[1143])),\
            ((gamma_3FGL.x[1467],gamma_3FGL.y[1467]),(gamma_3FGL.x[1468],gamma_3FGL.y[1468])),\
            ((gamma_3FGL.x[1601],gamma_3FGL.y[1601]),(gamma_3FGL.x[1603],gamma_3FGL.y[1603])),\
            ((gamma_3FGL.x[1601],gamma_3FGL.y[1601]),(gamma_3FGL.x[2306],gamma_3FGL.y[2306])),\
            ((gamma_3FGL.x[1602],gamma_3FGL.y[1602]),(gamma_3FGL.x[1603],gamma_3FGL.y[1603])),\
            ((gamma_3FGL.x[1626],gamma_3FGL.y[1626]),(gamma_3FGL.x[1628],gamma_3FGL.y[1628])),\
            ((gamma_3FGL.x[1628],gamma_3FGL.y[1628]),(gamma_3FGL.x[2150],gamma_3FGL.y[2150])),\
            ((gamma_3FGL.x[1628],gamma_3FGL.y[1628]),(gamma_3FGL.x[2889],gamma_3FGL.y[2889])),\
            ((gamma_3FGL.x[1739],gamma_3FGL.y[1739]),(gamma_3FGL.x[1856],gamma_3FGL.y[1856])),\
            ((gamma_3FGL.x[1740],gamma_3FGL.y[1740]),(gamma_3FGL.x[1742],gamma_3FGL.y[1742])),\
            ((gamma_3FGL.x[1741],gamma_3FGL.y[1741]),(gamma_3FGL.x[1742],gamma_3FGL.y[1742])),\
            ((gamma_3FGL.x[1741],gamma_3FGL.y[1741]),(gamma_3FGL.x[2182],gamma_3FGL.y[2182])),\
            ((gamma_3FGL.x[1781],gamma_3FGL.y[1781]),(gamma_3FGL.x[1782],gamma_3FGL.y[1782])),\
            ((gamma_3FGL.x[1781],gamma_3FGL.y[1781]),(gamma_3FGL.x[2567],gamma_3FGL.y[2567])),\
            ((gamma_3FGL.x[1782],gamma_3FGL.y[1782]),(gamma_3FGL.x[1784],gamma_3FGL.y[1784])),\
            ((gamma_3FGL.x[1784],gamma_3FGL.y[1784]),(gamma_3FGL.x[1787],gamma_3FGL.y[1787])),\
            ((gamma_3FGL.x[1826],gamma_3FGL.y[1826]),(gamma_3FGL.x[1830],gamma_3FGL.y[1830])),\
            ((gamma_3FGL.x[1826],gamma_3FGL.y[1826]),(gamma_3FGL.x[2239],gamma_3FGL.y[2239])),\
            ((gamma_3FGL.x[1855],gamma_3FGL.y[1855]),(gamma_3FGL.x[2182],gamma_3FGL.y[2182])),\
            ((gamma_3FGL.x[1856],gamma_3FGL.y[1856]),(gamma_3FGL.x[1857],gamma_3FGL.y[1857])),\
            ((gamma_3FGL.x[2303],gamma_3FGL.y[2303]),(gamma_3FGL.x[2306],gamma_3FGL.y[2306])),\
            ((gamma_3FGL.x[2149],gamma_3FGL.y[2149]),(gamma_3FGL.x[2150],gamma_3FGL.y[2150])),\
            ((gamma_3FGL.x[2889],gamma_3FGL.y[2889]),(gamma_3FGL.x[2891],gamma_3FGL.y[2891]))]

Golden_Gate = [((gamma_3FGL.x[727],gamma_3FGL.y[727]),(gamma_3FGL.x[2048],gamma_3FGL.y[2048])),\
               ((gamma_3FGL.x[727],gamma_3FGL.y[727]),(gamma_3FGL.x[2049],gamma_3FGL.y[2049])),\
               ((gamma_3FGL.x[727],gamma_3FGL.y[727]),(gamma_3FGL.x[2946],gamma_3FGL.y[2946])),\
               ((gamma_3FGL.x[746],gamma_3FGL.y[746]),(gamma_3FGL.x[1258],gamma_3FGL.y[1258])),\
               ((gamma_3FGL.x[1215],gamma_3FGL.y[1215]),(gamma_3FGL.x[1217],gamma_3FGL.y[1217])),\
               ((gamma_3FGL.x[1215],gamma_3FGL.y[1215]),(gamma_3FGL.x[1711],gamma_3FGL.y[1711])),\
               ((gamma_3FGL.x[1215],gamma_3FGL.y[1215]),(gamma_3FGL.x[2048],gamma_3FGL.y[2048])),\
               ((gamma_3FGL.x[1217],gamma_3FGL.y[1217]),(gamma_3FGL.x[1707],gamma_3FGL.y[1707])),\
               ((gamma_3FGL.x[1217],gamma_3FGL.y[1217]),(gamma_3FGL.x[1710],gamma_3FGL.y[1710])),\
               ((gamma_3FGL.x[1217],gamma_3FGL.y[1217]),(gamma_3FGL.x[2017],gamma_3FGL.y[2017])),\
               ((gamma_3FGL.x[1258],gamma_3FGL.y[1258]),(gamma_3FGL.x[1259],gamma_3FGL.y[1259])),\
               ((gamma_3FGL.x[1258],gamma_3FGL.y[1258]),(gamma_3FGL.x[1263],gamma_3FGL.y[1263])),\
               ((gamma_3FGL.x[1258],gamma_3FGL.y[1258]),(gamma_3FGL.x[1943],gamma_3FGL.y[1943])),\
               ((gamma_3FGL.x[1259],gamma_3FGL.y[1259]),(gamma_3FGL.x[1262],gamma_3FGL.y[1262])),\
               ((gamma_3FGL.x[1259],gamma_3FGL.y[1259]),(gamma_3FGL.x[1329],gamma_3FGL.y[1329])),\
               ((gamma_3FGL.x[1259],gamma_3FGL.y[1259]),(gamma_3FGL.x[2947],gamma_3FGL.y[2947])),\
               ((gamma_3FGL.x[1262],gamma_3FGL.y[1262]),(gamma_3FGL.x[2707],gamma_3FGL.y[2707])),\
               ((gamma_3FGL.x[1263],gamma_3FGL.y[1263]),(gamma_3FGL.x[1519],gamma_3FGL.y[1519])),\
               ((gamma_3FGL.x[1329],gamma_3FGL.y[1329]),(gamma_3FGL.x[2059],gamma_3FGL.y[2059])),\
               ((gamma_3FGL.x[1519],gamma_3FGL.y[1519]),(gamma_3FGL.x[2058],gamma_3FGL.y[2058])),\
               ((gamma_3FGL.x[1608],gamma_3FGL.y[1608]),(gamma_3FGL.x[2705],gamma_3FGL.y[2705])),\
               ((gamma_3FGL.x[1707],gamma_3FGL.y[1707]),(gamma_3FGL.x[2049],gamma_3FGL.y[2049])),\
               ((gamma_3FGL.x[1710],gamma_3FGL.y[1710]),(gamma_3FGL.x[1711],gamma_3FGL.y[1711])),\
               ((gamma_3FGL.x[1710],gamma_3FGL.y[1710]),(gamma_3FGL.x[2017],gamma_3FGL.y[2017])),\
               ((gamma_3FGL.x[1712],gamma_3FGL.y[1712]),(gamma_3FGL.x[1711],gamma_3FGL.y[1711])),\
               ((gamma_3FGL.x[1712],gamma_3FGL.y[1712]),(gamma_3FGL.x[1714],gamma_3FGL.y[1714])),\
               ((gamma_3FGL.x[1775],gamma_3FGL.y[1775]),(gamma_3FGL.x[2707],gamma_3FGL.y[2707])),\
               ((gamma_3FGL.x[1943],gamma_3FGL.y[1943]),(gamma_3FGL.x[2705],gamma_3FGL.y[2705])),\
               ((gamma_3FGL.x[1946],gamma_3FGL.y[1946]),(gamma_3FGL.x[2946],gamma_3FGL.y[2946])),\
               ((gamma_3FGL.x[2017],gamma_3FGL.y[2017]),(gamma_3FGL.x[2049],gamma_3FGL.y[2049])),\
               ((gamma_3FGL.x[2017],gamma_3FGL.y[2017]),(gamma_3FGL.x[2636],gamma_3FGL.y[2636])),\
               ((gamma_3FGL.x[2047],gamma_3FGL.y[2047]),(gamma_3FGL.x[2049],gamma_3FGL.y[2049])),\
               ((gamma_3FGL.x[2047],gamma_3FGL.y[2047]),(gamma_3FGL.x[2059],gamma_3FGL.y[2059])),\
               ((gamma_3FGL.x[2048],gamma_3FGL.y[2048]),(gamma_3FGL.x[2049],gamma_3FGL.y[2049])),\
               ((gamma_3FGL.x[2048],gamma_3FGL.y[2048]),(gamma_3FGL.x[2060],gamma_3FGL.y[2060])),\
               ((gamma_3FGL.x[2058],gamma_3FGL.y[2058]),(gamma_3FGL.x[2060],gamma_3FGL.y[2060])),\
               ((gamma_3FGL.x[2636],gamma_3FGL.y[2636]),(gamma_3FGL.x[2637],gamma_3FGL.y[2637])),\
               ((gamma_3FGL.x[2637],gamma_3FGL.y[2637]),(gamma_3FGL.x[2639],gamma_3FGL.y[2639]))]
               #((gamma_3FGL.x[1710],gamma_3FGL.y[1710]),(gamma_3FGL.x[],gamma_3FGL.y[])),\
               #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[1711],gamma_3FGL.y[1711])),\
               #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[2947],gamma_3FGL.y[2947])),\

Hulk = [((gamma_3FGL.x[824],gamma_3FGL.y[824]),(gamma_3FGL.x[825],gamma_3FGL.y[825])),\
        ((gamma_3FGL.x[824],gamma_3FGL.y[824]),(gamma_3FGL.x[1549],gamma_3FGL.y[1549])),\
        ((gamma_3FGL.x[825],gamma_3FGL.y[825]),(gamma_3FGL.x[2622],gamma_3FGL.y[2622])),\
        ((gamma_3FGL.x[1226],gamma_3FGL.y[1226]),(gamma_3FGL.x[1227],gamma_3FGL.y[1227])),\
        ((gamma_3FGL.x[1226],gamma_3FGL.y[1226]),(gamma_3FGL.x[1531],gamma_3FGL.y[1531])),\
        ((gamma_3FGL.x[1227],gamma_3FGL.y[1227]),(gamma_3FGL.x[2222],gamma_3FGL.y[2222])),\
        ((gamma_3FGL.x[1230],gamma_3FGL.y[1230]),(gamma_3FGL.x[1532],gamma_3FGL.y[1532])),\
        ((gamma_3FGL.x[1230],gamma_3FGL.y[1230]),(gamma_3FGL.x[2410],gamma_3FGL.y[2410])),\
        ((gamma_3FGL.x[1531],gamma_3FGL.y[1531]),(gamma_3FGL.x[2387],gamma_3FGL.y[2387])),\
        ((gamma_3FGL.x[1532],gamma_3FGL.y[1532]),(gamma_3FGL.x[1566],gamma_3FGL.y[1566])),\
        ((gamma_3FGL.x[1549],gamma_3FGL.y[1549]),(gamma_3FGL.x[2236],gamma_3FGL.y[2236])),\
        ((gamma_3FGL.x[1565],gamma_3FGL.y[1565]),(gamma_3FGL.x[1566],gamma_3FGL.y[1566])),\
        ((gamma_3FGL.x[1565],gamma_3FGL.y[1565]),(gamma_3FGL.x[2386],gamma_3FGL.y[2386])),\
        ((gamma_3FGL.x[1629],gamma_3FGL.y[1629]),(gamma_3FGL.x[1630],gamma_3FGL.y[1630])),\
        ((gamma_3FGL.x[1629],gamma_3FGL.y[1629]),(gamma_3FGL.x[2409],gamma_3FGL.y[2409])),\
        ((gamma_3FGL.x[1630],gamma_3FGL.y[1630]),(gamma_3FGL.x[1631],gamma_3FGL.y[1631])),\
        ((gamma_3FGL.x[1631],gamma_3FGL.y[1631]),(gamma_3FGL.x[2238],gamma_3FGL.y[2238])),\
        ((gamma_3FGL.x[1772],gamma_3FGL.y[1772]),(gamma_3FGL.x[1774],gamma_3FGL.y[1774])),\
        ((gamma_3FGL.x[1772],gamma_3FGL.y[1772]),(gamma_3FGL.x[1933],gamma_3FGL.y[1933])),\
        ((gamma_3FGL.x[1773],gamma_3FGL.y[1773]),(gamma_3FGL.x[1774],gamma_3FGL.y[1774])),\
        ((gamma_3FGL.x[1773],gamma_3FGL.y[1773]),(gamma_3FGL.x[2582],gamma_3FGL.y[2582])),\
        ((gamma_3FGL.x[1894],gamma_3FGL.y[1894]),(gamma_3FGL.x[1895],gamma_3FGL.y[1895])),\
        ((gamma_3FGL.x[1895],gamma_3FGL.y[1895]),(gamma_3FGL.x[2222],gamma_3FGL.y[2222])),\
        ((gamma_3FGL.x[1929],gamma_3FGL.y[1929]),(gamma_3FGL.x[1932],gamma_3FGL.y[1932])),\
        ((gamma_3FGL.x[1929],gamma_3FGL.y[1929]),(gamma_3FGL.x[2822],gamma_3FGL.y[2822])),\
        ((gamma_3FGL.x[1930],gamma_3FGL.y[1930]),(gamma_3FGL.x[1933],gamma_3FGL.y[1933])),\
        ((gamma_3FGL.x[1930],gamma_3FGL.y[1930]),(gamma_3FGL.x[2577],gamma_3FGL.y[2577])),\
        ((gamma_3FGL.x[1932],gamma_3FGL.y[1932]),(gamma_3FGL.x[1934],gamma_3FGL.y[1934])),\
        ((gamma_3FGL.x[1933],gamma_3FGL.y[1933]),(gamma_3FGL.x[1934],gamma_3FGL.y[1934])),\
        ((gamma_3FGL.x[2119],gamma_3FGL.y[2119]),(gamma_3FGL.x[1894],gamma_3FGL.y[1894])),\
        ((gamma_3FGL.x[2119],gamma_3FGL.y[2119]),(gamma_3FGL.x[2497],gamma_3FGL.y[2497])),\
        ((gamma_3FGL.x[2223],gamma_3FGL.y[2223]),(gamma_3FGL.x[2409],gamma_3FGL.y[2409])),\
        ((gamma_3FGL.x[2223],gamma_3FGL.y[2223]),(gamma_3FGL.x[2499],gamma_3FGL.y[2499])),\
        ((gamma_3FGL.x[2233],gamma_3FGL.y[2233]),(gamma_3FGL.x[2234],gamma_3FGL.y[2234])),\
        ((gamma_3FGL.x[2233],gamma_3FGL.y[2233]),(gamma_3FGL.x[2235],gamma_3FGL.y[2235])),\
        ((gamma_3FGL.x[2234],gamma_3FGL.y[2234]),(gamma_3FGL.x[2237],gamma_3FGL.y[2237])),\
        ((gamma_3FGL.x[2235],gamma_3FGL.y[2235]),(gamma_3FGL.x[2236],gamma_3FGL.y[2236])),\
        ((gamma_3FGL.x[2237],gamma_3FGL.y[2237]),(gamma_3FGL.x[2238],gamma_3FGL.y[2238])),\
        ((gamma_3FGL.x[2386],gamma_3FGL.y[2386]),(gamma_3FGL.x[2387],gamma_3FGL.y[2387])),\
        ((gamma_3FGL.x[2410],gamma_3FGL.y[2410]),(gamma_3FGL.x[2819],gamma_3FGL.y[2819])),\
        ((gamma_3FGL.x[2497],gamma_3FGL.y[2497]),(gamma_3FGL.x[2498],gamma_3FGL.y[2498])),\
        ((gamma_3FGL.x[2498],gamma_3FGL.y[2498]),(gamma_3FGL.x[2499],gamma_3FGL.y[2499])),\
        ((gamma_3FGL.x[2577],gamma_3FGL.y[2577]),(gamma_3FGL.x[2579],gamma_3FGL.y[2579])),\
        ((gamma_3FGL.x[2579],gamma_3FGL.y[2579]),(gamma_3FGL.x[2582],gamma_3FGL.y[2582])),\
        ((gamma_3FGL.x[2580],gamma_3FGL.y[2580]),(gamma_3FGL.x[2581],gamma_3FGL.y[2581])),\
        ((gamma_3FGL.x[2580],gamma_3FGL.y[2580]),(gamma_3FGL.x[2622],gamma_3FGL.y[2622])),\
        ((gamma_3FGL.x[2581],gamma_3FGL.y[2581]),(gamma_3FGL.x[2582],gamma_3FGL.y[2582])),\
        ((gamma_3FGL.x[2784],gamma_3FGL.y[2784]),(gamma_3FGL.x[2785],gamma_3FGL.y[2785])),\
        ((gamma_3FGL.x[2784],gamma_3FGL.y[2784]),(gamma_3FGL.x[2788],gamma_3FGL.y[2788])),\
        ((gamma_3FGL.x[2785],gamma_3FGL.y[2785]),(gamma_3FGL.x[2786],gamma_3FGL.y[2786])),\
        ((gamma_3FGL.x[2786],gamma_3FGL.y[2786]),(gamma_3FGL.x[2787],gamma_3FGL.y[2787])),\
        ((gamma_3FGL.x[2788],gamma_3FGL.y[2788]),(gamma_3FGL.x[2820],gamma_3FGL.y[2820])),\
        ((gamma_3FGL.x[2819],gamma_3FGL.y[2819]),(gamma_3FGL.x[2821],gamma_3FGL.y[2821])),\
        ((gamma_3FGL.x[2820],gamma_3FGL.y[2820]),(gamma_3FGL.x[2822],gamma_3FGL.y[2822]))]
        #((gamma_3FGL.x[1773],gamma_3FGL.y[1773]),(gamma_3FGL.x[],gamma_3FGL.y[]))]

The_Little_Prince = [((gamma_3FGL.x[627],gamma_3FGL.y[627]),(gamma_3FGL.x[1581],gamma_3FGL.y[1581])),\
                     ((gamma_3FGL.x[627],gamma_3FGL.y[627]),(gamma_3FGL.x[2839],gamma_3FGL.y[2839])),\
                     ((gamma_3FGL.x[1019],gamma_3FGL.y[1019]),(gamma_3FGL.x[2163],gamma_3FGL.y[2163])),\
                     ((gamma_3FGL.x[1019],gamma_3FGL.y[1019]),(gamma_3FGL.x[2840],gamma_3FGL.y[2840])),\
                     ((gamma_3FGL.x[1176],gamma_3FGL.y[1176]),(gamma_3FGL.x[1178],gamma_3FGL.y[1178])),\
                     ((gamma_3FGL.x[1177],gamma_3FGL.y[1177]),(gamma_3FGL.x[1178],gamma_3FGL.y[1178])),\
                     ((gamma_3FGL.x[1179],gamma_3FGL.y[1179]),(gamma_3FGL.x[1180],gamma_3FGL.y[1180])),\
                     ((gamma_3FGL.x[1179],gamma_3FGL.y[1179]),(gamma_3FGL.x[1443],gamma_3FGL.y[1443])),\
                     ((gamma_3FGL.x[1180],gamma_3FGL.y[1180]),(gamma_3FGL.x[1464],gamma_3FGL.y[1464])),\
                     ((gamma_3FGL.x[1443],gamma_3FGL.y[1443]),(gamma_3FGL.x[2199],gamma_3FGL.y[2199])),\
                     ((gamma_3FGL.x[1464],gamma_3FGL.y[1464]),(gamma_3FGL.x[2344],gamma_3FGL.y[2344])),\
                     ((gamma_3FGL.x[2163],gamma_3FGL.y[2163]),(gamma_3FGL.x[2164],gamma_3FGL.y[2164])),\
                     ((gamma_3FGL.x[2164],gamma_3FGL.y[2164]),(gamma_3FGL.x[2839],gamma_3FGL.y[2839])),\
                     ((gamma_3FGL.x[2199],gamma_3FGL.y[2199]),(gamma_3FGL.x[2583],gamma_3FGL.y[2583])),\
                     ((gamma_3FGL.x[2353],gamma_3FGL.y[2353]),(gamma_3FGL.x[2583],gamma_3FGL.y[2583])),\
                     ((gamma_3FGL.x[2344],gamma_3FGL.y[2344]),(gamma_3FGL.x[2371],gamma_3FGL.y[2371])),\
                     ((gamma_3FGL.x[2368],gamma_3FGL.y[2368]),(gamma_3FGL.x[2370],gamma_3FGL.y[2370])),\
                     ((gamma_3FGL.x[2370],gamma_3FGL.y[2370]),(gamma_3FGL.x[2371],gamma_3FGL.y[2371])),\
                     ((gamma_3FGL.x[2371],gamma_3FGL.y[2371]),(gamma_3FGL.x[2372],gamma_3FGL.y[2372])),\
                     ((gamma_3FGL.x[2583],gamma_3FGL.y[2583]),(gamma_3FGL.x[2840],gamma_3FGL.y[2840])),\
                     ((gamma_3FGL.x[2839],gamma_3FGL.y[2839]),(gamma_3FGL.x[2840],gamma_3FGL.y[2840]))]
                     #((gamma_3FGL.x[627],gamma_3FGL.y[627]),(gamma_3FGL.x[],gamma_3FGL.y[])),\

Mjolnir = [((gamma_3FGL.x[728],gamma_3FGL.y[728]),(gamma_3FGL.x[729],gamma_3FGL.y[729])),\
           ((gamma_3FGL.x[728],gamma_3FGL.y[728]),(gamma_3FGL.x[730],gamma_3FGL.y[730])),\
           ((gamma_3FGL.x[728],gamma_3FGL.y[728]),(gamma_3FGL.x[1283],gamma_3FGL.y[1283])),\
           ((gamma_3FGL.x[729],gamma_3FGL.y[729]),(gamma_3FGL.x[1283],gamma_3FGL.y[1283])),\
           ((gamma_3FGL.x[729],gamma_3FGL.y[729]),(gamma_3FGL.x[2317],gamma_3FGL.y[2317])),\
           ((gamma_3FGL.x[730],gamma_3FGL.y[730]),(gamma_3FGL.x[2316],gamma_3FGL.y[2316])),\
           ((gamma_3FGL.x[889],gamma_3FGL.y[889]),(gamma_3FGL.x[1288],gamma_3FGL.y[1288])),\
           ((gamma_3FGL.x[889],gamma_3FGL.y[889]),(gamma_3FGL.x[1484],gamma_3FGL.y[1484])),\
           ((gamma_3FGL.x[1283],gamma_3FGL.y[1283]),(gamma_3FGL.x[1284],gamma_3FGL.y[1284])),\
           ((gamma_3FGL.x[1284],gamma_3FGL.y[1284]),(gamma_3FGL.x[1576],gamma_3FGL.y[1576])),\
           ((gamma_3FGL.x[1285],gamma_3FGL.y[1285]),(gamma_3FGL.x[1666],gamma_3FGL.y[1666])),\
           ((gamma_3FGL.x[1288],gamma_3FGL.y[1288]),(gamma_3FGL.x[1668],gamma_3FGL.y[1668])),\
           ((gamma_3FGL.x[1484],gamma_3FGL.y[1484]),(gamma_3FGL.x[2285],gamma_3FGL.y[2285])),\
           ((gamma_3FGL.x[1576],gamma_3FGL.y[1576]),(gamma_3FGL.x[1578],gamma_3FGL.y[1578])),\
           ((gamma_3FGL.x[1666],gamma_3FGL.y[1666]),(gamma_3FGL.x[1669],gamma_3FGL.y[1669])),\
           ((gamma_3FGL.x[1667],gamma_3FGL.y[1667]),(gamma_3FGL.x[1668],gamma_3FGL.y[1668])),\
           ((gamma_3FGL.x[1667],gamma_3FGL.y[1667]),(gamma_3FGL.x[1669],gamma_3FGL.y[1669])),\
           ((gamma_3FGL.x[1732],gamma_3FGL.y[1732]),(gamma_3FGL.x[2070],gamma_3FGL.y[2070])),\
           ((gamma_3FGL.x[1732],gamma_3FGL.y[1732]),(gamma_3FGL.x[2287],gamma_3FGL.y[2287])),\
           ((gamma_3FGL.x[1998],gamma_3FGL.y[1998]),(gamma_3FGL.x[1999],gamma_3FGL.y[1999])),\
           ((gamma_3FGL.x[1998],gamma_3FGL.y[1998]),(gamma_3FGL.x[2068],gamma_3FGL.y[2068])),\
           ((gamma_3FGL.x[1998],gamma_3FGL.y[1998]),(gamma_3FGL.x[2317],gamma_3FGL.y[2317])),\
           ((gamma_3FGL.x[2068],gamma_3FGL.y[2068]),(gamma_3FGL.x[2287],gamma_3FGL.y[2287])),\
           ((gamma_3FGL.x[2285],gamma_3FGL.y[2285]),(gamma_3FGL.x[2287],gamma_3FGL.y[2287]))]
           #((gamma_3FGL.x[1285],gamma_3FGL.y[1285]),(gamma_3FGL.x[],gamma_3FGL.y[])),\

Mount_Fuji = [((gamma_3FGL.x[47],gamma_3FGL.y[47]),(gamma_3FGL.x[50],gamma_3FGL.y[50])),\
              ((gamma_3FGL.x[47],gamma_3FGL.y[47]),(gamma_3FGL.x[1309],gamma_3FGL.y[1309])),\
              ((gamma_3FGL.x[50],gamma_3FGL.y[50]),(gamma_3FGL.x[755],gamma_3FGL.y[755])),\
              ((gamma_3FGL.x[755],gamma_3FGL.y[755]),(gamma_3FGL.x[757],gamma_3FGL.y[757])),\
              ((gamma_3FGL.x[757],gamma_3FGL.y[757]),(gamma_3FGL.x[761],gamma_3FGL.y[761])),\
              ((gamma_3FGL.x[761],gamma_3FGL.y[761]),(gamma_3FGL.x[762],gamma_3FGL.y[762])),\
              ((gamma_3FGL.x[762],gamma_3FGL.y[762]),(gamma_3FGL.x[1024],gamma_3FGL.y[1024])),\
              ((gamma_3FGL.x[1024],gamma_3FGL.y[1024]),(gamma_3FGL.x[2674],gamma_3FGL.y[2674])),\
              ((gamma_3FGL.x[1027],gamma_3FGL.y[1027]),(gamma_3FGL.x[1030],gamma_3FGL.y[1030])),\
              ((gamma_3FGL.x[1027],gamma_3FGL.y[1027]),(gamma_3FGL.x[1309],gamma_3FGL.y[1309])),\
              ((gamma_3FGL.x[1027],gamma_3FGL.y[1027]),(gamma_3FGL.x[1321],gamma_3FGL.y[1321])),\
              ((gamma_3FGL.x[1030],gamma_3FGL.y[1030]),(gamma_3FGL.x[2035],gamma_3FGL.y[2035])),\
              ((gamma_3FGL.x[1042],gamma_3FGL.y[1042]),(gamma_3FGL.x[1043],gamma_3FGL.y[1043])),\
              ((gamma_3FGL.x[1042],gamma_3FGL.y[1042]),(gamma_3FGL.x[2951],gamma_3FGL.y[2951])),\
              ((gamma_3FGL.x[1043],gamma_3FGL.y[1043]),(gamma_3FGL.x[1328],gamma_3FGL.y[1328])),\
              ((gamma_3FGL.x[1319],gamma_3FGL.y[1319]),(gamma_3FGL.x[1321],gamma_3FGL.y[1321])),\
              ((gamma_3FGL.x[1319],gamma_3FGL.y[1319]),(gamma_3FGL.x[1322],gamma_3FGL.y[1322])),\
              ((gamma_3FGL.x[1322],gamma_3FGL.y[1322]),(gamma_3FGL.x[2933],gamma_3FGL.y[2933])),\
              ((gamma_3FGL.x[1328],gamma_3FGL.y[1328]),(gamma_3FGL.x[2674],gamma_3FGL.y[2674])),\
              ((gamma_3FGL.x[2035],gamma_3FGL.y[2035]),(gamma_3FGL.x[2036],gamma_3FGL.y[2036])),\
              ((gamma_3FGL.x[2036],gamma_3FGL.y[2036]),(gamma_3FGL.x[2702],gamma_3FGL.y[2702])),\
              ((gamma_3FGL.x[2698],gamma_3FGL.y[2698]),(gamma_3FGL.x[2699],gamma_3FGL.y[2699])),\
              ((gamma_3FGL.x[2698],gamma_3FGL.y[2698]),(gamma_3FGL.x[2952],gamma_3FGL.y[2952])),\
              ((gamma_3FGL.x[2699],gamma_3FGL.y[2699]),(gamma_3FGL.x[2934],gamma_3FGL.y[2934])),\
              ((gamma_3FGL.x[2700],gamma_3FGL.y[2700]),(gamma_3FGL.x[2702],gamma_3FGL.y[2702])),\
              ((gamma_3FGL.x[2700],gamma_3FGL.y[2700]),(gamma_3FGL.x[2951],gamma_3FGL.y[2951])),\
              ((gamma_3FGL.x[2933],gamma_3FGL.y[2933]),(gamma_3FGL.x[2935],gamma_3FGL.y[2935])),\
              ((gamma_3FGL.x[2934],gamma_3FGL.y[2934]),(gamma_3FGL.x[2935],gamma_3FGL.y[2935])),\
              ((gamma_3FGL.x[2951],gamma_3FGL.y[2951]),(gamma_3FGL.x[2952],gamma_3FGL.y[2952]))]

Castle = [((gamma_3FGL.x[2],gamma_3FGL.y[2]),(gamma_3FGL.x[892],gamma_3FGL.y[892])),\
          ((gamma_3FGL.x[24],gamma_3FGL.y[24]),(gamma_3FGL.x[1606],gamma_3FGL.y[1606])),\
          ((gamma_3FGL.x[74],gamma_3FGL.y[74]),(gamma_3FGL.x[95],gamma_3FGL.y[95])),\
          ((gamma_3FGL.x[95],gamma_3FGL.y[95]),(gamma_3FGL.x[1291],gamma_3FGL.y[1291])),\
          ((gamma_3FGL.x[308],gamma_3FGL.y[308]),(gamma_3FGL.x[375],gamma_3FGL.y[375])),\
          ((gamma_3FGL.x[308],gamma_3FGL.y[308]),(gamma_3FGL.x[449],gamma_3FGL.y[449])),\
          ((gamma_3FGL.x[308],gamma_3FGL.y[308]),(gamma_3FGL.x[2969],gamma_3FGL.y[2969])),\
          ((gamma_3FGL.x[373],gamma_3FGL.y[373]),(gamma_3FGL.x[375],gamma_3FGL.y[375])),\
          ((gamma_3FGL.x[373],gamma_3FGL.y[373]),(gamma_3FGL.x[1428],gamma_3FGL.y[1428])),\
          ((gamma_3FGL.x[437],gamma_3FGL.y[437]),(gamma_3FGL.x[438],gamma_3FGL.y[438])),\
          ((gamma_3FGL.x[620],gamma_3FGL.y[620]),(gamma_3FGL.x[751],gamma_3FGL.y[751])),\
          ((gamma_3FGL.x[620],gamma_3FGL.y[620]),(gamma_3FGL.x[892],gamma_3FGL.y[892])),\
          ((gamma_3FGL.x[712],gamma_3FGL.y[712]),(gamma_3FGL.x[714],gamma_3FGL.y[714])),\
          ((gamma_3FGL.x[712],gamma_3FGL.y[712]),(gamma_3FGL.x[954],gamma_3FGL.y[954])),\
          ((gamma_3FGL.x[712],gamma_3FGL.y[712]),(gamma_3FGL.x[1642],gamma_3FGL.y[1642])),\
          ((gamma_3FGL.x[714],gamma_3FGL.y[714]),(gamma_3FGL.x[1244],gamma_3FGL.y[1244])),\
          ((gamma_3FGL.x[720],gamma_3FGL.y[720]),(gamma_3FGL.x[1253],gamma_3FGL.y[1253])),\
          ((gamma_3FGL.x[720],gamma_3FGL.y[720]),(gamma_3FGL.x[1976],gamma_3FGL.y[1976])),\
          ((gamma_3FGL.x[720],gamma_3FGL.y[720]),(gamma_3FGL.x[2173],gamma_3FGL.y[2173])),\
          ((gamma_3FGL.x[749],gamma_3FGL.y[749]),(gamma_3FGL.x[751],gamma_3FGL.y[751])),\
          ((gamma_3FGL.x[749],gamma_3FGL.y[749]),(gamma_3FGL.x[2969],gamma_3FGL.y[2969])),\
          ((gamma_3FGL.x[832],gamma_3FGL.y[832]),(gamma_3FGL.x[834],gamma_3FGL.y[834])),\
          ((gamma_3FGL.x[832],gamma_3FGL.y[832]),(gamma_3FGL.x[1289],gamma_3FGL.y[1289])),\
          ((gamma_3FGL.x[832],gamma_3FGL.y[832]),(gamma_3FGL.x[2109],gamma_3FGL.y[2109])),\
          ((gamma_3FGL.x[834],gamma_3FGL.y[834]),(gamma_3FGL.x[836],gamma_3FGL.y[836])),\
          ((gamma_3FGL.x[836],gamma_3FGL.y[836]),(gamma_3FGL.x[1642],gamma_3FGL.y[1642])),\
          ((gamma_3FGL.x[952],gamma_3FGL.y[952]),(gamma_3FGL.x[954],gamma_3FGL.y[954])),\
          ((gamma_3FGL.x[952],gamma_3FGL.y[952]),(gamma_3FGL.x[2109],gamma_3FGL.y[2109])),\
          ((gamma_3FGL.x[1246],gamma_3FGL.y[1246]),(gamma_3FGL.x[1244],gamma_3FGL.y[1244])),\
          ((gamma_3FGL.x[1246],gamma_3FGL.y[1246]),(gamma_3FGL.x[2173],gamma_3FGL.y[2173])),\
          ((gamma_3FGL.x[1289],gamma_3FGL.y[1289]),(gamma_3FGL.x[1292],gamma_3FGL.y[1292])),\
          ((gamma_3FGL.x[1291],gamma_3FGL.y[1291]),(gamma_3FGL.x[1293],gamma_3FGL.y[1293])),\
          ((gamma_3FGL.x[1291],gamma_3FGL.y[1291]),(gamma_3FGL.x[2708],gamma_3FGL.y[2708])),\
          ((gamma_3FGL.x[1292],gamma_3FGL.y[1292]),(gamma_3FGL.x[1293],gamma_3FGL.y[1293])),\
          ((gamma_3FGL.x[1428],gamma_3FGL.y[1428]),(gamma_3FGL.x[1866],gamma_3FGL.y[1866])),\
          ((gamma_3FGL.x[1605],gamma_3FGL.y[1605]),(gamma_3FGL.x[1606],gamma_3FGL.y[1606])),\
          ((gamma_3FGL.x[1605],gamma_3FGL.y[1605]),(gamma_3FGL.x[1980],gamma_3FGL.y[1980])),\
          ((gamma_3FGL.x[1866],gamma_3FGL.y[1866]),(gamma_3FGL.x[1979],gamma_3FGL.y[1979])),\
          ((gamma_3FGL.x[1976],gamma_3FGL.y[1976]),(gamma_3FGL.x[1979],gamma_3FGL.y[1979])),\
          ((gamma_3FGL.x[1976],gamma_3FGL.y[1976]),(gamma_3FGL.x[1980],gamma_3FGL.y[1980])),\
          ((gamma_3FGL.x[2091],gamma_3FGL.y[2091]),(gamma_3FGL.x[2617],gamma_3FGL.y[2617])),\
          ((gamma_3FGL.x[2091],gamma_3FGL.y[2091]),(gamma_3FGL.x[2937],gamma_3FGL.y[2937])),\
          ((gamma_3FGL.x[2617],gamma_3FGL.y[2617]),(gamma_3FGL.x[2620],gamma_3FGL.y[2620])),\
          ((gamma_3FGL.x[2708],gamma_3FGL.y[2708]),(gamma_3FGL.x[2709],gamma_3FGL.y[2709])),\
          ((gamma_3FGL.x[2709],gamma_3FGL.y[2709]),(gamma_3FGL.x[2711],gamma_3FGL.y[2711]))]
          #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[2620],gamma_3FGL.y[2620])),\

Obelisk = [((gamma_3FGL.x[1122],gamma_3FGL.y[1122]),(gamma_3FGL.x[2836],gamma_3FGL.y[2836])),\
           ((gamma_3FGL.x[1116],gamma_3FGL.y[1116]),(gamma_3FGL.x[1120],gamma_3FGL.y[1120])),\
           ((gamma_3FGL.x[1116],gamma_3FGL.y[1116]),(gamma_3FGL.x[1390],gamma_3FGL.y[1390])),\
           ((gamma_3FGL.x[1120],gamma_3FGL.y[1120]),(gamma_3FGL.x[1122],gamma_3FGL.y[1122])),\
           ((gamma_3FGL.x[1122],gamma_3FGL.y[1122]),(gamma_3FGL.x[1123],gamma_3FGL.y[1123])),\
           ((gamma_3FGL.x[1123],gamma_3FGL.y[1123]),(gamma_3FGL.x[1312],gamma_3FGL.y[1312])),\
           ((gamma_3FGL.x[1312],gamma_3FGL.y[1312]),(gamma_3FGL.x[1313],gamma_3FGL.y[1313])),\
           ((gamma_3FGL.x[1312],gamma_3FGL.y[1312]),(gamma_3FGL.x[2838],gamma_3FGL.y[2838])),\
           ((gamma_3FGL.x[2342],gamma_3FGL.y[2342]),(gamma_3FGL.x[2836],gamma_3FGL.y[2836])),\
           ((gamma_3FGL.x[2342],gamma_3FGL.y[2342]),(gamma_3FGL.x[2838],gamma_3FGL.y[2838])),\
           ((gamma_3FGL.x[2836],gamma_3FGL.y[2836]),(gamma_3FGL.x[2837],gamma_3FGL.y[2837])),\
           ((gamma_3FGL.x[2837],gamma_3FGL.y[2837]),(gamma_3FGL.x[2838],gamma_3FGL.y[2838]))]

Pharos = [((gamma_3FGL.x[1004],gamma_3FGL.y[1004]),(gamma_3FGL.x[1005],gamma_3FGL.y[1005])),\
          ((gamma_3FGL.x[1004],gamma_3FGL.y[1004]),(gamma_3FGL.x[1372],gamma_3FGL.y[1372])),\
          ((gamma_3FGL.x[1005],gamma_3FGL.y[1005]),(gamma_3FGL.x[2774],gamma_3FGL.y[2774])),\
          ((gamma_3FGL.x[1069],gamma_3FGL.y[1069]),(gamma_3FGL.x[1070],gamma_3FGL.y[1070])),\
          ((gamma_3FGL.x[1069],gamma_3FGL.y[1069]),(gamma_3FGL.x[1071],gamma_3FGL.y[1071])),\
          ((gamma_3FGL.x[1069],gamma_3FGL.y[1069]),(gamma_3FGL.x[1378],gamma_3FGL.y[1378])),\
          ((gamma_3FGL.x[1070],gamma_3FGL.y[1070]),(gamma_3FGL.x[1082],gamma_3FGL.y[1082])),\
          ((gamma_3FGL.x[1071],gamma_3FGL.y[1071]),(gamma_3FGL.x[1805],gamma_3FGL.y[1805])),\
          ((gamma_3FGL.x[1076],gamma_3FGL.y[1076]),(gamma_3FGL.x[1078],gamma_3FGL.y[1078])),\
          ((gamma_3FGL.x[1076],gamma_3FGL.y[1076]),(gamma_3FGL.x[2775],gamma_3FGL.y[2775])),\
          ((gamma_3FGL.x[1077],gamma_3FGL.y[1077]),(gamma_3FGL.x[1078],gamma_3FGL.y[1078])),\
          ((gamma_3FGL.x[1077],gamma_3FGL.y[1077]),(gamma_3FGL.x[1083],gamma_3FGL.y[1083])),\
          ((gamma_3FGL.x[1077],gamma_3FGL.y[1077]),(gamma_3FGL.x[1801],gamma_3FGL.y[1801])),\
          ((gamma_3FGL.x[1077],gamma_3FGL.y[1077]),(gamma_3FGL.x[1802],gamma_3FGL.y[1802])),\
          ((gamma_3FGL.x[1081],gamma_3FGL.y[1081]),(gamma_3FGL.x[1082],gamma_3FGL.y[1082])),\
          ((gamma_3FGL.x[1081],gamma_3FGL.y[1081]),(gamma_3FGL.x[1083],gamma_3FGL.y[1083])),\
          ((gamma_3FGL.x[1265],gamma_3FGL.y[1265]),(gamma_3FGL.x[2988],gamma_3FGL.y[2988])),\
          ((gamma_3FGL.x[1377],gamma_3FGL.y[1377]),(gamma_3FGL.x[1378],gamma_3FGL.y[1378])),\
          ((gamma_3FGL.x[1802],gamma_3FGL.y[1802]),(gamma_3FGL.x[2983],gamma_3FGL.y[2983])),\
          ((gamma_3FGL.x[1805],gamma_3FGL.y[1805]),(gamma_3FGL.x[2989],gamma_3FGL.y[2989])),\
          ((gamma_3FGL.x[2022],gamma_3FGL.y[2022]),(gamma_3FGL.x[2988],gamma_3FGL.y[2988])),\
          ((gamma_3FGL.x[2519],gamma_3FGL.y[2519]),(gamma_3FGL.x[2520],gamma_3FGL.y[2520])),\
          ((gamma_3FGL.x[2773],gamma_3FGL.y[2773]),(gamma_3FGL.x[2774],gamma_3FGL.y[2774])),\
          ((gamma_3FGL.x[2773],gamma_3FGL.y[2773]),(gamma_3FGL.x[2775],gamma_3FGL.y[2775])),\
          ((gamma_3FGL.x[2983],gamma_3FGL.y[2983]),(gamma_3FGL.x[2989],gamma_3FGL.y[2989])),\
          ((gamma_3FGL.x[2988],gamma_3FGL.y[2988]),(gamma_3FGL.x[3003],gamma_3FGL.y[3003]))]

Radio_Telescope = [((gamma_3FGL.x[682],gamma_3FGL.y[682]),(gamma_3FGL.x[1054],gamma_3FGL.y[1054])),\
                   ((gamma_3FGL.x[682],gamma_3FGL.y[682]),(gamma_3FGL.x[2740],gamma_3FGL.y[2740])),\
                   ((gamma_3FGL.x[775],gamma_3FGL.y[775]),(gamma_3FGL.x[2741],gamma_3FGL.y[2741])),\
                   ((gamma_3FGL.x[870],gamma_3FGL.y[870]),(gamma_3FGL.x[871],gamma_3FGL.y[871])),\
                   ((gamma_3FGL.x[870],gamma_3FGL.y[870]),(gamma_3FGL.x[2013],gamma_3FGL.y[2013])),\
                   ((gamma_3FGL.x[871],gamma_3FGL.y[871]),(gamma_3FGL.x[1499],gamma_3FGL.y[1499])),\
                   ((gamma_3FGL.x[1054],gamma_3FGL.y[1054]),(gamma_3FGL.x[2013],gamma_3FGL.y[2013])),\
                   ((gamma_3FGL.x[1498],gamma_3FGL.y[1498]),(gamma_3FGL.x[1499],gamma_3FGL.y[1499])),\
                   ((gamma_3FGL.x[1498],gamma_3FGL.y[1498]),(gamma_3FGL.x[2928],gamma_3FGL.y[2928])),\
                   ((gamma_3FGL.x[1672],gamma_3FGL.y[1672]),(gamma_3FGL.x[1673],gamma_3FGL.y[1673])),\
                   ((gamma_3FGL.x[1672],gamma_3FGL.y[1672]),(gamma_3FGL.x[2654],gamma_3FGL.y[2654])),\
                   ((gamma_3FGL.x[1673],gamma_3FGL.y[1673]),(gamma_3FGL.x[2656],gamma_3FGL.y[2656])),\
                   ((gamma_3FGL.x[1725],gamma_3FGL.y[1725]),(gamma_3FGL.x[2655],gamma_3FGL.y[2655])),\
                   ((gamma_3FGL.x[1725],gamma_3FGL.y[1725]),(gamma_3FGL.x[2928],gamma_3FGL.y[2928])),\
                   ((gamma_3FGL.x[1764],gamma_3FGL.y[1764]),(gamma_3FGL.x[2564],gamma_3FGL.y[2564])),\
                   ((gamma_3FGL.x[1764],gamma_3FGL.y[1764]),(gamma_3FGL.x[2740],gamma_3FGL.y[2740])),\
                   ((gamma_3FGL.x[2564],gamma_3FGL.y[2564]),(gamma_3FGL.x[2692],gamma_3FGL.y[2692])),\
                   ((gamma_3FGL.x[2654],gamma_3FGL.y[2654]),(gamma_3FGL.x[2655],gamma_3FGL.y[2655])),\
                   ((gamma_3FGL.x[2655],gamma_3FGL.y[2655]),(gamma_3FGL.x[2657],gamma_3FGL.y[2657])),\
                   ((gamma_3FGL.x[2656],gamma_3FGL.y[2656]),(gamma_3FGL.x[2928],gamma_3FGL.y[2928])),\
                   ((gamma_3FGL.x[2657],gamma_3FGL.y[2657]),(gamma_3FGL.x[2928],gamma_3FGL.y[2928])),\
                   ((gamma_3FGL.x[2691],gamma_3FGL.y[2691]),(gamma_3FGL.x[2692],gamma_3FGL.y[2692])),\
                   ((gamma_3FGL.x[2691],gamma_3FGL.y[2691]),(gamma_3FGL.x[2928],gamma_3FGL.y[2928])),\
                   ((gamma_3FGL.x[2716],gamma_3FGL.y[2716]),(gamma_3FGL.x[2742],gamma_3FGL.y[2742])),\
                   ((gamma_3FGL.x[2716],gamma_3FGL.y[2716]),(gamma_3FGL.x[2954],gamma_3FGL.y[2954])),\
                   ((gamma_3FGL.x[2741],gamma_3FGL.y[2741]),(gamma_3FGL.x[2742],gamma_3FGL.y[2742]))]
                   #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[2930],gamma_3FGL.y[2930])),\

Saturn_V_Rocket = [((gamma_3FGL.x[236],gamma_3FGL.y[236]),(gamma_3FGL.x[480],gamma_3FGL.y[480])),\
                   ((gamma_3FGL.x[236],gamma_3FGL.y[236]),(gamma_3FGL.x[1812],gamma_3FGL.y[1812])),\
                   ((gamma_3FGL.x[236],gamma_3FGL.y[236]),(gamma_3FGL.x[1813],gamma_3FGL.y[1813])),\
                   ((gamma_3FGL.x[268],gamma_3FGL.y[268]),(gamma_3FGL.x[269],gamma_3FGL.y[269])),\
                   ((gamma_3FGL.x[268],gamma_3FGL.y[268]),(gamma_3FGL.x[399],gamma_3FGL.y[399])),\
                   ((gamma_3FGL.x[269],gamma_3FGL.y[269]),(gamma_3FGL.x[384],gamma_3FGL.y[384])),\
                   ((gamma_3FGL.x[384],gamma_3FGL.y[384]),(gamma_3FGL.x[2062],gamma_3FGL.y[2062])),\
                   ((gamma_3FGL.x[399],gamma_3FGL.y[399]),(gamma_3FGL.x[526],gamma_3FGL.y[526])),\
                   ((gamma_3FGL.x[480],gamma_3FGL.y[480]),(gamma_3FGL.x[526],gamma_3FGL.y[526])),\
                   ((gamma_3FGL.x[1128],gamma_3FGL.y[1128]),(gamma_3FGL.x[1405],gamma_3FGL.y[1405])),\
                   ((gamma_3FGL.x[1128],gamma_3FGL.y[1128]),(gamma_3FGL.x[1813],gamma_3FGL.y[1813])),\
                   ((gamma_3FGL.x[1405],gamma_3FGL.y[1405]),(gamma_3FGL.x[1837],gamma_3FGL.y[1837])),\
                   ((gamma_3FGL.x[1811],gamma_3FGL.y[1811]),(gamma_3FGL.x[1812],gamma_3FGL.y[1812])),\
                   ((gamma_3FGL.x[1812],gamma_3FGL.y[1812]),(gamma_3FGL.x[1813],gamma_3FGL.y[1813]))]
                   #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[1837],gamma_3FGL.y[1837])),\
                   #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[2062],gamma_3FGL.y[2062])),\
                   
Schrodinger_Cat = [((gamma_3FGL.x[558],gamma_3FGL.y[558]),(gamma_3FGL.x[560],gamma_3FGL.y[560])),\
                   ((gamma_3FGL.x[558],gamma_3FGL.y[558]),(gamma_3FGL.x[1421],gamma_3FGL.y[1421])),\
                   ((gamma_3FGL.x[560],gamma_3FGL.y[560]),(gamma_3FGL.x[2320],gamma_3FGL.y[2320])),\
                   ((gamma_3FGL.x[791],gamma_3FGL.y[791]),(gamma_3FGL.x[896],gamma_3FGL.y[896])),\
                   ((gamma_3FGL.x[791],gamma_3FGL.y[791]),(gamma_3FGL.x[903],gamma_3FGL.y[903])),\
                   ((gamma_3FGL.x[791],gamma_3FGL.y[791]),(gamma_3FGL.x[904],gamma_3FGL.y[904])),\
                   ((gamma_3FGL.x[791],gamma_3FGL.y[791]),(gamma_3FGL.x[1844],gamma_3FGL.y[1844])),\
                   ((gamma_3FGL.x[893],gamma_3FGL.y[893]),(gamma_3FGL.x[900],gamma_3FGL.y[900])),\
                   ((gamma_3FGL.x[896],gamma_3FGL.y[896]),(gamma_3FGL.x[1162],gamma_3FGL.y[1162])),\
                   ((gamma_3FGL.x[896],gamma_3FGL.y[896]),(gamma_3FGL.x[1421],gamma_3FGL.y[1421])),\
                   ((gamma_3FGL.x[896],gamma_3FGL.y[896]),(gamma_3FGL.x[2943],gamma_3FGL.y[2943])),\
                   ((gamma_3FGL.x[900],gamma_3FGL.y[900]),(gamma_3FGL.x[901],gamma_3FGL.y[901])),\
                   ((gamma_3FGL.x[903],gamma_3FGL.y[903]),(gamma_3FGL.x[904],gamma_3FGL.y[904])),\
                   ((gamma_3FGL.x[903],gamma_3FGL.y[903]),(gamma_3FGL.x[2943],gamma_3FGL.y[2943])),\
                   ((gamma_3FGL.x[904],gamma_3FGL.y[904]),(gamma_3FGL.x[1162],gamma_3FGL.y[1162])),\
                   ((gamma_3FGL.x[1162],gamma_3FGL.y[1162]),(gamma_3FGL.x[2320],gamma_3FGL.y[2320])),\
                   ((gamma_3FGL.x[1162],gamma_3FGL.y[1162]),(gamma_3FGL.x[2943],gamma_3FGL.y[2943])),\
                   ((gamma_3FGL.x[1421],gamma_3FGL.y[1421]),(gamma_3FGL.x[1430],gamma_3FGL.y[1430])),\
                   ((gamma_3FGL.x[1430],gamma_3FGL.y[1430]),(gamma_3FGL.x[1844],gamma_3FGL.y[1844]))]

Starship_Enterprise = [((gamma_3FGL.x[35],gamma_3FGL.y[35]),(gamma_3FGL.x[379],gamma_3FGL.y[379])),\
                       ((gamma_3FGL.x[37],gamma_3FGL.y[37]),(gamma_3FGL.x[337],gamma_3FGL.y[337])),\
                       ((gamma_3FGL.x[37],gamma_3FGL.y[37]),(gamma_3FGL.x[380],gamma_3FGL.y[380])),\
                       ((gamma_3FGL.x[75],gamma_3FGL.y[75]),(gamma_3FGL.x[77],gamma_3FGL.y[77])),\
                       ((gamma_3FGL.x[75],gamma_3FGL.y[75]),(gamma_3FGL.x[249],gamma_3FGL.y[249])),\
                       ((gamma_3FGL.x[82],gamma_3FGL.y[82]),(gamma_3FGL.x[209],gamma_3FGL.y[209])),\
                       ((gamma_3FGL.x[83],gamma_3FGL.y[83]),(gamma_3FGL.x[323],gamma_3FGL.y[323])),\
                       ((gamma_3FGL.x[83],gamma_3FGL.y[83]),(gamma_3FGL.x[377],gamma_3FGL.y[377])),\
                       ((gamma_3FGL.x[83],gamma_3FGL.y[83]),(gamma_3FGL.x[474],gamma_3FGL.y[474])),\
                       ((gamma_3FGL.x[121],gamma_3FGL.y[121]),(gamma_3FGL.x[122],gamma_3FGL.y[122])),\
                       ((gamma_3FGL.x[121],gamma_3FGL.y[121]),(gamma_3FGL.x[204],gamma_3FGL.y[204])),\
                       ((gamma_3FGL.x[122],gamma_3FGL.y[122]),(gamma_3FGL.x[123],gamma_3FGL.y[123])),\
                       ((gamma_3FGL.x[123],gamma_3FGL.y[123]),(gamma_3FGL.x[490],gamma_3FGL.y[490])),\
                       ((gamma_3FGL.x[126],gamma_3FGL.y[126]),(gamma_3FGL.x[252],gamma_3FGL.y[252])),\
                       ((gamma_3FGL.x[126],gamma_3FGL.y[126]),(gamma_3FGL.x[387],gamma_3FGL.y[387])),\
                       ((gamma_3FGL.x[204],gamma_3FGL.y[204]),(gamma_3FGL.x[249],gamma_3FGL.y[249])),\
                       ((gamma_3FGL.x[209],gamma_3FGL.y[209]),(gamma_3FGL.x[472],gamma_3FGL.y[472])),\
                       ((gamma_3FGL.x[209],gamma_3FGL.y[209]),(gamma_3FGL.x[1209],gamma_3FGL.y[1209])),\
                       ((gamma_3FGL.x[247],gamma_3FGL.y[247]),(gamma_3FGL.x[249],gamma_3FGL.y[249])),\
                       ((gamma_3FGL.x[251],gamma_3FGL.y[251]),(gamma_3FGL.x[252],gamma_3FGL.y[252])),\
                       ((gamma_3FGL.x[251],gamma_3FGL.y[251]),(gamma_3FGL.x[337],gamma_3FGL.y[337])),\
                       ((gamma_3FGL.x[324],gamma_3FGL.y[324]),(gamma_3FGL.x[325],gamma_3FGL.y[325])),\
                       ((gamma_3FGL.x[324],gamma_3FGL.y[324]),(gamma_3FGL.x[380],gamma_3FGL.y[380])),\
                       ((gamma_3FGL.x[325],gamma_3FGL.y[325]),(gamma_3FGL.x[387],gamma_3FGL.y[387])),\
                       ((gamma_3FGL.x[377],gamma_3FGL.y[377]),(gamma_3FGL.x[2031],gamma_3FGL.y[2031])),\
                       ((gamma_3FGL.x[473],gamma_3FGL.y[473]),(gamma_3FGL.x[474],gamma_3FGL.y[474])),\
                       ((gamma_3FGL.x[473],gamma_3FGL.y[473]),(gamma_3FGL.x[944],gamma_3FGL.y[944])),\
                       ((gamma_3FGL.x[476],gamma_3FGL.y[476]),(gamma_3FGL.x[478],gamma_3FGL.y[478])),\
                       ((gamma_3FGL.x[476],gamma_3FGL.y[476]),(gamma_3FGL.x[2981],gamma_3FGL.y[2981])),\
                       ((gamma_3FGL.x[478],gamma_3FGL.y[478]),(gamma_3FGL.x[479],gamma_3FGL.y[479])),\
                       ((gamma_3FGL.x[479],gamma_3FGL.y[479]),(gamma_3FGL.x[1209],gamma_3FGL.y[1209])),\
                       ((gamma_3FGL.x[941],gamma_3FGL.y[941]),(gamma_3FGL.x[943],gamma_3FGL.y[943])),\
                       ((gamma_3FGL.x[941],gamma_3FGL.y[941]),(gamma_3FGL.x[2012],gamma_3FGL.y[2012])),\
                       ((gamma_3FGL.x[943],gamma_3FGL.y[943]),(gamma_3FGL.x[944],gamma_3FGL.y[944])),\
                       ((gamma_3FGL.x[2012],gamma_3FGL.y[2012]),(gamma_3FGL.x[2030],gamma_3FGL.y[2030])),\
                       ((gamma_3FGL.x[2030],gamma_3FGL.y[2030]),(gamma_3FGL.x[2031],gamma_3FGL.y[2031]))]
                       #((gamma_3FGL.x[2012],gamma_3FGL.y[2012]),(gamma_3FGL.x[],gamma_3FGL.y[])),\

TARDIS = [((gamma_3FGL.x[569],gamma_3FGL.y[569]),(gamma_3FGL.x[591],gamma_3FGL.y[591])),\
          ((gamma_3FGL.x[569],gamma_3FGL.y[569]),(gamma_3FGL.x[1249],gamma_3FGL.y[1249])),\
          ((gamma_3FGL.x[570],gamma_3FGL.y[570]),(gamma_3FGL.x[571],gamma_3FGL.y[571])),\
          ((gamma_3FGL.x[570],gamma_3FGL.y[570]),(gamma_3FGL.x[1249],gamma_3FGL.y[1249])),\
          ((gamma_3FGL.x[571],gamma_3FGL.y[571]),(gamma_3FGL.x[591],gamma_3FGL.y[591])),\
          ((gamma_3FGL.x[571],gamma_3FGL.y[571]),(gamma_3FGL.x[709],gamma_3FGL.y[709])),\
          ((gamma_3FGL.x[591],gamma_3FGL.y[591]),(gamma_3FGL.x[709],gamma_3FGL.y[709])),\
          ((gamma_3FGL.x[591],gamma_3FGL.y[591]),(gamma_3FGL.x[820],gamma_3FGL.y[820])),\
          ((gamma_3FGL.x[708],gamma_3FGL.y[708]),(gamma_3FGL.x[709],gamma_3FGL.y[709])),\
          ((gamma_3FGL.x[708],gamma_3FGL.y[708]),(gamma_3FGL.x[2682],gamma_3FGL.y[2682])),\
          ((gamma_3FGL.x[820],gamma_3FGL.y[820]),(gamma_3FGL.x[951],gamma_3FGL.y[951])),\
          ((gamma_3FGL.x[820],gamma_3FGL.y[820]),(gamma_3FGL.x[2682],gamma_3FGL.y[2682])),\
          ((gamma_3FGL.x[951],gamma_3FGL.y[951]),(gamma_3FGL.x[1759],gamma_3FGL.y[1759])),\
          ((gamma_3FGL.x[1249],gamma_3FGL.y[1249]),(gamma_3FGL.x[1759],gamma_3FGL.y[1759]))]
          #((gamma_3FGL.x[570],gamma_3FGL.y[570]),(gamma_3FGL.x[],gamma_3FGL.y[])),\
          #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[571],gamma_3FGL.y[571])),\
          #((gamma_3FGL.x[],gamma_3FGL.y[]),(gamma_3FGL.x[572],gamma_3FGL.y[572])),\

Vasa = [((gamma_3FGL.x[556],gamma_3FGL.y[556]),(gamma_3FGL.x[961],gamma_3FGL.y[961])),\
        ((gamma_3FGL.x[556],gamma_3FGL.y[556]),(gamma_3FGL.x[1506],gamma_3FGL.y[1506])),\
        ((gamma_3FGL.x[782],gamma_3FGL.y[782]),(gamma_3FGL.x[1356],gamma_3FGL.y[1356])),\
        ((gamma_3FGL.x[782],gamma_3FGL.y[782]),(gamma_3FGL.x[1503],gamma_3FGL.y[1503])),\
        ((gamma_3FGL.x[881],gamma_3FGL.y[881]),(gamma_3FGL.x[1505],gamma_3FGL.y[1505])),\
        ((gamma_3FGL.x[881],gamma_3FGL.y[881]),(gamma_3FGL.x[2136],gamma_3FGL.y[2136])),\
        ((gamma_3FGL.x[961],gamma_3FGL.y[961]),(gamma_3FGL.x[964],gamma_3FGL.y[964])),\
        ((gamma_3FGL.x[964],gamma_3FGL.y[964]),(gamma_3FGL.x[1086],gamma_3FGL.y[1086])),\
        ((gamma_3FGL.x[966],gamma_3FGL.y[966]),(gamma_3FGL.x[2792],gamma_3FGL.y[2792])),\
        ((gamma_3FGL.x[966],gamma_3FGL.y[966]),(gamma_3FGL.x[2810],gamma_3FGL.y[2810])),\
        ((gamma_3FGL.x[991],gamma_3FGL.y[991]),(gamma_3FGL.x[2139],gamma_3FGL.y[2139])),\
        ((gamma_3FGL.x[991],gamma_3FGL.y[991]),(gamma_3FGL.x[2760],gamma_3FGL.y[2760])),\
        ((gamma_3FGL.x[993],gamma_3FGL.y[993]),(gamma_3FGL.x[2096],gamma_3FGL.y[2096])),\
        ((gamma_3FGL.x[993],gamma_3FGL.y[993]),(gamma_3FGL.x[2136],gamma_3FGL.y[2136])),\
        ((gamma_3FGL.x[1065],gamma_3FGL.y[1065]),(gamma_3FGL.x[1068],gamma_3FGL.y[1068])),\
        ((gamma_3FGL.x[1068],gamma_3FGL.y[1068]),(gamma_3FGL.x[1074],gamma_3FGL.y[1074])),\
        ((gamma_3FGL.x[1072],gamma_3FGL.y[1072]),(gamma_3FGL.x[1074],gamma_3FGL.y[1074])),\
        ((gamma_3FGL.x[1074],gamma_3FGL.y[1074]),(gamma_3FGL.x[2153],gamma_3FGL.y[2153])),\
        ((gamma_3FGL.x[1075],gamma_3FGL.y[1075]),(gamma_3FGL.x[2153],gamma_3FGL.y[2153])),\
        ((gamma_3FGL.x[1075],gamma_3FGL.y[1075]),(gamma_3FGL.x[2154],gamma_3FGL.y[2154])),\
        ((gamma_3FGL.x[1086],gamma_3FGL.y[1086]),(gamma_3FGL.x[1087],gamma_3FGL.y[1087])),\
        ((gamma_3FGL.x[1087],gamma_3FGL.y[1087]),(gamma_3FGL.x[1092],gamma_3FGL.y[1092])),\
        ((gamma_3FGL.x[1092],gamma_3FGL.y[1092]),(gamma_3FGL.x[2168],gamma_3FGL.y[2168])),\
        ((gamma_3FGL.x[1092],gamma_3FGL.y[1092]),(gamma_3FGL.x[2450],gamma_3FGL.y[2450])),\
        ((gamma_3FGL.x[1346],gamma_3FGL.y[1346]),(gamma_3FGL.x[1767],gamma_3FGL.y[1767])),\
        ((gamma_3FGL.x[1346],gamma_3FGL.y[1346]),(gamma_3FGL.x[2777],gamma_3FGL.y[2777])),\
        ((gamma_3FGL.x[1356],gamma_3FGL.y[1356]),(gamma_3FGL.x[2311],gamma_3FGL.y[2311])),\
        ((gamma_3FGL.x[1356],gamma_3FGL.y[1356]),(gamma_3FGL.x[2948],gamma_3FGL.y[2948])),\
        ((gamma_3FGL.x[1503],gamma_3FGL.y[1503]),(gamma_3FGL.x[1504],gamma_3FGL.y[1504])),\
        ((gamma_3FGL.x[1505],gamma_3FGL.y[1505]),(gamma_3FGL.x[1624],gamma_3FGL.y[1624])),\
        ((gamma_3FGL.x[1506],gamma_3FGL.y[1506]),(gamma_3FGL.x[1625],gamma_3FGL.y[1625])),\
        ((gamma_3FGL.x[1623],gamma_3FGL.y[1623]),(gamma_3FGL.x[1624],gamma_3FGL.y[1624])),\
        ((gamma_3FGL.x[1623],gamma_3FGL.y[1623]),(gamma_3FGL.x[2948],gamma_3FGL.y[2948])),\
        ((gamma_3FGL.x[1624],gamma_3FGL.y[1624]),(gamma_3FGL.x[1625],gamma_3FGL.y[1625])),\
        ((gamma_3FGL.x[1624],gamma_3FGL.y[1624]),(gamma_3FGL.x[2776],gamma_3FGL.y[2776])),\
        ((gamma_3FGL.x[1625],gamma_3FGL.y[1625]),(gamma_3FGL.x[2894],gamma_3FGL.y[2894])),\
        ((gamma_3FGL.x[1767],gamma_3FGL.y[1767]),(gamma_3FGL.x[2563],gamma_3FGL.y[2563])),\
        ((gamma_3FGL.x[1790],gamma_3FGL.y[1790]),(gamma_3FGL.x[2792],gamma_3FGL.y[2792])),\
        ((gamma_3FGL.x[1790],gamma_3FGL.y[1790]),(gamma_3FGL.x[2897],gamma_3FGL.y[2897])),\
        ((gamma_3FGL.x[1795],gamma_3FGL.y[1795]),(gamma_3FGL.x[2151],gamma_3FGL.y[2151])),\
        ((gamma_3FGL.x[1795],gamma_3FGL.y[1795]),(gamma_3FGL.x[2153],gamma_3FGL.y[2153])),\
        ((gamma_3FGL.x[2008],gamma_3FGL.y[2008]),(gamma_3FGL.x[2948],gamma_3FGL.y[2948])),\
        ((gamma_3FGL.x[2136],gamma_3FGL.y[2136]),(gamma_3FGL.x[2169],gamma_3FGL.y[2169])),\
        ((gamma_3FGL.x[2151],gamma_3FGL.y[2151]),(gamma_3FGL.x[2169],gamma_3FGL.y[2169])),\
        ((gamma_3FGL.x[2152],gamma_3FGL.y[2152]),(gamma_3FGL.x[2168],gamma_3FGL.y[2168])),\
        ((gamma_3FGL.x[2152],gamma_3FGL.y[2152]),(gamma_3FGL.x[2777],gamma_3FGL.y[2777])),\
        ((gamma_3FGL.x[2154],gamma_3FGL.y[2154]),(gamma_3FGL.x[2155],gamma_3FGL.y[2155])),\
        ((gamma_3FGL.x[2155],gamma_3FGL.y[2155]),(gamma_3FGL.x[2168],gamma_3FGL.y[2168])),\
        ((gamma_3FGL.x[2449],gamma_3FGL.y[2449]),(gamma_3FGL.x[2450],gamma_3FGL.y[2450])),\
        ((gamma_3FGL.x[2449],gamma_3FGL.y[2449]),(gamma_3FGL.x[2811],gamma_3FGL.y[2811])),\
        ((gamma_3FGL.x[2759],gamma_3FGL.y[2759]),(gamma_3FGL.x[2760],gamma_3FGL.y[2760])),\
        ((gamma_3FGL.x[2776],gamma_3FGL.y[2776]),(gamma_3FGL.x[2777],gamma_3FGL.y[2777])),\
        ((gamma_3FGL.x[2810],gamma_3FGL.y[2810]),(gamma_3FGL.x[2811],gamma_3FGL.y[2811])),\
        ((gamma_3FGL.x[2894],gamma_3FGL.y[2894]),(gamma_3FGL.x[2897],gamma_3FGL.y[2897]))]
        #((gamma_3FGL.x[1066],gamma_3FGL.y[1066]),(gamma_3FGL.x[],gamma_3FGL.y[])),\

for i in range(len(gamma_GRB2.x)):
    ax0.annotate(str(i),(gamma_GRB2.x[i],gamma_GRB2.y[i]),color='w',fontsize=6)
    
fermi1 = mc.LineCollection(Black_Widow_Spider, colors='white', alpha=0.5, zorder=10+2.5)
fermi2 = mc.LineCollection(Colosseum, colors='white', alpha=0.5, zorder=10+2.5)
fermi3 = mc.LineCollection(Eiffel_Tower, colors='white', alpha=0.5, zorder=10+2.5)
fermi4 = mc.LineCollection(Einstein, colors='white', alpha=0.5, zorder=10+2.5)
fermi5 = mc.LineCollection(Fermi_Satellite, colors='white', alpha=0.5, zorder=10+2.5)
fermi6 = mc.LineCollection(Godzilla, colors='white', alpha=0.5, zorder=10+2.5)
fermi7 = mc.LineCollection(Golden_Gate, colors='white', alpha=0.5, zorder=10+2.5)
fermi8 = mc.LineCollection(Hulk, colors='white', alpha=0.5, zorder=10+2.5)
fermi9 = mc.LineCollection(The_Little_Prince, colors='white', alpha=0.5, zorder=10+2.5)
fermi10 = mc.LineCollection(Mjolnir, colors='white', alpha=0.5, zorder=10+2.5)
fermi11 = mc.LineCollection(Mount_Fuji, colors='white', alpha=0.5, zorder=10+2.5)
fermi12 = mc.LineCollection(Castle, colors='white', alpha=0.5, zorder=10+2.5)
fermi13 = mc.LineCollection(Obelisk, colors='white', alpha=0.5, zorder=10+2.5)
fermi14 = mc.LineCollection(Pharos, colors='white', alpha=0.5, zorder=10+2.5)
fermi15 = mc.LineCollection(Radio_Telescope, colors='white', alpha=0.5, zorder=10+2.5)
fermi16 = mc.LineCollection(Saturn_V_Rocket, colors='white', alpha=0.5, zorder=10+2.5)
fermi17 = mc.LineCollection(Schrodinger_Cat, colors='white', alpha=0.5, zorder=10+2.5)
fermi18 = mc.LineCollection(Starship_Enterprise, colors='white', alpha=0.5, zorder=10+2.5)
fermi19 = mc.LineCollection(TARDIS, colors='white', alpha=0.5, zorder=10+2.5)
fermi20 = mc.LineCollection(Vasa, colors='white', alpha=0.5, zorder=10+2.5)
ax0.add_collection(fermi1)
ax0.add_collection(fermi2)
ax0.add_collection(fermi3)
ax0.add_collection(fermi4)
ax0.add_collection(fermi5)
ax0.add_collection(fermi6)
ax0.add_collection(fermi7)
ax0.add_collection(fermi8)
ax0.add_collection(fermi9)
ax0.add_collection(fermi10)
ax0.add_collection(fermi11)
ax0.add_collection(fermi12)
ax0.add_collection(fermi13)
ax0.add_collection(fermi14)
ax0.add_collection(fermi15)
ax0.add_collection(fermi16)
ax0.add_collection(fermi17)
ax0.add_collection(fermi18)
ax0.add_collection(fermi19)
ax0.add_collection(fermi20)

time5 = time.time()
print(time1-time0)
print(time2-time1)
print(time3-time2)
print(time4-time3)
print(time5-time4)

plt.show()

