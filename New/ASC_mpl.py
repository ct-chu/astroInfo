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
import sys
from sys import platform
import os
import gc
import feedparser
import re
import objgraph

##################
#memory leak
debug_mode = 0
##################

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
Obs.date = datetime.utcnow().replace(second=0,microsecond=0)
#####################################
# plot parameters
image_size = 1.6
side_space = 6
fig = plt.figure(figsize=(image_size*7.2*(1+1/side_space),image_size*4.8+1.2), facecolor='black')
fig.subplots_adjust(0,0,1,1,0,0)

gs = matplotlib.gridspec.GridSpec(6, 2, wspace=0, hspace=0, width_ratios=[1, side_space], height_ratios=[90,50,50,60,90,50])

ax0 = plt.subplot(gs[:5, 1])
ax0.set_facecolor('black')
ax0.set_aspect('equal', anchor='N')

ax1 = plt.subplot(gs[0, 0])
ax1.set_facecolor('black')
ax1.set_aspect('equal', anchor='NE')

ax2 = plt.subplot(gs[1, 0])
ax2.set_facecolor('black')
ax2.set_aspect('equal', anchor='NE')

ax3 = plt.subplot(gs[2, 0])
ax3.set_facecolor('black')
ax3.set_aspect('equal', anchor='NE')

ax4 = plt.subplot(gs[3, 0])
ax4.set_facecolor('black')
ax4.set_aspect('equal', anchor='NE')

ax5 = plt.subplot(gs[4:, 0])
ax5.set_facecolor('black')
ax5.set_aspect('equal', anchor='SE')

ax6 = plt.subplot(gs[5, 1])
ax6.set_facecolor('black')
#ax6.set_aspect('equal', anchor='NW')
    
matplotlib.rcParams['savefig.facecolor'] = (0,0,0)

##zenith_shift_ra     = -2.5
##zenith_shift_dec    = -1.5
##rotate_angle        = -1.5
##aspect_ratio        = 0.94 #y/x
##plot_scale          = 174
##x_shift             = -11.5
##y_shift             = 6

zenith_shift_ra     = -2.0
zenith_shift_dec    = -1.5
rotate_angle        = -2.0
aspect_ratio        = 0.90 #y/x
plot_scale          = 175
x_shift             = -11.5
y_shift             = 6.0

if platform == 'win32':
    DjV_S_6     = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/DEJAVUSANS.TTF', size=6)
    DjV_S_8     = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/DEJAVUSANS.TTF', size=8)
    DjV_S_9     = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/DEJAVUSANS.TTF', size=9)
    DjV_S_10    = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/DEJAVUSANS.TTF', size=10)
    DjV_S_12    = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/DEJAVUSANS.TTF', size=12)
    emoji_20    = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/YUGOTHB.TTC', size=20)
elif platform == 'darwin':
    DjV_S_6     = font_manager.FontProperties(fname = '/Library/Fonts/DEJAVUSANS.TTF', size=6)
    DjV_S_8     = font_manager.FontProperties(fname = '/Library/Fonts/DEJAVUSANS.TTF', size=8)
    DjV_S_9     = font_manager.FontProperties(fname = '/Library/Fonts/DEJAVUSANS.TTF', size=9)
    DjV_S_10    = font_manager.FontProperties(fname = '/Library/Fonts/DEJAVUSANS.TTF', size=10)
    DjV_S_12    = font_manager.FontProperties(fname = '/Library/Fonts/DEJAVUSANS.TTF', size=12)
    emoji_20    = font_manager.FontProperties(fname = '/Library/Fonts/YUGOTHB.TTC', size=20)
elif platform == 'linux':
    DjV_S_6     = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/DejaVu Sans/DejaVu_Sans_Book.ttf', size=6)
    DjV_S_8     = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/DejaVu Sans/DejaVu_Sans_Book.ttf', size=8)
    DjV_S_9     = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/DejaVu Sans/DejaVu_Sans_Book.ttf', size=9)
    DjV_S_10    = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/DejaVu Sans/DejaVu_Sans_Book.ttf', size=10)
    DjV_S_12    = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/DejaVu Sans/DejaVu_Sans_Book.ttf', size=12)
    emoji_20    = font_manager.FontProperties(fname = '/home/pi/.local/share/fonts/Unknown Vendor/TrueType/Yu Gothic/Yu_Gothic_Bold.ttc', size=20)
# raw data
horizon     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
equator     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
ecliptic    = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)

# log
def timelog(log):
    print(str(datetime.now().time().replace(microsecond=0))+'> '+log)
    
# make relative path (pathlib.Path.cwd() <=> current Dir)
timelog('importing star catalogue')
And = numpy.zeros(shape=(178,5))
And = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','And.csv'))
Ant = numpy.zeros(shape=(48,5))
Ant = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ant.csv'))
Aps = numpy.zeros(shape=(36,5))
Aps = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Aps.csv'))
Aqr = numpy.zeros(shape=(171,5))
Aqr = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Aqr.csv'))
Aql = numpy.zeros(shape=(131,5))
Aql = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Aql.csv'))
Ara = numpy.zeros(shape=(64,5))
Ara = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ara.csv'))
Ari = numpy.zeros(shape=(86,5))
Ari = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ari.csv'))
Aur = numpy.zeros(shape=(161,5))
Aur = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Aur.csv'))
Boo = numpy.zeros(shape=(154,5))
Boo = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Boo.csv'))
Cae = numpy.zeros(shape=(21,5))
Cae = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cae.csv'))
Cam = numpy.zeros(shape=(158,5))
Cam = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cam.csv'))
Cnc = numpy.zeros(shape=(112,5))
Cnc = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cnc.csv'))
CVn = numpy.zeros(shape=(61,5))
CVn = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CVn.csv'))
CMa = numpy.zeros(shape=(155,5))
CMa = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CMa.csv'))
CMi = numpy.zeros(shape=(44,5))
CMi = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CMi.csv'))
Cap = numpy.zeros(shape=(87,5))
Cap = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cap.csv'))
Car = numpy.zeros(shape=(210,5))
Car = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Car.csv'))
Cas = numpy.zeros(shape=(164,5))
Cas = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cas.csv'))
Cen = numpy.zeros(shape=(281,5))
Cen = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cen.csv'))
Cep = numpy.zeros(shape=(157,5))
Cep = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cep.csv'))
Cet = numpy.zeros(shape=(177,5))
Cet = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cet.csv'))
Cha = numpy.zeros(shape=(34,5))
Cha = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cha.csv'))
Cir = numpy.zeros(shape=(34,5))
Cir = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cir.csv'))
Col = numpy.zeros(shape=(78,5))
Col = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Col.csv'))
Com = numpy.zeros(shape=(71,5))
Com = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Com.csv'))
CrA = numpy.zeros(shape=(46,5))
CrA = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CrA.csv'))
CrB = numpy.zeros(shape=(40,5))
CrB = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CrB.csv'))
Crv = numpy.zeros(shape=(28,5))
Crv = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Crv.csv'))
Crt = numpy.zeros(shape=(33,5))
Crt = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Crt.csv'))
Cru = numpy.zeros(shape=(48,5))
Cru = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cru.csv'))
Cyg = numpy.zeros(shape=(291,5))
Cyg = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cyg.csv'))
Del = numpy.zeros(shape=(47,5))
Del = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Del.csv'))
Dor = numpy.zeros(shape=(34,5))
Dor = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Dor.csv'))
Dra = numpy.zeros(shape=(226,5))
Dra = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Dra.csv'))
Equ = numpy.zeros(shape=(15,5))
Equ = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Equ.csv'))
Eri = numpy.zeros(shape=(197,5))
Eri = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Eri.csv'))
For = numpy.zeros(shape=(64,5))
For = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','For.csv'))
Gem = numpy.zeros(shape=(123,5))
Gem = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Gem.csv'))
Gru = numpy.zeros(shape=(62,5))
Gru = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Gru.csv'))
Her = numpy.zeros(shape=(263,5))
Her = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Her.csv'))
Hor = numpy.zeros(shape=(36,5))
Hor = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Hor.csv'))
Hya = numpy.zeros(shape=(246,5))
Hya = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Hya.csv'))
Hyi = numpy.zeros(shape=(33,5))
Hyi = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Hyi.csv'))
Ind = numpy.zeros(shape=(39,5))
Ind = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ind.csv'))
Lac = numpy.zeros(shape=(67,5))
Lac = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lac.csv'))
Leo = numpy.zeros(shape=(130,5))
Leo = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Leo.csv'))
LMi = numpy.zeros(shape=(36,5))
LMi = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','LMi.csv'))
Lep = numpy.zeros(shape=(76,5))
Lep = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lep.csv'))
Lib = numpy.zeros(shape=(86,5))
Lib = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lib.csv'))
Lup = numpy.zeros(shape=(117,5))
Lup = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lup.csv'))
Lyn = numpy.zeros(shape=(100,5))
Lyn = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lyn.csv'))
Lyr = numpy.zeros(shape=(83,5))
Lyr = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lyr.csv'))
Men = numpy.zeros(shape=(26,5))
Men = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Men.csv'))
Mic = numpy.zeros(shape=(39,5))
Mic = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Mic.csv'))
Mon = numpy.zeros(shape=(153,5))
Mon = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Mon.csv'))
Mus = numpy.zeros(shape=(59,5))
Mus = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Mus.csv'))
Nor = numpy.zeros(shape=(41,5))
Nor = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Nor.csv'))
Oct = numpy.zeros(shape=(67,5))
Oct = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Oct.csv'))
Oph = numpy.zeros(shape=(179,5))
Oph = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Oph.csv'))
Ori = numpy.zeros(shape=(225,5))
Ori = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ori.csv'))
Pav = numpy.zeros(shape=(82,5))
Pav = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Pav.csv'))
Peg = numpy.zeros(shape=(176,5))
Peg = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Peg.csv'))
Per = numpy.zeros(shape=(160,5))
Per = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Per.csv'))
Phe = numpy.zeros(shape=(70,5))
Phe = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Phe.csv'))
Pic = numpy.zeros(shape=(50,5))
Pic = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Pic.csv'))
Psc = numpy.zeros(shape=(141,5))
Psc = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Psc.csv'))
PsA = numpy.zeros(shape=(49,5))
PsA = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','PsA.csv'))
Pup = numpy.zeros(shape=(275,5))
Pup = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Pup.csv'))
Pyx = numpy.zeros(shape=(48,5))
Pyx = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Pyx.csv'))
Ret = numpy.zeros(shape=(24,5))
Ret = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ret.csv'))
Sge = numpy.zeros(shape=(31,5))
Sge = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sge.csv'))
Sgr = numpy.zeros(shape=(219,5))
Sgr = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sgr.csv'))
Sco = numpy.zeros(shape=(174,5))
Sco = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sco.csv'))
Scl = numpy.zeros(shape=(59,5))
Scl = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Scl.csv'))
Sct = numpy.zeros(shape=(30,5))
Sct = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sct.csv'))
Ser = numpy.zeros(shape=(112,5))
Ser = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ser.csv'))
Sex = numpy.zeros(shape=(40,5))
Sex = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sex.csv'))
Tau = numpy.zeros(shape=(223,5))
Tau = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Tau.csv'))
Tel = numpy.zeros(shape=(51,5))
Tel = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Tel.csv'))
Tri = numpy.zeros(shape=(26,5))
Tri = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Tri.csv'))
TrA = numpy.zeros(shape=(35,5))
TrA = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','TrA.csv'))
Tuc = numpy.zeros(shape=(50,5))
Tuc = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Tuc.csv'))
UMa = numpy.zeros(shape=(224,5))
UMa = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','UMa.csv'))
UMi = numpy.zeros(shape=(42,5))
UMi = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','UMi.csv'))
Vel = numpy.zeros(shape=(193,5))
Vel = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Vel.csv'))
Vir = numpy.zeros(shape=(174,5))
Vir = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Vir.csv'))
Vol = numpy.zeros(shape=(33,5))
Vol = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Vol.csv'))
Vul = numpy.zeros(shape=(77,5))
Vul = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Vul.csv'))
# LROC WAC basemap Shapefile
Mare    = numpy.zeros(shape=(267482,5)) 
Mare    = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_mare.csv'))
Crater  = numpy.zeros(shape=(182111,5))
Crater  = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_crater.csv'))
# milkyway
MW_southernedge = numpy.zeros(shape=(263,4))
MW_southernedge = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_southernedge.csv'))
MW_MonPer       = numpy.zeros(shape=(71,4))
MW_MonPer       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_MonPer.csv'))
MW_CamCas       = numpy.zeros(shape=(13,4))
MW_CamCas       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_CamCas.csv'))
MW_Cep          = numpy.zeros(shape=(13,4))
MW_Cep          = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_Cep.csv'))
MW_CygOph       = numpy.zeros(shape=(40,4))
MW_CygOph       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_CygOph.csv'))
MW_OphSco       = numpy.zeros(shape=(17,4))
MW_OphSco       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_OphSco.csv'))
MW_LupVel       = numpy.zeros(shape=(78,4))
MW_LupVel       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LupVel.csv'))
MW_VelMon       = numpy.zeros(shape=(34,4))
MW_VelMon       = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_VelMon.csv'))
dark_PerCas     = numpy.zeros(shape=(35,4))
dark_PerCas     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_PerCas.csv'))
dark_CasCep     = numpy.zeros(shape=(28,4))
dark_CasCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CasCep.csv'))
dark_betaCas    = numpy.zeros(shape=(20,4))
dark_betaCas    = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_betaCas.csv'))
dark_CygCep     = numpy.zeros(shape=(22,4))
dark_CygCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CygCep.csv'))
dark_CygOph     = numpy.zeros(shape=(197,4))
dark_CygOph     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_CygOph.csv'))
dark_thetaOph   = numpy.zeros(shape=(28,4))
dark_thetaOph   = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_thetaOph.csv'))
dark_lambdaSco  = numpy.zeros(shape=(17,4))
dark_lambdaSco  = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_lambdaSco.csv'))
dark_ScoNor     = numpy.zeros(shape=(31,4))
dark_ScoNor     = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_ScoNor.csv'))
dark_Coalsack   = numpy.zeros(shape=(32,4))
dark_Coalsack   = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_Coalsack.csv'))
dark_Vel        = numpy.zeros(shape=(22,4))
dark_Vel        = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','dark_Vel.csv'))
MW_LMC1         = numpy.zeros(shape=(34,4))
MW_LMC1         = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LMC1.csv'))
MW_LMC2         = numpy.zeros(shape=(12,4))
MW_LMC2         = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_LMC2.csv'))
MW_SMC          = numpy.zeros(shape=(14,4))
MW_SMC          = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','MW_SMC.csv'))
# constellation boundaries
boundary        = numpy.zeros(shape=(13238,5))
boundary        = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','boundary.csv'))

