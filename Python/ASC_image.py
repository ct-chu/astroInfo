import time
from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, ContentTooShortError
import socket
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as mpath
from matplotlib import font_manager
from matplotlib import collections as mc
import matplotlib.animation
import pandas
import numpy
import math
import cv2
from skyfield import almanac, almanac_east_asia
from skyfield.api import load, wgs84, PlanetaryConstants
from skyfield.framelib import ecliptic_frame
from skyfield.almanac import find_discrete, risings_and_settings
from skyfield.magnitudelib import planetary_magnitude
from pytz import timezone, common_timezones
from datetime import date, datetime, timedelta
import cartopy.crs as ccrs
import pathlib
from PIL import Image
import itertools
from operator import itemgetter
import sys
from sys import platform
import os
import gc
import feedparser
import re
import objgraph
import pysftp

##################
#memory leak
debug_mode = 0
##################

######################
# initial parameters #
######################

count=0
T0 = time.time()

#matplotlib.rcParams['savefig.facecolor'] = ('#F0F0F0')

#####################################
# ephem setting
tz          = timezone('Asia/Hong_Kong')

ephem       = load('data/de421.bsp') #1900-2050 only
#ephem      = load('de422.bsp') #-3000-3000 only
#ephem      = load('de430t.bsp') #1550-2650 only
ephemJ      = load('data/jup310.bsp') #Jupiter
sun         = ephem['sun']
mercury     = ephem['mercury']
venus       = ephem['venus']
earthmoon   = ephem['earth_barycenter']
earth       = ephem['earth']
moon        = ephem['moon']
mars        = ephem['mars']
jupiter     = ephem['jupiter_barycenter']
jupiterJ    = ephemJ['jupiter_barycenter']
io          = ephemJ['Io']
europa      = ephemJ['Europa']
ganymede    = ephemJ['Ganymede']
callisto    = ephemJ['Callisto']
saturn      = ephem['saturn_barycenter']
uranus      = ephem['uranus_barycenter']
neptune     = ephem['neptune_barycenter']
pluto       = ephem['pluto_barycenter']
#####################################
# moon geometry
pc = PlanetaryConstants()
pc.read_text(load('data/moon/moon_080317.tf'))
pc.read_text(load('data/pck00008.tpc'))
pc.read_binary(load('data/moon/moon_pa_de421_1900-2050.bpc'))
frame = pc.build_frame_named('MOON_ME_DE421')
#####################################

#####################################
# location information
#HKO
Trig_0      = (earth + wgs84.latlon((22+18/60+7.3/3600),(114+10/60+27.6/3600)),\
               22+18/60+7.3/3600,114+10/60+27.6/3600,'22:18:07.3','N','114:10:27.6','E')

#Hokoon
hokoon      = (earth + wgs84.latlon((22+23/60+1/3600),(114+6/60+29/3600)),\
               22+23/60+1/3600,114+6/60+29/3600,'22:23:01','N','114:06:29','E')

OBS         = hokoon #<= set your observatory

ts          = load.timescale()
date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
date_local  = date_UTC.astimezone(tz)
#####################################

# plot parameters
fig = plt.figure(figsize=(10.8, 7.2), facecolor='black')
fig.subplots_adjust(0,0,1,1,0,0)

gs = matplotlib.gridspec.GridSpec(3, 2, wspace=0, hspace=0, width_ratios=[0, 1], height_ratios=[1,0,0])

ax0 = plt.subplot(gs[:5, 1])
ax0.set_facecolor('black')
ax0.set_aspect('equal', anchor='N')

ax3 = plt.subplot(gs[2, 0])
ax3.set_facecolor('black')
ax3.set_aspect('equal', anchor='NE')

ax4 = fig.add_axes([-0.1, 0, 0.3, 0.2])
ax4.set_facecolor('black')
ax4.set_aspect('equal', anchor='NE')
    
matplotlib.rcParams['savefig.facecolor'] = (0,0,0)

##zenith_shift_ra     = -2.5
##zenith_shift_dec    = -1.5
##rotate_angle        = -1.5
##aspect_ratio        = 0.94 #y/x
##plot_scale          = 174
##x_shift             = -11.5
##y_shift             = 6

zenith_shift_ra     = 2.95144569
zenith_shift_dec    = 0.39390588
rotate_angle        = -3.84009685
aspect_ratio        = 0.92716790
plot_scale          = 175.85732515
x_shift             = -22.57327227
y_shift             = 9.31539685

DjV_S_6     = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=6)
DjV_S_8     = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=8)
DjV_S_9     = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=9)
DjV_S_10    = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=10)
DjV_S_12    = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=12)
emoji_20    = font_manager.FontProperties(fname = 'fonts/YuGothB.ttc', size=20)
chara_chi   = font_manager.FontProperties(fname = 'fonts/SimHei.ttf')

# log
def timelog(log):
    print(str(datetime.now().time().replace(microsecond=0))+'> '+log)
    
# make relative path (pathlib.Path.cwd() <=> current Dir)
timelog('importing star catalogue')
And = numpy.zeros(shape=(178,5))
And = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','And.csv'))
Ant = numpy.zeros(shape=(48,5))
Ant = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ant.csv'))
Aps = numpy.zeros(shape=(36,5))
Aps = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Aps.csv'))
Aqr = numpy.zeros(shape=(171,5))
Aqr = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Aqr.csv'))
Aql = numpy.zeros(shape=(131,5))
Aql = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Aql.csv'))
Ara = numpy.zeros(shape=(64,5))
Ara = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ara.csv'))
Ari = numpy.zeros(shape=(86,5))
Ari = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ari.csv'))
Aur = numpy.zeros(shape=(161,5))
Aur = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Aur.csv'))
Boo = numpy.zeros(shape=(154,5))
Boo = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Boo.csv'))
Cae = numpy.zeros(shape=(21,5))
Cae = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cae.csv'))
Cam = numpy.zeros(shape=(158,5))
Cam = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cam.csv'))
Cnc = numpy.zeros(shape=(112,5))
Cnc = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cnc.csv'))
CVn = numpy.zeros(shape=(61,5))
CVn = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','CVn.csv'))
CMa = numpy.zeros(shape=(155,5))
CMa = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','CMa.csv'))
CMi = numpy.zeros(shape=(44,5))
CMi = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','CMi.csv'))
Cap = numpy.zeros(shape=(87,5))
Cap = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cap.csv'))
Car = numpy.zeros(shape=(210,5))
Car = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Car.csv'))
Cas = numpy.zeros(shape=(164,5))
Cas = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cas.csv'))
Cen = numpy.zeros(shape=(281,5))
Cen = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cen.csv'))
Cep = numpy.zeros(shape=(157,5))
Cep = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cep.csv'))
Cet = numpy.zeros(shape=(177,5))
Cet = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cet.csv'))
Cha = numpy.zeros(shape=(34,5))
Cha = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cha.csv'))
Cir = numpy.zeros(shape=(34,5))
Cir = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cir.csv'))
Col = numpy.zeros(shape=(78,5))
Col = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Col.csv'))
Com = numpy.zeros(shape=(71,5))
Com = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Com.csv'))
CrA = numpy.zeros(shape=(46,5))
CrA = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','CrA.csv'))
CrB = numpy.zeros(shape=(40,5))
CrB = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','CrB.csv'))
Crv = numpy.zeros(shape=(28,5))
Crv = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Crv.csv'))
Crt = numpy.zeros(shape=(33,5))
Crt = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Crt.csv'))
Cru = numpy.zeros(shape=(48,5))
Cru = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cru.csv'))
Cyg = numpy.zeros(shape=(291,5))
Cyg = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Cyg.csv'))
Del = numpy.zeros(shape=(47,5))
Del = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Del.csv'))
Dor = numpy.zeros(shape=(34,5))
Dor = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Dor.csv'))
Dra = numpy.zeros(shape=(226,5))
Dra = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Dra.csv'))
Equ = numpy.zeros(shape=(15,5))
Equ = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Equ.csv'))
Eri = numpy.zeros(shape=(197,5))
Eri = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Eri.csv'))
For = numpy.zeros(shape=(64,5))
For = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','For.csv'))
Gem = numpy.zeros(shape=(123,5))
Gem = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Gem.csv'))
Gru = numpy.zeros(shape=(62,5))
Gru = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Gru.csv'))
Her = numpy.zeros(shape=(263,5))
Her = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Her.csv'))
Hor = numpy.zeros(shape=(36,5))
Hor = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Hor.csv'))
Hya = numpy.zeros(shape=(246,5))
Hya = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Hya.csv'))
Hyi = numpy.zeros(shape=(33,5))
Hyi = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Hyi.csv'))
Ind = numpy.zeros(shape=(39,5))
Ind = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ind.csv'))
Lac = numpy.zeros(shape=(67,5))
Lac = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lac.csv'))
Leo = numpy.zeros(shape=(130,5))
Leo = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Leo.csv'))
LMi = numpy.zeros(shape=(36,5))
LMi = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','LMi.csv'))
Lep = numpy.zeros(shape=(76,5))
Lep = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lep.csv'))
Lib = numpy.zeros(shape=(86,5))
Lib = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lib.csv'))
Lup = numpy.zeros(shape=(117,5))
Lup = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lup.csv'))
Lyn = numpy.zeros(shape=(100,5))
Lyn = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lyn.csv'))
Lyr = numpy.zeros(shape=(83,5))
Lyr = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Lyr.csv'))
Men = numpy.zeros(shape=(26,5))
Men = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Men.csv'))
Mic = numpy.zeros(shape=(39,5))
Mic = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Mic.csv'))
Mon = numpy.zeros(shape=(153,5))
Mon = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Mon.csv'))
Mus = numpy.zeros(shape=(59,5))
Mus = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Mus.csv'))
Nor = numpy.zeros(shape=(41,5))
Nor = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Nor.csv'))
Oct = numpy.zeros(shape=(67,5))
Oct = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Oct.csv'))
Oph = numpy.zeros(shape=(179,5))
Oph = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Oph.csv'))
Ori = numpy.zeros(shape=(225,5))
Ori = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ori.csv'))
Pav = numpy.zeros(shape=(82,5))
Pav = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Pav.csv'))
Peg = numpy.zeros(shape=(176,5))
Peg = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Peg.csv'))
Per = numpy.zeros(shape=(160,5))
Per = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Per.csv'))
Phe = numpy.zeros(shape=(70,5))
Phe = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Phe.csv'))
Pic = numpy.zeros(shape=(50,5))
Pic = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Pic.csv'))
Psc = numpy.zeros(shape=(141,5))
Psc = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Psc.csv'))
PsA = numpy.zeros(shape=(49,5))
PsA = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','PsA.csv'))
Pup = numpy.zeros(shape=(275,5))
Pup = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Pup.csv'))
Pyx = numpy.zeros(shape=(48,5))
Pyx = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Pyx.csv'))
Ret = numpy.zeros(shape=(24,5))
Ret = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ret.csv'))
Sge = numpy.zeros(shape=(31,5))
Sge = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Sge.csv'))
Sgr = numpy.zeros(shape=(219,5))
Sgr = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Sgr.csv'))
Sco = numpy.zeros(shape=(174,5))
Sco = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Sco.csv'))
Scl = numpy.zeros(shape=(59,5))
Scl = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Scl.csv'))
Sct = numpy.zeros(shape=(30,5))
Sct = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Sct.csv'))
Ser = numpy.zeros(shape=(112,5))
Ser = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Ser.csv'))
Sex = numpy.zeros(shape=(40,5))
Sex = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Sex.csv'))
Tau = numpy.zeros(shape=(223,5))
Tau = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Tau.csv'))
Tel = numpy.zeros(shape=(51,5))
Tel = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Tel.csv'))
Tri = numpy.zeros(shape=(26,5))
Tri = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Tri.csv'))
TrA = numpy.zeros(shape=(35,5))
TrA = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','TrA.csv'))
Tuc = numpy.zeros(shape=(50,5))
Tuc = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Tuc.csv'))
UMa = numpy.zeros(shape=(224,5))
UMa = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','UMa.csv'))
UMi = numpy.zeros(shape=(42,5))
UMi = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','UMi.csv'))
Vel = numpy.zeros(shape=(193,5))
Vel = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Vel.csv'))
Vir = numpy.zeros(shape=(174,5))
Vir = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Vir.csv'))
Vol = numpy.zeros(shape=(33,5))
Vol = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Vol.csv'))
Vul = numpy.zeros(shape=(77,5))
Vul = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','Vul.csv'))
# LROC WAC basemap Shapefile
Mare    = numpy.zeros(shape=(267482,5)) 
Mare    = pandas.read_csv(pathlib.Path.cwd().joinpath('data','moon','moon_mare.csv'))
Crater  = numpy.zeros(shape=(182111,5))
Crater  = pandas.read_csv(pathlib.Path.cwd().joinpath('data','moon','moon_crater.csv'))
# milkyway
MW_southernedge = numpy.zeros(shape=(263,4))
MW_southernedge = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_southernedge.csv'))
MW_MonPer       = numpy.zeros(shape=(71,4))
MW_MonPer       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_MonPer.csv'))
MW_CamCas       = numpy.zeros(shape=(13,4))
MW_CamCas       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_CamCas.csv'))
MW_Cep          = numpy.zeros(shape=(13,4))
MW_Cep          = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_Cep.csv'))
MW_CygOph       = numpy.zeros(shape=(40,4))
MW_CygOph       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_CygOph.csv'))
MW_OphSco       = numpy.zeros(shape=(17,4))
MW_OphSco       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_OphSco.csv'))
MW_LupVel       = numpy.zeros(shape=(78,4))
MW_LupVel       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_LupVel.csv'))
MW_VelMon       = numpy.zeros(shape=(34,4))
MW_VelMon       = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_VelMon.csv'))
dark_PerCas     = numpy.zeros(shape=(35,4))
dark_PerCas     = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_PerCas.csv'))
dark_CasCep     = numpy.zeros(shape=(28,4))
dark_CasCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_CasCep.csv'))
dark_betaCas    = numpy.zeros(shape=(20,4))
dark_betaCas    = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_betaCas.csv'))
dark_CygCep     = numpy.zeros(shape=(22,4))
dark_CygCep     = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_CygCep.csv'))
dark_CygOph     = numpy.zeros(shape=(197,4))
dark_CygOph     = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_CygOph.csv'))
dark_thetaOph   = numpy.zeros(shape=(28,4))
dark_thetaOph   = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_thetaOph.csv'))
dark_lambdaSco  = numpy.zeros(shape=(17,4))
dark_lambdaSco  = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_lambdaSco.csv'))
dark_ScoNor     = numpy.zeros(shape=(31,4))
dark_ScoNor     = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_ScoNor.csv'))
dark_Coalsack   = numpy.zeros(shape=(32,4))
dark_Coalsack   = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_Coalsack.csv'))
dark_Vel        = numpy.zeros(shape=(22,4))
dark_Vel        = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','dark_Vel.csv'))
MW_LMC1         = numpy.zeros(shape=(34,4))
MW_LMC1         = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_LMC1.csv'))
MW_LMC2         = numpy.zeros(shape=(12,4))
MW_LMC2         = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_LMC2.csv'))
MW_SMC          = numpy.zeros(shape=(14,4))
MW_SMC          = pandas.read_csv(pathlib.Path.cwd().joinpath('data','milkyway','MW_SMC.csv'))
# constellation boundaries
boundary        = numpy.zeros(shape=(13238,5))
boundary        = pandas.read_csv(pathlib.Path.cwd().joinpath('data','constellation_western','boundary.csv'))