if debug_mode == 1:
    timelog('ref count And: '+str(sys.getrefcount(And)))
    timelog('ref count Mare: '+str(sys.getrefcount(Mare)))
    timelog('ref count MW_southernedge: '+str(sys.getrefcount(MW_southernedge)))
    timelog('ref count boundary: '+str(sys.getrefcount(boundary)))
    
####################
# define functions #
####################

def plot_solar():
    global plot_alpha, hori_border, hori_xmax, hori_xmin, hori_ymax, hori_ymin, horizon_line, equator_line, ecliptic_line,\
           Sun, Moon, Mercury, Venus, Mars, Jupiter, Io, Europa, Ganymede, Callisto, Saturn, Uranus, Neptune,\
           solar_obj,solar_color,moon_chi,\
           Sun_x,Moon_x,Mercury_x,Venus_x,Mars_x,Jupiter_x,Saturn_x,Uranus_x,Neptune_x,\
           Sun_y,Moon_y,Mercury_y,Venus_y,Mars_y,Jupiter_y,Saturn_y,Uranus_y,Neptune_y

    Sun         = ephem.Sun()
    Sun.compute(Obs)
    Moon        = ephem.Moon()
    Moon.compute(Obs)
    Mercury     = ephem.Mercury()
    Mercury.compute(Obs)
    Venus       = ephem.Venus()
    Venus.compute(Obs)
    Mars        = ephem.Mars()
    Mars.compute(Obs)
    Jupiter     = ephem.Jupiter()
    Jupiter.compute(Obs)
    Io          = ephem.Io()
    Io.compute(Obs)
    Europa      = ephem.Europa()
    Europa.compute(Obs)
    Ganymede    = ephem.Ganymede()
    Ganymede.compute(Obs)
    Callisto    = ephem.Callisto()
    Callisto.compute(Obs)
    Saturn      = ephem.Saturn()
    Saturn.compute(Obs)  
    Uranus      = ephem.Uranus()
    Uranus.compute(Obs)
    Neptune     = ephem.Neptune()
    Neptune.compute(Obs)
    
    # position angle of the Moon's bright limb from North point of the disc of the Moon to East
    moon_chi = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Moon.ra),\
                                       math.sin(Sun.dec)*math.cos(Moon.dec)-math.cos(Sun.dec)*math.sin(Moon.dec)*math.cos(Sun.ra-Moon.ra)))
    if moon_chi < 0:
        moon_chi = moon_chi+360
 
    timelog('drawing grids')

    # alpha
    if math.degrees(Sun.alt) >= 0:
        plot_alpha = 0.2
    else:
        plot_alpha = 0.1
        
    # horizon
    for i in range(360):
        horizon.loc[i] = [i,math.degrees(math.atan(-math.cos(math.radians(ra0-i))/math.tan(math.radians(dec0)))),0,0]

    horizon.x = list(map(transform_x, horizon.RA, horizon.Dec))
    horizon.y = list(map(transform_y, horizon.RA, horizon.Dec))

    horizon_pt = []
    for i in range(len(horizon)-1):
        horizon_pt.append([horizon['x'].tolist()[i],horizon['y'].tolist()[i]])

    horizon_line = plt.Polygon(horizon_pt, closed=True, fill=None, edgecolor=(0,1,0,1), zorder=1+2.5)
    ax0.add_patch(horizon_line)

    # horizon size
    hori_xmax = max(horizon.x)
    hori_xmin = min(horizon.x)
    hori_ymax = max(horizon.y)
    hori_ymin = min(horizon.y)
    hori_border = hori_xmax-hori_xmin
    
    ax0.annotate('z',((hori_xmax+hori_xmin)/2+2.5,(hori_ymax+hori_ymin)/2+1),color='g')
    z_m = matplotlib.markers.MarkerStyle(marker='+')
    z_m._transform = z_m.get_transform().rotate_deg(rotate_angle)
    ax0.scatter((hori_xmax+hori_xmin)/2,(hori_ymax+hori_ymin)/2,c='g',marker=z_m)
    
    # equator
    equator['RA'] = numpy.arange(len(equator))

    equator.x = list(map(transform_x, equator.RA, equator.Dec))
    equator.y = list(map(transform_y, equator.RA, equator.Dec))

    equator_pt = []
    for i in range(len(equator)-1):
        if (equator['x'].tolist()[i]-x_shift)**2 < (hori_border/2)**2-((equator['y'].tolist()[i]-y_shift)/aspect_ratio)**2:
            equator_pt.append([equator['x'].tolist()[i],equator['y'].tolist()[i]])
    
    equator_line = plt.Polygon(sorted(equator_pt), closed=False, fill=None, edgecolor=(1,0,0,plot_alpha), zorder=1+2.5)
    ax0.add_patch(equator_line)

    # ecliptic
    epsilon_J2000 = 23.4392911
    for i in range(360):
        ecliptic.loc[i] = [math.degrees(math.atan2(math.sin(math.radians(i))*math.cos(math.radians(epsilon_J2000)),math.cos(math.radians(i)))),\
                           math.degrees(math.asin(math.sin(math.radians(epsilon_J2000))*math.sin(math.radians(i)))),0,0]

    ecliptic.x = list(map(transform_x, ecliptic.RA, ecliptic.Dec))
    ecliptic.y = list(map(transform_y, ecliptic.RA, ecliptic.Dec))

    ecliptic_pt = []
    for i in range(len(ecliptic)-1):
        if (ecliptic['x'].tolist()[i]-x_shift)**2 < (hori_border/2)**2-((ecliptic['y'].tolist()[i]-y_shift)/aspect_ratio)**2:
            ecliptic_pt.append([ecliptic['x'].tolist()[i],ecliptic['y'].tolist()[i]])
            
    ecliptic_line = plt.Polygon(sorted(ecliptic_pt), closed=False, fill=None, edgecolor=(1,1,0,plot_alpha), zorder=1+2.5)
    ax0.add_patch(ecliptic_line)   
    
    timelog('plotting solar system objects')
           
    Sun_x       = transform_x(math.degrees(Sun.ra),math.degrees(Sun.dec))
    Sun_y       = transform_y(math.degrees(Sun.ra),math.degrees(Sun.dec))
    Moon_x      = transform_x(math.degrees(Moon.ra),math.degrees(Moon.dec))
    Moon_y      = transform_y(math.degrees(Moon.ra),math.degrees(Moon.dec))
    Mercury_x   = transform_x(math.degrees(Mercury.ra),math.degrees(Mercury.dec))
    Mercury_y   = transform_y(math.degrees(Mercury.ra),math.degrees(Mercury.dec))
    Venus_x     = transform_x(math.degrees(Venus.ra),math.degrees(Venus.dec))
    Venus_y     = transform_y(math.degrees(Venus.ra),math.degrees(Venus.dec))
    Mars_x      = transform_x(math.degrees(Mars.ra),math.degrees(Mars.dec))
    Mars_y      = transform_y(math.degrees(Mars.ra),math.degrees(Mars.dec))
    Jupiter_x   = transform_x(math.degrees(Jupiter.ra),math.degrees(Jupiter.dec))
    Jupiter_y   = transform_y(math.degrees(Jupiter.ra),math.degrees(Jupiter.dec))
    Saturn_x    = transform_x(math.degrees(Saturn.ra),math.degrees(Saturn.dec))
    Saturn_y    = transform_y(math.degrees(Saturn.ra),math.degrees(Saturn.dec))
    Uranus_x    = transform_x(math.degrees(Uranus.ra),math.degrees(Uranus.dec))
    Uranus_y    = transform_y(math.degrees(Uranus.ra),math.degrees(Uranus.dec))
    Neptune_x   = transform_x(math.degrees(Neptune.ra),math.degrees(Neptune.dec))
    Neptune_y   = transform_y(math.degrees(Neptune.ra),math.degrees(Neptune.dec))

    solar_pos_x = [Sun_x,Moon_x,Mercury_x,Venus_x,Mars_x,Jupiter_x,Saturn_x,Uranus_x,Neptune_x]
    solar_pos_y = [Sun_y,Moon_y,Mercury_y,Venus_y,Mars_y,Jupiter_y,Saturn_y,Uranus_y,Neptune_y]
    solar_color = ['#FFCC33','#DAD9D7','#97979F','#C18F17','#E27B58','#C88B3A','#A49B72','#D5FBFC','#3E66F9']

    solar_obj = ax0.scatter(solar_pos_x,solar_pos_y,alpha=plot_alpha+0.25,color=solar_color,zorder=4+2.5)
    
    ax0.annotate('$\u263C$',(Sun_x+2.5,Sun_y+1),color=solar_color[0])
    if moon_chi>180:
        ax0.annotate('$\u263D$',(Moon_x+2.5,Moon_y+1),color=solar_color[1])
    else:
        ax0.annotate('$\u263E$',(Moon_x+2.5,Moon_y+1),color=solar_color[1])
    ax0.annotate('$\u263F$',(Mercury_x+2.5,Mercury_y+1),color=solar_color[2])
    ax0.annotate('$\u2640$',(Venus_x+2.5,Venus_y+1),color=solar_color[3])
    ax0.annotate('$\u2642$',(Mars_x+2.5,Mars_y+1),color=solar_color[4])
    ax0.annotate('$\u2643$',(Jupiter_x+2.5,Jupiter_y+1),color=solar_color[5])
    ax0.annotate('$\u2644$',(Saturn_x+2.5,Saturn_y+1),color=solar_color[6])
    ax0.annotate('$\u2645$',(Uranus_x+2.5,Uranus_y+1),color=solar_color[7])
    ax0.annotate('$\u2646$',(Neptune_x+2.5,Neptune_y+1),color=solar_color[8])

    if debug_mode == 1:
        timelog('ref count horizon_line: '+str(sys.getrefcount(horizon_line)))
        timelog('ref count equator_line: '+str(sys.getrefcount(equator_line)))
        timelog('ref count ecliptic_pt: '+str(sys.getrefcount(ecliptic_pt)))
        timelog('ref count ecliptic_line: '+str(sys.getrefcount(ecliptic_line)))
        timelog('ref count Sun_x: '+str(sys.getrefcount(Sun_x)))
        timelog('ref count Sun_y: '+str(sys.getrefcount(Sun_y)))
        timelog('ref count solar_pos_x: '+str(sys.getrefcount(solar_pos_x)))
        timelog('ref count solar_pos_y: '+str(sys.getrefcount(solar_pos_y)))
        timelog('ref count solar_color: '+str(sys.getrefcount(solar_color)))
        timelog('ref count solar_obj: '+str(sys.getrefcount(solar_obj)))