if debug_mode == 1:
    timelog('ref count And: '+str(sys.getrefcount(And)))
    timelog('ref count Mare: '+str(sys.getrefcount(Mare)))
    timelog('ref count MW_southernedge: '+str(sys.getrefcount(MW_southernedge)))
    timelog('ref count boundary: '+str(sys.getrefcount(boundary)))
    
####################
# define functions #
####################

def plot_solar():
    Tsolar0 = time.time()
    global plot_alpha, hori_border, hori_xmax, hori_xmin, hori_ymax, hori_ymin, horizon_poly, equator_poly, ecliptic_poly,\
           sun_vector, moon_vector, mercury_vector, venus_vector, mars_vector, jupiter_vector, Io, Europa, Ganymede, Callisto, saturn_vector, uranus_vector, neptune_vector,\
           solar_obj,solar_color,moon_chi,\
           Sun_x,Moon_x,Mercury_x,Venus_x,Mars_x,Jupiter_x,Saturn_x,Uranus_x,Neptune_x,\
           Sun_y,Moon_y,Mercury_y,Venus_y,Mars_y,Jupiter_y,Saturn_y,Uranus_y,Neptune_y

    sun_vector      = OBS[0].at(date_UTC).observe(sun).apparent()
    mercury_vector  = OBS[0].at(date_UTC).observe(mercury).apparent()
    venus_vector    = OBS[0].at(date_UTC).observe(venus).apparent()
    moon_vector     = OBS[0].at(date_UTC).observe(moon).apparent()
    mars_vector     = OBS[0].at(date_UTC).observe(mars).apparent()
    jupiter_vector  = OBS[0].at(date_UTC).observe(jupiter).apparent()
    saturn_vector   = OBS[0].at(date_UTC).observe(saturn).apparent()
    uranus_vector   = OBS[0].at(date_UTC).observe(uranus).apparent()
    neptune_vector  = OBS[0].at(date_UTC).observe(neptune).apparent()
    pluto_vector    = OBS[0].at(date_UTC).observe(pluto).apparent()
    
    # position angle of the Moon's bright limb from North point of the disc of the Moon to East
    moon_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-moon_vector.radec()[0].radians),
                                       math.sin(sun_vector.radec()[1].radians)*math.cos(moon_vector.radec()[1].radians)-
                                       math.cos(sun_vector.radec()[1].radians)*math.sin(moon_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-moon_vector.radec()[0].radians))) % 360

    timelog('drawing grids')

    # alpha
    if sun_vector.altaz()[0].degrees >= 0:
        plot_alpha = 0.2
    else:
        plot_alpha = 0.15
        
    # horizon ###################################
    hori_ra = []
    hori_dec= []
    for i in range(361):
        hori_ra.append(OBS[0].at(date_UTC).from_altaz(alt_degrees=0, az_degrees=i).radec()[0].hours*15)
        hori_dec.append(OBS[0].at(date_UTC).from_altaz(alt_degrees=0, az_degrees=i).radec()[1].degrees)

    horizon_pt = list(zip(map(transform_x,hori_ra,hori_dec),map(transform_y,hori_ra,hori_dec)))
        
    horizon_poly = plt.Polygon(horizon_pt, closed=True, fill=None, edgecolor=(0,1,0,1), zorder=1+2.5)
    ax0.add_patch(horizon_poly)

    # horizon size
    hori_xmax = max(horizon_pt,key=itemgetter(0))[0]
    hori_xmin = min(horizon_pt,key=itemgetter(0))[0]
    hori_ymax = max(horizon_pt,key=itemgetter(1))[1]
    hori_ymin = min(horizon_pt,key=itemgetter(1))[1]
    hori_border = hori_xmax-hori_xmin

    ax0.annotate('z',((hori_xmax+hori_xmin)/2+2.5,(hori_ymax+hori_ymin)/2+1),color='g')
    z_m = matplotlib.markers.MarkerStyle(marker='+')
    z_m._transform = z_m.get_transform().rotate_deg(rotate_angle)
    ax0.scatter((hori_xmax+hori_xmin)/2,(hori_ymax+hori_ymin)/2,c='g',marker=z_m)
    
    # equator ###################################
    equator_pt = list(zip(map(transform_x,list(range(361)),[0]*361),map(transform_y,list(range(361)),[0]*361)))
    
    equator_poly = plt.Polygon(equator_pt, closed=False, fill=None, edgecolor=(1,0,0,plot_alpha), zorder=1+2.5)
    equator_poly.set_clip_path(horizon_poly)
    ax0.add_patch(equator_poly)

    # ecliptic ###################################
    epsilon_J2000 = 23.4392911
    eclip_ra = []
    eclip_dec= []

    # ecliptic lon at horizon
    ec_hori_X = math.degrees(math.atan2(-math.cos(math.radians(15*sidereal_time)),math.sin(math.radians(epsilon_J2000))*math.tan(math.radians(OBS[1]))+math.cos(math.radians(epsilon_J2000))*math.sin(math.radians(15*sidereal_time))))
    
    for i in numpy.linspace(ec_hori_X-10,ec_hori_X+190,180):
        eclip_ra.append(math.degrees(math.atan2(math.sin(math.radians(i))*math.cos(math.radians(epsilon_J2000)),math.cos(math.radians(i)))))
        eclip_dec.append(math.degrees(math.asin(math.sin(math.radians(epsilon_J2000))*math.sin(math.radians(i)))))

    ecliptic_pt = list(zip(map(transform_x,eclip_ra,eclip_dec),map(transform_y,eclip_ra,eclip_dec)))
        
    ecliptic_poly = plt.Polygon(ecliptic_pt, closed=False, fill=None, edgecolor=(1,1,0,plot_alpha), zorder=1+2.5)
    ecliptic_poly.set_clip_path(horizon_poly)
    ax0.add_patch(ecliptic_poly)   

    #solar object ###################################
    timelog('plotting solar system objects')

    Sun_x       = transform_x(sun_vector.radec()[0]._degrees,sun_vector.radec()[1]._degrees)
    Sun_y       = transform_y(sun_vector.radec()[0]._degrees,sun_vector.radec()[1]._degrees)
    Moon_x      = transform_x(moon_vector.radec()[0]._degrees,moon_vector.radec()[1]._degrees)
    Moon_y      = transform_y(moon_vector.radec()[0]._degrees,moon_vector.radec()[1]._degrees)
    Mercury_x   = transform_x(mercury_vector.radec()[0]._degrees,mercury_vector.radec()[1]._degrees)
    Mercury_y   = transform_y(mercury_vector.radec()[0]._degrees,mercury_vector.radec()[1]._degrees)
    Venus_x     = transform_x(venus_vector.radec()[0]._degrees,venus_vector.radec()[1]._degrees)
    Venus_y     = transform_y(venus_vector.radec()[0]._degrees,venus_vector.radec()[1]._degrees)
    Mars_x      = transform_x(mars_vector.radec()[0]._degrees,mars_vector.radec()[1]._degrees)
    Mars_y      = transform_y(mars_vector.radec()[0]._degrees,mars_vector.radec()[1]._degrees)
    Jupiter_x   = transform_x(jupiter_vector.radec()[0]._degrees,jupiter_vector.radec()[1]._degrees)
    Jupiter_y   = transform_y(jupiter_vector.radec()[0]._degrees,jupiter_vector.radec()[1]._degrees)
    Saturn_x    = transform_x(saturn_vector.radec()[0]._degrees,saturn_vector.radec()[1]._degrees)
    Saturn_y    = transform_y(saturn_vector.radec()[0]._degrees,saturn_vector.radec()[1]._degrees)
    Uranus_x    = transform_x(uranus_vector.radec()[0]._degrees,uranus_vector.radec()[1]._degrees)
    Uranus_y    = transform_y(uranus_vector.radec()[0]._degrees,uranus_vector.radec()[1]._degrees)
    Neptune_x   = transform_x(neptune_vector.radec()[0]._degrees,neptune_vector.radec()[1]._degrees)
    Neptune_y   = transform_y(neptune_vector.radec()[0]._degrees,neptune_vector.radec()[1]._degrees)

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

    Tsolar1 = time.time()
    #print(Tsolar1-Tsolar0)

    if debug_mode == 1:
        timelog('ref count horizon_poly: '+str(sys.getrefcount(horizon_poly)))
        timelog('ref count equator_poly: '+str(sys.getrefcount(equator_poly)))
        timelog('ref count ecliptic_pt: '+str(sys.getrefcount(ecliptic_pt)))
        timelog('ref count ecliptic_poly: '+str(sys.getrefcount(ecliptic_poly)))
        timelog('ref count Sun_x: '+str(sys.getrefcount(Sun_x)))
        timelog('ref count Sun_y: '+str(sys.getrefcount(Sun_y)))
        timelog('ref count solar_pos_x: '+str(sys.getrefcount(solar_pos_x)))
        timelog('ref count solar_pos_y: '+str(sys.getrefcount(solar_pos_y)))
        timelog('ref count solar_color: '+str(sys.getrefcount(solar_color)))
        timelog('ref count solar_obj: '+str(sys.getrefcount(solar_obj)))

def plot_constellation():
    Tconstellation0 = time.time()
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
        df['xy'] = list(zip(df.x,df.y))

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
    
    constellation_line = [[And.xy,And_line,'And'],[Ant.xy,Ant_line,'Ant'],[Aps.xy,Aps_line,'Aps'],[Aqr.xy,Aqr_line,'$\u2652$'],\
                          [Aql.xy,Aql_line,'Aql'],[Ara.xy,Ara_line,'Ara'],[Ari.xy,Ari_line,'$\u2648$'],[Aur.xy,Aur_line,'Aur'],\
                          [Boo.xy,Boo_line,'Boo'],[Cae.xy,Cae_line,'Cae'],[Cam.xy,Cam_line,'Cam'],[Cnc.xy,Cnc_line,'$\u264B$'],\
                          [CVn.xy,CVn_line,'CVn'],[CMa.xy,CMa_line,'CMa'],[CMi.xy,CMi_line,'CMi'],[Cap.xy,Cap_line,'$\u2651$'],\
                          [Car.xy,Car_line,'Car'],[Cas.xy,Cas_line,'Cas'],[Cen.xy,Cen_line,'Cen'],[Cep.xy,Cep_line,'Cep'],\
                          [Cet.xy,Cet_line,'Cet'],[Cha.xy,Cha_line,'Cha'],[Cir.xy,Cir_line,'Cir'],[Col.xy,Col_line,'Col'],\
                          [Com.xy,Com_line,'Com'],[CrA.xy,CrA_line,'CrA'],[CrB.xy,CrB_line,'CrB'],[Crv.xy,Crv_line,'Crv'],\
                          [Crt.xy,Crt_line,'Crt'],[Cru.xy,Cru_line,'Cru'],[Cyg.xy,Cyg_line,'Cyg'],[Del.xy,Del_line,'Del'],\
                          [Dor.xy,Dor_line,'Dor'],[Dra.xy,Dra_line,'Dra'],[Equ.xy,Equ_line,'Equ'],[Eri.xy,Eri_line,'Eri'],\
                          [For.xy,For_line,'For'],[Gem.xy,Gem_line,'$\u264A$'],[Gru.xy,Gru_line,'Gru'],[Her.xy,Her_line,'Her'],\
                          [Hor.xy,Hor_line,'Hor'],[Hya.xy,Hya_line,'Hya'],[Hyi.xy,Hyi_line,'Hyi'],[Ind.xy,Ind_line,'Ind'],\
                          [Lac.xy,Lac_line,'Lac'],[Leo.xy,Leo_line,'$\u264C$'],[LMi.xy,LMi_line,'LMi'],[Lep.xy,Lep_line,'Lep'],\
                          [Lib.xy,Lib_line,'$\u264E$'],[Lup.xy,Lup_line,'Lup'],[Lyn.xy,Lyn_line,'Lyn'],[Lyr.xy,Lyr_line,'Lyr'],\
                          [Men.xy,Men_line,'Men'],[Mic.xy,Mic_line,'Mic'],[Mon.xy,Mon_line,'Mon'],[Mus.xy,Mus_line,'Mus'],\
                          [Nor.xy,Nor_line,'Nor'],[Oct.xy,Oct_line,'Oct'],[Oph.xy,Oph_line,'Oph'],[Ori.xy,Ori_line,'Ori'],\
                          [Pav.xy,Pav_line,'Pav'],[Peg.xy,Peg_line,'Peg'],[Per.xy,Per_line,'Per'],[Phe.xy,Phe_line,'Phe'],\
                          [Pic.xy,Pic_line,'Pic'],[Psc.xy,Psc_line,'$\u2653$'],[PsA.xy,PsA_line,'PsA'],[Pup.xy,Pup_line,'Pup'],\
                          [Pyx.xy,Pyx_line,'Pyx'],[Ret.xy,Ret_line,'Ret'],[Sge.xy,Sge_line,'Sge'],[Sgr.xy,Sgr_line,'$\u2650$'],\
                          [Sco.xy,Sco_line,'$\u264F$'],[Scl.xy,Scl_line,'Scl'],[Sct.xy,Sct_line,'Sct'],[Ser.xy,Ser_line,'Ser'],\
                          [Sex.xy,Sex_line,'Sex'],[Tau.xy,Tau_line,'$\u2649$'],[Tel.xy,Tel_line,'Tel'],[Tri.xy,Tri_line,'Tri'],\
                          [TrA.xy,TrA_line,'TrA'],[Tuc.xy,Tuc_line,'Tuc'],[UMa.xy,UMa_line,'UMa'],[UMi.xy,UMi_line,'UMi'],\
                          [Vel.xy,Vel_line,'Vel'],[Vir.xy,Vir_line,'$\u264D$'],[Vol.xy,Vol_line,'Vol'],[Vul.xy,Vul_line,'Vul']]

    # constellation linecollection
    constellation_line_z_xy = []
    constellation_line_xy = []
    for i in range(len(constellation_line)):
        for j in range(len(constellation_line[i][1])):
            if i in set([3,6,11,15,37,45,48,58,65,71,72,77,85]): # zodiacs
                constellation_line_z_xy.append((constellation_line[i][0][constellation_line[i][1][j][0]],constellation_line[i][0][constellation_line[i][1][j][1]]))
            else:
                constellation_line_xy.append((constellation_line[i][0][constellation_line[i][1][j][0]],constellation_line[i][0][constellation_line[i][1][j][1]]))
    
    lc_west_z = mc.LineCollection(constellation_line_z_xy, colors=[(1,1,0,plot_alpha) if numpy.hypot((x1-x2),(y1-y2)) < hori_border/2
                                                                   else (0,0,0,0) for ((x1,y1),(x2,y2)) in constellation_line_z_xy], zorder=10+2.5)
    lc_west = mc.LineCollection(constellation_line_xy, colors=[(1,1,1,plot_alpha) if numpy.hypot((x1-x2),(y1-y2)) < hori_border/2
                                                               else (0,0,0,0) for ((x1,y1),(x2,y2)) in constellation_line_xy], zorder=10+2.5)
    ax0.add_collection(lc_west_z)
    ax0.add_collection(lc_west)

   # others linecollection       
    constellation_dotted_line = [[(Aur.x[3],Aur.y[3]),(Tau.x[1],Tau.y[1])],[(Aur.x[2],Aur.y[2]),(Tau.x[1],Tau.y[1])],\
                                 [(Peg.x[1],Peg.y[1]),(And.x[0],And.y[0])],[(Peg.x[3],Peg.y[3]),(And.x[0],And.y[0])],\
                                 [(Ser.x[3],Ser.y[3]),(Oph.x[7],Oph.y[7])],[(Ser.x[2],Ser.y[2]),(Oph.x[3],Oph.y[3])],\
                                 [(PsA.x[0],PsA.y[0]),(Aqr.x[18],Aqr.y[18])]]

    constellation_dotted_line_list = []
    for i in range(len(constellation_dotted_line)):
        constellation_dotted_line_list.append(constellation_dotted_line[i])
    
    lc_west_dotted = mc.LineCollection(constellation_dotted_line_list, colors=[(1,1,1,plot_alpha) if numpy.hypot((x1-x2),(y1-y2)) < hori_border/2
                                                                               else (0,0,0,0) for ((x1,y1),(x2,y2)) in constellation_dotted_line_list], linestyles='dashed',zorder=10+2.5)
    ax0.add_collection(lc_west_dotted)

    # annotation
    for xy,z,n in constellation_line:
        if n in set(['$\u2652$','$\u2648$','$\u264B$','$\u2651$','$\u264A$','$\u264C$','$\u264E$','$\u2653$','$\u2650$','$\u264F$','$\u2649$','$\u264D$']):
            hypotenu = math.hypot(list(sum(xys)/len(xys) for xys in zip(*xy))[0]-x_shift,list(sum(xys)/len(xys) for xys in zip(*xy))[1]-y_shift)
            sqrtdiff = math.sqrt(((hori_border/2)**2)-(1-aspect_ratio**2)*((list(sum(xys)/len(xys) for xys in zip(*xy))[1]-y_shift)/aspect_ratio)**2)
            if hypotenu < sqrtdiff and max(xy,key=itemgetter(0))[0]-min(xy,key=itemgetter(0))[0] < hori_border:
                ax0.annotate(str(n),((list(sum(xys)/len(xys) for xys in zip(*xy)))[0],(list(sum(xys)/len(xys) for xys in zip(*xy)))[1]-labelxy),color='y')

    Tconstellation1 = time.time()
    #print(Tconstellation1-Tconstellation0)
    
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
    Tmw0 = time.time()
    
    timelog('weaving Milkyway')
    
    MW_list = [MW_southernedge,MW_MonPer,MW_CamCas,MW_Cep,MW_CygOph,MW_OphSco,MW_LupVel,MW_VelMon,\
               dark_PerCas,dark_CasCep,dark_betaCas,dark_CygCep,dark_CygOph,dark_thetaOph,dark_lambdaSco,dark_ScoNor,dark_Coalsack,dark_Vel,\
               MW_LMC1,MW_LMC2,MW_SMC]

    MW_line_list = []
    for df in MW_list:
        df.x = list(map(transform_x, df.RA, df.Dec))
        df.y = list(map(transform_y, df.RA, df.Dec))
        
        df['xy'] = list(zip(df.x,df.y))
        dflist = [(x,y) for x,y in df['xy'] if hori_xmin < x < hori_xmax and hori_ymin < y < hori_ymax]
    
        if dflist != []:
            MW_line_list.append(dflist)

    lc_MW = mc.LineCollection(MW_line_list, colors='b',alpha=plot_alpha/4, zorder=1+2.5)
    lc_MW.set_clip_path(horizon_poly)
    ax0.add_collection(lc_MW)

    Tmw1 = time.time()
    #print(Tmw1-Tmw0)

    if debug_mode == 1:
        timelog('ref count MW_list: '+str(sys.getrefcount(MW_list)))
        timelog('ref count MW_line_list: '+str(sys.getrefcount(MW_line_list)))
        timelog('ref count lc_MW: '+str(sys.getrefcount(lc_MW)))