def plot_constellation():
    global constellation_list, lc_west, lc_west_z, lc_west_dotted, labelxy
    
    timelog('drawing constellations')
    
    constellation_list = [And,Ant,Aps,Aqr,Aql,Ara,Ari,Aur,Boo,Cae,Cam,Cnc,CVn,CMa,CMi,Cap,Car,Cas,Cen,Cep,\
                          Cet,Cha,Cir,Col,Com,CrA,CrB,Crv,Crt,Cru,Cyg,Del,Dor,Dra,Equ,Eri,For,Gem,Gru,Her,\
                          Hor,Hya,Hyi,Ind,Lac,Leo,LMi,Lep,Lib,Lup,Lyn,Lyr,Men,Mic,Mon,Mus,Nor,Oct,Oph,Ori,\
                          Pav,Peg,Per,Phe,Pic,Psc,PsA,Pup,Pyx,Ret,Sge,Sgr,Sco,Scl,Sct,Ser,Sex,Tau,Tel,Tri,\
                          TrA,Tuc,UMa,UMi,Vel,Vir,Vol,Vul]
    
    for df in constellation_list:
        df.x = list(map(transform_x, df.RA, df.Dec))
        df.y = list(map(transform_y, df.RA, df.Dec))

    labelxy = 2
    
    And_line = [[0,3],[1,3],[1,7],[1,9],[2,9],[3,13],[3,14],[5,10],[7,18],[8,14],[10,19],[11,18],[16,19],[13,16]]
    Ant_line = [[0,2],[0,3],[1,3]]        
    Aps_line = [[0,3],[1,2],[1,3]]
    Aqr_line = [[0,1],[0,5],[1,6],[1,10],[2,8],[3,7],[3,18],[4,8],[4,9],[4,12],[6,17],[7,30],[9,17],[10,13],[11,12],\
                [11,14],[14,31],[19,30],[19,31],[21,22]]
    Aql_line = [[0,1],[0,4],[0,6],[2,4],[3,7],[4,5],[4,7]]
    Ara_line = [[0,1],[0,2],[0,3],[2,6],[3,4]]
    Ari_line = [[0,1],[0,2]]
    Aur_line = [[0,1],[0,3],[0,4],[1,2],[4,5],[4,7]]
    Boo_line = [[0,1],[0,2],[0,6],[0,11],[2,4],[3,5],[3,6],[4,5]]
    Cae_line = [[0,2]]
    Cam_line = [[0,2],[0,4],[1,7],[2,7]]
    Cnc_line = [[0,1],[1,2],[1,3]]
    CVn_line = [[0,1]]
    CMa_line = [[0,3],[0,6],[0,12],[0,13],[1,7],[2,6],[2,7],[2,8],[4,8],[12,13]]
    CMi_line = [[0,1]]
    Cap_line = [[0,3],[0,4],[1,2],[1,7],[2,5],[3,9],[4,10],[5,9],[6,7],[6,10]]
    Car_line = [[0,10],[2,10],[2,14],[3,11],[3,14],[4,6],[4,15],[8,11],[8,13],[12,13],[12,15]]
    Cas_line = [[0,1],[0,2],[2,3],[3,4]]
    Cen_line = [[0,5],[1,5],[3,6],[3,7],[4,5],[4,8],[5,7],[6,12],[8,18],[11,18]]
    Cep_line = [[0,2],[0,3],[0,4],[1,2],[1,5],[3,5],[3,6]]
    Cet_line = [[0,3],[0,5],[0,6],[1,4],[1,18],[2,4],[2,8],[3,7],[4,25],[5,8],[7,8],[12,13],[12,18],[13,25]]
    Cha_line = [[0,1]]
    Cir_line = [[0,1],[0,2]]
    Col_line = [[0,1],[0,3],[1,4],[1,2]]
    Com_line = [[0,1],[0,19]]
    CrA_line = [[0,1],[0,6],[1,2],[2,4],[3,4],[5,6]]
    CrB_line = [[1,2],[1,3],[2,4],[3,6],[5,6],[5,10]]
    Crv_line = [[0,2],[0,3],[1,2],[1,3],[3,4]]
    Crt_line = [[0,1],[0,2],[0,6],[1,3],[2,3],[2,5],[4,6]]
    Cru_line = [[0,4],[1,2]]
    Cyg_line = [[0,1],[1,2],[1,3],[1,11],[2,5],[3,9],[4,11],[8,9]]
    Del_line = [[0,1],[0,2],[0,4],[1,3],[3,4]]
    Dor_line = [[0,1],[0,2],[1,3]]
    Dra_line = [[0,2],[0,8],[1,4],[1,5],[2,29],[3,8],[3,9],[4,6],[5,7],[6,9],[7,11],[8,29],[10,11]]
    Equ_line = [[0,2],[0,3],[1,2],[1,3]]
    Eri_line = [[0,8],[1,24],[1,27],[2,4],[2,16],[3,18],[3,22],[4,9],[5,8],[5,21],[6,14],[6,19],[7,17],[7,23],[9,12],\
                [10,14],[10,20],[12,30],[13,15],[13,16],[15,27],[17,30],[18,21],[19,22],[20,23]]
    For_line = [[0,1],[1,7]]
    Gem_line = [[0,8],[1,12],[3,5],[3,6],[4,5],[7,10],[8,10],[8,12],[9,13],[11,13]]
    Gru_line = [[0,1],[0,2],[0,5],[1,3],[1,4],[4,5]]
    Her_line = [[0,1],[0,5],[0,8],[1,6],[1,14],[2,4],[2,14],[3,6],[3,12],[3,14],[4,7],[6,13],[7,10],[9,12],[10,11]]
    Hor_line = [[0,3],[0,6],[0,9]]
    Hya_line = [[0,11],[0,12],[1,4],[1,14],[2,5],[2,9],[3,6],[3,8],[4,18],[5,13],[5,17],[6,14],[7,8],[7,12],[9,11],\
                [13,19],[15,17],[15,19]]
    Hyi_line = [[0,2],[0,4],[1,5],[3,4],[3,5]]
    Ind_line = [[0,2],[1,2]]
    Lac_line = [[0,2],[0,3],[1,5],[2,4],[4,5]]
    Leo_line = [[0,5],[0,7],[0,8],[0,10],[1,2],[1,5],[2,17],[3,6],[3,8],[3,17],[4,11],[5,12],[6,11]]
    LMi_line = [[0,1],[1,2]]
    Lep_line = [[0,1],[0,3],[0,4],[1,5],[1,12],[2,12],[3,8],[3,9],[4,6],[5,7],[9,10]]
    Lib_line = [[0,1],[0,2],[0,5],[1,2],[2,3],[3,4],[5,6]]
    Lup_line = [[0,1],[0,5],[0,7],[1,3],[2,3],[2,4],[2,6],[3,8],[4,5],[6,10]]
    Lyn_line = [[0,1],[1,2],[2,3],[3,7],[4,5],[4,7]]
    Lyr_line = [[0,6],[0,12],[1,2],[1,4],[2,6],[4,6],[6,12]]
    Men_line = [[0,1],[0,2],[1,4]]
    Mic_line = [[0,1],[0,3],[1,2],[3,5]]
    Mon_line = [[0,2],[1,5],[2,3],[2,5],[4,6],[5,6],[5,7]]
    Mus_line = [[0,1],[0,2],[0,4],[0,5],[3,5]]
    Nor_line = [[0,1],[0,7],[3,7]]
    Oct_line = [[0,2],[1,2]]
    Oph_line = [[0,5],[0,9],[1,2],[1,7],[1,12],[2,6],[3,6],[3,11],[5,11],[9,12]]
    Ori_line = [[0,5],[0,6],[1,4],[1,10],[1,17],[2,6],[2,10],[2,34],[3,4],[3,6],[4,5],[8,12],[8,21],[12,13],[13,26],\
                [17,27],[21,34],[23,24],[23,33],[24,27],[27,33]]
    Pav_line = [[0,1],[1,2],[2,3],[3,4]]
    Peg_line = [[0,7],[1,2],[1,4],[1,6],[2,3],[2,5],[5,7],[6,9],[8,9]]
    Per_line = [[0,4],[0,5],[0,9],[1,6],[1,9],[2,10],[2,12],[3,5],[3,12],[4,7],[5,13],[6,18],[13,17],[17,21]]
    Phe_line = [[0,1],[0,3],[1,2],[1,4],[2,6],[2,8],[3,7],[3,10],[4,7],[10,11],[11,16]]
    Pic_line = [[0,2],[1,2]]
    Psc_line = [[0,4],[0,34],[1,6],[1,21],[2,3],[2,9],[3,6],[3,11],[4,7],[5,9],[5,19],[7,10],[10,19],[11,21],[18,12],\
                [18,34]]
    PsA_line = [[0,1],[0,2],[1,13],[2,5],[3,5],[3,7],[4,7],[4,13]]
    Pup_line = [[0,2],[0,10],[1,4],[1,29],[2,11],[2,13],[3,4],[5,10],[6,11],[6,21],[10,14],[13,33],[21,28],[28,29]]
    Pyx_line = [[0,1],[0,2]]
    Ret_line = [[0,1],[0,2],[1,4],[2,6],[4,6]]
    Sge_line = [[0,1],[1,2],[1,3]]
    Sgr_line = [[0,2],[0,3],[0,6],[0,7],[1,8],[1,9],[1,11],[2,8],[2,9],[3,4],[3,6],[3,8],[4,8],[4,12],[5,11],\
                [5,36],[6,20],[9,23],[10,11],[13,24],[13,36],[14,16],[16,17],[16,18],[18,22],[22,27],[23,27]]
    Sco_line = [[0,8],[0,10],[1,5],[2,11],[2,14],[3,8],[3,12],[4,6],[4,9],[4,10],[14,16],[5,7],[5,11],[9,17],[12,16]]
    Scl_line = [[0,3],[1,2],[2,3]]
    Sct_line = [[0,1],[0,2],[0,3],[1,6],[3,4],[4,6]]
    Ser_line = [[0,5],[0,7],[1,10],[2,5],[3,10],[4,7],[4,8],[4,9],[8,9]]
    Sex_line = [[0,1],[0,2]]
    Tau_line = [[0,3],[0,4],[1,6],[4,9],[5,9],[5,11],[6,12],[7,11],[9,12]]
    Tel_line = [[0,1],[0,2]]
    Tri_line = [[0,1],[0,2],[1,2]]
    TrA_line = [[0,1],[0,2],[1,4],[2,4]]
    Tuc_line = [[0,1],[0,4],[1,3],[1,9],[2,3],[2,9]]
    UMa_line = [[0,3],[0,10],[1,4],[1,10],[1,15],[2,3],[4,5],[4,17],[5,10],[5,16],[6,7],[6,12],[6,16],[8,9],[9,14],\
                [9,17],[11,15],[11,17]]
    UMi_line = [[0,6],[1,2],[1,5],[2,9],[3,5],[3,6],[5,9]]
    Vel_line = [[0,8],[0,15],[1,3],[1,8],[2,7],[2,14],[3,6],[4,6],[4,11],[7,12],[11,12],[14,15]]
    Vir_line = [[0,2],[0,13],[0,15],[1,3],[2,3],[2,14],[3,5],[4,9],[4,10],[5,9],[5,15],[7,14],[8,11],[10,18],[11,13],\
                [12,18]]
    Vol_line = [[0,4],[0,5],[1,2],[1,3],[2,5],[3,5]]
    Vul_line = [[0,2],[0,5]]
    
    constellation_line = [[And.x,And.y,And_line,'And'],[Ant.x,Ant.y,Ant_line,'Ant'],[Aps.x,Aps.y,Aps_line,'Aps'],[Aqr.x,Aqr.y,Aqr_line,'$\u2652$'],\
                          [Aql.x,Aql.y,Aql_line,'Aql'],[Ara.x,Ara.y,Ara_line,'Ara'],[Ari.x,Ari.y,Ari_line,'$\u2648$'],[Aur.x,Aur.y,Aur_line,'Aur'],\
                          [Boo.x,Boo.y,Boo_line,'Boo'],[Cae.x,Cae.y,Cae_line,'Cae'],[Cam.x,Cam.y,Cam_line,'Cam'],[Cnc.x,Cnc.y,Cnc_line,'$\u264B$'],\
                          [CVn.x,CVn.y,CVn_line,'CVn'],[CMa.x,CMa.y,CMa_line,'CMa'],[CMi.x,CMi.y,CMi_line,'CMi'],[Cap.x,Cap.y,Cap_line,'$\u2651$'],\
                          [Car.x,Car.y,Car_line,'Car'],[Cas.x,Cas.y,Cas_line,'Cas'],[Cen.x,Cen.y,Cen_line,'Cen'],[Cep.x,Cep.y,Cep_line,'Cep'],\
                          [Cet.x,Cet.y,Cet_line,'Cet'],[Cha.x,Cha.y,Cha_line,'Cha'],[Cir.x,Cir.y,Cir_line,'Cir'],[Col.x,Col.y,Col_line,'Col'],\
                          [Com.x,Com.y,Com_line,'Com'],[CrA.x,CrA.y,CrA_line,'CrA'],[CrB.x,CrB.y,CrB_line,'CrB'],[Crv.x,Crv.y,Crv_line,'Crv'],\
                          [Crt.x,Crt.y,Crt_line,'Crt'],[Cru.x,Cru.y,Cru_line,'Cru'],[Cyg.x,Cyg.y,Cyg_line,'Cyg'],[Del.x,Del.y,Del_line,'Del'],\
                          [Dor.x,Dor.y,Dor_line,'Dor'],[Dra.x,Dra.y,Dra_line,'Dra'],[Equ.x,Equ.y,Equ_line,'Equ'],[Eri.x,Eri.y,Eri_line,'Eri'],\
                          [For.x,For.y,For_line,'For'],[Gem.x,Gem.y,Gem_line,'$\u264A$'],[Gru.x,Gru.y,Gru_line,'Gru'],[Her.x,Her.y,Her_line,'Her'],\
                          [Hor.x,Hor.y,Hor_line,'Hor'],[Hya.x,Hya.y,Hya_line,'Hya'],[Hyi.x,Hyi.y,Hyi_line,'Hyi'],[Ind.x,Ind.y,Ind_line,'Ind'],\
                          [Lac.x,Lac.y,Lac_line,'Lac'],[Leo.x,Leo.y,Leo_line,'$\u264C$'],[LMi.x,LMi.y,LMi_line,'LMi'],[Lep.x,Lep.y,Lep_line,'Lep'],\
                          [Lib.x,Lib.y,Lib_line,'$\u264E$'],[Lup.x,Lup.y,Lup_line,'Lup'],[Lyn.x,Lyn.y,Lyn_line,'Lyn'],[Lyr.x,Lyr.y,Lyr_line,'Lyr'],\
                          [Men.x,Men.y,Men_line,'Men'],[Mic.x,Mic.y,Mic_line,'Mic'],[Mon.x,Mon.y,Mon_line,'Mon'],[Mus.x,Mus.y,Mus_line,'Mus'],\
                          [Nor.x,Nor.y,Nor_line,'Nor'],[Oct.x,Oct.y,Oct_line,'Oct'],[Oph.x,Oph.y,Oph_line,'Oph'],[Ori.x,Ori.y,Ori_line,'Ori'],\
                          [Pav.x,Pav.y,Pav_line,'Pav'],[Peg.x,Peg.y,Peg_line,'Peg'],[Per.x,Per.y,Per_line,'Per'],[Phe.x,Phe.y,Phe_line,'Phe'],\
                          [Pic.x,Pic.y,Pic_line,'Pic'],[Psc.x,Psc.y,Psc_line,'$\u2653$'],[PsA.x,PsA.y,PsA_line,'PsA'],[Pup.x,Pup.y,Pup_line,'Pup'],\
                          [Pyx.x,Pyx.y,Pyx_line,'Pyx'],[Ret.x,Ret.y,Ret_line,'Ret'],[Sge.x,Sge.y,Sge_line,'Sge'],[Sgr.x,Sgr.y,Sgr_line,'$\u2650$'],\
                          [Sco.x,Sco.y,Sco_line,'$\u264F$'],[Scl.x,Scl.y,Scl_line,'Scl'],[Sct.x,Sct.y,Sct_line,'Sct'],[Ser.x,Ser.y,Ser_line,'Ser'],\
                          [Sex.x,Sex.y,Sex_line,'Sex'],[Tau.x,Tau.y,Tau_line,'$\u2649$'],[Tel.x,Tel.y,Tel_line,'Tel'],[Tri.x,Tri.y,Tri_line,'Tri'],\
                          [TrA.x,TrA.y,TrA_line,'TrA'],[Tuc.x,Tuc.y,Tuc_line,'Tuc'],[UMa.x,UMa.y,UMa_line,'UMa'],[UMi.x,UMi.y,UMi_line,'UMi'],\
                          [Vel.x,Vel.y,Vel_line,'Vel'],[Vir.x,Vir.y,Vir_line,'$\u264D$'],[Vol.x,Vol.y,Vol_line,'Vol'],[Vul.x,Vul.y,Vul_line,'Vul']]

    # constellation linecollection
    constellation_line_z_xy1 = [] # (x,y) pair of vertics 1
    constellation_line_z_xy2 = [] # (x,y) pair of vertics 2
    constellation_line_xy1 = []
    constellation_line_xy2 = []
    for i in range(len(constellation_line)):
        for j in range(len(constellation_line[i][2])):
            if math.hypot(constellation_line[i][0][constellation_line[i][2][j][0]]-constellation_line[i][0][constellation_line[i][2][j][1]],\
                          constellation_line[i][1][constellation_line[i][2][j][0]]-constellation_line[i][1][constellation_line[i][2][j][1]]) < hori_border/2:
                if i in set([3,6,11,15,37,45,48,58,65,71,72,77,85]): # zodiacs
                    constellation_line_z_xy1.append([(constellation_line[i][0][constellation_line[i][2][j][0]]),(constellation_line[i][1][constellation_line[i][2][j][0]])])
                    constellation_line_z_xy2.append([(constellation_line[i][0][constellation_line[i][2][j][1]]),(constellation_line[i][1][constellation_line[i][2][j][1]])])
                else:
                    constellation_line_xy1.append([(constellation_line[i][0][constellation_line[i][2][j][0]]),(constellation_line[i][1][constellation_line[i][2][j][0]])])
                    constellation_line_xy2.append([(constellation_line[i][0][constellation_line[i][2][j][1]]),(constellation_line[i][1][constellation_line[i][2][j][1]])])

    constellation_line_z_list = zip(constellation_line_z_xy1,constellation_line_z_xy2)
    constellation_line_list = zip(constellation_line_xy1,constellation_line_xy2)
    
    lc_west_z = mc.LineCollection(constellation_line_z_list, colors='yellow', zorder=10+2.5)
    lc_west = mc.LineCollection(constellation_line_list, colors='white', zorder=10+2.5)
    lc_west_z.set_alpha(plot_alpha)
    lc_west.set_alpha(plot_alpha)
    ax0.add_collection(lc_west_z)
    ax0.add_collection(lc_west)

   # others linecollection       
    constellation_dotted_line = [[(Aur.x[3],Aur.y[3]),(Tau.x[1],Tau.y[1])],[(Aur.x[2],Aur.y[2]),(Tau.x[1],Tau.y[1])],\
                                 [(Peg.x[1],Peg.y[1]),(And.x[0],And.y[0])],[(Peg.x[3],Peg.y[3]),(And.x[0],And.y[0])],\
                                 [(Ser.x[3],Ser.y[3]),(Oph.x[7],Oph.y[7])],[(Ser.x[2],Ser.y[2]),(Oph.x[3],Oph.y[3])],\
                                 [(PsA.x[0],PsA.y[0]),(Aqr.x[18],Aqr.y[18])]]

    constellation_dotted_line_list = []
    for i in range(len(constellation_dotted_line)):
        if math.hypot(constellation_dotted_line[i][0][0]-constellation_dotted_line[i][1][0],\
                      constellation_dotted_line[i][0][1]-constellation_dotted_line[i][1][1]) < hori_border/2:
            constellation_dotted_line_list.append(constellation_dotted_line[i])
    
    lc_west_dotted = mc.LineCollection(constellation_dotted_line_list, colors='white', linestyles='dashed',zorder=10+2.5)
    lc_west_dotted.set_alpha(plot_alpha)
    ax0.add_collection(lc_west_dotted)

    # annotation
    for x,y,z,n in constellation_line:
        if math.hypot(numpy.mean(x)-x_shift,numpy.mean(y)-y_shift) \
           < math.sqrt(((hori_border/2)**2)-(1-aspect_ratio**2)*((numpy.mean(y)-y_shift)/aspect_ratio)**2) \
           and max(x)-min(x) < hori_border:
            if n in set(['$\u2652$','$\u2648$','$\u264B$','$\u2651$','$\u264A$','$\u264C$','$\u264E$','$\u2653$','$\u2650$','$\u264F$','$\u2649$','$\u264D$']):
                ax0.annotate(str(n),(numpy.mean(x),numpy.mean(y)-labelxy),color='y')

    if debug_mode == 1:
        timelog('ref count constellation_list: '+str(sys.getrefcount(constellation_list)))
        timelog('ref count labelxy: '+str(sys.getrefcount(labelxy)))
        timelog('ref count And_line: '+str(sys.getrefcount(And_line)))
        timelog('ref count constellation_line: '+str(sys.getrefcount(constellation_line)))
        timelog('ref count constellation_line_z_xy1: '+str(sys.getrefcount(constellation_line_z_xy1)))
        timelog('ref count constellation_line_z_xy2: '+str(sys.getrefcount(constellation_line_z_xy2)))
        timelog('ref count constellation_line_xy1: '+str(sys.getrefcount(constellation_line_xy1)))
        timelog('ref count constellation_line_xy2: '+str(sys.getrefcount(constellation_line_xy2)))
        timelog('ref count constellation_line_z_list: '+str(sys.getrefcount(constellation_line_z_list)))
        timelog('ref count constellation_line_list: '+str(sys.getrefcount(constellation_line_list)))
        timelog('ref count lc_west_z: '+str(sys.getrefcount(lc_west_z)))
        timelog('ref count lc_west: '+str(sys.getrefcount(lc_west)))
        timelog('ref count constellation_dotted_line: '+str(sys.getrefcount(constellation_dotted_line)))
        timelog('ref count constellation_dotted_line_list: '+str(sys.getrefcount(constellation_dotted_line_list)))
        timelog('ref count lc_west_dotted: '+str(sys.getrefcount(lc_west_dotted)))
        