def plot_boundary():
    Tb0 = time.time()
    
    timelog('drawing boundaries')

    boundary.x = list(map(transform_x, boundary.RA*15, boundary.Dec)) #convert RA to degrees
    boundary.y = list(map(transform_y, boundary.RA*15, boundary.Dec))
    
    boundary['xy'] = list(zip(boundary.x,boundary.y))
    boundary_pt_lists = boundary.groupby('Constellation')['xy'].apply(pandas.Series.tolist).tolist()

    for boundary_pt_list in boundary_pt_lists:
        if max(numpy.sqrt((numpy.diff(boundary_pt_list, axis=0) ** 2).sum(axis=1))) > hori_border/2:
            boundary_pt_lists.remove(boundary_pt_list)
        
    pc_boundary = mc.PolyCollection(boundary_pt_lists, closed=True, facecolors=[0,0,0,0], edgecolors=[1,0.5,0,plot_alpha/2], zorder=1+2.5)
    pc_boundary.set_clip_path(horizon_poly)
    ax0.add_collection(pc_boundary)

    Tb1 = time.time()
    #print(Tb1-Tb0)

    if debug_mode == 1:
        timelog('ref count boundary.x: '+str(sys.getrefcount(boundary.x)))
        timelog('ref count boundary.y: '+str(sys.getrefcount(boundary.y)))
        timelog('ref count boundary_line_list: '+str(sys.getrefcount(boundary_line_list)))
        timelog('ref count lc_boundary: '+str(sys.getrefcount(lc_boundary)))
 
def write_label(x,y,z,c1,c2,c3):
    Ts0 = time.time()
    
    if (x,y,z) == (0,0,0):
        timelog('timestamp')

    ax0.annotate(OBS[4]+'\n'+OBS[6],(hori_xmax+x-60,hori_ymin+y+20),ha='right',color=c1,zorder=12+2.5+z)
    ax0.annotate(OBS[3]+'\n'+OBS[5],(hori_xmax+x,hori_ymin+y+20),ha='right',color=c1,zorder=12+2.5+z)
    ax0.annotate('可觀自然教育中心暨天文館',(hori_xmax+x,hori_ymax+y),ha='right',va='top',fontproperties=chara_chi,fontsize=10,color=c1,zorder=12+2.5+z)
    ax0.annotate('Ho Koon Nature Education cum\nAstronomical Centre',(hori_xmax+x,hori_ymax+y-10),ha='right',va='top',color=c1,zorder=12+2.5+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x,hori_ymin+y),ha='right',color=c1,zorder=12+2.5+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x+1,hori_ymin+y+1),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x,hori_ymin+y+1),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x-1,hori_ymin+y+1),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x+1,hori_ymin+y),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x-1,hori_ymin+y),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x+1,hori_ymin+y-1),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x,hori_ymin+y-1),ha='right',color='k',zorder=12+2.4+z)
    ax0.annotate('sky at HKT '+str(date_local.strftime('%d/%m/%Y %H:%M:%S')),(hori_xmax+x-1,hori_ymin+y-1),ha='right',color='k',zorder=12+2.4+z)
    # ax0.annotate('ephemeris by Skyfield (ascl:1907.024)',(360+x,hori_ymin+y),rotation=90,ha='right',va='bottom',color=c2,zorder=12+2.5+z)

    Ts1 = time.time()
    #print(Ts1-Ts0)