def plot_MW():
    timelog('weaving Milkyway')
    
    MW_list = [MW_southernedge,MW_MonPer,MW_CamCas,MW_Cep,MW_CygOph,MW_OphSco,MW_LupVel,MW_VelMon,\
               dark_PerCas,dark_CasCep,dark_betaCas,dark_CygCep,dark_CygOph,dark_thetaOph,dark_lambdaSco,dark_ScoNor,dark_Coalsack,dark_Vel,\
               MW_LMC1,MW_LMC2,MW_SMC]

    MW_line_list = []
    for df in MW_list:
        df.x = list(map(transform_x, df.RA, df.Dec))
        df.y = list(map(transform_y, df.RA, df.Dec))
        for i in range(len(df)-1):
            if (df.x[i]-x_shift)**2 < (hori_border/2)**2-((df.y[i]-y_shift)/aspect_ratio)**2:
                MW_line_list.append([(df.x[i],df.y[i]),(df.x[i+1],df.y[i+1])])

    lc_MW = mc.LineCollection(MW_line_list, colors='b',alpha=plot_alpha/4, zorder=1+2.5)
    ax0.add_collection(lc_MW)

    if debug_mode == 1:
        timelog('ref count MW_list: '+str(sys.getrefcount(MW_list)))
        timelog('ref count MW_line_list: '+str(sys.getrefcount(MW_line_list)))
        timelog('ref count lc_MW: '+str(sys.getrefcount(lc_MW)))

def plot_boundary():
    timelog('drawing boundaries')
    
    boundary.x = list(map(transform_x, boundary.RA*15, boundary.Dec)) #convert RA to degrees
    boundary.y = list(map(transform_y, boundary.RA*15, boundary.Dec))
    
    boundary['xy'] = list(zip(boundary.x,boundary.y))
    boundary_pt_list = boundary.groupby('Constellation')['xy'].apply(pandas.Series.tolist).tolist()
    
#     boundary_line_list = []
#     for i in range(len(boundary)-1):
#         if (boundary.x[i]-x_shift)**2 < (hori_border/2)**2-((boundary.y[i]-y_shift)/aspect_ratio)**2 and \
#            (boundary.x[i+1]-x_shift)**2 < (hori_border/2)**2-((boundary.y[i+1]-y_shift)/aspect_ratio)**2 and \
#            boundary.Constellation[i] == boundary.Constellation[i+1]:
#             boundary_line_list.append([(boundary.x[i],boundary.y[i]),(boundary.x[i+1],boundary.y[i+1])])

    pc_boundary = mc.PolyCollection(boundary_pt_list, closed=True, facecolors=[0,0,0,0], edgecolors=[1,0.5,0,plot_alpha/2], zorder=1+2.5)
    pc_boundary.set_clip_path(horizon_line)
    ax0.add_collection(pc_boundary)

    if debug_mode == 1:
        timelog('ref count boundary.x: '+str(sys.getrefcount(boundary.x)))
        timelog('ref count boundary.y: '+str(sys.getrefcount(boundary.y)))
        timelog('ref count boundary_line_list: '+str(sys.getrefcount(boundary_line_list)))
        timelog('ref count lc_boundary: '+str(sys.getrefcount(lc_boundary)))
 
def write_label():
    timelog('timestamp')
    
    ax0.annotate('N',(hori_xmin,hori_ymin+10),color='w')
    ax0.annotate(str(Obs.lat),(hori_xmin+65,hori_ymin+10),ha='right',color='w')
    ax0.annotate('E',(hori_xmin,hori_ymin),color='w')
    ax0.annotate(str(Obs.lon),(hori_xmin+65,hori_ymin),ha='right',color='w')
    ax0.annotate('Ho Koon Nature Education cum\nAstronomical Centre',(hori_xmax,hori_ymax),ha='right',va='top',color='w')
    ax0.annotate('sky at HKT '+str(ephem.localtime(Obs.date).strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax,hori_ymin),ha='right',color='w')
    ax0.annotate('astronomical computations by PyEphem',(360,hori_ymin),rotation=90,ha='right',va='bottom',color='dimgrey')

    # BesutifulSoup, for temp & RH
    try:
        link_w = 'http://www.weather.gov.hk/wxinfo/ts/text_readings_e.htm'
        html_w = requests.get(link_w).text
        soup_w = BeautifulSoup(html_w, 'html.parser')
    except:
        pass

    #RSS from HKO, for UV
    try:
        feed = feedparser.parse('https://rss.weather.gov.hk/rss/CurrentWeather.xml')
        urlretrieve(re.search('(?P<url>https?://[^\s"\"]+)', feed.entries[0]['summary']).group('url'), 'weather_icon.png')
        weather_icon = Image.open('weather_icon.png')
        ax0.imshow(weather_icon, extent=(310,360,190,240))
    except:
        pass

    # BesutifulSoup, for sunspot
    try:
        link_s = 'http://spaceweather.com/'
        html_s = requests.get(link_s).text
        soup_s = BeautifulSoup(html_s, 'html.parser')
    except:
        pass

    #temp
    try:
        HK_temp = re.search(r'(.*Tsuen\sWan\sHo\sKoon.*)', soup_w.get_text()).group(0).split()[4]
        
        temp_cmap = matplotlib.cm.get_cmap('coolwarm')
        ax0.annotate('air temp.: ',(310,190),ha='left',va='top',fontproperties=DjV_S_8,color='darkgrey')
        ax0.annotate(HK_temp+'$\u00B0$C',(360,184),ha='right',va='top',fontproperties=DjV_S_12,\
                     color=temp_cmap(numpy.clip(float(HK_temp)/40,0,1)))

        # record temp
        CC_hokoon.update(pandas.DataFrame({'temp':float(HK_temp)},index=[CC_hokoon.index[-1]]))
    except:
        ax0.annotate('Maintenance',(360,184),ha='right',va='top',fontproperties=DjV_S_12,color='r')

    #RH
    try:
        HK_RH = re.search(r'(.*Tsuen\sWan\sHo\sKoon.*)', soup_w.get_text()).group(0).split()[5]
        
        ax0.annotate('R.H.: ',(310,170),ha='left',va='top',fontproperties=DjV_S_8,color='darkgrey')
        RH_wedge = patches.Wedge((328,160),4,(100-float(HK_RH))/100*360+90,360+90,width=2,edgecolor='none')
        ax0.add_patch(RH_wedge)
        ax0.annotate(HK_RH+'%',(360,164),ha='right',va='top',fontproperties=DjV_S_12,color='w')

    except:
        ax0.annotate('Maintenance',(360,164),ha='right',va='top',fontproperties=DjV_S_12,color='r')

    #UV
    try:
        HK_UV = re.search(r'(.*)Intensity of UV radiation : (.*?) .*', feed.entries[0]['summary']).group(2).replace('<br/>','').replace('<br','')
        ax0.annotate('UV intensity: ',(310,150),ha='left',va='top',fontproperties=DjV_S_8,color='darkgrey')
        ax0.annotate(str(HK_UV),(360,144),ha='right',va='top',fontproperties=DjV_S_12,color='w')
        if str(HK_UV) == 'high':
            ax0.annotate('(⌐■_■)☂',(335,134),ha='center',va='top',fontproperties=DjV_S_12,color='w')
        elif str(HK_UV) == 'moderate':
            ax0.annotate('(⌐■_■)',(335,134),ha='center',va='top',fontproperties=DjV_S_12,color='w')
        elif str(HK_UV) == 'low':
            ax0.annotate('(⌐⊡_⊡)',(335,134),ha='center',va='top',fontproperties=DjV_S_12,color='w')
        elif str(HK_UV) == 'very':
            ax0.annotate('HIGH',(335,134),ha='center',va='top',fontproperties=DjV_S_12,color='r')
        elif str(HK_UV) == 'extreme':
            ax0.annotate('HELP!!',(335,134),ha='center',va='top',fontproperties=DjV_S_12,color='r')

    #sunspot
        SW_ss = soup_s.find_all(class_="solarWindText")[4].get_text().split()[2] #the 5th solarWindText class in SW page
        ax0.annotate('Sunspots: ',(310,120),ha='left',va='top',fontproperties=DjV_S_8,color='darkgrey')
        ax0.annotate(SW_ss,(360,114),ha='right',va='top',fontproperties=DjV_S_12,color='w')
    except:
        pass

def update_para():
    global transform_x, transform_y, ra0, dec0, zenith_shift_ra, zenith_shift_dec, rotate_angle, aspect_ratio, plot_scale, x_shift, y_shift

    ra0 = math.degrees(Obs.sidereal_time()) + zenith_shift_ra
    dec0 = math.degrees(Obs.lat) + zenith_shift_dec
    
    # projection formula (Lambert Azimuthal Equal-Area with rotation)  # for Moonglow ASC
    transform_x = lambda x,y: x_shift+plot_scale\
                  *(math.cos(math.radians(rotate_angle))\
                   *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                   -math.sin(math.radians(rotate_angle))\
                   *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
    transform_y = lambda x,y: y_shift+aspect_ratio*plot_scale\
                  *(math.sin(math.radians(rotate_angle))\
                   *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                   +math.cos(math.radians(rotate_angle))\
                   *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))

    if debug_mode == 1:
        timelog('ref count ra0: '+str(sys.getrefcount(ra0)))
        timelog('ref count dec0: '+str(sys.getrefcount(dec0)))
        timelog('ref count transform_x: '+str(sys.getrefcount(transform_x)))
        timelog('ref count transform_y: '+str(sys.getrefcount(transform_y)))

def plot_ASC():
    # show image
    ax0.imshow(asc, extent=[-360, 360, -240, 240])
    ax0.set_xlim((-360,360))
    ax0.set_ylim((-240,240))
    
    plot_solar()
    plot_constellation()
    plot_MW()
    plot_boundary()
    write_label()

def side_panel():   
    moon_phase()
    jovian_moons()
    mercury_venus()
    cloud_detection()
    ephemeris()
    past_24h_stat()
    