def update_para():
    global transform_x, transform_y, sidereal_time, ra0, dec0, zenith_shift_ra, zenith_shift_dec, rotate_angle, aspect_ratio, plot_scale, x_shift, y_shift

    sidereal_time = date_UTC.gmst+OBS[2]/15
    ra0 = 15*sidereal_time + zenith_shift_ra
    dec0 = OBS[1] + zenith_shift_dec
    
    #@jit
    def transform_x(x,y):
        transform_x = x_shift+plot_scale\
                      *(math.cos(math.radians(rotate_angle))\
                        *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                        *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                        -math.sin(math.radians(rotate_angle))\
                        *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                        *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
        return transform_x

    #@jit
    def transform_y(x,y):
        transform_y = y_shift+aspect_ratio*plot_scale\
                      *(math.sin(math.radians(rotate_angle))\
                        *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                        *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                        +math.cos(math.radians(rotate_angle))\
                        *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                        *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
        return transform_y
    
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
    write_label(0,0,0,'w','dimgrey','y')
    cloud_detection()
    # write_weather()

    Tmv0 = time.time()

    timelog('drawing Mercury and Venus')
    
    ax3.set_xlim((-90,90))
    ax3.set_ylim((-50,50))

    mercury_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-mercury_vector.radec()[0].radians),
                                          math.sin(sun_vector.radec()[1].radians)*math.cos(mercury_vector.radec()[1].radians)
                                          -math.cos(sun_vector.radec()[1].radians)*math.sin(mercury_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-mercury_vector.radec()[0].radians))) % 360

    venus_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians),
                                        math.sin(sun_vector.radec()[1].radians)*math.cos(venus_vector.radec()[1].radians)
                                        -math.cos(sun_vector.radec()[1].radians)*math.sin(venus_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians))) % 360

    ax3.annotate('Mercury & Venus',(0,35),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white')

    Mercury_offsetx = -45
    Venus_offsetx = 45
    MV_d = 30
    rot_pa_limb_mercury = mercury_chi-90
    rot_pa_limb_venus = venus_chi-90

    Mercury_precent = almanac.fraction_illuminated(ephem, 'mercury', date_UTC)
    Venus_percent = almanac.fraction_illuminated(ephem, 'venus', date_UTC)

    if Mercury_precent == 0:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), 0, 0, 0, color='black') #dummy
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='black') #dummy
    elif 0 < Mercury_precent < 0.5:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='#97979F')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 270+rot_pa_limb_mercury, 90+rot_pa_limb_mercury, color='black')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), MV_d*(1-Mercury_precent/0.5), MV_d, angle=rot_pa_limb_mercury, color='black')
    elif Mercury_precent == 0.5:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 90+rot_pa_limb_mercury, 270+rot_pa_limb_mercury, color='#97979F')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='#97979F') #dummy
    elif 0.5 < Mercury_precent < 1:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='black')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), MV_d/2, 90+rot_pa_limb_mercury, 270+rot_pa_limb_mercury, color='#97979F')
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), MV_d*(1-Mercury_precent/0.5), MV_d, angle=rot_pa_limb_mercury, color='#97979F')
    elif Mercury_precent == 1:
        Merdisc0 = patches.Circle((Mercury_offsetx,0), MV_d/2, color='#97979F')
        Merdisc1 = patches.Wedge((Mercury_offsetx,0), 0, 0, 0,color='#97979F') #dummy
        Merdisc2 = patches.Ellipse((Mercury_offsetx,0), 0, 0, 0, color='#97979F') #dummy

    ax3.add_patch(Merdisc0)
    ax3.add_patch(Merdisc1)
    ax3.add_patch(Merdisc2)

    if Venus_percent == 0:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), 0, 0, 0, color='black') #dummy
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='black') #dummy
    elif 0 < Venus_percent < 0.5:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='#C18F17')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 270+rot_pa_limb_venus, 90+rot_pa_limb_venus, color='black')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), MV_d*(1-Venus_percent/0.5), MV_d, angle=rot_pa_limb_venus, color='black')
    elif Venus_percent == 0.5:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 90+rot_pa_limb_venus, 270+rot_pa_limb_venus, color='#C18F17')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='#C18F17') #dummy
    elif 0.5 < Venus_percent < 1:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='black')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), MV_d/2, 90+rot_pa_limb_venus, 270+rot_pa_limb_venus, color='#C18F17')
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), MV_d*(1-Venus_percent/0.5), MV_d, angle=rot_pa_limb_venus, color='#C18F17')
    elif Venus_percent == 1:
        Vendisc0 = patches.Circle((Venus_offsetx,0), MV_d/2, color='#C18F17')
        Vendisc1 = patches.Wedge((Venus_offsetx,0), 0, 0, 0,color='#C18F17') #dummy
        Vendisc2 = patches.Ellipse((Venus_offsetx,0), 0, 0, 0, color='#C18F17') #dummy

    ax3.add_patch(Vendisc0)
    ax3.add_patch(Vendisc1)
    ax3.add_patch(Vendisc2)

    dist_SM = math.degrees(math.acos(math.sin(sun_vector.radec()[1].radians)*math.sin(mercury_vector.radec()[1].radians)+math.cos(sun_vector.radec()[1].radians)*math.cos(mercury_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-mercury_vector.radec()[0].radians)))
    ax3.annotate(str(round(dist_SM,1))+u'\N{DEGREE SIGN}',(Mercury_offsetx,0),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8,color='#FFCC33')
    dist_SV = math.degrees(math.acos(math.sin(sun_vector.radec()[1].radians)*math.sin(venus_vector.radec()[1].radians)+math.cos(sun_vector.radec()[1].radians)*math.cos(venus_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians)))
    ax3.annotate(str(round(dist_SV,1))+u'\N{DEGREE SIGN}',(Venus_offsetx,0),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8,color='#FFCC33')
    
    ax3.annotate('\u2190 E',(-90,-35),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_10,color='red')
    ax3.annotate('dist. from Sun',(0,-35),xycoords=('data'),ha='center',va='bottom',fontproperties=DjV_S_8,color='#FFCC33')
    ax3.annotate('W \u2192',(90,-35),xycoords=('data'),ha='right',va='bottom',fontproperties=DjV_S_10,color='red')

    Tmv1 = time.time()
    #print(Tmv1-Tmv0)