def moon_phase(): #ax1
    global moon_chi
    Moon.compute(Obs)

    ax1.set_xlim((-90,90))
    ax1.set_ylim((-90,90))
    
    timelog('drawing Moon')
    
    # Moon phase
    ax1.annotate('Moon Phase',(0,85),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')

    ph_r = 50*Moon.size/2100 # line inner radius
    ph_R = 60*Moon.size/2100 # line outer radius
    ph_l = 68*Moon.size/2100 # text radius
    M_d = Moon.size/2100*110
    rot_pa_limb_moon = moon_chi-90 # rotate for position angle of the Moon's bright limb, parallatic angle count from zenith to eq. north clockwise

    moondisc0 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
    
    if Moon.phase == 0:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), 0, 0, 0, color='#94908D') #dummy
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#94908D') #dummy
    elif 0 < Moon.phase < 50:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
        moondisc2 = patches.Wedge((0,0), M_d/2, 270+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), 90+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), color='#94908D')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon.phase/50), M_d, angle=rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), color='#94908D')
    elif Moon.phase == 50:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), 270+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#F0F0F0') #dummy
    elif 50 < Moon.phase < 100:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), 270+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon.phase/50), M_d, angle=rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), color='#F0F0F0')
    elif Moon.phase == 100:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
        moondisc2 = patches.Wedge((0,0), 0, 0, 0,color='#F0F0F0') #dummy
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#F0F0F0') #dummy

    ax1.add_patch(moondisc0)
    ax1.add_patch(moondisc1)
    ax1.add_patch(moondisc2)
    ax1.add_patch(moondisc3)
    
    # eq. coord.
    if Moon.alt > 0:
        ax1.annotate('N',(ph_l*math.sin(Moon.parallactic_angle()),ph_l*math.cos(Moon.parallactic_angle())),\
                     xycoords=('data'),rotation=-math.degrees(Moon.parallactic_angle()),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(Moon.parallactic_angle()),ph_R*math.sin(Moon.parallactic_angle())],\
                 [ph_r*math.cos(Moon.parallactic_angle()),ph_R*math.cos(Moon.parallactic_angle())],color='red')
        
        ax1.annotate('E',(ph_l*math.sin(Moon.parallactic_angle()+3*math.pi/2),ph_l*math.cos(Moon.parallactic_angle()+3*math.pi/2)),\
                     xycoords=('data'),rotation=-math.degrees(Moon.parallactic_angle()),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(Moon.parallactic_angle()+3*math.pi/2),ph_R*math.sin(Moon.parallactic_angle()+3*math.pi/2)],\
                 [ph_r*math.cos(Moon.parallactic_angle()+3*math.pi/2),ph_R*math.cos(Moon.parallactic_angle()+3*math.pi/2)],color='red')
        
        ax1.annotate('S',(ph_l*math.sin(Moon.parallactic_angle()+math.pi),ph_l*math.cos(Moon.parallactic_angle()+math.pi)),\
                     xycoords=('data'),rotation=-math.degrees(Moon.parallactic_angle()),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(Moon.parallactic_angle()+math.pi),ph_R*math.sin(Moon.parallactic_angle()+math.pi)],\
                 [ph_r*math.cos(Moon.parallactic_angle()+math.pi),ph_R*math.cos(Moon.parallactic_angle()+math.pi)],color='red')
        
        ax1.annotate('W',(ph_l*math.sin(Moon.parallactic_angle()+math.pi/2),ph_l*math.cos(Moon.parallactic_angle()+math.pi/2)),\
                     xycoords=('data'),rotation=-math.degrees(Moon.parallactic_angle()),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(Moon.parallactic_angle()+math.pi/2),ph_R*math.sin(Moon.parallactic_angle()+math.pi/2)],\
                 [ph_r*math.cos(Moon.parallactic_angle()+math.pi/2),ph_R*math.cos(Moon.parallactic_angle()+math.pi/2)],color='red')

    ax1.annotate('eq \ncoord.',(-90,-70),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_9,color='red')

    # selenographic
    ax1.annotate('seleno-\ngraphic',(90,-70),xycoords=('data'),ha='right',va='bottom',fontproperties=DjV_S_9,color='cyan')

    T               = (ephem.julian_date(Obs)-2451545)/36525 # should use Julian Emphemeris Date instead
    asc_node        = 125.04452-1934.136261*T\
                      +0.0020708*T*T\
                      +T*T*T/450000 # longitude of ascending node of Moon mean orbit
    L_s             = 280.4665+36000.7698*T # mean longitude of Sun
    L_m             = 218.3165+481267.8813*T # mean longitude of Moon
    nu_lon          = -17.2/3600*math.sin(math.radians(asc_node))\
                      -1.32/3600*math.sin(math.radians(2*L_s))\
                      -0.23/3600*math.sin(math.radians(2*L_m))\
                      +0.21/3600*math.sin(math.radians(2*asc_node)) # nutation in longitude
    Inc             = 1.54242 # inclination of mean lunar equator to ecliptic
    M_s             = 357.5291092\
                      +35999.0502909*T\
                      -0.0001536*T*T\
                      +T*T*T/24490000 # Sun mean anomaly
    M_m             = 134.9634114\
                      +477198.8676313*T\
                      +0.008997*T*T\
                      +T*T*T/69699\
                      -T*T*T*T/14712000 # Moon mean anomaly
    D_m             = 297.8502042\
                      +445267.1115168*T\
                      -0.00163*T*T\
                      +T*T*T/545868\
                      -T*T*T*T/113065000 # mean elongation of Moon
    F_m             = 93.2720993\
                      +483202.0175273*T\
                      -0.0034029*T*T\
                      -T*T*T/3526000\
                      +T*T*T*T/863310000 # Moon argument of latitude
    rho             = -0.02752*math.cos(math.radians(M_m))\
                      -0.02245*math.sin(math.radians(F_m))\
                      +0.00684*math.cos(math.radians(M_m-2*F_m))\
                      -0.00293*math.cos(math.radians(2*F_m))\
                      -0.00085*math.cos(math.radians(2*F_m-2*D_m))\
                      -0.00054*math.cos(math.radians(M_m-2*D_m))\
                      -0.0002*math.sin(math.radians(M_m+F_m))\
                      -0.0002*math.cos(math.radians(M_m+2*F_m))\
                      -0.0002*math.cos(math.radians(M_m-F_m))\
                      +0.00014*math.cos(math.radians(M_m+2*F_m-2*D_m))
    sigma           = -0.02816*math.sin(math.radians(M_m))\
                      +0.02244*math.cos(math.radians(F_m))\
                      -0.00682*math.sin(math.radians(M_m-2*F_m))\
                      -0.00279*math.sin(math.radians(2*F_m))\
                      -0.00083*math.sin(math.radians(2*F_m-2*D_m))\
                      +0.00069*math.sin(math.radians(M_m-2*D_m))\
                      +0.0004*math.cos(math.radians(M_m+F_m))\
                      -0.00025*math.sin(math.radians(2*M_m))\
                      -0.00023*math.sin(math.radians(M_m+2*F_m))\
                      +0.0002*math.cos(math.radians(M_m-F_m))\
                      +0.00019*math.sin(math.radians(M_m-F_m))\
                      +0.00013*math.sin(math.radians(M_m+2*F_m-2*D_m))\
                      -0.0001*math.cos(math.radians(M_m-3*F_m))
    V_m             = asc_node + nu_lon + sigma/math.sin(math.radians(Inc))
    epsilion        = 23.4355636928 #(IAU 2000B nutation series)
    X_m             = math.sin(math.radians(Inc)+rho)*math.sin(math.radians(V_m))
    Y_m             = math.sin(math.radians(Inc)+rho)*math.cos(math.radians(V_m))*math.cos(math.radians(epsilion))\
                      -math.cos(math.radians(Inc)+rho)*math.sin(math.radians(epsilion))
    omega           = math.atan2(X_m,Y_m)
    PA_axis_moon_N  = math.asin(math.sqrt(X_m*X_m+Y_m*Y_m)*math.cos(Moon.ra-omega)/math.cos(Moon.libration_lat))
            
    PA_axis_moon_z  = Moon.parallactic_angle()-PA_axis_moon_N # clockwise
    
    ax1.annotate('N',(ph_l*math.sin(PA_axis_moon_z),ph_l*math.cos(PA_axis_moon_z)),\
                 xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1.plot([ph_r*math.sin(PA_axis_moon_z),ph_R*math.sin(PA_axis_moon_z)],\
             [ph_r*math.cos(PA_axis_moon_z),ph_R*math.cos(PA_axis_moon_z)],color='cyan')
    
    ax1.annotate('E',(ph_l*math.sin(PA_axis_moon_z+math.pi/2),ph_l*math.cos(PA_axis_moon_z+math.pi/2)),\
                 xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1.plot([ph_r*math.sin(PA_axis_moon_z+math.pi/2),ph_R*math.sin(PA_axis_moon_z+math.pi/2)],\
             [ph_r*math.cos(PA_axis_moon_z+math.pi/2),ph_R*math.cos(PA_axis_moon_z+math.pi/2)],color='cyan')
    
    ax1.annotate('S',(ph_l*math.sin(PA_axis_moon_z+math.pi),ph_l*math.cos(PA_axis_moon_z+math.pi)),\
                 xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1.plot([ph_r*math.sin(PA_axis_moon_z+math.pi),ph_R*math.sin(PA_axis_moon_z+math.pi)],\
             [ph_r*math.cos(PA_axis_moon_z+math.pi),ph_R*math.cos(PA_axis_moon_z+math.pi)],color='cyan')
    
    ax1.annotate('W',(ph_l*math.sin(PA_axis_moon_z+3*math.pi/2),ph_l*math.cos(PA_axis_moon_z+3*math.pi/2)),\
                 xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1.plot([ph_r*math.sin(PA_axis_moon_z+3*math.pi/2),ph_R*math.sin(PA_axis_moon_z+3*math.pi/2)],\
             [ph_r*math.cos(PA_axis_moon_z+3*math.pi/2),ph_R*math.cos(PA_axis_moon_z+3*math.pi/2)],color='cyan')

    # Mare in Orthographic projection with rotation
    lon0 = math.degrees(Moon.libration_long)
    lat0 = math.degrees(Moon.libration_lat)
    
    moon_rot = -math.degrees(PA_axis_moon_z) # anti-clockwise
    transform_moon_x = lambda x,y: M_d/2*(math.cos(math.radians(moon_rot))\
                                          *(math.cos(math.radians(y))*math.sin(math.radians(x-lon0)))\
                                          -math.sin(math.radians(moon_rot))\
                                          *(math.cos(math.radians(lat0))*math.sin(math.radians(y))-math.sin(math.radians(lat0))*math.cos(math.radians(y))*math.cos(math.radians(x-lon0)))) 
    transform_moon_y = lambda x,y: M_d/2*(math.sin(math.radians(moon_rot))\
                                          *(math.cos(math.radians(y))*math.sin(math.radians(x-lon0)))\
                                          +math.cos(math.radians(moon_rot))\
                                          *(math.cos(math.radians(lat0))*math.sin(math.radians(y))-math.sin(math.radians(lat0))*math.cos(math.radians(y))*math.cos(math.radians(x-lon0))))
    
    Mare_pt_lon = Mare.groupby('shapeid')['x'].apply(list)
    Mare_pt_lat = Mare.groupby('shapeid')['y'].apply(list)

    Mare_pt_list = Mare.groupby('shapeid')['x'].sum().reset_index()['shapeid']

    Mare_verts = []
    for i in Mare_pt_list:
        Mare_pt_x = list(map(transform_moon_x, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_pt_y = list(map(transform_moon_y, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_verts.append(list(zip(Mare_pt_x, Mare_pt_y)))

    Crater_pt_lon = Crater.groupby('shapeid')['x'].apply(list)
    Crater_pt_lat = Crater.groupby('shapeid')['y'].apply(list)

    Crater_pt_list = Crater.groupby('shapeid')['x'].sum().reset_index()['shapeid']

    Crater_verts = []
    for i in Crater_pt_list:
        Crater_pt_x = list(map(transform_moon_x, Crater_pt_lon.loc[i], Crater_pt_lat.loc[i]))
        Crater_pt_y = list(map(transform_moon_y, Crater_pt_lon.loc[i], Crater_pt_lat.loc[i]))
        Crater_verts.append(list(zip(Crater_pt_x, Crater_pt_y)))

    Mare_poly = mc.PolyCollection(Mare_verts,linewidths=0,facecolors='#696e65',zorder=3)
    Crater_poly = mc.PolyCollection(Crater_verts,linewidths=0,facecolors='#F0F0F0',alpha=0.25,zorder=4)
    ax1.add_collection(Mare_poly)
    ax1.add_collection(Crater_poly)
    
    # zenith
    if Moon.alt > 0:
        ax1.arrow(0,M_d/2,0,10,color='green',head_width=5, head_length=5)
        ax1.annotate(str(round(Moon.size/60,1))+"'",(90,70),xycoords=('data'),ha='right',va='top',fontproperties=DjV_S_9,color='orange')
    else:
        ax1.annotate('below horizon',(90,70),xycoords=('data'),ha='right',va='top',fontproperties=DjV_S_9,color='orange')
    ax1.annotate('zenith',(-90,70),xycoords=('data'),ha='left',va='top',fontproperties=DjV_S_9,color='green')
    
    phase_moon = 'illuminated '+str(round(Moon.phase,2))+'%' # projected 2D apparent area
    if Moon.phase >= 0:
        ax1.annotate(phase_moon,(0,-85),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_10,color='#F0F0F0')
    else:
        ax1.annotate(phase_moon,(0,-85),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_10,color='#94908D')

def jovian_moons(): #ax2
    Jupiter.compute(Obs)
    Io.compute(Obs)
    Europa.compute(Obs)
    Ganymede.compute(Obs)
    Callisto.compute(Obs)

    ax2.set_xlim((-90,90))
    ax2.set_ylim((-50,50))

    timelog('drawing Jupiter')
    
    ax2.annotate('Jovian Moons',(0,45),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')
    
    Io_radius = 1821.6/69911
    Europa_radius = 1560.8/69911
    Callisto_radius = 2634.1/69911
    Ganymede_radius = 2410.3/69911
    jov_radius = 90/(1+max(abs(Io.x-Io_radius),abs(Io.x+Io_radius),\
                           abs(Europa.x-Europa_radius),abs(Europa.x+Europa_radius),\
                           abs(Callisto.x-Callisto_radius),abs(Callisto.x+Callisto_radius),\
                           abs(Ganymede.x-Ganymede_radius),abs(Ganymede.x+Ganymede_radius)))
    
    Io_r = 5*Io_radius*jov_radius
    Eu_r = 5*Europa_radius*jov_radius
    Ca_r = 5*Callisto_radius*jov_radius
    Ga_r = 5*Ganymede_radius*jov_radius

    Jupdisc = patches.Circle((0,0), jov_radius, color='#C88B3A')
    
    if not (Io.z < 0 and -1 < Io.x < 1):
        Iodisc = patches.Circle((-Io.x*jov_radius,-Io.y*jov_radius), Io_r, color='#9f9538')
    else:
        Iodisc = patches.Circle((-Io.x*jov_radius,-Io.y*jov_radius), 0, color='#9f9538')
    
    if not (Europa.z < 0 and -1 < Europa.x < 1):
        Europadisc = patches.Circle((-Europa.x*jov_radius,-Europa.y*jov_radius), Eu_r, color='#6c5d40')
    else:
        Europadisc = patches.Circle((-Europa.x*jov_radius,-Europa.y*jov_radius), 0, color='#6c5d40')
    
    if not (Callisto.z < 0 and -1 < Callisto.x < 1):
        Callistodisc = patches.Circle((-Callisto.x*jov_radius,-Callisto.y*jov_radius), Ca_r, color='#766b5d')
    else:
        Callistodisc = patches.Circle((-Callisto.x*jov_radius,-Callisto.y*jov_radius), 0, color='#766b5d')
    
    if not (Ganymede.z < 0 and -1 < Ganymede.x < 1):
        Ganymededisc = patches.Circle((-Ganymede.x*jov_radius,-Ganymede.y*jov_radius), Ga_r, color='#544a45')
    else:
        Ganymededisc = patches.Circle((-Ganymede.x*jov_radius,-Ganymede.y*jov_radius), 0, color='#544a45')

    ax2.annotate('I',(-Io.x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#9f9538')
    ax2.annotate('E',(-Europa.x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#6c5d40')
    ax2.annotate('C',(-Callisto.x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#766b5d')
    ax2.annotate('G',(-Ganymede.x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#544a45')

    ax2.add_patch(Jupdisc)
    ax2.add_patch(Iodisc)
    ax2.add_patch(Europadisc)
    ax2.add_patch(Callistodisc)
    ax2.add_patch(Ganymededisc)


    d0 = date(2019,6,1) # http://jupos.privat.t-online.de/index.htm 
    delta = date.today()-d0
    grs_lon = 310+delta.days/365.2425*12*4 # should oftenly update, monthly rate ~ 4deg

    if math.degrees(Jupiter.cmlII)-90 < grs_lon < math.degrees(Jupiter.cmlII):
        GRS = 'GRS at east'
    elif grs_lon == math.degrees(Jupiter.cmlII):
        GRS = 'GRS transit'
    elif math.degrees(Jupiter.cmlII) < grs_lon < math.degrees(Jupiter.cmlII)+90:
        GRS = 'GRS at west'
    else:
        GRS = 'no GRS'
    ax2.annotate(GRS,(0,-45),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#C88B3A')

    ax2.annotate('\u2190 E',(-90,-45),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_10,color='red')
    ax2.annotate('W \u2192',(90,-45),xycoords=('data'),ha='right',va='bottom',fontproperties=DjV_S_10,color='red')

def mercury_venus(): #ax3
    Mercury.compute(Obs)
    Venus.compute(Obs)    

    ax3.set_xlim((-90,90))
    ax3.set_ylim((-50,50))

    mercury_chi = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Mercury.ra),\
                                          math.sin(Sun.dec)*math.cos(Mercury.dec)-math.cos(Sun.dec)*math.sin(Mercury.dec)*math.cos(Sun.ra-Mercury.ra)))
    if mercury_chi < 0:
        mercury_chi = mercury_chi+360

    venus_chi = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Venus.ra),\
                                        math.sin(Sun.dec)*math.cos(Venus.dec)-math.cos(Sun.dec)*math.sin(Venus.dec)*math.cos(Sun.ra-Venus.ra)))
    if venus_chi < 0:
        venus_chi = venus_chi+360

    timelog('drawing Mercury and Venus')

    ax3.annotate('Mercury & Venus',(0,35),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')

    Mercury_offsetx = -45
    Venus_offsetx = 45
    MV_d = 30
    rot_pa_limb_mercury = mercury_chi-90
    rot_pa_limb_venus = venus_chi-90
    
    if Mercury.phase == 0:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), 0, 0, 0, color='black') #dummy
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='black') #dummy
    elif 0 < Mercury.phase < 50:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='#97979F')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 270+rot_pa_limb_mercury, 90+rot_pa_limb_mercury, color='black')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), MV_d*(1-Mercury.phase/50), MV_d, angle=rot_pa_limb_mercury, color='black')
    elif Mercury.phase == 50:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 90+rot_pa_limb_mercury, 270+rot_pa_limb_mercury, color='#97979F')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='#97979F') #dummy
    elif 50 < Mercury.phase < 100:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 90+rot_pa_limb_mercury, 270+rot_pa_limb_mercury, color='#97979F')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), MV_d*(1-Mercury.phase/50), MV_d, angle=rot_pa_limb_mercury, color='#97979F')
    elif Mercury.phase == 100:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='#97979F')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), 0, 0, 0,color='#97979F') #dummy
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='#97979F') #dummy

    ax3.add_patch(Merdisc0)
    ax3.add_patch(Merdisc1)
    ax3.add_patch(Merdisc2)

    if Venus.phase == 0:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), 0, 0, 0, color='black') #dummy
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='black') #dummy
    elif 0 < Venus.phase < 50:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='#C18F17')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 270+rot_pa_limb_venus, 90+rot_pa_limb_venus, color='black')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), MV_d*(1-Venus.phase/50), MV_d, angle=rot_pa_limb_venus, color='black')
    elif Venus.phase == 50:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 90+rot_pa_limb_venus, 270+rot_pa_limb_venus, color='#C18F17')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='#C18F17') #dummy
    elif 50 < Venus.phase < 100:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 90+rot_pa_limb_venus, 270+rot_pa_limb_venus, color='#C18F17')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), MV_d*(1-Venus.phase/50), MV_d, angle=rot_pa_limb_venus, color='#C18F17')
    elif Venus.phase == 100:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='#C18F17')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), 0, 0, 0,color='#C18F17') #dummy
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='#C18F17') #dummy

    ax3.add_patch(Vendisc0)
    ax3.add_patch(Vendisc1)
    ax3.add_patch(Vendisc2)

    dist_SM = math.degrees(math.acos(math.sin(Sun.dec)*math.sin(Mercury.dec)+math.cos(Sun.dec)*math.cos(Mercury.dec)*math.cos(Sun.ra-Mercury.ra)))
    ax3.annotate(str(round(dist_SM,1))+u'\N{DEGREE SIGN}',(Mercury_offsetx,0),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8,color='#FFCC33')
    dist_SV = math.degrees(math.acos(math.sin(Sun.dec)*math.sin(Venus.dec)+math.cos(Sun.dec)*math.cos(Venus.dec)*math.cos(Sun.ra-Venus.ra)))
    ax3.annotate(str(round(dist_SV,1))+u'\N{DEGREE SIGN}',(Venus_offsetx,0),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8,color='#FFCC33')
    
    ax3.annotate('\u2190 E',(-90,-35),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_10,color='red')
    ax3.annotate('dist. to Sun',(0,-35),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#FFCC33')
    ax3.annotate('W \u2192',(90,-35),xycoords=('data'),ha='right',va='bottom',fontproperties=DjV_S_10,color='red')

def cloud_detection(): #ax4
    ax4.set_xlim((-90,90))
    ax4.set_ylim((-40,80))

    ax4.annotate('Cloud Coverage',(0,75),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white',zorder=11)
    ax4.annotate('experimental',(0,50),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8, color='red',zorder=11)
    CC_bg = patches.Rectangle((-90,40),180,40,color='k',zorder=10)
    ax4.add_patch(CC_bg)
    
    timelog('counting cloud')

    try:
        # bg mask
        mask_source = Image.open(pathlib.Path.cwd().joinpath('ASC','mask_source.jpg'))
        mask_source_rgb = mask_source.convert('RGB')
        hokoon_raw = numpy.arange(480*720).reshape(480,720) # (row,col)
        hokoon_mask = numpy.ma.make_mask(hokoon_raw,copy=True,shrink=True,dtype=numpy.bool)

        for row in range(480):
            hokoon_mask_row = []
            for col in range(720):
                r, g, b = mask_source_rgb.getpixel((col, row)) # (x,y)
                if r+g+b > 225:
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
                if r+g+b > 650:
                    sun_mask_row.append(True)
                else:
                    sun_mask_row.append(False)

            sun_mask[row] = sun_mask_row

        # combine mask
        real_mask = hokoon_mask + sun_mask

        # copy for RGB channel
        real_mask_3d = numpy.zeros_like(mask_source)
        for i in range(3): 
            real_mask_3d[:,:,i] = real_mask.copy()
       
        # apply mask
        masked_asc = numpy.ma.masked_array(asc, mask=real_mask_3d, dtype='float64')
        r = masked_asc[:,:,0]
        g = masked_asc[:,:,1]
        b = masked_asc[:,:,2]

        ################################################################################################

        # HSI approach
        # A Simple Method for the Assessment of the Cloud Cover State in High-Latitude Regions by a Ground-Based Digital Camera
        # Souza-Echer, M. P., Pereira, E. B., Bins, L. S., and An-drade, M. A. R., J. Atmos. Ocean. Technol., 23, 437–447
        # https://doi.org/10.1175/JTECH1833.1
        I_HSI = r+g+b # real I_HSI = 3*I_HSI
        min_rgb = numpy.minimum(numpy.minimum(r,g),b) # use mininmum to compare value element-wise

        S_HSI_ASC_0 = (1-3*min_rgb/I_HSI).tolist() # rewrite to list of list
        S_HSI_ASC = list(itertools.chain.from_iterable(S_HSI_ASC_0)) # reduce to single list
        reduced_S_HSI_ASC = [x for x in S_HSI_ASC if x != None] # clean up

        # BR ratio approach
        BR_ratio_ASC_0 = ((b-r)/(b+r)).tolist()
        BR_ratio_ASC = list(itertools.chain.from_iterable(BR_ratio_ASC_0))
        reduced_BR_ratio_ASC = [x for x in BR_ratio_ASC if x != None]

        ################################################################################################
        # sky condition
        if -18 <= math.degrees(Sun.alt) <= 0: # twilight
            sky_con = 'っω-) twilight'
            ss_color = '#9DA5BF'
            l_color = '#9DA5BF'
            CC = numpy.nan
        elif 0 < math.degrees(Sun.alt) <= 15: # low angle
            if math.degrees(Sun.az) < 180:
                sky_con = 'っω-) sunrise'
                ss_color = '#FFCC33'
                l_color = '#FFCC33'
            else:
                sky_con = '-_-)ﾉｼ sunset'
                ss_color = '#FD5E53'
                l_color = '#FD5E53'
            CC = numpy.nan
        elif 15 < math.degrees(Sun.alt): # daytime
            if numpy.percentile(reduced_S_HSI_ASC,85) < 0.05:
                sky_con = '(TдT) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%'
                ss_color = '#ADACA9'
                l_color = '#525356'
            else:
                if numpy.percentile(reduced_BR_ratio_ASC,85) <= 0.04:
                    sky_con = '(ﾟｰﾟ) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%'
                    ss_color = '#A7A69D'
                    l_color = '#585962'
                else:
                    sky_con = '(・ω・) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%'
                    ss_color = '#002b66'
                    l_color = '#ffd499'
            CC = round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC))
        else: # nighttime
            if numpy.mean(reduced_S_HSI_ASC) < 0.05:
                sky_con = '(・ω・) '+str(round(sum(i <= 0 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%'
                ss_color = '#002b66'
                l_color = '#ffd499'
            elif 0.05 <= numpy.mean(reduced_S_HSI_ASC) <= 0.07:
                sky_con = '(ﾟｰﾟ) '+str(round(sum(i <= 0 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%'
                ss_color = '#A7A69D'
                l_color = '#585962'
            else:
                sky_con = '(TдT) '+str(round(sum(i <= 0 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%'
                ss_color = '#ADACA9'
                l_color = '#525356'
            CC = round(sum(i <= 0 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC))

        ax4.annotate(sky_con,(0,0),xycoords=('data'),ha='center',va='center',fontproperties=emoji_20, color='white',zorder=3)
        ax4.set_facecolor(ss_color)

        # record cloud coverage
        CC_hokoon.update(pandas.DataFrame({'CC':CC},index=[CC_hokoon.index[-1]]))

##        if numpy.isnan(CC) == False:
##            # plot hourly-averaged value
##            HV_CC_x = [0]*25
##            HV_CC_y = [0]*25
##            for i in range(25):
##                HV_CC_x[i] = -(i-12)/12*90
##                HV_CC_y[i] = 40*(CC_hokoon[(CC_hokoon['HKT'] >= datetime.now()-timedelta(hours=i+1)) & (CC_hokoon['HKT'] < datetime.now()-timedelta(hours=i))].CC.mean()-50)/50
##            ax4.plot(HV_CC_x,HV_CC_y,color=l_color,linewidth=0.5,alpha=0.75,zorder=1)
##
##            # current value
##            ax4.axhline(y=40*(CC_hokoon['CC'].iloc[-1]-50)/50, color='g', linewidth=0.5, linestyle='-', alpha=0.75, zorder=1)
##    
##            for xc in [-90/6*4,-90/6*2,90/6*0,90/6*2,90/6*4,90/6*6]:
##                ax4.axvline(x=xc, color='w', linewidth=0.5, linestyle='--', alpha=0.5, zorder=2)
##                ax4.axvline(x=xc-90/6, color='w', linewidth=0.5, linestyle='--', alpha=0.25, zorder=2)
##            for yc in [-20,0,20]:
##                ax4.axhline(y=yc, color='w', linewidth=0.5, linestyle='--', alpha=0.5, zorder=2)
##
##            ax4.annotate('-4h',(90/6*4,-40),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_6,color='w',alpha=0.5)
##            ax4.annotate('-8h',(90/6*2,-40),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_6,color='w',alpha=0.5)
##            ax4.annotate('-12h',(90/6*0,-40),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_6,color='w',alpha=0.5)
##            ax4.annotate('-16h',(-90/6*2,-40),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_6,color='w',alpha=0.5)
##            ax4.annotate('-20h',(-90/6*4,-40),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_6,color='w',alpha=0.5)
##
##            ax4.annotate('hr-avg',(-85,-30),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_6,color=l_color,alpha=1)
##            ax4.annotate('now',(-85,-38),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_6,color='g',alpha=0.75)

    except:
        ax4.annotate('_(:3」∠)_ fail',(0,0),xycoords=('data'),ha='center',va='center',fontproperties=emoji_20, color='white',zorder=3)
        ax4.set_facecolor('red')

def ephemeris(): #ax5
    ax5.set_xlim((-90,90))
    ax5.set_ylim((-140,140))
    
    Obs.horizon = '0'
    
    ax5.annotate('Ephemeris',(0,135),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')

    sym_x = -85
    rise_x = -40
    set_x = 22.5
    mag_x = 87.5
    ax5.annotate('rise',(rise_x,105),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='white')
    ax5.annotate('set',(set_x,105),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='white')
    ax5.annotate('mag',(mag_x,105),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='white')
    
    
    # Moon
    moon_y = 85
    if moon_chi>180:
        ax5.annotate('\u263D',(sym_x,moon_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#DAD9D7')
    else:
        ax5.annotate('\u263E',(sym_x,moon_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#DAD9D7')
    
    next_rise_moon = ephem.localtime(Obs.next_rising(ephem.Moon())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Moon()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_moon),(rise_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_moon),(rise_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_moon = ephem.localtime(Obs.next_setting(ephem.Moon())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Moon()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_moon),(set_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_moon),(set_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Moon.mag,1)),(mag_x,moon_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Mercury
    mercury_y = 65
    ax5.annotate('\u263F',(sym_x,mercury_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#97979F')
    
    next_rise_mercury = ephem.localtime(Obs.next_rising(ephem.Mercury())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Mercury()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_mercury),(rise_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_mercury),(rise_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_mercury = ephem.localtime(Obs.next_setting(ephem.Mercury())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Mercury()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_mercury),(set_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_mercury),(set_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Mercury.mag,1)),(mag_x,mercury_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Venus
    venus_y = 45
    ax5.annotate('\u2640',(sym_x,venus_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#C18F17')
    
    next_rise_venus = ephem.localtime(Obs.next_rising(ephem.Venus())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Venus()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_venus),(rise_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_venus),(rise_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_venus = ephem.localtime(Obs.next_setting(ephem.Venus())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Venus()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_venus),(set_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_venus),(set_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Venus.mag,1)),(mag_x,venus_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Mars
    mars_y = 25
    ax5.annotate('\u2642',(sym_x,mars_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#E27B58')
    
    next_rise_mars = ephem.localtime(Obs.next_rising(ephem.Mars())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Mars()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_mars),(rise_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_mars),(rise_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_mars = ephem.localtime(Obs.next_setting(ephem.Mars())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Mars()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_mars),(set_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_mars),(set_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Mars.mag,1)),(mag_x,mars_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Jupiter
    jupiter_y = 5
    ax5.annotate('\u2643',(sym_x,jupiter_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#C88B3A')
    
    next_rise_jupiter = ephem.localtime(Obs.next_rising(ephem.Jupiter())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Jupiter()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_jupiter),(rise_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_jupiter),(rise_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_jupiter = ephem.localtime(Obs.next_setting(ephem.Jupiter())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Jupiter()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_jupiter),(set_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_jupiter),(set_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Jupiter.mag,1)),(mag_x,jupiter_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Saturn
    saturn_y = -15
    ax5.annotate('\u2644',(sym_x,saturn_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#A49B72')
    
    next_rise_saturn = ephem.localtime(Obs.next_rising(ephem.Saturn())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Saturn()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_saturn),(rise_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_saturn),(rise_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_saturn = ephem.localtime(Obs.next_setting(ephem.Saturn())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Saturn()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_saturn),(set_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_saturn),(set_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Saturn.mag,1)),(mag_x,saturn_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Uranus
    uranus_y = -35
    ax5.annotate('\u2645',(sym_x,uranus_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#D5FBFC')
    
    next_rise_uranus = ephem.localtime(Obs.next_rising(ephem.Uranus())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Uranus()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_uranus),(rise_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_uranus),(rise_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_uranus = ephem.localtime(Obs.next_setting(ephem.Uranus())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Uranus()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_uranus),(set_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_uranus),(set_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Uranus.mag,1)),(mag_x,uranus_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    # Neptune
    neptune_y = -55
    ax5.annotate('\u2646',(sym_x,neptune_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#3E66F9')
    
    next_rise_neptune = ephem.localtime(Obs.next_rising(ephem.Neptune())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Neptune()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_neptune),(rise_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_neptune),(rise_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_neptune = ephem.localtime(Obs.next_setting(ephem.Neptune())).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Neptune()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_neptune),(set_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_neptune),(set_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate(str(round(Neptune.mag,1)),(mag_x,neptune_y),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_10,color='yellow')
    
    ###################################################################################################################################################
    
    # astronomical twilight
    Obs.horizon = '-18'

    ax5.annotate('Astronomical Twilight',(0,-75),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')

    sun_y = -105
    ax5.annotate('\u263C',(sym_x,sun_y),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_10,color='#FFCC33')

    next_rise_sun = ephem.localtime(Obs.next_rising(ephem.Sun(), use_center=True)).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_rising(ephem.Sun()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_rise_sun),(rise_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_rise_sun),(rise_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    next_set_sun = ephem.localtime(Obs.next_setting(ephem.Sun(), use_center=True)).strftime('%X')
    if datetime.date(ephem.localtime(Obs.next_setting(ephem.Sun()))) > datetime.date(ephem.localtime(Obs.date)):
        ax5.annotate(str(next_set_sun),(set_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='green')
    else:
        ax5.annotate(str(next_set_sun),(set_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_10,color='orange')

    ax5.annotate('orange: today ',(0,-125),xycoords=('data'),ha='right',va='center',fontproperties=DjV_S_8,color='orange')
    ax5.annotate(' green: +1day',(0,-125),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_8,color='green')

def past_24h_stat(): #ax6
    ax6.set_xlim((24,0))
    ax6.set_ylim((0,100))
    ax6.axis('off')
    
    # time axis
    def diff_hour(datetime1):
        diff = datetime.now()-datetime1
        return diff.days*24+diff.seconds/3600

    back_hour = [0]*len(CC_hokoon['HKT'])
    for i in range(len(CC_hokoon['HKT'])):
        back_hour[i] = diff_hour(CC_hokoon['HKT'][i])
        
    # plot graph
    for yc in [0,20,40,60,80,100]:
        ax6.axhline(y=yc, color='w', linewidth=0.5, linestyle='--', alpha=0.5, zorder=2)

    oclock = [0]*24
    for i in range(24):
        oclock[i] = diff_hour((datetime.now()-timedelta(hours=i)).replace(minute=0,second=0,microsecond=0))
        ax6.axvline(x=oclock[i], color='w', linewidth=0.5, linestyle='--', alpha=0.5, zorder=2)
        ax6.annotate(str((datetime.now()-timedelta(hours=i)).hour)+':00',(oclock[i],0),xycoords=('data'),\
                     ha='center',va='bottom',fontproperties=DjV_S_8,color='w',alpha=0.5)
    
    # cloud coverage  
    ax6.annotate('20',(24,20),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_8,color='w',alpha=0.5)
    ax6.annotate('40',(24,40),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_8,color='w',alpha=0.5)
    ax6.annotate('60',(24,60),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_8,color='w',alpha=0.5)
    ax6.annotate('80',(24,80),xycoords=('data'),ha='left',va='center',fontproperties=DjV_S_8,color='w',alpha=0.5)

    ax6.plot(back_hour,CC_hokoon['CC'],color='grey',linewidth=1,zorder=1)

    # temp
    temp_max = int(round(CC_hokoon['temp'].mean())+5)
    temp_min = int(round(CC_hokoon['temp'].mean())-5)
    temp_cmap = matplotlib.cm.get_cmap('coolwarm')
    
    for i in [1,2,3,4]:
        ax6.annotate(str(temp_max-2*i),(0,100-20*i),xycoords=('data'),ha='right',va='center',\
                     fontproperties=DjV_S_8,color=temp_cmap(numpy.clip((temp_max-2*i)/40,0,1)),alpha=1)

    ax6.scatter(back_hour,10*(CC_hokoon['temp']-temp_min),c=temp_cmap(numpy.clip(CC_hokoon['temp']/40,0,1)),\
                edgecolor='none',s=1,alpha=1,zorder=1)
    ax6.plot(back_hour,10*(CC_hokoon['temp']-temp_min),color='gray',zorder=0)
   
def refresh_sky(i):
    global fig, asc, CC_hokoon, count

    #################################
    # read record and put timestamp #
    #################################       
    CC_hokoon = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CC_hokoon.csv'), index_col=0)
    #print(CC_hokoon.memory_usage(deep=True))
    CC_hokoon = CC_hokoon.append({'HKT':ephem.localtime(Obs.date).replace(microsecond=0)}, ignore_index=True) # can't use datetime in dict
    CC_hokoon['HKT'] = pandas.to_datetime(CC_hokoon['HKT']) # convert to datetime object

    ###########
    # removal #
    ###########
    start = time.time()

    # clear the world
    gc.collect()
    try:
        ax0.clear()
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        ax6.clear()
        timelog('Armageddon')
    except:
        timelog('survivor')

    ##########
    # update #
    ##########

    # update time
    Obs.date = datetime.utcnow().replace(second=0,microsecond=0)

    # update ASC
    try:
        urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
        asc = Image.open('asc.jpg')
    except ContentTooShortError: # try again
        timelog('try again')
        urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
        asc = Image.open('asc.jpg')        
    except HTTPError:
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','serverdead.jpg'))
    except:
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','black.jpg'))
        
    # update transformation
    update_para()

    try:
        plot_ASC()
    except:
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','black.jpg'))
        plot_ASC()
        
    side_panel()

    # plot
    fig.canvas.draw() 
    fig.canvas.flush_events()
    #fig.savefig('Hokoon_ASIM_'+str("{:%Y_%m_%d-%H_%M_%S}".format(datetime.now()))+'.png')
    #plt.savefig('Hokoon_ASIM_'+str("{:%Y_%m_%d-%H_%M_%S}".format(datetime.now()))+'.png')
    plt.savefig('Hokoon_ASIM.png')
    #plt.close(fig)

    ########################
    # save and trim record #
    ########################
    CC_hokoon.drop(CC_hokoon[CC_hokoon['HKT'] <= datetime.now()-timedelta(hours=24)].index, inplace=True) # keep only last 24h data
    CC_hokoon.reset_index(drop=True,inplace=True)

    CC_hokoon.to_csv(pathlib.Path.cwd().joinpath('ASC','CC_hokoon.csv'))

    end = time.time()
    timelog(str(round(end-start,2))+'s wasted')
    count = count + 1
    if count == 1:
        timelog('This is the begining of this section')
    else:
        timelog(str(count)+' snapshots in this section')
    timelog('runtime: '+str(timedelta(seconds=end-T0)).split('.')[0])
    if platform == 'linux':
        timelog(str(os.popen('vcgencmd measure_temp').readline().splitlines()[0]).replace('temp=','core_temp: '))
    timelog('memory usage:')
    print('')
    objgraph.show_growth()
    print('')
    
if platform == 'win32':
    ani = matplotlib.animation.FuncAnimation(fig, refresh_sky, repeat=False, interval=45000, save_count=0)
else:
    ani = matplotlib.animation.FuncAnimation(fig, refresh_sky, repeat=False, interval=10000, save_count=0)

timelog('backend is '+str(matplotlib.get_backend()))

plt.show()

#objgraph.show_most_common_types(objects=objgraph.get_leaking_objects())
#objgraph.show_refs(objgraph.get_leaking_objects()[:3], refcounts=True)