def cloud_detection(): #ax4
    Tcc0 = time.time()
    
    timelog('counting cloud')
    
    ax4.set_xlim((-90,90))
    ax4.set_ylim((-40,80))

    ax4.annotate('Cloud Coverage',(0,75),xycoords=('data'),ha='center',va='top',fontproperties=DjV_S_12,color='white',zorder=11)
    ax4.annotate('experimental',(0,50),xycoords=('data'),ha='center',va='center',fontproperties=DjV_S_8, color='red',zorder=11)
    CC_bg = patches.Rectangle((-90,40),180,40,color='k',zorder=10)
    ax4.add_patch(CC_bg)
    
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
        if -18 <= sun_vector.altaz()[0]._degrees <= 0: # twilight
            sky_con = 'っω-) twilight'
            ss_color = '#9DA5BF'
            l_color = '#9DA5BF'
            CC = numpy.nan
        elif 0 < sun_vector.altaz()[0]._degrees <= 15: # low angle
            if sun_vector.altaz()[1]._degrees < 180:
                sky_con = 'っω-) sunrise'
                ss_color = '#FFCC33'
                l_color = '#FFCC33'
            else:
                sky_con = '-_-)ﾉｼ sunset'
                ss_color = '#FD5E53'
                l_color = '#FD5E53'
            CC = numpy.nan
        elif 15 < sun_vector.altaz()[0]._degrees: # daytime
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

    except Exception as e:
        print(e)
        ax4.annotate('_(:3」∠)_ fail',(0,0),xycoords=('data'),ha='center',va='center',fontproperties=emoji_20, color='white',zorder=3)
        ax4.set_facecolor('red')

    Tcc1 = time.time()
    #print(Tcc1-Tcc0)

   
def refresh_sky(i):
    global fig, asc, CC_hokoon, count, date_UTC, date_local

    #################################
    # read record and put timestamp #
    #################################       
    CC_hokoon = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CC_hokoon.csv'), index_col=0)
    #print(CC_hokoon.memory_usage(deep=True))
    CC_hokoon = CC_hokoon.append({'HKT':str(date_local.strftime('%Y/%m/%d %H:%M:%S'))}, ignore_index=True) # can't use datetime in dict
    CC_hokoon['HKT'] = pandas.to_datetime(CC_hokoon['HKT'],yearfirst=True) # convert to datetime object

    ###########
    # removal #
    ###########
    start = time.time()
    count = count + 1

    # clear the world
    gc.collect()
    try:
        ax0.clear()
        ax3.clear()
        ax4.clear()
        timelog('Armageddon')
    except:
        timelog('survivor')

    ##########
    # update #
    ##########

    # update time
    date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
    date_local  = date_UTC.astimezone(tz)

    # update ASC
    socket.setdefaulttimeout(10)
    try:
        try:
            urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
            asc = Image.open('asc.jpg')
            asc = asc.resize((720,480),Image.ANTIALIAS)
#     except ContentTooShortError: # try again
#         timelog('try again')
#         urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
#         asc = Image.open('asc.jpg')
#         asc = asc.resize((720,480),Image.ANTIALIAS)
        except Exception as e:
            print(e)
            urlretrieve('http://192.168.1.222/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
            asc = Image.open('asc.jpg')
            asc = asc.resize((720,480),Image.ANTIALIAS)
#     except HTTPError:
#         asc = Image.open(pathlib.Path.cwd().joinpath('ASC','serverdead.jpg'))
    except Exception as e:
        print(e)
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','black.jpg'))
        
    # update transformation
    update_para()

    try:
        plot_ASC()
    except:
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','black.jpg'))
        plot_ASC()

    # plot
    fig.canvas.draw() 
    fig.canvas.flush_events()
    #fig.savefig('Hokoon_ASIM_'+str("{:%Y_%m_%d-%H_%M_%S}".format(datetime.now()))+'.png')
    #plt.savefig('Hokoon_ASIM_'+str("{:%Y_%m_%d-%H_%M_%S}".format(datetime.now()))+'.png')
    plt.savefig('output/Hokoon_ASC.png')
    
    # make red version
    img = Image.open("output/Hokoon_ASC.png").convert("RGB")
    width, height = img.size
    pixels = img.load()
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            newR = round((r+g+b)/3) if ((r+g+b)/3)>90 else round((r+g+b)/3+(r+g)/2.5)
            newG = 0
            newB = 0
            pixels[px, py] = (newR, newG, newB)
    img.save("output/Hokoon_ASC_red.png")

    ########################
    #  get sunspot number  #
    ########################

    try:
        link_ss = 'http://sidc.oma.be/silso/home'
        html_ss = requests.get(link_ss).text
        soup_ss = BeautifulSoup(html_ss, 'html.parser')
        SW_ss = soup_ss.find_all('table')[1].get_text().split()[-1]
        f = open("output/sunspot.json", "w")
        f.write("{ \"ssn\" \n: " + SW_ss + "\n}")
        f.close()
    except:
        print('silso fail')
        try:
            link_ss = 'http://spaceweather.com/'
            html_ss = requests.get(link_ss).text
            soup_ss = BeautifulSoup(html_ss, 'html.parser')
            SW_ss = soup_ss.find_all(class_='solarWindText')[4].get_text().split()[2]
            f = open("output/sunspot.json", "w")
            f.write(SW_ss)
            f.close()
        except:
            print('spaceweather fail')
        pass

    #upload to SFTP
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    userfile = open("id.txt", "r")
    user = userfile.read()
    pwfile = open("pw.txt", "r")
    password = pwfile.read()
    with pysftp.Connection('192.168.1.223', username=user, password=password, cnopts=cnopts) as sftp:
        sftp.cwd("/var/www/html/astroInfo/images")
        sftp.put("./output/Hokoon_ASC.png", "./Hokoon_ASC.png")
        sftp.put( "./output/Hokoon_ASC_red.png", "./Hokoon_ASC_red.png")
        sftp.put( "./output/sunspot.json", "./sunspot.json")
        sftp.close()

    timelog('ftp upload job done')

    ########################
    # save and trim record #
    ########################
    CC_hokoon.drop(CC_hokoon[CC_hokoon['HKT'] <= datetime.now()-timedelta(hours=24)].index, inplace=True) # keep only last 24h data
    CC_hokoon.reset_index(drop=True,inplace=True)

    CC_hokoon.to_csv(pathlib.Path.cwd().joinpath('ASC','CC_hokoon.csv'))

    end = time.time()
    timelog(str(round(end-start,2))+'s wasted')
    
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

def refresh_refresh_sky(i):
    try:
        refresh_sky(i)
    except Exception as e:
        print(e)
        pass
    
    
if platform == 'win32':
    #ani = matplotlib.animation.FuncAnimation(fig, refresh_sky, repeat=False, interval=45000, save_count=0)
    ani = matplotlib.animation.FuncAnimation(fig, refresh_refresh_sky, repeat=False, interval=10000, save_count=0)
else:
    while True:
        i = ""
        refresh_refresh_sky(i)
        time.sleep(60)

timelog('backend is '+str(matplotlib.get_backend()))

# plt.get_current_fig_manager().window.wm_geometry('-5-25')

# plt.show()