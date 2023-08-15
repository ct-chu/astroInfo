import time
start = time.time()

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import collections as mc
#import pylab as pl
import pandas
import numpy
import math
import ephem
from datetime import date, datetime
import tkinter as tk
from tkinter import *
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pathlib
from PIL import Image
import itertools
from sys import platform

######################
# initial parameters #
######################
root = tk.Tk()
##root.wm_title('All Sky Image Monitor v.'\
##              +str(date.today().year)\
##              +str(f'{date.today().month:02d}')\
##              +str(f'{date.today().day:02d}'))
root.wm_title('All Sky Image Monitor v.20181207')
root.config(bg='black')
root.iconbitmap(pathlib.Path.cwd().joinpath('ASC','hokoon.ico'))
root.geometry('1350x920+0+0')
   
# observatory
hokoon = ephem.Observer()
hokoon.lon = '114.108008'
hokoon.lat = '22.383678'
hokoon.date = datetime.utcnow()
#hokoon.date = '2018/10/29 00:00:00'
### turnoff atmospheric refraction
##hokoon.pressure = 0
##hokoon.horizon = '-0:34'

# plot parameters
image_size = 1.6
##fig = plt.figure(figsize=(image_size*7.2,image_size*4.8), facecolor='black')
##ax0 = fig.add_subplot(1,1,1)
fig, ax0 = plt.subplots(figsize=(1,1), facecolor='black')
fig.subplots_adjust(0,0,1,1)
ax0.set_facecolor('black')
ax0.set_aspect('equal')
ax0.set_xlim((-360,360))
ax0.set_ylim((-240,240))
ax_label = ax0.twiny()
ax_label.set_position(ax0.get_position())
ax_label.set_facecolor(ax0.get_facecolor())
ax_label.set_aspect(ax0.get_aspect())
ax_label.set_xlim(ax0.get_xlim())
ax_label.set_ylim(ax0.get_ylim())
ax_cursor = ax0.twiny()
#plt.axis('off')

plot_para = [0] * 7
plot_para = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','plot_para.csv'),\
                            header=None, index_col=None)
#-1.0, -1.5, -3.0, 0.92, 174.0, -12.0, 6.0
#-3.0, -1.5, -1.5, 0.94, 174.0, -11.5, 6.0
#-2.0, -1.5, -2.0, 0.90, 182.0, -11.5, 6.0
zenith_shift_ra = tk.DoubleVar()
zenith_shift_ra.set(round(float(plot_para.loc[0]),1))
zenith_shift_dec = tk.DoubleVar()
zenith_shift_dec.set(round(float(plot_para.loc[1]),1))
rotate_angle = tk.DoubleVar()
rotate_angle.set(round(float(plot_para.loc[2]),1))
aspect_ratio = tk.DoubleVar()
aspect_ratio.set(round(float(plot_para.loc[3]),2)) #y/x
plot_scale = tk.DoubleVar()
plot_scale.set(round(float(plot_para.loc[4]),1))
x_shift = tk.DoubleVar()
x_shift.set(round(float(plot_para.loc[5]),1))
y_shift = tk.DoubleVar()
y_shift.set(round(float(plot_para.loc[6]),1))

save_para = tk.StringVar()
save_para.set('save parameters')
sky_culture = tk.IntVar()
sky_culture.set(1)
star_on = tk.IntVar()
star_on.set(0)

DjV_S_12    = font.Font(family='DejaVu Sans', size=12)
DjV_S_12_   = font.Font(family='DejaVu Sans', size=12, underline=True)
DjV_S_12B   = font.Font(family='DejaVu Sans', size=12, weight='bold')
Arial_20B   = font.Font(family='Arial', size=20, weight='bold')
DjV_S_10    = font.Font(family='DejaVu Sans', size=10)
DjV_S_8     = font.Font(family='DejaVu Sans', size=8)
DjV_S_1     = font.Font(family='DejaVu Sans', size=1)
if platform == 'win32':
    TMN_10      = font.Font(family='Terminal', size=10)
else:
    TMN_10      = font.Font(family='Monaco', size=10)

# chinese charaters
if platform == 'win32':
    chara_chi = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/YUGOTHR.TTC')
else:
    chara_chi = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF')

# japanese charaters
if platform == 'win32':
    chara_jap = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/YUGOTHR.TTC')
else:
    chara_jap = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF')

# raw data
horizon     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
equator     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
ecliptic    = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)

Sun = ephem.Sun()
Sun.compute(hokoon)
Moon = ephem.Moon()
Moon.compute(hokoon)
Mercury = ephem.Mercury()
Mercury.compute(hokoon)
Venus = ephem.Venus()
Venus.compute(hokoon)
Mars = ephem.Mars()
Mars.compute(hokoon)
Jupiter = ephem.Jupiter()
Jupiter.compute(hokoon)
Io = ephem.Io()
Io.compute(hokoon)
Europa = ephem.Europa()
Europa.compute(hokoon)
Ganymede = ephem.Ganymede()
Ganymede.compute(hokoon)
Callisto = ephem.Callisto()
Callisto.compute(hokoon)
Saturn = ephem.Saturn()
Saturn.compute(hokoon)  
Uranus = ephem.Uranus()
Uranus.compute(hokoon)
Neptune = ephem.Neptune()
Neptune.compute(hokoon)
            
# make relative path (pathlib.Path.cwd() <=> current Dir)
print('importing star catalogue')
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
Mare = numpy.zeros(shape=(449593,5)) 
Mare = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_mare.csv'))
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
# radio sources
radio           = numpy.zeros(shape=(27,6))
radio           = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','radio.csv'))
# gamma ray
gamma_3FGL      = numpy.zeros(shape=(3034,7))
gamma_3FGL      = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','3FGL.csv'))

####################
# define functions #
####################

def plot_horizon():
    global plot_alpha, hori_border, hori_xmax, hori_xmin, hori_ymax, hori_ymin, horizon_line, equator_line, ecliptic_line

    # alpha
    if math.degrees(Sun.alt) >= 0:
        plot_alpha = 0.2
    else:
        plot_alpha = 0.1

    if button_mode.get() == 2:
        plot_alpha = plot_alpha + 0.25
        
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

    # equator
    equator['RA'] = numpy.arange(len(equator))

    equator.x = list(map(transform_x, equator.RA, equator.Dec))
    equator.y = list(map(transform_y, equator.RA, equator.Dec))

    equator_pt = []
    for i in range(len(equator)-1):
        if (equator['x'].tolist()[i]-x_shift.get())**2 < (hori_border/2)**2-((equator['y'].tolist()[i]-y_shift.get())/aspect_ratio.get())**2:
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
        if (ecliptic['x'].tolist()[i]-x_shift.get())**2 < (hori_border/2)**2-((ecliptic['y'].tolist()[i]-y_shift.get())/aspect_ratio.get())**2:
            ecliptic_pt.append([ecliptic['x'].tolist()[i],ecliptic['y'].tolist()[i]])
            
    ecliptic_line = plt.Polygon(sorted(ecliptic_pt), closed=False, fill=None, edgecolor=(1,1,0,plot_alpha), zorder=1+2.5)
    ax0.add_patch(ecliptic_line)   
        
def plot_solar():
    global solar_obj,solar_color,\
           Sun_x,Moon_x,Mercury_x,Venus_x,Mars_x,Jupiter_x,Saturn_x,Uranus_x,Neptune_x,\
           Sun_y,Moon_y,Mercury_y,Venus_y,Mars_y,Jupiter_y,Saturn_y,Uranus_y,Neptune_y
    
    print('plotting solar system objects')
    prompt_text('plotting solar system objects')
    fm_bottom.update()
    
    Sun = ephem.Sun()
    Sun.compute(hokoon)
    Moon = ephem.Moon()
    Moon.compute(hokoon)
    Mercury = ephem.Mercury()
    Mercury.compute(hokoon)
    Venus = ephem.Venus()
    Venus.compute(hokoon)
    Mars = ephem.Mars()
    Mars.compute(hokoon)
    Jupiter = ephem.Jupiter()
    Jupiter.compute(hokoon)
    Saturn = ephem.Saturn()
    Saturn.compute(hokoon)  
    Uranus = ephem.Uranus()
    Uranus.compute(hokoon)
    Neptune = ephem.Neptune()
    Neptune.compute(hokoon)
    
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

def solar_label():
    ax_label.annotate('$\u263C$',(Sun_x+2.5,Sun_y+1),color=solar_color[0])
    if moon_chi>180:
        ax_label.annotate('$\u263D$',(Moon_x+2.5,Moon_y+1),color=solar_color[1])
    else:
        ax_label.annotate('$\u263E$',(Moon_x+2.5,Moon_y+1),color=solar_color[1])
    ax_label.annotate('$\u263F$',(Mercury_x+2.5,Mercury_y+1),color=solar_color[2])
    ax_label.annotate('$\u2640$',(Venus_x+2.5,Venus_y+1),color=solar_color[3])
    ax_label.annotate('$\u2642$',(Mars_x+2.5,Mars_y+1),color=solar_color[4])
    ax_label.annotate('$\u2643$',(Jupiter_x+2.5,Jupiter_y+1),color=solar_color[5])
    ax_label.annotate('$\u2644$',(Saturn_x+2.5,Saturn_y+1),color=solar_color[6])
    ax_label.annotate('$\u2645$',(Uranus_x+2.5,Uranus_y+1),color=solar_color[7])
    ax_label.annotate('$\u2646$',(Neptune_x+2.5,Neptune_y+1),color=solar_color[8])

def transform_stars():
    global constellation_list
    
    print('calculating')
    prompt_text('doing Maths')
    fm_bottom.update()
    
    constellation_list = [And,Ant,Aps,Aqr,Aql,Ara,Ari,Aur,Boo,Cae,Cam,Cnc,CVn,CMa,CMi,Cap,Car,Cas,Cen,Cep,\
                          Cet,Cha,Cir,Col,Com,CrA,CrB,Crv,Crt,Cru,Cyg,Del,Dor,Dra,Equ,Eri,For,Gem,Gru,Her,\
                          Hor,Hya,Hyi,Ind,Lac,Leo,LMi,Lep,Lib,Lup,Lyn,Lyr,Men,Mic,Mon,Mus,Nor,Oct,Oph,Ori,\
                          Pav,Peg,Per,Phe,Pic,Psc,PsA,Pup,Pyx,Ret,Sge,Sgr,Sco,Scl,Sct,Ser,Sex,Tau,Tel,Tri,\
                          TrA,Tuc,UMa,UMi,Vel,Vir,Vol,Vul,radio,gamma_3FGL]
    
    for df in constellation_list:
        df.x = list(map(transform_x, df.RA, df.Dec))
        df.y = list(map(transform_y, df.RA, df.Dec))

def plot_stars():
    global manystars, mag_lim

    print('putting stars on sky')
    prompt_text('putting stars on sky')
    fm_bottom.update()
    
    constellation_star = [[And.x,And.y,And.mag],[Ant.x,Ant.y,Ant.mag],[Aps.x,Aps.y,Aps.mag],[Aqr.x,Aqr.y,Aqr.mag],\
                          [Aql.x,Aql.y,Aql.mag],[Ara.x,Ara.y,Ara.mag],[Ari.x,Ari.y,Ari.mag],[Aur.x,Aur.y,Aur.mag],\
                          [Boo.x,Boo.y,Boo.mag],[Cae.x,Cae.y,Cae.mag],[Cam.x,Cam.y,Cam.mag],[Cnc.x,Cnc.y,Cnc.mag],\
                          [CVn.x,CVn.y,CVn.mag],[CMa.x,CMa.y,CMa.mag],[CMi.x,CMi.y,CMi.mag],[Cap.x,Cap.y,Cap.mag],\
                          [Car.x,Car.y,Car.mag],[Cas.x,Cas.y,Cas.mag],[Cen.x,Cen.y,Cen.mag],[Cep.x,Cep.y,Cep.mag],\
                          [Cet.x,Cet.y,Cet.mag],[Cha.x,Cha.y,Cha.mag],[Cir.x,Cir.y,Cir.mag],[Col.x,Col.y,Col.mag],\
                          [Com.x,Com.y,Com.mag],[CrA.x,CrA.y,CrA.mag],[CrB.x,CrB.y,CrB.mag],[Crv.x,Crv.y,Crv.mag],\
                          [Crt.x,Crt.y,Crt.mag],[Cru.x,Cru.y,Cru.mag],[Cyg.x,Cyg.y,Cyg.mag],[Del.x,Del.y,Del.mag],\
                          [Dor.x,Dor.y,Dor.mag],[Dra.x,Dra.y,Dra.mag],[Equ.x,Equ.y,Equ.mag],[Eri.x,Eri.y,Eri.mag],\
                          [For.x,For.y,For.mag],[Gem.x,Gem.y,Gem.mag],[Gru.x,Gru.y,Gru.mag],[Her.x,Her.y,Her.mag],\
                          [Hor.x,Hor.y,Hor.mag],[Hya.x,Hya.y,Hya.mag],[Hyi.x,Hyi.y,Hyi.mag],[Ind.x,Ind.y,Ind.mag],\
                          [Lac.x,Lac.y,Lac.mag],[Leo.x,Leo.y,Leo.mag],[LMi.x,LMi.y,LMi.mag],[Lep.x,Lep.y,Lep.mag],\
                          [Lib.x,Lib.y,Lib.mag],[Lup.x,Lup.y,Lup.mag],[Lyn.x,Lyn.y,Lyn.mag],[Lyr.x,Lyr.y,Lyr.mag],\
                          [Men.x,Men.y,Men.mag],[Mic.x,Mic.y,Mic.mag],[Mon.x,Mon.y,Mon.mag],[Mus.x,Mus.y,Mus.mag],\
                          [Nor.x,Nor.y,Nor.mag],[Oct.x,Oct.y,Oct.mag],[Oph.x,Oph.y,Oph.mag],[Ori.x,Ori.y,Ori.mag],\
                          [Pav.x,Pav.y,Pav.mag],[Peg.x,Peg.y,Peg.mag],[Per.x,Per.y,Per.mag],[Phe.x,Phe.y,Phe.mag],\
                          [Pic.x,Pic.y,Pic.mag],[Psc.x,Psc.y,Psc.mag],[PsA.x,PsA.y,PsA.mag],[Pup.x,Pup.y,Pup.mag],\
                          [Pyx.x,Pyx.y,Pyx.mag],[Ret.x,Ret.y,Ret.mag],[Sge.x,Sge.y,Sge.mag],[Sgr.x,Sgr.y,Sgr.mag],\
                          [Sco.x,Sco.y,Sco.mag],[Scl.x,Scl.y,Scl.mag],[Sct.x,Sct.y,Sct.mag],[Ser.x,Ser.y,Ser.mag],\
                          [Sex.x,Sex.y,Sex.mag],[Tau.x,Tau.y,Tau.mag],[Tel.x,Tel.y,Tel.mag],[Tri.x,Tri.y,Tri.mag],\
                          [TrA.x,TrA.y,TrA.mag],[Tuc.x,Tuc.y,Tuc.mag],[UMa.x,UMa.y,UMa.mag],[UMi.x,UMi.y,UMi.mag],\
                          [Vel.x,Vel.y,Vel.mag],[Vir.x,Vir.y,Vir.mag],[Vol.x,Vol.y,Vol.mag],[Vul.x,Vul.y,Vul.mag]]

    stars_x = []
    stars_y = []
    stars_m = []
    mag_lim = 7
    for x,y,z in constellation_star:
        for j in range(len(x)):
            if (x[j]-x_shift.get())**2 < (hori_border/2)**2-((y[j]-y_shift.get())/aspect_ratio.get())**2:
                if z[j] <= mag_lim:
                    stars_x.append(x[j])
                    stars_y.append(y[j])
                    stars_m.append(5*(10**(-0.4*z[j]))**0.5)

    if star_on.get() == 1: # optical
        manystars = ax0.scatter(stars_x,stars_y, stars_m, c='white', alpha=plot_alpha, zorder=3+2.5)
    elif star_on.get() == 2: # radio
        manystars = ax0.scatter(radio.x,radio.y, 10*numpy.log(radio.Jy), c='white', zorder=3+2.5)
        for i in range(len(radio)):
            ax_label.annotate(str(radio.ID[i]),(radio.x[i],radio.y[i]-labelxy),color='w',horizontalalignment='center',verticalalignment='top')
    elif star_on.get() == 3: # gamma 3FGL
        manystars = ax0.scatter(gamma_3FGL.x,gamma_3FGL.y, numpy.log10(gamma_3FGL.Flux_Density)+14, c='white', zorder=3+2.5)
        
def plot_constellation():
    global lc_west, lc_west_z, lc_west_dotted, labelxy,\
           lc_C_A, lc_C_B, lc_C_C, lc_C_D, lc_C_D_z, lc_C_E, lc_C_E_z, lc_C_F, lc_C_F_z, lc_C_G, lc_C_G_z, lc_C_H, \
           lc_J_A, lc_J_B, lc_J_C, lc_J_D, lc_J_D_z, lc_J_E, lc_J_E_z, lc_J_F, lc_J_F_z, lc_J_G, lc_J_G_z, lc_J_H

    labelxy = 2
    
    print('drawing constellations')
    prompt_text('drawing constellations')
    fm_bottom.update()
    
    if sky_culture.get() == 0:
        # western constellations
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
                              constellation_line[i][1][constellation_line[i][2][j][0]]-constellation_line[i][1][constellation_line[i][2][j][1]]) < hori_border:
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
        constellation_dotted_line_list = [[(Aur.x[3],Aur.y[3]),(Tau.x[1],Tau.y[1])],[(Aur.x[2],Aur.y[2]),(Tau.x[1],Tau.y[1])],\
                                          [(Peg.x[1],Peg.y[1]),(And.x[0],And.y[0])],[(Peg.x[3],Peg.y[3]),(And.x[0],And.y[0])],\
                                          [(Ser.x[3],Ser.y[3]),(Oph.x[7],Oph.y[7])],[(Ser.x[2],Ser.y[2]),(Oph.x[3],Oph.y[3])],\
                                          [(PsA.x[0],PsA.y[0]),(Aqr.x[18],Aqr.y[18])]]
                
        lc_west_dotted = mc.LineCollection(constellation_dotted_line_list, colors='white', linestyles='dashed',zorder=10+2.5)
        lc_west_dotted.set_alpha(plot_alpha)
        ax0.add_collection(lc_west_dotted)

        # annotation
        for x,y,z,n in constellation_line:
            if math.hypot(numpy.mean(x)-x_shift.get(),numpy.mean(y)-y_shift.get()) \
               < math.sqrt(((hori_border/2)**2)-(1-aspect_ratio.get()**2)*((numpy.mean(y)-y_shift.get())/aspect_ratio.get())**2) \
               and max(x)-min(x) < hori_border:
                if n in set(['$\u2652$','$\u2648$','$\u264B$','$\u2651$','$\u264A$','$\u264C$','$\u264E$','$\u2653$','$\u2650$','$\u264F$','$\u2649$','$\u264D$']):
                    ax_label.annotate(str(n),(numpy.mean(x),numpy.mean(y)-labelxy),color='y')
                elif button_mode.get() == 2:
                    ax_label.annotate(str(n),(numpy.mean(x),numpy.mean(y)-labelxy),color='w')

    elif sky_culture.get() == 1:
        # chinese constellations
        
        ########
        #紫微垣#
        ########
        #北極#
        C_A01 = [[UMi.x[1],UMi.x[2]],[UMi.y[1],UMi.y[2]],[UMi.x[1],UMi.x[4]],[UMi.y[1],UMi.y[4]],\
                 [UMi.x[4],UMi.x[8]],[UMi.y[4],UMi.y[8]],[UMi.x[8],Cam.x[29]],[UMi.y[8],Cam.y[29]]]
        CA01n = [numpy.mean([UMi.x[2],UMi.x[4],UMi.x[8],Cam.x[29]]),\
                 numpy.mean([UMi.y[2],UMi.y[4],UMi.y[8],Cam.y[29]])]
        #四輔#
        C_A02 = [[Cam.x[26],Cam.x[43]],[Cam.y[26],Cam.y[43]]]
        CA02n = [numpy.mean([Cam.x[26],Cam.x[43]]),\
                 numpy.mean([Cam.y[26],Cam.y[43]])-labelxy]
        #天乙#
        C_A03 = []
        CA03n = [Dra.x[19],Dra.y[19]-labelxy]
        #太乙#
        C_A04 = []
        CA04n = [Dra.x[101]+labelxy,Dra.y[101]-labelxy]
        #紫微左垣#
        C_A05 = [[Cas.x[44],Cep.x[14]],[Cas.y[44],Cep.y[14]],[Cep.x[14],Dra.x[50]],[Cep.y[14],Dra.y[50]],\
                 [Dra.x[1],Dra.x[4]],[Dra.y[1],Dra.y[4]],[Dra.x[1],Dra.x[12]],[Dra.y[1],Dra.y[12]],\
                 [Dra.x[4],Dra.x[25]],[Dra.y[4],Dra.y[25]],[Dra.x[5],Dra.x[12]],[Dra.y[5],Dra.y[12]],\
                 [Dra.x[25],Dra.x[50]],[Dra.y[25],Dra.y[50]]]
        CA05n = [numpy.mean([Cep.x[14],Dra.x[50]]),\
                 numpy.mean([Cep.y[14],Dra.y[50]])]
        #紫微右垣#
        C_A06 = [[Cam.x[2],Cam.x[10]],[Cam.y[2],Cam.y[10]],[Cam.x[2],Cam.x[20]],[Cam.y[2],Cam.y[20]],\
                 [Cam.x[20],UMa.x[23]],[Cam.y[20],UMa.y[23]],[Dra.x[7],Dra.x[11]],[Dra.y[7],Dra.y[11]],\
                 [Dra.x[10],Dra.x[11]],[Dra.y[10],Dra.y[11]],[Dra.x[10],UMa.x[23]],[Dra.y[10],UMa.y[23]]]
        CA06n = [numpy.mean([Cam.x[20],Dra.x[10],UMa.x[23]]),\
                 numpy.mean([Cam.y[20],Dra.y[10],UMa.y[23]])]
        #陰德#
        C_A07 = []
        CA07n = [Dra.x[27],Dra.y[27]-labelxy]
        #尚書#
        C_A08= [[Dra.x[26],Dra.x[43]],[Dra.y[26],Dra.y[43]],[Dra.x[31],Dra.x[43]],[Dra.y[31],Dra.y[43]],\
                 [Dra.x[38],Dra.x[43]],[Dra.y[38],Dra.y[43]]]
        CA08n = [numpy.mean([Dra.x[26],Dra.x[31],Dra.x[38],Dra.x[43]])+labelxy,\
                 numpy.mean([Dra.y[26],Dra.y[31],Dra.y[38],Dra.y[43]])]
        #女史#
        C_A09 = []
        CA09n = [Dra.x[17],Dra.y[17]-labelxy]
        #柱史#
        C_A10 = []
        CA10n = [Dra.x[13],Dra.y[13]-labelxy]
        #御女#
        C_A11 = [[Dra.x[6],Dra.x[15]],[Dra.y[6],Dra.y[15]],[Dra.x[15],Dra.x[59]],[Dra.y[15],Dra.y[59]]]
        CA11n = [numpy.mean([Dra.x[6],Dra.x[15],Dra.x[59]])+labelxy,\
                 numpy.mean([Dra.y[6],Dra.y[15],Dra.y[59]])]
        #天柱#
        C_A12 = [[Cep.x[84],Dra.x[92]],[Cep.y[84],Dra.y[92]],[Cep.x[84],Dra.x[146]],[Cep.y[84],Dra.y[146]],\
                 [Dra.x[47],Dra.x[126]],[Dra.y[47],Dra.y[126]],[Dra.x[47],Dra.x[146]],[Dra.y[47],Dra.y[146]]]
        CA12n = [numpy.mean([Cep.x[84],Dra.x[47],Dra.x[126],Dra.x[146]]),\
                 numpy.mean([Cep.y[84],Dra.y[47],Dra.y[126],Dra.y[146]])]
        #大理#
        C_A13 = []
        CA13n = [Cam.x[22],Cam.y[22]-labelxy]
        #勾陳#
        C_A14 = [[Cep.x[10],Cep.x[17]],[Cep.y[10],Cep.y[17]],[Cep.x[10],UMi.x[0]],[Cep.y[10],UMi.y[0]],\
                 [UMi.x[0],UMi.x[6]],[UMi.y[0],UMi.y[6]],[UMi.x[3],UMi.x[5]],[UMi.y[3],UMi.y[5]],\
                 [UMi.x[3],UMi.x[6]],[UMi.y[3],UMi.y[6]]]
        CA14n = [numpy.mean([Cep.x[10],Cep.x[17],UMi.x[0],UMi.x[3],UMi.x[5],UMi.x[6]]),\
                 numpy.mean([Cep.y[10],Cep.y[17],UMi.y[0],UMi.y[3],UMi.y[5],UMi.y[6]])-labelxy]
        #六甲#
        C_A15 = [[Cam.x[6],Cam.x[42]],[Cam.y[6],Cam.y[42]],[Cam.x[11],Cam.x[42]],[Cam.y[11],Cam.y[42]],\
                 [Cam.x[11],Cep.x[26]],[Cam.y[11],Cep.y[26]],[Cam.x[15],Cep.x[26]],[Cam.y[15],Cep.y[26]]]
        CA15n = [numpy.mean([Cam.x[6],Cam.x[11],Cam.x[15],Cam.x[42],Cep.x[26]]),\
                 numpy.mean([Cam.y[6],Cam.y[11],Cam.y[15],Cam.y[42],Cep.y[26]])+labelxy]
        #天皇大帝#
        C_A16 = []
        CA16n = [Cep.x[37],Cep.y[37]-labelxy]
        #五帝內座#
        C_A17 = [[Cas.x[41],Cep.x[46]],[Cas.y[41],Cep.y[46]],[Cep.x[29],Cep.x[46]],[Cep.y[29],Cep.y[46]],\
                 [Cep.x[42],Cep.x[46]],[Cep.y[42],Cep.y[46]],[Cep.x[46],Cep.x[69]],[Cep.y[46],Cep.y[69]]]
        CA17n = [numpy.mean([Cas.x[41],Cep.x[29],Cep.x[42],Cep.x[46],Cep.x[69]]),\
                 numpy.mean([Cas.y[41],Cep.y[29],Cep.y[42],Cep.y[46],Cep.y[69]])-labelxy]
        #華蓋#
        C_A18 = [[Cas.x[17],Cas.x[40]],[Cas.y[17],Cas.y[40]],[Cas.x[17],Cas.x[61]],[Cas.y[17],Cas.y[61]],\
                 [Cas.x[31],Cas.x[61]],[Cas.y[31],Cas.y[61]],[Cas.x[39],Cas.x[40]],[Cas.y[39],Cas.y[40]]]
        CA18n = [numpy.mean([Cas.x[17],Cas.x[31],Cas.x[39],Cas.x[40],Cas.x[61]]),\
                 numpy.mean([Cas.y[17],Cas.y[31],Cas.y[39],Cas.y[40],Cas.y[61]])]
        #杠#
        C_A19 = [[Cam.x[7],Cas.x[23]],[Cam.y[7],Cas.y[23]],[Cas.x[7],Cas.x[12]],[Cas.y[7],Cas.y[12]],\
                 [Cas.x[7],Cas.x[37]],[Cas.y[7],Cas.y[37]],[Cas.x[12],Cas.x[36]],[Cas.y[12],Cas.y[36]],\
                 [Cas.x[23],Cas.x[37]],[Cas.y[23],Cas.y[37]],[Cas.x[36],Cas.x[77]],[Cas.y[36],Cas.y[77]]]
        CA19n = [numpy.mean([Cam.x[7],Cas.x[7],Cas.x[12],Cas.x[23],Cas.x[36],Cas.x[37],Cas.x[77]]),\
                 numpy.mean([Cam.y[7],Cas.y[7],Cas.y[12],Cas.y[23],Cas.y[36],Cas.y[37],Cas.y[77]])]
        #傳舍#
        C_A20 = [[Cam.x[1],Cam.x[5]],[Cam.y[1],Cam.y[5]],[Cam.x[1],Cas.x[62]],[Cam.y[1],Cas.y[62]],\
                 [Cam.x[5],Cam.x[18]],[Cam.y[5],Cam.y[18]],[Cas.x[58],Cas.x[96]],[Cas.y[58],Cas.y[96]],\
                 [Cas.x[58],Cep.x[25]],[Cas.y[58],Cep.y[25]],[Cas.x[62],Cas.x[96]],[Cas.y[62],Cas.y[96]]]
        CA20n = [numpy.mean([Cam.x[1],Cam.x[5],Cam.x[18],Cas.x[58],Cas.x[62],Cas.x[96],Cep.x[25]]),\
                 numpy.mean([Cam.y[1],Cam.y[5],Cam.y[18],Cas.y[58],Cas.y[62],Cas.y[96],Cep.y[25]])]
        #內階#
        C_A21 = [[UMa.x[11],UMa.x[46]],[UMa.y[11],UMa.y[46]],[UMa.x[15],UMa.x[88]],[UMa.y[15],UMa.y[88]],\
                 [UMa.x[46],UMa.x[71]],[UMa.y[46],UMa.y[71]],[UMa.x[53],UMa.x[88]],[UMa.y[53],UMa.y[88]]]
        CA21n = [numpy.mean([UMa.x[11],UMa.x[15],UMa.x[46],UMa.x[53],UMa.x[71],UMa.x[88]]),\
                 numpy.mean([UMa.y[11],UMa.y[15],UMa.y[46],UMa.y[53],UMa.y[71],UMa.y[88]])-labelxy]
        #天廚#
        C_A22 = [[Dra.x[3],Dra.x[21]],[Dra.y[3],Dra.y[21]],[Dra.x[9],Dra.x[16]],[Dra.y[9],Dra.y[16]],\
                 [Dra.x[9],Dra.x[21]],[Dra.y[9],Dra.y[21]],[Dra.x[16],Dra.x[55]],[Dra.y[16],Dra.y[55]],\
                 [Dra.x[18],Dra.x[55]],[Dra.y[18],Dra.y[55]]]
        CA22n = [numpy.mean([Dra.x[3],Dra.x[9],Dra.x[16],Dra.x[18],Dra.x[21],Dra.x[55]]),\
                 numpy.mean([Dra.y[3],Dra.y[9],Dra.y[16],Dra.y[18],Dra.y[21],Dra.y[55]])]
        #八穀#
        C_A23 = [[Aur.x[6],Cam.x[69]],[Aur.y[6],Cam.y[69]],[Cam.x[4],Cam.x[69]],[Cam.y[4],Cam.y[69]],\
                 [Cam.x[17],Cam.x[24]],[Cam.y[17],Cam.y[24]]]
        CA23n = [numpy.mean([Aur.x[6],Cam.x[4],Cam.x[17],Cam.x[24],Cam.x[69]]),\
                 numpy.mean([Aur.y[6],Cam.y[4],Cam.y[17],Cam.y[24],Cam.y[69]])]
        #天棓#
        C_A24 = [[Dra.x[0],Dra.x[2]],[Dra.y[0],Dra.y[2]],[Dra.x[0],Her.x[9]],[Dra.y[0],Her.y[9]],\
                 [Dra.x[2],Dra.x[30]],[Dra.y[2],Dra.y[30]],[Dra.x[8],Dra.x[30]],[Dra.y[8],Dra.y[30]]]
        CA24n = [numpy.mean([Dra.x[0],Dra.x[2],Dra.x[8],Dra.x[30]]),\
                 numpy.mean([Dra.y[0],Dra.y[2],Dra.y[8],Dra.y[30]])]
        #內廚#
        C_A25 = [[Dra.x[52],Dra.x[67]],[Dra.y[52],Dra.y[67]]]
        CA25n = [numpy.mean([Dra.x[52],Dra.x[67]]),\
                 numpy.mean([Dra.y[52],Dra.y[67]])-labelxy]
        #文昌#
        C_A26 = [[UMa.x[9],UMa.x[21]],[UMa.y[9],UMa.y[21]],[UMa.x[9],UMa.x[24]],[UMa.y[9],UMa.y[24]],\
                 [UMa.x[17],UMa.x[24]],[UMa.y[17],UMa.y[24]],[UMa.x[21],UMa.x[33]],[UMa.y[21],UMa.y[33]]]
        CA26n = [numpy.mean([UMa.x[9],UMa.x[17],UMa.x[21],UMa.x[24],UMa.x[33]]),\
                 numpy.mean([UMa.y[9],UMa.y[17],UMa.y[21],UMa.y[24],UMa.y[33]])]
        #三師#
        C_A27 = [[UMa.x[30],UMa.x[47]],[UMa.y[30],UMa.y[47]]]
        CA27n = [numpy.mean([UMa.x[30],UMa.x[47]]),\
                 numpy.mean([UMa.y[30],UMa.y[47]])-labelxy]
        #三公#
        C_A28 = [[CVn.x[2],CVn.x[11]],[CVn.y[2],CVn.y[11]]]
        CA28n = [numpy.mean([CVn.x[2],CVn.x[11]]),\
                 numpy.mean([CVn.y[2],CVn.y[11]])-labelxy]
        #天床#
        C_A29 = [[Dra.x[48],UMi.x[7]],[Dra.y[48],UMi.y[7]],[Dra.x[48],UMi.x[12]],[Dra.y[48],UMi.y[12]],\
                 [UMi.x[12],UMi.x[13]],[UMi.y[12],UMi.y[13]]]
        CA29n = [numpy.mean([UMi.x[7],UMi.x[12],UMi.x[13]]),\
                 numpy.mean([UMi.y[7],UMi.y[12],UMi.y[13]])]
        #太尊#
        C_A30 = []
        CA30n = [UMa.x[6],UMa.y[6]-labelxy]
        #天牢#
        C_A31 = [[UMa.x[28],UMa.x[56]],[UMa.y[28],UMa.y[56]],[UMa.x[38],UMa.x[42]],[UMa.y[38],UMa.y[42]],\
                 [UMa.x[41],UMa.x[113]],[UMa.y[41],UMa.y[113]]]
        CA31n = [numpy.mean([UMa.x[28],UMa.x[38],UMa.x[41],UMa.x[42],UMa.x[56],UMa.x[113]]),\
                 numpy.mean([UMa.y[28],UMa.y[38],UMa.y[41],UMa.y[42],UMa.y[56],UMa.y[113]])-labelxy]
        #太陽守#
        C_A32 = []
        CA32n = [UMa.x[16],UMa.y[16]-labelxy]
        #勢#
        C_A33 = [[LMi.x[0],LMi.x[8]],[LMi.y[0],LMi.y[8]],[LMi.x[8],LMi.x[21]],[LMi.y[8],LMi.y[21]],\
                 [LMi.x[15],LMi.x[21]],[LMi.y[15],LMi.y[21]]]
        CA33n = [numpy.mean([LMi.x[0],LMi.x[8],LMi.x[15],LMi.x[21]]),\
                 numpy.mean([LMi.y[0],LMi.y[8],LMi.y[15],LMi.y[21]])]
        #相#
        C_A34 = []
        CA34n = [CVn.x[5],CVn.y[5]-labelxy]
        #玄戈#
        C_A35 = []
        CA35n = [Boo.x[9],Boo.y[9]-labelxy]
        #玄戈#
        C_A36 = []
        CA36n = [UMa.x[103],UMa.y[103]-labelxy]
        #北斗#
        C_A37 = [[UMa.x[0],UMa.x[3]],[UMa.y[0],UMa.y[3]],[UMa.x[0],UMa.x[10]],[UMa.y[0],UMa.y[10]],\
                 [UMa.x[1],UMa.x[4]],[UMa.y[1],UMa.y[4]],[UMa.x[2],UMa.x[3]],[UMa.y[2],UMa.y[3]],\
                 [UMa.x[4],UMa.x[5]],[UMa.y[4],UMa.y[5]],[UMa.x[5],UMa.x[10]],[UMa.y[5],UMa.y[10]]]
        CA37n = [numpy.mean([UMa.x[0],UMa.x[1],UMa.x[4],UMa.x[5],UMa.x[10]]),\
                 numpy.mean([UMa.y[0],UMa.y[1],UMa.y[4],UMa.y[5],UMa.y[10]])]
        #輔#
        C_A38 = []
        CA38n = [UMa.x[19]+labelxy,UMa.y[19]-labelxy]
        #天槍#
        C_A39 = [[Boo.x[7],Boo.x[18]],[Boo.y[7],Boo.y[18]],[Boo.x[14],Boo.x[18]],[Boo.y[14],Boo.y[18]]]
        CA39n = [numpy.mean([Boo.x[7],Boo.x[14],Boo.x[18]]),\
                 numpy.mean([Boo.y[7],Boo.y[14],Boo.y[18]])-labelxy]
        
        C_A_list = [C_A01,C_A02,C_A03,C_A04,C_A05,C_A06,C_A07,C_A08,C_A09,C_A10,\
                    C_A11,C_A12,C_A13,C_A14,C_A15,C_A16,C_A17,C_A18,C_A19,C_A20,\
                    C_A21,C_A22,C_A23,C_A24,C_A25,C_A26,C_A27,C_A28,C_A29,C_A30,\
                    C_A31,C_A32,C_A33,C_A34,C_A35,C_A36,C_A37,C_A38,C_A39]

        # 紫微垣 linecollection
        C_A_line_xy1 = []
        C_A_line_xy2 = []        
        for i in range(len(C_A_list)):
            for j in range(len(C_A_list[i]))[0::2]:
                if math.hypot(C_A_list[i][j][0]-C_A_list[i][j][1],C_A_list[i][j+1][0]-C_A_list[i][j+1][1]) < hori_border:
                    C_A_line_xy1.append((C_A_list[i][j][0],C_A_list[i][j+1][0]))
                    C_A_line_xy2.append((C_A_list[i][j][1],C_A_list[i][j+1][1]))

        C_A_line_list = []
        for i in range(len(C_A_line_xy1)):            
            C_A_line_list.append([C_A_line_xy1[i],C_A_line_xy2[i]])
        
        lc_C_A = mc.LineCollection(C_A_line_list, colors='white', zorder=2+2.5)
        lc_C_A.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_A)

        CAn_list = [[CA01n,'北極'],[CA02n,'四輔'],[CA03n,'天乙'],[CA04n,'太乙'],[CA05n,'紫微左垣'],\
                    [CA06n,'紫微右垣'],[CA07n,'陰德'],[CA08n,'尚書'],[CA09n,'女史'],[CA10n,'柱史'],\
                    [CA11n,'御女'],[CA12n,'天柱'],[CA13n,'大理'],[CA14n,'勾陳'],[CA15n,'六甲'],\
                    [CA16n,'天皇大帝'],[CA17n,'五帝內座'],[CA18n,'華蓋'],[CA19n,'杠'],[CA20n,'傳舍'],\
                    [CA21n,'內階'],[CA22n,'天廚'],[CA23n,'八穀'],[CA24n,'天棓'],[CA25n,'內廚'],\
                    [CA26n,'文昌'],[CA27n,'三師'],[CA28n,'三公'],[CA29n,'天床'],[CA30n,'太尊'],\
                    [CA31n,'天牢'],[CA32n,'太陽守'],[CA33n,'勢'],[CA34n,'相'],[CA35n,'玄戈'],\
                    [CA36n,'玄戈'],[CA37n,'北斗'],[CA38n,'輔'],[CA39n,'天槍']]
      
        for i in range(len(CAn_list)):
            if len(CAn_list[i][0]) != 0:
                if (CAn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CAn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CAn_list[i][0])-min(CAn_list[i][0]) < hori_border:
                    ax_label.annotate(str(CAn_list[i][1]),(CAn_list[i][0][0],CAn_list[i][0][1]),color='w',\
                                      fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ########
        #太微垣#
        ########
        #太微左垣#
        C_B01 = [[Com.x[19],Vir.x[1]],[Com.y[19],Vir.y[1]],[Vir.x[1],Vir.x[3]],[Vir.y[1],Vir.y[3]],\
                 [Vir.x[3],Vir.x[5]],[Vir.y[3],Vir.y[5]],[Vir.x[5],Vir.x[9]],[Vir.y[5],Vir.y[9]]]
        CB01n = [numpy.mean([Vir.x[1],Vir.x[3],Vir.x[5],Vir.x[9]]),\
                 numpy.mean([Vir.y[1],Vir.y[3],Vir.y[5],Vir.y[9]])]
        #太微右垣#
        C_B02 = [[Leo.x[2],Leo.x[5]],[Leo.y[2],Leo.y[5]],[Leo.x[5],Leo.x[12]],[Leo.y[5],Leo.y[12]],\
                 [Leo.x[12],Leo.x[13]],[Leo.y[12],Leo.y[13]],[Leo.x[13],Vir.x[4]],[Leo.y[13],Vir.y[4]]]
        CB02n = [numpy.mean([Leo.x[2],Leo.x[5],Leo.x[12],Leo.x[13],Vir.x[4]]),\
                 numpy.mean([Leo.y[2],Leo.y[5],Leo.y[12],Leo.y[13],Vir.y[4]])-labelxy]
        #謁者#
        C_B03 = []
        CB03n = [Vir.x[30],Vir.y[30]-labelxy]
        #三公#
        C_B04 = []
        CB04n = [Vir.x[64],Vir.y[64]-labelxy]
        #九卿#
        C_B05 = [[Vir.x[27],Vir.x[41]],[Vir.y[27],Vir.y[41]]]
        CB05n = [numpy.mean([Vir.x[27],Vir.x[41]])+labelxy,\
                 numpy.mean([Vir.y[27],Vir.y[41]])]
        #五諸侯#
        C_B06 = [[Com.x[3],Com.x[16]],[Com.y[3],Com.y[16]],[Com.x[3],Com.x[38]],[Com.y[3],Com.y[38]],\
                 [Com.x[15],Com.x[16]],[Com.y[15],Com.y[16]]]
        CB06n = [numpy.mean([Com.x[3],Com.x[16],Com.x[38]])+2*labelxy,\
                 numpy.mean([Com.y[3],Com.y[16],Com.y[38]])+labelxy]
        #內屏#
        C_B07 = [[Vir.x[10],Vir.x[18]],[Vir.y[10],Vir.y[18]],[Vir.x[10],Vir.x[26]],[Vir.y[10],Vir.y[26]],\
                 [Vir.x[12],Vir.x[18]],[Vir.y[12],Vir.y[18]]]
        CB07n = [numpy.mean([Vir.x[10],Vir.x[12],Vir.x[18],Vir.x[26]]),\
                 numpy.mean([Vir.y[10],Vir.y[12],Vir.y[18],Vir.y[26]])+labelxy]
        #五帝座#
        C_B08 = [[Leo.x[1],Leo.x[52]],[Leo.y[1],Leo.y[52]],[Leo.x[1],Leo.x[87]],[Leo.y[1],Leo.y[87]]]
        CB08n = [numpy.mean([Leo.x[1],Leo.x[52],Leo.x[87]]),\
                 numpy.mean([Leo.y[1],Leo.y[52],Leo.y[87]])-2*labelxy]
        #幸臣#
        C_B09 = []
        CB09n = [] # ???
        #太子#
        C_B10 = []
        CB10n = [Leo.x[21],Leo.y[21]-labelxy]
        #從官#
        C_B11 = []
        CB11n = [Leo.x[37]+labelxy,Leo.y[37]-labelxy]
        #郎將#
        C_B12 = []
        CB12n = [Com.x[9],Com.y[9]-labelxy]
        #虎賁#
        C_B13 = []
        CB13n = [Leo.x[23],Leo.y[23]-labelxy]
        #常陳#
        C_B14 = [[CVn.x[0],CVn.x[31]],[CVn.y[0],CVn.y[31]],[CVn.x[1],CVn.x[10]],[CVn.y[1],CVn.y[10]],\
                 [CVn.x[1],CVn.x[31]],[CVn.y[1],CVn.y[31]],[CVn.x[10],CVn.x[20]],[CVn.y[10],CVn.y[20]],\
                 [CVn.x[20],UMa.x[52]],[CVn.y[20],UMa.y[52]]]
        CB14n = [numpy.mean([CVn.x[0],CVn.x[1],CVn.x[10],CVn.x[20],CVn.x[31]]),\
                 numpy.mean([CVn.y[0],CVn.y[1],CVn.y[10],CVn.y[20],CVn.y[31]])]
        #郎位#
        C_B15 = [[Com.x[1],Com.x[11]],[Com.y[1],Com.y[11]],[Com.x[5],Com.x[17]],[Com.y[5],Com.y[17]],\
                 [Com.x[5],Com.x[21]],[Com.y[5],Com.y[21]],[Com.x[6],Com.x[10]],[Com.y[6],Com.y[10]],\
                 [Com.x[6],Com.x[22]],[Com.y[6],Com.y[22]],[Com.x[10],Com.x[23]],[Com.y[10],Com.y[23]],\
                 [Com.x[11],Com.x[13]],[Com.y[11],Com.y[13]],[Com.x[13],Com.x[20]],[Com.y[13],Com.y[20]],\
                 [Com.x[17],Com.x[20]],[Com.y[17],Com.y[20]],[Com.x[21],Com.x[23]],[Com.y[21],Com.y[23]],\
                 [Com.x[22],Com.x[29]],[Com.y[22],Com.y[29]],[Com.x[25],Com.x[29]],[Com.y[25],Com.y[29]],\
                 [Com.x[25],Com.x[35]],[Com.y[25],Com.y[35]]]
        CB15n = [numpy.mean([Com.x[1],Com.x[5],Com.x[6],Com.x[10],Com.x[11],Com.x[13],Com.x[17],Com.x[20],\
                             Com.x[21],Com.x[22],Com.x[23],Com.x[25],Com.x[29],Com.x[35]])+labelxy,\
                 numpy.mean([Com.y[1],Com.y[5],Com.y[6],Com.y[10],Com.y[11],Com.y[13],Com.y[17],Com.y[20],\
                             Com.y[21],Com.y[22],Com.y[23],Com.y[25],Com.y[29],Com.y[35]])-2*labelxy]
        #明堂#
        C_B16 = [[Leo.x[14],Leo.x[26]],[Leo.y[14],Leo.y[26]],[Leo.x[14],Leo.x[29]],[Leo.y[14],Leo.y[29]]]
        CB16n = [numpy.mean([Leo.x[14],Leo.x[26],Leo.x[29]])+labelxy,\
                 numpy.mean([Leo.y[14],Leo.y[26],Leo.y[29]])]
        #靈台#
        C_B17 = [[Leo.x[22],Leo.x[31]],[Leo.y[22],Leo.y[31]],[Leo.x[28],Leo.x[31]],[Leo.y[28],Leo.y[31]]]
        CB17n = [numpy.mean([Leo.x[22],Leo.x[28],Leo.x[31]])-labelxy,\
                 numpy.mean([Leo.y[22],Leo.y[28],Leo.y[31]])]
        #少微#
        C_B18 = [[Leo.x[20],LMi.x[6]],[Leo.y[20],LMi.y[6]],[Leo.x[49],LMi.x[6]],[Leo.y[49],LMi.y[6]]]
        CB18n = [numpy.mean([Leo.x[20],Leo.x[49],LMi.x[6]])-labelxy,\
                 numpy.mean([Leo.y[20],Leo.y[49],LMi.y[6]])]
        #長垣#
        C_B19 = [[Leo.x[34],Leo.x[40]],[Leo.y[34],Leo.y[40]],[Leo.x[40],Leo.x[48]],[Leo.y[40],Leo.y[48]],\
                 [Leo.x[47],Leo.x[48]],[Leo.y[47],Leo.y[48]]]
        CB19n = [numpy.mean([Leo.x[34],Leo.x[40],Leo.x[47],Leo.x[48]]),\
                 numpy.mean([Leo.y[34],Leo.y[40],Leo.y[47],Leo.y[48]])]
        #三台#
        C_B20 = [[UMa.x[7],UMa.x[12]],[UMa.y[7],UMa.y[12]],[UMa.x[7],UMa.x[13]],[UMa.y[7],UMa.y[13]],\
                 [UMa.x[8],UMa.x[14]],[UMa.y[8],UMa.y[14]],[UMa.x[12],UMa.x[14]],[UMa.y[12],UMa.y[14]],\
                 [UMa.x[13],UMa.x[20]],[UMa.y[13],UMa.y[20]]]
        CB20n = [numpy.mean([UMa.x[7],UMa.x[8],UMa.x[12],UMa.x[13],UMa.x[14],UMa.x[20]])+labelxy,\
                 numpy.mean([UMa.y[7],UMa.y[8],UMa.y[12],UMa.y[13],UMa.y[14],UMa.y[20]])-labelxy]

        C_B_list = [C_B01,C_B02,C_B03,C_B04,C_B05,C_B06,C_B07,C_B08,C_B09,C_B10,\
                    C_B11,C_B12,C_B13,C_B14,C_B15,C_B16,C_B17,C_B18,C_B19,C_B20]

        # 太微垣 linecollection
        C_B_line_xy1 = []
        C_B_line_xy2 = []        
        for i in range(len(C_B_list)):
            for j in range(len(C_B_list[i]))[0::2]:
                if math.hypot(C_B_list[i][j][0]-C_B_list[i][j][1],C_B_list[i][j+1][0]-C_B_list[i][j+1][1]) < hori_border:
                    C_B_line_xy1.append((C_B_list[i][j][0],C_B_list[i][j+1][0]))
                    C_B_line_xy2.append((C_B_list[i][j][1],C_B_list[i][j+1][1]))

        C_B_line_list = []
        for i in range(len(C_B_line_xy1)):            
            C_B_line_list.append([C_B_line_xy1[i],C_B_line_xy2[i]])
        
        lc_C_B = mc.LineCollection(C_B_line_list, colors='white', zorder=2+2.5)
        lc_C_B.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_B)
        
        CBn_list = [[CB01n,'太微左垣'],[CB02n,'太微右垣'],[CB03n,'謁者'],[CB04n,'三公'],[CB05n,'九卿'],\
                    [CB06n,'五諸侯'],[CB07n,'內屏'],[CB08n,'五帝座'],[CB09n,'幸臣'],[CB10n,'太子'],\
                    [CB11n,'從官'],[CB12n,'郎將'],[CB13n,'虎賁'],[CB14n,'常陳'],[CB15n,'郎位'],\
                    [CB16n,'明堂'],[CB17n,'靈台'],[CB18n,'少微'],[CB19n,'長垣'],[CB20n,'三台']]
      
        for i in range(len(CBn_list)):
            if len(CBn_list[i][0]) != 0:
                if (CBn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CBn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CBn_list[i][0])-min(CBn_list[i][0]) < hori_border:
                    ax_label.annotate(str(CBn_list[i][1]),(CBn_list[i][0][0],CBn_list[i][0][1]),color='w',\
                                      fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ########
        #天市垣#
        ########
        #天市左垣#
        C_C01 = [[Aql.x[2],Her.x[75]],[Aql.y[2],Her.y[75]],[Aql.x[2],Ser.x[15]],[Aql.y[2],Ser.y[15]],\
                 [Her.x[2],Her.x[20]],[Her.y[2],Her.y[20]],[Her.x[4],Her.x[10]],[Her.y[4],Her.y[10]],\
                 [Her.x[4],Her.x[20]],[Her.y[4],Her.y[20]],[Her.x[10],Her.x[75]],[Her.y[10],Her.y[75]],\
                 [Oph.x[1],Ser.x[3]],[Oph.y[1],Ser.y[3]],[Oph.x[8],Ser.x[1]],[Oph.y[8],Ser.y[1]],\
                 [Oph.x[8],Ser.x[3]],[Oph.y[8],Ser.y[3]],[Ser.x[1],Ser.x[15]],[Ser.y[1],Ser.y[15]]]
        CC01n = [numpy.mean([Aql.x[2],Ser.x[15]]),\
                 numpy.mean([Aql.y[2],Ser.y[15]])]
        #天市右垣#
        C_C02 = [[Her.x[0],Her.x[8]],[Her.y[0],Her.y[8]],[Her.x[8],Her.x[38]],[Her.y[8],Her.y[38]],\
                 [Her.x[38],Ser.x[8]],[Her.y[38],Ser.y[8]],[Oph.x[2],Oph.x[6]],[Oph.y[2],Oph.y[6]],\
                 [Oph.x[3],Ser.x[5]],[Oph.y[3],Ser.y[5]],[Oph.x[3],Oph.x[6]],[Oph.y[3],Oph.y[6]],\
                 [Ser.x[0],Ser.x[5]],[Ser.y[0],Ser.y[5]],[Ser.x[0],Ser.x[7]],[Ser.y[0],Ser.y[7]],\
                 [Ser.x[4],Ser.x[7]],[Ser.y[4],Ser.y[7]],[Ser.x[4],Ser.x[8]],[Ser.y[4],Ser.y[8]]]
        CC02n = [numpy.mean([Her.x[0],Her.x[8],Her.x[38],Oph.x[2],Oph.x[3],Oph.x[6],Ser.x[0],Ser.x[4],\
                             Ser.x[5],Ser.x[7],Ser.x[8]]),\
                 numpy.mean([Her.y[0],Her.y[8],Her.y[38],Oph.y[2],Oph.y[3],Oph.y[6],Ser.y[0],Ser.y[4],\
                             Ser.y[5],Ser.y[7],Ser.y[8]])]
        #市樓#
        C_C03 = [[Oph.x[25],Ser.x[10]],[Oph.y[25],Ser.y[10]],[Oph.x[42],Ser.x[11]],[Oph.y[42],Ser.y[11]]]
        CC03n = [numpy.mean([Oph.x[25],Oph.x[42],Ser.x[10],Ser.x[11]])+labelxy,\
                 numpy.mean([Oph.y[25],Oph.y[42],Ser.y[10],Ser.y[11]])]
        #車肆#
        C_C04 = [[Oph.x[26],Oph.x[29]],[Oph.y[26],Oph.y[29]]]
        CC04n = [numpy.mean([Oph.x[26],Oph.x[29]]),\
                 numpy.mean([Oph.y[26],Oph.y[29]])+labelxy]
        #宗正#
        C_C05 = [[Oph.x[4],Oph.x[10]],[Oph.y[4],Oph.y[10]]]
        CC05n = [numpy.mean([Oph.x[4],Oph.x[10]])+labelxy,\
                 numpy.mean([Oph.y[4],Oph.y[10]])]
        #宗人#
        C_C06 = [[Oph.x[12],Oph.x[22]],[Oph.y[12],Oph.y[22]],[Oph.x[12],Oph.x[27]],[Oph.y[12],Oph.y[27]],\
                 [Oph.x[13],Oph.x[22]],[Oph.y[13],Oph.y[22]]]
        CC06n = [numpy.mean([Oph.x[12],Oph.x[13],Oph.x[22]]),\
                 numpy.mean([Oph.y[12],Oph.y[13],Oph.y[22]])-2*labelxy]
        #宗#
        C_C07 = [[Her.x[15],Her.x[19]],[Her.y[15],Her.y[19]]]
        CC07n = [numpy.mean([Her.x[15],Her.x[19]])+labelxy,\
                 numpy.mean([Her.y[15],Her.y[19]])]
        #帛度#
        C_C08 = [[Her.x[18],Her.x[35]],[Her.y[18],Her.y[35]]]
        CC08n = [numpy.mean([Her.x[18],Her.x[35]]),\
                 numpy.mean([Her.y[18],Her.y[35]])-labelxy]
        #屠肆#
        C_C09 = [[Her.x[11],Her.x[44]],[Her.y[11],Her.y[44]]]
        CC09n = [numpy.mean([Her.x[11],Her.x[44]]),\
                 numpy.mean([Her.y[11],Her.y[44]])-labelxy]
        #侯#
        C_C10 = []
        CC10n = [Oph.x[0],Oph.y[0]-labelxy]
        #帝座#
        C_C11 = []
        CC11n = [Her.x[5],Her.y[5]-labelxy]
        #宦者#
        C_C12 = [[Her.x[33],Oph.x[45]],[Her.y[33],Oph.y[45]],[Her.x[33],Her.x[132]],[Her.y[33],Her.y[132]],\
                 [Her.x[37],Her.x[132]],[Her.y[37],Her.y[132]]]
        CC12n = [numpy.mean([Her.x[33],Oph.x[45],Her.x[132]]),\
                 numpy.mean([Her.y[33],Oph.y[45],Her.y[132]])]
        #列肆#
        C_C13 = [[Oph.x[11],Ser.x[17]],[Oph.y[11],Ser.y[17]]]
        CC13n = [numpy.mean([Oph.x[11],Ser.x[17]]),\
                 numpy.mean([Oph.y[11],Ser.y[17]])-labelxy]
        #斗#
        C_C14 = [[Her.x[23],Her.x[31]],[Her.y[23],Her.y[31]]]
        CC14n = [numpy.mean([Her.x[23],Her.x[31]])+labelxy,\
                 numpy.mean([Her.y[23],Her.y[31]])]
        #斛#
        C_C15 = [[Her.x[51],Her.x[76]],[Her.y[51],Her.y[76]],[Her.x[76],Oph.x[5]],[Her.y[76],Oph.y[5]],\
                 [Oph.x[5],Oph.x[18]],[Oph.y[5],Oph.y[18]]]
        CC15n = [numpy.mean([Her.x[51],Her.x[76],Oph.x[5],Oph.x[18]]),\
                 numpy.mean([Her.y[51],Her.y[76],Oph.y[5],Oph.y[18]])]
        #貫索#
        C_C16 = [[CrB.x[1],CrB.x[2]],[CrB.y[1],CrB.y[2]],[CrB.x[1],CrB.x[3]],[CrB.y[1],CrB.y[3]],\
                 [CrB.x[2],CrB.x[4]],[CrB.y[2],CrB.y[4]],[CrB.x[3],CrB.x[6]],[CrB.y[3],CrB.y[6]],\
                 [CrB.x[4],CrB.x[18]],[CrB.y[4],CrB.y[18]],[CrB.x[5],CrB.x[6]],[CrB.y[5],CrB.y[6]],\
                 [CrB.x[5],CrB.x[10]],[CrB.y[5],CrB.y[10]],[CrB.x[10],CrB.x[15]],[CrB.y[10],CrB.y[15]]]
        CC16n = [numpy.mean([CrB.x[1],CrB.x[2],CrB.x[3],CrB.x[4],CrB.x[5],CrB.x[6],CrB.x[10],CrB.x[15],\
                             CrB.x[18]]),\
                 numpy.mean([CrB.y[1],CrB.y[2],CrB.y[3],CrB.y[4],CrB.y[5],CrB.y[6],CrB.y[10],CrB.y[15],\
                             CrB.y[18]])]
        #七公#
        C_C17 = [[Boo.x[4],Boo.x[10]],[Boo.y[4],Boo.y[10]],[Boo.x[10],Boo.x[31]],[Boo.y[10],Boo.y[31]],\
                 [Her.x[13],Her.x[17]],[Her.y[13],Her.y[17]],[Boo.x[31],Her.x[25]],[Boo.y[31],Her.y[25]],\
                 [Her.x[13],Her.x[32]],[Her.y[13],Her.y[32]],[Her.x[17],Her.x[25]],[Her.y[17],Her.y[25]]]
        CC17n = [numpy.mean([Boo.x[4],Boo.x[10],Boo.x[31],Her.x[13],Her.x[17],Her.x[25],Her.x[32]]),\
                 numpy.mean([Boo.y[4],Boo.y[10],Boo.y[31],Her.y[13],Her.y[17],Her.y[25],Her.y[32]])-labelxy]
        #天紀#
        C_C18 = [[CrB.x[9],Her.x[1]],[CrB.y[9],Her.y[1]],[Her.x[1],Her.x[14]],[Her.y[1],Her.y[14]],\
                 [Her.x[12],Her.x[88]],[Her.y[12],Her.y[88]],[Her.x[14],Her.x[56]],[Her.y[14],Her.y[56]],\
                 [Her.x[30],Her.x[56]],[Her.y[30],Her.y[56]],[Her.x[30],Her.x[88]],[Her.y[30],Her.y[88]]]
        CC18n = [numpy.mean([CrB.x[9],Her.x[1],Her.x[12],Her.x[14],Her.x[30],Her.x[56],Her.x[88]]),\
                 numpy.mean([CrB.y[9],Her.y[1],Her.y[12],Her.y[14],Her.y[30],Her.y[56],Her.y[88]])-labelxy]
        #女床#
        C_C19 = [[Her.x[3],Her.x[26]],[Her.y[3],Her.y[26]],[Her.x[22],Her.x[26]],[Her.y[22],Her.y[26]]]
        CC19n = [numpy.mean([Her.x[3],Her.x[22],Her.x[26]])-labelxy,\
                 numpy.mean([Her.y[3],Her.y[22],Her.y[26]])]

        C_C_list = [C_C01,C_C02,C_C03,C_C04,C_C05,C_C06,C_C07,C_C08,C_C09,C_C10,\
                    C_C11,C_C12,C_C13,C_C14,C_C15,C_C16,C_C17,C_C18,C_C19]

        # 天市垣 linecollection
        C_C_line_xy1 = []
        C_C_line_xy2 = []        
        for i in range(len(C_C_list)):
            for j in range(len(C_C_list[i]))[0::2]:
                if math.hypot(C_C_list[i][j][0]-C_C_list[i][j][1],C_C_list[i][j+1][0]-C_C_list[i][j+1][1]) < hori_border:
                    C_C_line_xy1.append((C_C_list[i][j][0],C_C_list[i][j+1][0]))
                    C_C_line_xy2.append((C_C_list[i][j][1],C_C_list[i][j+1][1]))

        C_C_line_list = []
        for i in range(len(C_C_line_xy1)):            
            C_C_line_list.append([C_C_line_xy1[i],C_C_line_xy2[i]])
        
        lc_C_C = mc.LineCollection(C_C_line_list, colors='white', zorder=2+2.5)
        lc_C_C.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_C)

        CCn_list = [[CC01n,'天市左垣'],[CC02n,'天市右垣'],[CC03n,'市樓'],[CC04n,'車肆'],[CC05n,'宗正'],\
                    [CC06n,'宗人'],[CC07n,'宗'],[CC08n,'帛度'],[CC09n,'屠肆'],[CC10n,'侯'],\
                    [CC11n,'帝座'],[CC12n,'宦者'],[CC13n,'列肆'],[CC14n,'斗'],[CC15n,'斛'],\
                    [CC16n,'貫索'],[CC17n,'七公'],[CC18n,'天紀'],[CC19n,'女床']]
      
        for i in range(len(CCn_list)):
            if len(CCn_list[i][0]) != 0:
                if (CCn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CCn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CCn_list[i][0])-min(CCn_list[i][0]) < hori_border:
                    ax_label.annotate(str(CCn_list[i][1]),(CCn_list[i][0][0],CCn_list[i][0][1]),color='w',\
                                      fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #東宮蒼龍#
        ##########
        #角宿#
        C_D01 = [[Vir.x[0],Vir.x[2]],[Vir.y[0],Vir.y[2]]]
        CD01n = [numpy.mean([Vir.x[0],Vir.x[2]])-labelxy,\
                 numpy.mean([Vir.y[0],Vir.y[2]])]
        #平道#
        C_D02 = [[Vir.x[15],Vir.x[33]],[Vir.y[15],Vir.y[33]]]
        CD02n = [numpy.mean([Vir.x[15],Vir.x[33]])+labelxy,\
                 numpy.mean([Vir.y[15],Vir.y[33]])]
        #天田#
        C_D03 = [[Vir.x[14],Vir.x[29]],[Vir.y[14],Vir.y[29]]]
        CD03n = [numpy.mean([Vir.x[14],Vir.x[29]]),\
                 numpy.mean([Vir.y[14],Vir.y[29]])-labelxy]
        #進賢#
        C_D04 = []
        CD04n = [] # ???
        #周鼎#
        C_D05 = [[Com.x[0],Com.x[8]],[Com.y[0],Com.y[8]],[Com.x[4],Com.x[8]],[Com.y[4],Com.y[8]]]
        CD05n = [numpy.mean([Com.x[0],Com.x[4],Com.x[8]])+2*labelxy,\
                 numpy.mean([Com.y[0],Com.y[4],Com.y[8]])]
        #天門#
        C_D06 = [[Vir.x[22],Vir.x[35]],[Vir.y[22],Vir.y[35]]]
        CD06n = [numpy.mean([Vir.x[22],Vir.x[35]]),\
                 numpy.mean([Vir.y[22],Vir.y[35]])-labelxy]
        #平#
        C_D07 = [[Hya.x[1],Hya.x[4]],[Hya.y[1],Hya.y[4]]]
        CD07n = [numpy.mean([Hya.x[1],Hya.x[4]]),\
                 numpy.mean([Hya.y[1],Hya.y[4]])-labelxy]
        #庫樓#
        C_D08 = [[Cen.x[6],Cen.x[7]],[Cen.y[6],Cen.y[7]],[Cen.x[3],Cen.x[6]],[Cen.y[3],Cen.y[6]],\
                 [Cen.x[3],Cen.x[25]],[Cen.y[3],Cen.y[25]],[Cen.x[17],Cen.x[25]],[Cen.y[17],Cen.y[25]],\
                 [Cen.x[4],Cen.x[17]],[Cen.y[4],Cen.y[17]],[Cen.x[4],Cen.x[15]],[Cen.y[4],Cen.y[15]],\
                 [Cen.x[15],Cen.x[19]],[Cen.y[15],Cen.y[19]]]
        CD08n = [numpy.mean([Cen.x[3],Cen.x[4],Cen.x[6],Cen.x[7],Cen.x[15],Cen.x[17],Cen.x[19],Cen.x[25]]),\
                 numpy.mean([Cen.y[3],Cen.y[4],Cen.y[6],Cen.y[7],Cen.y[15],Cen.y[17],Cen.y[19],Cen.y[25]])+2*labelxy]
        #柱#
        C_D09 = [[Cen.x[16],Cen.x[32]],[Cen.y[16],Cen.y[32]],[Cen.x[22],Cen.x[34]],[Cen.y[22],Cen.y[34]],\
                 [Cen.x[26],Cen.x[39]],[Cen.y[26],Cen.y[39]],[Cen.x[39],Cen.x[47]],[Cen.y[39],Cen.y[47]],\
                 [Lup.x[7],Lup.x[18]],[Lup.y[7],Lup.y[18]]]
        CD09an = [numpy.mean([Cen.x[16],Cen.x[32]])+labelxy,\
                  numpy.mean([Cen.y[16],Cen.y[32]])-labelxy]
        CD09bn = [numpy.mean([Cen.x[22],Cen.x[34]])-labelxy,\
                  numpy.mean([Cen.y[22],Cen.y[34]])+labelxy]
        CD09cn = [numpy.mean([Cen.x[26],Cen.x[39],Cen.x[47]])+labelxy,\
                  numpy.mean([Cen.y[26],Cen.y[39],Cen.y[47]])+2*labelxy]
        CD09dn = [numpy.mean([Lup.x[7],Lup.x[18]]),\
                  numpy.mean([Lup.y[7],Lup.y[18]])-labelxy]
        #衡#
        C_D10 = [[Cen.x[10],Cen.x[13]],[Cen.y[10],Cen.y[13]],[Cen.x[10],Cen.x[14]],[Cen.y[10],Cen.y[14]],\
                 [Cen.x[14],Cen.x[33]],[Cen.y[14],Cen.y[33]]]
        CD10n = [numpy.mean([Cen.x[10],Cen.x[13],Cen.x[14],Cen.x[33]]),\
                 numpy.mean([Cen.y[10],Cen.y[13],Cen.y[14],Cen.y[33]])-labelxy]
        #南門#
        C_D11 = [[Cen.x[0],Cen.x[5]],[Cen.y[0],Cen.y[5]]]
        CD11n = [numpy.mean([Cen.x[0],Cen.x[5]]),\
                 numpy.mean([Cen.y[0],Cen.y[5]])-labelxy]
        #亢宿#
        C_D12 = [[Vir.x[11],Vir.x[13]],[Vir.y[11],Vir.y[13]],[Vir.x[11],Vir.x[25]],[Vir.y[11],Vir.y[25]],\
                 [Vir.x[13],Vir.x[17]],[Vir.y[13],Vir.y[17]]]
        CD12n = [numpy.mean([Vir.x[11],Vir.x[13],Vir.x[25],Vir.x[17]]),\
                 numpy.mean([Vir.y[11],Vir.y[13],Vir.y[25],Vir.y[17]])]
        #大角#
        C_D13 = []
        CD13n = [Boo.x[0],Boo.y[0]-labelxy]
        #右攝提#
        C_D14 = [[Boo.x[1],Boo.x[13]],[Boo.y[1],Boo.y[13]],[Boo.x[8],Boo.x[13]],[Boo.y[8],Boo.y[13]]]
        CD14n = [numpy.mean([Boo.x[1],Boo.x[8],Boo.x[13]])-labelxy,\
                 numpy.mean([Boo.y[1],Boo.y[8],Boo.y[13]])]
        #左攝提#
        C_D15 = [[Boo.x[11],Boo.x[29]],[Boo.y[11],Boo.y[29]],[Boo.x[17],Boo.x[29]],[Boo.y[17],Boo.y[29]]]
        CD15n = [numpy.mean([Boo.x[11],Boo.x[17],Boo.x[29]])-labelxy,\
                 numpy.mean([Boo.y[11],Boo.y[17],Boo.y[29]])]
        #頓頑#
        C_D16 = [[Lup.x[8],Lup.x[32]],[Lup.y[8],Lup.y[32]]]
        CD16n = [numpy.mean([Lup.x[8],Lup.x[32]])+labelxy,\
                 numpy.mean([Lup.y[8],Lup.y[32]])]
        #陽門#
        C_D17 = [[Cen.x[21],Cen.x[23]],[Cen.y[21],Cen.y[23]]]
        CD17n = [numpy.mean([Cen.x[21],Cen.x[23]])+2*labelxy,\
                 numpy.mean([Cen.y[21],Cen.y[23]])+labelxy]
        #折威#
        C_D18 = [[Lib.x[2],Lib.x[21]],[Lib.y[2],Lib.y[21]],[Lib.x[21],Lib.x[38]],[Lib.y[21],Lib.y[38]]]
        CD18n = [numpy.mean([Lib.x[2],Lib.x[21],Lib.x[38]]),\
                 numpy.mean([Lib.y[2],Lib.y[21],Lib.y[38]])-labelxy]
        #氐宿#
        C_D19 = [[Lib.x[0],Lib.x[5]],[Lib.y[0],Lib.y[5]],[Lib.x[1],Lib.x[8]],[Lib.y[1],Lib.y[8]],\
                 [Lib.x[5],Lib.x[8]],[Lib.y[5],Lib.y[8]]]
        CD19n = [numpy.mean([Lib.x[0],Lib.x[1],Lib.x[5],Lib.x[8]]),\
                 numpy.mean([Lib.y[0],Lib.y[1],Lib.y[5],Lib.y[8]])]
        #天乳#
        C_D20 = []
        CD20n = [Ser.x[2],Ser.y[2]-labelxy]
        #招搖#
        C_D21 = []
        CD21n = [Boo.x[3],Boo.y[3]-labelxy]
        #梗河#
        C_D22 = [[Boo.x[2],Boo.x[12]],[Boo.y[2],Boo.y[12]],[Boo.x[6],Boo.x[12]],[Boo.y[6],Boo.y[12]]]
        CD22n = [numpy.mean([Boo.x[2],Boo.x[6],Boo.x[12]]),\
                 numpy.mean([Boo.y[2],Boo.y[6],Boo.y[12]])-labelxy]
        #帝席#
        C_D23 = [[Boo.x[23],Boo.x[115]],[Boo.y[23],Boo.y[115]],[Boo.x[30],Boo.x[115]],[Boo.y[30],Boo.y[115]]]
        CD23n = [numpy.mean([Boo.x[23],Boo.x[30],Boo.x[115]]),\
                 numpy.mean([Boo.y[23],Boo.y[30],Boo.y[115]])]
        #亢池#
        C_D24 = [[Boo.x[25],Boo.x[50]],[Boo.y[25],Boo.y[50]],[Boo.x[44],Boo.x[50]],[Boo.y[44],Boo.y[50]]]
        CD24n = [numpy.mean([Boo.x[25],Boo.x[44],Boo.x[50]])-labelxy,\
                 numpy.mean([Boo.y[25],Boo.y[44],Boo.y[50]])]
        #陣車#
        C_D25 = [[Hya.x[18],Hya.x[111]],[Hya.y[18],Hya.y[111]],[Hya.x[111],Lup.x[17]],[Hya.y[111],Lup.y[17]]]
        CD25n = [numpy.mean([Hya.x[18],Hya.x[111],Lup.x[17]]),\
                 numpy.mean([Hya.y[18],Hya.y[111],Lup.y[17]])]
        #騎官#
        C_D26 = [[Cen.x[12],Lup.x[1]],[Cen.y[12],Lup.y[1]],[Cen.x[12],Lup.x[3]],[Cen.y[12],Lup.y[3]],\
                 [Lup.x[0],Lup.x[15]],[Lup.y[0],Lup.y[15]],[Lup.x[1],Lup.x[12]],[Lup.y[1],Lup.y[12]],\
                 [Lup.x[2],Lup.x[3]],[Lup.y[2],Lup.y[3]],[Lup.x[4],Lup.x[12]],[Lup.y[4],Lup.y[12]],\
                 [Lup.x[4],Lup.x[14]],[Lup.y[4],Lup.y[14]],[Lup.x[14],Lup.x[29]],[Lup.y[14],Lup.y[29]],\
                 [Lup.x[15],Lup.x[29]],[Lup.y[15],Lup.y[29]]]
        CD26n = [numpy.mean([Cen.x[12],Lup.x[0],Lup.x[1],Lup.x[2],Lup.x[3],Lup.x[4],Lup.x[12],Lup.x[14],\
                             Lup.x[15],Lup.x[29]]),\
                 numpy.mean([Cen.y[12],Lup.y[0],Lup.y[1],Lup.y[2],Lup.y[3],Lup.y[4],Lup.y[12],Lup.y[14],\
                             Lup.y[15],Lup.y[29]])+labelxy]
        #車騎#
        C_D27 = [[Lup.x[5],Lup.x[11]],[Lup.y[5],Lup.y[11]],[Lup.x[11],Lup.x[19]],[Lup.y[11],Lup.y[19]]]
        CD27n = [numpy.mean([Lup.x[5],Lup.x[11],Lup.x[19]]),\
                 numpy.mean([Lup.y[5],Lup.y[11],Lup.y[19]])]
        #天輻#
        C_D28 = [[Lib.x[3],Lib.x[4]],[Lib.y[3],Lib.y[4]]]
        CD28n = [numpy.mean([Lib.x[3],Lib.x[4]])+2*labelxy,\
                 numpy.mean([Lib.y[3],Lib.y[4]])]
        #騎陣將軍#
        C_D29 = []
        CD29n = [Lup.x[9],Lup.y[9]-labelxy]
        #房宿#
        C_D30 = [[Sco.x[4],Sco.x[6]],[Sco.y[4],Sco.y[6]],[Sco.x[4],Sco.x[9]],[Sco.y[4],Sco.y[9]],\
                 [Sco.x[9],Sco.x[17]],[Sco.y[9],Sco.y[17]]]
        CD30n = [numpy.mean([Sco.x[4],Sco.x[6],Sco.x[9],Sco.x[17]]),\
                 numpy.mean([Sco.y[4],Sco.y[6],Sco.y[9],Sco.y[17]])]
        #鉤鈐#
        C_D31 = []
        CD31n = [Sco.x[18],Sco.y[18]-labelxy]
        #鍵閉#
        C_D32 = []
        CD32n = [Sco.x[19],Sco.y[19]-labelxy]
        #罰#
        C_D33 = [[Lib.x[27],Sco.x[73]],[Lib.y[27],Sco.y[73]],[Sco.x[60],Sco.x[73]],[Sco.y[60],Sco.y[73]]]
        CD33n = [numpy.mean([Lib.x[27],Sco.x[60],Sco.x[73]])-labelxy,\
                 numpy.mean([Lib.y[27],Sco.y[60],Sco.y[73]])]
        #東咸#
        C_D34 = [[Oph.x[15],Oph.x[20]],[Oph.y[15],Oph.y[20]],[Oph.x[20],Oph.x[23]],[Oph.y[20],Oph.y[23]],\
                 [Oph.x[21],Oph.x[23]],[Oph.y[21],Oph.y[23]]]
        CD34n = [numpy.mean([Oph.x[15],Oph.x[20],Oph.x[21],Oph.x[23]])-labelxy,\
                 numpy.mean([Oph.y[15],Oph.y[20],Oph.y[21],Oph.y[23]])]
        #西咸#
        C_D35 = [[Lib.x[6],Lib.x[11]],[Lib.y[6],Lib.y[11]],[Lib.x[6],Lib.x[25]],[Lib.y[6],Lib.y[25]],\
                 [Lib.x[11],Sco.x[29]],[Lib.y[11],Sco.y[29]]]
        CD35n = [numpy.mean([Lib.x[6],Lib.x[11],Lib.x[25],Sco.x[29]])+labelxy,\
                 numpy.mean([Lib.y[6],Lib.y[11],Lib.y[25],Sco.y[29]])]
        #日#
        C_D36 = []
        CD36n = [Lib.x[10],Lib.y[10]-labelxy]
        #從官#
        C_D37 = [[Lup.x[10],Lup.x[27]],[Lup.y[10],Lup.y[27]]]
        CD37n = [numpy.mean([Lup.x[10],Lup.x[27]]),\
                 numpy.mean([Lup.y[10],Lup.y[27]])-labelxy]
        #心宿#
        C_D38 = [[Sco.x[0],Sco.x[8]],[Sco.y[0],Sco.y[8]],[Sco.x[0],Sco.x[10]],[Sco.y[0],Sco.y[10]]]
        CD38n = [numpy.mean([Sco.x[0],Sco.x[8],Sco.x[10]]),\
                 numpy.mean([Sco.y[0],Sco.y[8],Sco.y[10]])-labelxy]
        #積卒#
        C_D39 = [[Lup.x[6],Lup.x[13]],[Lup.y[6],Lup.y[13]]]
        CD39n = [numpy.mean([Lup.x[6],Lup.x[13]])-labelxy,\
                 numpy.mean([Lup.y[6],Lup.y[13]])]
        #尾宿#
        C_D40 = [[Sco.x[1],Sco.x[5]],[Sco.y[1],Sco.y[5]],[Sco.x[2],Sco.x[11]],[Sco.y[2],Sco.y[11]],\
                 [Sco.x[2],Sco.x[14]],[Sco.y[2],Sco.y[14]],[Sco.x[3],Sco.x[12]],[Sco.y[3],Sco.y[12]],\
                 [Sco.x[5],Sco.x[7]],[Sco.y[5],Sco.y[7]],[Sco.x[5],Sco.x[11]],[Sco.y[5],Sco.y[11]],\
                 [Sco.x[12],Sco.x[16]],[Sco.y[12],Sco.y[16]],[Sco.x[14],Sco.x[16]],[Sco.y[14],Sco.y[16]]]
        CD40n = [numpy.mean([Sco.x[1],Sco.x[2],Sco.x[3],Sco.x[5],Sco.x[7],Sco.x[11],Sco.x[12],Sco.x[14],Sco.x[16]]),\
                 numpy.mean([Sco.y[1],Sco.y[2],Sco.y[3],Sco.y[5],Sco.y[7],Sco.y[11],Sco.y[12],Sco.y[14],Sco.y[16]])]
        #神宮#
        C_D41 = []
        CD41n = [Sco.x[28],Sco.y[28]-labelxy]
        #龜#
        C_D42 = [[Ara.x[2],Ara.x[6]],[Ara.y[2],Ara.y[6]],[Ara.x[2],Ara.x[7]],[Ara.y[2],Ara.y[7]],\
                 [Ara.x[3],Ara.x[4]],[Ara.y[3],Ara.y[4]],[Ara.x[3],Ara.x[7]],[Ara.y[3],Ara.y[7]],\
                 [Ara.x[4],Ara.x[6]],[Ara.y[4],Ara.y[6]]]
        CD42n = [numpy.mean([Ara.x[2],Ara.x[3],Ara.x[4],Ara.x[6],Ara.x[7]]),\
                 numpy.mean([Ara.y[2],Ara.y[3],Ara.y[4],Ara.y[6],Ara.y[7]])]
        #天江#
        C_D43 = [[Oph.x[7],Oph.x[14]],[Oph.y[7],Oph.y[14]],[Oph.x[7],Oph.x[39]],[Oph.y[7],Oph.y[39]]]
        CD43n = [numpy.mean([Oph.x[7],Oph.x[14],Oph.x[39]]),\
                 numpy.mean([Oph.y[7],Oph.y[14],Oph.y[39]])-labelxy]
        #傅說#
        C_D44 = []
        CD44n = [Sco.x[13],Sco.y[13]-labelxy]
        #魚#
        C_D45 = []
        CD45n = [numpy.mean([Sco.x[65],Sco.x[78],Sco.x[86],Sco.x[97],Sco.x[98],Sco.x[109],Sco.x[124],Sco.x[144],\
                             Sco.x[150],Sco.x[155]]),\
                 numpy.mean([Sco.y[65],Sco.y[78],Sco.y[86],Sco.y[97],Sco.y[98],Sco.y[109],Sco.y[124],Sco.y[144],\
                             Sco.y[150],Sco.y[155]])-labelxy]
        #箕宿#
        C_D46 = [[Sgr.x[0],Sgr.x[3]],[Sgr.y[0],Sgr.y[3]],[Sgr.x[0],Sgr.x[7]],[Sgr.y[0],Sgr.y[7]],\
                 [Sgr.x[3],Sgr.x[6]],[Sgr.y[3],Sgr.y[6]]]
        CD46n = [numpy.mean([Sgr.x[0],Sgr.x[3],Sgr.x[6],Sgr.x[7]]),\
                 numpy.mean([Sgr.y[0],Sgr.y[3],Sgr.y[6],Sgr.y[7]])]
        #糠#
        C_D47 = []
        CD47n = [Oph.x[16],Oph.y[16]-labelxy]
        #杵#
        C_D48 = [[Ara.x[0],Ara.x[1]],[Ara.y[0],Ara.y[1]],[Ara.x[1],Ara.x[8]],[Ara.y[1],Ara.y[8]]]
        CD48n = [numpy.mean([Ara.x[0],Ara.x[1],Ara.x[8]]),\
                 numpy.mean([Ara.y[0],Ara.y[1],Ara.y[8]])-labelxy]

        C_D_list = [C_D01,C_D02,C_D03,C_D04,C_D05,C_D06,C_D07,C_D08,C_D09,C_D10,\
                    C_D11,C_D12,C_D13,C_D14,C_D15,C_D16,C_D17,C_D18,C_D19,C_D20,\
                    C_D21,C_D22,C_D23,C_D24,C_D25,C_D26,C_D27,C_D28,C_D29,C_D30,\
                    C_D31,C_D32,C_D33,C_D34,C_D35,C_D36,C_D37,C_D38,C_D39,C_D40,\
                    C_D41,C_D42,C_D43,C_D44,C_D45,C_D46,C_D47,C_D48]

        # 東宮蒼龍 linecollection
        C_D_line_z_xy1 = []
        C_D_line_z_xy2 = [] 
        C_D_line_xy1 = []
        C_D_line_xy2 = []        
        for i in range(len(C_D_list)):
            for j in range(len(C_D_list[i]))[0::2]:
                if math.hypot(C_D_list[i][j][0]-C_D_list[i][j][1],C_D_list[i][j+1][0]-C_D_list[i][j+1][1]) < hori_border:
                    if i in set([0,11,18,29,37,39,45]):
                        C_D_line_z_xy1.append((C_D_list[i][j][0],C_D_list[i][j+1][0]))
                        C_D_line_z_xy2.append((C_D_list[i][j][1],C_D_list[i][j+1][1]))
                    else:
                        C_D_line_xy1.append((C_D_list[i][j][0],C_D_list[i][j+1][0]))
                        C_D_line_xy2.append((C_D_list[i][j][1],C_D_list[i][j+1][1]))

        C_D_line_z_list = []
        for i in range(len(C_D_line_z_xy1)):            
            C_D_line_z_list.append([C_D_line_z_xy1[i],C_D_line_z_xy2[i]])
        
        C_D_line_list = []
        for i in range(len(C_D_line_xy1)):            
            C_D_line_list.append([C_D_line_xy1[i],C_D_line_xy2[i]])
        
        lc_C_D_z = mc.LineCollection(C_D_line_z_list, colors='yellow', zorder=2+2.5)
        lc_C_D = mc.LineCollection(C_D_line_list, colors='white', zorder=2+2.5)
        lc_C_D_z.set_alpha(plot_alpha)
        lc_C_D.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_D_z)
        ax0.add_collection(lc_C_D)

        CDn_list = [[CD01n,'角宿'],[CD02n,'平道'],[CD03n,'天田'],[CD04n,'進賢'],[CD05n,'周鼎'],\
                    [CD06n,'天門'],[CD07n,'平'],[CD08n,'庫樓'],[CD09an,'柱'],[CD09bn,'柱'],\
                    [CD09cn,'柱'],[CD09dn,'柱'],[CD10n,'衡'],[CD11n,'南門'],[CD12n,'亢宿'],\
                    [CD13n,'大角'],[CD14n,'右攝提'],[CD15n,'左攝提'],[CD16n,'頓頑'],[CD17n,'陽門'],\
                    [CD18n,'折威'],[CD19n,'氐宿'],[CD20n,'天乳'],[CD21n,'招搖'],[CD22n,'梗河'],\
                    [CD23n,'帝席'],[CD24n,'亢池'],[CD25n,'陣車'],[CD26n,'騎官'],[CD27n,'車騎'],\
                    [CD28n,'天輻'],[CD29n,'騎陣將軍'],[CD30n,'房宿'],[CD31n,'鉤鈐'],[CD32n,'鍵閉'],\
                    [CD33n,'罰'],[CD34n,'東咸'],[CD35n,'西咸'],[CD36n,'日'],[CD37n,'從官'],\
                    [CD38n,'心宿'],[CD39n,'積卒'],[CD40n,'尾宿'],[CD41n,'神宮'],[CD42n,'龜'],\
                    [CD43n,'天江'],[CD44n,'傅說'],[CD45n,'魚'],[CD46n,'箕宿'],[CD47n,'糠'],\
                    [CD48n,'杵']]

        for i in range(len(CDn_list)):
            if len(CDn_list[i][0]) != 0:
                if (CDn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CDn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CDn_list[i][0])-min(CDn_list[i][0]) < hori_border:
                    if i in set([0,14,21,32,40,42,48]):
                        ax_label.annotate(str(CDn_list[i][1]),(CDn_list[i][0][0],CDn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(CDn_list[i][1]),(CDn_list[i][0][0],CDn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #北宮玄武#
        ##########
        #斗宿#
        C_E01 = [[Sgr.x[1],Sgr.x[8]],[Sgr.y[1],Sgr.y[8]],[Sgr.x[1],Sgr.x[9]],[Sgr.y[1],Sgr.y[9]],\
                 [Sgr.x[2],Sgr.x[9]],[Sgr.y[2],Sgr.y[9]],[Sgr.x[4],Sgr.x[8]],[Sgr.y[4],Sgr.y[8]],\
                 [Sgr.x[4],Sgr.x[12]],[Sgr.y[4],Sgr.y[12]]]
        CE01n = [numpy.mean([Sgr.x[1],Sgr.x[2],Sgr.x[4],Sgr.x[8],Sgr.x[9],Sgr.x[12]]),\
                 numpy.mean([Sgr.y[1],Sgr.y[2],Sgr.y[4],Sgr.y[8],Sgr.y[9],Sgr.y[12]])]
        #建#
        C_E02 = [[Sgr.x[5],Sgr.x[36]],[Sgr.y[5],Sgr.y[36]],[Sgr.x[5],Sgr.x[11]],[Sgr.y[5],Sgr.y[11]],\
                 [Sgr.x[10],Sgr.x[11]],[Sgr.y[10],Sgr.y[11]],[Sgr.x[13],Sgr.x[24]],[Sgr.y[13],Sgr.y[24]],\
                 [Sgr.x[13],Sgr.x[36]],[Sgr.y[13],Sgr.y[36]]]
        CE02n = [numpy.mean([Sgr.x[5],Sgr.x[10],Sgr.x[11],Sgr.x[13],Sgr.x[24],Sgr.x[36]]),\
                 numpy.mean([Sgr.y[5],Sgr.y[10],Sgr.y[11],Sgr.y[13],Sgr.y[24],Sgr.y[36]])]
        #天弁#
        C_E03 = [[Aql.x[5],Aql.x[9]],[Aql.y[5],Aql.y[9]],[Aql.x[5],Aql.x[38]],[Aql.y[5],Aql.y[38]],\
                 [Aql.x[9],Sct.x[5]],[Aql.y[9],Sct.y[5]],[Aql.x[37],Aql.x[38]],[Aql.y[37],Aql.y[38]],\
                 [Sct.x[0],Sct.x[4]],[Sct.y[0],Sct.y[4]],[Sct.x[1],Sct.x[5]],[Sct.y[1],Sct.y[5]],\
                 [Sct.x[1],Sct.x[6]],[Sct.y[1],Sct.y[6]],[Sct.x[4],Sct.x[6]],[Sct.y[4],Sct.y[6]],]
        CE03n = [numpy.mean([Aql.x[5],Aql.x[9],Aql.x[37],Aql.x[38],Sct.x[0],Sct.x[1],Sct.x[4],Sct.x[5],\
                             Sct.x[6]]),\
                 numpy.mean([Aql.y[5],Aql.y[9],Aql.y[37],Aql.y[38],Sct.y[0],Sct.y[1],Sct.y[4],Sct.y[5],\
                             Sct.y[6]])]
        #鱉#
        C_E04 = [[CrA.x[0],CrA.x[1]],[CrA.y[0],CrA.y[1]],[CrA.x[0],CrA.x[7]],[CrA.y[0],CrA.y[7]],\
                 [CrA.x[1],CrA.x[2]],[CrA.y[1],CrA.y[2]],[CrA.x[2],CrA.x[4]],[CrA.y[2],CrA.y[4]],\
                 [CrA.x[3],CrA.x[8]],[CrA.y[3],CrA.y[8]],[CrA.x[3],Tel.x[0]],[CrA.y[3],Tel.y[0]],\
                 [CrA.x[4],CrA.x[19]],[CrA.y[4],CrA.y[19]],[CrA.x[5],CrA.x[7]],[CrA.y[5],CrA.y[7]],\
                 [CrA.x[5],CrA.x[15]],[CrA.y[5],CrA.y[15]],[CrA.x[8],CrA.x[15]],[CrA.y[8],CrA.y[15]],\
                 [Tel.x[0],CrA.x[19]],[Tel.y[0],CrA.y[19]]]
        CE04n = [numpy.mean([CrA.x[0],CrA.x[1],CrA.x[2],CrA.x[3],CrA.x[4],CrA.x[5],CrA.x[7],CrA.x[8],\
                             CrA.x[15],CrA.x[19],Tel.x[0]]),\
                 numpy.mean([CrA.y[0],CrA.y[1],CrA.y[2],CrA.y[3],CrA.y[4],CrA.y[5],CrA.y[7],CrA.y[8],\
                             CrA.y[15],CrA.y[19],Tel.y[0]])]
        #天雞#
        C_E05 = [[Sgr.x[34],Sgr.x[42]],[Sgr.y[34],Sgr.y[42]]]
        CE05n = [numpy.mean([Sgr.x[34],Sgr.x[42]]),\
                 numpy.mean([Sgr.y[34],Sgr.y[42]])]
        #天籥#
        C_E06 = [[Oph.x[31],Oph.x[34]],[Oph.y[31],Oph.y[34]],[Oph.x[31],Oph.x[91]],[Oph.y[31],Oph.y[91]],\
                 [Oph.x[34],Sgr.x[141]],[Oph.y[34],Sgr.y[141]],[Oph.x[91],Sgr.x[20]],[Oph.y[91],Sgr.y[20]]]
        CE06n = [numpy.mean([Oph.x[31],Oph.x[34],Oph.x[91],Sgr.x[20],Sgr.x[141]]),\
                 numpy.mean([Oph.y[31],Oph.y[34],Oph.y[91],Sgr.y[20],Sgr.y[141]])]
        #狗國#
        C_E07 = [[Sgr.x[19],Sgr.x[22]],[Sgr.y[19],Sgr.y[22]],[Sgr.x[22],Sgr.x[32]],[Sgr.y[22],Sgr.y[32]],\
                 [Sgr.x[27],Sgr.x[32]],[Sgr.y[27],Sgr.y[32]]]
        CE07n = [numpy.mean([Sgr.x[19],Sgr.x[22],Sgr.x[27],Sgr.x[32]]),\
                 numpy.mean([Sgr.y[19],Sgr.y[22],Sgr.y[27],Sgr.y[32]])]
        #天淵#
        C_E08 = [[Sgr.x[14],Sgr.x[15]],[Sgr.y[14],Sgr.y[15]]]
        CE08n = [numpy.mean([Sgr.x[14],Sgr.x[15]]),\
                 numpy.mean([Sgr.y[14],Sgr.y[15]])]
        #狗#
        C_E09 = [[Sgr.x[23],Sgr.x[41]],[Sgr.y[23],Sgr.y[41]]]
        CE09n = [numpy.mean([Sgr.x[23],Sgr.x[41]]),\
                 numpy.mean([Sgr.y[23],Sgr.y[41]])]
        #農丈人#
        C_E10 = []
        CE10n = [Sgr.x[35],Sgr.y[35]]
        #牛宿#
        C_E11 = [[Cap.x[1],Cap.x[2]],[Cap.y[1],Cap.y[2]],[Cap.x[1],Cap.x[15]],[Cap.y[1],Cap.y[15]],\
                 [Cap.x[1],Cap.x[24]],[Cap.y[1],Cap.y[24]],[Cap.x[1],Cap.x[39]],[Cap.y[1],Cap.y[39]],\
                 [Cap.x[15],Cap.x[45]],[Cap.y[15],Cap.y[45]],[Cap.x[24],Cap.x[45]],[Cap.y[24],Cap.y[45]]]
        CE11n = [numpy.mean([Cap.x[1],Cap.x[2],Cap.x[15],Cap.x[24],Cap.x[39],Cap.x[45]]),\
                 numpy.mean([Cap.y[1],Cap.y[2],Cap.y[15],Cap.y[24],Cap.y[39],Cap.y[45]])]
        #天田#
        C_E12 = [[Cap.x[6],Cap.x[7]],[Cap.y[6],Cap.y[7]],[Cap.x[7],Mic.x[10]],[Cap.y[7],Mic.y[10]],\
                 [Cap.x[10],Mic.x[10]],[Cap.y[10],Mic.y[10]]]
        CE12n = [numpy.mean([Cap.x[6],Cap.x[7],Cap.x[10],Mic.x[10]]),\
                 numpy.mean([Cap.y[6],Cap.y[7],Cap.y[10],Mic.y[10]])]
        #九坎#
        C_E13 = []
        CE13n = [] # ???
        #河鼓#
        C_E14 = [[Aql.x[0],Aql.x[1]],[Aql.y[0],Aql.y[1]],[Aql.x[0],Aql.x[6]],[Aql.y[0],Aql.y[6]]]
        CE14n = [numpy.mean([Aql.x[0],Aql.x[1],Aql.x[6]]),\
                 numpy.mean([Aql.y[0],Aql.y[1],Aql.y[6]])]
        #織女#
        C_E15 = [[Lyr.x[0],Lyr.x[12]],[Lyr.y[0],Lyr.y[12]],[Lyr.x[6],Lyr.x[12]],[Lyr.y[6],Lyr.y[12]]]
        CE15n = [numpy.mean([Lyr.x[0],Lyr.x[6],Lyr.x[12]]),\
                 numpy.mean([Lyr.y[0],Lyr.y[6],Lyr.y[12]])]
        #左旗#
        C_E16 = [[Aql.x[52],Del.x[6]],[Aql.y[52],Del.y[6]],[Aql.x[52],Sge.x[8]],[Aql.y[52],Sge.y[8]],\
                 [Sge.x[0],Sge.x[4]],[Sge.y[0],Sge.y[4]],[Sge.x[0],Sge.x[7]],[Sge.y[0],Sge.y[7]],\
                 [Sge.x[1],Sge.x[3]],[Sge.y[1],Sge.y[3]],[Sge.x[1],Sge.x[4]],[Sge.y[1],Sge.y[4]],\
                 [Sge.x[2],Sge.x[3]],[Sge.y[2],Sge.y[3]],[Sge.x[7],Sge.x[8]],[Sge.y[7],Sge.y[8]]]
        CE16n = [numpy.mean([Aql.x[52],Del.x[6],Sge.x[0],Sge.x[1],Sge.x[2],Sge.x[3],Sge.x[4],Sge.x[7],\
                             Sge.x[8]]),\
                 numpy.mean([Aql.y[52],Del.y[6],Sge.y[0],Sge.y[1],Sge.y[2],Sge.y[3],Sge.y[4],Sge.y[7],\
                             Sge.y[8]])]
        #右旗#
        C_E17 = [[Aql.x[4],Aql.x[13]],[Aql.y[4],Aql.y[13]],[Aql.x[4],Aql.x[27]],[Aql.y[4],Aql.y[27]],\
                 [Aql.x[11],Aql.x[13]],[Aql.y[11],Aql.y[13]],[Aql.x[11],Aql.x[39]],[Aql.y[11],Aql.y[39]],\
                 [Aql.x[12],Aql.x[27]],[Aql.y[12],Aql.y[27]],[Aql.x[17],Aql.x[39]],[Aql.y[17],Aql.y[39]],\
                 [Aql.x[17],Aql.x[57]],[Aql.y[17],Aql.y[57]]]
        CE17n = [numpy.mean([Aql.x[4],Aql.x[11],Aql.x[12],Aql.x[13],Aql.x[17],Aql.x[27],Aql.x[39],Aql.x[57]]),\
                 numpy.mean([Aql.y[4],Aql.y[11],Aql.y[12],Aql.y[13],Aql.y[17],Aql.y[27],Aql.y[39],Aql.y[57]])]
        #天桴#
        C_E18 = [[Aql.x[3],Aql.x[53]],[Aql.y[3],Aql.y[53]],[Aql.x[7],Aql.x[48]],[Aql.y[7],Aql.y[48]],\
                 [Aql.x[48],Aql.x[53]],[Aql.y[48],Aql.y[53]]]
        CE18n = [numpy.mean([Aql.x[3],Aql.x[7],Aql.x[48],Aql.x[53]]),\
                 numpy.mean([Aql.y[3],Aql.y[7],Aql.y[48],Aql.y[53]])]
        #羅堰#
        C_E19 = [[Cap.x[19],Cap.x[21]],[Cap.y[19],Cap.y[21]],[Cap.x[19],Cap.x[44]],[Cap.y[19],Cap.y[44]]]
        CE19n = [numpy.mean([Cap.x[19],Cap.x[21],Cap.x[44]]),\
                 numpy.mean([Cap.y[19],Cap.y[21],Cap.y[44]])]
        #漸臺#
        C_E20 = [[Lyr.x[1],Lyr.x[2]],[Lyr.y[1],Lyr.y[2]],[Lyr.x[1],Lyr.x[19]],[Lyr.y[1],Lyr.y[19]],\
                 [Lyr.x[2],Lyr.x[4]],[Lyr.y[2],Lyr.y[4]]]
        CE20n = [numpy.mean([Lyr.x[1],Lyr.x[2],Lyr.x[4],Lyr.x[19]]),\
                 numpy.mean([Lyr.y[1],Lyr.y[2],Lyr.y[4],Lyr.y[19]])]
        #輦道#
        C_E21 = [[Cyg.x[46],Cyg.x[57]],[Cyg.y[46],Cyg.y[57]],[Cyg.x[57],Lyr.x[7]],[Cyg.y[57],Lyr.y[7]],\
                 [Lyr.x[3],Lyr.x[8]],[Lyr.y[3],Lyr.y[8]],[Lyr.x[7],Lyr.x[8]],[Lyr.y[7],Lyr.y[8]]]
        CE21n = [numpy.mean([Cyg.x[46],Cyg.x[57],Lyr.x[3],Lyr.x[7],Lyr.x[8]]),\
                 numpy.mean([Cyg.y[46],Cyg.y[57],Lyr.y[3],Lyr.y[7],Lyr.y[8]])]
        #女宿#
        C_E22 = [[Aqr.x[5],Aqr.x[28]],[Aqr.y[5],Aqr.y[28]],[Aqr.x[16],Aqr.x[94]],[Aqr.y[16],Aqr.y[94]],\
                 [Aqr.x[28],Aqr.x[94]],[Aqr.y[28],Aqr.y[94]]]
        CE22n = [numpy.mean([Aqr.x[5],Aqr.x[16],Aqr.x[28],Aqr.x[94]]),\
                 numpy.mean([Aqr.y[5],Aqr.y[16],Aqr.y[28],Aqr.y[94]])]
        #十二國#
        C_E23 = []
        CE23n = [numpy.mean([Cap.x[4],Cap.x[5],Cap.x[9],Cap.x[11],Cap.x[16],Cap.x[22],Cap.x[27],Cap.x[28],\
                             Cap.x[29],Cap.x[33],Cap.x[36],Cap.x[37],Cap.x[62],Cap.x[63]]),\
                 numpy.mean([Cap.y[4],Cap.y[5],Cap.y[9],Cap.y[11],Cap.y[16],Cap.y[22],Cap.y[27],Cap.y[28],\
                             Cap.y[29],Cap.y[33],Cap.y[36],Cap.y[37],Cap.y[62],Cap.y[63]])]
        #燕#
        C_E23a = []
        CE23an = [Cap.x[4],Cap.y[4]]
        #周#
        C_E23b = []
        CE23bn = [Cap.x[16],Cap.y[16]]
        #晉#
        C_E23c = []
        CE23cn = [Cap.x[11],Cap.y[11]]
        #魏#
        C_E23d = []
        CE23dn = [Cap.x[28],Cap.y[28]]
        #楚#
        C_E23e = []
        CE23en = [Cap.x[22],Cap.y[22]]
        #齊#
        C_E23f = []
        CE23fn = [Cap.x[27],Cap.y[27]]
        #韓#
        C_E23g = []
        CE23gn = [Cap.x[37],Cap.y[37]]
        #越#
        C_E23h = []
        CE23hn = [Cap.x[36],Cap.y[36]]
        #鄭#
        C_E23i = []
        CE23in = [Cap.x[62],Cap.y[62]]
        #趙#
        C_E23j = []
        CE23jn = [Cap.x[63],Cap.y[63]]
        #代#
        C_E23k = [[Cap.x[9],Cap.x[33]],[Cap.y[9],Cap.y[33]]]
        CE23kn = [numpy.mean([Cap.x[9],Cap.x[33]]),\
                  numpy.mean([Cap.y[9],Cap.y[33]])]
        #秦#
        C_E23l = [[Cap.x[5],Cap.x[29]],[Cap.y[5],Cap.y[29]]]
        CE23ln = [numpy.mean([Cap.x[5],Cap.x[29]]),\
                  numpy.mean([Cap.y[5],Cap.y[29]])]
        #離珠#
        C_E24 = [[Aql.x[10],Aql.x[15]],[Aql.y[10],Aql.y[15]],[Aql.x[10],Aqr.x[38]],[Aql.y[10],Aqr.y[38]],\
                 [Aql.x[15],Aql.x[16]],[Aql.y[15],Aql.y[16]]]
        CE24n = [numpy.mean([Aql.x[10],Aql.x[15],Aql.x[16],Aqr.x[38]]),\
                 numpy.mean([Aql.y[10],Aql.y[15],Aql.y[16],Aqr.y[38]])]
        #敗瓜#
        C_E25 = [[Del.x[2],Del.x[10]],[Del.y[2],Del.y[10]],[Del.x[2],Del.x[11]],[Del.y[2],Del.y[11]],\
                 [Del.x[7],Del.x[11]],[Del.y[7],Del.y[11]],[Del.x[10],Del.x[16]],[Del.y[10],Del.y[16]],\
                 [Del.x[11],Del.x[16]],[Del.y[11],Del.y[16]]]
        CE25n = [numpy.mean([Del.x[2],Del.x[7],Del.x[10],Del.x[11],Del.x[16]]),\
                 numpy.mean([Del.y[2],Del.y[7],Del.y[10],Del.y[11],Del.y[16]])]
        #瓠瓜#
        C_E26 = [[Del.x[0],Del.x[1]],[Del.y[0],Del.y[1]],[Del.x[0],Del.x[4]],[Del.y[0],Del.y[4]],\
                 [Del.x[0],Del.x[5]],[Del.y[0],Del.y[5]],[Del.x[1],Del.x[3]],[Del.y[1],Del.y[3]],\
                 [Del.x[3],Del.x[4]],[Del.y[3],Del.y[4]]]
        CE26n = [numpy.mean([Del.x[0],Del.x[1],Del.x[3],Del.x[4],Del.x[5]]),\
                 numpy.mean([Del.y[0],Del.y[1],Del.y[3],Del.y[4],Del.y[5]])]
        #天津#
        C_E27 = [[Cyg.x[0],Cyg.x[10]],[Cyg.y[0],Cyg.y[10]],[Cyg.x[0],Cyg.x[12]],[Cyg.y[0],Cyg.y[12]],\
                 [Cyg.x[1],Cyg.x[2]],[Cyg.y[1],Cyg.y[2]],[Cyg.x[1],Cyg.x[3]],[Cyg.y[1],Cyg.y[3]],\
                 [Cyg.x[2],Cyg.x[5]],[Cyg.y[2],Cyg.y[5]],[Cyg.x[3],Cyg.x[10]],[Cyg.y[3],Cyg.y[10]],\
                 [Cyg.x[5],Cyg.x[22]],[Cyg.y[5],Cyg.y[22]],[Cyg.x[7],Cyg.x[12]],[Cyg.y[7],Cyg.y[12]],\
                 [Cyg.x[7],Cyg.x[22]],[Cyg.y[7],Cyg.y[22]]]
        CE27n = [numpy.mean([Cyg.x[0],Cyg.x[1],Cyg.x[2],Cyg.x[3],Cyg.x[5],Cyg.x[7],Cyg.x[10],Cyg.x[12],\
                             Cyg.x[22]]),\
                 numpy.mean([Cyg.y[0],Cyg.y[1],Cyg.y[2],Cyg.y[3],Cyg.y[5],Cyg.y[7],Cyg.y[10],Cyg.y[12],\
                             Cyg.y[22]])]
        #奚仲#
        C_E28 = [[Cyg.x[8],Cyg.x[9]],[Cyg.y[8],Cyg.y[9]],[Cyg.x[9],Cyg.x[23]],[Cyg.y[9],Cyg.y[23]],\
                 [Cyg.x[23],Cyg.x[135]],[Cyg.y[23],Cyg.y[135]]]
        CE28n = [numpy.mean([Cyg.x[8],Cyg.x[9],Cyg.x[23],Cyg.x[135]]),\
                 numpy.mean([Cyg.y[8],Cyg.y[9],Cyg.y[23],Cyg.y[135]])]
        #扶筐#
        C_E29 = [[Dra.x[20],Dra.x[36]],[Dra.y[20],Dra.y[36]],[Dra.x[20],Dra.x[80]],[Dra.y[20],Dra.y[80]],\
                 [Dra.x[22],Dra.x[36]],[Dra.y[22],Dra.y[36]],[Dra.x[22],Dra.x[42]],[Dra.y[22],Dra.y[42]],\
                 [Dra.x[63],Dra.x[72]],[Dra.y[63],Dra.y[72]],[Dra.x[72],Dra.x[80]],[Dra.y[72],Dra.y[80]]]
        CE29n = [numpy.mean([Dra.x[20],Dra.x[22],Dra.x[36],Dra.x[42],Dra.x[63],Dra.x[72],Dra.x[80]]),\
                 numpy.mean([Dra.y[20],Dra.y[22],Dra.y[36],Dra.y[42],Dra.y[63],Dra.y[72],Dra.y[80]])]
        #虛宿#
        C_E30 = [[Equ.x[0],Aqr.x[0]],[Equ.y[0],Aqr.y[0]]]
        CE30n = [numpy.mean([Equ.x[0],Aqr.x[0]]),\
                 numpy.mean([Equ.y[0],Aqr.y[0]])]
        #司命#
        C_E31 = [[Aqr.x[65],Aqr.x[126]],[Aqr.y[65],Aqr.y[126]]]
        CE31n = [numpy.mean([Aqr.x[65],Aqr.x[126]]),\
                 numpy.mean([Aqr.y[65],Aqr.y[126]])]
        #司祿#
        C_E32 = [[Aqr.x[36],Peg.x[63]],[Aqr.y[36],Peg.y[63]]]
        CE32n = [numpy.mean([Aqr.x[36],Peg.x[63]]),\
                 numpy.mean([Aqr.y[36],Peg.y[63]])]
        #司危#
        C_E33 = [[Equ.x[3],Equ.x[6]],[Equ.y[3],Equ.y[6]]]
        CE33n = [numpy.mean([Equ.x[3],Equ.x[6]]),\
                 numpy.mean([Equ.y[3],Equ.y[6]])]
        #司非#
        C_E34 = [[Equ.x[1],Equ.x[2]],[Equ.y[1],Equ.y[2]]]
        CE34n = [numpy.mean([Equ.x[1],Equ.x[2]]),\
                 numpy.mean([Equ.y[1],Equ.y[2]])]
        #哭#
        C_E35 = [[Cap.x[17],Aqr.x[52]],[Cap.y[17],Aqr.y[52]]]
        CE35n = [numpy.mean([Cap.x[17],Aqr.x[52]]),\
                 numpy.mean([Cap.y[17],Aqr.y[52]])]
        #泣#
        C_E36 = [[Aqr.x[10],Aqr.x[50]],[Aqr.y[10],Aqr.y[50]]]
        CE36n = [numpy.mean([Aqr.x[10],Aqr.x[50]]),\
                 numpy.mean([Aqr.y[10],Aqr.y[50]])]
        #天壘城#
        C_E37 = [[Aqr.x[20],Cap.x[26]],[Aqr.y[20],Cap.y[26]],[Aqr.x[20],Aqr.x[95]],[Aqr.y[20],Aqr.y[95]],\
                 [Aqr.x[23],Cap.x[18]],[Aqr.y[23],Cap.y[18]],[Aqr.x[53],Cap.x[26]],[Aqr.y[53],Cap.y[26]],\
                 [Aqr.x[53],Cap.x[30]],[Aqr.y[53],Cap.y[30]],[Aqr.x[66],Aqr.x[95]],[Aqr.y[66],Aqr.y[95]],\
                 [Cap.x[18],Cap.x[30]],[Cap.y[18],Cap.y[30]]]
        CE37n = [numpy.mean([Aqr.x[20],Aqr.x[23],Aqr.x[53],Aqr.x[66],Aqr.x[95],Cap.x[18],Cap.x[26],Cap.x[30]]),\
                 numpy.mean([Aqr.y[20],Aqr.y[23],Aqr.y[53],Aqr.y[66],Aqr.y[95],Cap.y[18],Cap.y[26],Cap.y[30]])]
        #敗臼#
        C_E38 = [[Gru.x[2],Gru.x[9]],[Gru.y[2],Gru.y[9]],[Gru.x[9],PsA.x[5]],[Gru.y[9],PsA.y[5]],\
                 [PsA.x[5],PsA.x[31]],[PsA.y[5],PsA.y[31]]]
        CE38n = [numpy.mean([Gru.x[2],Gru.x[9],PsA.x[5],PsA.x[31]]),\
                 numpy.mean([Gru.y[2],Gru.y[9],PsA.y[5],PsA.y[31]])]
        #離瑜#
        C_E39 = []
        CE39n = [Mic.x[1],Mic.y[1]]
        #危宿#
        C_E40 = [[Aqr.x[1],Peg.x[7]],[Aqr.y[1],Peg.y[7]],[Peg.x[0],Peg.x[7]],[Peg.y[0],Peg.y[7]]]
        CE40n = [numpy.mean([Aqr.x[1],Peg.x[0],Peg.x[7]]),\
                 numpy.mean([Aqr.y[1],Peg.y[0],Peg.y[7]])]
        #墳墓#
        C_E41 = [[Aqr.x[6],Aqr.x[17]],[Aqr.y[6],Aqr.y[17]],[Aqr.x[9],Aqr.x[17]],[Aqr.y[9],Aqr.y[17]],\
                 [Aqr.x[17],Aqr.x[22]],[Aqr.y[17],Aqr.y[22]]]
        CE41n = [numpy.mean([Aqr.x[6],Aqr.x[9],Aqr.x[17],Aqr.x[22]]),\
                 numpy.mean([Aqr.y[6],Aqr.y[9],Aqr.y[17],Aqr.y[22]])]
        #人#
        C_E42 = [[Peg.x[10],Peg.x[14]],[Peg.y[10],Peg.y[14]],[Peg.x[10],Peg.x[18]],[Peg.y[10],Peg.y[18]],\
                 [Peg.x[14],Peg.x[39]],[Peg.y[14],Peg.y[39]]]
        CE42n = [numpy.mean([Peg.x[10],Peg.x[14],Peg.x[18],Peg.x[39]]),\
                 numpy.mean([Peg.y[10],Peg.y[14],Peg.y[18],Peg.y[39]])]
        #杵#
        C_E43 = [[Lac.x[1],Peg.x[13]],[Lac.y[1],Peg.y[13]],[Peg.x[13],Peg.x[69]],[Peg.y[13],Peg.y[69]]]
        CE43n = [numpy.mean([Lac.x[1],Peg.x[13],Peg.x[69]]),\
                 numpy.mean([Lac.y[1],Peg.y[13],Peg.y[69]])]
        #臼#
        C_E44 = [[Cyg.x[29],Peg.x[11]],[Cyg.y[29],Peg.y[11]],[Peg.x[8],Peg.x[11]],[Peg.y[8],Peg.y[11]],\
                 [Peg.x[8],Peg.x[25]],[Peg.y[8],Peg.y[25]]]
        CE44n = [numpy.mean([Cyg.x[29],Peg.x[8],Peg.x[11],Peg.x[25]]),\
                 numpy.mean([Cyg.y[29],Peg.y[8],Peg.y[11],Peg.y[25]])]
        #車府#
        C_E45 = [[Cyg.x[6],Cyg.x[31]],[Cyg.y[6],Cyg.y[31]],[Cyg.x[6],Cyg.x[48]],[Cyg.y[6],Cyg.y[48]],\
                 [Cyg.x[15],Cyg.x[31]],[Cyg.y[15],Cyg.y[31]],[Cyg.x[15],Lac.x[7]],[Cyg.y[15],Lac.y[7]],\
                 [Lac.x[4],Lac.x[7]],[Lac.y[4],Lac.y[7]],[Lac.x[4],Lac.x[11]],[Lac.y[4],Lac.y[11]]]
        CE45n = [numpy.mean([Cyg.x[6],Cyg.x[15],Cyg.x[31],Cyg.x[48],Lac.x[4],Lac.x[7],Lac.x[11]]),\
                 numpy.mean([Cyg.y[6],Cyg.y[15],Cyg.y[31],Cyg.y[48],Lac.y[4],Lac.y[7],Lac.y[11]])]
        #天鉤#
        C_E46 = [[Cep.x[0],Cep.x[4]],[Cep.y[0],Cep.y[4]],[Cep.x[0],Cep.x[12]],[Cep.y[0],Cep.y[12]],\
                 [Cep.x[4],Cep.x[9]],[Cep.y[4],Cep.y[9]],[Cep.x[5],Cep.x[35]],[Cep.y[5],Cep.y[35]],\
                 [Cep.x[5],Cep.x[44]],[Cep.y[5],Cep.y[44]],[Cep.x[9],Cep.x[55]],[Cep.y[9],Cep.y[55]],\
                 [Cep.x[12],Cep.x[44]],[Cep.y[12],Cep.y[44]],[Cep.x[20],Cep.x[35]],[Cep.y[20],Cep.y[35]]]
        CE46n = [numpy.mean([Cep.x[0],Cep.x[4],Cep.x[5],Cep.x[9],Cep.x[12],Cep.x[20],Cep.x[35],Cep.x[44],\
                             Cep.x[55]]),\
                 numpy.mean([Cep.y[0],Cep.y[4],Cep.y[5],Cep.y[9],Cep.y[12],Cep.y[20],Cep.y[35],Cep.y[44],\
                             Cep.y[55]])]
        #造父#
        C_E47 = [[Cep.x[3],Cep.x[6]],[Cep.y[3],Cep.y[6]],[Cep.x[3],Cep.x[24]],[Cep.y[3],Cep.y[24]],\
                 [Cep.x[7],Cep.x[11]],[Cep.y[7],Cep.y[11]],[Cep.x[7],Cep.x[24]],[Cep.y[7],Cep.y[24]]]
        CE47n = [numpy.mean([Cep.x[3],Cep.x[6],Cep.x[7],Cep.x[11],Cep.x[24]]),\
                 numpy.mean([Cep.y[3],Cep.y[6],Cep.y[7],Cep.y[11],Cep.y[24]])]
        #蓋屋#
        C_E48 = [[Aqr.x[24],Aqr.x[46]],[Aqr.y[24],Aqr.y[46]]]
        CE48n = [numpy.mean([Aqr.x[24],Aqr.x[46]]),\
                 numpy.mean([Aqr.y[24],Aqr.y[46]])]
        #虛梁#
        C_E49 = [[Aqr.x[33],Aqr.x[68]],[Aqr.y[33],Aqr.y[68]],[Aqr.x[33],Aqr.x[75]],[Aqr.y[33],Aqr.y[75]],\
                 [Aqr.x[71],Aqr.x[75]],[Aqr.y[71],Aqr.y[75]]]
        CE49n = [numpy.mean([Aqr.x[33],Aqr.x[68],Aqr.x[71],Aqr.x[75]]),\
                 numpy.mean([Aqr.y[33],Aqr.y[68],Aqr.y[71],Aqr.y[75]])]
        #天錢#
        C_E50 = [[PsA.x[4],PsA.x[6]],[PsA.y[4],PsA.y[6]],[PsA.x[4],PsA.x[9]],[PsA.y[4],PsA.y[9]],\
                 [PsA.x[6],PsA.x[7]],[PsA.y[6],PsA.y[7]],[PsA.x[7],PsA.x[9]],[PsA.y[7],PsA.y[9]]]
        CE50n = [numpy.mean([PsA.x[4],PsA.x[6],PsA.x[7],PsA.x[9]]),\
                 numpy.mean([PsA.y[4],PsA.y[6],PsA.y[7],PsA.y[9]])]
        #室宿#
        C_E51 = [[Peg.x[1],Peg.x[2]],[Peg.y[1],Peg.y[2]]]
        CE51n = [numpy.mean([Peg.x[1],Peg.x[2]]),\
                 numpy.mean([Peg.y[1],Peg.y[2]])]
        #離宮#
        C_E52 = [[Peg.x[4],Peg.x[23]],[Peg.y[4],Peg.y[23]],[Peg.x[6],Peg.x[9]],[Peg.y[6],Peg.y[9]],\
                 [Peg.x[15],Peg.x[19]],[Peg.y[15],Peg.y[19]]]
        CE52n = [numpy.mean([Peg.x[4],Peg.x[6],Peg.x[9],Peg.x[15],Peg.x[19],Peg.x[23]]),\
                 numpy.mean([Peg.y[4],Peg.y[6],Peg.y[9],Peg.y[15],Peg.y[19],Peg.y[23]])]
        #雷電#
        C_E53 = [[Peg.x[5],Peg.x[12]],[Peg.y[5],Peg.y[12]],[Peg.x[12],Peg.x[37]],[Peg.y[12],Peg.y[37]],\
                 [Peg.x[16],Peg.x[34]],[Peg.y[16],Peg.y[34]],[Peg.x[16],Peg.x[37]],[Peg.y[16],Peg.y[37]],\
                 [Peg.x[17],Peg.x[34]],[Peg.y[17],Peg.y[34]]]
        CE53n = [numpy.mean([Peg.x[5],Peg.x[12],Peg.x[16],Peg.x[17],Peg.x[34],Peg.x[37]]),\
                 numpy.mean([Peg.y[5],Peg.y[12],Peg.y[16],Peg.y[17],Peg.y[34],Peg.y[37]])]
        #壘壁陣#
        C_E54 = [[Aqr.x[4],Aqr.x[12]],[Aqr.y[4],Aqr.y[12]],[Aqr.x[4],Aqr.x[29]],[Aqr.y[4],Aqr.y[29]],\
                 [Aqr.x[13],Aqr.x[29]],[Aqr.y[13],Aqr.y[29]],[Aqr.x[12],Psc.x[20]],[Aqr.y[12],Psc.y[20]],\
                 [Cap.x[0],Aqr.x[13]],[Cap.y[0],Aqr.y[13]],[Cap.x[0],Cap.x[3]],[Cap.y[0],Cap.y[3]],\
                 [Cap.x[0],Cap.x[13]],[Cap.y[0],Cap.y[13]],[Cap.x[3],Cap.x[12]],[Cap.y[3],Cap.y[12]],\
                 [Cap.x[12],Cap.x[13]],[Cap.y[12],Cap.y[13]],[Psc.x[8],Psc.x[14]],[Psc.y[8],Psc.y[14]],\
                 [Psc.x[8],Psc.x[20]],[Psc.y[8],Psc.y[20]],[Psc.x[14],Psc.x[26]],[Psc.y[14],Psc.y[26]],\
                 [Psc.x[20],Psc.x[26]],[Psc.y[20],Psc.y[26]]]
        CE54n = [numpy.mean([Aqr.x[4],Aqr.x[12],Aqr.x[13],Aqr.x[29],Cap.x[0],Cap.x[3],Cap.x[12],Cap.x[13],\
                             Psc.x[8],Psc.x[14],Psc.x[20],Psc.x[26]]),\
                 numpy.mean([Aqr.y[4],Aqr.y[12],Aqr.y[13],Aqr.y[29],Cap.y[0],Cap.y[3],Cap.y[12],Cap.y[13],\
                             Psc.y[8],Psc.y[14],Psc.y[20],Psc.y[26]])]
        #羽林軍#
        C_E55 = [[Aqr.x[2],Aqr.x[61]],[Aqr.y[2],Aqr.y[61]],[Aqr.x[2],Aqr.x[64]],[Aqr.y[2],Aqr.y[64]],\
                 [Aqr.x[3],Aqr.x[26]],[Aqr.y[3],Aqr.y[26]],[Aqr.x[7],Aqr.x[41]],[Aqr.y[7],Aqr.y[41]],\
                 [Aqr.x[8],Aqr.x[77]],[Aqr.y[8],Aqr.y[77]],[Aqr.x[11],Aqr.x[14]],[Aqr.y[11],Aqr.y[14]],\
                 [Aqr.x[14],Aqr.x[31]],[Aqr.y[14],Aqr.y[31]],[Aqr.x[15],Aqr.x[134]],[Aqr.y[15],Aqr.y[134]],\
                 [Aqr.x[18],Aqr.x[26]],[Aqr.y[18],Aqr.y[26]],[Aqr.x[19],Aqr.x[32]],[Aqr.y[19],Aqr.y[32]],\
                 [Aqr.x[27],Aqr.x[134]],[Aqr.y[27],Aqr.y[134]],[Aqr.x[32],Aqr.x[34]],[Aqr.y[32],Aqr.y[34]],\
                 [Aqr.x[35],Aqr.x[41]],[Aqr.y[35],Aqr.y[41]],[Aqr.x[37],Aqr.x[56]],[Aqr.y[37],Aqr.y[56]],\
                 [Aqr.x[40],Aqr.x[43]],[Aqr.y[40],Aqr.y[43]],[Aqr.x[47],Aqr.x[78]],[Aqr.y[47],Aqr.y[78]],\
                 [Aqr.x[56],PsA.x[13]],[Aqr.y[56],PsA.y[13]],[Aqr.x[73],Aqr.x[90]],[Aqr.y[73],Aqr.y[90]],\
                 [Aqr.x[77],Aqr.x[114]],[Aqr.y[77],Aqr.y[114]],[PsA.x[1],PsA.x[25]],[PsA.y[1],PsA.y[25]]]
        CE55n = [numpy.mean([Aqr.x[2],Aqr.x[3],Aqr.x[7],Aqr.x[8],Aqr.x[11],Aqr.x[14],Aqr.x[15],Aqr.x[18],\
                             Aqr.x[19],Aqr.x[26],Aqr.x[27],Aqr.x[31],Aqr.x[32],Aqr.x[34],Aqr.x[35],Aqr.x[37],\
                             Aqr.x[40],Aqr.x[41],Aqr.x[43],Aqr.x[47],Aqr.x[56],Aqr.x[61],Aqr.x[64],Aqr.x[73],\
                             Aqr.x[77],Aqr.x[78],Aqr.x[90],Aqr.x[114],Aqr.x[134],PsA.x[1],PsA.x[13],PsA.x[25]]),\
                 numpy.mean([Aqr.y[2],Aqr.y[3],Aqr.y[7],Aqr.y[8],Aqr.y[11],Aqr.y[14],Aqr.y[15],Aqr.y[18],\
                             Aqr.y[19],Aqr.y[26],Aqr.y[27],Aqr.y[31],Aqr.y[32],Aqr.y[34],Aqr.y[35],Aqr.y[37],\
                             Aqr.y[40],Aqr.y[41],Aqr.y[43],Aqr.y[47],Aqr.y[56],Aqr.y[61],Aqr.y[64],Aqr.y[73],\
                             Aqr.y[77],Aqr.y[78],Aqr.y[90],Aqr.y[114],Aqr.y[134],PsA.y[1],PsA.y[13],PsA.y[25]])]
        #鈇鉞#
        C_E56 = [[Aqr.x[39],Aqr.x[42]],[Aqr.y[39],Aqr.y[42]],[Aqr.x[42],Aqr.x[49]],[Aqr.y[42],Aqr.y[49]]]
        CE56n = [numpy.mean([Aqr.x[39],Aqr.x[42],Aqr.x[49]]),\
                 numpy.mean([Aqr.y[39],Aqr.y[42],Aqr.y[49]])]
        #北落師門#
        C_E57 = []
        CE57n = [PsA.x[0],PsA.y[0]]
        #八魁#
        C_E58 = [[Cet.x[15],Cet.x[26]],[Cet.y[15],Cet.y[26]],[Cet.x[16],Cet.x[26]],[Cet.y[16],Cet.y[26]],\
                 [Cet.x[26],Cet.x[29]],[Cet.y[26],Cet.y[29]]]
        CE58n = [numpy.mean([Cet.x[15],Cet.x[16],Cet.x[26],Cet.x[29]]),\
                 numpy.mean([Cet.y[15],Cet.y[16],Cet.y[26],Cet.y[29]])]
        #天綱#
        C_E59 = []
        CE59n = [PsA.x[2],PsA.y[2]]
        #土公吏#
        C_E60 = [[Peg.x[30],Peg.x[59]],[Peg.y[30],Peg.y[59]]]
        CE60n = [numpy.mean([Peg.x[30],Peg.x[59]]),\
                 numpy.mean([Peg.y[30],Peg.y[59]])]
        #螣蛇#
        C_E61 = [[And.x[6],And.x[26]],[And.y[6],And.y[26]],[And.x[6],And.x[30]],[And.y[6],And.y[30]],\
                 [And.x[10],And.x[12]],[And.y[10],And.y[12]],[And.x[10],And.x[30]],[And.y[10],And.y[30]],\
                 [And.x[17],And.x[20]],[And.y[17],And.y[20]],[And.x[17],And.x[26]],[And.y[17],And.y[26]],\
                 [And.x[20],Lac.x[9]],[And.y[20],Lac.y[9]],[Cas.x[13],Cas.x[24]],[Cas.y[13],Cas.y[24]],\
                 [Cas.x[13],Cas.x[25]],[Cas.y[13],Cas.y[25]],[Cas.x[24],Cas.x[27]],[Cas.y[24],Cas.y[27]],\
                 [Cas.x[25],Lac.x[3]],[Cas.y[25],Lac.y[3]],[Cas.x[27],Lac.x[9]],[Cas.y[27],Lac.y[9]],\
                 [Cep.x[8],Lac.x[3]],[Cep.y[8],Lac.y[3]],[Cep.x[8],Cep.x[61]],[Cep.y[8],Cep.y[61]],\
                 [Cep.x[61],Cyg.x[27]],[Cep.y[61],Cyg.y[27]],[Cyg.x[19],Cyg.x[27]],[Cyg.y[19],Cyg.y[27]],\
                 [Cyg.x[19],Lac.x[8]],[Cyg.y[19],Lac.y[8]],[Lac.x[0],Lac.x[8]],[Lac.y[0],Lac.y[8]]]
        CE61n = [numpy.mean([And.x[6],And.x[10],And.x[12],And.x[17],And.x[20],And.x[26],And.x[30],Cas.x[13],\
                             Cas.x[24],Cas.x[25],Cas.x[27],Cep.x[8],Cep.x[61],Cyg.x[19],Cyg.x[27],Lac.x[0],\
                             Lac.x[3],Lac.x[8],Lac.x[9]]),\
                 numpy.mean([And.y[6],And.y[10],And.y[12],And.y[17],And.y[20],And.y[26],And.y[30],Cas.y[13],\
                             Cas.y[24],Cas.y[25],Cas.y[27],Cep.y[8],Cep.y[61],Cyg.y[19],Cyg.y[27],Lac.y[0],\
                             Lac.y[3],Lac.y[8],Lac.y[9]])]
        #壁宿#
        C_E62 = [[And.x[0],Peg.x[3]],[And.y[0],Peg.y[3]]]
        CE62n = [numpy.mean([And.x[0],Peg.x[3]]),\
                 numpy.mean([And.y[0],Peg.y[3]])]
        #霹靂#
        C_E63 = [[Psc.x[1],Psc.x[6]],[Psc.y[1],Psc.y[6]],[Psc.x[1],Psc.x[13]],[Psc.y[1],Psc.y[13]],\
                 [Psc.x[2],Psc.x[3]],[Psc.y[2],Psc.y[3]],[Psc.x[3],Psc.x[6]],[Psc.y[3],Psc.y[6]]]
        CE63n = [numpy.mean([Psc.x[1],Psc.x[2],Psc.x[3],Psc.x[6],Psc.x[13]]),\
                 numpy.mean([Psc.y[1],Psc.y[2],Psc.y[3],Psc.y[6],Psc.y[13]])]
        #雲雨#
        C_E64 = [[Psc.x[11],Psc.x[61]],[Psc.y[11],Psc.y[61]],[Psc.x[21],Psc.x[61]],[Psc.y[21],Psc.y[61]]]
        CE64n = [numpy.mean([Psc.x[11],Psc.x[21],Psc.x[61]]),\
                 numpy.mean([Psc.y[11],Psc.y[21],Psc.y[61]])]
        #天廄#
        C_E65 = [[And.x[16],And.x[37]],[And.y[16],And.y[37]],[And.x[19],And.x[37]],[And.y[19],And.y[37]]]
        CE65n = [numpy.mean([And.x[16],And.x[19],And.x[37]]),\
                 numpy.mean([And.y[16],And.y[19],And.y[37]])]
        #鈇鑕#
        C_E66 = [[Cet.x[9],Cet.x[24]],[Cet.y[9],Cet.y[24]],[Cet.x[9],Cet.x[34]],[Cet.y[9],Cet.y[34]]]
        CE66n = [numpy.mean([Cet.x[9],Cet.x[24],Cet.x[34]]),\
                 numpy.mean([Cet.y[9],Cet.y[24],Cet.y[34]])]
        #土公#
        C_E67 = []
        CE67n = [] # ???

        C_E_list = [C_E01,C_E02,C_E03,C_E04,C_E05,C_E06,C_E07,C_E08,C_E09,C_E10,\
                    C_E11,C_E12,C_E13,C_E14,C_E15,C_E16,C_E17,C_E18,C_E19,C_E20,\
                    C_E21,C_E22,C_E23,C_E23a,C_E23b,C_E23c,C_E23d,C_E23e,C_E23f,C_E23g,\
                    C_E23h,C_E23i,C_E23j,C_E23k,C_E23l,C_E24,C_E25,C_E26,C_E27,C_E28,\
                    C_E29,C_E30,C_E31,C_E32,C_E33,C_E34,C_E35,C_E36,C_E37,C_E38,\
                    C_E39,C_E40,C_E41,C_E42,C_E43,C_E44,C_E45,C_E46,C_E47,C_E48,\
                    C_E49,C_E50,C_E51,C_E52,C_E53,C_E54,C_E55,C_E56,C_E57,C_E58,\
                    C_E59,C_E60,C_E61,C_E62,C_E63,C_E64,C_E65,C_E66,C_E67]

        # 北宮玄武 linecollection
        C_E_line_z_xy1 = []
        C_E_line_z_xy2 = [] 
        C_E_line_xy1 = []
        C_E_line_xy2 = []        
        for i in range(len(C_E_list)):
            for j in range(len(C_E_list[i]))[0::2]:
                if math.hypot(C_E_list[i][j][0]-C_E_list[i][j][1],C_E_list[i][j+1][0]-C_E_list[i][j+1][1]) < hori_border:
                    if i in set([0,10,21,41,51,62,73]):
                        C_E_line_z_xy1.append((C_E_list[i][j][0],C_E_list[i][j+1][0]))
                        C_E_line_z_xy2.append((C_E_list[i][j][1],C_E_list[i][j+1][1]))
                    else:
                        C_E_line_xy1.append((C_E_list[i][j][0],C_E_list[i][j+1][0]))
                        C_E_line_xy2.append((C_E_list[i][j][1],C_E_list[i][j+1][1]))

        C_E_line_z_list = []
        for i in range(len(C_E_line_z_xy1)):            
            C_E_line_z_list.append([C_E_line_z_xy1[i],C_E_line_z_xy2[i]])
        
        C_E_line_list = []
        for i in range(len(C_E_line_xy1)):            
            C_E_line_list.append([C_E_line_xy1[i],C_E_line_xy2[i]])
        
        lc_C_E_z = mc.LineCollection(C_E_line_z_list, colors='yellow', zorder=2+2.5)
        lc_C_E = mc.LineCollection(C_E_line_list, colors='white', zorder=2+2.5)
        lc_C_E_z.set_alpha(plot_alpha)
        lc_C_E.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_E_z)
        ax0.add_collection(lc_C_E)

        CEn_list = [[CE01n,'斗宿'],[CE02n,'建'],[CE03n,'天弁'],[CE04n,'鱉'],[CE05n,'天雞'],\
                    [CE06n,'天籥'],[CE07n,'狗國'],[CE08n,'天淵'],[CE09n,'狗'],[CE10n,'農丈人'],\
                    [CE11n,'牛宿'],[CE12n,'天田'],[CE13n,'九坎'],[CE14n,'河鼓'],[CE15n,'織女'],\
                    [CE16n,'左旗'],[CE17n,'右旗'],[CE18n,'天桴'],[CE19n,'羅堰'],[CE20n,'漸臺'],\
                    [CE21n,'輦道'],[CE22n,'女宿'],[CE23n,'十二國'],[CE23an,'燕'],[CE23bn,'周'],\
                    [CE23cn,'晉'],[CE23dn,'魏'],[CE23en,'楚'],[CE23fn,'齊'],[CE23gn,'韓'],\
                    [CE23hn,'越'],[CE23in,'鄭'],[CE23jn,'趙'],[CE23kn,'代'],[CE23ln,'秦'],\
                    [CE24n,'離珠'],[CE25n,'敗瓜'],[CE26n,'瓠瓜'],[CE27n,'天津'],[CE28n,'奚仲'],\
                    [CE29n,'扶筐'],[CE30n,'虛宿'],[CE31n,'司命'],[CE32n,'司祿'],[CE33n,'司危'],\
                    [CE34n,'司非'],[CE35n,'哭'],[CE36n,'泣'],[CE37n,'天壘城'],[CE38n,'敗臼'],\
                    [CE39n,'離瑜'],[CE40n,'危宿'],[CE41n,'墳墓'],[CE42n,'人'],[CE43n,'杵'],\
                    [CE44n,'臼'],[CE45n,'車府'],[CE46n,'天鉤'],[CE47n,'造父'],[CE48n,'蓋屋'],\
                    [CE49n,'虛梁'],[CE50n,'天錢'],[CE51n,'室宿'],[CE52n,'離宮'],[CE53n,'雷電'],\
                    [CE54n,'壘壁陣'],[CE55n,'羽林軍'],[CE56n,'鈇鉞'],[CE57n,'北落師門'],[CE58n,'八魁'],\
                    [CE59n,'天綱'],[CE60n,'土公吏'],[CE61n,'螣蛇'],[CE62n,'壁宿'],[CE63n,'霹靂'],\
                    [CE64n,'雲雨'],[CE65n,'天廄'],[CE66n,'鈇鑕'],[CE67n,'土公']]

        for i in range(len(CEn_list)):
            if len(CEn_list[i][0]) != 0:
                if (CEn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CEn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CEn_list[i][0])-min(CEn_list[i][0]) < hori_border:
                    if i in set([0,10,21,41,51,62,73]):
                        ax_label.annotate(str(CEn_list[i][1]),(CEn_list[i][0][0],CEn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(CEn_list[i][1]),(CEn_list[i][0][0],CEn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #西宮白虎#
        ##########
        #奎宿#
        C_F01 = [[And.x[1],And.x[7]],[And.y[1],And.y[7]],[And.x[1],Psc.x[27]],[And.y[1],Psc.y[27]],\
                 [And.x[3],And.x[13]],[And.y[3],And.y[13]],[And.x[3],And.x[14]],[And.y[3],And.y[14]],\
                 [And.x[7],And.x[18]],[And.y[7],And.y[18]],[And.x[8],And.x[14]],[And.y[8],And.y[14]],\
                 [And.x[8],And.x[15]],[And.y[8],And.y[15]],[And.x[13],And.x[18]],[And.y[13],And.y[18]],\
                 [And.x[15],Psc.x[33]],[And.y[15],Psc.y[33]],[Psc.x[12],Psc.x[29]],[Psc.y[12],Psc.y[29]],\
                 [Psc.x[12],Psc.x[27]],[Psc.y[12],Psc.y[27]],[Psc.x[16],Psc.x[17]],[Psc.y[16],Psc.y[17]],\
                 [Psc.x[16],Psc.x[18]],[Psc.y[16],Psc.y[18]],[Psc.x[17],Psc.x[33]],[Psc.y[17],Psc.y[33]],\
                 [Psc.x[18],Psc.x[29]],[Psc.y[18],Psc.y[29]]]
        CF01n = [numpy.mean([And.x[1],And.x[3],And.x[7],And.x[8],And.x[13],And.x[14],And.x[15],And.x[18],\
                             Psc.x[12],Psc.x[16],Psc.x[17],Psc.x[18],Psc.x[27],Psc.x[29],Psc.x[33]]),\
                 numpy.mean([And.y[1],And.y[3],And.y[7],And.y[8],And.y[13],And.y[14],And.y[15],And.y[18],\
                             Psc.y[12],Psc.y[16],Psc.y[17],Psc.y[18],Psc.y[27],Psc.y[29],Psc.y[33]])]
        #外屏#
        C_F02 = [[Psc.x[5],Psc.x[9]],[Psc.y[5],Psc.y[9]],[Psc.x[5],Psc.x[31]],[Psc.y[5],Psc.y[31]],\
                 [Psc.x[7],Psc.x[15]],[Psc.y[7],Psc.y[15]],[Psc.x[10],Psc.x[15]],[Psc.y[10],Psc.y[15]],\
                 [Psc.x[10],Psc.x[19]],[Psc.y[10],Psc.y[19]],[Psc.x[19],Psc.x[31]],[Psc.y[19],Psc.y[31]]]
        CF02n = [numpy.mean([Psc.x[5],Psc.x[7],Psc.x[9],Psc.x[10],Psc.x[15],Psc.x[19],Psc.x[31]]),\
                 numpy.mean([Psc.y[5],Psc.y[7],Psc.y[9],Psc.y[10],Psc.y[15],Psc.y[19],Psc.y[31]])]
        #天溷#
        C_F03 = [[Cet.x[20],Cet.x[130]],[Cet.y[20],Cet.y[130]],[Cet.x[43],Cet.x[130]],[Cet.y[43],Cet.y[130]],\
                 [Cet.x[43],Cet.x[133]],[Cet.y[43],Cet.y[133]]]
        CF03n = [numpy.mean([Cet.x[20],Cet.x[43],Cet.x[130],Cet.x[133]]),\
                 numpy.mean([Cet.y[20],Cet.y[43],Cet.y[130],Cet.y[133]])]
        #土司空#
        C_F04 = []
        CF04n = [Cet.x[0],Cet.y[0]]
        #軍南門#
        C_F05 = []
        CF05n = [And.x[11],And.y[11]]
        #閣道#
        C_F06 = [[Cas.x[3],Cas.x[4]],[Cas.y[3],Cas.y[4]],[Cas.x[3],Cas.x[9]],[Cas.y[3],Cas.y[9]],\
                 [Cas.x[4],Cas.x[10]],[Cas.y[4],Cas.y[10]],[Cas.x[9],Cas.x[26]],[Cas.y[9],Cas.y[26]],\
                 [Cas.x[11],Cas.x[26]],[Cas.y[11],Cas.y[26]]]
        CF06n = [numpy.mean([Cas.x[3],Cas.x[4],Cas.x[9],Cas.x[10],Cas.x[11],Cas.x[26]]),\
                 numpy.mean([Cas.y[3],Cas.y[4],Cas.y[9],Cas.y[10],Cas.y[11],Cas.y[26]])]
        #附路#
        C_F07 = []
        CF07n = [Cas.x[6],Cas.y[6]]
        #王良#
        C_F08 = [[Cas.x[0],Cas.x[5]],[Cas.y[0],Cas.y[5]],[Cas.x[0],Cas.x[16]],[Cas.y[0],Cas.y[16]],\
                 [Cas.x[1],Cas.x[8]],[Cas.y[1],Cas.y[8]],[Cas.x[5],Cas.x[8]],[Cas.y[5],Cas.y[8]]]
        CF08n = [numpy.mean([Cas.x[0],Cas.x[1],Cas.x[5],Cas.x[8],Cas.x[16]]),\
                 numpy.mean([Cas.y[0],Cas.y[1],Cas.y[5],Cas.y[8],Cas.y[16]])]
        #策#
        C_F09 = []
        CF09n = [Cas.x[2],Cas.y[2]]
        #婁宿#
        C_F10 = [[Ari.x[0],Ari.x[1]],[Ari.y[0],Ari.y[1]],[Ari.x[1],Ari.x[9]],[Ari.y[1],Ari.y[9]]]
        CF10n = [numpy.mean([Ari.x[0],Ari.x[1],Ari.x[9]]),\
                 numpy.mean([Ari.y[0],Ari.y[1],Ari.y[9]])]
        #左更#
        C_F11 = [[Ari.x[18],Ari.x[24]],[Ari.y[18],Ari.y[24]],[Ari.x[22],Ari.x[34]],[Ari.y[22],Ari.y[34]],\
                 [Ari.x[24],Ari.x[39]],[Ari.y[24],Ari.y[39]],[Ari.x[34],Ari.x[39]],[Ari.y[34],Ari.y[39]]]
        CF11n = [numpy.mean([Ari.x[18],Ari.x[22],Ari.x[24],Ari.x[34],Ari.x[39]]),\
                 numpy.mean([Ari.y[18],Ari.y[22],Ari.y[24],Ari.y[34],Ari.y[39]])]
        #右更#
        C_F12 = [[Psc.x[0],Psc.x[45]],[Psc.y[0],Psc.y[45]],[Psc.x[0],Psc.x[52]],[Psc.y[0],Psc.y[52]],\
                 [Psc.x[4],Psc.x[52]],[Psc.y[4],Psc.y[52]]]
        CF12n = [numpy.mean([Psc.x[0],Psc.x[4],Psc.x[45],Psc.x[52]]),\
                 numpy.mean([Psc.y[0],Psc.y[4],Psc.y[45],Psc.y[52]])]
        #天倉#
        C_F13 = [[Cet.x[3],Cet.x[6]],[Cet.y[3],Cet.y[6]],[Cet.x[3],Cet.x[7]],[Cet.y[3],Cet.y[7]],\
                 [Cet.x[5],Cet.x[8]],[Cet.y[5],Cet.y[8]],[Cet.x[5],Cet.x[48]],[Cet.y[5],Cet.y[48]],\
                 [Cet.x[7],Cet.x[8]],[Cet.y[7],Cet.y[8]]]
        CF13n = [numpy.mean([Cet.x[3],Cet.x[5],Cet.x[6],Cet.x[7],Cet.x[8],Cet.x[48]]),\
                 numpy.mean([Cet.y[3],Cet.y[5],Cet.y[6],Cet.y[7],Cet.y[8],Cet.y[48]])]
        #天庾#
        C_F14 = []
        CF14n = [For.x[1],For.y[1]]
        #天大將軍#
        C_F15 = [[And.x[2],Per.x[15]],[And.y[2],Per.y[15]],[And.x[2],Tri.x[3]],[And.y[2],Tri.y[3]],\
                 [And.x[4],And.x[41]],[And.y[4],And.y[41]],[And.x[4],Per.x[15]],[And.y[4],Per.y[15]],\
                 [And.x[9],And.x[28]],[And.y[9],And.y[28]],[And.x[9],And.x[31]],[And.y[9],And.y[31]],\
                 [And.x[28],And.x[57]],[And.y[28],And.y[57]],[And.x[31],And.x[41]],[And.y[31],And.y[41]],\
                 [And.x[57],Tri.x[0]],[And.y[57],Tri.y[0]],[Tri.x[0],Tri.x[2]],[Tri.y[0],Tri.y[2]],\
                 [Tri.x[2],Tri.x[3]],[Tri.y[2],Tri.y[3]]]
        CF15n = [numpy.mean([And.x[2],And.x[4],And.x[9],And.x[28],And.x[31],And.x[41],And.x[57],Per.x[15],\
                             Tri.x[0],Tri.x[2],Tri.x[3]]),\
                 numpy.mean([And.y[2],And.y[4],And.y[9],And.y[28],And.y[31],And.y[41],And.y[57],Per.y[15],\
                             Tri.y[0],Tri.y[2],Tri.y[3]])]
        #胃宿#
        C_F16 = [[Ari.x[2],Ari.x[5]],[Ari.y[2],Ari.y[5]],[Ari.x[5],Ari.x[8]],[Ari.y[5],Ari.y[8]]]
        CF16n = [numpy.mean([Ari.x[2],Ari.x[5],Ari.x[8]]),\
                 numpy.mean([Ari.y[2],Ari.y[5],Ari.y[8]])]
        #天廩#
        C_F17 = [[Tau.x[7],Tau.x[11]],[Tau.y[7],Tau.y[11]],[Tau.x[11],Tau.x[55]],[Tau.y[11],Tau.y[55]],\
                 [Tau.x[16],Tau.x[55]],[Tau.y[16],Tau.y[55]]]
        CF17n = [numpy.mean([Tau.x[7],Tau.x[11],Tau.x[16],Tau.x[55]]),\
                 numpy.mean([Tau.y[7],Tau.y[11],Tau.y[16],Tau.y[55]])]
        #天囷#
        C_F18 = [[Cet.x[1],Cet.x[74]],[Cet.y[1],Cet.y[74]],[Cet.x[4],Cet.x[10]],[Cet.y[4],Cet.y[10]],\
                 [Cet.x[4],Cet.x[25]],[Cet.y[4],Cet.y[25]],[Cet.x[10],Cet.x[45]],[Cet.y[10],Cet.y[45]],\
                 [Cet.x[12],Cet.x[14]],[Cet.y[12],Cet.y[14]],[Cet.x[12],Cet.x[18]],[Cet.y[12],Cet.y[18]],\
                 [Cet.x[13],Cet.x[14]],[Cet.y[13],Cet.y[14]],[Cet.x[13],Cet.x[25]],[Cet.y[13],Cet.y[25]],\
                 [Cet.x[18],Cet.x[74]],[Cet.y[18],Cet.y[74]],[Cet.x[45],Cet.x[50]],[Cet.y[45],Cet.y[50]],\
                 [Cet.x[50],Cet.x[102]],[Cet.y[50],Cet.y[102]],[Cet.x[59],Cet.x[102]],[Cet.y[59],Cet.y[102]]]
        CF18n = [numpy.mean([Cet.x[1],Cet.x[4],Cet.x[10],Cet.x[12],Cet.x[13],Cet.x[14],Cet.x[18],Cet.x[25],\
                             Cet.x[45],Cet.x[50],Cet.x[59],Cet.x[74],Cet.x[102]]),\
                 numpy.mean([Cet.y[1],Cet.y[4],Cet.y[10],Cet.y[12],Cet.y[13],Cet.y[14],Cet.y[18],Cet.y[25],\
                             Cet.y[45],Cet.y[50],Cet.y[59],Cet.y[74],Cet.y[102]])]
        #大陵#
        C_F19 = [[Per.x[1],Per.x[6]],[Per.y[1],Per.y[6]],[Per.x[1],Per.x[9]],[Per.y[1],Per.y[9]],\
                 [Per.x[6],Per.x[18]],[Per.y[6],Per.y[18]],[Per.x[9],Per.x[14]],[Per.y[9],Per.y[14]],\
                 [Per.x[11],Per.x[14]],[Per.y[11],Per.y[14]],[Per.x[11],Per.x[44]],[Per.y[11],Per.y[44]],\
                 [Per.x[18],Per.x[32]],[Per.y[18],Per.y[32]]]
        CF19n = [numpy.mean([Per.x[1],Per.x[6],Per.x[9],Per.x[11],Per.x[14],Per.x[18],Per.x[32],Per.x[44]]),\
                 numpy.mean([Per.y[1],Per.y[6],Per.y[9],Per.y[11],Per.y[14],Per.y[18],Per.y[32],Per.y[44]])]
        #天船#
        C_F20 = [[Cam.x[23],Per.x[24]],[Cam.y[23],Per.y[24]],[Per.x[0],Per.x[4]],[Per.y[0],Per.y[4]],\
                 [Per.x[0],Per.x[19]],[Per.y[0],Per.y[19]],[Per.x[4],Per.x[7]],[Per.y[4],Per.y[7]],\
                 [Per.x[5],Per.x[13]],[Per.y[5],Per.y[13]],[Per.x[5],Per.x[19]],[Per.y[5],Per.y[19]],\
                 [Per.x[13],Per.x[17]],[Per.y[13],Per.y[17]],[Per.x[17],Per.x[24]],[Per.y[17],Per.y[24]]]
        CF20n = [numpy.mean([Cam.x[23],Per.x[0],Per.x[4],Per.x[5],Per.x[7],Per.x[13],Per.x[17],Per.x[19],\
                             Per.x[24]]),\
                 numpy.mean([Cam.y[23],Per.y[0],Per.y[4],Per.y[5],Per.y[7],Per.y[13],Per.y[17],Per.y[19],\
                             Per.y[24]])]
        #積尸#
        C_F21 = []
        CF21n = [Per.x[27],Per.y[27]]
        #積水#
        C_F22 = []
        CF22n = [Per.x[21],Per.y[21]]
        #昴宿#
        C_F23 = []
        CF23n = [numpy.mean([Tau.x[2],Tau.x[8],Tau.x[10],Tau.x[14],Tau.x[17],Tau.x[26],Tau.x[52]]),\
                 numpy.mean([Tau.y[2],Tau.y[8],Tau.y[10],Tau.y[14],Tau.y[17],Tau.y[26],Tau.y[52]])]
        #天阿#
        C_F24 = []
        CF24n = [Ari.x[27],Ari.y[27]]
        #月#
        C_F25 = []
        CF25n = [Tau.x[27],Tau.y[27]]
        #天陰#
        C_F26 = [[Ari.x[3],Ari.x[15]],[Ari.y[3],Ari.y[15]],[Ari.x[12],Ari.x[15]],[Ari.y[12],Ari.y[15]]]
        CF26n = [numpy.mean([Ari.x[3],Ari.x[12],Ari.x[15]]),\
                 numpy.mean([Ari.y[3],Ari.y[12],Ari.y[15]])]
        #芻蒿#
        C_F27 = [[Cet.x[23],Cet.x[57]],[Cet.y[23],Cet.y[57]],[Cet.x[27],Cet.x[81]],[Cet.y[27],Cet.y[81]],\
                 [Cet.x[57],Cet.x[81]],[Cet.y[57],Cet.y[81]]]
        CF27n = [numpy.mean([Cet.x[23],Cet.x[27],Cet.x[57],Cet.x[81]]),\
                 numpy.mean([Cet.y[23],Cet.y[27],Cet.y[57],Cet.y[81]])]
        #天苑#
        C_F28 = [[Cet.x[11],Eri.x[12]],[Cet.y[11],Eri.y[12]],[Cet.x[11],Eri.x[30]],[Cet.y[11],Eri.y[30]],\
                 [Eri.x[2],Eri.x[28]],[Eri.y[2],Eri.y[28]],[Eri.x[4],Eri.x[9]],[Eri.y[4],Eri.y[9]],\
                 [Eri.x[4],Eri.x[28]],[Eri.y[4],Eri.y[28]],[Eri.x[7],Eri.x[17]],[Eri.y[7],Eri.y[17]],\
                 [Eri.x[7],Eri.x[23]],[Eri.y[7],Eri.y[23]],[Eri.x[9],Eri.x[42]],[Eri.y[9],Eri.y[42]],\
                 [Eri.x[12],Eri.x[42]],[Eri.y[12],Eri.y[42]],[Eri.x[17],Eri.x[39]],[Eri.y[17],Eri.y[39]],\
                 [Eri.x[20],Eri.x[23]],[Eri.y[20],Eri.y[23]],[Eri.x[20],Eri.x[59]],[Eri.y[20],Eri.y[59]],\
                 [Eri.x[30],Eri.x[39]],[Eri.y[30],Eri.y[39]],[Eri.x[34],Eri.x[35]],[Eri.y[34],Eri.y[35]],\
                 [Eri.x[34],Eri.x[59]],[Eri.y[34],Eri.y[59]]]
        CF28n = [numpy.mean([Cet.x[11],Eri.x[2],Eri.x[4],Eri.x[7],Eri.x[9],Eri.x[12],Eri.x[17],Eri.x[20],\
                             Eri.x[23],Eri.x[28],Eri.x[30],Eri.x[34],Eri.x[35],Eri.x[39],Eri.x[42],Eri.x[59]]),\
                 numpy.mean([Cet.y[11],Eri.y[2],Eri.y[4],Eri.y[7],Eri.y[9],Eri.y[12],Eri.y[17],Eri.y[20],\
                             Eri.y[23],Eri.y[28],Eri.y[30],Eri.y[34],Eri.y[35],Eri.y[39],Eri.y[42],Eri.y[59]])]
        #卷舌#
        C_F29 = [[Per.x[2],Per.x[10]],[Per.y[2],Per.y[10]],[Per.x[2],Per.x[12]],[Per.y[2],Per.y[12]],\
                 [Per.x[3],Per.x[8]],[Per.y[3],Per.y[8]],[Per.x[3],Per.x[12]],[Per.y[3],Per.y[12]],\
                 [Per.x[10],Per.x[36]],[Per.y[10],Per.y[36]]]
        CF29n = [numpy.mean([Per.x[2],Per.x[3],Per.x[8],Per.x[10],Per.x[12],Per.x[36]]),\
                 numpy.mean([Per.y[2],Per.y[3],Per.y[8],Per.y[10],Per.y[12],Per.y[36]])]
        #天讒#
        C_F30 = []
        CF30n = [Per.x[42],Per.y[42]]
        #礪石#
        C_F31 = [[Tau.x[45],Tau.x[71]],[Tau.y[45],Tau.y[71]],[Tau.x[59],Tau.x[76]],[Tau.y[59],Tau.y[76]],\
                 [Tau.x[71],Tau.x[76]],[Tau.y[71],Tau.y[76]]]
        CF31n = [numpy.mean([Tau.x[45],Tau.x[59],Tau.x[71],Tau.x[76]]),\
                 numpy.mean([Tau.y[45],Tau.y[59],Tau.y[71],Tau.y[76]])]
        #畢宿#
        C_F32 = [[Tau.x[0],Tau.x[4]],[Tau.y[0],Tau.y[4]],[Tau.x[4],Tau.x[29]],[Tau.y[4],Tau.y[29]],\
                 [Tau.x[5],Tau.x[9]],[Tau.y[5],Tau.y[9]],[Tau.x[6],Tau.x[25]],[Tau.y[6],Tau.y[25]],\
                 [Tau.x[9],Tau.x[12]],[Tau.y[9],Tau.y[12]],[Tau.x[9],Tau.x[29]],[Tau.y[9],Tau.y[29]],\
                 [Tau.x[12],Tau.x[25]],[Tau.y[12],Tau.y[25]]]
        CF32n = [numpy.mean([Tau.x[0],Tau.x[4],Tau.x[5],Tau.x[6],Tau.x[9],Tau.x[12],Tau.x[25],Tau.x[29]]),\
                 numpy.mean([Tau.y[0],Tau.y[4],Tau.y[5],Tau.y[6],Tau.y[9],Tau.y[12],Tau.y[25],Tau.y[29]])]
        #附耳#
        C_F33 = []
        CF33n = [Tau.x[34],Tau.y[34]]
        #天街#
        C_F34 = [[Tau.x[18],Tau.x[43]],[Tau.y[18],Tau.y[43]]]
        CF34n = [numpy.mean([Tau.x[18],Tau.x[43]]),\
                 numpy.mean([Tau.y[18],Tau.y[43]])]
        #天節#
        C_F35 = [[Tau.x[19],Tau.x[54]],[Tau.y[19],Tau.y[54]],[Tau.x[19],Tau.x[81]],[Tau.y[19],Tau.y[81]],\
                 [Tau.x[20],Tau.x[49]],[Tau.y[20],Tau.y[49]],[Tau.x[20],Tau.x[81]],[Tau.y[20],Tau.y[81]],\
                 [Tau.x[32],Tau.x[33]],[Tau.y[32],Tau.y[33]],[Tau.x[33],Tau.x[98]],[Tau.y[33],Tau.y[98]],\
                 [Tau.x[49],Tau.x[98]],[Tau.y[49],Tau.y[98]]]
        CF35n = [numpy.mean([Tau.x[19],Tau.x[20],Tau.x[32],Tau.x[33],Tau.x[49],Tau.x[54],Tau.x[81],Tau.x[98]]),\
                 numpy.mean([Tau.y[19],Tau.y[20],Tau.y[32],Tau.y[33],Tau.y[49],Tau.y[54],Tau.y[81],Tau.y[98]])]
        #諸王#
        C_F36 = [[Tau.x[23],Tau.x[120]],[Tau.y[23],Tau.y[120]],[Tau.x[30],Tau.x[56]],[Tau.y[30],Tau.y[56]],\
                 [Tau.x[56],Tau.x[84]],[Tau.y[56],Tau.y[84]],[Tau.x[84],Tau.x[89]],[Tau.y[84],Tau.y[89]],\
                 [Tau.x[89],Tau.x[120]],[Tau.y[89],Tau.y[120]]]
        CF36n = [numpy.mean([Tau.x[23],Tau.x[30],Tau.x[56],Tau.x[84],Tau.x[89],Tau.x[120]]),\
                 numpy.mean([Tau.y[23],Tau.y[30],Tau.y[56],Tau.y[84],Tau.y[89],Tau.y[120]])]
        #天高#
        C_F37 = [[Tau.x[31],Tau.x[44]],[Tau.y[31],Tau.y[44]],[Tau.x[31],Tau.x[53]],[Tau.y[31],Tau.y[53]],\
                 [Tau.x[44],Tau.x[53]],[Tau.y[44],Tau.y[53]]]
        CF37n = [numpy.mean([Tau.x[31],Tau.x[44],Tau.x[53]]),\
                 numpy.mean([Tau.y[31],Tau.y[44],Tau.y[53]])]
        #九州殊口#
        C_F38 = [[Eri.x[13],Eri.x[55]],[Eri.y[13],Eri.y[55]],[Eri.x[13],Eri.x[118]],[Eri.y[13],Eri.y[118]],\
                 [Eri.x[16],Eri.x[44]],[Eri.y[16],Eri.y[44]],[Eri.x[16],Eri.x[55]],[Eri.y[16],Eri.y[55]]]
        CF38n = [numpy.mean([Eri.x[13],Eri.x[16],Eri.x[44],Eri.x[55],Eri.x[118]]),\
                 numpy.mean([Eri.y[13],Eri.y[16],Eri.y[44],Eri.y[55],Eri.y[118]])]
        #五車#
        C_F39 = [[Aur.x[0],Aur.x[1]],[Aur.y[0],Aur.y[1]],[Aur.x[0],Aur.x[3]],[Aur.y[0],Aur.y[3]],\
                 [Aur.x[1],Aur.x[2]],[Aur.y[1],Aur.y[2]],[Aur.x[2],Tau.x[1]],[Aur.y[2],Tau.y[1]]]
        CF39n = [numpy.mean([Aur.x[0],Aur.x[1],Aur.x[2],Aur.x[3],Tau.x[1]]),\
                 numpy.mean([Aur.y[0],Aur.y[1],Aur.y[2],Aur.y[3],Tau.y[1]])]
        #柱#
        C_F40 = [[Aur.x[4],Aur.x[5]],[Aur.y[4],Aur.y[5]],[Aur.x[4],Aur.x[7]],[Aur.y[4],Aur.y[7]],\
                 [Aur.x[8],Aur.x[11]],[Aur.y[8],Aur.y[11]],[Aur.x[8],Aur.x[14]],[Aur.y[8],Aur.y[14]],\
                 [Aur.x[15],Aur.x[41]],[Aur.y[15],Aur.y[41]]]
        CF40an = [numpy.mean([Aur.x[4],Aur.x[5],Aur.x[7]]),\
                  numpy.mean([Aur.y[4],Aur.y[5],Aur.y[7]])]
        CF40bn = [numpy.mean([Aur.x[8],Aur.x[11],Aur.x[14]]),\
                  numpy.mean([Aur.y[8],Aur.y[11],Aur.y[14]])]
        CF40cn = [numpy.mean([Aur.x[15],Aur.x[41]]),\
                  numpy.mean([Aur.y[15],Aur.y[41]])]
        #天潢#
        C_F41 = [[Aur.x[18],Aur.x[29]],[Aur.y[18],Aur.y[29]],[Aur.x[23],Aur.x[29]],[Aur.y[23],Aur.y[29]],\
                 [Aur.x[26],Aur.x[29]],[Aur.y[26],Aur.y[29]],[Aur.x[29],Aur.x[30]],[Aur.y[29],Aur.y[30]]]
        CF41n = [numpy.mean([Aur.x[18],Aur.x[23],Aur.x[26],Aur.x[29],Aur.x[30]]),\
                 numpy.mean([Aur.y[18],Aur.y[23],Aur.y[26],Aur.y[29],Aur.y[30]])]
        #咸池#
        C_F42 = [[Aur.x[13],Aur.x[35]],[Aur.y[13],Aur.y[35]]]
        CF42n = [numpy.mean([Aur.x[13],Aur.x[35]]),\
                 numpy.mean([Aur.y[13],Aur.y[35]])]
        #天關#
        C_F43 = []
        CF43n = [Tau.x[3],Tau.y[3]]
        #參旗#
        C_F44 = [[Ori.x[8],Ori.x[12]],[Ori.y[8],Ori.y[12]],[Ori.x[8],Ori.x[21]],[Ori.y[8],Ori.y[21]],\
                 [Ori.x[12],Ori.x[13]],[Ori.y[12],Ori.y[13]],[Ori.x[13],Ori.x[26]],[Ori.y[13],Ori.y[26]],\
                 [Ori.x[15],Ori.x[38]],[Ori.y[15],Ori.y[38]],[Ori.x[15],Ori.x[55]],[Ori.y[15],Ori.y[55]],\
                 [Ori.x[21],Ori.x[34]],[Ori.y[21],Ori.y[34]],[Ori.x[34],Ori.x[55]],[Ori.y[34],Ori.y[55]]]
        CF44n = [numpy.mean([Ori.x[8],Ori.x[12],Ori.x[13],Ori.x[15],Ori.x[21],Ori.x[26],Ori.x[34],Ori.x[38],\
                             Ori.x[55]]),\
                 numpy.mean([Ori.y[8],Ori.y[12],Ori.y[13],Ori.y[15],Ori.y[21],Ori.y[26],Ori.y[34],Ori.y[38],\
                             Ori.y[55]])]
        #九斿#
        C_F45 = [[Eri.x[15],Eri.x[27]],[Eri.y[15],Eri.y[27]],[Eri.x[15],Tau.x[66]],[Eri.y[15],Tau.y[66]],\
                 [Eri.x[25],Eri.x[75]],[Eri.y[25],Eri.y[75]],[Eri.x[25],Lep.x[37]],[Eri.y[25],Lep.y[37]],\
                 [Eri.x[27],Eri.x[69]],[Eri.y[27],Eri.y[69]],[Eri.x[41],Eri.x[48]],[Eri.y[41],Eri.y[48]],\
                 [Eri.x[41],Eri.x[69]],[Eri.y[41],Eri.y[69]],[Eri.x[48],Eri.x[75]],[Eri.y[48],Eri.y[75]]]
        CF45n = [numpy.mean([Eri.x[15],Eri.x[25],Eri.x[27],Eri.x[41],Eri.x[48],Eri.x[69],Eri.x[75],Lep.x[37],\
                             Tau.x[66]]),\
                 numpy.mean([Eri.y[15],Eri.y[25],Eri.y[27],Eri.y[41],Eri.y[48],Eri.y[69],Eri.y[75],Lep.y[37],\
                             Tau.y[66]])]
        #天園#
        C_F46 = [[Eri.x[3],Eri.x[33]],[Eri.y[3],Eri.y[33]],[Eri.x[3],Eri.x[38]],[Eri.y[3],Eri.y[38]],\
                 [Eri.x[5],Eri.x[8]],[Eri.y[5],Eri.y[8]],[Eri.x[5],Eri.x[21]],[Eri.y[5],Eri.y[21]],\
                 [Eri.x[6],Eri.x[14]],[Eri.y[6],Eri.y[14]],[Eri.x[6],Eri.x[19]],[Eri.y[6],Eri.y[19]],\
                 [Eri.x[8],Phe.x[6]],[Eri.y[8],Phe.y[6]],[Eri.x[10],Eri.x[14]],[Eri.y[10],Eri.y[14]],\
                 [Eri.x[10],Eri.x[31]],[Eri.y[10],Eri.y[31]],[Eri.x[19],Eri.x[37]],[Eri.y[19],Eri.y[37]],\
                 [Eri.x[21],Eri.x[38]],[Eri.y[21],Eri.y[38]],[Eri.x[33],Eri.x[37]],[Eri.y[33],Eri.y[37]]]
        CF46n = [numpy.mean([Eri.x[3],Eri.x[5],Eri.x[6],Eri.x[8],Eri.x[10],Eri.x[14],Eri.x[19],Eri.x[21],\
                             Eri.x[31],Eri.x[33],Eri.x[37],Eri.x[38],Phe.x[6]]),\
                 numpy.mean([Eri.y[3],Eri.y[5],Eri.y[6],Eri.y[8],Eri.y[10],Eri.y[14],Eri.y[19],Eri.y[21],\
                             Eri.y[31],Eri.y[33],Eri.y[37],Eri.y[38],Phe.y[6]])]
        #觜宿#
        C_F47 = [[Ori.x[10],Ori.x[22]],[Ori.y[10],Ori.y[22]],[Ori.x[16],Ori.x[22]],[Ori.y[16],Ori.y[22]]]
        CF47n = [numpy.mean([Ori.x[10],Ori.x[16],Ori.x[22]]),\
                 numpy.mean([Ori.y[10],Ori.y[16],Ori.y[22]])]
        #司怪#
        C_F48 = [[Gem.x[16],Ori.x[33]],[Gem.y[16],Ori.y[33]],[Gem.x[16],Tau.x[37]],[Gem.y[16],Tau.y[37]],\
                 [Ori.x[23],Ori.x[33]],[Ori.y[23],Ori.y[33]]]
        CF48n = [numpy.mean([Gem.x[16],Ori.x[23],Ori.x[33],Tau.x[37]]),\
                 numpy.mean([Gem.y[16],Ori.y[23],Ori.y[33],Tau.y[37]])]
        #座旗#
        C_F49 = [[Aur.x[17],Aur.x[28]],[Aur.y[17],Aur.y[28]],[Aur.x[17],Aur.x[36]],[Aur.y[17],Aur.y[36]],\
                 [Aur.x[27],Aur.x[36]],[Aur.y[27],Aur.y[36]],[Aur.x[27],Lyn.x[11]],[Aur.y[27],Lyn.y[11]],\
                 [Aur.x[28],Aur.x[33]],[Aur.y[28],Aur.y[33]],[Aur.x[33],Aur.x[51]],[Aur.y[33],Aur.y[51]],\
                 [Aur.x[34],Lyn.x[11]],[Aur.y[34],Lyn.y[11]],[Aur.x[51],Aur.x[94]],[Aur.y[51],Aur.y[94]],]
        CF49n = [numpy.mean([Aur.x[17],Aur.x[27],Aur.x[28],Aur.x[33],Aur.x[34],Aur.x[36],Aur.x[51],Aur.x[94],\
                             Lyn.x[11]]),\
                 numpy.mean([Aur.y[17],Aur.y[27],Aur.y[28],Aur.y[33],Aur.y[34],Aur.y[36],Aur.y[51],Aur.y[94],\
                             Lyn.y[11]])]
        #參宿#
        C_F50 = [[Ori.x[0],Ori.x[6]],[Ori.y[0],Ori.y[6]],[Ori.x[1],Ori.x[4]],[Ori.y[1],Ori.y[4]],\
                 [Ori.x[2],Ori.x[6]],[Ori.y[2],Ori.y[6]],[Ori.x[3],Ori.x[4]],[Ori.y[3],Ori.y[4]],\
                 [Ori.x[3],Ori.x[6]],[Ori.y[3],Ori.y[6]],[Ori.x[4],Ori.x[5]],[Ori.y[4],Ori.y[5]],]
        CF50n = [numpy.mean([Ori.x[0],Ori.x[1],Ori.x[2],Ori.x[3],Ori.x[4],Ori.x[5],Ori.x[6]]),\
                 numpy.mean([Ori.y[0],Ori.y[1],Ori.y[2],Ori.y[3],Ori.y[4],Ori.y[5],Ori.y[6]])]
        #伐#
        C_F51 = [[Ori.x[7],Ori.x[51]],[Ori.y[7],Ori.y[51]],[Ori.x[31],Ori.x[51]],[Ori.y[31],Ori.y[51]]]
        CF51n = [numpy.mean([Ori.x[7],Ori.x[31],Ori.x[51]]),\
                 numpy.mean([Ori.y[7],Ori.y[31],Ori.y[51]])]
        #玉井#
        C_F52 = [[Eri.x[1],Eri.x[43]],[Eri.y[1],Eri.y[43]],[Eri.x[1],Ori.x[11]],[Eri.y[1],Ori.y[11]],\
                 [Eri.x[24],Eri.x[43]],[Eri.y[24],Eri.y[43]]]
        CF52n = [numpy.mean([Eri.x[1],Eri.x[24],Eri.x[43],Ori.x[11]]),\
                 numpy.mean([Eri.y[1],Eri.y[24],Eri.y[43],Ori.y[11]])]
        #屏#
        C_F53 = [[Lep.x[2],Lep.x[3]],[Lep.y[2],Lep.y[3]]]
        CF53n = [numpy.mean([Lep.x[2],Lep.x[3]]),\
                 numpy.mean([Lep.y[2],Lep.y[3]])]
        #軍井#
        C_F54 = [[Lep.x[8],Lep.x[9]],[Lep.y[8],Lep.y[9]],[Lep.x[8],Lep.x[20]],[Lep.y[8],Lep.y[20]],\
                 [Lep.x[9],Lep.x[10]],[Lep.y[9],Lep.y[10]]]
        CF54n = [numpy.mean([Lep.x[8],Lep.x[9],Lep.x[10],Lep.x[20]]),\
                 numpy.mean([Lep.y[8],Lep.y[9],Lep.y[10],Lep.y[20]])]
        #厠#
        C_F55 = [[Lep.x[0],Lep.x[1]],[Lep.y[0],Lep.y[1]],[Lep.x[1],Lep.x[5]],[Lep.y[1],Lep.y[5]],\
                 [Lep.x[5],Lep.x[7]],[Lep.y[5],Lep.y[7]]]
        CF55n = [numpy.mean([Lep.x[0],Lep.x[1],Lep.x[5],Lep.x[7]]),\
                 numpy.mean([Lep.y[0],Lep.y[1],Lep.y[5],Lep.y[7]])]
        #屎#
        C_F56 = []
        CF56n = [Col.x[11],Col.y[11]]

        C_F_list = [C_F01,C_F02,C_F03,C_F04,C_F05,C_F06,C_F07,C_F08,C_F09,C_F10,\
                    C_F11,C_F12,C_F13,C_F14,C_F15,C_F16,C_F17,C_F18,C_F19,C_F20,\
                    C_F21,C_F22,C_F23,C_F24,C_F25,C_F26,C_F27,C_F28,C_F29,C_F30,\
                    C_F31,C_F32,C_F33,C_F34,C_F35,C_F36,C_F37,C_F38,C_F39,C_F40,\
                    C_F41,C_F42,C_F43,C_F44,C_F45,C_F46,C_F47,C_F48,C_F49,C_F50,\
                    C_F51,C_F52,C_F53,C_F54,C_F55,C_F56]

        # 西宮白虎 linecollection
        C_F_line_z_xy1 = []
        C_F_line_z_xy2 = [] 
        C_F_line_xy1 = []
        C_F_line_xy2 = []        
        for i in range(len(C_F_list)):
            for j in range(len(C_F_list[i]))[0::2]:
                if math.hypot(C_F_list[i][j][0]-C_F_list[i][j][1],C_F_list[i][j+1][0]-C_F_list[i][j+1][1]) < hori_border:
                    if i in set([0,9,15,22,31,46,49]):
                        C_F_line_z_xy1.append((C_F_list[i][j][0],C_F_list[i][j+1][0]))
                        C_F_line_z_xy2.append((C_F_list[i][j][1],C_F_list[i][j+1][1]))
                    else:
                        C_F_line_xy1.append((C_F_list[i][j][0],C_F_list[i][j+1][0]))
                        C_F_line_xy2.append((C_F_list[i][j][1],C_F_list[i][j+1][1]))

        C_F_line_z_list = []
        for i in range(len(C_F_line_z_xy1)):            
            C_F_line_z_list.append([C_F_line_z_xy1[i],C_F_line_z_xy2[i]])
        
        C_F_line_list = []
        for i in range(len(C_F_line_xy1)):            
            C_F_line_list.append([C_F_line_xy1[i],C_F_line_xy2[i]])
        
        lc_C_F_z = mc.LineCollection(C_F_line_z_list, colors='yellow', zorder=2+2.5)
        lc_C_F = mc.LineCollection(C_F_line_list, colors='white', zorder=2+2.5)
        lc_C_F_z.set_alpha(plot_alpha)
        lc_C_F.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_F_z)
        ax0.add_collection(lc_C_F)

        CFn_list = [[CF01n,'奎宿'],[CF02n,'外屏'],[CF03n,'天溷'],[CF04n,'土司空'],[CF05n,'軍南門'],\
                    [CF06n,'閣道'],[CF07n,'附路'],[CF08n,'王良'],[CF09n,'策'],[CF10n,'婁宿'],\
                    [CF11n,'左更'],[CF12n,'右更'],[CF13n,'天倉'],[CF14n,'天庾'],[CF15n,'天大將軍'],\
                    [CF16n,'胃宿'],[CF17n,'天廩'],[CF18n,'天囷'],[CF19n,'大陵'],[CF20n,'天船'],\
                    [CF21n,'積尸'],[CF22n,'積水'],[CF23n,'昴宿'],[CF24n,'天阿'],[CF25n,'月'],\
                    [CF26n,'天陰'],[CF27n,'芻蒿'],[CF28n,'天苑'],[CF29n,'卷舌'],[CF30n,'天讒'],\
                    [CF31n,'礪石'],[CF32n,'畢宿'],[CF33n,'附耳'],[CF34n,'天街'],[CF35n,'天節'],\
                    [CF36n,'諸王'],[CF37n,'天高'],[CF38n,'九州殊口'],[CF39n,'五車'],[CF40an,'柱'],\
                    [CF40bn,'柱'],[CF40cn,'柱'],[CF41n,'天潢'],[CF42n,'咸池'],[CF43n,'天關'],\
                    [CF44n,'參旗'],[CF45n,'九斿'],[CF46n,'天園'],[CF47n,'觜宿'],[CF48n,'司怪'],\
                    [CF49n,'座旗'],[CF50n,'參宿'],[CF51n,'伐'],[CF52n,'玉井'],[CF53n,'屏'],\
                    [CF54n,'軍井'],[CF55n,'厠'],[CF56n,'屎']]

        for i in range(len(CFn_list)):
            if len(CFn_list[i][0]) != 0:
                if (CFn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CFn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CFn_list[i][0])-min(CFn_list[i][0]) < hori_border:
                    if i in set([0,9,15,22,31,48,51]):
                        ax_label.annotate(str(CFn_list[i][1]),(CFn_list[i][0][0],CFn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(CFn_list[i][1]),(CFn_list[i][0][0],CFn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #南宮朱雀#
        ##########
        #井宿#
        C_G01 = [[Gem.x[1],Gem.x[7]],[Gem.y[1],Gem.y[7]],[Gem.x[1],Gem.x[12]],[Gem.y[1],Gem.y[12]],\
                 [Gem.x[1],Gem.x[15]],[Gem.y[1],Gem.y[15]],[Gem.x[3],Gem.x[15]],[Gem.y[3],Gem.y[15]],\
                 [Gem.x[5],Gem.x[38]],[Gem.y[5],Gem.y[38]],[Gem.x[10],Gem.x[12]],[Gem.y[10],Gem.y[12]],\
                 [Gem.x[12],Gem.x[38]],[Gem.y[12],Gem.y[38]],[Gem.x[15],Gem.x[38]],[Gem.y[15],Gem.y[38]]]
        CG01n = [numpy.mean([Gem.x[1],Gem.x[3],Gem.x[5],Gem.x[7],Gem.x[10],Gem.x[12],Gem.x[15],Gem.x[38]]),\
                 numpy.mean([Gem.y[1],Gem.y[3],Gem.y[5],Gem.y[7],Gem.y[10],Gem.y[12],Gem.y[15],Gem.y[38]])]
        #鉞#
        C_G02 = []
        CG02n = [Gem.x[6],Gem.y[6]]
        #南河#
        C_G03 = [[CMi.x[0],CMi.x[1]],[CMi.y[0],CMi.y[1]],[CMi.x[1],CMi.x[5]],[CMi.y[1],CMi.y[5]]]
        CG03n = [numpy.mean([CMi.x[0],CMi.x[1],CMi.x[5]]),\
                 numpy.mean([CMi.y[0],CMi.y[1],CMi.y[5]])]
        #北河#
        C_G04 = [[Gem.x[0],Gem.x[4]],[Gem.y[0],Gem.y[4]],[Gem.x[4],Gem.x[17]],[Gem.y[4],Gem.y[17]]]
        CG04n = [numpy.mean([Gem.x[0],Gem.x[4],Gem.x[17]]),\
                 numpy.mean([Gem.y[0],Gem.y[4],Gem.y[17]])]
        #天樽#
        C_G05 = [[Gem.x[8],Gem.x[28]],[Gem.y[8],Gem.y[28]],[Gem.x[8],Gem.x[34]],[Gem.y[8],Gem.y[34]]]
        CG05n = [numpy.mean([Gem.x[8],Gem.x[28],Gem.x[34]]),\
                 numpy.mean([Gem.y[8],Gem.y[28],Gem.y[34]])]
        #五諸候#
        C_G06 = [[Gem.x[11],Gem.x[19]],[Gem.y[11],Gem.y[19]],[Gem.x[13],Gem.x[14]],[Gem.y[13],Gem.y[14]],\
                 [Gem.x[13],Gem.x[19]],[Gem.y[13],Gem.y[19]],[Gem.x[14],Gem.x[25]],[Gem.y[14],Gem.y[25]]]
        CG06n = [numpy.mean([Gem.x[11],Gem.x[13],Gem.x[14],Gem.x[19],Gem.x[25]]),\
                 numpy.mean([Gem.y[11],Gem.y[13],Gem.y[14],Gem.y[19],Gem.y[25]])]
        #積水#
        C_G07 = []
        CG07n = [Aur.x[31],Aur.y[31]]
        #積薪#
        C_G08 = []
        CG08n = [Gem.x[9],Gem.y[9]]
        #水府#
        C_G09 = [[Ori.x[24],Ori.x[27]],[Ori.y[24],Ori.y[27]],[Ori.x[27],Ori.x[60]],[Ori.y[27],Ori.y[60]],\
                 [Ori.x[47],Ori.x[60]],[Ori.y[47],Ori.y[60]]]
        CG09n = [numpy.mean([Ori.x[24],Ori.x[27],Ori.x[47],Ori.x[60]]),\
                 numpy.mean([Ori.y[24],Ori.y[27],Ori.y[47],Ori.y[60]])]
        #水位#
        C_G10 = [[Cnc.x[5],CMi.x[11]],[Cnc.y[5],CMi.y[11]],[Cnc.x[5],Cnc.x[25]],[Cnc.y[5],Cnc.y[25]],\
                 [CMi.x[4],CMi.x[11]],[CMi.y[4],CMi.y[11]],]
        CG10n = [numpy.mean([Cnc.x[5],Cnc.x[25],CMi.x[4],CMi.x[11]]),\
                 numpy.mean([Cnc.y[5],Cnc.y[25],CMi.y[4],CMi.y[11]])]
        #四瀆#
        C_G11 = [[Gem.x[32],Mon.x[10]],[Gem.y[32],Mon.y[10]],[Mon.x[4],Mon.x[6]],[Mon.y[4],Mon.y[6]],\
                 [Mon.x[6],Mon.x[10]],[Mon.y[6],Mon.y[10]]]
        CG11n = [numpy.mean([Gem.x[32],Mon.x[4],Mon.x[6],Mon.x[10]]),\
                 numpy.mean([Gem.y[32],Mon.y[4],Mon.y[6],Mon.y[10]])]
        #軍市#
        C_G12 = [[CMa.x[3],CMa.x[14]],[CMa.y[3],CMa.y[14]],[CMa.x[3],CMa.x[17]],[CMa.y[3],CMa.y[17]],\
                 [CMa.x[9],CMa.x[14]],[CMa.y[9],CMa.y[14]],[CMa.x[9],CMa.x[22]],[CMa.y[9],CMa.y[22]],\
                 [CMa.x[17],CMa.x[25]],[CMa.y[17],CMa.y[25]],[CMa.x[22],CMa.x[25]],[CMa.y[22],CMa.y[25]]]
        CG12n = [numpy.mean([CMa.x[3],CMa.x[9],CMa.x[14],CMa.x[17],CMa.x[22],CMa.x[25]]),\
                 numpy.mean([CMa.y[3],CMa.y[9],CMa.y[14],CMa.y[17],CMa.y[22],CMa.y[25]])]
        #野雞#
        C_G13 = []
        CG13n = [CMa.x[10],CMa.y[10]]
        #丈人#
        C_G14 = [[Col.x[0],Col.x[3]],[Col.y[0],Col.y[3]]]
        CG14n = [numpy.mean([Col.x[0],Col.x[3]]),\
                 numpy.mean([Col.y[0],Col.y[3]])]
        #子#
        C_G15 = [[Col.x[1],Col.x[8]],[Col.y[1],Col.y[8]]]
        CG15n = [numpy.mean([Col.x[1],Col.x[8]]),\
                 numpy.mean([Col.y[1],Col.y[8]])]
        #孫#
        C_G16 = [[Col.x[6],Col.x[10]],[Col.y[6],Col.y[10]]]
        CG16n = [numpy.mean([Col.x[6],Col.x[10]]),\
                 numpy.mean([Col.y[6],Col.y[10]])]
        #闕丘#
        C_G17 = [[Mon.x[2],Mon.x[5]],[Mon.y[2],Mon.y[5]]]
        CG17n = [numpy.mean([Mon.x[2],Mon.x[5]]),\
                 numpy.mean([Mon.y[2],Mon.y[5]])]
        #天狼#
        C_G18 = []
        CG18n = [CMa.x[0],CMa.y[0]]
        #弧矢#
        C_G19 = [[CMa.x[1],CMa.x[4]],[CMa.y[1],CMa.y[4]],[CMa.x[1],CMa.x[11]],[CMa.y[1],CMa.y[11]],\
                 [CMa.x[2],CMa.x[4]],[CMa.y[2],CMa.y[4]],[CMa.x[4],Pup.x[7]],[CMa.y[4],Pup.y[7]],\
                 [CMa.x[4],Pup.x[21]],[CMa.y[4],Pup.y[21]],[CMa.x[11],Pup.x[1]],[CMa.y[11],Pup.y[1]],\
                 [Pup.x[1],Pup.x[7]],[Pup.y[1],Pup.y[7]],[Pup.x[7],Pup.x[37]],[Pup.y[7],Pup.y[37]],\
                 [Pup.x[21],Pup.x[22]],[Pup.y[21],Pup.y[22]],[Pup.x[22],Pup.x[37]],[Pup.y[22],Pup.y[37]]]
        CG19n = [numpy.mean([CMa.x[1],CMa.x[2],CMa.x[4],CMa.x[11],Pup.x[1],Pup.x[7],Pup.x[21],Pup.x[22],\
                             Pup.x[37]]),\
                 numpy.mean([CMa.y[1],CMa.y[2],CMa.y[4],CMa.y[11],Pup.y[1],Pup.y[7],Pup.y[21],Pup.y[22],\
                             Pup.y[37]])]
        #老人#
        C_G20 = []
        CG20n = [Car.x[0],Car.y[0]]
        #鬼宿#
        C_G21 = [[Cnc.x[1],Cnc.x[4]],[Cnc.y[1],Cnc.y[4]],[Cnc.x[4],Cnc.x[14]],[Cnc.y[4],Cnc.y[14]],\
                 [Cnc.x[14],Cnc.x[16]],[Cnc.y[14],Cnc.y[16]]]
        CG21n = [numpy.mean([Cnc.x[1],Cnc.x[4],Cnc.x[14],Cnc.x[16]]),\
                 numpy.mean([Cnc.y[1],Cnc.y[4],Cnc.y[14],Cnc.y[16]])]
        #積尸#
        C_G22 = []
        CG22n = [Cnc.x[78],Cnc.y[78]]
        #爟#
        C_G23 = [[Cnc.x[24],Cnc.x[26]],[Cnc.y[24],Cnc.y[26]],[Cnc.x[24],Cnc.x[45]],[Cnc.y[24],Cnc.y[45]],\
                 [Cnc.x[31],Cnc.x[45]],[Cnc.y[31],Cnc.y[45]]]
        CG23n = [numpy.mean([Cnc.x[24],Cnc.x[26],Cnc.x[31],Cnc.x[45]]),\
                 numpy.mean([Cnc.y[24],Cnc.y[26],Cnc.y[31],Cnc.y[45]])]
        #天狗#
        C_G24 = [[Pyx.x[0],Pyx.x[1]],[Pyx.y[0],Pyx.y[1]],[Pyx.x[0],Pyx.x[2]],[Pyx.y[0],Pyx.y[2]],\
                 [Pyx.x[0],Pyx.x[7]],[Pyx.y[0],Pyx.y[7]],[Pyx.x[1],Vel.x[14]],[Pyx.y[1],Vel.y[14]],\
                 [Vel.x[14],Vel.x[15]],[Vel.y[14],Vel.y[15]]]
        CG24n = [numpy.mean([Pyx.x[0],Pyx.x[1],Pyx.x[2],Pyx.x[7],Vel.x[14],Vel.x[15]]),\
                 numpy.mean([Pyx.y[0],Pyx.y[1],Pyx.y[2],Pyx.y[7],Vel.y[14],Vel.y[15]])]
        #外廚#
        C_G25 = [[Hya.x[10],Hya.x[23]],[Hya.y[10],Hya.y[23]],[Hya.x[23],Hya.x[58]],[Hya.y[23],Hya.y[58]]]
        CG25n = [numpy.mean([Hya.x[10],Hya.x[23],Hya.x[58]]),\
                 numpy.mean([Hya.y[10],Hya.y[23],Hya.y[58]])]
        #天社#
        C_G26 = [[Vel.x[0],Vel.x[10]],[Vel.y[0],Vel.y[10]],[Vel.x[1],Vel.x[3]],[Vel.y[1],Vel.y[3]],\
                 [Vel.x[1],Vel.x[10]],[Vel.y[1],Vel.y[10]],[Vel.x[3],Vel.x[5]],[Vel.y[3],Vel.y[5]]]
        CG26n = [numpy.mean([Vel.x[0],Vel.x[1],Vel.x[3],Vel.x[5],Vel.x[10]]),\
                 numpy.mean([Vel.y[0],Vel.y[1],Vel.y[3],Vel.y[5],Vel.y[10]])]
        #天記#
        C_G27 = []
        CG27n = [Vel.x[2],Vel.y[2]]
        #柳宿#
        C_G28 = [[Hya.x[2],Hya.x[5]],[Hya.y[2],Hya.y[5]],[Hya.x[2],Hya.x[41]],[Hya.y[2],Hya.y[41]],\
                 [Hya.x[5],Hya.x[13]],[Hya.y[5],Hya.y[13]],[Hya.x[9],Hya.x[41]],[Hya.y[9],Hya.y[41]],\
                 [Hya.x[13],Hya.x[19]],[Hya.y[13],Hya.y[19]],[Hya.x[15],Hya.x[17]],[Hya.y[15],Hya.y[17]],\
                 [Hya.x[15],Hya.x[19]],[Hya.y[15],Hya.y[19]]]
        CG28n = [numpy.mean([Hya.x[2],Hya.x[5],Hya.x[9],Hya.x[13],Hya.x[15],Hya.x[17],Hya.x[19],Hya.x[41]]),\
                 numpy.mean([Hya.y[2],Hya.y[5],Hya.y[9],Hya.y[13],Hya.y[15],Hya.y[17],Hya.y[19],Hya.y[41]])]
        #酒旗#
        C_G29 = [[Leo.x[30],Leo.x[41]],[Leo.y[30],Leo.y[41]],[Leo.x[30],Leo.x[43]],[Leo.y[30],Leo.y[43]]]
        CG29n = [numpy.mean([Leo.x[30],Leo.x[41],Leo.x[43]]),\
                 numpy.mean([Leo.y[30],Leo.y[41],Leo.y[43]])]
        #星宿#
        C_G30 = [[Hya.x[0],Hya.x[21]],[Hya.y[0],Hya.y[21]],[Hya.x[0],Hya.x[30]],[Hya.y[0],Hya.y[30]],\
                 [Hya.x[0],Hya.x[152]],[Hya.y[0],Hya.y[152]],[Hya.x[11],Hya.x[20]],[Hya.y[11],Hya.y[20]],\
                 [Hya.x[20],Hya.x[21]],[Hya.y[20],Hya.y[21]],[Hya.x[29],Hya.x[30]],[Hya.y[29],Hya.y[30]],\
                 [Hya.x[29],Hya.x[152]],[Hya.y[29],Hya.y[152]]]
        CG30n = [numpy.mean([Hya.x[0],Hya.x[11],Hya.x[20],Hya.x[21],Hya.x[29],Hya.x[30],Hya.x[152]]),\
                 numpy.mean([Hya.y[0],Hya.y[11],Hya.y[20],Hya.y[21],Hya.y[29],Hya.y[30],Hya.y[152]])]
        #天相#
        C_G31 = [[Sex.x[4],Sex.x[7]],[Sex.y[4],Sex.y[7]]]
        CG31n = [numpy.mean([Sex.x[4],Sex.x[7]]),\
                 numpy.mean([Sex.y[4],Sex.y[7]])]
        #軒轅#
        C_G32 = [[Leo.x[0],Leo.x[7]],[Leo.y[0],Leo.y[7]],[Leo.x[0],Leo.x[8]],[Leo.y[0],Leo.y[8]],\
                 [Leo.x[0],Leo.x[10]],[Leo.y[0],Leo.y[10]],[Leo.x[3],Leo.x[6]],[Leo.y[3],Leo.y[6]],\
                 [Leo.x[3],Leo.x[8]],[Leo.y[3],Leo.y[8]],[Leo.x[4],Leo.x[11]],[Leo.y[4],Leo.y[11]],\
                 [Leo.x[4],Leo.x[15]],[Leo.y[4],Leo.y[15]],[Leo.x[6],Leo.x[11]],[Leo.y[6],Leo.y[11]],\
                 [Leo.x[15],Leo.x[18]],[Leo.y[15],Leo.y[18]],[Leo.x[18],Leo.x[57]],[Leo.y[18],Leo.y[57]],\
                 [Leo.x[57],Lyn.x[0]],[Leo.y[57],Lyn.y[0]],[Lyn.x[0],Lyn.x[1]],[Lyn.y[0],Lyn.y[1]],\
                 [Lyn.x[1],Lyn.x[6]],[Lyn.y[1],Lyn.y[6]],[Lyn.x[2],Lyn.x[6]],[Lyn.y[2],Lyn.y[6]]]
        CG32n = [numpy.mean([Leo.x[0],Leo.x[3],Leo.x[4],Leo.x[6],Leo.x[7],Leo.x[8],Leo.x[10],Leo.x[11],\
                             Leo.x[15],Leo.x[18],Leo.x[57],Lyn.x[0],Lyn.x[1],Lyn.x[2],Lyn.x[6]]),\
                 numpy.mean([Leo.y[0],Leo.y[3],Leo.y[4],Leo.y[6],Leo.y[7],Leo.y[8],Leo.y[10],Leo.y[11],\
                             Leo.y[15],Leo.y[18],Leo.y[57],Lyn.y[0],Lyn.y[1],Lyn.y[2],Lyn.y[6]])]
        #御女#
        C_G33 = []
        CG33n = [Leo.x[16],Leo.y[16]]
        #內平#
        C_G34 = [[LMi.x[2],LMi.x[24]],[LMi.y[2],LMi.y[24]]]
        CG34n = [numpy.mean([LMi.x[2],LMi.x[24]]),\
                 numpy.mean([LMi.y[2],LMi.y[24]])]
        #張宿#
        C_G35 = [[Hya.x[7],Hya.x[8]],[Hya.y[7],Hya.y[8]],[Hya.x[7],Hya.x[12]],[Hya.y[7],Hya.y[12]],\
                 [Hya.x[8],Hya.x[35]],[Hya.y[8],Hya.y[35]],[Hya.x[8],Hya.x[37]],[Hya.y[8],Hya.y[37]],\
                 [Hya.x[12],Hya.x[37]],[Hya.y[12],Hya.y[37]],[Hya.x[12],Hya.x[47]],[Hya.y[12],Hya.y[47]]]
        CG35n = [numpy.mean([Hya.x[7],Hya.x[8],Hya.x[12],Hya.x[35],Hya.x[37],Hya.x[47]]),\
                 numpy.mean([Hya.y[7],Hya.y[8],Hya.y[12],Hya.y[35],Hya.y[37],Hya.y[47]])]
        #翼宿#
        C_G36 = [[Crt.x[0],Crt.x[2]],[Crt.y[0],Crt.y[2]],[Crt.x[0],Crt.x[9]],[Crt.y[0],Crt.y[9]],\
                 [Crt.x[1],Crt.x[2]],[Crt.y[1],Crt.y[2]],[Crt.x[1],Crt.x[7]],[Crt.y[1],Crt.y[7]],\
                 [Crt.x[2],Crt.x[5]],[Crt.y[2],Crt.y[5]],[Crt.x[3],Crt.x[7]],[Crt.y[3],Crt.y[7]],\
                 [Crt.x[4],Crt.x[6]],[Crt.y[4],Crt.y[6]],[Crt.x[5],Crt.x[7]],[Crt.y[5],Crt.y[7]],\
                 [Crt.x[5],Crt.x[8]],[Crt.y[5],Crt.y[8]],[Crt.x[6],Crt.x[15]],[Crt.y[6],Crt.y[15]],\
                 [Crt.x[9],Crt.x[15]],[Crt.y[9],Crt.y[15]],[Crt.x[1],Hya.x[3]],[Crt.y[1],Hya.y[3]],\
                 [Crt.x[3],Hya.x[38]],[Crt.y[3],Hya.y[38]]]
        CG36n = [numpy.mean([Crt.x[0],Crt.x[1],Crt.x[2],Crt.x[3],Crt.x[4],Crt.x[5],Crt.x[6],Crt.x[7],\
                             Crt.x[8],Crt.x[9],Crt.x[15],Hya.x[3],Hya.x[38]]),\
                 numpy.mean([Crt.y[0],Crt.y[1],Crt.y[2],Crt.y[3],Crt.y[4],Crt.y[5],Crt.y[6],Crt.y[7],\
                             Crt.y[8],Crt.y[9],Crt.y[15],Hya.y[3],Hya.y[38]])]
        #軫宿#
        C_G37 = [[Crv.x[0],Crv.x[2]],[Crv.y[0],Crv.y[2]],[Crv.x[0],Crv.x[3]],[Crv.y[0],Crv.y[3]],\
                 [Crv.x[1],Crv.x[2]],[Crv.y[1],Crv.y[2]]]
        CG37n = [numpy.mean([Crv.x[0],Crv.x[1],Crv.x[2],Crv.x[3]]),\
                 numpy.mean([Crv.y[0],Crv.y[1],Crv.y[2],Crv.y[3]])]
        #長沙#
        C_G38 = []
        CG38n = [Crv.x[7],Crv.y[7]]
        #左轄#
        C_G39 = []
        CG39n = [Crv.x[5],Crv.y[5]]
        #右轄#
        C_G40 = []
        CG40n = [Crv.x[4],Crv.y[4]]
        #青丘#
        C_G41 = [[Hya.x[6],Hya.x[46]],[Hya.y[6],Hya.y[46]],[Hya.x[6],Hya.x[123]],[Hya.y[6],Hya.y[123]],\
                 [Hya.x[14],Hya.x[119]],[Hya.y[14],Hya.y[119]],[Hya.x[26],Hya.x[96]],[Hya.y[26],Hya.y[96]],\
                 [Hya.x[46],Hya.x[80]],[Hya.y[46],Hya.y[80]],[Hya.x[80],Hya.x[119]],[Hya.y[80],Hya.y[119]],\
                 [Hya.x[96],Hya.x[123]],[Hya.y[96],Hya.y[123]]]
        CG41n = [numpy.mean([Hya.x[6],Hya.x[14],Hya.x[26],Hya.x[46],Hya.x[80],Hya.x[96],Hya.x[119],Hya.x[123]]),\
                 numpy.mean([Hya.y[6],Hya.y[14],Hya.y[26],Hya.y[46],Hya.y[80],Hya.y[96],Hya.y[119],Hya.y[123]])]

        C_G_list = [C_G01,C_G02,C_G03,C_G04,C_G05,C_G06,C_G07,C_G08,C_G09,C_G10,\
                    C_G11,C_G12,C_G13,C_G14,C_G15,C_G16,C_G17,C_G18,C_G19,C_G20,\
                    C_G21,C_G22,C_G23,C_G24,C_G25,C_G26,C_G27,C_G28,C_G29,C_G30,\
                    C_G31,C_G32,C_G33,C_G34,C_G35,C_G36,C_G37,C_G38,C_G39,C_G40,\
                    C_G41]

        # 南宮朱雀 linecollection
        C_G_line_z_xy1 = []
        C_G_line_z_xy2 = [] 
        C_G_line_xy1 = []
        C_G_line_xy2 = []        
        for i in range(len(C_G_list)):
            for j in range(len(C_G_list[i]))[0::2]:
                if math.hypot(C_G_list[i][j][0]-C_G_list[i][j][1],C_G_list[i][j+1][0]-C_G_list[i][j+1][1]) < hori_border:
                    if i in set([0,20,27,29,34,35,36]):
                        C_G_line_z_xy1.append((C_G_list[i][j][0],C_G_list[i][j+1][0]))
                        C_G_line_z_xy2.append((C_G_list[i][j][1],C_G_list[i][j+1][1]))
                    else:
                        C_G_line_xy1.append((C_G_list[i][j][0],C_G_list[i][j+1][0]))
                        C_G_line_xy2.append((C_G_list[i][j][1],C_G_list[i][j+1][1]))

        C_G_line_z_list = []
        for i in range(len(C_G_line_z_xy1)):            
            C_G_line_z_list.append([C_G_line_z_xy1[i],C_G_line_z_xy2[i]])
        
        C_G_line_list = []
        for i in range(len(C_G_line_xy1)):            
            C_G_line_list.append([C_G_line_xy1[i],C_G_line_xy2[i]])
        
        lc_C_G_z = mc.LineCollection(C_G_line_z_list, colors='yellow', zorder=2+2.5)
        lc_C_G = mc.LineCollection(C_G_line_list, colors='white', zorder=2+2.5)
        lc_C_G_z.set_alpha(plot_alpha)
        lc_C_G.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_G_z)
        ax0.add_collection(lc_C_G)

        CGn_list = [[CG01n,'井宿'],[CG02n,'鉞'],[CG03n,'南河'],[CG04n,'北河'],[CG05n,'天樽'],\
                    [CG06n,'五諸候'],[CG07n,'積水'],[CG08n,'積薪'],[CG09n,'水府'],[CG10n,'水位'],\
                    [CG11n,'四瀆'],[CG12n,'軍市'],[CG13n,'野雞'],[CG14n,'丈人'],[CG15n,'子'],\
                    [CG16n,'孫'],[CG17n,'闕丘'],[CG18n,'天狼'],[CG19n,'弧矢'],[CG20n,'老人'],\
                    [CG21n,'鬼宿'],[CG22n,'積尸'],[CG23n,'爟'],[CG24n,'天狗'],[CG25n,'外廚'],\
                    [CG26n,'天社'],[CG27n,'天記'],[CG28n,'柳宿'],[CG29n,'酒旗'],[CG30n,'星宿'],\
                    [CG31n,'天相'],[CG32n,'軒轅'],[CG33n,'御女'],[CG34n,'內平'],[CG35n,'張宿'],\
                    [CG36n,'翼宿'],[CG37n,'軫宿'],[CG38n,'長沙'],[CG39n,'左轄'],[CG40n,'右轄'],\
                    [CG41n,'青丘']]

        for i in range(len(CGn_list)):
            if len(CGn_list[i][0]) != 0:
                if (CGn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CGn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CGn_list[i][0])-min(CGn_list[i][0]) < hori_border:
                    if i in set([0,20,27,29,34,35,36]):
                        ax_label.annotate(str(CGn_list[i][1]),(CGn_list[i][0][0],CGn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(CGn_list[i][1]),(CGn_list[i][0][0],CGn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #南極星區#
        ##########
        #海山#
        C_H01 = [[Car.x[13],Cen.x[11]],[Car.y[13],Cen.y[11]],[Cen.x[11],Mus.x[3]],[Cen.y[11],Mus.y[3]]]
        CH01n = [numpy.mean([Car.x[13],Cen.x[11],Mus.x[3]]),\
                 numpy.mean([Car.y[13],Cen.y[11],Mus.y[3]])]
        #十字架#
        C_H02 = [[Cru.x[0],Cru.x[4]],[Cru.y[0],Cru.y[4]],[Cru.x[2],Cru.x[3]],[Cru.y[2],Cru.y[3]]]
        CH02n = [numpy.mean([Cru.x[0],Cru.x[2],Cru.x[3],Cru.x[4]]),\
                 numpy.mean([Cru.y[0],Cru.y[2],Cru.y[3],Cru.y[4]])]
        #馬尾#
        C_H03 = [[Cen.x[8],Cen.x[20]],[Cen.y[8],Cen.y[20]],[Cen.x[20],Cen.x[49]],[Cen.y[20],Cen.y[49]]]
        CH03n = [numpy.mean([Cen.x[8],Cen.x[20],Cen.x[49]]),\
                 numpy.mean([Cen.y[8],Cen.y[20],Cen.y[49]])]
        #馬腹#
        C_H04 = []
        CH04n = [Cen.x[1],Cen.y[1]]
        #蜜蜂#
        C_H05 = [[Mus.x[0],Mus.x[1]],[Mus.y[0],Mus.y[1]]]
        CH05n = [numpy.mean([Mus.x[0],Mus.x[1]]),\
                 numpy.mean([Mus.y[0],Mus.y[1]])]
        #三角形#
        C_H06 = [[TrA.x[0],TrA.x[1]],[TrA.y[0],TrA.y[1]],[TrA.x[0],TrA.x[2]],[TrA.y[0],TrA.y[2]],\
                 [TrA.x[1],TrA.x[2]],[TrA.y[1],TrA.y[2]]]
        CH06n = [numpy.mean([TrA.x[0],TrA.x[1],TrA.x[2]]),\
                 numpy.mean([TrA.y[0],TrA.y[1],TrA.y[2]])]
        #異雀#
        C_H07 = [[Aps.x[0],Aps.x[6]],[Aps.y[0],Aps.y[6]],[Aps.x[0],Aps.x[7]],[Aps.y[0],Aps.y[7]],\
                 [Aps.x[1],Aps.x[2]],[Aps.y[1],Aps.y[2]],[Aps.x[1],Oct.x[20]],[Aps.y[1],Oct.y[20]],\
                 [Aps.x[2],Aps.x[7]],[Aps.y[2],Aps.y[7]],[Aps.x[2],Aps.x[9]],[Aps.y[2],Aps.y[9]],\
                 [Aps.x[4],Aps.x[9]],[Aps.y[4],Aps.y[9]],[Aps.x[5],Aps.x[7]],[Aps.y[5],Aps.y[7]]]
        CH07n = [numpy.mean([Aps.x[0],Aps.x[1],Aps.x[2],Aps.x[4],Aps.x[5],Aps.x[6],Aps.x[7],Aps.x[9],\
                             Oct.x[20]]),\
                 numpy.mean([Aps.y[0],Aps.y[1],Aps.y[2],Aps.y[4],Aps.y[5],Aps.y[6],Aps.y[7],Aps.y[9],\
                             Oct.y[20]])]
        #孔雀#
        C_H08 = [[Pav.x[0],Pav.x[7]],[Pav.y[0],Pav.y[7]],[Pav.x[1],Pav.x[2]],[Pav.y[1],Pav.y[2]],\
                 [Pav.x[2],Pav.x[10]],[Pav.y[2],Pav.y[10]],[Pav.x[3],Pav.x[5]],[Pav.y[3],Pav.y[5]],\
                 [Pav.x[3],Pav.x[8]],[Pav.y[3],Pav.y[8]],[Pav.x[4],Pav.x[5]],[Pav.y[4],Pav.y[5]],\
                 [Pav.x[4],Pav.x[7]],[Pav.y[4],Pav.y[7]],[Pav.x[6],Pav.x[10]],[Pav.y[6],Pav.y[10]],\
                 [Pav.x[6],Pav.x[11]],[Pav.y[6],Pav.y[11]],[Pav.x[8],Pav.x[11]],[Pav.y[8],Pav.y[11]]]
        CH08n = [numpy.mean([Pav.x[0],Pav.x[1],Pav.x[2],Pav.x[3],Pav.x[4],Pav.x[5],Pav.x[6],Pav.x[7],\
                             Pav.x[8],Pav.x[10],Pav.x[11]]),\
                 numpy.mean([Pav.y[0],Pav.y[1],Pav.y[2],Pav.y[3],Pav.y[4],Pav.y[5],Pav.y[6],Pav.y[7],\
                             Pav.y[8],Pav.y[10],Pav.y[11]])]
        #波斯#
        C_H09 = []
        CH09n = [Ind.x[0],Ind.y[0]]
        #蛇尾#
        C_H10 = [[Hyi.x[0],Oct.x[0]],[Hyi.y[0],Oct.y[0]],[Oct.x[0],Oct.x[6]],[Oct.y[0],Oct.y[6]]]
        CH10n = [numpy.mean([Hyi.x[0],Oct.x[0],Oct.x[6]]),\
                 numpy.mean([Hyi.y[0],Oct.y[0],Oct.y[6]])]
        #蛇腹#
        C_H11 = [[Hyi.x[3],Hyi.x[4]],[Hyi.y[3],Hyi.y[4]],[Hyi.x[3],Hyi.x[5]],[Hyi.y[3],Hyi.y[5]],\
                 [Hyi.x[4],Hyi.x[7]],[Hyi.y[4],Hyi.y[7]]]
        CH11n = [numpy.mean([Hyi.x[3],Hyi.x[4],Hyi.x[5],Hyi.x[7]]),\
                 numpy.mean([Hyi.y[3],Hyi.y[4],Hyi.y[5],Hyi.y[7]])]
        #蛇首#
        C_H12 = [[Hyi.x[1],Ret.x[1]],[Hyi.y[1],Ret.y[1]]]
        CH12n = [numpy.mean([Hyi.x[1],Ret.x[1]]),\
                 numpy.mean([Hyi.y[1],Ret.y[1]])]
        #鳥喙#
        C_H13 = [[Tuc.x[0],Tuc.x[4]],[Tuc.y[0],Tuc.y[4]],[Tuc.x[2],Tuc.x[5]],[Tuc.y[2],Tuc.y[5]],\
                 [Tuc.x[2],Tuc.x[13]],[Tuc.y[2],Tuc.y[13]],[Tuc.x[3],Tuc.x[13]],[Tuc.y[3],Tuc.y[13]],\
                 [Tuc.x[3],Tuc.x[25]],[Tuc.y[3],Tuc.y[25]],[Tuc.x[4],Tuc.x[25]],[Tuc.y[4],Tuc.y[25]]]
        CH13n = [numpy.mean([Tuc.x[0],Tuc.x[2],Tuc.x[3],Tuc.x[4],Tuc.x[5],Tuc.x[13],Tuc.x[25]]),\
                 numpy.mean([Tuc.y[0],Tuc.y[2],Tuc.y[3],Tuc.y[4],Tuc.y[5],Tuc.y[13],Tuc.y[25]])]
        #鶴#
        C_H14 = [[Gru.x[0],Gru.x[1]],[Gru.y[0],Gru.y[1]],[Gru.x[1],Gru.x[3]],[Gru.y[1],Gru.y[3]],\
                 [Gru.x[1],Gru.x[4]],[Gru.y[1],Gru.y[4]],[Gru.x[1],Gru.x[6]],[Gru.y[1],Gru.y[6]],\
                 [Gru.x[1],Gru.x[7]],[Gru.y[1],Gru.y[7]],[Gru.x[1],Gru.x[8]],[Gru.y[1],Gru.y[8]],\
                 [Gru.x[3],Tuc.x[1]],[Gru.y[3],Tuc.y[1]],[Gru.x[6],Gru.x[10]],[Gru.y[6],Gru.y[10]],\
                 [Gru.x[7],Tuc.x[1]],[Gru.y[7],Tuc.y[1]]]
        CH14n = [numpy.mean([Gru.x[0],Gru.x[1],Gru.x[3],Gru.x[4],Gru.x[6],Gru.x[7],Gru.x[8],Gru.x[10],\
                             Tuc.x[1]]),\
                 numpy.mean([Gru.y[0],Gru.y[1],Gru.y[3],Gru.y[4],Gru.y[6],Gru.y[7],Gru.y[8],Gru.y[10],\
                             Tuc.y[1]])]
        #火鳥#
        C_H15 = [[Phe.x[0],Phe.x[5]],[Phe.y[0],Phe.y[5]],[Phe.x[0],Phe.x[9]],[Phe.y[0],Phe.y[9]],\
                 [Phe.x[1],Phe.x[2]],[Phe.y[1],Phe.y[2]],[Phe.x[1],Phe.x[12]],[Phe.y[1],Phe.y[12]],\
                 [Phe.x[3],Phe.x[5]],[Phe.y[3],Phe.y[5]],[Phe.x[3],Phe.x[11]],[Phe.y[3],Phe.y[11]],\
                 [Phe.x[9],Phe.x[12]],[Phe.y[9],Phe.y[12]],[Phe.x[10],Phe.x[11]],[Phe.y[10],Phe.y[11]],\
                 [Phe.x[10],Scl.x[1]],[Phe.y[10],Scl.y[1]]]
        CH15n = [numpy.mean([Phe.x[0],Phe.x[1],Phe.x[2],Phe.x[3],Phe.x[5],Phe.x[9],Phe.x[10],Phe.x[11],\
                             Phe.x[12],Scl.x[1]]),\
                 numpy.mean([Phe.y[0],Phe.y[1],Phe.y[2],Phe.y[3],Phe.y[5],Phe.y[9],Phe.y[10],Phe.y[11],\
                             Phe.y[12],Scl.y[1]])]
        #水委#
        C_H16 = [[Eri.x[0],Phe.x[4]],[Eri.y[0],Phe.y[4]],[Phe.x[4],Phe.x[7]],[Phe.y[4],Phe.y[7]]]
        CH16n = [numpy.mean([Eri.x[0],Phe.x[4],Phe.x[7]]),\
                 numpy.mean([Eri.y[0],Phe.y[4],Phe.y[7]])]
        #附白#
        C_H17 = [[Hyi.x[2],Hyi.x[6]],[Hyi.y[2],Hyi.y[6]]]
        CH17n = [numpy.mean([Hyi.x[2],Hyi.x[6]]),\
                 numpy.mean([Hyi.y[2],Hyi.y[6]])]
        #夾白#
        C_H18 = [[Dor.x[6],Ret.x[0]],[Dor.y[6],Ret.y[0]]]
        CH18n = [numpy.mean([Dor.x[6],Ret.x[0]]),\
                 numpy.mean([Dor.y[6],Ret.y[0]])]
        #金魚#
        C_H19 = [[Dor.x[0],Dor.x[1]],[Dor.y[0],Dor.y[1]],[Dor.x[0],Dor.x[2]],[Dor.y[0],Dor.y[2]],\
                 [Dor.x[1],Dor.x[3]],[Dor.y[1],Dor.y[3]],[Dor.x[3],Dor.x[8]],[Dor.y[3],Dor.y[8]]]
        CH19n = [numpy.mean([Dor.x[0],Dor.x[1],Dor.x[2],Dor.x[3],Dor.x[8]]),\
                 numpy.mean([Dor.y[0],Dor.y[1],Dor.y[2],Dor.y[3],Dor.y[8]])]
        #海石#
        C_H20 = [[Car.x[2],Car.x[3]],[Car.y[2],Car.y[3]],[Car.x[3],Car.x[18]],[Car.y[3],Car.y[18]],\
                 [Car.x[5],Car.x[11]],[Car.y[5],Car.y[11]],[Car.x[11],Car.x[18]],[Car.y[11],Car.y[18]]]
        CH20n = [numpy.mean([Car.x[2],Car.x[3],Car.x[5],Car.x[11],Car.x[18]]),\
                 numpy.mean([Car.y[2],Car.y[3],Car.y[5],Car.y[11],Car.y[18]])]
        #飛魚#
        C_H21 = [[Vol.x[0],Vol.x[4]],[Vol.y[0],Vol.y[4]],[Vol.x[1],Vol.x[4]],[Vol.y[1],Vol.y[4]],\
                 [Vol.x[2],Vol.x[4]],[Vol.y[2],Vol.y[4]],[Vol.x[3],Vol.x[4]],[Vol.y[3],Vol.y[4]],\
                 [Vol.x[4],Vol.x[11]],[Vol.y[4],Vol.y[11]]]
        CH21n = [numpy.mean([Vol.x[0],Vol.x[1],Vol.x[2],Vol.x[3],Vol.x[4],Vol.x[11]]),\
                 numpy.mean([Vol.y[0],Vol.y[1],Vol.y[2],Vol.y[3],Vol.y[4],Vol.y[11]])]
        #南船#
        C_H22 = [[Car.x[1],Car.x[6]],[Car.y[1],Car.y[6]],[Car.x[4],Car.x[6]],[Car.y[4],Car.y[6]],\
                 [Car.x[4],Car.x[7]],[Car.y[4],Car.y[7]],[Car.x[7],Car.x[8]],[Car.y[7],Car.y[8]]]
        CH22n = [numpy.mean([Car.x[1],Car.x[4],Car.x[6],Car.x[7],Car.x[8]]),\
                 numpy.mean([Car.y[1],Car.y[4],Car.y[6],Car.y[7],Car.y[8]])]
        #小斗#
        C_H23 = [[Cha.x[1],Cha.x[4]],[Cha.y[1],Cha.y[4]],[Cha.x[1],Cha.x[5]],[Cha.y[1],Cha.y[5]],\
                 [Cha.x[2],Cha.x[5]],[Cha.y[2],Cha.y[5]],[Cha.x[3],Cha.x[8]],[Cha.y[3],Cha.y[8]],\
                 [Cha.x[4],Cha.x[7]],[Cha.y[4],Cha.y[7]],[Cha.x[7],Cha.x[8]],[Cha.y[7],Cha.y[8]]]
        CH23n = [numpy.mean([Cha.x[1],Cha.x[2],Cha.x[3],Cha.x[4],Cha.x[5],Cha.x[7],Cha.x[8]]),\
                 numpy.mean([Cha.y[1],Cha.y[2],Cha.y[3],Cha.y[4],Cha.y[5],Cha.y[7],Cha.y[8]])]

        C_H_list = [C_H01,C_H02,C_H03,C_H04,C_H05,C_H06,C_H07,C_H08,C_H09,C_H10,\
                    C_H11,C_H12,C_H13,C_H14,C_H15,C_H16,C_H17,C_H18,C_H19,C_H20,\
                    C_H21,C_H22,C_H23]

        # 南極星區 linecollection
        C_H_line_xy1 = []
        C_H_line_xy2 = []        
        for i in range(len(C_H_list)):
            for j in range(len(C_H_list[i]))[0::2]:
                if math.hypot(C_H_list[i][j][0]-C_H_list[i][j][1],C_H_list[i][j+1][0]-C_H_list[i][j+1][1]) < hori_border:
                    C_H_line_xy1.append((C_H_list[i][j][0],C_H_list[i][j+1][0]))
                    C_H_line_xy2.append((C_H_list[i][j][1],C_H_list[i][j+1][1]))

        C_H_line_list = []
        for i in range(len(C_H_line_xy1)):            
            C_H_line_list.append([C_H_line_xy1[i],C_H_line_xy2[i]])
        
        lc_C_H = mc.LineCollection(C_H_line_list, colors='white', zorder=2+2.5)
        lc_C_H.set_alpha(plot_alpha)
        ax0.add_collection(lc_C_H)

        CHn_list = [[CH01n,'海山'],[CH02n,'十字架'],[CH03n,'馬尾'],[CH04n,'馬腹'],[CH05n,'蜜蜂'],\
                    [CH06n,'三角形'],[CH07n,'異雀'],[CH08n,'孔雀'],[CH09n,'波斯'],[CH10n,'蛇尾'],\
                    [CH11n,'蛇腹'],[CH12n,'蛇首'],[CH13n,'鳥喙'],[CH14n,'鶴'],[CH15n,'火鳥'],\
                    [CH16n,'水委'],[CH17n,'附白'],[CH18n,'夾白'],[CH19n,'金魚'],[CH20n,'海石'],\
                    [CH21n,'飛魚'],[CH22n,'南船'],[CH23n,'小斗']]

        for i in range(len(CHn_list)):
            if len(CHn_list[i][0]) != 0:
                if (CHn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((CHn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(CHn_list[i][0])-min(CHn_list[i][0]) < hori_border:
                    ax_label.annotate(str(CHn_list[i][1]),(CHn_list[i][0][0],CHn_list[i][0][1]),color='w',\
                                      fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    
    elif sky_culture.get() == 2:
        # japanese constellations
        
        ########
        #紫微垣#
        ########
        #北極#
        J_A01 = [[Cam.x[29],UMi.x[0]],[Cam.y[29],UMi.y[0]],[Cam.x[29],UMi.x[8]],[Cam.y[29],UMi.y[8]],\
                 [UMi.x[1],UMi.x[2]],[UMi.y[1],UMi.y[2]],[UMi.x[1],UMi.x[4]],[UMi.y[1],UMi.y[4]],\
                 [UMi.x[4],UMi.x[8]],[UMi.y[4],UMi.y[8]]]
        JA01n = [numpy.mean([Cam.x[29],UMi.x[0],UMi.x[1],UMi.x[2],UMi.x[4],UMi.x[8]]),\
                 numpy.mean([Cam.y[29],UMi.y[0],UMi.y[1],UMi.y[2],UMi.y[4],UMi.y[8]])]
        #四輔　しほ#
        J_A02 = []
        JA02n = [] # ?
        #勾陳　こうちん#
        J_A03 = [[Cep.x[17],Cep.x[19]],[Cep.y[17],Cep.y[19]],[Cep.x[17],Cep.x[37]],[Cep.y[17],Cep.y[37]],\
                 [Cep.x[37],UMi.x[6]],[Cep.y[37],UMi.y[6]],[UMi.x[3],UMi.x[5]],[UMi.y[3],UMi.y[5]],\
                 [UMi.x[3],UMi.x[6]],[UMi.y[3],UMi.y[6]],[UMi.x[5],UMi.x[10]],[UMi.y[5],UMi.y[10]]]
        JA03n = [numpy.mean([Cep.x[17],Cep.x[19],Cep.x[37],UMi.x[3],UMi.x[6]]),\
                 numpy.mean([Cep.y[17],Cep.y[19],Cep.y[37],UMi.y[3],UMi.y[6]])]
        #天皇大帝　てんこうたいてい#
        J_A04 = []
        JA04n = [] # ?
        #天柱　てんちゅう#
        J_A05 = [[Cep.x[13],Cep.x[87]],[Cep.y[13],Cep.y[87]],[Cep.x[76],Cep.x[87]],[Cep.y[76],Cep.y[87]],\
                 [Cep.x[76],Cep.x[91]],[Cep.y[76],Cep.y[91]],[Cep.x[91],Dra.x[65]],[Cep.y[91],Dra.y[65]]]
        JA05n = [numpy.mean([Cep.x[13],Cep.x[76],Cep.x[87],Cep.x[91],Dra.x[65]]),\
                 numpy.mean([Cep.y[13],Cep.y[76],Cep.y[87],Cep.y[91],Dra.y[65]])]
        #御女　ぎょじょ# 
        J_A06 = [[Dra.x[41],Dra.x[83]],[Dra.y[41],Dra.y[83]],[Dra.x[41],UMi.x[25]],[Dra.y[41],UMi.y[25]],\
                 [Dra.x[83],UMi.x[17]],[Dra.y[83],UMi.y[17]],[UMi.x[17],UMi.x[25]],[UMi.y[17],UMi.y[25]]]
        JA06n = [numpy.mean([Dra.x[41],Dra.x[83],UMi.x[17],UMi.x[25]]),\
                 numpy.mean([Dra.y[41],Dra.y[83],UMi.y[17],UMi.y[25]])]
        #女史　じょし# 
        J_A07 = []
        JA07n = [Dra.x[6],Dra.y[6]-labelxy]
        #柱史　ちゅうし# 
        J_A08 = []
        JA08n = [Dra.x[17],Dra.y[17]-labelxy]
        #尚書　しょうしょ#
        J_A09 = [[Dra.x[26],Dra.x[31]],[Dra.y[26],Dra.y[31]],[Dra.x[31],Dra.x[38]],[Dra.y[31],Dra.y[38]],\
                 [Dra.x[31],Dra.x[53]],[Dra.y[31],Dra.y[53]],[Dra.x[31],Dra.x[68]],[Dra.y[31],Dra.y[68]]]
        JA09n = [numpy.mean([Dra.x[26],Dra.x[31],Dra.x[38],Dra.x[53],Dra.x[68]]),\
                 numpy.mean([Dra.y[26],Dra.y[31],Dra.y[38],Dra.y[53],Dra.y[68]])-labelxy]
        #天床　てんしょう#
        J_A10 = []
        JA10n = [] # ?
        #大理　たいり# 
        J_A11 = [[Dra.x[48],Dra.x[95]],[Dra.y[48],Dra.y[95]]]
        JA11n = [numpy.mean([Dra.x[48],Dra.x[95]]),\
                 numpy.mean([Dra.y[48],Dra.y[95]])-labelxy]
        #陰徳　いんとく# 
        J_A12 = [[UMi.x[12],UMi.x[18]],[UMi.y[12],UMi.y[18]]]
        JA12n = [numpy.mean([UMi.x[12],UMi.x[18]]),\
                 numpy.mean([UMi.y[12],UMi.y[18]])-labelxy]
        #六甲　りくこう#
        J_A13 = []
        JA13n = [] # ?
        #五帝內座　ごていたいざ# 
        J_A14 = [[Cas.x[44],Cep.x[62]],[Cas.y[44],Cep.y[62]],[Cep.x[1],Cep.x[62]],[Cep.y[1],Cep.y[62]],\
                 [Cep.x[10],Cep.x[62]],[Cep.y[10],Cep.y[62]],[Cep.x[46],Cep.x[62]],[Cep.y[46],Cep.y[62]]]
        JA14n = [numpy.mean([Cas.x[44],Cep.x[1],Cep.x[10],Cep.x[46],Cep.x[62]]),\
                 numpy.mean([Cas.y[44],Cep.y[1],Cep.y[10],Cep.y[46],Cep.y[62]])-labelxy]
        #華蓋　かがい# 
        J_A15 = [[Cas.x[7],Cas.x[12]],[Cas.y[7],Cas.y[12]],[Cas.x[7],Cas.x[34]],[Cas.y[7],Cas.y[34]],\
                 [Cas.x[12],Cas.x[36]],[Cas.y[12],Cas.y[36]],[Cas.x[17],Cas.x[61]],[Cas.y[17],Cas.y[61]],\
                 [Cas.x[23],Cas.x[34]],[Cas.y[23],Cas.y[34]],[Cas.x[31],Cas.x[61]],[Cas.y[31],Cas.y[61]],\
                 [Cas.x[36],Cas.x[61]],[Cas.y[36],Cas.y[61]],[Cas.x[51],Cas.x[61]],[Cas.y[51],Cas.y[61]]]
        JA15n = [numpy.mean([Cas.x[7],Cas.x[12],Cas.x[17],Cas.x[23],Cas.x[31],Cas.x[34],Cas.x[36],Cas.x[51],\
                             Cas.x[61]]),\
                 numpy.mean([Cas.y[7],Cas.y[12],Cas.y[17],Cas.y[23],Cas.y[31],Cas.y[34],Cas.y[36],Cas.y[51],\
                             Cas.y[61]])-labelxy]
        #杠　こう#
        J_A16 = []
        JA16n = [] # ?
        #右垣墻　うえんしょう# 
        J_A17 = [[Cam.x[7],Cas.x[10]],[Cam.y[7],Cas.y[10]],[Dra.x[7],Dra.x[11]],[Dra.y[7],Dra.y[11]],\
                 [Cam.x[7],Cam.x[39]],[Cam.y[7],Cam.y[39]],[Dra.x[11],Dra.x[27]],[Dra.y[11],Dra.y[27]],\
                 [Cam.x[36],Dra.x[27]],[Cam.y[36],Dra.y[27]],[Cam.x[36],Cam.x[39]],[Cam.y[36],Cam.y[39]]]
        JA17n = [numpy.mean([Cam.x[7],Cam.x[36],Cam.x[39],Cas.x[10],Dra.x[7],Dra.x[11],Dra.x[27]]),\
                 numpy.mean([Cam.y[7],Cam.y[36],Cam.y[39],Cas.y[10],Dra.y[7],Dra.y[11],Dra.y[27]])]
        #左垣墻　さえんしょう# 
        J_A18 = [[Cas.x[40],Cep.x[14]],[Cas.y[40],Cep.y[14]],[Cep.x[14],Cep.x[81]],[Cep.y[14],Cep.y[81]],\
                 [Cep.x[81],Dra.x[13]],[Cep.y[81],Dra.y[13]],[Dra.x[1],Dra.x[4]],[Dra.y[1],Dra.y[4]],\
                 [Dra.x[1],Dra.x[12]],[Dra.y[1],Dra.y[12]],[Dra.x[4],Dra.x[43]],[Dra.y[4],Dra.y[43]],\
                 [Dra.x[5],Dra.x[12]],[Dra.y[5],Dra.y[12]],[Dra.x[13],Dra.x[43]],[Dra.y[13],Dra.y[43]]]
        JA18n = [numpy.mean([Cas.x[40],Cep.x[14],Cep.x[81],Dra.x[4],Dra.x[13],Dra.x[43]]),\
                 numpy.mean([Cas.y[40],Cep.y[14],Cep.y[81],Dra.y[4],Dra.y[13],Dra.y[43]])]
        #天乙　てんいつ# 
        J_A19 = []
        JA19n = [Dra.x[19],Dra.y[19]-labelxy]
        #太乙　たいいつ# 
        J_A20 = []
        JA20n = [Dra.x[101]+labelxy,Dra.y[101]-labelxy]
        #內厨　ないちゅう# 
        J_A21 = []
        JA21n = [Dra.x[10],Dra.y[10]-labelxy]
        #北斗　ほくと# 
        J_A22 = [[UMa.x[0],UMa.x[3]],[UMa.y[0],UMa.y[3]],[UMa.x[0],UMa.x[10]],[UMa.y[0],UMa.y[10]],\
                 [UMa.x[1],UMa.x[4]],[UMa.y[1],UMa.y[4]],[UMa.x[2],UMa.x[3]],[UMa.y[2],UMa.y[3]],\
                 [UMa.x[4],UMa.x[5]],[UMa.y[4],UMa.y[5]],[UMa.x[5],UMa.x[10]],[UMa.y[5],UMa.y[10]]]
        JA22n = [numpy.mean([UMa.x[0],UMa.x[1],UMa.x[4],UMa.x[5],UMa.x[10]]),\
                 numpy.mean([UMa.y[0],UMa.y[1],UMa.y[4],UMa.y[5],UMa.y[10]])]
        #輔　ほ# 
        J_A23 = []
        JA23n = [UMa.x[19],UMa.y[19]-labelxy]
        #天槍　てんそう# 
        J_A24 = [[Boo.x[7],Boo.x[18]],[Boo.y[7],Boo.y[18]],[Boo.x[14],Boo.x[18]],[Boo.y[14],Boo.y[18]]]
        JA24n = [numpy.mean([Boo.x[7],Boo.x[14],Boo.x[18]]),\
                 numpy.mean([Boo.y[7],Boo.y[14],Boo.y[18]])-labelxy]
        #玄戈　げんか# 
        J_A25 = []
        JA25n = [Boo.x[9],Boo.y[9]-labelxy]
        #三公　さんこう# 
        J_A26 = [[CVn.x[2],CVn.x[54]],[CVn.y[2],CVn.y[54]],[CVn.x[11],CVn.x[54]],[CVn.y[11],CVn.y[54]]]
        JA26n = [numpy.mean([CVn.x[2],CVn.x[11],CVn.x[54]]),\
                 numpy.mean([CVn.y[2],CVn.y[11],CVn.y[54]])]
        #相　しょう# 
        J_A27 = []
        JA27n = [CVn.x[5],CVn.y[5]-labelxy]
        #天理　てんり# 
        J_A28 = []
        JA28n = [UMa.x[55],UMa.y[55]-labelxy]
        #太陽守　たいようしゅ# 
        J_A29 = []
        JA29n = [UMa.x[16],UMa.y[16]-labelxy]
        #太尊　たいそん# 
        J_A30 = []
        JA30n = [UMa.x[6],UMa.y[6]-labelxy]
        #天牢　てんろう# 
        J_A31 = [[UMa.x[34],UMa.x[48]],[UMa.y[34],UMa.y[48]],[UMa.x[34],UMa.x[69]],[UMa.y[34],UMa.y[69]],\
                 [UMa.x[44],UMa.x[69]],[UMa.y[44],UMa.y[69]],[UMa.x[44],UMa.x[79]],[UMa.y[44],UMa.y[79]],\
                 [UMa.x[48],UMa.x[96]],[UMa.y[48],UMa.y[96]],[UMa.x[79],UMa.x[96]],[UMa.y[79],UMa.y[96]]]
        JA31n = [numpy.mean([UMa.x[34],UMa.x[44],UMa.x[48],UMa.x[69],UMa.x[79],UMa.x[96]]),\
                 numpy.mean([UMa.y[34],UMa.y[44],UMa.y[48],UMa.y[69],UMa.y[79],UMa.y[96]])]
        #勢　せい#
        J_A32 = []
        JA32n = [] # ?
        #文昌　ぶんしょう# 
        J_A33 = [[UMa.x[9],UMa.x[21]],[UMa.y[9],UMa.y[21]],[UMa.x[9],UMa.x[24]],[UMa.y[9],UMa.y[24]],\
                 [UMa.x[15],UMa.x[17]],[UMa.y[15],UMa.y[17]],[UMa.x[17],UMa.x[24]],[UMa.y[17],UMa.y[24]],\
                 [UMa.x[21],UMa.x[33]],[UMa.y[21],UMa.y[33]]]
        JA33n = [numpy.mean([UMa.x[9],UMa.x[15],UMa.x[17],UMa.x[21],UMa.x[24],UMa.x[33]]),\
                 numpy.mean([UMa.y[9],UMa.y[15],UMa.y[17],UMa.y[21],UMa.y[24],UMa.y[33]])]
        #內階　ないかい# 
        J_A34 = [[Cam.x[20],Cam.x[21]],[Cam.y[20],Cam.y[21]],[Cam.x[20],UMa.x[57]],[Cam.y[20],UMa.y[57]],\
                 [Cam.x[21],Cam.x[31]],[Cam.y[21],Cam.y[31]]]
        JA34n = [numpy.mean([Cam.x[20],Cam.x[21],Cam.x[31],UMa.x[57]]),\
                 numpy.mean([Cam.y[20],Cam.y[21],Cam.y[31],UMa.y[57]])]
        #三師　さんし# 
        J_A35 = [[UMa.x[37],UMa.x[45]],[UMa.y[37],UMa.y[45]],[UMa.x[37],UMa.x[99]],[UMa.y[37],UMa.y[99]]]
        JA35n = [numpy.mean([UMa.x[37],UMa.x[45],UMa.x[99]]),\
                 numpy.mean([UMa.y[37],UMa.y[45],UMa.y[99]])-labelxy]
        #八穀　はちこく# 
        J_A36 = [[Aur.x[6],Aur.x[24]],[Aur.y[6],Aur.y[24]],[Aur.x[24],Cam.x[28]],[Aur.y[24],Cam.y[28]],\
                 [Cam.x[0],Cam.x[28]],[Cam.y[0],Cam.y[28]],[Cam.x[4],Cam.x[30]],[Cam.y[4],Cam.y[30]],\
                 [Cam.x[24],Cam.x[30]],[Cam.y[24],Cam.y[30]],[Cam.x[28],Cam.x[32]],[Cam.y[28],Cam.y[32]]]
        JA36n = [numpy.mean([Aur.x[6],Aur.x[24],Cam.x[0],Cam.x[4],Cam.x[24],Cam.x[28],Cam.x[30],Cam.x[32]]),\
                 numpy.mean([Aur.y[6],Aur.y[24],Cam.y[0],Cam.y[4],Cam.y[24],Cam.y[28],Cam.y[30],Cam.y[32]])]
        #傅舎　でんしゃ# 
        J_A37 = []
        JA37n = [Cam.x[2],Cam.y[2]-labelxy]
        #天厨　てんちゅう# 
        J_A38 = [[Dra.x[3],Dra.x[9]],[Dra.y[3],Dra.y[9]],[Dra.x[3],Dra.x[18]],[Dra.y[3],Dra.y[18]],\
                 [Dra.x[9],Dra.x[16]],[Dra.y[9],Dra.y[16]],[Dra.x[16],Dra.x[18]],[Dra.y[16],Dra.y[18]]]
        JA38n = [numpy.mean([Dra.x[3],Dra.x[9],Dra.x[16],Dra.x[18]]),\
                 numpy.mean([Dra.y[3],Dra.y[9],Dra.y[16],Dra.y[18]])]
        #天棓　てんぼう# 
        J_A39 = [[Dra.x[0],Dra.x[8]],[Dra.y[0],Dra.y[8]],[Dra.x[0],Her.x[9]],[Dra.y[0],Her.y[9]],\
                 [Dra.x[2],Her.x[9]],[Dra.y[2],Her.y[9]],[Dra.x[2],Dra.x[30]],[Dra.y[2],Dra.y[30]],\
                 [Dra.x[8],Dra.x[30]],[Dra.y[8],Dra.y[30]]]
        JA39n = [numpy.mean([Dra.x[0],Dra.x[2],Dra.x[8],Dra.x[30],Her.x[9]]),\
                 numpy.mean([Dra.y[0],Dra.y[2],Dra.y[8],Dra.y[30],Her.y[9]])]
        #東宮傅　とうぐうふ# 
        J_A40 = []
        JA40n = [UMi.x[9],UMi.y[9]-labelxy]
        #御息所　みやすんどころ# 
        J_A41 = []
        JA41n = [UMi.x[11],UMi.y[11]-labelxy]
        #中務　なかつかさ#
        J_A42 = []
        JA42n = [] # ?
        #式部　しきぶ# 
        J_A43 = [[UMa.x[11],UMa.x[25]],[UMa.y[11],UMa.y[25]],[UMa.x[23],UMa.x[32]],[UMa.y[23],UMa.y[32]],\
                 [UMa.x[23],UMa.x[49]],[UMa.y[23],UMa.y[49]],[UMa.x[25],UMa.x[63]],[UMa.y[25],UMa.y[63]],\
                 [UMa.x[27],UMa.x[32]],[UMa.y[27],UMa.y[32]],[UMa.x[27],UMa.x[63]],[UMa.y[27],UMa.y[63]]]
        JA43n = [numpy.mean([UMa.x[11],UMa.x[23],UMa.x[25],UMa.x[32],UMa.x[49],UMa.x[63]]),\
                 numpy.mean([UMa.y[11],UMa.y[23],UMa.y[25],UMa.y[32],UMa.y[49],UMa.y[63]])]
        #治部　じぶ# 
        J_A44 = [[Cam.x[33],Lyn.x[5]],[Cam.y[33],Lyn.y[5]],[Lyn.x[4],Lyn.x[17]],[Lyn.y[4],Lyn.y[17]],\
                 [Lyn.x[4],Lyn.x[22]],[Lyn.y[4],Lyn.y[22]],[Lyn.x[5],Lyn.x[10]],[Lyn.y[5],Lyn.y[10]],\
                 [Lyn.x[10],Lyn.x[22]],[Lyn.y[10],Lyn.y[22]],[Lyn.x[13],Lyn.x[17]],[Lyn.y[13],Lyn.y[17]]]
        JA44n = [numpy.mean([Cam.x[33],Lyn.x[4],Lyn.x[5],Lyn.x[10],Lyn.x[13],Lyn.x[17],Lyn.x[22]]),\
                 numpy.mean([Cam.y[33],Lyn.y[4],Lyn.y[5],Lyn.y[10],Lyn.y[13],Lyn.y[17],Lyn.y[22]])]
        #大膳# 
        J_A45 = [[Cep.x[2],Cep.x[47]],[Cep.y[2],Cep.y[47]],[Cep.x[21],Cep.x[28]],[Cep.y[21],Cep.y[28]],\
                 [Cep.x[21],Cep.x[45]],[Cep.y[21],Cep.y[45]],[Cep.x[28],Cep.x[77]],[Cep.y[28],Cep.y[77]],\
                 [Cep.x[45],Cep.x[47]],[Cep.y[45],Cep.y[47]]]
        JA45n = [numpy.mean([Cep.x[2],Cep.x[21],Cep.x[28],Cep.x[45],Cep.x[47]]),\
                 numpy.mean([Cep.y[2],Cep.y[21],Cep.y[28],Cep.y[45],Cep.y[47]])]
        #內膳# 
        J_A46 = [[Dra.x[23],Dra.x[25]],[Dra.y[23],Dra.y[25]]]
        JA46n = [numpy.mean([Dra.x[23],Dra.x[25]])-labelxy,\
                 numpy.mean([Dra.y[23],Dra.y[25]])]
        #神祇# 
        J_A47 = [[Dra.x[11],Dra.x[58]],[Dra.y[11],Dra.y[58]],[UMa.x[36],UMa.x[59]],[UMa.y[36],UMa.y[59]],\
                 [UMa.x[36],UMa.x[75]],[UMa.y[36],UMa.y[75]],[Dra.x[58],UMa.x[75]],[Dra.y[58],UMa.y[75]],\
                 [UMa.x[59],UMa.x[70]],[UMa.y[59],UMa.y[70]]]
        JA47n = [numpy.mean([Dra.x[11],Dra.x[58],UMa.x[36],UMa.x[59],UMa.x[70],UMa.x[75]]),\
                 numpy.mean([Dra.y[11],Dra.y[58],UMa.y[36],UMa.y[59],UMa.y[70],UMa.y[75]])]
        #天帆　てんはん#
        J_A48 = []
        JA48n = [] # ?

        J_A_list = [J_A01,J_A02,J_A03,J_A04,J_A05,J_A06,J_A07,J_A08,J_A09,J_A10,\
                    J_A11,J_A12,J_A13,J_A14,J_A15,J_A16,J_A17,J_A18,J_A19,J_A20,\
                    J_A21,J_A22,J_A23,J_A24,J_A25,J_A26,J_A27,J_A28,J_A29,J_A30,\
                    J_A31,J_A32,J_A33,J_A34,J_A35,J_A36,J_A37,J_A38,J_A39,J_A40,\
                    J_A41,J_A42,J_A43,J_A44,J_A45,J_A46,J_A47,J_A48]

        # 紫微垣 linecollection
        J_A_line_xy1 = []
        J_A_line_xy2 = []        
        for i in range(len(J_A_list)):
            for j in range(len(J_A_list[i]))[0::2]:
                if math.hypot(J_A_list[i][j][0]-J_A_list[i][j][1],J_A_list[i][j+1][0]-J_A_list[i][j+1][1]) < hori_border:
                    J_A_line_xy1.append((J_A_list[i][j][0],J_A_list[i][j+1][0]))
                    J_A_line_xy2.append((J_A_list[i][j][1],J_A_list[i][j+1][1]))

        J_A_line_list = []
        for i in range(len(J_A_line_xy1)):            
            J_A_line_list.append([J_A_line_xy1[i],J_A_line_xy2[i]])
        
        lc_J_A = mc.LineCollection(J_A_line_list, colors='white', zorder=2+2.5)
        lc_J_A.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_A)

        JAn_list = [[JA01n,'北極'],[JA02n,'四輔'],[JA03n,'勾陳'],[JA04n,'天皇大帝'],[JA05n,'天柱'],\
                    [JA06n,'御女'],[JA07n,'女史'],[JA08n,'柱史'],[JA09n,'尚書'],[JA10n,'天床'],\
                    [JA11n,'大理'],[JA12n,'陰徳'],[JA13n,'六甲'],[JA14n,'五帝內座'],[JA15n,'華蓋'],\
                    [JA16n,'杠'],[JA17n,'右垣墻'],[JA18n,'左垣墻'],[JA19n,'天乙'],[JA20n,'太乙'],\
                    [JA21n,'內厨'],[JA22n,'北斗'],[JA23n,'輔'],[JA24n,'天槍'],[JA25n,'玄戈'],\
                    [JA26n,'三公'],[JA27n,'相'],[JA28n,'天理'],[JA29n,'太陽守'],[JA30n,'太尊'],\
                    [JA31n,'天牢'],[JA32n,'勢'],[JA33n,'文昌'],[JA34n,'內階'],[JA35n,'三師'],\
                    [JA36n,'八穀'],[JA37n,'傅舎'],[JA38n,'天厨'],[JA39n,'天棓'],[JA40n,'東宮傅'],\
                    [JA41n,'御息所'],[JA42n,'中務'],[JA43n,'式部'],[JA44n,'治部'],[JA45n,'大膳'],\
                    [JA46n,'內膳'],[JA47n,'神祇'],[JA48n,'天帆']]
    
        for i in range(len(JAn_list)):
            if len(JAn_list[i][0]) != 0:
                if (JAn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JAn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JAn_list[i][0])-min(JAn_list[i][0]) < hori_border:
                    ax_label.annotate(str(JAn_list[i][1]),(JAn_list[i][0][0],JAn_list[i][0][1]),color='w',\
                                      fontproperties=chara_jap,horizontalalignment='center',verticalalignment='top')

        ########
        #太微垣#
        ########

        #五帝座 ごていざ# 
        J_B01 = []
        JB01n = [Leo.x[1],Leo.y[1]-labelxy]
        #太子　たいし# 
        J_B02 = []
        JB02n = [Leo.x[21],Leo.y[21]-labelxy]
        #従官　じゅうかん# 
        J_B03 = []
        JB03n = [Leo.x[37],Leo.y[37]-labelxy]
        #幸臣　こうしん# 
        J_B04 = []
        JB04n = [Com.x[25],Com.y[25]-labelxy]
        #五諸侯　ごしょこう# 
        J_B05 = [[Com.x[2],Com.x[14]],[Com.y[2],Com.y[14]],[Com.x[2],Com.x[15]],[Com.y[2],Com.y[15]],\
                 [Com.x[7],Com.x[22]],[Com.y[7],Com.y[22]],[Com.x[14],Com.x[22]],[Com.y[14],Com.y[22]]]
        JB05n = [numpy.mean([Com.x[2],Com.x[7],Com.x[14],Com.x[15],Com.x[22]]),\
                 numpy.mean([Com.y[2],Com.y[7],Com.y[14],Com.y[15],Com.y[22]])-labelxy]
        #九卿　きゅうけい# 
        J_B06 = [[Vir.x[27],Vir.x[41]],[Vir.y[27],Vir.y[41]],[Vir.x[41],Vir.x[64]],[Vir.y[41],Vir.y[64]]]
        JB06n = [numpy.mean([Vir.x[27],Vir.x[41],Vir.x[64]])+labelxy,\
                 numpy.mean([Vir.y[27],Vir.y[41],Vir.y[64]])]
        #三公　さんこう#
        J_B07 = []
        JB07n = [] # ?
        #內屏　ないへい# 
        J_B08 = [[Vir.x[10],Vir.x[18]],[Vir.y[10],Vir.y[18]],[Vir.x[10],Vir.x[26]],[Vir.y[10],Vir.y[26]],\
                 [Vir.x[12],Vir.x[18]],[Vir.y[12],Vir.y[18]]]
        JB08n = [numpy.mean([Vir.x[10],Vir.x[12],Vir.x[18],Vir.x[26]]),\
                 numpy.mean([Vir.y[10],Vir.y[12],Vir.y[18],Vir.y[26]])]
        #右垣墻　うえんしょう# 
        J_B09 = [[Leo.x[2],Leo.x[5]],[Leo.y[2],Leo.y[5]],[Leo.x[5],Leo.x[12]],[Leo.y[5],Leo.y[12]],\
                 [Leo.x[12],Leo.x[13]],[Leo.y[12],Leo.y[13]],[Leo.x[13],Vir.x[4]],[Leo.y[13],Vir.y[4]]]
        JB09n = [numpy.mean([Leo.x[2],Leo.x[5],Leo.x[12],Leo.x[13],Vir.x[4]]),\
                 numpy.mean([Leo.y[2],Leo.y[5],Leo.y[12],Leo.y[13],Vir.y[4]])-labelxy]
        #左垣墻　さえんしょう# 
        J_B10 = [[Com.x[19],Vir.x[1]],[Com.y[19],Vir.y[1]],[Vir.x[1],Vir.x[3]],[Vir.y[1],Vir.y[3]],\
                 [Vir.x[3],Vir.x[5]],[Vir.y[3],Vir.y[5]],[Vir.x[5],Vir.x[9]],[Vir.y[5],Vir.y[9]]]
        JB10n = [numpy.mean([Com.x[19],Vir.x[1],Vir.x[3],Vir.x[5],Vir.x[9]]),\
                 numpy.mean([Com.y[19],Vir.y[1],Vir.y[3],Vir.y[5],Vir.y[9]])]
        #郎将　ろうしょう# 
        J_B11 = []
        JB11n = [CVn.x[0],CVn.y[0]-labelxy]
        #郎位　ろうい# 
        J_B12 = []
        JB12n = [Com.x[11],Com.y[11]-labelxy]
        #常陳　じょうちん# 
        J_B13 = []
        JB13n = [UMa.x[58],UMa.y[58]-labelxy]
        #三台　さんだい# 
        J_B14 = [[UMa.x[7],UMa.x[12]],[UMa.y[7],UMa.y[12]],[UMa.x[7],UMa.x[13]],[UMa.y[7],UMa.y[13]],\
                 [UMa.x[8],UMa.x[14]],[UMa.y[8],UMa.y[14]],[UMa.x[12],UMa.x[14]],[UMa.y[12],UMa.y[14]],\
                 [UMa.x[13],UMa.x[20]],[UMa.y[13],UMa.y[20]]]
        JB14n = [numpy.mean([UMa.x[7],UMa.x[8],UMa.x[12],UMa.x[13],UMa.x[14],UMa.x[20]]),\
                 numpy.mean([UMa.y[7],UMa.y[8],UMa.y[12],UMa.y[13],UMa.y[14],UMa.y[20]])]
        #虎賁　こほん# 
        J_B15 = []
        JB15n = [Leo.x[23],Leo.y[23]-labelxy]
        #少微 しょうび# 
        J_B16 = [[Leo.x[17],Leo.x[20]],[Leo.y[17],Leo.y[20]],[Leo.x[17],Leo.x[49]],[Leo.y[17],Leo.y[49]],\
                 [Leo.x[20],LMi.x[6]],[Leo.y[20],LMi.y[6]],[Leo.x[49],LMi.x[6]],[Leo.y[49],LMi.y[6]]]
        JB16n = [numpy.mean([Leo.x[17],Leo.x[20],Leo.x[49],LMi.x[6]]),\
                 numpy.mean([Leo.y[17],Leo.y[20],Leo.y[49],LMi.y[6]])]
        #長垣　ちょうえん# 
        J_B17 = [[Leo.x[34],Leo.x[40]],[Leo.y[34],Leo.y[40]],[Leo.x[40],Leo.x[48]],[Leo.y[40],Leo.y[48]],\
                 [Leo.x[47],Leo.x[48]],[Leo.y[47],Leo.y[48]]]
        JB17n = [numpy.mean([Leo.x[34],Leo.x[40],Leo.x[47],Leo.x[48]]),\
                 numpy.mean([Leo.y[34],Leo.y[40],Leo.y[47],Leo.y[48]])]
        #霊台　ねいだい# 
        J_B18 = [[Leo.x[22],Leo.x[31]],[Leo.y[22],Leo.y[31]],[Leo.x[28],Leo.x[31]],[Leo.y[28],Leo.y[31]]]
        JB18n = [numpy.mean([Leo.x[22],Leo.x[28],Leo.x[31]]),\
                 numpy.mean([Leo.y[22],Leo.y[28],Leo.y[31]])]
        #明堂　めいどう# 
        J_B19 = [[Leo.x[29],Leo.x[42]],[Leo.y[29],Leo.y[42]],[Leo.x[42],Leo.x[45]],[Leo.y[42],Leo.y[45]]]
        JB19n = [numpy.mean([Leo.x[29],Leo.x[42],Leo.x[45]]),\
                 numpy.mean([Leo.y[29],Leo.y[42],Leo.y[45]])-labelxy]
        #謁者　えっしゃ# 
        J_B20 = []
        JB20n = [Vir.x[30],Vir.y[30]-labelxy]
        #大将# 
        J_B21 = [[CVn.x[1],UMa.x[52]],[CVn.y[1],UMa.y[52]]]
        JB21n = [numpy.mean([CVn.x[1],UMa.x[52]]),\
                 numpy.mean([CVn.y[1],UMa.y[52]])-labelxy]
        #中将# 
        J_B22 = [[CVn.x[3],CVn.x[6]],[CVn.y[3],CVn.y[6]],[CVn.x[3],CVn.x[7]],[CVn.y[3],CVn.y[7]],\
                 [CVn.x[7],CVn.x[29]],[CVn.y[7],CVn.y[29]],[CVn.x[12],CVn.x[29]],[CVn.y[12],CVn.y[29]],\
                 [CVn.x[12],Com.x[4]],[CVn.y[12],Com.y[4]],[Com.x[0],Com.x[4]],[Com.y[0],Com.y[4]],\
                 [Com.x[4],Com.x[9]],[Com.y[4],Com.y[9]]]
        JB22n = [numpy.mean([CVn.x[3],CVn.x[6],CVn.x[7],CVn.x[12],CVn.x[29],Com.x[0],Com.x[4],Com.x[9]]),\
                 numpy.mean([CVn.y[3],CVn.y[6],CVn.y[7],CVn.y[12],CVn.y[29],Com.y[0],Com.y[4],Com.y[9]])]
        #少将# 
        J_B23 = [[UMa.x[28],UMa.x[41]],[UMa.y[28],UMa.y[41]],[UMa.x[31],UMa.x[125]],[UMa.y[31],UMa.y[125]],\
                 [UMa.x[41],UMa.x[42]],[UMa.y[41],UMa.y[42]],[UMa.x[42],UMa.x[125]],[UMa.y[42],UMa.y[125]]]
        JB23n = [numpy.mean([UMa.x[28],UMa.x[31],UMa.x[41],UMa.x[42],UMa.x[125]])-labelxy,\
                 numpy.mean([UMa.y[28],UMa.y[31],UMa.y[41],UMa.y[42],UMa.y[125]])]
        #宮內　くない# 
        J_B24 = [[Leo.x[60],LMi.x[8]],[Leo.y[60],LMi.y[8]],[LMi.x[0],LMi.x[8]],[LMi.y[0],LMi.y[8]],\
                 [LMi.x[1],LMi.x[5]],[LMi.y[1],LMi.y[5]],[LMi.x[2],LMi.x[5]],[LMi.y[2],LMi.y[5]],\
                 [LMi.x[4],LMi.x[5]],[LMi.y[4],LMi.y[5]],[LMi.x[4],LMi.x[8]],[LMi.y[4],LMi.y[8]]]
        JB24n = [numpy.mean([LMi.x[0],LMi.x[1],LMi.x[4],LMi.x[5],LMi.x[8]]),\
                 numpy.mean([LMi.y[0],LMi.y[1],LMi.y[4],LMi.y[5],LMi.y[8]])]
        #民部# 
        J_B25 = [[Leo.x[24],Sex.x[14]],[Leo.y[24],Sex.y[14]],[Leo.x[25],Leo.x[46]],[Leo.y[25],Leo.y[46]],\
                 [Leo.x[46],Sex.x[2]],[Leo.y[46],Sex.y[2]],[Leo.x[66],Sex.x[14]],[Leo.y[66],Sex.y[14]],\
                 [Sex.x[0],Sex.x[2]],[Sex.y[0],Sex.y[2]],[Sex.x[0],Sex.x[14]],[Sex.y[0],Sex.y[14]],\
                 [Sex.x[2],Sex.x[3]],[Sex.y[2],Sex.y[3]]]
        JB25n = [numpy.mean([Leo.x[24],Leo.x[25],Leo.x[46],Leo.x[66],Sex.x[0],Sex.x[2],Sex.x[3],Sex.x[14]]),\
                 numpy.mean([Leo.y[24],Leo.y[25],Leo.y[46],Leo.y[66],Sex.y[0],Sex.y[2],Sex.y[3],Sex.y[14]])]
        #刑部　ぎょうぶ# 
        J_B26 = [[Crv.x[20],Vir.x[56]],[Crv.y[20],Vir.y[56]],[Vir.x[19],Vir.x[23]],[Vir.y[19],Vir.y[23]],\
                 [Vir.x[19],Vir.x[56]],[Vir.y[19],Vir.y[56]]]
        JB26n = [numpy.mean([Crv.x[20],Vir.x[19],Vir.x[23],Vir.x[56]]),\
                 numpy.mean([Crv.y[20],Vir.y[19],Vir.y[23],Vir.y[56]])]
        #陰陽寮　おんみょうりょう# 
        J_B27 = [[Leo.x[14],Leo.x[26]],[Leo.y[14],Leo.y[26]],[Leo.x[19],Leo.x[26]],[Leo.y[19],Leo.y[26]]]
        JB27n = [numpy.mean([Leo.x[14],Leo.x[19],Leo.x[26]]),\
                 numpy.mean([Leo.y[14],Leo.y[19],Leo.y[26]])-labelxy]

        J_B_list = [J_B01,J_B02,J_B03,J_B04,J_B05,J_B06,J_B07,J_B08,J_B09,J_B10,\
                    J_B11,J_B12,J_B13,J_B14,J_B15,J_B16,J_B17,J_B18,J_B19,J_B20,\
                    J_B21,J_B22,J_B23,J_B24,J_B25,J_B26,J_B27]

        # 太微垣 linecollection
        J_B_line_xy1 = []
        J_B_line_xy2 = []        
        for i in range(len(J_B_list)):
            for j in range(len(J_B_list[i]))[0::2]:
                if math.hypot(J_B_list[i][j][0]-J_B_list[i][j][1],J_B_list[i][j+1][0]-J_B_list[i][j+1][1]) < hori_border:
                    J_B_line_xy1.append((J_B_list[i][j][0],J_B_list[i][j+1][0]))
                    J_B_line_xy2.append((J_B_list[i][j][1],J_B_list[i][j+1][1]))

        J_B_line_list = []
        for i in range(len(J_B_line_xy1)):            
            J_B_line_list.append([J_B_line_xy1[i],J_B_line_xy2[i]])
        
        lc_J_B = mc.LineCollection(J_B_line_list, colors='white', zorder=2+2.5)
        lc_J_B.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_B)

        JBn_list = [[JB01n,'五帝座'],[JB02n,'太子'],[JB03n,'従官'],[JB04n,'幸臣'],[JB05n,'五諸侯'],\
                    [JB06n,'九卿'],[JB07n,'三公'],[JB08n,'內屏'],[JB09n,'右垣墻'],[JB10n,'左垣墻'],\
                    [JB11n,'郎将'],[JB12n,'郎位'],[JB13n,'常陳'],[JB14n,'三台'],[JB15n,'虎賁'],\
                    [JB16n,'少微'],[JB17n,'長垣'],[JB18n,'霊台'],[JB19n,'明堂'],[JB20n,'謁者'],\
                    [JB21n,'大将'],[JB22n,'中将'],[JB23n,'少将'],[JB24n,'宮內'],[JB25n,'民部'],\
                    [JB26n,'刑部'],[JB27n,'陰陽寮']]
  
        for i in range(len(JBn_list)):
            if len(JBn_list[i][0]) != 0:
                if (JBn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JBn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JBn_list[i][0])-min(JBn_list[i][0]) < hori_border:
                    ax_label.annotate(str(JBn_list[i][1]),(JBn_list[i][0][0],JBn_list[i][0][1]),color='w',\
                                      fontproperties=chara_jap,horizontalalignment='center',verticalalignment='top')

        ########
        #天市垣#
        ########

        #帝座　ていざ#　
        J_C01 = []
        JC01n = [Her.x[5],Her.y[5]-labelxy]
        #侯　こう# 
        J_C02 = []
        JC02n = [Oph.x[0],Oph.y[0]-labelxy]
        #宦者　かんしゃ# 
        J_C03 = [[Her.x[33],Oph.x[133]],[Her.y[33],Oph.y[133]]]
        JC03n = [numpy.mean([Her.x[33],Oph.x[133]]),\
                 numpy.mean([Her.y[33],Oph.y[133]])]
        #斗　と# 
        J_C04 = [[Her.x[51],Her.x[76]],[Her.y[51],Her.y[76]],[Her.x[51],Oph.x[18]],[Her.y[51],Oph.y[18]],\
                 [Her.x[54],Her.x[76]],[Her.y[54],Her.y[76]],[Oph.x[5],Oph.x[18]],[Oph.y[5],Oph.y[18]]]
        JC04n = [numpy.mean([Her.x[51],Her.x[76],Oph.x[5],Oph.x[18]]),\
                 numpy.mean([Her.y[51],Her.y[76],Oph.y[5],Oph.y[18]])]
        #斛　こく# 
        J_C05 = [[Her.x[113],Oph.x[65]],[Her.y[113],Oph.y[65]]]
        JC05n = [numpy.mean([Her.x[113],Oph.x[65]])+labelxy,\
                 numpy.mean([Her.y[113],Oph.y[65]])]
        #列肆　ねっし# 
        J_C06 = [[Oph.x[11],Ser.x[17]],[Oph.y[11],Ser.y[17]]]
        JC06n = [numpy.mean([Oph.x[11],Ser.x[17]]),\
                 numpy.mean([Oph.y[11],Ser.y[17]])-labelxy]
        #車肆　しゃし# 
        J_C07 = [[Oph.x[26],Oph.x[29]],[Oph.y[26],Oph.y[29]]]
        JC07n = [numpy.mean([Oph.x[26],Oph.x[29]]),\
                 numpy.mean([Oph.y[26],Oph.y[29]])+labelxy]
        #市楼　しろう# 
        J_C08 = [[Oph.x[25],Ser.x[11]],[Oph.y[25],Ser.y[11]],[Ser.x[10],Ser.x[11]],[Ser.y[10],Ser.y[11]]]
        JC08n = [numpy.mean([Oph.x[25],Ser.x[10],Ser.x[11]]),\
                 numpy.mean([Oph.y[25],Ser.y[10],Ser.y[11]])]
        #宗正　そうせい# 
        J_C09 = [[Oph.x[4],Oph.x[10]],[Oph.y[4],Oph.y[10]]]
        JC09n = [numpy.mean([Oph.x[4],Oph.x[10]])+labelxy,\
                 numpy.mean([Oph.y[4],Oph.y[10]])]
        #宗人　そうじん# 
        J_C10 = [[Oph.x[12],Oph.x[22]],[Oph.y[12],Oph.y[22]],[Oph.x[12],Oph.x[27]],[Oph.y[12],Oph.y[27]],\
                 [Oph.x[13],Oph.x[22]],[Oph.y[13],Oph.y[22]]]
        JC10n = [numpy.mean([Oph.x[12],Oph.x[13],Oph.x[22],Oph.x[27]])-labelxy,\
                 numpy.mean([Oph.y[12],Oph.y[13],Oph.y[22],Oph.y[27]])+labelxy]
        #宗　そう# 
        J_C11 = [[Oph.x[9],Oph.x[28]],[Oph.y[9],Oph.y[28]]]
        JC11n = [numpy.mean([Oph.x[9],Oph.x[28]])+labelxy,\
                 numpy.mean([Oph.y[9],Oph.y[28]])]
        #帛度　はくど# 
        J_C12 = [[Her.x[46],Her.x[59]],[Her.y[46],Her.y[59]]]
        JC12n = [numpy.mean([Her.x[46],Her.x[59]]),\
                 numpy.mean([Her.y[46],Her.y[59]])-labelxy]
        #屠肆　とし# 
        J_C13 = [[Her.x[18],Her.x[35]],[Her.y[18],Her.y[35]]]
        JC13n = [numpy.mean([Her.x[18],Her.x[35]]),\
                 numpy.mean([Her.y[18],Her.y[35]])+2*labelxy]
        #右垣墻　うえんしょう# 
        J_C14 = [[Her.x[0],Her.x[8]],[Her.y[0],Her.y[8]],[Her.x[8],Her.x[38]],[Her.y[8],Her.y[38]],\
                 [Her.x[38],Ser.x[8]],[Her.y[38],Ser.y[8]],[Oph.x[2],Oph.x[6]],[Oph.y[2],Oph.y[6]],\
                 [Oph.x[3],Ser.x[5]],[Oph.y[3],Ser.y[5]],[Oph.x[3],Oph.x[6]],[Oph.y[3],Oph.y[6]],\
                 [Ser.x[0],Ser.x[5]],[Ser.y[0],Ser.y[5]],[Ser.x[0],Ser.x[7]],[Ser.y[0],Ser.y[7]],\
                 [Ser.x[4],Ser.x[7]],[Ser.y[4],Ser.y[7]],[Ser.x[4],Ser.x[8]],[Ser.y[4],Ser.y[8]]]
        JC14n = [numpy.mean([Her.x[0],Her.x[8],Her.x[38],Oph.x[2],Oph.x[3],Oph.x[6],Ser.x[0],Ser.x[4],\
                             Ser.x[5],Ser.x[7],Ser.x[8]]),\
                 numpy.mean([Her.y[0],Her.y[8],Her.y[38],Oph.y[2],Oph.y[3],Oph.y[6],Ser.y[0],Ser.y[4],\
                             Ser.y[5],Ser.y[7],Ser.y[8]])]
        #左垣墻　さえんしょう# 
        J_C15 = [[Aql.x[2],Her.x[15]],[Aql.y[2],Her.y[15]],[Aql.x[2],Ser.x[15]],[Aql.y[2],Ser.y[15]],\
                 [Her.x[2],Her.x[20]],[Her.y[2],Her.y[20]],[Her.x[4],Her.x[10]],[Her.y[4],Her.y[10]],\
                 [Her.x[4],Her.x[20]],[Her.y[4],Her.y[20]],[Her.x[10],Her.x[15]],[Her.y[10],Her.y[15]],\
                 [Oph.x[1],Ser.x[3]],[Oph.y[1],Ser.y[3]],[Oph.x[8],Ser.x[1]],[Oph.y[8],Ser.y[1]],\
                 [Oph.x[8],Ser.x[3]],[Oph.y[8],Ser.y[3]],[Ser.x[1],Ser.x[15]],[Ser.y[1],Ser.y[15]]]
        JC15n = [numpy.mean([Aql.x[2],Her.x[4],Her.x[10],Her.x[15],Oph.x[8],Ser.x[1],Ser.x[15]]),\
                 numpy.mean([Aql.y[2],Her.y[4],Her.y[10],Her.y[15],Oph.y[8],Ser.y[1],Ser.y[15]])]
        #天紀　てんき# 
        J_C16 = [[CrB.x[9],Her.x[1]],[CrB.y[9],Her.y[1]],[Her.x[1],Her.x[14]],[Her.y[1],Her.y[14]],\
                 [Her.x[12],Her.x[67]],[Her.y[12],Her.y[67]],[Her.x[12],Lyr.x[5]],[Her.y[12],Lyr.y[5]],\
                 [Her.x[14],Her.x[56]],[Her.y[14],Her.y[56]],[Her.x[56],Her.x[67]],[Her.y[56],Her.y[67]]]
        JC16n = [numpy.mean([Her.x[1],Her.x[12],Her.x[14],Her.x[56],Her.x[67]]),\
                 numpy.mean([Her.y[1],Her.y[12],Her.y[14],Her.y[56],Her.y[67]])-labelxy]
        #女牀　じょそう# 
        J_C17 = [[Her.x[3],Her.x[26]],[Her.y[3],Her.y[26]],[Her.x[22],Her.x[26]],[Her.y[22],Her.y[26]]]
        JC17n = [numpy.mean([Her.x[3],Her.x[22],Her.x[26]])-labelxy,\
                 numpy.mean([Her.y[3],Her.y[22],Her.y[26]])-labelxy]
        #貫索　かんさく# 
        J_C18 = [[CrB.x[1],CrB.x[2]],[CrB.y[1],CrB.y[2]],[CrB.x[1],CrB.x[3]],[CrB.y[1],CrB.y[3]],\
                 [CrB.x[2],CrB.x[4]],[CrB.y[2],CrB.y[4]],[CrB.x[3],CrB.x[6]],[CrB.y[3],CrB.y[6]],\
                 [CrB.x[4],CrB.x[18]],[CrB.y[4],CrB.y[18]],[CrB.x[5],CrB.x[6]],[CrB.y[5],CrB.y[6]],\
                 [CrB.x[5],CrB.x[10]],[CrB.y[5],CrB.y[10]],[CrB.x[10],CrB.x[22]],[CrB.y[10],CrB.y[22]]]
        JC18n = [numpy.mean([CrB.x[1],CrB.x[2],CrB.x[3],CrB.x[4],CrB.x[5],CrB.x[6],CrB.x[10],CrB.x[18],\
                             CrB.x[22]]),\
                 numpy.mean([CrB.y[1],CrB.y[2],CrB.y[3],CrB.y[4],CrB.y[5],CrB.y[6],CrB.y[10],CrB.y[18],\
                             CrB.y[22]])]
        #七公　しちこう# 
        J_C19 = [[Boo.x[4],Boo.x[10]],[Boo.y[4],Boo.y[10]],[Boo.x[10],CrB.x[26]],[Boo.y[10],CrB.y[26]],\
                 [CrB.x[7],CrB.x[8]],[CrB.y[7],CrB.y[8]],[CrB.x[7],Her.x[81]],[CrB.y[7],Her.y[81]],\
                 [CrB.x[8],CrB.x[26]],[CrB.y[8],CrB.y[26]],[Her.x[6],Her.x[81]],[Her.y[6],Her.y[81]]]
        JC19n = [numpy.mean([Boo.x[10],CrB.x[7],CrB.x[8],CrB.x[26],Her.x[6],Her.x[81]]),\
                 numpy.mean([Boo.y[10],CrB.y[7],CrB.y[8],CrB.y[26],Her.y[6],Her.y[81]])+labelxy]
        #兵部　ひょうぶ# 
        J_C20 = [[Dra.x[98],Her.x[87]],[Dra.y[98],Her.y[87]]]
        JC20n = [numpy.mean([Dra.x[98],Her.x[87]])+labelxy,\
                 numpy.mean([Dra.y[98],Her.y[87]])-labelxy]
        #宰相# 
        J_C21 = [[Boo.x[5],Boo.x[31]],[Boo.y[5],Boo.y[31]],[Boo.x[31],Her.x[62]],[Boo.y[31],Her.y[62]],\
                 [Her.x[13],Her.x[17]],[Her.y[13],Her.y[17]],[Her.x[13],Her.x[32]],[Her.y[13],Her.y[32]],\
                 [Her.x[16],Her.x[29]],[Her.y[16],Her.y[29]],[Her.x[17],Her.x[28]],[Her.y[17],Her.y[28]],\
                 [Her.x[17],Her.x[62]],[Her.y[17],Her.y[62]],[Her.x[29],Her.x[32]],[Her.y[29],Her.y[32]]]
        JC21n = [numpy.mean([Her.x[13],Her.x[16],Her.x[17],Her.x[28],Her.x[29],Her.x[32],Her.x[62]])-labelxy,\
                 numpy.mean([Her.y[13],Her.y[16],Her.y[17],Her.y[28],Her.y[29],Her.y[32],Her.y[62]])]
        #市正# 
        J_C22 = [[Her.x[23],Her.x[31]],[Her.y[23],Her.y[31]],[Her.x[23],Her.x[47]],[Her.y[23],Her.y[47]],\
                 [Her.x[47],Ser.x[9]],[Her.y[47],Ser.y[9]],[Ser.x[9],Ser.x[50]],[Ser.y[9],Ser.y[50]],\
                 [Ser.x[13],Ser.x[16]],[Ser.y[13],Ser.y[16]],[Ser.x[13],Ser.x[50]],[Ser.y[13],Ser.y[50]],\
                 [Ser.x[16],Ser.x[18]],[Ser.y[16],Ser.y[18]]]
        JC22n = [numpy.mean([Her.x[47],Ser.x[9],Ser.x[13],Ser.x[16],Ser.x[18],Ser.x[50]]),\
                 numpy.mean([Her.y[47],Ser.y[9],Ser.y[13],Ser.y[16],Ser.y[18],Ser.y[50]])]
        #鎮守府# 
        J_C23 = [[Her.x[7],Her.x[21]],[Her.y[7],Her.y[21]]]
        JC23n = [numpy.mean([Her.x[7],Her.x[21]])+3*labelxy,\
                 numpy.mean([Her.y[7],Her.y[21]])]
        #軍監# 
        J_C24 = [[Aql.x[8],Her.x[19]],[Aql.y[8],Her.y[19]],[Her.x[11],Her.x[19]],[Her.y[11],Her.y[19]]]
        JC24n = [numpy.mean([Aql.x[8],Her.x[11],Her.x[19]]),\
                 numpy.mean([Aql.y[8],Her.y[11],Her.y[19]])-labelxy]

        J_C_list = [J_C01,J_C02,J_C03,J_C04,J_C05,J_C06,J_C07,J_C08,J_C09,J_C10,\
                    J_C11,J_C12,J_C13,J_C14,J_C15,J_C16,J_C17,J_C18,J_C19,J_C20,\
                    J_C21,J_C22,J_C23,J_C24]

        # 天市垣 linecollection
        J_C_line_xy1 = []
        J_C_line_xy2 = []        
        for i in range(len(J_C_list)):
            for j in range(len(J_C_list[i]))[0::2]:
                if math.hypot(J_C_list[i][j][0]-J_C_list[i][j][1],J_C_list[i][j+1][0]-J_C_list[i][j+1][1]) < hori_border:
                    J_C_line_xy1.append((J_C_list[i][j][0],J_C_list[i][j+1][0]))
                    J_C_line_xy2.append((J_C_list[i][j][1],J_C_list[i][j+1][1]))

        J_C_line_list = []
        for i in range(len(J_C_line_xy1)):            
            J_C_line_list.append([J_C_line_xy1[i],J_C_line_xy2[i]])
        
        lc_J_C = mc.LineCollection(J_C_line_list, colors='white', zorder=2+2.5)
        lc_J_C.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_C)

        JCn_list = [[JC01n,'帝座'],[JC02n,'侯'],[JC03n,'宦者'],[JC04n,'斗'],[JC05n,'斛'],\
                    [JC06n,'列肆'],[JC07n,'車肆'],[JC08n,'市楼'],[JC09n,'宗正'],[JC10n,'宗人'],\
                    [JC11n,'宗'],[JC12n,'帛度'],[JC13n,'屠肆'],[JC14n,'右垣墻'],[JC15n,'左垣墻'],\
                    [JC16n,'天紀'],[JC17n,'女牀'],[JC18n,'貫索'],[JC19n,'七公'],[JC20n,'兵部'],\
                    [JC21n,'宰相'],[JC22n,'市正'],[JC23n,'鎮守府'],[JC24n,'軍監']]
  
        for i in range(len(JCn_list)):
            if len(JCn_list[i][0]) != 0:
                if (JCn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JCn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JCn_list[i][0])-min(JCn_list[i][0]) < hori_border:
                    ax_label.annotate(str(JCn_list[i][1]),(JCn_list[i][0][0],JCn_list[i][0][1]),color='w',\
                                      fontproperties=chara_jap,horizontalalignment='center',verticalalignment='top')

        ##########
        #東宮蒼龍#
        ##########

        #角宿　かく# 
        J_D01 = [[Vir.x[0],Vir.x[2]],[Vir.y[0],Vir.y[2]]]
        JD01n = [numpy.mean([Vir.x[0],Vir.x[2]]),\
                 numpy.mean([Vir.y[0],Vir.y[2]])]
        #平道　へいどう# 
        J_D02 = [[Vir.x[20],Vir.x[76]],[Vir.y[20],Vir.y[76]]]
        JD02n = [numpy.mean([Vir.x[20],Vir.x[76]]),\
                 numpy.mean([Vir.y[20],Vir.y[76]])]
        #天田　てんでん# 
        J_D03 = [[Vir.x[24],Vir.x[49]],[Vir.y[24],Vir.y[49]]]
        JD03n = [numpy.mean([Vir.x[24],Vir.x[49]]),\
                 numpy.mean([Vir.y[24],Vir.y[49]])]
        #周鼎　しゅうてい# 
        J_D04 = [[Boo.x[27],Boo.x[55]],[Boo.y[27],Boo.y[55]],[Boo.x[27],Boo.x[69]],[Boo.y[27],Boo.y[69]],\
                 [Boo.x[55],Boo.x[69]],[Boo.y[55],Boo.y[69]]]
        JD04n = [numpy.mean([Boo.x[27],Boo.x[55],Boo.x[69]]),\
                 numpy.mean([Boo.y[27],Boo.y[55],Boo.y[69]])]
        #進賢　しんけん# 
        J_D05 = []
        JD05n = [Vir.x[15],Vir.y[15]-labelxy]
        #天門　てんもん# ?
        J_D06 = [[Vir.x[42],Vir.x[98]],[Vir.y[42],Vir.y[98]]]
        JD06n = [numpy.mean([Vir.x[42],Vir.x[98]]),\
                 numpy.mean([Vir.y[42],Vir.y[98]])]
        #平　へい# 
        J_D07 = [[Hya.x[1],Hya.x[42]],[Hya.y[1],Hya.y[42]]]
        JD07n = [numpy.mean([Hya.x[1],Hya.x[42]]),\
                 numpy.mean([Hya.y[1],Hya.y[42]])]
        #庫楼　こうろう# 
        J_D08 = [[Cen.x[3],Cen.x[6]],[Cen.y[3],Cen.y[6]],[Cen.x[3],Cen.x[9]],[Cen.y[3],Cen.y[9]],\
                 [Cen.x[6],Lup.x[0]],[Cen.y[6],Lup.y[0]],[Cen.x[7],Lup.x[0]],[Cen.y[7],Lup.y[0]],\
                 [Cen.x[9],Cen.x[27]],[Cen.y[9],Cen.y[27]],[Cen.x[27],Cen.x[42]],[Cen.y[27],Cen.y[42]]]
        JD08n = [numpy.mean([Cen.x[3],Cen.x[6],Cen.x[7],Cen.x[9],Cen.x[27],Cen.x[42],Lup.x[0]]),\
                 numpy.mean([Cen.y[3],Cen.y[6],Cen.y[7],Cen.y[9],Cen.y[27],Cen.y[42],Lup.y[0]])]
        #柱　ちゅう# 
        J_D09 = [[Cen.x[16],Cen.x[32]],[Cen.y[16],Cen.y[32]],[Cen.x[22],Cen.x[34]],[Cen.y[22],Cen.y[34]],\
                 [Cen.x[25],Cen.x[26]],[Cen.y[25],Cen.y[26]],[Cen.x[25],Cen.x[39]],[Cen.y[25],Cen.y[39]],\
                 [Lup.x[7],Lup.x[18]],[Lup.y[7],Lup.y[18]]]
        JD09an = [numpy.mean([Cen.x[16],Cen.x[32]]),\
                  numpy.mean([Cen.y[16],Cen.y[32]])]
        JD09bn = [numpy.mean([Cen.x[22],Cen.x[34]]),\
                  numpy.mean([Cen.y[22],Cen.y[34]])]
        JD09cn = [numpy.mean([Cen.x[25],Cen.x[26],Cen.x[39]]),\
                  numpy.mean([Cen.y[25],Cen.y[26],Cen.y[39]])]
        JD09dn = [numpy.mean([Lup.x[7],Lup.x[18]]),\
                  numpy.mean([Lup.y[7],Lup.y[18]])]
        #衡　こう# 
        J_D10 = [[Cen.x[10],Cen.x[13]],[Cen.y[10],Cen.y[13]],[Cen.x[10],Cen.x[14]],[Cen.y[10],Cen.y[14]],\
                 [Cen.x[14],Cen.x[33]],[Cen.y[14],Cen.y[33]]]
        JD10n = [numpy.mean([Cen.x[10],Cen.x[13],Cen.x[14],Cen.x[33]]),\
                 numpy.mean([Cen.y[10],Cen.y[13],Cen.y[14],Cen.y[33]])]
        #南門　なんもん# 
        J_D11 = [[Cen.x[4],Cen.x[5]],[Cen.y[4],Cen.y[5]]]
        JD11n = [numpy.mean([Cen.x[4],Cen.x[5]]),\
                 numpy.mean([Cen.y[4],Cen.y[5]])]
        #亢宿　こう# 
        J_D12 = [[Vir.x[11],Vir.x[13]],[Vir.y[11],Vir.y[13]],[Vir.x[11],Vir.x[25]],[Vir.y[11],Vir.y[25]],\
                 [Vir.x[13],Vir.x[17]],[Vir.y[13],Vir.y[17]]]
        JD12n = [numpy.mean([Vir.x[11],Vir.x[13],Vir.x[17],Vir.x[25]]),\
                 numpy.mean([Vir.y[11],Vir.y[13],Vir.y[17],Vir.y[25]])]
        #大角　たいかく# 
        J_D13 = []
        JD13n = [Boo.x[0],Boo.y[0]-labelxy]
        #右摂提　うせってい# 
        J_D14 = [[Boo.x[1],Boo.x[13]],[Boo.y[1],Boo.y[13]],[Boo.x[8],Boo.x[13]],[Boo.y[8],Boo.y[13]]]
        JD14n = [numpy.mean([Boo.x[1],Boo.x[8],Boo.x[13]]),\
                 numpy.mean([Boo.y[1],Boo.y[8],Boo.y[13]])]
        #左摂提　させってい# 
        J_D15 = [[Boo.x[11],Boo.x[29]],[Boo.y[11],Boo.y[29]],[Boo.x[17],Boo.x[29]],[Boo.y[17],Boo.y[29]]]
        JD15n = [numpy.mean([Boo.x[11],Boo.x[17],Boo.x[29]]),\
                 numpy.mean([Boo.y[11],Boo.y[17],Boo.y[29]])]
        #折威　せつい#
        J_D16 = []
        JD16n = [] # ?
        #頓頑　とんがん#
        J_D17 = []
        JD17n = [] # ?
        #陽門　ようもん# 
        J_D18 = [[Vir.x[31],Vir.x[65]],[Vir.y[31],Vir.y[65]]]
        JD18n = [numpy.mean([Vir.x[31],Vir.x[65]]),\
                 numpy.mean([Vir.y[31],Vir.y[65]])]
        #氐宿  てい# 
        J_D19 = [[Lib.x[0],Lib.x[1]],[Lib.y[0],Lib.y[1]],[Lib.x[0],Lib.x[5]],[Lib.y[0],Lib.y[5]],\
                 [Lib.x[1],Lib.x[8]],[Lib.y[1],Lib.y[8]],[Lib.x[5],Lib.x[8]],[Lib.y[5],Lib.y[8]]]
        JD19n = [numpy.mean([Lib.x[0],Lib.x[1],Lib.x[5],Lib.x[8]]),\
                 numpy.mean([Lib.y[0],Lib.y[1],Lib.y[5],Lib.y[8]])]
        #亢池　こうち# 
        J_D20 = [[Boo.x[25],Boo.x[44]],[Boo.y[25],Boo.y[44]],[Boo.x[25],Boo.x[50]],[Boo.y[25],Boo.y[50]],\
                 [Boo.x[40],Boo.x[44]],[Boo.y[40],Boo.y[44]],[Boo.x[40],Boo.x[50]],[Boo.y[40],Boo.y[50]]]
        JD20n = [numpy.mean([Boo.x[25],Boo.x[40],Boo.x[44],Boo.x[50]]),\
                 numpy.mean([Boo.y[25],Boo.y[40],Boo.y[44],Boo.y[50]])]
        #帝座　ていざ# 
        J_D21 = [[Boo.x[23],Boo.x[82]],[Boo.y[23],Boo.y[82]],[Boo.x[23],CVn.x[28]],[Boo.y[23],CVn.y[28]]]
        JD21n = [numpy.mean([Boo.x[23],Boo.x[82],CVn.x[28]]),\
                 numpy.mean([Boo.y[23],Boo.y[82],CVn.y[28]])]
        #梗河　こうが# 
        J_D22 = [[Boo.x[2],Boo.x[12]],[Boo.y[2],Boo.y[12]],[Boo.x[6],Boo.x[12]],[Boo.y[6],Boo.y[12]]]
        JD22n = [numpy.mean([Boo.x[2],Boo.x[6],Boo.x[12]]),\
                 numpy.mean([Boo.y[2],Boo.y[6],Boo.y[12]])]
        #招搖　しょうよう# 
        J_D23 = []
        JD23n = [Boo.x[3],Boo.y[3]-labelxy]
        #天乳　てんにゅう# 
        J_D24 = []
        JD24n = [Ser.x[2],Ser.y[2]-labelxy]
        #天輻　てんぷく# 
        J_D25 = [[Lib.x[3],Lib.x[4]],[Lib.y[3],Lib.y[4]]]
        JD25n = [numpy.mean([Lib.x[3],Lib.x[4]]),\
                 numpy.mean([Lib.y[3],Lib.y[4]])]
        #陣車　じんしゃ# ?
        J_D26 = []
        JD26n = [Lib.x[2],Lib.y[2]-labelxy]
        #騎官　きかん# 
        J_D27 = [[Lup.x[1],Lup.x[3]],[Lup.y[1],Lup.y[3]],[Lup.x[1],Lup.x[15]],[Lup.y[1],Lup.y[15]],\
                 [Lup.x[2],Lup.x[3]],[Lup.y[2],Lup.y[3]],[Lup.x[3],Lup.x[42]],[Lup.y[3],Lup.y[42]],\
                 [Lup.x[8],Lup.x[23]],[Lup.y[8],Lup.y[23]],[Lup.x[8],Lup.x[27]],[Lup.y[8],Lup.y[27]],\
                 [Lup.x[23],Lup.x[42]],[Lup.y[23],Lup.y[42]]]
        JD27n = [numpy.mean([Lup.x[1],Lup.x[2],Lup.x[3],Lup.x[8],Lup.x[15],Lup.x[23],Lup.x[27],Lup.x[42]]),\
                 numpy.mean([Lup.y[1],Lup.y[2],Lup.y[3],Lup.y[8],Lup.y[15],Lup.y[23],Lup.y[27],Lup.y[42]])]
        #車騎　しゃき# 
        J_D28 = [[Lup.x[9],Lup.x[14]],[Lup.y[9],Lup.y[14]],[Lup.x[9],Lup.x[29]],[Lup.y[9],Lup.y[29]]]
        JD28n = [numpy.mean([Lup.x[9],Lup.x[14],Lup.x[29]]),\
                 numpy.mean([Lup.y[9],Lup.y[14],Lup.y[29]])]
        #将軍　しょうぐん#
        J_D29 = []
        JD29n = [] # ?
        #房宿　ぼう# 
        J_D30 = [[Sco.x[4],Sco.x[6]],[Sco.y[4],Sco.y[6]],[Sco.x[4],Sco.x[9]],[Sco.y[4],Sco.y[9]],\
                 [Sco.x[9],Sco.x[17]],[Sco.y[9],Sco.y[17]]]
        JD30n = [numpy.mean([Sco.x[4],Sco.x[6],Sco.x[9],Sco.x[17]]),\
                 numpy.mean([Sco.y[4],Sco.y[6],Sco.y[9],Sco.y[17]])]
        #鈎鈐　こうけん# 
        J_D31 = []
        JD31n = [Sco.x[23],Sco.y[23]-labelxy]
        #鍵閉　けんぺい# 
        J_D32 = []
        JD32n = [Sco.x[19],Sco.y[19]-labelxy]
        #罰　ばつ# 
        J_D33 = [[Oph.x[15],Oph.x[20]],[Oph.y[15],Oph.y[20]],[Oph.x[20],Oph.x[23]],[Oph.y[20],Oph.y[23]]]
        JD33n = [numpy.mean([Oph.x[15],Oph.x[20],Oph.x[23]]),\
                 numpy.mean([Oph.x[15],Oph.x[20],Oph.x[23]])]
        #西咸　せいかん# 
        J_D34 = [[Lib.x[6],Lib.x[11]],[Lib.y[6],Lib.y[11]],[Lib.x[11],Sco.x[29]],[Lib.y[11],Sco.y[29]],\
                 [Sco.x[29],Sco.x[38]],[Sco.y[29],Sco.y[38]]]
        JD34n = [numpy.mean([Lib.x[6],Lib.x[11],Sco.x[29],Sco.x[38]]),\
                 numpy.mean([Lib.y[6],Lib.y[11],Sco.y[29],Sco.y[38]])]
        #東咸　とうかん# 
        J_D35 = [[Oph.x[21],Oph.x[35]],[Oph.y[21],Oph.y[35]],[Oph.x[21],Oph.x[36]],[Oph.y[21],Oph.y[36]]]
        JD35n = [numpy.mean([Oph.x[21],Oph.x[35],Oph.x[36]]),\
                 numpy.mean([Oph.y[21],Oph.y[35],Oph.y[36]])]
        #日　じつ# 
        J_D36 = []
        JD36n = [Sco.x[25],Sco.y[25]-labelxy]
        #従官　じゅうかん# 
        J_D37 = [[Lup.x[10],Lup.x[35]],[Lup.y[10],Lup.y[35]]]
        JD37n = [numpy.mean([Lup.x[10],Lup.x[35]]),\
                 numpy.mean([Lup.y[10],Lup.y[35]])]
        #心宿　しん# 
        J_D38 = [[Sco.x[0],Sco.x[8]],[Sco.y[0],Sco.y[8]],[Sco.x[0],Sco.x[10]],[Sco.y[0],Sco.y[10]]]
        JD38n = [numpy.mean([Sco.x[0],Sco.x[8],Sco.x[10]]),\
                 numpy.mean([Sco.y[0],Sco.y[8],Sco.y[10]])]
        #積卒　せきそつ# 
        J_D39 = [[Lup.x[6],Lup.x[13]],[Lup.y[6],Lup.y[13]]]
        JD39n = [numpy.mean([Lup.x[6],Lup.x[13]]),\
                 numpy.mean([Lup.y[6],Lup.y[13]])]
        #尾宿　び# 
        J_D40 = [[Sco.x[1],Sco.x[5]],[Sco.y[1],Sco.y[5]],[Sco.x[1],Sco.x[7]],[Sco.y[1],Sco.y[7]],\
                 [Sco.x[2],Sco.x[11]],[Sco.y[2],Sco.y[11]],[Sco.x[2],Sco.x[14]],[Sco.y[2],Sco.y[14]],\
                 [Sco.x[3],Sco.x[12]],[Sco.y[3],Sco.y[12]],[Sco.x[5],Sco.x[11]],[Sco.y[5],Sco.y[11]],\
                 [Sco.x[12],Sco.x[16]],[Sco.y[12],Sco.y[16]],[Sco.x[14],Sco.x[16]],[Sco.y[14],Sco.y[16]]]
        JD40n = [numpy.mean([Sco.x[1],Sco.x[2],Sco.x[3],Sco.x[5],Sco.x[7],Sco.x[11],Sco.x[12],Sco.x[14],\
                             Sco.x[16]]),\
                 numpy.mean([Sco.y[1],Sco.y[2],Sco.y[3],Sco.y[5],Sco.y[7],Sco.y[11],Sco.y[12],Sco.y[14],\
                             Sco.y[16]])]
        #神宮　じんきゅう# 
        J_D41 = []
        JD41n = [Sco.x[15],Sco.y[15]-labelxy]
        #天江　てんこう# 
        J_D42 = [[Oph.x[7],Oph.x[14]],[Oph.y[7],Oph.y[14]],[Oph.x[7],Oph.x[39]],[Oph.y[7],Oph.y[39]],\
                 [Oph.x[14],Oph.x[31]],[Oph.y[14],Oph.y[31]]]
        JD42n = [numpy.mean([Oph.x[7],Oph.x[14],Oph.x[31],Oph.x[39]]),\
                 numpy.mean([Oph.y[7],Oph.y[14],Oph.y[31],Oph.y[39]])]
        #伝說　ふえつ# 
        J_D43 = []
        JD43n = [Sco.x[13],Sco.y[13]-labelxy]
        #魚　ぎょ# 
        J_D44 = []
        JD44n = [numpy.mean([Sco.x[65],Sco.x[78],Sco.x[86],Sco.x[97],Sco.x[98],Sco.x[109],Sco.x[124],Sco.x[144],\
                             Sco.x[150],Sco.x[155]]),\
                 numpy.mean([Sco.y[65],Sco.y[78],Sco.y[86],Sco.y[97],Sco.y[98],Sco.y[109],Sco.y[124],Sco.y[144],\
                             Sco.y[150],Sco.y[155]])]
        #亀　き# 
        J_D45 = [[Ara.x[2],Ara.x[6]],[Ara.y[2],Ara.y[6]],[Ara.x[2],Ara.x[7]],[Ara.y[2],Ara.y[7]],\
                 [Ara.x[3],Ara.x[4]],[Ara.y[3],Ara.y[4]],[Ara.x[3],Ara.x[7]],[Ara.y[3],Ara.y[7]],\
                 [Ara.x[4],Ara.x[6]],[Ara.y[4],Ara.y[6]]]
        JD45n = [numpy.mean([Ara.x[2],Ara.x[3],Ara.x[4],Ara.x[6],Ara.x[7]]),\
                 numpy.mean([Ara.y[2],Ara.y[3],Ara.y[4],Ara.y[6],Ara.y[7]])]
        #箕宿　き# 
        J_D46 = [[Sgr.x[0],Sgr.x[3]],[Sgr.y[0],Sgr.y[3]],[Sgr.x[0],Sgr.x[7]],[Sgr.y[0],Sgr.y[7]],\
                 [Sgr.x[3],Sgr.x[6]],[Sgr.y[3],Sgr.y[6]],[Sgr.x[6],Sgr.x[7]],[Sgr.y[6],Sgr.y[7]]]
        JD46n = [numpy.mean([Sgr.x[0],Sgr.x[3],Sgr.x[6],Sgr.x[7]]),\
                 numpy.mean([Sgr.y[0],Sgr.y[3],Sgr.y[6],Sgr.y[7]])]
        #糠　こう#
        J_D47 = []
        JD47n = [] # ?
        #杵　しょ# 
        J_D48 = []
        JD48n = [Tel.x[0],Tel.y[0]-labelxy]
        #左衛門# 
        J_D49 = [[Vir.x[21],Vir.x[22]],[Vir.y[21],Vir.y[22]],[Vir.x[21],Vir.x[35]],[Vir.y[21],Vir.y[35]]]
        JD49n = [numpy.mean([Vir.x[21],Vir.x[22],Vir.x[35]]),\
                 numpy.mean([Vir.y[21],Vir.y[22],Vir.y[35]])]
        #天湖# 
        J_D50 = [[Boo.x[26],Vir.x[14]],[Boo.y[26],Vir.y[14]]]
        JD50n = [numpy.mean([Boo.x[26],Vir.x[14]]),\
                 numpy.mean([Boo.y[26],Vir.y[14]])]
        #湯母# 
        J_D51 = [[Ser.x[20],Ser.x[23]],[Ser.y[20],Ser.y[23]],[Ser.x[20],Vir.x[16]],[Ser.y[20],Vir.y[16]],\
                 [Vir.x[7],Vir.x[16]],[Vir.y[7],Vir.y[16]]]
        JD51n = [numpy.mean([Ser.x[20],Ser.x[23],Vir.x[7],Vir.x[16]]),\
                 numpy.mean([Ser.y[20],Ser.y[23],Vir.y[7],Vir.y[16]])]
        #湯座# 
        J_D52 = [[Lib.x[7],Vir.x[8]],[Lib.y[7],Vir.y[8]]]
        JD52n = [numpy.mean([Lib.x[7],Vir.x[8]]),\
                 numpy.mean([Lib.y[7],Vir.y[8]])]
        #內侍　ないし# 
        J_D53 = [[Lib.x[9],Lib.x[14]],[Lib.y[9],Lib.y[14]]]
        JD53n = [numpy.mean([Lib.x[9],Lib.x[14]]),\
                 numpy.mean([Lib.y[9],Lib.y[14]])]
        #采女　うねめ# 
        J_D54 = [[Oph.x[16],Sgr.x[20]],[Oph.y[16],Sgr.y[20]]]
        JD54n = [numpy.mean([Oph.x[16],Sgr.x[20]]),\
                 numpy.mean([Oph.y[16],Sgr.y[20]])]
        #腹赤# ?
        J_D55 = []
        JD55n = [Sco.x[33],Sco.y[33]-labelxy]

        J_D_list = [J_D01,J_D02,J_D03,J_D04,J_D05,J_D06,J_D07,J_D08,J_D09,J_D10,\
                    J_D11,J_D12,J_D13,J_D14,J_D15,J_D16,J_D17,J_D18,J_D19,J_D20,\
                    J_D21,J_D22,J_D23,J_D24,J_D25,J_D26,J_D27,J_D28,J_D29,J_D30,\
                    J_D31,J_D32,J_D33,J_D34,J_D35,J_D36,J_D37,J_D38,J_D39,J_D40,\
                    J_D41,J_D42,J_D43,J_D44,J_D45,J_D46,J_D47,J_D48,J_D49,J_D50,\
                    J_D51,J_D52,J_D53,J_D54,J_D55]

        # 東宮蒼龍 linecollection
        J_D_line_z_xy1 = []
        J_D_line_z_xy2 = [] 
        J_D_line_xy1 = []
        J_D_line_xy2 = []        
        for i in range(len(J_D_list)):
            for j in range(len(J_D_list[i]))[0::2]:
                if math.hypot(J_D_list[i][j][0]-J_D_list[i][j][1],J_D_list[i][j+1][0]-J_D_list[i][j+1][1]) < hori_border:
                    if i in set([0,11,18,29,37,39,45]):
                        J_D_line_z_xy1.append((J_D_list[i][j][0],J_D_list[i][j+1][0]))
                        J_D_line_z_xy2.append((J_D_list[i][j][1],J_D_list[i][j+1][1]))
                    else:
                        J_D_line_xy1.append((J_D_list[i][j][0],J_D_list[i][j+1][0]))
                        J_D_line_xy2.append((J_D_list[i][j][1],J_D_list[i][j+1][1]))

        J_D_line_z_list = []
        for i in range(len(J_D_line_z_xy1)):            
            J_D_line_z_list.append([J_D_line_z_xy1[i],J_D_line_z_xy2[i]])
        
        J_D_line_list = []
        for i in range(len(J_D_line_xy1)):            
            J_D_line_list.append([J_D_line_xy1[i],J_D_line_xy2[i]])
        
        lc_J_D_z = mc.LineCollection(J_D_line_z_list, colors='yellow', zorder=2+2.5)
        lc_J_D = mc.LineCollection(J_D_line_list, colors='white', zorder=2+2.5)
        lc_J_D_z.set_alpha(plot_alpha)
        lc_J_D.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_D_z)
        ax0.add_collection(lc_J_D)

        JDn_list = [[JD01n,'角宿'],[JD02n,'平道'],[JD03n,'天田'],[JD04n,'周鼎'],[JD05n,'進賢'],\
                    [JD06n,'天門'],[JD07n,'平'],[JD08n,'庫楼'],[JD09an,'柱'],[JD09bn,'柱'],\
                    [JD09cn,'柱'],[JD09dn,'柱'],[JD10n,'衡'],[JD11n,'南門'],[JD12n,'亢宿'],\
                    [JD13n,'大角'],[JD14n,'右摂提'],[JD15n,'左摂提'],[JD16n,'折威'],[JD17n,'頓頑'],\
                    [JD18n,'陽門'],[JD19n,'氐宿'],[JD20n,'亢池'],[JD21n,'帝座'],[JD22n,'梗河'],\
                    [JD23n,'招搖'],[JD24n,'天乳'],[JD25n,'天輻'],[JD26n,'陣車'],[JD27n,'騎官'],\
                    [JD28n,'車騎'],[JD29n,'将軍'],[JD30n,'房宿'],[JD31n,'鈎鈐'],[JD32n,'鍵閉'],\
                    [JD33n,'罰'],[JD34n,'西咸'],[JD35n,'東咸'],[JD36n,'日'],[JD37n,'従官'],\
                    [JD38n,'心宿'],[JD39n,'積卒'],[JD40n,'尾宿'],[JD41n,'神宮'],[JD42n,'天江'],\
                    [JD43n,'伝說'],[JD44n,'魚'],[JD45n,'亀'],[JD46n,'箕宿'],[JD47n,'糠'],\
                    [JD48n,'杵'],[JD49n,'左衛門'],[JD50n,'天湖'],[JD51n,'湯母'],[JD52n,'湯座'],\
                    [JD53n,'內侍'],[JD54n,'采女'],[JD55n,'腹赤']]

        for i in range(len(JDn_list)):
            if len(JDn_list[i][0]) != 0:
                if (JDn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JDn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JDn_list[i][0])-min(JDn_list[i][0]) < hori_border:
                    if i in set([0,14,21,32,40,42,48]):
                        ax_label.annotate(str(JDn_list[i][1]),(JDn_list[i][0][0],JDn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(JDn_list[i][1]),(JDn_list[i][0][0],JDn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #北宮玄武#
        ##########

        #斗宿　と# 
        J_E01 = [[Sgr.x[1],Sgr.x[8]],[Sgr.y[1],Sgr.y[8]],[Sgr.x[1],Sgr.x[9]],[Sgr.y[1],Sgr.y[9]],\
                 [Sgr.x[2],Sgr.x[9]],[Sgr.y[2],Sgr.y[9]],[Sgr.x[4],Sgr.x[8]],[Sgr.y[4],Sgr.y[8]],\
                 [Sgr.x[4],Sgr.x[12]],[Sgr.y[4],Sgr.y[12]]]
        JE01n = [numpy.mean([Sgr.x[1],Sgr.x[2],Sgr.x[4],Sgr.x[8],Sgr.x[9],Sgr.x[12]]),\
                 numpy.mean([Sgr.y[1],Sgr.y[2],Sgr.y[4],Sgr.y[8],Sgr.y[9],Sgr.y[12]])]
        #天籥　てんやく# 
        J_E02 = []
        JE02n = [Sgr.x[51],Sgr.y[51]-labelxy]
        #天弁　てんべん# 
        J_E03 = [[Aql.x[5],Aql.x[9]],[Aql.y[5],Aql.y[9]],[Aql.x[9],Sct.x[5]],[Aql.y[9],Sct.y[5]],\
                 [Sct.x[0],Sct.x[6]],[Sct.y[0],Sct.y[6]],[Sct.x[1],Sct.x[5]],[Sct.y[1],Sct.y[5]],\
                 [Sct.x[1],Sct.x[9]],[Sct.y[1],Sct.y[9]],[Sct.x[6],Sct.x[9]],[Sct.y[6],Sct.y[9]]]
        JE03n = [numpy.mean([Aql.x[5],Aql.x[9],Sct.x[0],Sct.x[1],Sct.x[5],Sct.x[6],Sct.x[9]]),\
                 numpy.mean([Aql.y[5],Aql.y[9],Sct.y[0],Sct.y[1],Sct.y[5],Sct.y[6],Sct.y[9]])]
        #建　けん# 
        J_E04 = [[Sgr.x[5],Sgr.x[11]],[Sgr.y[5],Sgr.y[11]],[Sgr.x[5],Sgr.x[36]],[Sgr.y[5],Sgr.y[36]],\
                 [Sgr.x[10],Sgr.x[11]],[Sgr.y[10],Sgr.y[11]],[Sgr.x[13],Sgr.x[24]],[Sgr.y[13],Sgr.y[24]],\
                 [Sgr.x[13],Sgr.x[36]],[Sgr.y[13],Sgr.y[36]]]
        JE04n = [numpy.mean([Sgr.x[5],Sgr.x[10],Sgr.x[11],Sgr.x[13],Sgr.x[24],Sgr.x[36]]),\
                 numpy.mean([Sgr.y[5],Sgr.y[10],Sgr.y[11],Sgr.y[13],Sgr.y[24],Sgr.y[36]])]
        #天鶏　てんけい# 
        J_E05 = [[Sgr.x[34],Sgr.x[42]],[Sgr.y[34],Sgr.y[42]]]
        JE05n = [numpy.mean([Sgr.x[34],Sgr.x[42]]),\
                 numpy.mean([Sgr.y[34],Sgr.y[42]])]
        #狗　こう# 
        J_E06 = [[Sgr.x[23],Sgr.x[41]],[Sgr.y[23],Sgr.y[41]]]
        JE06n = [numpy.mean([Sgr.x[23],Sgr.x[41]]),\
                 numpy.mean([Sgr.y[23],Sgr.y[41]])]
        #狗国　こうこく# 
        J_E07 = [[Sgr.x[19],Sgr.x[22]],[Sgr.y[19],Sgr.y[22]],[Sgr.x[19],Sgr.x[27]],[Sgr.y[19],Sgr.y[27]],\
                 [Sgr.x[22],Sgr.x[32]],[Sgr.y[22],Sgr.y[32]],[Sgr.x[27],Sgr.x[32]],[Sgr.y[27],Sgr.y[32]]]
        JE07n = [numpy.mean([Sgr.x[19],Sgr.x[22],Sgr.x[32],Sgr.x[27],Sgr.x[32]]),\
                 numpy.mean([Sgr.y[19],Sgr.y[22],Sgr.y[32],Sgr.y[27],Sgr.y[32]])]
        #天淵　てんえん# 
        J_E08 = [[Sgr.x[14],Sgr.x[18]],[Sgr.y[14],Sgr.y[18]]]
        JE08n = [numpy.mean([Sgr.x[14],Sgr.x[18]]),\
                 numpy.mean([Sgr.y[14],Sgr.y[18]])]
        #農丈人　のうじょうにん# 
        J_E09 = []
        JE09n = [] # ?
        #鼈　べつ# 
        J_E10 = [[CrA.x[0],CrA.x[1]],[CrA.y[0],CrA.y[1]],[CrA.x[0],CrA.x[7]],[CrA.y[0],CrA.y[7]],\
                 [CrA.x[1],CrA.x[2]],[CrA.y[1],CrA.y[2]],[CrA.x[2],CrA.x[4]],[CrA.y[2],CrA.y[4]],\
                 [CrA.x[3],CrA.x[14]],[CrA.y[3],CrA.y[14]],[CrA.x[3],CrA.x[22]],[CrA.y[3],CrA.y[22]],\
                 [CrA.x[4],CrA.x[13]],[CrA.y[4],CrA.y[13]],[CrA.x[7],CrA.x[15]],[CrA.y[7],CrA.y[15]],\
                 [CrA.x[9],CrA.x[15]],[CrA.y[9],CrA.y[15]],[CrA.x[9],CrA.x[22]],[CrA.y[9],CrA.y[22]],
                 [CrA.x[13],CrA.x[19]],[CrA.y[13],CrA.y[19]],[CrA.x[14],CrA.x[19]],[CrA.y[14],CrA.y[19]]]
        JE10n = [numpy.mean([CrA.x[0],CrA.x[1],CrA.x[2],CrA.x[3],CrA.x[4],CrA.x[7],CrA.x[9],CrA.x[13],\
                             CrA.x[14],CrA.x[15],CrA.x[19],CrA.x[22]]),\
                 numpy.mean([CrA.y[0],CrA.y[1],CrA.y[2],CrA.y[3],CrA.y[4],CrA.y[7],CrA.y[9],CrA.y[13],\
                             CrA.y[14],CrA.y[15],CrA.y[19],CrA.y[22]])]
        #牛宿　ぎゅう# 
        J_E11 = [[Cap.x[1],Cap.x[2]],[Cap.y[1],Cap.y[2]],[Cap.x[1],Cap.x[14]],[Cap.y[1],Cap.y[14]],\
                 [Cap.x[1],Cap.x[15]],[Cap.y[1],Cap.y[15]],[Cap.x[1],Cap.x[24]],[Cap.y[1],Cap.y[24]],\
                 [Cap.x[24],Cap.x[45]],[Cap.y[24],Cap.y[45]]]
        JE11n = [numpy.mean([Cap.x[1],Cap.x[2],Cap.x[14],Cap.x[15],Cap.x[24],Cap.x[45]]),\
                 numpy.mean([Cap.y[1],Cap.y[2],Cap.y[14],Cap.y[15],Cap.y[24],Cap.y[45]])]
        #天桴　てんぷ# 
        J_E12 = [[Aql.x[3],Aql.x[53]],[Aql.y[3],Aql.y[53]],[Aql.x[7],Aql.x[48]],[Aql.y[7],Aql.y[48]],\
                 [Aql.x[48],Aql.x[53]],[Aql.y[48],Aql.y[53]]]
        JE12n = [numpy.mean([Aql.x[3],Aql.x[7],Aql.x[48],Aql.x[53]]),\
                 numpy.mean([Aql.y[3],Aql.y[7],Aql.y[48],Aql.y[53]])]
        #河鼓　かこ# 
        J_E13 = [[Aql.x[0],Aql.x[1]],[Aql.y[0],Aql.y[1]],[Aql.x[0],Aql.x[6]],[Aql.y[0],Aql.y[6]]]
        JE13n = [numpy.mean([Aql.x[0],Aql.x[1],Aql.x[6]]),\
                 numpy.mean([Aql.y[0],Aql.y[1],Aql.y[6]])]
        #右旗　うき# 
        J_E14 = [[Aql.x[4],Aql.x[25]],[Aql.y[4],Aql.y[25]],[Aql.x[4],Aql.x[47]],[Aql.y[4],Aql.y[47]],\
                 [Aql.x[11],Aql.x[20]],[Aql.y[11],Aql.y[20]],[Aql.x[11],Aql.x[25]],[Aql.y[11],Aql.y[25]],\
                 [Aql.x[12],Aql.x[27]],[Aql.y[12],Aql.y[27]],[Aql.x[12],Aql.x[47]],[Aql.y[12],Aql.y[47]],\
                 [Aql.x[12],Aql.x[65]],[Aql.y[12],Aql.y[65]]]
        JE14n = [numpy.mean([Aql.x[4],Aql.x[11],Aql.x[12],Aql.x[20],Aql.x[25],Aql.x[27],Aql.x[47],Aql.x[65]]),\
                 numpy.mean([Aql.y[4],Aql.y[11],Aql.y[12],Aql.y[20],Aql.y[25],Aql.y[27],Aql.y[47],Aql.y[65]])]
        #左旗　さき# 
        J_E15 = [[Cyg.x[4],Cyg.x[28]],[Cyg.y[4],Cyg.y[28]],[Cyg.x[4],Vul.x[0]],[Cyg.y[4],Vul.y[0]],\
                 [Cyg.x[28],Vul.x[4]],[Cyg.y[28],Vul.y[4]],[Del.x[6],Sge.x[0]],[Del.y[6],Sge.y[0]],\
                 [Sge.x[0],Vul.x[2]],[Sge.y[0],Vul.y[2]],[Vul.x[0],Vul.x[5]],[Vul.y[0],Vul.y[5]],\
                 [Vul.x[0],Vul.x[10]],[Vul.y[0],Vul.y[10]],[Vul.x[2],Vul.x[4]],[Vul.y[2],Vul.y[4]]]
        JE15n = [numpy.mean([Cyg.x[4],Cyg.x[28],Del.x[6],Sge.x[0],Vul.x[0],Vul.x[2],Vul.x[4],Vul.x[5],\
                             Vul.x[10]]),\
                 numpy.mean([Cyg.y[4],Cyg.y[28],Del.y[6],Sge.y[0],Vul.y[0],Vul.y[2],Vul.y[4],Vul.y[5],\
                             Vul.y[10]])]
        #織女　しょくじょ# 
        J_E16 = [[Lyr.x[0],Lyr.x[6]],[Lyr.y[0],Lyr.y[6]],[Lyr.x[0],Lyr.x[12]],[Lyr.y[0],Lyr.y[12]]]
        JE16n = [numpy.mean([Lyr.x[0],Lyr.x[6],Lyr.x[12]]),\
                 numpy.mean([Lyr.y[0],Lyr.y[6],Lyr.y[12]])]
        #漸台　ぜんだい# 
        J_E17 = [[Lyr.x[1],Lyr.x[19]],[Lyr.y[1],Lyr.y[19]],[Lyr.x[2],Lyr.x[4]],[Lyr.y[2],Lyr.y[4]],\
                 [Lyr.x[4],Lyr.x[19]],[Lyr.y[4],Lyr.y[19]]]
        JE17n = [numpy.mean([Lyr.x[1],Lyr.x[2],Lyr.x[4],Lyr.x[19]]),\
                 numpy.mean([Lyr.y[1],Lyr.y[2],Lyr.y[4],Lyr.y[19]])]
        #輦道　ねんどう# 
        J_E18 = [[Cyg.x[30],Cyg.x[57]],[Cyg.y[30],Cyg.y[57]],[Cyg.x[57],Lyr.x[7]],[Cyg.y[57],Lyr.y[7]],\
                 [Lyr.x[3],Lyr.x[8]],[Lyr.y[3],Lyr.y[8]],[Lyr.x[7],Lyr.x[8]],[Lyr.y[7],Lyr.y[8]]]
        JE18n = [numpy.mean([Cyg.x[30],Cyg.x[57],Lyr.x[3],Lyr.x[7],Lyr.x[8]]),\
                 numpy.mean([Cyg.y[30],Cyg.y[57],Lyr.y[3],Lyr.y[7],Lyr.y[8]])]
        #羅堰　らえん# 
        J_E19 = [[Cap.x[19],Cap.x[21]],[Cap.y[19],Cap.y[21]]]
        JE19n = [numpy.mean([Cap.x[19],Cap.x[21]]),\
                 numpy.mean([Cap.y[19],Cap.y[21]])]
        #天田　てんでん#
        J_E20 = []
        JE20n = [] # ?
        #九坎　きゅうかん# ?
        J_E21 = []
        JE21n = [Pav.x[0],Pav.y[0]-labelxy]
        #女宿　じょ# 
        J_E22 = [[Aqr.x[5],Aqr.x[28]],[Aqr.y[5],Aqr.y[28]],[Aqr.x[16],Aqr.x[94]],[Aqr.y[16],Aqr.y[94]],\
                 [Aqr.x[28],Aqr.x[94]],[Aqr.y[28],Aqr.y[94]]]
        JE22n = [numpy.mean([Aqr.x[5],Aqr.x[16],Aqr.x[28],Aqr.x[94]]),\
                 numpy.mean([Aqr.y[5],Aqr.y[16],Aqr.y[28],Aqr.y[94]])]
        #離珠　りしゅ# 
        J_E23 = [[Aqr.x[38],Aql.x[33]],[Aqr.y[38],Aql.y[33]],[Aql.x[10],Aql.x[15]],[Aql.y[10],Aql.y[15]],\
                 [Aql.x[10],Aqr.x[38]],[Aql.y[10],Aqr.y[38]],[Aql.x[15],Aql.x[16]],[Aql.y[15],Aql.y[16]],\
                 [Aql.x[16],Aql.x[33]],[Aql.y[16],Aql.y[33]]]
        JE23n = [numpy.mean([Aqr.x[38],Aql.x[10],Aql.x[15],Aql.x[16],Aql.x[33],Aqr.x[38]]),\
                 numpy.mean([Aqr.y[38],Aql.y[10],Aql.y[15],Aql.y[16],Aql.y[33],Aqr.y[38]])]
        #敗瓜　はいか# 
        J_E24 = [[Del.x[2],Del.x[10]],[Del.y[2],Del.y[10]],[Del.x[2],Del.x[11]],[Del.y[2],Del.y[11]],\
                 [Del.x[10],Del.x[16]],[Del.y[10],Del.y[16]],[Del.x[11],Del.x[16]],[Del.y[11],Del.y[16]]]
        JE24n = [numpy.mean([Del.x[2],Del.x[10],Del.x[11],Del.x[16]]),\
                 numpy.mean([Del.y[2],Del.y[10],Del.y[11],Del.y[16]])]
        #瓠瓜　こか# 
        J_E25 = [[Del.x[0],Del.x[4]],[Del.y[0],Del.y[4]],[Del.x[0],Del.x[5]],[Del.y[0],Del.y[5]],\
                 [Del.x[1],Del.x[3]],[Del.y[1],Del.y[3]],[Del.x[1],Del.x[5]],[Del.y[1],Del.y[5]],\
                 [Del.x[3],Del.x[4]],[Del.y[3],Del.y[4]]]
        JE25n = [numpy.mean([Del.x[2],Del.x[10],Del.x[11],Del.x[16]]),\
                 numpy.mean([Del.y[2],Del.y[10],Del.y[11],Del.y[16]])]
        #天津　てんしん# 
        J_E26 = [[Cyg.x[0],Cyg.x[12]],[Cyg.y[0],Cyg.y[12]],[Cyg.x[0],Cyg.x[13]],[Cyg.y[0],Cyg.y[13]],\
                 [Cyg.x[1],Cyg.x[2]],[Cyg.y[1],Cyg.y[2]],[Cyg.x[1],Cyg.x[3]],[Cyg.y[1],Cyg.y[3]],\
                 [Cyg.x[2],Cyg.x[5]],[Cyg.y[2],Cyg.y[5]],[Cyg.x[3],Cyg.x[13]],[Cyg.y[3],Cyg.y[13]],\
                 [Cyg.x[5],Cyg.x[22]],[Cyg.y[5],Cyg.y[22]],[Cyg.x[7],Cyg.x[12]],[Cyg.y[7],Cyg.y[12]],\
                 [Cyg.x[7],Cyg.x[22]],[Cyg.y[7],Cyg.y[22]]]
        JE26n = [numpy.mean([Cyg.x[0],Cyg.x[1],Cyg.x[2],Cyg.x[3],Cyg.x[5],Cyg.x[7],Cyg.x[12],Cyg.x[13],\
                             Cyg.x[22]]),\
                 numpy.mean([Cyg.y[0],Cyg.y[1],Cyg.y[2],Cyg.y[3],Cyg.y[5],Cyg.y[7],Cyg.y[12],Cyg.y[13],\
                             Cyg.y[22]])]
        #奚仲　けいちゅう# 
        J_E27 = [[Cyg.x[9],Cyg.x[8]],[Cyg.y[9],Cyg.y[8]],[Cyg.x[9],Cyg.x[23]],[Cyg.y[9],Cyg.y[23]],\
                 [Cyg.x[23],Cyg.x[51]],[Cyg.y[23],Cyg.y[51]]]
        JE27n = [numpy.mean([Cyg.x[9],Cyg.x[8],Cyg.x[23],Cyg.x[51]]),\
                 numpy.mean([Cyg.y[9],Cyg.y[8],Cyg.y[23],Cyg.y[51]])]
        #扶筐　ふきょう# 
        J_E28 = [[Dra.x[20],Dra.x[80]],[Dra.y[20],Dra.y[80]],[Dra.x[20],Dra.x[121]],[Dra.y[20],Dra.y[121]],\
                 [Dra.x[22],Dra.x[36]],[Dra.y[22],Dra.y[36]],[Dra.x[22],Dra.x[42]],[Dra.y[22],Dra.y[42]],\
                 [Dra.x[36],Dra.x[121]],[Dra.y[36],Dra.y[121]],[Dra.x[46],Dra.x[80]],[Dra.y[46],Dra.y[80]]]
        JE28n = [numpy.mean([Dra.x[20],Dra.x[22],Dra.x[36],Dra.x[42],Dra.x[46],Dra.x[80],Dra.x[121]]),\
                 numpy.mean([Dra.y[20],Dra.y[22],Dra.y[36],Dra.y[42],Dra.y[46],Dra.y[80],Dra.y[121]])]
        #十二国　じゅうにこく#
        J_E29 = []
        JE29n = [numpy.mean([Cap.x[6],Cap.x[7],Cap.x[9],Cap.x[10],Cap.x[16],Cap.x[27],Cap.x[29]]),\
                 numpy.mean([Cap.y[6],Cap.y[7],Cap.y[9],Cap.y[10],Cap.y[16],Cap.y[27],Cap.y[29]])]
        #燕#
        J_E29a = []
        JE29an = [] # ?
        #周# 
        J_E29b = [[Cap.x[6],Cap.x[7]],[Cap.y[6],Cap.y[7]]]
        JE29bn = [numpy.mean([Cap.x[6],Cap.x[7]]),\
                  numpy.mean([Cap.y[6],Cap.y[7]])]
        #晉#
        J_E29c = []
        JE29cn = [] # ?
        #魏# 
        J_E29d = []
        JE29dn = [Cap.x[10],Cap.y[10]-labelxy]
        #楚#
        J_E29e = []
        JE29en = [] # ? 
        #齊#
        J_E29f = []
        JE29fn = [] # ?
        #韓#
        J_E29g = []
        JE29gn = [] # ?
        #越#
        J_E29h = []
        JE29hn = [] # ?
        #鄭#
        J_E29i = []
        JE29in = [] # ?
        #趙#
        J_E29j = []
        JE29jn = [] # ?
        #代# 
        J_E29k = [[Cap.x[9],Cap.x[29]],[Cap.y[9],Cap.y[29]]]
        JE29kn = [numpy.mean([Cap.x[9],Cap.x[29]]),\
                  numpy.mean([Cap.y[9],Cap.y[29]])]
        #秦# 
        J_E29l = [[Cap.x[16],Cap.x[27]],[Cap.y[16],Cap.y[27]]]
        JE29ln = [numpy.mean([Cap.x[16],Cap.x[27]]),\
                  numpy.mean([Cap.y[16],Cap.y[27]])]
        #虛宿　きょ# 
        J_E30 = [[Aqr.x[0],Equ.x[0]],[Aqr.y[0],Equ.y[0]]]
        JE30n = [numpy.mean([Aqr.x[0],Equ.x[0]]),\
                 numpy.mean([Aqr.y[0],Equ.y[0]])]
        #司命　しめい# 
        J_E31 = [[Aqr.x[36],Aqr.x[65]],[Aqr.y[36],Aqr.y[65]]]
        JE31n = [numpy.mean([Aqr.x[36],Aqr.x[65]]),\
                 numpy.mean([Aqr.y[36],Aqr.y[65]])]
        #司禄　しろく# 
        J_E32 = [[Peg.x[41],Peg.x[67]],[Peg.y[41],Peg.y[67]]]
        JE32n = [numpy.mean([Peg.x[41],Peg.x[67]]),\
                 numpy.mean([Peg.y[41],Peg.y[67]])]
        #司危　しき# 
        J_E33 = [[Equ.x[3],Equ.x[6]],[Equ.y[3],Equ.y[6]]]
        JE33n = [numpy.mean([Equ.x[3],Equ.x[6]]),\
                 numpy.mean([Equ.y[3],Equ.y[6]])]
        #司非　しひ# 
        J_E34 = [[Equ.x[1],Equ.x[2]],[Equ.y[1],Equ.y[2]]]
        JE34n = [numpy.mean([Equ.x[1],Equ.x[2]]),\
                 numpy.mean([Equ.y[1],Equ.y[2]])]
        #哭　こく# 
        J_E35 = [[Cap.x[4],Cap.x[11]],[Cap.y[4],Cap.y[11]]]
        JE35n = [numpy.mean([Cap.x[4],Cap.x[11]]),\
                 numpy.mean([Cap.y[4],Cap.y[11]])]
        #泣　きゅう# 
        J_E36 = [[Aqr.x[10],Aqr.x[50]],[Aqr.y[10],Aqr.y[50]]]
        JE36n = [numpy.mean([Aqr.x[10],Aqr.x[50]]),\
                 numpy.mean([Aqr.y[10],Aqr.y[50]])]
        #離瑜　りゆ# 
        J_E37 = [[Gru.x[2],Gru.x[9]],[Gru.y[2],Gru.y[9]],[Gru.x[9],Gru.x[10]],[Gru.y[9],Gru.y[10]]]
        JE37n = [numpy.mean([Gru.x[2],Gru.x[9],Gru.x[10]]),\
                 numpy.mean([Gru.y[2],Gru.y[9],Gru.y[10]])]
        #天塁城　てんるいじょう# 
        J_E38 = [[PsA.x[4],PsA.x[6]],[PsA.y[4],PsA.y[6]]]
        JE38n = [numpy.mean([PsA.x[4],PsA.x[6]]),\
                 numpy.mean([PsA.y[4],PsA.y[6]])]
        #敗臼　はいきゅう# 
        J_E39 = [[Gru.x[0],Gru.x[1]],[Gru.y[0],Gru.y[1]]]
        JE39n = [numpy.mean([Gru.x[0],Gru.x[1]]),\
                 numpy.mean([Gru.y[0],Gru.y[1]])]
        #危宿　き# 
        J_E40 = [[Aqr.x[1],Peg.x[7]],[Aqr.y[1],Peg.y[7]],[Peg.x[0],Peg.x[7]],[Peg.y[0],Peg.y[7]]]
        JE40n = [numpy.mean([Aqr.x[1],Peg.x[0],Peg.x[7]]),\
                 numpy.mean([Aqr.y[1],Peg.y[0],Peg.y[7]])]
        #墳墓　ふんぼ# 
        J_E41 = [[Aqr.x[6],Aqr.x[17]],[Aqr.y[6],Aqr.y[17]],[Aqr.x[9],Aqr.x[17]],[Aqr.y[9],Aqr.y[17]],\
                 [Aqr.x[17],Aqr.x[22]],[Aqr.y[17],Aqr.y[22]]]
        JE41n = [numpy.mean([Aqr.x[6],Aqr.x[9],Aqr.x[17],Aqr.x[22]]),\
                 numpy.mean([Aqr.y[6],Aqr.y[9],Aqr.y[17],Aqr.y[22]])]
        #蓋屋　がいおく# 
        J_E42 = []
        JE42n = [Aqr.x[24],Aqr.y[24]-labelxy]
        #虚梁　きょりょう# 
        J_E43 = []
        JE43n = [Aqr.x[155],Aqr.y[155]-labelxy]
        #天銭　てんせん# 
        J_E44 = [[Aqr.x[37],Aqr.x[47]],[Aqr.y[37],Aqr.y[47]],[Aqr.x[37],Aqr.x[56]],[Aqr.y[37],Aqr.y[56]]]
        JE44n = [numpy.mean([Aqr.x[37],Aqr.x[47],Aqr.x[56]]),\
                 numpy.mean([Aqr.y[37],Aqr.y[47],Aqr.y[56]])]
        #人　じん#
        J_E45 = [[Cyg.x[29],Peg.x[31]],[Cyg.y[29],Peg.y[31]],[Peg.x[11],Peg.x[31]],[Peg.y[11],Peg.y[31]],\
                 [Peg.x[31],Peg.x[33]],[Peg.y[31],Peg.y[33]],[Peg.x[31],Peg.x[53]],[Peg.y[31],Peg.y[53]]]
        JE45n = [numpy.mean([Cyg.x[29],Peg.x[11],Peg.x[31],Peg.x[33],Peg.x[53]]),\
                 numpy.mean([Cyg.y[29],Peg.y[11],Peg.y[31],Peg.y[33],Peg.y[53]])]
        #杵　しょ# 
        J_E46 = [[Lac.x[1],Peg.x[13]],[Lac.y[1],Peg.y[13]]]
        JE46n = [numpy.mean([Lac.x[1],Peg.x[13]]),\
                 numpy.mean([Lac.y[1],Peg.y[13]])]
        #臼　きゅう# 
        J_E47 = [[Peg.x[8],Peg.x[69]],[Peg.y[8],Peg.y[69]],[Peg.x[8],Peg.x[88]],[Peg.y[8],Peg.y[88]],\
                 [Peg.x[25],Peg.x[88]],[Peg.y[25],Peg.y[88]]]
        JE47n = [numpy.mean([Peg.x[8],Peg.x[25],Peg.x[69],Peg.x[88]]),\
                 numpy.mean([Peg.y[8],Peg.y[25],Peg.y[69],Peg.y[88]])]
        #車府　しゃふ# 
        J_E48 = [[Cyg.x[37],Cyg.x[92]],[Cyg.y[37],Cyg.y[92]],[Cyg.x[37],Lac.x[7]],[Cyg.y[37],Lac.y[7]]]
        JE48n = [numpy.mean([Cyg.x[37],Cyg.x[92],Lac.x[7]]),\
                 numpy.mean([Cyg.y[37],Cyg.y[92],Lac.y[7]])]
        #造父　ぞうほ# 
        J_E49 = [[Cep.x[3],Cep.x[6]],[Cep.y[3],Cep.y[6]],[Cep.x[6],Cep.x[8]],[Cep.y[6],Cep.y[8]],\
                 [Cep.x[6],Cep.x[24]],[Cep.y[6],Cep.y[24]],[Cep.x[6],Cep.x[39]],[Cep.y[6],Cep.y[39]]]
        JE49n = [numpy.mean([Cep.x[3],Cep.x[6],Cep.x[8],Cep.x[24],Cep.x[39]]),\
                 numpy.mean([Cep.y[3],Cep.y[6],Cep.y[8],Cep.y[24],Cep.y[39]])]
        #天鉤　てんこう# 
        J_E50 = [[Cep.x[0],Cep.x[4]],[Cep.y[0],Cep.y[4]],[Cep.x[0],Cep.x[22]],[Cep.y[0],Cep.y[22]],\
                 [Cep.x[4],Dra.x[91]],[Cep.y[4],Dra.y[91]],[Cep.x[5],Cep.x[22]],[Cep.y[5],Cep.y[22]],\
                 [Cep.x[5],Cep.x[35]],[Cep.y[5],Cep.y[35]],[Cep.x[9],Dra.x[91]],[Cep.y[9],Dra.y[91]],\
                 [Cep.x[20],Cep.x[35]],[Cep.y[20],Cep.y[35]]]
        JE50n = [numpy.mean([Cep.x[0],Cep.x[4],Cep.x[5],Cep.x[9],Cep.x[20],Cep.x[22],Cep.x[35],Dra.x[91]]),\
                 numpy.mean([Cep.y[0],Cep.y[4],Cep.y[5],Cep.y[9],Cep.y[20],Cep.y[22],Cep.y[35],Dra.y[91]])]
        #室宿　しつ# 
        J_E51 = [[Peg.x[1],Peg.x[2]],[Peg.y[1],Peg.y[2]]]
        JE51n = [numpy.mean([Peg.x[1],Peg.x[2]]),\
                 numpy.mean([Peg.y[1],Peg.y[2]])]
        #離宮　りきゅう# 
        J_E52 = [[Peg.x[1],Peg.x[6]],[Peg.y[1],Peg.y[6]],[Peg.x[1],Peg.x[19]],[Peg.y[1],Peg.y[19]],\
                 [Peg.x[1],Peg.x[23]],[Peg.y[1],Peg.y[23]],[Peg.x[4],Peg.x[23]],[Peg.y[4],Peg.y[23]],\
                 [Peg.x[15],Peg.x[19]],[Peg.y[15],Peg.y[19]]]
        JE52n = [numpy.mean([Peg.x[1],Peg.x[4],Peg.x[6],Peg.x[15],Peg.x[19],Peg.x[23]]),\
                 numpy.mean([Peg.y[1],Peg.y[4],Peg.y[6],Peg.y[15],Peg.y[19],Peg.y[23]])]
        #騰蛇　とうだ# 
        J_E53 = [[And.x[6],And.x[12]],[And.y[6],And.y[12]],[And.x[6],And.x[17]],[And.y[6],And.y[17]],\
                 [And.x[12],And.x[53]],[And.y[12],And.y[53]],[And.x[17],And.x[20]],[And.y[17],And.y[20]],\
                 [And.x[20],Lac.x[9]],[And.y[20],Lac.y[9]],[Cas.x[24],Lac.x[9]],[Cas.y[24],Lac.y[9]],\
                 [Lac.x[0],Lac.x[9]],[Lac.y[0],Lac.y[9]]]
        JE53n = [numpy.mean([And.x[6],And.x[12],And.x[17],And.x[20],And.x[53],Cas.x[24],Lac.x[0],Lac.x[9]]),\
                 numpy.mean([And.y[6],And.y[12],And.y[17],And.y[20],And.y[53],Cas.y[24],Lac.y[0],Lac.y[9]])]
        #雷電　らいでん# 
        J_E54 = [[Peg.x[16],Peg.x[27]],[Peg.y[16],Peg.y[27]],[Peg.x[16],Peg.x[38]],[Peg.y[16],Peg.y[38]],\
                 [Peg.x[17],Peg.x[34]],[Peg.y[17],Peg.y[34]],[Peg.x[27],Peg.x[37]],[Peg.y[27],Peg.y[37]],\
                 [Peg.x[34],Peg.x[38]],[Peg.y[34],Peg.y[38]]]
        JE54n = [numpy.mean([Peg.x[16],Peg.x[17],Peg.x[27],Peg.x[34],Peg.x[37],Peg.x[38]]),\
                 numpy.mean([Peg.y[16],Peg.y[17],Peg.y[27],Peg.y[34],Peg.y[37],Peg.y[38]])]
        #土公吏　どこうり# 
        J_E55 = [[Peg.x[5],Peg.x[12]],[Peg.y[5],Peg.y[12]]]
        JE55n = [numpy.mean([Peg.x[5],Peg.x[12]]),\
                 numpy.mean([Peg.y[5],Peg.y[12]])]
        #塁壁陣　るいへきじん# 
        J_E56 = [[Aqr.x[4],Aqr.x[12]],[Aqr.y[4],Aqr.y[12]],[Aqr.x[4],Aqr.x[29]],[Aqr.y[4],Aqr.y[29]],\
                 [Aqr.x[12],Psc.x[20]],[Aqr.y[12],Psc.y[20]],[Aqr.x[13],Aqr.x[29]],[Aqr.y[13],Aqr.y[29]],\
                 [Aqr.x[13],Cap.x[0]],[Aqr.y[13],Cap.y[0]],[Cap.x[0],Cap.x[3]],[Cap.y[0],Cap.y[3]],\
                 [Cap.x[0],Cap.x[13]],[Cap.y[0],Cap.y[13]],[Cap.x[3],Cap.x[12]],[Cap.y[3],Cap.y[12]],\
                 [Cap.x[12],Cap.x[13]],[Cap.y[12],Cap.y[13]],[Psc.x[8],Psc.x[14]],[Psc.y[8],Psc.y[14]],\
                 [Psc.x[8],Psc.x[20]],[Psc.y[8],Psc.y[20]],[Psc.x[14],Psc.x[26]],[Psc.y[14],Psc.y[26]],\
                 [Psc.x[20],Psc.x[26]],[Psc.y[20],Psc.y[26]]]
        JE56n = [numpy.mean([Aqr.x[4],Aqr.x[12],Aqr.x[13],Aqr.x[29],Cap.x[0],Cap.x[3],Cap.x[12],Cap.x[13],\
                             Psc.x[8],Psc.x[14],Psc.x[20],Psc.x[26]]),\
                 numpy.mean([Aqr.y[4],Aqr.y[12],Aqr.y[13],Aqr.y[29],Cap.y[0],Cap.y[3],Cap.y[12],Cap.y[13],\
                             Psc.y[8],Psc.y[14],Psc.y[20],Psc.y[26]])]
        #羽林軍　うりんぐん# 
        J_E57 = [[Aqr.x[2],Aqr.x[3]],[Aqr.y[2],Aqr.y[3]],[Aqr.x[2],Aqr.x[8]],[Aqr.y[2],Aqr.y[8]],\
                 [Aqr.x[2],Aqr.x[25]],[Aqr.y[2],Aqr.y[25]],[Aqr.x[2],Aqr.x[35]],[Aqr.y[2],Aqr.y[35]],\
                 [Aqr.x[3],Aqr.x[26]],[Aqr.y[3],Aqr.y[26]],[Aqr.x[7],Aqr.x[15]],[Aqr.y[7],Aqr.y[15]],\
                 [Aqr.x[7],Aqr.x[41]],[Aqr.y[7],Aqr.y[41]],[Aqr.x[8],Aqr.x[140]],[Aqr.y[8],Aqr.y[140]],\
                 [Aqr.x[11],Aqr.x[14]],[Aqr.y[11],Aqr.y[14]],[Aqr.x[14],Aqr.x[31]],[Aqr.y[14],Aqr.y[31]],\
                 [Aqr.x[18],Aqr.x[26]],[Aqr.y[18],Aqr.y[26]],[Aqr.x[19],Aqr.x[30]],[Aqr.y[19],Aqr.y[30]],\
                 [Aqr.x[19],Aqr.x[32]],[Aqr.y[19],Aqr.y[32]],[Aqr.x[25],Aqr.x[43]],[Aqr.y[25],Aqr.y[43]],\
                 [Aqr.x[30],Aqr.x[42]],[Aqr.y[30],Aqr.y[42]],[Aqr.x[31],Aqr.x[35]],[Aqr.y[31],Aqr.y[35]],\
                 [Aqr.x[32],Aqr.x[41]],[Aqr.y[32],Aqr.y[41]],[Aqr.x[35],Aqr.x[41]],[Aqr.y[35],Aqr.y[41]],\
                 [Aqr.x[42],Aqr.x[45]],[Aqr.y[42],Aqr.y[45]],[Aqr.x[45],Cet.x[16]],[Aqr.y[45],Cet.y[16]],\
                 [Aqr.x[45],Scl.x[3]],[Aqr.y[45],Scl.y[3]],[Aqr.x[73],Aqr.x[140]],[Aqr.y[73],Aqr.y[140]],\
                 [Cet.x[15],Cet.x[26]],[Cet.y[15],Cet.y[26]],[Cet.x[16],Cet.x[26]],[Cet.y[16],Cet.y[26]],\
                 [Cet.x[26],Cet.x[29]],[Cet.y[26],Cet.y[29]]]
        JE57n = [numpy.mean([Aqr.x[2],Aqr.x[3],Aqr.x[7],Aqr.x[8],Aqr.x[11],Aqr.x[14],Aqr.x[15],Aqr.x[18],\
                             Aqr.x[19],Aqr.x[25],Aqr.x[26],Aqr.x[30],Aqr.x[31],Aqr.x[32],Aqr.x[35],Aqr.x[41],\
                             Aqr.x[42],Aqr.x[43],Aqr.x[45],Aqr.x[73],Aqr.x[140],Cet.x[15],Cet.x[16],Cet.x[26],\
                             Cet.x[29],Scl.x[3]]),\
                 numpy.mean([Aqr.y[2],Aqr.y[3],Aqr.y[7],Aqr.y[8],Aqr.y[11],Aqr.y[14],Aqr.y[15],Aqr.y[18],\
                             Aqr.y[19],Aqr.y[25],Aqr.y[26],Aqr.y[30],Aqr.y[31],Aqr.y[32],Aqr.y[35],Aqr.y[41],\
                             Aqr.y[42],Aqr.y[43],Aqr.y[45],Aqr.y[73],Aqr.y[140],Cet.y[15],Cet.y[16],Cet.y[26],\
                             Cet.y[29],Scl.y[3]])]
        #天綱　てんこう# 
        J_E58 = []
        JE58n = [PsA.x[1],PsA.y[1]-labelxy]
        #北落師門　ほくらきしもん# 
        J_E59 = []
        JE59n = [PsA.x[0],PsA.y[0]-labelxy]
        #鈇鉞　ふえつ# 
        J_E60 = [[Scl.x[1],Scl.x[2]],[Scl.y[1],Scl.y[2]]]
        JE60n = [numpy.mean([Scl.x[1],Scl.x[2]]),\
                 numpy.mean([Scl.y[1],Scl.y[2]])]
        #八魁　はちかい# 
        J_E61 = [[Phe.x[0],Phe.x[5]],[Phe.y[0],Phe.y[5]]]
        JE61n = [numpy.mean([Phe.x[0],Phe.x[5]]),\
                 numpy.mean([Phe.y[0],Phe.y[5]])]
        #壁宿　へき# 
        J_E62 = [[And.x[0],Peg.x[3]],[And.y[0],Peg.y[3]]]
        JE62n = [numpy.mean([And.x[0],Peg.x[3]]),\
                 numpy.mean([And.y[0],Peg.y[3]])]
        #天厩　てんきゅう# 
        J_E63 = [[And.x[32],And.x[36]],[And.y[32],And.y[36]],[And.x[36],Cas.x[28]],[And.y[36],Cas.y[28]]]
        JE63n = [numpy.mean([And.x[32],And.x[36],Cas.x[28]]),\
                 numpy.mean([And.y[32],And.y[36],Cas.y[28]])]
        #土公　どこう# ?
        J_E64 = []
        JE64n = [Psc.x[46],Psc.y[46]-labelxy]
        #霹靂　へきれき# 
        J_E65 = [[Psc.x[1],Psc.x[6]],[Psc.y[1],Psc.y[6]],[Psc.x[1],Psc.x[13]],[Psc.y[1],Psc.y[13]],\
                 [Psc.x[2],Psc.x[3]],[Psc.y[2],Psc.y[3]],[Psc.x[3],Psc.x[6]],[Psc.y[3],Psc.y[6]]]
        JE65n = [numpy.mean([Psc.x[1],Psc.x[2],Psc.x[3],Psc.x[6],Psc.x[13]]),\
                 numpy.mean([Psc.y[1],Psc.y[2],Psc.y[3],Psc.y[6],Psc.y[13]])]
        #雲雨　うんう# 
        J_E66 = [[Psc.x[11],Psc.x[42]],[Psc.y[11],Psc.y[42]],[Psc.x[11],Psc.x[53]],[Psc.y[11],Psc.y[53]],\
                 [Psc.x[42],Psc.x[75]],[Psc.y[42],Psc.y[75]],[Psc.x[53],Psc.x[75]],[Psc.y[53],Psc.y[75]]]
        JE66n = [numpy.mean([Psc.x[11],Psc.x[42],Psc.x[53],Psc.x[75]]),\
                 numpy.mean([Psc.y[11],Psc.y[42],Psc.y[53],Psc.y[75]])]
        #鉄鑕　ふしつ# 
        J_E67 = [[Scl.x[0],Scl.x[13]],[Scl.y[0],Scl.y[13]]]
        JE67n = [numpy.mean([Scl.x[0],Scl.x[13]]),\
                 numpy.mean([Scl.y[0],Scl.y[13]])]
        #天蚕　てんさん#
        J_E68 = []
        JE68n = [] # ?
        #右京# 
        J_E69 = [[Cyg.x[14],Cyg.x[16]],[Cyg.y[14],Cyg.y[16]],[Cyg.x[14],Vul.x[1]],[Cyg.y[14],Vul.y[1]],\
                 [Cyg.x[16],Vul.x[3]],[Cyg.y[16],Vul.y[3]],[Vul.x[1],Vul.x[6]],[Vul.y[1],Vul.y[6]],\
                 [Vul.x[3],Vul.x[8]],[Vul.y[3],Vul.y[8]],[Vul.x[6],Vul.x[27]],[Vul.y[6],Vul.y[27]],\
                 [Vul.x[7],Vul.x[8]],[Vul.y[7],Vul.y[8]],[Vul.x[7],Vul.x[27]],[Vul.y[7],Vul.y[27]]]
        JE69n = [numpy.mean([Cyg.x[14],Cyg.x[16],Vul.x[1],Vul.x[3],Vul.x[6],Vul.x[7],Vul.x[8],Vul.x[27]]),\
                 numpy.mean([Cyg.y[14],Cyg.y[16],Vul.y[1],Vul.y[3],Vul.y[6],Vul.y[7],Vul.y[8],Vul.y[27]])]
        #左京# 
        J_E70 = [[Peg.x[10],Peg.x[14]],[Peg.y[10],Peg.y[14]],[Peg.x[10],Peg.x[18]],[Peg.y[10],Peg.y[18]],\
                 [Peg.x[14],Peg.x[40]],[Peg.y[14],Peg.y[40]],[Peg.x[18],Peg.x[39]],[Peg.y[18],Peg.y[39]],\
                 [Peg.x[39],Peg.x[40]],[Peg.y[39],Peg.y[40]]]
        JE70n = [numpy.mean([Peg.x[10],Peg.x[14],Peg.x[18],Peg.x[39],Peg.x[40]]),\
                 numpy.mean([Peg.x[10],Peg.x[14],Peg.x[18],Peg.x[39],Peg.x[40]])]
        #諸陵# 
        J_E71 = [[Aqr.x[62],Peg.x[26]],[Aqr.y[62],Peg.y[26]],[Peg.x[22],Peg.x[26]],[Peg.y[22],Peg.y[26]],\
                 [Peg.x[22],Peg.x[49]],[Peg.y[22],Peg.y[49]],[Peg.x[22],Peg.x[73]],[Peg.y[22],Peg.y[73]]]
        JE71n = [numpy.mean([Aqr.x[62],Peg.x[22],Peg.x[26],Peg.x[49],Peg.x[73]]),\
                 numpy.mean([Aqr.y[62],Peg.y[22],Peg.y[26],Peg.y[49],Peg.y[73]])]
        #右馬# ?
        J_E72 = [[And.x[5],And.x[34]],[And.y[5],And.y[34]],[And.x[5],Lac.x[35]],[And.y[5],Lac.y[35]],\
                 [And.x[34],Lac.x[11]],[And.y[34],Lac.y[11]],[Lac.x[4],Lac.x[6]],[Lac.y[4],Lac.y[6]],\
                 [Lac.x[4],Lac.x[11]],[Lac.y[4],Lac.y[11]],[Lac.x[10],Lac.x[35]],[Lac.y[10],Lac.y[35]],\
                 [Lac.x[11],Lac.x[13]],[Lac.y[11],Lac.y[13]]]
        JE72n = [numpy.mean([And.x[5],And.x[34],Lac.x[4],Lac.x[6],Lac.x[10],Lac.x[11],Lac.x[13],Lac.x[35]]),\
                 numpy.mean([And.y[5],And.y[34],Lac.y[4],Lac.y[6],Lac.y[10],Lac.y[11],Lac.y[13],Lac.y[35]])]
        #外衛# 
        J_E73 = [[Gru.x[5],PsA.x[3]],[Gru.y[5],PsA.y[3]],[PsA.x[2],PsA.x[5]],[PsA.y[2],PsA.y[5]],\
                 [PsA.x[3],PsA.x[5]],[PsA.y[3],PsA.y[5]]]
        JE73n = [numpy.mean([Gru.x[5],PsA.x[2],PsA.x[3],PsA.x[5]]),\
                 numpy.mean([Gru.y[5],PsA.y[2],PsA.y[3],PsA.y[5]])]
        #左馬# 
        J_E74 = [[And.x[16],And.x[37]],[And.y[16],And.y[37]],[And.x[19],And.x[37]],[And.y[19],And.y[37]]]
        JE74n = [numpy.mean([And.x[16],And.x[19],And.x[37]]),\
                 numpy.mean([And.y[16],And.y[19],And.y[37]])]

        J_E_list = [J_E01,J_E02,J_E03,J_E04,J_E05,J_E06,J_E07,J_E08,J_E09,J_E10,\
                    J_E11,J_E12,J_E13,J_E14,J_E15,J_E16,J_E17,J_E18,J_E19,J_E20,\
                    J_E21,J_E22,J_E23,J_E24,J_E25,J_E26,J_E27,J_E28,J_E29,J_E29a,\
                    J_E29b,J_E29c,J_E29d,J_E29e,J_E29f,J_E29g,J_E29h,J_E29i,J_E29j,J_E29k,\
                    J_E29l,J_E30,J_E31,J_E32,J_E33,J_E34,J_E35,J_E36,J_E37,J_E38,\
                    J_E39,J_E40,J_E41,J_E42,J_E43,J_E44,J_E45,J_E46,J_E47,J_E48,\
                    J_E49,J_E50,J_E51,J_E52,J_E53,J_E54,J_E55,J_E56,J_E57,J_E58,\
                    J_E59,J_E60,J_E61,J_E62,J_E63,J_E64,J_E65,J_E66,J_E67,J_E68,\
                    J_E69,J_E70,J_E71,J_E72,J_E73,J_E74]

        # 北宮玄武 linecollection
        J_E_line_z_xy1 = []
        J_E_line_z_xy2 = [] 
        J_E_line_xy1 = []
        J_E_line_xy2 = []        
        for i in range(len(J_E_list)):
            for j in range(len(J_E_list[i]))[0::2]:
                if math.hypot(J_E_list[i][j][0]-J_E_list[i][j][1],J_E_list[i][j+1][0]-J_E_list[i][j+1][1]) < hori_border:
                    if i in set([0,10,21,41,51,62,73]):
                        J_E_line_z_xy1.append((J_E_list[i][j][0],J_E_list[i][j+1][0]))
                        J_E_line_z_xy2.append((J_E_list[i][j][1],J_E_list[i][j+1][1]))
                    else:
                        J_E_line_xy1.append((J_E_list[i][j][0],J_E_list[i][j+1][0]))
                        J_E_line_xy2.append((J_E_list[i][j][1],J_E_list[i][j+1][1]))

        J_E_line_z_list = []
        for i in range(len(J_E_line_z_xy1)):            
            J_E_line_z_list.append([J_E_line_z_xy1[i],J_E_line_z_xy2[i]])
        
        J_E_line_list = []
        for i in range(len(J_E_line_xy1)):            
            J_E_line_list.append([J_E_line_xy1[i],J_E_line_xy2[i]])
        
        lc_J_E_z = mc.LineCollection(J_E_line_z_list, colors='yellow', zorder=2+2.5)
        lc_J_E = mc.LineCollection(J_E_line_list, colors='white', zorder=2+2.5)
        lc_J_E_z.set_alpha(plot_alpha)
        lc_J_E.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_E_z)
        ax0.add_collection(lc_J_E)

        JEn_list = [[JE01n,'斗宿'],[JE02n,'天籥'],[JE03n,'天弁'],[JE04n,'建'],[JE05n,'天鶏'],\
                    [JE06n,'狗'],[JE07n,'狗国'],[JE08n,'天淵'],[JE09n,'農丈人'],[JE10n,'鼈'],\
                    [JE11n,'牛宿'],[JE12n,'天桴'],[JE13n,'河鼓'],[JE14n,'右旗'],[JE15n,'左旗'],\
                    [JE16n,'織女'],[JE17n,'漸台'],[JE18n,'輦道'],[JE19n,'羅堰'],[JE20n,'天田'],\
                    [JE21n,'九坎'],[JE22n,'女宿'],[JE23n,'離珠'],[JE24n,'敗瓜'],[JE25n,'瓠瓜'],\
                    [JE26n,'天津'],[JE27n,'奚仲'],[JE28n,'扶筐'],[JE29n,'十二国'],[JE29an,'燕'],\
                    [JE29bn,'周'],[JE29cn,'晉'],[JE29dn,'魏'],[JE29en,'楚'],[JE29fn,'齊'],\
                    [JE29gn,'韓'],[JE29hn,'越'],[JE29in,'鄭'],[JE29jn,'趙'],[JE29kn,'代'],\
                    [JE29ln,'秦'],[JE30n,'虛宿'],[JE31n,'司命'],[JE32n,'司禄'],[JE33n,'司危'],\
                    [JE34n,'司非'],[JE35n,'哭'],[JE36n,'泣'],[JE37n,'離瑜'],[JE38n,'天塁城'],\
                    [JE39n,'敗臼'],[JE40n,'危宿'],[JE41n,'墳墓'],[JE42n,'蓋屋'],[JE43n,'虚梁'],\
                    [JE44n,'天銭'],[JE45n,'人'],[JE46n,'杵'],[JE47n,'臼'],[JE48n,'車府'],\
                    [JE49n,'造父'],[JE50n,'天鉤'],[JE51n,'室宿'],[JE52n,'離宮'],[JE53n,'騰蛇'],\
                    [JE54n,'雷電'],[JE55n,'土公吏'],[JE56n,'塁壁陣'],[JE57n,'羽林軍'],[JE58n,'天綱'],\
                    [JE59n,'北落師門'],[JE60n,'鈇鉞'],[JE61n,'八魁'],[JE62n,'壁宿'],[JE63n,'天厩'],\
                    [JE64n,'土公'],[JE65n,'霹靂'],[JE66n,'雲雨'],[JE67n,'鉄鑕'],[JE68n,'天蚕'],\
                    [JE69n,'右京'],[JE70n,'左京'],[JE71n,'諸陵'],[JE72n,'右馬'],[JE73n,'外衛'],\
                    [JE74n,'左馬']]

        for i in range(len(JEn_list)):
            if len(JEn_list[i][0]) != 0:
                if (JEn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JEn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JEn_list[i][0])-min(JEn_list[i][0]) < hori_border:
                    if i in set([0,10,21,41,51,62,73]):
                        ax_label.annotate(str(JEn_list[i][1]),(JEn_list[i][0][0],JEn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(JEn_list[i][1]),(JEn_list[i][0][0],JEn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #西宮白虎#
        ##########

        #奎宿　けい# 
        J_F01 = [[And.x[1],And.x[7]],[And.y[1],And.y[7]],[And.x[1],Psc.x[27]],[And.y[1],Psc.y[27]],\
                 [And.x[3],And.x[8]],[And.y[3],And.y[8]],[And.x[3],And.x[13]],[And.y[3],And.y[13]],\
                 [And.x[7],And.x[18]],[And.y[7],And.y[18]],[And.x[8],And.x[15]],[And.y[8],And.y[15]],\
                 [And.x[13],And.x[45]],[And.y[13],And.y[45]],[And.x[15],Psc.x[33]],[And.y[15],Psc.y[33]],\
                 [And.x[18],And.x[45]],[And.y[18],And.y[45]],[Psc.x[12],Psc.x[18]],[Psc.y[12],Psc.y[18]],\
                 [Psc.x[12],Psc.x[27]],[Psc.y[12],Psc.y[27]],[Psc.x[16],Psc.x[18]],[Psc.y[16],Psc.y[18]],\
                 [Psc.x[16],Psc.x[33]],[Psc.y[16],Psc.y[33]]]
        JF01n = [numpy.mean([And.x[1],And.x[3],And.x[7],And.x[8],And.x[13],And.x[15],And.x[18],And.x[45],\
                             Psc.x[12],Psc.x[16],Psc.x[18],Psc.x[27],Psc.x[33]]),\
                 numpy.mean([And.y[1],And.y[3],And.y[7],And.y[8],And.y[13],And.y[15],And.y[18],And.y[45],\
                             Psc.y[12],Psc.y[16],Psc.y[18],Psc.y[27],Psc.y[33]])]
        #王良　おうりょう# 
        J_F02 = [[Cas.x[0],Cas.x[1]],[Cas.y[0],Cas.y[1]],[Cas.x[0],Cas.x[5]],[Cas.y[0],Cas.y[5]],\
                 [Cas.x[1],Cas.x[2]],[Cas.y[1],Cas.y[2]],[Cas.x[2],Cas.x[21]],[Cas.y[2],Cas.y[21]],\
                 [Cas.x[5],Cas.x[21]],[Cas.y[5],Cas.y[21]]]
        JF02n = [numpy.mean([Cas.x[0],Cas.x[1],Cas.x[2],Cas.x[5],Cas.x[21]]),\
                 numpy.mean([Cas.y[0],Cas.y[1],Cas.y[2],Cas.y[5],Cas.y[21]])]
        #策　さく# 
        J_F03 = []
        JF03n = [Cas.x[8],Cas.y[8]-labelxy]
        #附路　ふろ# 
        J_F04 = []
        JF04n = [Cas.x[6],Cas.y[6]-labelxy]
        #軍南門　ぐんなんもん# 
        J_F05 = []
        JF05n = [Tri.x[1],Tri.y[1]-labelxy]
        #閣道　かくどう# 
        J_F06 = [[Cas.x[3],Cas.x[4]],[Cas.y[3],Cas.y[4]],[Cas.x[3],Cas.x[29]],[Cas.y[3],Cas.y[29]],\
                 [Cas.x[4],Cas.x[38]],[Cas.y[4],Cas.y[38]],[Cas.x[9],Cas.x[26]],[Cas.y[9],Cas.y[26]],\
                 [Cas.x[9],Cas.x[29]],[Cas.y[9],Cas.y[29]]]
        JF06n = [numpy.mean([Cas.x[3],Cas.x[4],Cas.x[9],Cas.x[26],Cas.x[29],Cas.x[38]]),\
                 numpy.mean([Cas.y[3],Cas.y[4],Cas.y[9],Cas.y[26],Cas.y[29],Cas.y[38]])]
        #外屏　がいへい# 
        J_F07 = [[Psc.x[5],Psc.x[9]],[Psc.y[5],Psc.y[9]],[Psc.x[5],Psc.x[31]],[Psc.y[5],Psc.y[31]],\
                 [Psc.x[7],Psc.x[15]],[Psc.y[7],Psc.y[15]],[Psc.x[10],Psc.x[15]],[Psc.y[10],Psc.y[15]],\
                 [Psc.x[10],Psc.x[19]],[Psc.y[10],Psc.y[19]],[Psc.x[19],Psc.x[31]],[Psc.y[19],Psc.y[31]]]
        JF07n = [numpy.mean([Psc.x[5],Psc.x[7],Psc.x[9],Psc.x[10],Psc.x[15],Psc.x[19],Psc.x[31]]),\
                 numpy.mean([Psc.y[5],Psc.y[7],Psc.y[9],Psc.y[10],Psc.y[15],Psc.y[19],Psc.y[31]])]
        #天溷　てんこん# ?
        J_F08 = [[Cet.x[21],Cet.x[51]],[Cet.y[21],Cet.y[51]],[Cet.x[47],Cet.x[51]],[Cet.y[47],Cet.y[51]],\
                 [Cet.x[47],Cet.x[94]],[Cet.y[47],Cet.y[94]],[Cet.x[94],Cet.x[105]],[Cet.y[94],Cet.y[105]]]
        JF08n = [numpy.mean([Cet.x[21],Cet.x[47],Cet.x[51],Cet.x[94],Cet.x[105]]),\
                 numpy.mean([Cet.y[21],Cet.y[47],Cet.y[51],Cet.y[94],Cet.y[105]])]
        #土司空　どしくう# 
        J_F09 = []
        JF09n = [Cet.x[0],Cet.y[0]-labelxy]
        #婁宿　ろう# 
        J_F10 = [[Ari.x[0],Ari.x[1]],[Ari.y[0],Ari.y[1]],[Ari.x[1],Ari.x[9]],[Ari.y[1],Ari.y[9]]]
        JF10n = [numpy.mean([Ari.x[0],Ari.x[1],Ari.x[9]]),\
                 numpy.mean([Ari.y[0],Ari.y[1],Ari.y[9]])]
        #天大将軍　てんだいしょうぐん# 
        J_F11 = [[And.x[2],Per.x[15]],[And.y[2],Per.y[15]],[And.x[2],Tri.x[3]],[And.y[2],Tri.y[3]],\
                 [And.x[4],Per.x[15]],[And.y[4],Per.y[15]],[And.x[4],And.x[41]],[And.y[4],And.y[41]],\
                 [And.x[9],And.x[28]],[And.y[9],And.y[28]],[And.x[9],And.x[31]],[And.y[9],And.y[31]],\
                 [And.x[22],And.x[57]],[And.y[22],And.y[57]],[And.x[22],Tri.x[0]],[And.y[22],Tri.y[0]],\
                 [And.x[23],And.x[31]],[And.y[23],And.y[31]],[And.x[23],And.x[41]],[And.y[23],And.y[41]],\
                 [And.x[28],And.x[57]],[And.y[28],And.y[57]],[Tri.x[0],Tri.x[2]],[Tri.y[0],Tri.y[2]],\
                 [Tri.x[2],Tri.x[3]],[Tri.y[2],Tri.y[3]]]
        JF11n = [numpy.mean([And.x[2],And.x[4],And.x[9],And.x[22],And.x[23],And.x[28],And.x[31],And.x[41],\
                             And.x[57],Per.x[15],Tri.x[0],Tri.x[2],Tri.x[3]]),\
                 numpy.mean([And.y[2],And.y[4],And.y[9],And.y[22],And.y[23],And.y[28],And.y[31],And.y[41],\
                             And.y[57],Per.y[15],Tri.y[0],Tri.y[2],Tri.y[3]])]
        #右更　ゆうこう# 
        J_F12 = [[Psc.x[0],Psc.x[45]],[Psc.y[0],Psc.y[45]],[Psc.x[0],Psc.x[52]],[Psc.y[0],Psc.y[52]],\
                 [Psc.x[4],Psc.x[52]],[Psc.y[4],Psc.y[52]],[Psc.x[32],Psc.x[45]],[Psc.y[32],Psc.y[45]]]
        JF12n = [numpy.mean([Psc.x[0],Psc.x[4],Psc.x[32],Psc.x[45],Psc.x[52]]),\
                 numpy.mean([Psc.y[0],Psc.y[4],Psc.y[32],Psc.y[45],Psc.y[52]])]
        #左更　さこう# 
        J_F13 = [[Ari.x[14],Ari.x[19]],[Ari.y[14],Ari.y[19]],[Ari.x[19],Ari.x[35]],[Ari.y[19],Ari.y[35]]]
        JF13n = [numpy.mean([Ari.x[14],Ari.x[19],Ari.x[35]]),\
                 numpy.mean([Ari.y[14],Ari.y[19],Ari.y[35]])]
        #天倉　てんそう# 
        J_F14 = [[Cet.x[3],Cet.x[6]],[Cet.y[3],Cet.y[6]],[Cet.x[3],Cet.x[7]],[Cet.y[3],Cet.y[7]],\
                 [Cet.x[5],Cet.x[8]],[Cet.y[5],Cet.y[8]],[Cet.x[5],Cet.x[9]],[Cet.y[5],Cet.y[9]],\
                 [Cet.x[7],Cet.x[8]],[Cet.y[7],Cet.y[8]]]
        JF14n = [numpy.mean([Cet.x[3],Cet.x[5],Cet.x[6],Cet.x[7],Cet.x[8],Cet.x[9]]),\
                 numpy.mean([Cet.y[3],Cet.y[5],Cet.y[6],Cet.y[7],Cet.y[8],Cet.y[9]])]
        #天庾　てんそう# 
        J_F15 = [[For.x[2],For.x[7]],[For.y[2],For.y[7]],[For.x[2],For.x[8]],[For.y[2],For.y[8]]]
        JF15n = [numpy.mean([For.x[2],For.x[7],For.x[8]]),\
                 numpy.mean([For.y[2],For.y[7],For.y[8]])]
        #胃宿　い# 
        J_F16 = [[Ari.x[2],Ari.x[5]],[Ari.y[2],Ari.y[5]],[Ari.x[5],Ari.x[8]],[Ari.y[5],Ari.y[8]]]
        JF16n = [numpy.mean([Ari.x[2],Ari.x[5],Ari.x[8]]),\
                 numpy.mean([Ari.y[2],Ari.y[5],Ari.y[8]])]
        #大陵　たいりょう# 
        J_F17 = [[And.x[21],Per.x[16]],[And.y[21],Per.y[16]],[Per.x[1],Per.x[6]],[Per.y[1],Per.y[6]],\
                 [Per.x[1],Per.x[9]],[Per.y[1],Per.y[9]],[Per.x[6],Per.x[18]],[Per.y[6],Per.y[18]],\
                 [Per.x[9],Per.x[16]],[Per.y[9],Per.y[16]],[Per.x[18],Per.x[32]],[Per.y[18],Per.y[32]]]
        JF17n = [numpy.mean([And.x[21],Per.x[1],Per.x[6],Per.x[9],Per.x[16],Per.x[18],Per.x[32]]),\
                 numpy.mean([And.y[21],Per.y[1],Per.y[6],Per.y[9],Per.y[16],Per.y[18],Per.y[32]])]
        #積尸　せきし# 
        J_F18 = []
        JF18n = [Per.x[27],Per.y[27]-labelxy]
        #天船　てんせん# 
        J_F19 = [[Per.x[0],Per.x[4]],[Per.y[0],Per.y[4]],[Per.x[0],Per.x[5]],[Per.y[0],Per.y[5]],\
                 [Per.x[4],Per.x[7]],[Per.y[4],Per.y[7]],[Per.x[5],Per.x[13]],[Per.y[5],Per.y[13]],\
                 [Per.x[7],Per.x[44]],[Per.y[7],Per.y[44]],[Per.x[13],Per.x[17]],[Per.y[13],Per.y[17]],\
                 [Per.x[17],Per.x[24]],[Per.y[17],Per.y[24]]]
        JF19n = [numpy.mean([Per.x[0],Per.x[4],Per.x[5],Per.x[7],Per.x[13],Per.x[17],Per.x[24],Per.x[44]]),\
                 numpy.mean([Per.y[0],Per.y[4],Per.y[5],Per.y[7],Per.y[13],Per.y[17],Per.y[24],Per.y[44]])]
        #積水　せきすい# 
        J_F20 = []
        JF20n = [Per.x[21],Per.y[21]-labelxy]
        #天廩　てんりん# 
        J_F21 = [[Tau.x[7],Tau.x[11]],[Tau.y[7],Tau.y[11]],[Tau.x[11],Tau.x[55]],[Tau.y[11],Tau.y[55]],\
                 [Tau.x[16],Tau.x[55]],[Tau.y[16],Tau.y[55]]]
        JF21n = [numpy.mean([Tau.x[7],Tau.x[11],Tau.x[16],Tau.x[55]]),\
                 numpy.mean([Tau.y[7],Tau.y[11],Tau.y[16],Tau.y[55]])]
        #天囷　てんきん# 
        J_F22 = [[Cet.x[1],Cet.x[22]],[Cet.y[1],Cet.y[22]],[Cet.x[1],Cet.x[4]],[Cet.y[1],Cet.y[4]],\
                 [Cet.x[2],Cet.x[10]],[Cet.y[2],Cet.y[10]],[Cet.x[4],Cet.x[10]],[Cet.y[4],Cet.y[10]],\
                 [Cet.x[4],Cet.x[25]],[Cet.y[4],Cet.y[25]],[Cet.x[12],Cet.x[13]],[Cet.y[12],Cet.y[13]],\
                 [Cet.x[12],Cet.x[18]],[Cet.y[12],Cet.y[18]],[Cet.x[13],Cet.x[14]],[Cet.y[13],Cet.y[14]],\
                 [Cet.x[13],Cet.x[25]],[Cet.y[13],Cet.y[25]],[Cet.x[18],Cet.x[60]],[Cet.y[18],Cet.y[60]],\
                 [Cet.x[22],Cet.x[60]],[Cet.y[22],Cet.y[60]]]
        JF22n = [numpy.mean([Cet.x[1],Cet.x[2],Cet.x[4],Cet.x[10],Cet.x[12],Cet.x[13],Cet.x[14],Cet.x[18],\
                             Cet.x[22],Cet.x[25],Cet.x[60]]),\
                 numpy.mean([Cet.y[1],Cet.y[2],Cet.y[4],Cet.y[10],Cet.y[12],Cet.y[13],Cet.y[14],Cet.y[18],\
                             Cet.y[22],Cet.y[25],Cet.y[60]])]
        #昴宿　ぼう# 
        J_F23 = []
        JF23n = [numpy.mean([Tau.x[2],Tau.x[8],Tau.x[10],Tau.x[14],Tau.x[17],Tau.x[26],Tau.x[52]]),\
                 numpy.mean([Tau.y[2],Tau.y[8],Tau.y[10],Tau.y[14],Tau.y[17],Tau.y[26],Tau.y[52]])]
        #天阿　てんお# 
        J_F24 = []
        JF24n = [Ari.x[27],Ari.y[27]-labelxy]
        #月　げつ# 
        J_F25 = []
        JF25n = [Tau.x[27],Tau.y[27]-labelxy]
        #卷舌　かんぜつ# 
        J_F26 = [[Per.x[2],Per.x[10]],[Per.y[2],Per.y[10]],[Per.x[2],Per.x[12]],[Per.y[2],Per.y[12]],\
                 [Per.x[3],Per.x[8]],[Per.y[3],Per.y[8]],[Per.x[3],Per.x[12]],[Per.y[3],Per.y[12]],\
                 [Per.x[10],Per.x[36]],[Per.y[10],Per.y[36]]]
        JF26n = [numpy.mean([Per.x[2],Per.x[3],Per.x[8],Per.x[10],Per.x[12],Per.x[36]]),\
                 numpy.mean([Per.y[2],Per.y[3],Per.y[8],Per.y[10],Per.y[12],Per.y[36]])]
        #天讒　てんざん# 
        J_F27 = []
        JF27n = [Per.x[42],Per.y[42]-labelxy]
        #蠣石　れいせき# 
        J_F28 = [[Tau.x[57],Tau.x[59]],[Tau.y[57],Tau.y[59]],[Tau.x[57],Tau.x[76]],[Tau.y[57],Tau.y[76]],\
                 [Tau.x[71],Tau.x[76]],[Tau.y[71],Tau.y[76]]]
        JF28n = [numpy.mean([Tau.x[57],Tau.x[59],Tau.x[71],Tau.x[76]]),\
                 numpy.mean([Tau.y[57],Tau.y[59],Tau.y[71],Tau.y[76]])]
        #天陰　てんいん# ?
        J_F29 = [[Ari.x[3],Ari.x[15]],[Ari.y[3],Ari.y[15]],[Ari.x[12],Ari.x[15]],[Ari.y[12],Ari.y[15]],\
                 [Ari.x[15],Ari.x[20]],[Ari.y[15],Ari.y[20]]]
        JF29n = [numpy.mean([Ari.x[3],Ari.x[12],Ari.x[15],Ari.x[20]]),\
                 numpy.mean([Ari.y[3],Ari.y[12],Ari.y[15],Ari.y[20]])]
        #芻藁　すうこう# 
        J_F30 = [[Cet.x[19],Cet.x[27]],[Cet.y[19],Cet.y[27]],[Cet.x[23],Cet.x[27]],[Cet.y[23],Cet.y[27]]]
        JF30n = [numpy.mean([Cet.x[19],Cet.x[23],Cet.x[27]]),\
                 numpy.mean([Cet.y[19],Cet.y[23],Cet.y[27]])]
        #天苑　てんえん# 
        J_F31 = [[Cet.x[11],Eri.x[12]],[Cet.y[11],Eri.y[12]],[Cet.x[11],Eri.x[30]],[Cet.y[11],Eri.y[30]],\
                 [Eri.x[2],Eri.x[28]],[Eri.y[2],Eri.y[28]],[Eri.x[4],Eri.x[9]],[Eri.y[4],Eri.y[9]],\
                 [Eri.x[4],Eri.x[28]],[Eri.y[4],Eri.y[28]],[Eri.x[7],Eri.x[17]],[Eri.y[7],Eri.y[17]],\
                 [Eri.x[7],Eri.x[23]],[Eri.y[7],Eri.y[23]],[Eri.x[9],Eri.x[42]],[Eri.y[9],Eri.y[42]],\
                 [Eri.x[12],Eri.x[42]],[Eri.y[12],Eri.y[42]],[Eri.x[17],Eri.x[39]],[Eri.y[17],Eri.y[39]],\
                 [Eri.x[20],Eri.x[23]],[Eri.y[20],Eri.y[23]],[Eri.x[20],Eri.x[59]],[Eri.y[20],Eri.y[59]],\
                 [Eri.x[30],Eri.x[39]],[Eri.y[30],Eri.y[39]],[Eri.x[34],Eri.x[35]],[Eri.y[34],Eri.y[35]],\
                 [Eri.x[34],Eri.x[59]],[Eri.y[34],Eri.y[59]]]
        JF31n = [numpy.mean([Cet.x[11],Eri.x[2],Eri.x[4],Eri.x[7],Eri.x[9],Eri.x[12],Eri.x[17],Eri.x[20],\
                             Eri.x[23],Eri.x[28],Eri.x[30],Eri.x[34],Eri.x[35],Eri.x[39],Eri.x[42],Eri.x[59]]),\
                 numpy.mean([Cet.y[11],Eri.y[2],Eri.y[4],Eri.y[7],Eri.y[9],Eri.y[12],Eri.y[17],Eri.y[20],\
                             Eri.y[23],Eri.y[28],Eri.y[30],Eri.y[34],Eri.y[35],Eri.y[39],Eri.y[42],Eri.y[59]])]
        #畢宿　ひつ# 
        J_F32 = [[Tau.x[0],Tau.x[13]],[Tau.y[0],Tau.y[13]],[Tau.x[5],Tau.x[9]],[Tau.y[5],Tau.y[9]],\
                 [Tau.x[6],Tau.x[25]],[Tau.y[6],Tau.y[25]],[Tau.x[9],Tau.x[13]],[Tau.y[9],Tau.y[13]],\
                 [Tau.x[9],Tau.x[36]],[Tau.y[9],Tau.y[36]],[Tau.x[25],Tau.x[36]],[Tau.y[25],Tau.y[36]]]
        JF32n = [numpy.mean([Tau.x[0],Tau.x[5],Tau.x[6],Tau.x[9],Tau.x[13],Tau.x[25],Tau.x[36]]),\
                 numpy.mean([Tau.y[0],Tau.y[5],Tau.y[6],Tau.y[9],Tau.y[13],Tau.y[25],Tau.y[36]])]
        #附耳　ふじ# 
        J_F33 = []
        JF33n = [Tau.x[34],Tau.y[34]-labelxy]
        #天街　てんがい# 
        J_F34 = []
        JF34n = [Tau.x[18],Tau.y[18]-labelxy]
        #天高　てんこう# 
        J_F35 = [[Tau.x[48],Tau.x[53]],[Tau.y[48],Tau.y[53]],[Tau.x[48],Tau.x[65]],[Tau.y[48],Tau.y[65]]]
        JF35n = [numpy.mean([Tau.x[48],Tau.x[53],Tau.x[65]]),\
                 numpy.mean([Tau.y[48],Tau.y[53],Tau.y[65]])]
        #諸王　しょおう# 
        J_F36 = [[Tau.x[3],Tau.x[41]],[Tau.y[3],Tau.y[41]],[Tau.x[23],Tau.x[31]],[Tau.y[23],Tau.y[31]],\
                 [Tau.x[31],Tau.x[127]],[Tau.y[31],Tau.y[127]],[Tau.x[41],Tau.x[44]],[Tau.y[41],Tau.y[44]],\
                 [Tau.x[44],Tau.x[127]],[Tau.y[44],Tau.y[127]]]
        JF36n = [numpy.mean([Tau.x[3],Tau.x[23],Tau.x[31],Tau.x[41],Tau.x[44],Tau.x[127]]),\
                 numpy.mean([Tau.y[3],Tau.y[23],Tau.y[31],Tau.y[41],Tau.y[44],Tau.y[127]])]
        #五車　ごしゃ# 
        J_F37 = [[Aur.x[0],Aur.x[1]],[Aur.y[0],Aur.y[1]],[Aur.x[0],Aur.x[5]],[Aur.y[0],Aur.y[5]],\
                 [Aur.x[1],Aur.x[2]],[Aur.y[1],Aur.y[2]],[Aur.x[2],Tau.x[1]],[Aur.y[2],Tau.y[1]],\
                 [Aur.x[3],Aur.x[5]],[Aur.y[3],Aur.y[5]],[Aur.x[3],Tau.x[1]],[Aur.y[3],Tau.y[1]]]
        JF37n = [numpy.mean([Aur.x[0],Aur.x[1],Aur.x[2],Aur.x[3],Aur.x[5],Tau.x[1]]),\
                 numpy.mean([Aur.y[0],Aur.y[1],Aur.y[2],Aur.y[3],Aur.y[5],Tau.y[1]])]
        #柱　ちゅう# 
        J_F38 = [[Aur.x[4],Aur.x[5]],[Aur.y[4],Aur.y[5]],[Aur.x[4],Aur.x[7]],[Aur.y[4],Aur.y[7]],\
                 [Aur.x[8],Aur.x[14]],[Aur.y[8],Aur.y[14]],[Aur.x[11],Aur.x[14]],[Aur.y[11],Aur.y[14]],\
                 [Aur.x[15],Aur.x[41]],[Aur.y[15],Aur.y[41]]]
        JF38an = [numpy.mean([Aur.x[4],Aur.x[5],Aur.x[7]]),\
                  numpy.mean([Aur.y[4],Aur.y[5],Aur.y[7]])]
        JF38bn = [numpy.mean([Aur.x[8],Aur.x[11],Aur.x[14]]),\
                  numpy.mean([Aur.y[8],Aur.y[11],Aur.y[14]])]
        JF38cn = [numpy.mean([Aur.x[15],Aur.x[41]]),\
                  numpy.mean([Aur.y[15],Aur.y[41]])]
        #咸池　かんち# 
        J_F39 = [[Aur.x[13],Aur.x[18]],[Aur.y[13],Aur.y[18]],[Aur.x[13],Aur.x[23]],[Aur.y[13],Aur.y[23]],\
                 [Aur.x[18],Aur.x[23]],[Aur.y[18],Aur.y[23]]]
        JF39n = [numpy.mean([Aur.x[13],Aur.x[18],Aur.x[23]]),\
                 numpy.mean([Aur.y[13],Aur.y[18],Aur.y[23]])]
        #天潢　てんこう# 
        J_F40 = []
        JF40n = [Aur.x[29],Aur.y[29]-labelxy]
        #天関　てんかん# 
        J_F41 = []
        JF41n = [Tau.x[28],Tau.y[28]-labelxy]
        #天節　てんせつ# 
        J_F42 = [[Tau.x[19],Tau.x[20]],[Tau.y[19],Tau.y[20]],[Tau.x[19],Tau.x[54]],[Tau.y[19],Tau.y[54]],\
                 [Tau.x[20],Tau.x[75]],[Tau.y[20],Tau.y[75]],[Tau.x[24],Tau.x[54]],[Tau.y[24],Tau.y[54]],\
                 [Tau.x[29],Tau.x[61]],[Tau.y[29],Tau.y[61]],[Tau.x[29],Tau.x[85]],[Tau.y[29],Tau.y[85]],\
                 [Tau.x[75],Tau.x[85]],[Tau.y[75],Tau.y[85]]]
        JF42n = [numpy.mean([Aur.x[13],Aur.x[18],Aur.x[23]]),\
                 numpy.mean([Aur.y[13],Aur.y[18],Aur.y[23]])]
        #九州珠口　きゅうしゅうしゅこう# 
        J_F43 = [[Eri.x[11],Eri.x[44]],[Eri.y[11],Eri.y[44]],[Eri.x[11],Eri.x[47]],[Eri.y[11],Eri.y[47]],\
                 [Eri.x[16],Eri.x[29]],[Eri.y[16],Eri.y[29]],[Eri.x[16],Eri.x[44]],[Eri.y[16],Eri.y[44]],\
                 [Eri.x[29],Eri.x[55]],[Eri.y[29],Eri.y[55]],[Eri.x[47],Eri.x[118]],[Eri.y[47],Eri.y[118]],\
                 [Eri.x[55],Eri.x[95]],[Eri.y[55],Eri.y[95]],[Eri.x[95],Eri.x[118]],[Eri.y[95],Eri.y[118]]]
        JF43n = [numpy.mean([Eri.x[11],Eri.x[16],Eri.x[29],Eri.x[44],Eri.x[47],Eri.x[55],Eri.x[95],Eri.x[118]]),\
                 numpy.mean([Eri.y[11],Eri.y[16],Eri.y[29],Eri.y[44],Eri.y[47],Eri.y[55],Eri.y[95],Eri.y[118]])]
        #参旗　しんき# 
        J_F44 = [[Ori.x[8],Ori.x[12]],[Ori.y[8],Ori.y[12]],[Ori.x[8],Ori.x[21]],[Ori.y[8],Ori.y[21]],\
                 [Ori.x[12],Ori.x[13]],[Ori.y[12],Ori.y[13]],[Ori.x[13],Ori.x[26]],[Ori.y[13],Ori.y[26]],\
                 [Ori.x[15],Ori.x[35]],[Ori.y[15],Ori.y[35]],[Ori.x[15],Ori.x[55]],[Ori.y[15],Ori.y[55]],\
                 [Ori.x[21],Ori.x[34]],[Ori.y[21],Ori.y[34]],[Ori.x[34],Ori.x[55]],[Ori.y[34],Ori.y[55]],\
                 [Ori.x[35],Ori.x[42]],[Ori.y[35],Ori.y[42]]]
        JF44n = [numpy.mean([Ori.x[8],Ori.x[12],Ori.x[13],Ori.x[15],Ori.x[21],Ori.x[26],Ori.x[34],Ori.x[35],\
                             Ori.x[42],Ori.x[55]]),\
                 numpy.mean([Ori.y[8],Ori.y[12],Ori.y[13],Ori.y[15],Ori.y[21],Ori.y[26],Ori.y[34],Ori.y[35],\
                             Ori.y[42],Ori.y[55]])]
        #九斿　きゅうりゅう# 
        J_F45 = [[Eri.x[13],Eri.x[15]],[Eri.y[13],Eri.y[15]],[Eri.x[15],Eri.x[27]],[Eri.y[15],Eri.y[27]],\
                 [Eri.x[25],Eri.x[75]],[Eri.y[25],Eri.y[75]],[Eri.x[27],Eri.x[69]],[Eri.y[27],Eri.y[69]],\
                 [Eri.x[41],Eri.x[48]],[Eri.y[41],Eri.y[48]],[Eri.x[41],Eri.x[69]],[Eri.y[41],Eri.y[69]],\
                 [Eri.x[48],Eri.x[75]],[Eri.y[48],Eri.y[75]]]
        JF45n = [numpy.mean([Eri.x[13],Eri.x[15],Eri.x[25],Eri.x[27],Eri.x[41],Eri.x[48],Eri.x[69],Eri.x[75]]),\
                 numpy.mean([Eri.y[13],Eri.y[15],Eri.y[25],Eri.y[27],Eri.y[41],Eri.y[48],Eri.y[69],Eri.y[75]])]
        #天園　てんえん# 
        J_F46 = [[Eri.x[3],Eri.x[18]],[Eri.y[3],Eri.y[18]],[Eri.x[3],Eri.x[22]],[Eri.y[3],Eri.y[22]],\
                 [Eri.x[6],Eri.x[14]],[Eri.y[6],Eri.y[14]],[Eri.x[6],Eri.x[50]],[Eri.y[6],Eri.y[50]],\
                 [Eri.x[10],Eri.x[14]],[Eri.y[10],Eri.y[14]],[Eri.x[10],Eri.x[31]],[Eri.y[10],Eri.y[31]],\
                 [Eri.x[18],Eri.x[38]],[Eri.y[18],Eri.y[38]],[Eri.x[19],Eri.x[37]],[Eri.y[19],Eri.y[37]],\
                 [Eri.x[19],Eri.x[50]],[Eri.y[19],Eri.y[50]],[Eri.x[22],Eri.x[32]],[Eri.y[22],Eri.y[32]],\
                 [Eri.x[32],Eri.x[33]],[Eri.y[32],Eri.y[33]],[Eri.x[33],Eri.x[37]],[Eri.y[33],Eri.y[37]]]
        JF46n = [numpy.mean([Eri.x[3],Eri.x[6],Eri.x[10],Eri.x[14],Eri.x[18],Eri.x[19],Eri.x[22],Eri.x[31],\
                             Eri.x[32],Eri.x[33],Eri.x[37],Eri.x[38],Eri.x[50]]),\
                 numpy.mean([Eri.y[3],Eri.y[6],Eri.y[10],Eri.y[14],Eri.y[18],Eri.y[19],Eri.y[22],Eri.y[31],\
                             Eri.y[32],Eri.y[33],Eri.y[37],Eri.y[38],Eri.y[50]])]
        #觜宿　し# 
        J_F47 = [[Ori.x[10],Ori.x[22]],[Ori.y[10],Ori.y[22]],[Ori.x[16],Ori.x[22]],[Ori.y[16],Ori.y[22]]]
        JF47n = [numpy.mean([Ori.x[10],Ori.x[16],Ori.x[22]]),\
                 numpy.mean([Ori.y[10],Ori.y[16],Ori.y[22]])]
        #司怪　しかい
        J_F48 = [[Tau.x[42],Tau.x[91]],[Tau.y[42],Tau.y[91]],[Tau.x[87],Tau.x[141]],[Tau.y[87],Tau.y[141]],\
                 [Tau.x[91],Tau.x[141]],[Tau.y[91],Tau.y[141]]]
        JF48n = [numpy.mean([Tau.x[42],Tau.x[87],Tau.x[91],Tau.x[141]]),\
                 numpy.mean([Tau.y[42],Tau.y[87],Tau.y[91],Tau.y[141]])]
        #座旗　ざき# 
        J_F49 = [[Aur.x[10],Aur.x[63]],[Aur.y[10],Aur.y[63]],[Aur.x[27],Aur.x[28]],[Aur.y[27],Aur.y[28]],\
                 [Aur.x[27],Aur.x[34]],[Aur.y[27],Aur.y[34]],[Aur.x[28],Aur.x[51]],[Aur.y[28],Aur.y[51]],\
                 [Aur.x[51],Aur.x[63]],[Aur.y[51],Aur.y[63]]]
        JF49n = [numpy.mean([Aur.x[10],Aur.x[27],Aur.x[28],Aur.x[34],Aur.x[51],Aur.x[63]]),\
                 numpy.mean([Aur.y[10],Aur.y[27],Aur.y[28],Aur.y[34],Aur.y[51],Aur.y[63]])]
        #参宿　しん# 
        J_F50 = [[Ori.x[0],Ori.x[5]],[Ori.y[0],Ori.y[5]],[Ori.x[0],Ori.x[6]],[Ori.y[0],Ori.y[6]],\
                 [Ori.x[1],Ori.x[2]],[Ori.y[1],Ori.y[2]],[Ori.x[1],Ori.x[4]],[Ori.y[1],Ori.y[4]],\
                 [Ori.x[2],Ori.x[6]],[Ori.y[2],Ori.y[6]],[Ori.x[3],Ori.x[4]],[Ori.y[3],Ori.y[4]],\
                 [Ori.x[3],Ori.x[6]],[Ori.y[3],Ori.y[6]],[Ori.x[4],Ori.x[5]],[Ori.y[4],Ori.y[5]]]
        JF50n = [numpy.mean([Ori.x[0],Ori.x[1],Ori.x[2],Ori.x[3],Ori.x[4],Ori.x[5],Ori.x[6]]),\
                 numpy.mean([Ori.y[0],Ori.y[1],Ori.y[2],Ori.y[3],Ori.y[4],Ori.y[5],Ori.y[6]])]
        #伐　ばつ# 
        J_F51 = [[Ori.x[7],Ori.x[51]],[Ori.y[7],Ori.y[51]],[Ori.x[31],Ori.x[51]],[Ori.y[31],Ori.y[51]]]
        JF51n = [numpy.mean([Ori.x[7],Ori.x[31],Ori.x[51]]),\
                 numpy.mean([Ori.y[7],Ori.y[31],Ori.y[51]])]
        #玉井　ぎょくせい# 
        J_F52 = [[Eri.x[1],Eri.x[43]],[Eri.y[1],Eri.y[43]],[Eri.x[1],Ori.x[11]],[Eri.y[1],Ori.y[11]],\
                 [Eri.x[24],Eri.x[43]],[Eri.y[24],Eri.y[43]]]
        JF52n = [numpy.mean([Eri.x[1],Eri.x[24],Eri.x[43],Ori.x[11]]),\
                 numpy.mean([Eri.y[1],Eri.y[24],Eri.y[43],Ori.y[11]])]
        #軍井　ぐんせい# 
        J_F53 = [[Lep.x[8],Lep.x[9]],[Lep.y[8],Lep.y[9]],[Lep.x[8],Lep.x[20]],[Lep.y[8],Lep.y[20]],\
                 [Lep.x[9],Lep.x[10]],[Lep.y[9],Lep.y[10]],[Lep.x[10],Lep.x[20]],[Lep.y[10],Lep.y[20]]]
        JF53n = [numpy.mean([Lep.x[8],Lep.x[9],Lep.x[10],Lep.x[20]]),\
                 numpy.mean([Lep.y[8],Lep.y[9],Lep.y[10],Lep.y[20]])]
        #屏　へい# 
        J_F54 = [[Lep.x[2],Lep.x[3]],[Lep.y[2],Lep.y[3]]]
        JF54n = [numpy.mean([Lep.x[2],Lep.x[3]]),\
                 numpy.mean([Lep.y[2],Lep.y[3]])]
        #厠　し# 
        J_F55 = [[Lep.x[0],Lep.x[1]],[Lep.y[0],Lep.y[1]],[Lep.x[0],Lep.x[7]],[Lep.y[0],Lep.y[7]],\
                 [Lep.x[1],Lep.x[5]],[Lep.y[1],Lep.y[5]],[Lep.x[5],Lep.x[7]],[Lep.y[5],Lep.y[7]]]
        JF55n = [numpy.mean([Lep.x[0],Lep.x[1],Lep.x[5],Lep.x[7]]),\
                 numpy.mean([Lep.y[0],Lep.y[1],Lep.y[5],Lep.y[7]])]
        #屎　し# 
        J_F56 = []
        JF56n = [Col.x[14],Col.y[14]-labelxy]
        #主計　かずえ# 
        J_F57 = [[Phe.x[1],Phe.x[2]],[Phe.y[1],Phe.y[2]]]
        JF57n = [numpy.mean([Phe.x[1],Phe.x[2]]),\
                 numpy.mean([Phe.y[1],Phe.y[2]])]
        #天俵　てんひょう# 
        J_F58 = [[Cet.x[17],Cet.x[49]],[Cet.y[17],Cet.y[49]],[Cet.x[20],Cet.x[37]],[Cet.y[20],Cet.y[37]],\
                 [Cet.x[24],Cet.x[49]],[Cet.y[24],Cet.y[49]],[Cet.x[24],Scl.x[9]],[Cet.y[24],Scl.y[9]],\
                 [Cet.x[28],Cet.x[43]],[Cet.y[28],Cet.y[43]],[Cet.x[28],Cet.x[49]],[Cet.y[28],Cet.y[49]],\
                 [Cet.x[28],Cet.x[73]],[Cet.y[28],Cet.y[73]],[Cet.x[37],Cet.x[43]],[Cet.y[37],Cet.y[43]],\
                 [Cet.x[37],Cet.x[130]],[Cet.y[37],Cet.y[130]],[Cet.x[43],Cet.x[63]],[Cet.y[43],Cet.y[63]]]
        JF58n = [numpy.mean([Cet.x[17],Cet.x[20],Cet.x[24],Cet.x[28],Cet.x[37],Cet.x[43],Cet.x[49],Cet.x[63],\
                             Cet.x[73],Cet.x[130],Scl.x[9]]),\
                 numpy.mean([Cet.y[17],Cet.y[20],Cet.y[24],Cet.y[28],Cet.y[37],Cet.y[43],Cet.y[49],Cet.y[63],\
                             Cet.y[73],Cet.y[130],Scl.y[9]])]
        #兵庫　ひょうご# 
        J_F59 = []
        JF59n = [And.x[11],And.y[11]-labelxy]
        #主税# 
        J_F60 = [[For.x[3],For.x[6]],[For.y[3],For.y[6]],[For.x[3],For.x[9]],[For.y[3],For.y[9]],\
                 [For.x[9],For.x[13]],[For.y[9],For.y[13]]]
        JF60n = [numpy.mean([For.x[3],For.x[6],For.x[9],For.x[13]]),\
                 numpy.mean([For.y[3],For.y[6],For.y[9],For.y[13]])]
        #大蔵# 
        J_F61 = [[Ari.x[7],Ari.x[32]],[Ari.y[7],Ari.y[32]],[Ari.x[17],Ari.x[24]],[Ari.y[17],Ari.y[24]],\
                 [Ari.x[17],Ari.x[39]],[Ari.y[17],Ari.y[39]],[Ari.x[18],Ari.x[24]],[Ari.y[18],Ari.y[24]],\
                 [Ari.x[18],Ari.x[32]],[Ari.y[18],Ari.y[32]],[Ari.x[18],Ari.x[34]],[Ari.y[18],Ari.y[34]],\
                 [Ari.x[18],Ari.x[39]],[Ari.y[18],Ari.y[39]]]
        JF61n = [numpy.mean([Ari.x[7],Ari.x[17],Ari.x[18],Ari.x[24],Ari.x[32],Ari.x[34],Ari.x[39]]),\
                 numpy.mean([Ari.y[7],Ari.y[17],Ari.y[18],Ari.y[24],Ari.y[32],Ari.y[34],Ari.y[39]])]
        #大炊# 
        J_F62 = [[Cet.x[31],Eri.x[36]],[Cet.y[31],Eri.y[36]],[Eri.x[36],Eri.x[79]],[Eri.y[36],Eri.y[79]],\
                 [Eri.x[40],Eri.x[60]],[Eri.y[40],Eri.y[60]],[Eri.x[40],Eri.x[74]],[Eri.y[40],Eri.y[74]],\
                 [Eri.x[60],Tau.x[21]],[Eri.y[60],Tau.y[21]],[Eri.x[74],Eri.x[79]],[Eri.y[74],Eri.y[79]],\
                 [Tau.x[15],Tau.x[21]],[Tau.y[15],Tau.y[21]],[Tau.x[15],Tau.x[50]],[Tau.y[15],Tau.y[50]]]
        JF62n = [numpy.mean([Cet.x[31],Eri.x[36],Eri.x[40],Eri.x[60],Eri.x[74],Eri.x[79],Tau.x[15],Tau.x[21],\
                             Tau.x[50]]),\
                 numpy.mean([Cet.y[31],Eri.y[36],Eri.y[40],Eri.y[60],Eri.y[74],Eri.y[79],Tau.y[15],Tau.y[21],\
                             Tau.y[50]])]
        #松竹# 
        J_F63 = [[For.x[0],For.x[4]],[For.y[0],For.y[4]],[For.x[0],For.x[15]],[For.y[0],For.y[15]],\
                 [For.x[1],For.x[15]],[For.y[1],For.y[15]],[For.x[5],For.x[15]],[For.y[5],For.y[15]]]
        JF63n = [numpy.mean([For.x[0],For.x[1],For.x[4],For.x[5],For.x[15]]),\
                 numpy.mean([For.y[0],For.y[1],For.y[4],For.y[5],For.y[15]])]
        #鴻雁# 
        J_F64 = []
        JF64n = [Eri.x[57],Eri.y[57]-labelxy]
        #萩薄# 
        J_F65 = [[Cae.x[0],Cae.x[2]],[Cae.y[0],Cae.y[2]],[Cae.x[0],Hor.x[0]],[Cae.y[0],Hor.y[0]],\
                 [Cae.x[1],Cae.x[2]],[Cae.y[1],Cae.y[2]],[Cae.x[1],Col.x[7]],[Cae.y[1],Col.y[7]]]
        JF65n = [numpy.mean([Cae.x[0],Cae.x[1],Cae.x[2],Col.x[7],Hor.x[0]]),\
                 numpy.mean([Cae.y[0],Cae.y[1],Cae.y[2],Col.y[7],Hor.y[0]])]
        #天轅# 
        J_F66 = [[Aur.x[16],Aur.x[19]],[Aur.y[16],Aur.y[19]],[Aur.x[16],Aur.x[22]],[Aur.y[16],Aur.y[22]],\
                 [Aur.x[19],Per.x[20]],[Aur.y[19],Per.y[20]],[Per.x[20],Per.x[28]],[Per.y[20],Per.y[28]],\
                 [Per.x[28],Per.x[34]],[Per.y[28],Per.y[34]],[Per.x[34],Per.x[73]],[Per.y[34],Per.y[73]],\
                 [Per.x[73],Tau.x[45]],[Per.y[73],Tau.y[45]]]
        JF66n = [numpy.mean([Aur.x[16],Aur.x[19],Aur.x[22],Per.x[20],Per.x[28],Per.x[34],Per.x[73],Tau.x[45]]),\
                 numpy.mean([Aur.y[16],Aur.y[19],Aur.y[22],Per.y[20],Per.y[28],Per.y[34],Per.y[73],Tau.y[45]])]
        #太宰府# 
        J_F67 = [[Ori.x[9],Ori.x[18]],[Ori.y[9],Ori.y[18]],[Ori.x[14],Ori.x[41]],[Ori.y[14],Ori.y[41]],\
                 [Ori.x[18],Ori.x[32]],[Ori.y[18],Ori.y[32]],[Ori.x[32],Ori.x[41]],[Ori.y[32],Ori.y[41]]]
        JF67n = [numpy.mean([Ori.x[9],Ori.x[14],Ori.x[18],Ori.x[32],Ori.x[41]]),\
                 numpy.mean([Ori.y[9],Ori.y[14],Ori.y[18],Ori.y[32],Ori.y[41]])]
        #大弐　だいに# 
        J_F68 = [[Mon.x[7],Mon.x[17]],[Mon.y[7],Mon.y[17]]]
        JF68n = [numpy.mean([Mon.x[7],Mon.x[17]]),\
                 numpy.mean([Mon.y[7],Mon.y[17]])]
        #小弐　しょうに# 
        J_F69 = [[Lep.x[4],Lep.x[6]],[Lep.y[4],Lep.y[6]]]
        JF69n = [numpy.mean([Lep.x[4],Lep.x[6]]),\
                 numpy.mean([Lep.y[4],Lep.y[6]])]
        #玄蕃　げんば# 
        J_F70 = [[Gem.x[16],Ori.x[33]],[Gem.y[16],Ori.y[33]],[Gem.x[16],Tau.x[37]],[Gem.y[16],Tau.y[37]],\
                 [Ori.x[23],Ori.x[33]],[Ori.y[23],Ori.y[33]],[Tau.x[30],Tau.x[37]],[Tau.y[30],Tau.y[37]]]
        JF70n = [numpy.mean([Gem.x[16],Ori.x[23],Ori.x[33],Tau.x[30],Tau.x[37]]),\
                 numpy.mean([Gem.y[16],Ori.y[23],Ori.y[33],Tau.y[30],Tau.y[37]])]

        J_F_list = [J_F01,J_F02,J_F03,J_F04,J_F05,J_F06,J_F07,J_F08,J_F09,J_F10,\
                    J_F11,J_F12,J_F13,J_F14,J_F15,J_F16,J_F17,J_F18,J_F19,J_F20,\
                    J_F21,J_F22,J_F23,J_F24,J_F25,J_F26,J_F27,J_F28,J_F29,J_F30,\
                    J_F31,J_F32,J_F33,J_F34,J_F35,J_F36,J_F37,J_F38,J_F39,J_F40,\
                    J_F41,J_F42,J_F43,J_F44,J_F45,J_F46,J_F47,J_F48,J_F49,J_F50,\
                    J_F51,J_F52,J_F53,J_F54,J_F55,J_F56,J_F57,J_F58,J_F59,J_F60,\
                    J_F61,J_F62,J_F63,J_F64,J_F65,J_F66,J_F67,J_F68,J_F69,J_F70]

        # 西宮白虎 linecollection
        J_F_line_z_xy1 = []
        J_F_line_z_xy2 = [] 
        J_F_line_xy1 = []
        J_F_line_xy2 = []        
        for i in range(len(J_F_list)):
            for j in range(len(J_F_list[i]))[0::2]:
                if math.hypot(J_F_list[i][j][0]-J_F_list[i][j][1],J_F_list[i][j+1][0]-J_F_list[i][j+1][1]) < hori_border:
                    if i in set([0,9,15,22,31,46,49]):
                        J_F_line_z_xy1.append((J_F_list[i][j][0],J_F_list[i][j+1][0]))
                        J_F_line_z_xy2.append((J_F_list[i][j][1],J_F_list[i][j+1][1]))
                    else:
                        J_F_line_xy1.append((J_F_list[i][j][0],J_F_list[i][j+1][0]))
                        J_F_line_xy2.append((J_F_list[i][j][1],J_F_list[i][j+1][1]))

        J_F_line_z_list = []
        for i in range(len(J_F_line_z_xy1)):            
            J_F_line_z_list.append([J_F_line_z_xy1[i],J_F_line_z_xy2[i]])
        
        J_F_line_list = []
        for i in range(len(J_F_line_xy1)):            
            J_F_line_list.append([J_F_line_xy1[i],J_F_line_xy2[i]])
        
        lc_J_F_z = mc.LineCollection(J_F_line_z_list, colors='yellow', zorder=2+2.5)
        lc_J_F = mc.LineCollection(J_F_line_list, colors='white', zorder=2+2.5)
        lc_J_F_z.set_alpha(plot_alpha)
        lc_J_F.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_F_z)
        ax0.add_collection(lc_J_F)

        JFn_list = [[JF01n,'奎宿'],[JF02n,'王良'],[JF03n,'策'],[JF04n,'附路'],[JF05n,'軍南門'],\
                    [JF06n,'閣道'],[JF07n,'外屏'],[JF08n,'天溷'],[JF09n,'土司空'],[JF10n,'婁宿'],\
                    [JF11n,'天大将軍'],[JF12n,'右更'],[JF13n,'左更'],[JF14n,'天倉'],[JF15n,'天庾'],\
                    [JF16n,'胃宿'],[JF17n,'大陵'],[JF18n,'積尸'],[JF19n,'天船'],[JF20n,'積水'],\
                    [JF21n,'天廩'],[JF22n,'天囷'],[JF23n,'昴宿'],[JF24n,'天阿'],[JF25n,'月'],\
                    [JF26n,'卷舌'],[JF27n,'天讒'],[JF28n,'蠣石'],[JF29n,'天陰'],[JF30n,'芻藁'],\
                    [JF31n,'天苑'],[JF32n,'畢宿'],[JF33n,'附耳'],[JF34n,'天街'],[JF35n,'天高'],\
                    [JF36n,'諸王'],[JF37n,'五車'],[JF38an,'柱'],[JF38bn,'柱'],[JF38cn,'柱'],\
                    [JF39n,'咸池'],[JF40n,'天潢'],[JF41n,'天関'],[JF42n,'天節'],[JF43n,'九州珠口'],\
                    [JF44n,'参旗'],[JF45n,'九斿'],[JF46n,'天園'],[JF47n,'觜宿'],[JF48n,'司怪'],\
                    [JF49n,'座旗'],[JF50n,'参宿'],[JF51n,'伐'],[JF52n,'玉井'],[JF53n,'軍井'],\
                    [JF54n,'屏'],[JF55n,'厠'],[JF56n,'屎'],[JF57n,'主計'],[JF58n,'天俵'],\
                    [JF59n,'兵庫'],[JF60n,'主税'],[JF61n,'大蔵'],[JF62n,'大炊'],[JF63n,'松竹'],\
                    [JF64n,'鴻雁'],[JF65n,'萩薄'],[JF66n,'天轅'],[JF67n,'太宰府'],[JF68n,'大弐'],\
                    [JF69n,'小弐'],[JF70n,'玄蕃']]

        for i in range(len(JFn_list)):
            if len(JFn_list[i][0]) != 0:
                if (JFn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JFn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JFn_list[i][0])-min(JFn_list[i][0]) < hori_border:
                    if i in set([0,9,15,22,31,48,51]):
                        ax_label.annotate(str(JFn_list[i][1]),(JFn_list[i][0][0],JFn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(JFn_list[i][1]),(JFn_list[i][0][0],JFn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #南宮朱雀#
        ##########
                        
        #井宿　せい# 
        J_G01 = [[Gem.x[1],Gem.x[7]],[Gem.y[1],Gem.y[7]],[Gem.x[1],Gem.x[12]],[Gem.y[1],Gem.y[12]],\
                 [Gem.x[1],Gem.x[15]],[Gem.y[1],Gem.y[15]],[Gem.x[3],Gem.x[15]],[Gem.y[3],Gem.y[15]],\
                 [Gem.x[5],Gem.x[38]],[Gem.y[5],Gem.y[38]],[Gem.x[10],Gem.x[12]],[Gem.y[10],Gem.y[12]],\
                 [Gem.x[12],Gem.x[38]],[Gem.y[12],Gem.y[38]],[Gem.x[15],Gem.x[38]],[Gem.y[15],Gem.y[38]]]
        JG01n = [numpy.mean([Gem.x[1],Gem.x[3],Gem.x[5],Gem.x[7],Gem.x[10],Gem.x[12],Gem.x[15],Gem.x[38]]),\
                 numpy.mean([Gem.y[1],Gem.y[3],Gem.y[5],Gem.y[7],Gem.y[10],Gem.y[12],Gem.y[15],Gem.y[38]])]
        #鉞　えつ# 
        J_G02 = []
        JG02n = [Gem.x[6],Gem.y[6]-labelxy]
        #水府　すいふ# 
        J_G03 = [[Ori.x[24],Ori.x[27]],[Ori.y[24],Ori.y[27]],[Ori.x[24],Ori.x[47]],[Ori.y[24],Ori.y[47]],\
                 [Ori.x[27],Ori.x[60]],[Ori.y[27],Ori.y[60]],[Ori.x[47],Ori.x[60]],[Ori.y[47],Ori.y[60]]]
        JG03n = [numpy.mean([Ori.x[24],Ori.x[27],Ori.x[47],Ori.x[60]]),\
                 numpy.mean([Ori.y[24],Ori.y[27],Ori.y[47],Ori.y[60]])]
        #天樽　てんそん# 
        J_G04 = [[Gem.x[8],Gem.x[31]],[Gem.y[8],Gem.y[31]],[Gem.x[8],Gem.x[36]],[Gem.y[8],Gem.y[36]]]
        JG04n = [numpy.mean([Gem.x[8],Gem.x[31],Gem.x[36]]),\
                 numpy.mean([Gem.y[8],Gem.y[31],Gem.y[36]])]
        #五諸候　ごしょこう# 
        J_G05 = [[Gem.x[9],Gem.x[14]],[Gem.y[9],Gem.y[14]],[Gem.x[11],Gem.x[19]],[Gem.y[11],Gem.y[19]],\
                 [Gem.x[13],Gem.x[14]],[Gem.y[13],Gem.y[14]],[Gem.x[13],Gem.x[19]],[Gem.y[13],Gem.y[19]]]
        JG05n = [numpy.mean([Gem.x[9],Gem.x[11],Gem.x[13],Gem.x[14],Gem.x[19]]),\
                 numpy.mean([Gem.y[9],Gem.y[11],Gem.y[13],Gem.y[14],Gem.y[19]])]
        #北河　ほくか# 
        J_G06 = [[Gem.x[0],Gem.x[4]],[Gem.y[0],Gem.y[4]],[Gem.x[4],Gem.x[17]],[Gem.y[4],Gem.y[17]]]
        JG06n = [numpy.mean([Gem.x[0],Gem.x[4],Gem.x[17]]),\
                 numpy.mean([Gem.y[0],Gem.y[4],Gem.y[17]])]
        #積水　せきすい# 
        J_G07 = []
        JG07n = [Gem.x[23],Gem.y[23]-labelxy]
        #積薪　せきしん# 
        J_G08 = []
        JG08n = [Cnc.x[13],Cnc.y[13]-labelxy]
        #水位　すいい# 
        J_G09 = [[Gem.x[22],Gem.x[30]],[Gem.y[22],Gem.y[30]],[Gem.x[22],Gem.x[74]],[Gem.y[22],Gem.y[74]],\
                 [Gem.x[30],Gem.x[37]],[Gem.y[30],Gem.y[37]],[Gem.x[41],Gem.x[74]],[Gem.y[41],Gem.y[74]]]
        JG09n = [numpy.mean([Gem.x[22],Gem.x[30],Gem.x[37],Gem.x[41],Gem.x[74]]),\
                 numpy.mean([Gem.y[22],Gem.y[30],Gem.y[37],Gem.y[41],Gem.y[74]])]
        #南河　なんか# 
        J_G10 = [[CMi.x[0],CMi.x[1]],[CMi.y[0],CMi.y[1]],[CMi.x[1],CMi.x[2]],[CMi.y[1],CMi.y[2]],\
                 [CMi.x[2],CMi.x[4]],[CMi.y[2],CMi.y[4]]]
        JG10n = [numpy.mean([CMi.x[0],CMi.x[1],CMi.x[2],CMi.x[4]]),\
                 numpy.mean([CMi.y[0],CMi.y[1],CMi.y[2],CMi.y[4]])]
        #四涜　いっかくじゅう# 
        J_G11 = [[Gem.x[21],Mon.x[8]],[Gem.y[21],Mon.y[8]],[Mon.x[4],Mon.x[6]],[Mon.y[4],Mon.y[6]],\
                 [Mon.x[6],Mon.x[8]],[Mon.y[6],Mon.y[8]]]
        JG11n = [numpy.mean([Gem.x[21],Mon.x[4],Mon.x[6],Mon.x[8]]),\
                 numpy.mean([Gem.y[21],Mon.y[4],Mon.y[6],Mon.y[8]])]
        #闕丘　けっきゅう# 
        J_G12 = [[Mon.x[2],Mon.x[5]],[Mon.y[2],Mon.y[5]]]
        JG12n = [numpy.mean([Mon.x[2],Mon.x[5]]),\
                 numpy.mean([Mon.y[2],Mon.y[5]])]
        #軍市　ぐんし# 
        J_G13 = [[CMa.x[10],CMa.x[17]],[CMa.y[10],CMa.y[17]],[CMa.x[10],CMa.x[19]],[CMa.y[10],CMa.y[19]],\
                 [CMa.x[14],CMa.x[19]],[CMa.y[14],CMa.y[19]],[CMa.x[14],Lep.x[33]],[CMa.y[14],Lep.y[33]],\
                 [Lep.x[11],Lep.x[14]],[Lep.y[11],Lep.y[14]],[Lep.x[14],Lep.x[21]],[Lep.y[14],Lep.y[21]],\
                 [Lep.x[21],Lep.x[33]],[Lep.y[21],Lep.y[33]]]
        JG13n = [numpy.mean([CMa.x[10],CMa.x[14],CMa.x[17],CMa.x[19],Lep.x[11],Lep.x[14],Lep.x[21],Lep.x[33]]),\
                 numpy.mean([CMa.y[10],CMa.y[14],CMa.y[17],CMa.y[19],Lep.y[11],Lep.y[14],Lep.y[21],Lep.y[33]])]
        #野鶏　やけい# 
        J_G14 = []
        JG14n = [CMa.x[3],CMa.y[3]-labelxy]
        #天狼　てんろう# 
        J_G15 = []
        JG15n = [CMa.x[0],CMa.y[0]-labelxy]
        #丈人　じょうじん# 
        J_G16 = [[Col.x[0],Col.x[3]],[Col.y[0],Col.y[3]]]
        JG16n = [numpy.mean([Col.x[0],Col.x[3]]),\
                 numpy.mean([Col.y[0],Col.y[3]])]
        #子　し# 
        J_G17 = [[Col.x[1],Col.x[5]],[Col.y[1],Col.y[5]]]
        JG17n = [numpy.mean([Col.x[1],Col.x[5]]),\
                 numpy.mean([Col.y[1],Col.y[5]])]
        #孫　そん# 
        J_G18 = [[Col.x[2],Col.x[6]],[Col.y[2],Col.y[6]]]
        JG18n = [numpy.mean([Col.x[2],Col.x[6]]),\
                 numpy.mean([Col.y[2],Col.y[6]])]
        #老人　ろうじん# 
        J_G19 = []
        JG19n = [Car.x[0],Car.y[0]-labelxy]
        #弧矢　こし# 
        J_G20 = [[CMa.x[1],CMa.x[7]],[CMa.y[1],CMa.y[7]],[CMa.x[1],CMa.x[11]],[CMa.y[1],CMa.y[11]],\
                 [CMa.x[2],CMa.x[4]],[CMa.y[2],CMa.y[4]],[CMa.x[2],CMa.x[6]],[CMa.y[2],CMa.y[6]],\
                 [CMa.x[2],CMa.x[7]],[CMa.y[2],CMa.y[7]],[CMa.x[2],CMa.x[16]],[CMa.y[2],CMa.y[16]],\
                 [CMa.x[16],Pup.x[11]],[CMa.y[16],Pup.y[11]],[Pup.x[2],Pup.x[11]],[Pup.y[2],Pup.y[11]]]
        JG20n = [numpy.mean([CMa.x[1],CMa.x[2],CMa.x[4],CMa.x[6],CMa.x[7],CMa.x[11],CMa.x[16],Pup.x[2],\
                             Pup.x[11]]),\
                 numpy.mean([CMa.y[1],CMa.y[2],CMa.y[4],CMa.y[6],CMa.y[7],CMa.y[11],CMa.y[16],Pup.y[2],\
                             Pup.y[11]])]
        #鬼宿　き# 
        J_G21 = [[Cnc.x[1],Cnc.x[4]],[Cnc.y[1],Cnc.y[4]],[Cnc.x[1],Cnc.x[16]],[Cnc.y[1],Cnc.y[16]],\
                 [Cnc.x[4],Cnc.x[14]],[Cnc.y[4],Cnc.y[14]],[Cnc.x[14],Cnc.x[16]],[Cnc.y[14],Cnc.y[16]]]
        JG21n = [numpy.mean([Cnc.x[1],Cnc.x[4],Cnc.x[14],Cnc.x[16]]),\
                 numpy.mean([Cnc.y[1],Cnc.y[4],Cnc.y[14],Cnc.y[16]])]
        #積尸気　せきしき# 
        J_G22 = []
        JG22n = [Cnc.x[78],Cnc.y[78]-labelxy]
        #爟　かん# 
        J_G23 = [[Cnc.x[7],Cnc.x[24]],[Cnc.y[7],Cnc.y[24]],[Cnc.x[7],Cnc.x[77]],[Cnc.y[7],Cnc.y[77]]]
        JG23n = [numpy.mean([Cnc.x[7],Cnc.x[24],Cnc.x[77]]),\
                 numpy.mean([Cnc.y[7],Cnc.y[24],Cnc.y[77]])]
        #外厨　がいちゅう# 
        J_G24 = [[Hya.x[10],Hya.x[69]],[Hya.y[10],Hya.y[69]]]
        JG24n = [numpy.mean([Hya.x[10],Hya.x[69]]),\
                 numpy.mean([Hya.y[10],Hya.y[69]])]
        #天記　てんき# 
        J_G25 = []
        JG25n = [Hya.x[16],Hya.y[16]-labelxy]
        #天狗　てんこう# 
        J_G26 = [[Mon.x[0],Pup.x[85]],[Mon.y[0],Pup.y[85]],[Mon.x[40],Pup.x[85]],[Mon.y[40],Pup.y[85]],\
                 [Pup.x[52],Pup.x[64]],[Pup.y[52],Pup.y[64]],[Pup.x[64],Pup.x[85]],[Pup.y[64],Pup.y[85]]]
        JG26n = [numpy.mean([Mon.x[0],Mon.x[40],Pup.x[52],Pup.x[64],Pup.x[85]]),\
                 numpy.mean([Mon.y[0],Mon.y[40],Pup.y[52],Pup.y[64],Pup.y[85]])]
        #天社　てんしゃ# 
        J_G27 = [[Pup.x[0],Pup.x[8]],[Pup.y[0],Pup.y[8]],[Pup.x[0],Pup.x[18]],[Pup.y[0],Pup.y[18]],\
                 [Pup.x[0],Pup.x[20]],[Pup.y[0],Pup.y[20]],[Pup.x[18],Pyx.x[0]],[Pup.y[18],Pyx.y[0]],\
                 [Pup.x[18],Pyx.x[1]],[Pup.y[18],Pyx.y[1]]]
        JG27n = [numpy.mean([Pup.x[0],Pup.x[8],Pup.x[18],Pup.x[20],Pyx.x[0],Pyx.x[1]]),\
                 numpy.mean([Pup.y[0],Pup.y[8],Pup.y[18],Pup.y[20],Pyx.y[0],Pyx.y[1]])]
        #柳宿　りゅう# 
        J_G28 = [[Hya.x[2],Hya.x[5]],[Hya.y[2],Hya.y[5]],[Hya.x[2],Hya.x[41]],[Hya.y[2],Hya.y[41]],\
                 [Hya.x[5],Hya.x[13]],[Hya.y[5],Hya.y[13]],[Hya.x[9],Hya.x[41]],[Hya.y[9],Hya.y[41]],\
                 [Hya.x[13],Hya.x[19]],[Hya.y[13],Hya.y[19]],[Hya.x[15],Hya.x[17]],[Hya.y[15],Hya.y[17]],\
                 [Hya.x[15],Hya.x[19]],[Hya.y[15],Hya.y[19]]]
        JG28n = [numpy.mean([Hya.x[2],Hya.x[5],Hya.x[9],Hya.x[13],Hya.x[15],Hya.x[17],Hya.x[19],Hya.x[41]]),\
                 numpy.mean([Hya.y[2],Hya.y[5],Hya.y[9],Hya.y[13],Hya.y[15],Hya.y[17],Hya.y[19],Hya.y[41]])]
        #酒旗　しゅき# 
        J_G29 = [[Leo.x[30],Leo.x[62]],[Leo.y[30],Leo.y[62]],[Leo.x[32],Leo.x[62]],[Leo.y[32],Leo.y[62]]]
        JG29n = [numpy.mean([Leo.x[30],Leo.x[32],Leo.x[62]]),\
                 numpy.mean([Leo.y[30],Leo.y[32],Leo.y[62]])]
        #星宿　せい# 
        J_G30 = [[Hya.x[0],Hya.x[30]],[Hya.y[0],Hya.y[30]],[Hya.x[0],Hya.x[61]],[Hya.y[0],Hya.y[61]],\
                 [Hya.x[11],Hya.x[20]],[Hya.y[11],Hya.y[20]],[Hya.x[20],Hya.x[21]],[Hya.y[20],Hya.y[21]],\
                 [Hya.x[21],Hya.x[61]],[Hya.y[21],Hya.y[61]],[Hya.x[29],Hya.x[30]],[Hya.y[29],Hya.y[30]]]
        JG30n = [numpy.mean([Hya.x[0],Hya.x[11],Hya.x[20],Hya.x[21],Hya.x[29],Hya.x[30],Hya.x[61]]),\
                 numpy.mean([Hya.y[0],Hya.y[11],Hya.y[20],Hya.y[21],Hya.y[29],Hya.y[30],Hya.y[61]])]
        #天相　てんしょう# 
        J_G31 = [[Sex.x[4],Sex.x[7]],[Sex.y[4],Sex.y[7]]]
        JG31n = [numpy.mean([Sex.x[4],Sex.x[7]]),\
                 numpy.mean([Sex.y[4],Sex.y[7]])]
        #軒轅　けんえん# 
        J_G32 = [[Leo.x[0],Leo.x[7]],[Leo.y[0],Leo.y[7]],[Leo.x[0],Leo.x[8]],[Leo.y[0],Leo.y[8]],\
                 [Leo.x[0],Leo.x[10]],[Leo.y[0],Leo.y[10]],[Leo.x[0],Leo.x[16]],[Leo.y[0],Leo.y[16]],\
                 [Leo.x[3],Leo.x[6]],[Leo.y[3],Leo.y[6]],[Leo.x[3],Leo.x[8]],[Leo.y[3],Leo.y[8]],\
                 [Leo.x[4],Leo.x[11]],[Leo.y[4],Leo.y[11]],[Leo.x[4],Leo.x[15]],[Leo.y[4],Leo.y[15]],\
                 [Leo.x[6],Leo.x[11]],[Leo.y[6],Leo.y[11]],[Leo.x[15],Leo.x[18]],[Leo.y[15],Leo.y[18]],\
                 [Leo.x[18],Leo.x[57]],[Leo.y[18],Leo.y[57]],[Leo.x[57],Lyn.x[0]],[Leo.y[57],Lyn.y[0]],\
                 [Lyn.x[0],Lyn.x[1]],[Lyn.y[0],Lyn.y[1]],[Lyn.x[1],Lyn.x[6]],[Lyn.y[1],Lyn.y[6]],\
                 [Lyn.x[2],Lyn.x[6]],[Lyn.y[2],Lyn.y[6]],[Lyn.x[2],Lyn.x[15]],[Lyn.y[2],Lyn.y[15]]]
        JG32n = [numpy.mean([Leo.x[0],Leo.x[3],Leo.x[4],Leo.x[6],Leo.x[7],Leo.x[8],Leo.x[10],Leo.x[11],\
                             Leo.x[15],Leo.x[16],Leo.x[18],Leo.x[57],Lyn.x[0],Lyn.x[1],Lyn.x[2],Lyn.x[6],\
                             Lyn.x[15]]),\
                 numpy.mean([Leo.y[0],Leo.y[3],Leo.y[4],Leo.y[6],Leo.y[7],Leo.y[8],Leo.y[10],Leo.y[11],\
                             Leo.y[15],Leo.y[16],Leo.y[18],Leo.y[57],Lyn.y[0],Lyn.y[1],Lyn.y[2],Lyn.y[6],\
                             Lyn.y[15]])]
        #內平　ないへい# 
        J_G33 = [[LMi.x[3],LMi.x[12]],[LMi.y[3],LMi.y[12]],[LMi.x[3],Lyn.x[19]],[LMi.y[3],Lyn.y[19]]]
        JG33n = [numpy.mean([LMi.x[3],LMi.x[12],Lyn.x[19]]),\
                 numpy.mean([LMi.y[3],LMi.y[12],Lyn.y[19]])]
        #天稷#　てんしょく# 
        J_G34 = [[Vel.x[2],Vel.x[7]],[Vel.y[2],Vel.y[7]],[Vel.x[2],Vel.x[20]],[Vel.y[2],Vel.y[20]],\
                 [Vel.x[7],Vel.x[33]],[Vel.y[7],Vel.y[33]],[Vel.x[14],Vel.x[20]],[Vel.y[14],Vel.y[20]],\
                 [Vel.x[20],Vel.x[33]],[Vel.y[20],Vel.y[33]]]
        JG34n = [numpy.mean([Vel.x[2],Vel.x[7],Vel.x[14],Vel.x[20],Vel.x[33]]),\
                 numpy.mean([Vel.y[2],Vel.y[7],Vel.y[14],Vel.y[20],Vel.y[33]])]
        #張宿　ちょう# 
        J_G35 = [[Hya.x[8],Hya.x[12]],[Hya.y[8],Hya.y[12]],[Hya.x[8],Hya.x[35]],[Hya.y[8],Hya.y[35]],\
                 [Hya.x[12],Hya.x[47]],[Hya.y[12],Hya.y[47]]]
        JG35n = [numpy.mean([Hya.x[8],Hya.x[12],Hya.x[35],Hya.x[47]]),\
                 numpy.mean([Hya.y[8],Hya.y[12],Hya.y[35],Hya.y[47]])]
        #天廟　てんびょう# 
        J_G36 = [[Ant.x[3],Ant.x[18]],[Ant.y[3],Ant.y[18]],[Ant.x[18],Pyx.x[4]],[Ant.y[18],Pyx.y[4]],\
                 [Pyx.x[4],Pyx.x[5]],[Pyx.y[4],Pyx.y[5]]]
        JG36n = [numpy.mean([Ant.x[3],Ant.x[18],Pyx.x[4],Pyx.x[5]]),\
                 numpy.mean([Ant.y[3],Ant.y[18],Pyx.y[4],Pyx.y[5]])]
        #翼宿　よく# 
        J_G37 = [[Crt.x[0],Crt.x[2]],[Crt.y[0],Crt.y[2]],[Crt.x[0],Crt.x[6]],[Crt.y[0],Crt.y[6]],\
                 [Crt.x[1],Crt.x[7]],[Crt.y[1],Crt.y[7]],[Crt.x[1],Hya.x[3]],[Crt.y[1],Hya.y[3]],\
                 [Crt.x[2],Crt.x[5]],[Crt.y[2],Crt.y[5]],[Crt.x[2],Crt.x[7]],[Crt.y[2],Crt.y[7]],\
                 [Crt.x[3],Crt.x[7]],[Crt.y[3],Crt.y[7]],[Crt.x[3],Hya.x[38]],[Crt.y[3],Hya.y[38]],\
                 [Crt.x[4],Crt.x[6]],[Crt.y[4],Crt.y[6]],[Crt.x[6],Sex.x[10]],[Crt.y[6],Sex.y[10]]]
        JG37n = [numpy.mean([Crt.x[0],Crt.x[1],Crt.x[2],Crt.x[3],Crt.x[4],Crt.x[5],Crt.x[6],Crt.x[7],\
                             Hya.x[3],Hya.x[38],Sex.x[10]]),\
                 numpy.mean([Crt.y[0],Crt.y[1],Crt.y[2],Crt.y[3],Crt.y[4],Crt.y[5],Crt.y[6],Crt.y[7],\
                             Hya.y[3],Hya.y[38],Sex.y[10]])]
        #東甌　とうおう# 
        J_G38 = [[Vel.x[12],Vel.x[28]],[Vel.y[12],Vel.y[28]]]
        JG38n = [numpy.mean([Vel.x[12],Vel.x[28]]),\
                 numpy.mean([Vel.y[12],Vel.y[28]])]
        #軫宿　しん# 
        J_G39 = [[Crv.x[0],Crv.x[2]],[Crv.y[0],Crv.y[2]],[Crv.x[0],Crv.x[3]],[Crv.y[0],Crv.y[3]],\
                 [Crv.x[1],Crv.x[2]],[Crv.y[1],Crv.y[2]],[Crv.x[1],Crv.x[3]],[Crv.y[1],Crv.y[3]]]
        JG39n = [numpy.mean([Crv.x[0],Crv.x[1],Crv.x[2],Crv.x[3]]),\
                 numpy.mean([Crv.y[0],Crv.y[1],Crv.y[2],Crv.y[3]])]
        #右轄　うかつ# 
        J_G40 = []
        JG40n = [Crv.x[4],Crv.y[4]-labelxy]
        #左轄　さかつ# 
        J_G41 = []
        JG41n = [Crv.x[5],Crv.y[5]-labelxy]
        #長沙　ちょうさ# 
        J_G42 = []
        JG42n = [Crv.x[7],Crv.y[7]-labelxy]
        #青邱　せいきゅう# 
        J_G43 = [[Hya.x[6],Hya.x[46]],[Hya.y[6],Hya.y[46]],[Hya.x[6],Hya.x[123]],[Hya.y[6],Hya.y[123]],\
                 [Hya.x[14],Hya.x[119]],[Hya.y[14],Hya.y[119]],[Hya.x[26],Hya.x[96]],[Hya.y[26],Hya.y[96]],\
                 [Hya.x[46],Hya.x[80]],[Hya.y[46],Hya.y[80]],[Hya.x[80],Hya.x[119]],[Hya.y[80],Hya.y[119]],\
                 [Hya.x[96],Hya.x[123]],[Hya.y[96],Hya.y[123]]]
        JG43n = [numpy.mean([Hya.x[6],Hya.x[14],Hya.x[26],Hya.x[46],Hya.x[80],Hya.x[96],Hya.x[119],Hya.x[123]]),\
                 numpy.mean([Hya.y[6],Hya.y[14],Hya.y[26],Hya.y[46],Hya.y[80],Hya.y[96],Hya.y[119],Hya.y[123]])]
        #軍門　ぐんもん# 
        J_G44 = [[Hya.x[14],Hya.x[26]],[Hya.y[14],Hya.y[26]]]
        JG44n = [numpy.mean([Hya.x[14],Hya.x[26]]),\
                 numpy.mean([Hya.y[14],Hya.y[26]])]
        #土司空　どしくう#
        J_G45 = []
        JG45n = [] # ?
        #器府　きふ# 
        J_G46 = [[Cen.x[8],Cen.x[19]],[Cen.y[8],Cen.y[19]]]
        JG46n = [numpy.mean([Cen.x[8],Cen.x[19]]),\
                 numpy.mean([Cen.y[8],Cen.y[19]])]
        #曾孫　そうそん# 
        J_G47 = [[CMa.x[5],CMa.x[18]],[CMa.y[5],CMa.y[18]]]
        JG47n = [numpy.mean([CMa.x[5],CMa.x[18]]),\
                 numpy.mean([CMa.y[5],CMa.y[18]])]
        #玄孫　げんそん# 
        J_G48 = [[Col.x[4],Pup.x[4]],[Col.y[4],Pup.y[4]]]
        JG48n = [numpy.mean([Col.x[4],Pup.x[4]]),\
                 numpy.mean([Col.y[4],Pup.y[4]])]
        #箙# 
        J_G49 = [[CMa.x[8],Pup.x[21]],[CMa.y[8],Pup.y[21]],[Pup.x[6],Pup.x[21]],[Pup.y[6],Pup.y[21]]]
        JG49n = [numpy.mean([CMa.x[8],Pup.x[6],Pup.x[21]]),\
                 numpy.mean([CMa.y[8],Pup.y[6],Pup.y[21]])]
        #胡籙　ころく# 
        J_G50 = [[Pup.x[1],Pup.x[5]],[Pup.y[1],Pup.y[5]]]
        JG50n = [numpy.mean([Pup.x[1],Pup.x[5]]),\
                 numpy.mean([Pup.y[1],Pup.y[5]])]
        #隼人# 
        J_G51 = [[CMa.x[12],CMa.x[13]],[CMa.y[12],CMa.y[13]],[CMa.x[13],CMa.x[15]],[CMa.y[13],CMa.y[15]],\
                 [CMa.x[15],CMa.x[22]],[CMa.y[15],CMa.y[22]]]
        JG51n = [numpy.mean([CMa.x[12],CMa.x[13],CMa.x[15],CMa.x[22]]),\
                 numpy.mean([CMa.y[12],CMa.y[13],CMa.y[15],CMa.y[22]])]
        #主水　もんど# 
        J_G52 = [[Cnc.x[0],Cnc.x[25]],[Cnc.y[0],Cnc.y[25]],[Cnc.x[0],Mon.x[3]],[Cnc.y[0],Mon.y[3]]]
        JG52n = [numpy.mean([Cnc.x[0],Cnc.x[25],Mon.x[3]]),\
                 numpy.mean([Cnc.y[0],Cnc.y[25],Mon.y[3]])]
        #大学寮　だいがくりょう# 
        J_G53 = [[Lyn.x[3],UMa.x[53]],[Lyn.y[3],UMa.y[53]]]
        JG53n = [numpy.mean([Lyn.x[3],UMa.x[53]]),\
                 numpy.mean([Lyn.y[3],UMa.y[53]])]
        #造酒司　みきし# 
        J_G54 = [[Cnc.x[2],Cnc.x[11]],[Cnc.y[2],Cnc.y[11]],[Cnc.x[2],Cnc.x[20]],[Cnc.y[2],Cnc.y[20]],\
                 [Cnc.x[3],Cnc.x[9]],[Cnc.y[3],Cnc.y[9]],[Cnc.x[3],Cnc.x[12]],[Cnc.y[3],Cnc.y[12]],\
                 [Cnc.x[8],Cnc.x[9]],[Cnc.y[8],Cnc.y[9]],[Cnc.x[8],Cnc.x[11]],[Cnc.y[8],Cnc.y[11]]]
        JG54n = [numpy.mean([Cnc.x[2],Cnc.x[3],Cnc.x[8],Cnc.x[9],Cnc.x[11],Cnc.x[12],Cnc.x[20]]),\
                 numpy.mean([Cnc.y[2],Cnc.y[3],Cnc.y[8],Cnc.y[9],Cnc.y[11],Cnc.y[12],Cnc.y[20]])]
        #織部　おりべ# 
        J_G55 = [[Hya.x[66],Hya.x[75]],[Hya.y[66],Hya.y[75]],[Hya.x[66],Hya.x[76]],[Hya.y[66],Hya.y[76]],\
                 [Hya.x[75],Sex.x[1]],[Hya.y[75],Sex.y[1]]]
        JG55n = [numpy.mean([Hya.x[66],Hya.x[75],Hya.x[76],Sex.x[1]]),\
                 numpy.mean([Hya.y[66],Hya.y[75],Hya.y[76],Sex.y[1]])]
        #斎宮　さいぐう# 
        J_G56 = []
        JG56n = [Ant.x[1],Ant.y[1]-labelxy]
        #雅楽# 
        J_G57 = [[Crv.x[8],Crt.x[8]],[Crv.y[8],Crt.y[8]]]
        JG57n = [numpy.mean([Crv.x[8],Crt.x[8]]),\
                 numpy.mean([Crv.y[8],Crt.y[8]])]
        #右衛門# 
        J_G58 = [[Cen.x[67],Hya.x[40]],[Cen.y[67],Hya.y[40]]]
        JG58n = [numpy.mean([Cen.x[67],Hya.x[40]]),\
                 numpy.mean([Cen.y[67],Hya.y[40]])]
        ## ?
        J_G59 = [[Hya.x[4],Hya.x[51]],[Hya.y[4],Hya.y[51]]]
        JG59n = [numpy.mean([Hya.x[4],Hya.x[51]]),\
                 numpy.mean([Hya.y[4],Hya.y[51]])]

        J_G_list = [J_G01,J_G02,J_G03,J_G04,J_G05,J_G06,J_G07,J_G08,J_G09,J_G10,\
                    J_G11,J_G12,J_G13,J_G14,J_G15,J_G16,J_G17,J_G18,J_G19,J_G20,\
                    J_G21,J_G22,J_G23,J_G24,J_G25,J_G26,J_G27,J_G28,J_G29,J_G30,\
                    J_G31,J_G32,J_G33,J_G34,J_G35,J_G36,J_G37,J_G38,J_G39,J_G40,\
                    J_G41,J_G42,J_G43,J_G44,J_G45,J_G46,J_G47,J_G48,J_G49,J_G50,\
                    J_G51,J_G52,J_G53,J_G54,J_G55,J_G56,J_G57,J_G58,J_G59]

        # 南宮朱雀 linecollection
        J_G_line_z_xy1 = []
        J_G_line_z_xy2 = [] 
        J_G_line_xy1 = []
        J_G_line_xy2 = []        
        for i in range(len(J_G_list)):
            for j in range(len(J_G_list[i]))[0::2]:
                if math.hypot(J_G_list[i][j][0]-J_G_list[i][j][1],J_G_list[i][j+1][0]-J_G_list[i][j+1][1]) < hori_border:
                    if i in set([0,20,27,29,34,36,38]):
                        J_G_line_z_xy1.append((J_G_list[i][j][0],J_G_list[i][j+1][0]))
                        J_G_line_z_xy2.append((J_G_list[i][j][1],J_G_list[i][j+1][1]))
                    else:
                        J_G_line_xy1.append((J_G_list[i][j][0],J_G_list[i][j+1][0]))
                        J_G_line_xy2.append((J_G_list[i][j][1],J_G_list[i][j+1][1]))

        J_G_line_z_list = []
        for i in range(len(J_G_line_z_xy1)):            
            J_G_line_z_list.append([J_G_line_z_xy1[i],J_G_line_z_xy2[i]])
        
        J_G_line_list = []
        for i in range(len(J_G_line_xy1)):            
            J_G_line_list.append([J_G_line_xy1[i],J_G_line_xy2[i]])
        
        lc_J_G_z = mc.LineCollection(J_G_line_z_list, colors='yellow', zorder=2+2.5)
        lc_J_G = mc.LineCollection(J_G_line_list, colors='white', zorder=2+2.5)
        lc_J_G_z.set_alpha(plot_alpha)
        lc_J_G.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_G_z)
        ax0.add_collection(lc_J_G)

        JGn_list = [[JG01n,'井宿'],[JG02n,'鉞'],[JG03n,'水府'],[JG04n,'天樽'],[JG05n,'五諸候'],\
                    [JG06n,'北河'],[JG07n,'積水'],[JG08n,'積薪'],[JG09n,'水位'],[JG10n,'南河'],\
                    [JG11n,'四涜'],[JG12n,'闕丘'],[JG13n,'軍市'],[JG14n,'野鶏'],[JG15n,'天狼'],\
                    [JG16n,'丈人'],[JG17n,'子'],[JG18n,'孫'],[JG19n,'老人'],[JG20n,'弧矢'],\
                    [JG21n,'鬼宿'],[JG22n,'積尸気'],[JG23n,'爟'],[JG24n,'外厨'],[JG25n,'天記'],\
                    [JG26n,'天狗'],[JG27n,'天社'],[JG28n,'柳宿'],[JG29n,'酒旗'],[JG30n,'星宿'],\
                    [JG31n,'天相'],[JG32n,'軒轅'],[JG33n,'內平'],[JG34n,'天稷'],[JG35n,'張宿'],\
                    [JG36n,'天廟'],[JG37n,'翼宿'],[JG38n,'東甌'],[JG39n,'軫宿'],[JG40n,'右轄'],\
                    [JG41n,'左轄'],[JG42n,'長沙'],[JG43n,'青邱'],[JG44n,'軍門'],[JG45n,'土司空'],\
                    [JG46n,'器府'],[JG47n,'曾孫'],[JG48n,'玄孫'],[JG49n,'箙'],[JG50n,'胡籙'],\
                    [JG51n,'隼人'],[JG52n,'主水'],[JG53n,'大学寮'],[JG54n,'造酒司'],[JG55n,'織部'],\
                    [JG56n,'斎宮'],[JG57n,'雅楽'],[JG58n,'右衛門'],[JG59n,'']]

        for i in range(len(JGn_list)):
            if len(JGn_list[i][0]) != 0:
                if (JGn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JGn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JGn_list[i][0])-min(JGn_list[i][0]) < hori_border:
                    if i in set([0,9,15,22,31,48,51]):
                        ax_label.annotate(str(JGn_list[i][1]),(JGn_list[i][0][0],JGn_list[i][0][1]),color='y',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    else:
                        ax_label.annotate(str(JGn_list[i][1]),(JGn_list[i][0][0],JGn_list[i][0][1]),color='w',\
                                          fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')

        ##########
        #南極星區#
        ##########

        #十字架# 
        J_H01 = [[Cru.x[0],Cru.x[4]],[Cru.y[0],Cru.y[4]],[Cru.x[2],Cru.x[3]],[Cru.y[2],Cru.y[3]]]
        JH01n = [numpy.mean([Cru.x[0],Cru.x[2],Cru.x[3],Cru.x[4]]),\
                 numpy.mean([Cru.y[0],Cru.y[2],Cru.y[3],Cru.y[4]])]
        #馬腹# 
        J_H02 = [[Cen.x[20],Cen.x[59]],[Cen.y[20],Cen.y[59]],[Cen.x[59],Cru.x[6]],[Cen.y[59],Cru.y[6]]]
        JH02n = [numpy.mean([Cen.x[20],Cen.x[59],Cru.x[6]]),\
                 numpy.mean([Cen.y[20],Cen.y[59],Cru.y[6]])]
        #蜜蜂# 
        J_H03 = [[Mus.x[0],Mus.x[1]],[Mus.y[0],Mus.y[1]],[Mus.x[0],Mus.x[4]],[Mus.y[0],Mus.y[4]],\
                 [Mus.x[1],Mus.x[2]],[Mus.y[1],Mus.y[2]],[Mus.x[2],Mus.x[4]],[Mus.y[2],Mus.y[4]]]
        JH03n = [numpy.mean([Mus.x[0],Mus.x[1],Mus.x[2],Mus.x[4]]),\
                 numpy.mean([Mus.y[0],Mus.y[1],Mus.y[2],Mus.y[4]])]
        #三角形#
        J_H04 = [[TrA.x[0],TrA.x[2]],[TrA.y[0],TrA.y[2]],[TrA.x[1],TrA.x[2]],[TrA.y[1],TrA.y[2]]]
        JH04n = [numpy.mean([TrA.x[0],TrA.x[1],TrA.x[2]]),\
                 numpy.mean([TrA.y[0],TrA.y[1],TrA.y[2]])]
        #異雀# 
        J_H05 = [[Aps.x[0],Aps.x[6]],[Aps.y[0],Aps.y[6]],[Aps.x[0],Aps.x[7]],[Aps.y[0],Aps.y[7]],\
                 [Aps.x[1],Aps.x[2]],[Aps.y[1],Aps.y[2]],[Aps.x[1],Oct.x[20]],[Aps.y[1],Oct.y[20]],\
                 [Aps.x[2],Aps.x[7]],[Aps.y[2],Aps.y[7]],[Aps.x[2],Aps.x[9]],[Aps.y[2],Aps.y[9]],\
                 [Aps.x[4],Aps.x[9]],[Aps.y[4],Aps.y[9]],[Aps.x[5],Aps.x[6]],[Aps.y[5],Aps.y[6]],\
                 [Aps.x[5],Oct.x[2]],[Aps.y[5],Oct.y[2]]]
        JH05n = [numpy.mean([Aps.x[0],Aps.x[1],Aps.x[2],Aps.x[4],Aps.x[5],Aps.x[6],Aps.x[7],Aps.x[9],\
                             Oct.x[2],Oct.x[20]]),\
                 numpy.mean([Aps.y[0],Aps.y[1],Aps.y[2],Aps.y[4],Aps.y[5],Aps.y[6],Aps.y[7],Aps.y[9],\
                             Oct.y[2],Oct.y[20]])]
        #孔雀# 
        J_H06 = [[Ind.x[0],Ind.x[2]],[Ind.y[0],Ind.y[2]],[Ind.x[0],Pav.x[0]],[Ind.y[0],Pav.y[0]],\
                 [Ind.x[2],Ind.x[3]],[Ind.y[2],Ind.y[3]],[Ind.x[3],Ind.x[5]],[Ind.y[3],Ind.y[5]],\
                 [Ind.x[5],Ind.x[14]],[Ind.y[5],Ind.y[14]],[Ind.x[14],Ind.x[18]],[Ind.y[14],Ind.y[18]],\
                 [Pav.x[0],Pav.x[1]],[Pav.y[0],Pav.y[1]],[Pav.x[1],Pav.x[2]],[Pav.y[1],Pav.y[2]],\
                 [Pav.x[1],Pav.x[4]],[Pav.y[1],Pav.y[4]],[Pav.x[1],Pav.x[7]],[Pav.y[1],Pav.y[7]],\
                 [Pav.x[2],Pav.x[4]],[Pav.y[2],Pav.y[4]],[Pav.x[2],Pav.x[6]],[Pav.y[2],Pav.y[6]],\
                 [Pav.x[3],Pav.x[5]],[Pav.y[3],Pav.y[5]],[Pav.x[3],Pav.x[9]],[Pav.y[3],Pav.y[9]],\
                 [Pav.x[4],Pav.x[5]],[Pav.y[4],Pav.y[5]],[Pav.x[6],Pav.x[9]],[Pav.y[6],Pav.y[9]]]
        JH06n = [numpy.mean([Ind.x[0],Ind.x[2],Ind.x[3],Ind.x[5],Ind.x[14],Ind.x[18],Pav.x[0],Pav.x[1],\
                             Pav.x[2],Pav.x[3],Pav.x[4],Pav.x[5],Pav.x[6],Pav.x[7],Pav.x[9]]),\
                 numpy.mean([Ind.y[0],Ind.y[2],Ind.y[3],Ind.y[5],Ind.y[14],Ind.y[18],Pav.y[0],Pav.y[1],\
                             Pav.y[2],Pav.y[3],Pav.y[4],Pav.y[5],Pav.y[6],Pav.y[7],Pav.y[9]])]
        #波斯# 
        J_H07 = [[Ind.x[4],Ind.x[8]],[Ind.y[4],Ind.y[8]],[Ind.x[7],Ind.x[8]],[Ind.y[7],Ind.y[8]],\
                 [Ind.x[8],Ind.x[16]],[Ind.y[8],Ind.y[16]]]
        JH07n = [numpy.mean([Ind.x[4],Ind.x[7],Ind.x[8],Ind.x[16]]),\
                 numpy.mean([Ind.y[4],Ind.y[7],Ind.y[8],Ind.y[16]])]
        #蛇首# 
        J_H08 = [[Hyi.x[3],Hyi.x[4]],[Hyi.y[3],Hyi.y[4]]]
        JH08n = [numpy.mean([Hyi.x[3],Hyi.x[4]]),\
                 numpy.mean([Hyi.y[3],Hyi.y[4]])]
        #鳥喙# 
        J_H09 = [[Tuc.x[0],Tuc.x[4]],[Tuc.y[0],Tuc.y[4]],[Tuc.x[2],Tuc.x[9]],[Tuc.y[2],Tuc.y[9]],\
                 [Tuc.x[2],Tuc.x[13]],[Tuc.y[2],Tuc.y[13]],[Tuc.x[3],Tuc.x[9]],[Tuc.y[3],Tuc.y[9]],\
                 [Tuc.x[3],Tuc.x[13]],[Tuc.y[3],Tuc.y[13]],[Tuc.x[4],Tuc.x[9]],[Tuc.y[4],Tuc.y[9]]]
        JH09n = [numpy.mean([Tuc.x[0],Tuc.x[2],Tuc.x[3],Tuc.x[4],Tuc.x[9],Tuc.x[13]]),\
                 numpy.mean([Tuc.y[0],Tuc.y[2],Tuc.y[3],Tuc.y[4],Tuc.y[9],Tuc.y[13]])]
        #鶴# 
        J_H10 = [[Gru.x[0],Gru.x[1]],[Gru.y[0],Gru.y[1]],[Gru.x[1],Gru.x[3]],[Gru.y[1],Gru.y[3]],\
                 [Gru.x[1],Gru.x[6]],[Gru.y[1],Gru.y[6]],[Gru.x[1],Gru.x[7]],[Gru.y[1],Gru.y[7]],\
                 [Gru.x[1],Gru.x[8]],[Gru.y[1],Gru.y[8]],[Gru.x[1],Gru.x[29]],[Gru.y[1],Gru.y[29]],\
                 [Gru.x[3],Gru.x[12]],[Gru.y[3],Gru.y[12]],[Gru.x[7],Tuc.x[1]],[Gru.y[7],Tuc.y[1]],\
                 [Gru.x[12],Tuc.x[1]],[Gru.y[12],Tuc.y[1]]]
        JH10n = [numpy.mean([Gru.x[0],Gru.x[1],Gru.x[3],Gru.x[6],Gru.x[7],Gru.x[8],Gru.x[12],Gru.x[29],\
                             Tuc.x[1]]),\
                 numpy.mean([Gru.y[0],Gru.y[1],Gru.y[3],Gru.y[6],Gru.y[7],Gru.y[8],Gru.y[12],Gru.y[29],\
                             Tuc.y[1]])]
        #水委# 
        J_H11 = []
        JH11n = [Eri.x[0],Eri.y[0]-labelxy]
        #附白# 
        J_H12 = []
        JH12n = [Ret.x[0],Ret.y[0]-labelxy]
        #夾白# 
        J_H13 = [[Dor.x[6],Dor.x[13]],[Dor.y[6],Dor.y[13]]]
        JH13n = [numpy.mean([Dor.x[6],Dor.x[13]]),\
                 numpy.mean([Dor.y[6],Dor.y[13]])]
        #金魚# 
        J_H14 = [[Dor.x[0],Dor.x[1]],[Dor.y[0],Dor.y[1]],[Dor.x[0],Dor.x[2]],[Dor.y[0],Dor.y[2]],\
                 [Dor.x[1],Dor.x[3]],[Dor.y[1],Dor.y[3]],[Dor.x[3],Dor.x[9]],[Dor.y[3],Dor.y[9]]]
        JH14n = [numpy.mean([Dor.x[0],Dor.x[1],Dor.x[2],Dor.x[3],Dor.x[9]]),\
                 numpy.mean([Dor.y[0],Dor.y[1],Dor.y[2],Dor.y[3],Dor.y[9]])]
        #海石# 
        J_H15 = [[Car.x[2],Vel.x[8]],[Car.y[2],Vel.y[8]],[Car.x[2],Car.x[10]],[Car.y[2],Car.y[10]],\
                 [Car.x[9],Vel.x[1]],[Car.y[9],Vel.y[1]],[Car.x[10],Vel.x[0]],[Car.y[10],Vel.y[0]],\
                 [Pup.x[15],Vel.x[0]],[Pup.y[15],Vel.y[0]],[Vel.x[1],Vel.x[8]],[Vel.y[1],Vel.y[8]]]
        JH15n = [numpy.mean([Car.x[2],Car.x[9],Car.x[10],Pup.x[15],Vel.x[0],Vel.x[1],Vel.x[8]]),\
                 numpy.mean([Car.y[2],Car.y[9],Car.y[10],Pup.y[15],Vel.y[0],Vel.y[1],Vel.y[8]])]
        #飛魚# 
        J_H16 = [[Vol.x[0],Vol.x[5]],[Vol.y[0],Vol.y[5]],[Vol.x[0],Vol.x[8]],[Vol.y[0],Vol.y[8]],\
                 [Vol.x[1],Vol.x[5]],[Vol.y[1],Vol.y[5]],[Vol.x[2],Vol.x[5]],[Vol.y[2],Vol.y[5]],\
                 [Vol.x[3],Vol.x[5]],[Vol.y[3],Vol.y[5]]]
        JH16n = [numpy.mean([Vol.x[0],Vol.x[1],Vol.x[2],Vol.x[3],Vol.x[5],Vol.x[8]]),\
                 numpy.mean([Vol.y[0],Vol.y[1],Vol.y[2],Vol.y[3],Vol.y[5],Vol.y[8]])]
        #南船# 
        J_H17 = [[Cen.x[11],Mus.x[12]],[Cen.y[11],Mus.y[12]],[Cen.x[11],Cen.x[29]],[Cen.y[11],Cen.y[29]],\
                 [Cen.x[11],Cen.x[57]],[Cen.y[11],Cen.y[57]],[Cen.x[11],Cen.x[61]],[Cen.y[11],Cen.y[61]],\
                 [Cen.x[11],Cen.x[72]],[Cen.y[11],Cen.y[72]],[Cen.x[11],Cen.x[73]],[Cen.y[11],Cen.y[73]],\
                 [Cen.x[11],Cen.x[84]],[Cen.y[11],Cen.y[84]]]
        JH17n = [numpy.mean([Cen.x[11],Cen.x[29],Cen.x[57],Cen.x[61],Cen.x[72],Cen.x[73],Cen.x[84],Mus.x[12]]),\
                 numpy.mean([Cen.y[11],Cen.y[29],Cen.y[57],Cen.y[61],Cen.y[72],Cen.y[73],Cen.y[84],Mus.y[12]])]
        #小斗# 
        J_H18 = [[Cha.x[1],Cha.x[5]],[Cha.y[1],Cha.y[5]],[Cha.x[1],Cha.x[18]],[Cha.y[1],Cha.y[18]],\
                 [Cha.x[2],Cha.x[5]],[Cha.y[2],Cha.y[5]]]
        JH18n = [numpy.mean([Cha.x[1],Cha.x[2],Cha.x[5],Cha.x[18]]),\
                 numpy.mean([Cha.y[1],Cha.y[2],Cha.y[5],Cha.y[18]])]

        J_H_list = [J_H01,J_H02,J_H03,J_H04,J_H05,J_H06,J_H07,J_H08,J_H09,J_H10,\
                    J_H11,J_H12,J_H13,J_H14,J_H15,J_H16,J_H17,J_H18]

        # 南極星區 linecollection
        J_H_line_xy1 = []
        J_H_line_xy2 = []        
        for i in range(len(J_H_list)):
            for j in range(len(J_H_list[i]))[0::2]:
                if math.hypot(J_H_list[i][j][0]-J_H_list[i][j][1],J_H_list[i][j+1][0]-J_H_list[i][j+1][1]) < hori_border:
                    J_H_line_xy1.append((J_H_list[i][j][0],J_H_list[i][j+1][0]))
                    J_H_line_xy2.append((J_H_list[i][j][1],J_H_list[i][j+1][1]))

        J_H_line_list = []
        for i in range(len(J_H_line_xy1)):            
            J_H_line_list.append([J_H_line_xy1[i],J_H_line_xy2[i]])
        
        lc_J_H = mc.LineCollection(J_H_line_list, colors='white', zorder=2+2.5)
        lc_J_H.set_alpha(plot_alpha)
        ax0.add_collection(lc_J_H)

        JHn_list = [[JH01n,'十字架'],[JH02n,'馬腹'],[JH03n,'蜜蜂'],[JH04n,'三角形'],[JH05n,'異雀'],\
                    [JH06n,'孔雀'],[JH07n,'波斯'],[JH08n,'蛇首'],[JH09n,'鳥喙'],[JH10n,'鶴'],\
                    [JH11n,'水委'],[JH12n,'附白'],[JH13n,'夾白'],[JH14n,'金魚'],[JH15n,'海石'],\
                    [JH16n,'飛魚'],[JH17n,'南船'],[JH18n,'小斗']]

        for i in range(len(JHn_list)):
            if len(JHn_list[i][0]) != 0:
                if (JHn_list[i][0][0]-x_shift.get())**2 < (hori_border/2)**2-((JHn_list[i][0][1]-y_shift.get())/aspect_ratio.get())**2 \
                   and max(JHn_list[i][0])-min(JHn_list[i][0]) < hori_border:
                    ax_label.annotate(str(JHn_list[i][1]),(JHn_list[i][0][0],JHn_list[i][0][1]),color='w',\
                                      fontproperties=chara_chi,horizontalalignment='center',verticalalignment='top')
                    
def plot_MW():
    print('weaving Milkyway')
    prompt_text('weaving Milkyway')
    fm_bottom.update()
    
    MW_list = [MW_southernedge,MW_MonPer,MW_CamCas,MW_Cep,MW_CygOph,MW_OphSco,MW_LupVel,MW_VelMon,\
               dark_PerCas,dark_CasCep,dark_betaCas,dark_CygCep,dark_CygOph,dark_thetaOph,dark_lambdaSco,dark_ScoNor,dark_Coalsack,dark_Vel,\
               MW_LMC1,MW_LMC2,MW_SMC]

    for df in MW_list:
        df.x = list(map(transform_x, df.RA, df.Dec))
        df.y = list(map(transform_y, df.RA, df.Dec))
        for i in range(len(df)-1):
            if (df.x[i]-x_shift.get())**2 < (hori_border/2)**2-((df.y[i]-y_shift.get())/aspect_ratio.get())**2:
                ax_label.plot([df.x[i],df.x[i+1]],[df.y[i],df.y[i+1]],'b-',alpha=plot_alpha,zorder=1+2.5)

    print('drawing boundaries')
    prompt_text('drawing boundaries')
    fm_bottom.update()
    
    boundary.x = list(map(transform_x, boundary.RA*15, boundary.Dec)) #convert RA to degrees
    boundary.y = list(map(transform_y, boundary.RA*15, boundary.Dec))
    
    boundary_line_list = []
    for i in range(len(boundary)-1):
        if (boundary.x[i]-x_shift.get())**2 < (hori_border/2)**2-((boundary.y[i]-y_shift.get())/aspect_ratio.get())**2 and \
           (boundary.x[i+1]-x_shift.get())**2 < (hori_border/2)**2-((boundary.y[i+1]-y_shift.get())/aspect_ratio.get())**2 and \
           boundary.Constellation[i] == boundary.Constellation[i+1]:
            boundary_line_list.append([(boundary.x[i],boundary.y[i]),(boundary.x[i+1],boundary.y[i+1])])
    
    lc_boundary = mc.LineCollection(boundary_line_list, colors=[1,0.5,0,0.15], zorder=1+2.5)
    ax_label.add_collection(lc_boundary)

def prompt_text(message):
    prompttext_var = tk.StringVar()
    prompttext_var.set(str(datetime.now().strftime('%X'))+'>'+message)
    prompttext = tk.Label(fm_prompt, textvariable=str(prompttext_var), font=TMN_10, bg='black', fg='white', anchor='w')
    prompttext.grid(row=0, column=0, columnspan=2, sticky='EW')

def cursor_info():
    global ax_cursor
    ax_cursor.remove()
    ax_cursor = ax0.twiny()
    #cursor x court from left to right [0,1]?
    #cursor y count from bottom to top [-240,240]
    #asc[y,x]
    #asc x count from left to right [0,719]
    #asc y count from top to bottom [0,479]
    #pixel data are int8, avoid over 256
    numpy.seterr(divide='ignore', invalid='ignore') #ignore /0 or nan error
    if button_mode.get() == 1:
        ax_cursor.format_coord = lambda x,y : "x=%.3f y=%.3f [%03d %03d %03d] S=%.3f B/R=%.3f" \
                                 % (x*720-360, y, asc[int(240-y+.5),int(x*720+.5),0], asc[int(240-y+.5),int(x*720+.5),1], asc[int(240-y+.5),int(x*720+.5),2], \
                                    1-min(asc[int(240-y+.5),int(x*720+.5),0], asc[int(240-y+.5),int(x*720+.5),1], asc[int(240-y+.5),int(x*720+.5),2])/\
                                    (asc[int(240-y+.5),int(x*720+.5),0]/3+asc[int(240-y+.5),int(x*720+.5),1]/3+asc[int(240-y+.5),int(x*720+.5),2]/3), \
                                    (asc[int(240-y+.5),int(x*720+.5),2]/2-asc[int(240-y+.5),int(x*720+.5),0]/2)/(asc[int(240-y+.5),int(x*720+.5),2]/2+asc[int(240-y+.5),int(x*720+.5),0]/2))
    else:
        ax_cursor.format_coord = lambda x,y : "x=%.3f y=%.3f" % (x*720-360, y)
    
def plot_ASC():
    global ax_label
    # show image
    ax0.imshow(asc, extent=[-360, 360, -240, 240])
    transform_stars()
    
    # redraw grid lines
    try:
        horizon_line.remove()
        equator_line.remove()
        ecliptic_line.remove()
    except:
        print('no grids')
    plot_horizon()
    
    # refresh all labels (all text + MW + boundary)
    reset_label()
    cursor_info()
    
    # redraw stars
    try:
        manystars.remove()
    except:
        print('no stars')
    plot_stars()

    # remove all previous constellations if any
    wipe_constellations()
    plot_constellation()

    # redraw solar sys
    try:
        solar_obj.remove()
    except:
        print('no solar sys')
    plot_solar()
    solar_label()

    # cant put MW into a single artists rightnow, need to be handled seperatly
    if button_mode.get() == 2:
        plot_MW()
            
    #plt.axis('off')
    fig.canvas.draw() # plot
    fig.canvas.flush_events()
    print('done')
    prompt_text('done')
    fm_bottom.update()

def moonglow(): # Moonglow observatory
    global hokoon, asc
    
    hokoon.date = datetime.utcnow()
    hokoon.lon = '266.23134' 
    hokoon.lat = '38.829091'
    urlretrieve('http://www.allskycam.com/u/391/latest_full6.jpg', 'asc.jpg')
    asc = plt.imread('asc.jpg')
    update_para()
    plot_ASC()
    prompt_text('Moonglow observatory now. just to let you know this cam can actually capture stars except the Sun')
    fm_bottom.update()

def refresh_sky(): # Hokoon
    global hokoon, asc

    hokoon.date = datetime.utcnow()
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    
    if button_mode.get() == 1:
        try:
            urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
            asc = plt.imread('asc.jpg')
        except HTTPError:
            asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','serverdead.jpg'))
            prompt_text('server death count +1')
            fm_bottom.update()
    elif button_mode.get() ==2:
        asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','black.jpg'))
        
    update_para()
    side_button()
    plot_ASC()

def sky_20170215_2131():
    global hokoon, asc
    
    hokoon.date = '2017/02/15 13:31:02'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170215_2131.jpg'))
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/02/15 13:31:02')
    fm_bottom.update()
    
def sky_20170215_2302(): 
    global hokoon, asc
    
    hokoon.date = '2017/02/15 15:02:02'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170215_2302.jpg'))
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/02/15 15:02:02')
    fm_bottom.update()
    
def sky_20170218_2000(): 
    global hokoon, asc
    
    hokoon.date = '2017/02/18 12:00:00'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170218_2000.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/02/18 12:00:00')
    fm_bottom.update()
    
def sky_20170302_1939(): 
    global hokoon, asc
    
    hokoon.date = '2017/03/02 11:39:00'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170302_1939.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/03/02 11:39:00')
    fm_bottom.update()
    
def sky_20170325_0142(): 
    global hokoon, asc
    
    hokoon.date = '2017/03/24 17:42:00'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170325_0142.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/03/24 17:42:00')
    fm_bottom.update()
    
def sky_20170327_2331(): 
    global hokoon, asc
    
    hokoon.date = '2017/03/27 15:31:00'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170327_2331.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/03/27 15:31:00')
    fm_bottom.update()
    
def sky_20170402_2204(): 
    global hokoon, asc
    
    hokoon.date = '2017/04/02 14:04:00'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170402_2204.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/04/02 14:04:00')
    fm_bottom.update()
    
def sky_20170726_2000(): 
    global hokoon, asc
    
    hokoon.date = '2017/07/26 12:00:02'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170726_2000.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/07/26 12:00:02')
    fm_bottom.update()
    
def sky_20170922_0500(): 
    global hokoon, asc
    
    hokoon.date = '2017/09/21 21:00:01'
    hokoon.lon = '114.108008'
    hokoon.lat = '22.383678'
    asc = plt.imread(pathlib.Path.cwd().joinpath('ASC','asc20170922_0500.jpg')) 
    update_para()
    plot_ASC()
    prompt_text('Hokoon at 2017/09/21 21:00:01')
    fm_bottom.update()
    
# adjustment
def update_para():
    global transform_x, transform_y, ra0, dec0, zenith_shift_ra, zenith_shift_dec, rotate_angle, aspect_ratio, plot_scale, x_shift, y_shift

    ra0 = math.degrees(hokoon.sidereal_time()) + zenith_shift_ra.get()
    dec0 = math.degrees(hokoon.lat) + zenith_shift_dec.get()
    
##    # projection formula (Stereographic)  # plot_scale ~ 130
##    transform_x = lambda x,y: plot_scale\
##                  *(-2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##                  *math.cos(math.radians(y))*math.sin(math.radians(x-ra0))
##    transform_y = lambda x,y: aspect_ratio*plot_scale\
##                  *(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##                  *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))

##    # projection formula (Azimuthal Equidistant)  # plot_scale ~ 150
##    transform_x = lambda x,y: plot_scale\
##                  *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
##                  *((math.acos(math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##                    /math.sin(math.acos(math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
##    transform_y = lambda x,y: aspect_ratio*plot_scale\
##                  *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
##                  *((math.acos(math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##                    /math.sin(math.acos(math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))

##    # projection formula (Lambert Azimuthal Equal-Area)  # plot_scale ~ 180
##    transform_x = lambda x,y: plot_scale\
##                  *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
##                  *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))
##    transform_y = lambda x,y: aspect_ratio*plot_scale\
##                  *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
##                  *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))

##    # projection formula (Orthographic)  # plot_scale ~ 250
##    transform_x = lambda x,y: plot_scale\
##                  *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))
##    transform_y = lambda x,y: aspect_ratio*plot_scale\
##                  *(math.cos(math.radians(dec0))*math.sin(math.radians(y))\
##                    -math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))

    # projection formula (Lambert Azimuthal Equal-Area with rotation)  # plot_scale ~ 174  # for Moonglow ASC
    transform_x = lambda x,y: x_shift.get()+plot_scale.get()\
                  *(math.cos(math.radians(rotate_angle.get()))\
                   *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                   -math.sin(math.radians(rotate_angle.get()))\
                   *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
    transform_y = lambda x,y: y_shift.get()+aspect_ratio.get()*plot_scale.get()\
                  *(math.sin(math.radians(rotate_angle.get()))\
                   *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
                   +math.cos(math.radians(rotate_angle.get()))\
                   *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
                   *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
    
def RA_plus():
    global zenith_shift_ra
    zenith_shift_ra.set(zenith_shift_ra.get() + 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('zenith RA shift added 0.5\N{DEGREE SIGN}')
    fm_bottom.update()

def RA_minus():
    global zenith_shift_ra
    zenith_shift_ra.set(zenith_shift_ra.get() - 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('zenith RA shift subtracted 0.5\N{DEGREE SIGN}')
    fm_bottom.update()
    
def Dec_plus():
    global zenith_shift_dec
    zenith_shift_dec.set(zenith_shift_dec.get() + 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('zenith Dec shift added 0.5\N{DEGREE SIGN}')
    fm_bottom.update()
    
def Dec_minus():
    global zenith_shift_dec
    zenith_shift_dec.set(zenith_shift_dec.get() - 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('zenith Dec shift subtracted 0.5\N{DEGREE SIGN}')
    fm_bottom.update()
        
def rotate_plus():
    global rotate_angle
    rotate_angle.set(rotate_angle.get() + 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('turned 0.5\N{DEGREE SIGN} anticlockwise')
    fm_bottom.update()
       
def rotate_minus():
    global rotate_angle
    rotate_angle.set(rotate_angle.get() - 0.5)
    
    update_para()
    plot_ASC()
    prompt_text('turned 0.5\N{DEGREE SIGN} clockwise')
    fm_bottom.update()
   
def aspect_plus():
    global aspect_ratio
    aspect_ratio.set(aspect_ratio.get() + 0.01)
    
    update_para()
    plot_ASC()
    prompt_text('aspect ratio increased 0.01')
    fm_bottom.update()
       
def aspect_minus():
    global aspect_ratio
    aspect_ratio.set(aspect_ratio.get() - 0.01)
    
    update_para()
    plot_ASC()
    prompt_text('aspect ratio decreased 0.01')
    fm_bottom.update()
           
def scale_plus():
    global plot_scale
    plot_scale.set(plot_scale.get() + 1)
    
    update_para()
    plot_ASC()
    prompt_text('scale incresed by 1')
    fm_bottom.update()
    
def scale_minus():
    global plot_scale
    plot_scale.set(plot_scale.get() - 1)
    
    update_para()
    plot_ASC()
    prompt_text('scale decresed by 1')
    fm_bottom.update()
    
def x_shift_plus():
    global x_shift
    x_shift.set(x_shift.get() + 0.5)
    
    plot_ASC()
    prompt_text('plot shifted right 0.5')
    fm_bottom.update()

def x_shift_minus():
    global x_shift
    x_shift.set(x_shift.get() - 0.5)
    
    plot_ASC()
    prompt_text('plot shifted left 0.5')
    fm_bottom.update()

def y_shift_plus():
    global y_shift
    y_shift.set(y_shift.get() + 0.5)
    
    plot_ASC()
    prompt_text('plot shifted up 0.5')
    fm_bottom.update()

def y_shift_minus():
    global y_shift
    y_shift.set(y_shift.get() - 0.5)
    
    plot_ASC()
    prompt_text('plot shifted down 0.5')
    fm_bottom.update()

def set_para():
    global plot_para, zenith_shift_ra, zenith_shift_dec, rotate_angle, aspect_ratio, plot_scale, x_shift, y_shift
    plot_para.loc[0] = zenith_shift_ra.get()
    plot_para.loc[1] = zenith_shift_dec.get()
    plot_para.loc[2] = rotate_angle.get()
    plot_para.loc[3] = aspect_ratio.get() 
    plot_para.loc[4] = plot_scale.get()
    plot_para.loc[5] = x_shift.get()
    plot_para.loc[6] = y_shift.get()
    plot_para[0].to_csv(pathlib.Path.cwd().joinpath('ASC','plot_para.csv'), header=None, index=None)
    save_para.set('saved!')
    prompt_text('parameters overwrote, regert is already too late')
    fm_bottom.update()

def restore_default():
    global plot_para, zenith_shift_ra, zenith_shift_dec, rotate_angle, aspect_ratio, plot_scale, x_shift, y_shift
    zenith_shift_ra.set(-3.0)
    zenith_shift_dec.set(-1.5)
    rotate_angle.set(-1.5)
    aspect_ratio.set(0.94) 
    plot_scale.set(174.0)
    x_shift.set(-11.5)
    y_shift.set(6.0)
    plot_ASC()
    prompt_text('restored to default')
    fm_bottom.update()    
    
# stops mainloop. this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate
def _quit():
    root.quit()     
    root.destroy()

def poly_oval(x0,y0, x1,y1, steps=300, rotation=0): # x0,y0,x1,y1 are as create_oval,rotation is in degrees anti-clockwise
    """return an oval as coordinates suitable for create_polygon"""

    rotation = rotation * math.pi / 180.0

    # major and minor axes
    a = (x1 - x0) / 2.0
    b = (y1 - y0) / 2.0

    # center
    xc = x0 + a
    yc = y0 + b

    point_list = []

    # create the oval as a list of points
    for i in range(steps):

        # Calculate the angle for this step
        # 360 degrees == 2 pi radians
        theta = (math.pi * 2) * (float(i) / steps)

        x1 = a * math.cos(theta)
        y1 = b * math.sin(theta)

        # rotate x, y
        x = (x1 * math.cos(rotation)) + (y1 * math.sin(rotation))
        y = (y1 * math.cos(rotation)) - (x1 * math.sin(rotation))

        point_list.append(round(x + xc))
        point_list.append(round(y + yc))

    return point_list

def moon_phase():
    global moon_chi
    Moon.compute(hokoon)
    
    # position angle of the Moon's bright limb from North point of the disc of the Moon to East
    print('drawing Moon')
    prompt_text('drawing Moon')
    fm_bottom.update()
    moon_chi_0 = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Moon.ra),\
                                         math.sin(Sun.dec)*math.cos(Moon.dec)-math.cos(Sun.dec)*math.sin(Moon.dec)*math.cos(Sun.ra-Moon.ra)))
    if moon_chi_0<0:
        moon_chi = moon_chi_0+360
    else:
        moon_chi = moon_chi_0

    # Moon phase
    text_Moon_ph = tk.Label(fm_side, text='Moon Phase', font=DjV_S_12_, justify='center', bg='black', fg='white')
    text_Moon_ph.grid(row=0, column=0, columnspan=4, sticky='EW')

    draw_moon = tk.Canvas(fm_side, width=180, height=150, bg='black')
    draw_moon.grid(row=1, column=0, columnspan=4)
    draw_moon.configure(borderwidth=0, highlightthickness=0)
    ph_x0 = 90 # center x
    ph_y0 = 75 # center y
    ph_r = 50*Moon.size/2100 # line inner radius
    ph_R = 60*Moon.size/2100 # line outer radius
    ph_l = 65*Moon.size/2100 # text radius
    M_d = Moon.size/2100*110
    M_offsetx = (180-M_d)/2
    M_offsety = (150-M_d)/2
    rot_pa_limb_moon = moon_chi-90 # rotate for position angle of the Moon's bright limb, parallatic angle count from zenith to eq. north clockwise
    
    if Moon.phase == 0:
        draw_moon.create_oval(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, fill='#94908D', width=0)
    elif 0 < Moon.phase < 50:
        draw_moon.create_oval(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, fill='#F0F0F0', width=0)
        draw_moon.create_arc(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, \
                             start=270+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), extent=180, fill='#94908D', outline='#94908D', width=0)
        draw_moon.create_polygon(tuple(poly_oval(M_d*(1-Moon.phase/100)+M_offsetx,0+M_offsety,M_d*Moon.phase/100+M_offsetx,M_d+M_offsety, \
                                                 rotation=rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()))), fill='#94908D', outline='#94908D', width=0)
    elif Moon.phase == 50:
        draw_moon.create_oval(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, fill='#94908D', width=0)
        draw_moon.create_arc(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, \
                             start=90+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), extent=180, fill='#F0F0F0', outline='#F0F0F0', width=0)
    elif 50 < Moon.phase < 100:
        draw_moon.create_oval(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, fill='#94908D', width=0)
        draw_moon.create_polygon(tuple(poly_oval(M_d*(1-Moon.phase/100)+M_offsetx,0+M_offsety,M_d*Moon.phase/100+M_offsetx,M_d+M_offsety, \
                                                 rotation=rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()))), fill='#F0F0F0', outline='#F0F0F0', width=0)
        draw_moon.create_arc(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, \
                             start=90+rot_pa_limb_moon-math.degrees(Moon.parallactic_angle()), extent=180, fill='#F0F0F0', outline='#F0F0F0', width=0)
    elif Moon.phase == 100:
        draw_moon.create_oval(0+M_offsetx,0+M_offsety,M_d+M_offsetx,M_d+M_offsety, fill='#F0F0F0', width=0)
    
    # eq. coord.
    if Moon.alt > 0:
        draw_moon.create_text(ph_x0+ph_l*math.sin(Moon.parallactic_angle()),ph_y0-ph_l*math.cos(Moon.parallactic_angle()),\
                              angle=-math.degrees(Moon.parallactic_angle()), text='N', fill='red')
        draw_moon.create_line(ph_x0+ph_r*math.sin(Moon.parallactic_angle()),ph_y0-ph_r*math.cos(Moon.parallactic_angle()),\
                              ph_x0+ph_R*math.sin(Moon.parallactic_angle()),ph_y0-ph_R*math.cos(Moon.parallactic_angle()), fill='red')
        draw_moon.create_text(ph_x0+ph_l*math.sin(Moon.parallactic_angle()+3*math.pi/2),ph_y0-ph_l*math.cos(Moon.parallactic_angle()+3*math.pi/2),\
                              angle=-math.degrees(Moon.parallactic_angle()), text='E', fill='red')
        draw_moon.create_line(ph_x0+ph_r*math.sin(Moon.parallactic_angle()+3*math.pi/2),ph_y0-ph_r*math.cos(Moon.parallactic_angle()+3*math.pi/2),\
                              ph_x0+ph_R*math.sin(Moon.parallactic_angle()+3*math.pi/2),ph_y0-ph_R*math.cos(Moon.parallactic_angle()+3*math.pi/2), fill='red')
        draw_moon.create_text(ph_x0+ph_l*math.sin(Moon.parallactic_angle()+math.pi),ph_y0-ph_l*math.cos(Moon.parallactic_angle()+math.pi),\
                              angle=-math.degrees(Moon.parallactic_angle()), text='S', fill='red')
        draw_moon.create_line(ph_x0+ph_r*math.sin(Moon.parallactic_angle()+math.pi),ph_y0-ph_r*math.cos(Moon.parallactic_angle()+math.pi),\
                              ph_x0+ph_R*math.sin(Moon.parallactic_angle()+math.pi),ph_y0-ph_R*math.cos(Moon.parallactic_angle()+math.pi), fill='red')
        draw_moon.create_text(ph_x0+ph_l*math.sin(Moon.parallactic_angle()+math.pi/2),ph_y0-ph_l*math.cos(Moon.parallactic_angle()+math.pi/2),\
                              angle=-math.degrees(Moon.parallactic_angle()), text='W', fill='red')
        draw_moon.create_line(ph_x0+ph_r*math.sin(Moon.parallactic_angle()+math.pi/2),ph_y0-ph_r*math.cos(Moon.parallactic_angle()+math.pi/2),\
                              ph_x0+ph_R*math.sin(Moon.parallactic_angle()+math.pi/2),ph_y0-ph_R*math.cos(Moon.parallactic_angle()+math.pi/2), fill='red')
    draw_moon.create_text(21,132,text='eq \ncoord.', font=DjV_S_10, fill='red', justify='left')

    # selenographic
    draw_moon.create_text(155,132,text='seleno-\ngraphic', font=DjV_S_10, fill='cyan', justify='right')

    T = (ephem.julian_date(hokoon)-2451545)/36525 # should use Julian Emphemeris Date instead
    asc_node = 125.04452-1934.136261*T\
               +0.0020708*T*T\
               +T*T*T/450000 # longitude of ascending node of Moon mean orbit
    L_s = 280.4665+36000.7698*T # mean longitude of Sun
    L_m = 218.3165+481267.8813*T # mean longitude of Moon
    nu_lon = -17.2/3600*math.sin(math.radians(asc_node))\
             -1.32/3600*math.sin(math.radians(2*L_s))\
             -0.23/3600*math.sin(math.radians(2*L_m))\
             +0.21/3600*math.sin(math.radians(2*asc_node)) # nutation in longitude
    Inc = 1.54242 # inclination of mean lunar equator to ecliptic
    M_s = 357.5291092\
          +35999.0502909*T\
          -0.0001536*T*T\
          +T*T*T/24490000 # Sun mean anomaly
    M_m = 134.9634114\
          +477198.8676313*T\
          +0.008997*T*T\
          +T*T*T/69699\
          -T*T*T*T/14712000 # Moon mean anomaly
    D_m = 297.8502042\
          +445267.1115168*T\
          -0.00163*T*T\
          +T*T*T/545868\
          -T*T*T*T/113065000 # mean elongation of Moon
    F_m = 93.2720993\
          +483202.0175273*T\
          -0.0034029*T*T\
          -T*T*T/3526000\
          +T*T*T*T/863310000 # Moon argument of latitude
    rho = -0.02752*math.cos(math.radians(M_m))\
          -0.02245*math.sin(math.radians(F_m))\
          +0.00684*math.cos(math.radians(M_m-2*F_m))\
          -0.00293*math.cos(math.radians(2*F_m))\
          -0.00085*math.cos(math.radians(2*F_m-2*D_m))\
          -0.00054*math.cos(math.radians(M_m-2*D_m))\
          -0.0002*math.sin(math.radians(M_m+F_m))\
          -0.0002*math.cos(math.radians(M_m+2*F_m))\
          -0.0002*math.cos(math.radians(M_m-F_m))\
          +0.00014*math.cos(math.radians(M_m+2*F_m-2*D_m))
    sigma = -0.02816*math.sin(math.radians(M_m))\
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
    V_m = asc_node + nu_lon + sigma/math.sin(math.radians(Inc))
    epsilion = 23.4355636928 #(IAU 2000B nutation series)
    X_m = math.sin(math.radians(Inc)+rho)*math.sin(math.radians(V_m))
    Y_m = math.sin(math.radians(Inc)+rho)*math.cos(math.radians(V_m))*math.cos(math.radians(epsilion))\
          -math.cos(math.radians(Inc)+rho)*math.sin(math.radians(epsilion))
    omega = math.atan2(X_m,Y_m)
    PA_axis_moon_N = math.asin(math.sqrt(X_m*X_m+Y_m*Y_m)*math.cos(Moon.ra-omega)/math.cos(Moon.libration_lat))
            
    PA_axis_moon_z = Moon.parallactic_angle()-PA_axis_moon_N # clockwise
    
    draw_moon.create_text(ph_x0+ph_l*math.sin(PA_axis_moon_z),ph_y0-ph_l*math.cos(PA_axis_moon_z),\
                          angle=-math.degrees(PA_axis_moon_z), text='N', fill='cyan')
    draw_moon.create_line(ph_x0+ph_r*math.sin(PA_axis_moon_z),ph_y0-ph_r*math.cos(PA_axis_moon_z),\
                          ph_x0+ph_R*math.sin(PA_axis_moon_z),ph_y0-ph_R*math.cos(PA_axis_moon_z), fill='cyan')
    draw_moon.create_text(ph_x0+ph_l*math.sin(PA_axis_moon_z+math.pi/2),ph_y0-ph_l*math.cos(PA_axis_moon_z+math.pi/2),\
                          angle=-math.degrees(PA_axis_moon_z), text='E', fill='cyan')
    draw_moon.create_line(ph_x0+ph_r*math.sin(PA_axis_moon_z+math.pi/2),ph_y0-ph_r*math.cos(PA_axis_moon_z+math.pi/2),\
                          ph_x0+ph_R*math.sin(PA_axis_moon_z+math.pi/2),ph_y0-ph_R*math.cos(PA_axis_moon_z+math.pi/2), fill='cyan')
    draw_moon.create_text(ph_x0+ph_l*math.sin(PA_axis_moon_z+math.pi),ph_y0-ph_l*math.cos(PA_axis_moon_z+math.pi),\
                          angle=-math.degrees(PA_axis_moon_z), text='S', fill='cyan')
    draw_moon.create_line(ph_x0+ph_r*math.sin(PA_axis_moon_z+math.pi),ph_y0-ph_r*math.cos(PA_axis_moon_z+math.pi),\
                          ph_x0+ph_R*math.sin(PA_axis_moon_z+math.pi),ph_y0-ph_R*math.cos(PA_axis_moon_z+math.pi), fill='cyan')
    draw_moon.create_text(ph_x0+ph_l*math.sin(PA_axis_moon_z+3*math.pi/2),ph_y0-ph_l*math.cos(PA_axis_moon_z+3*math.pi/2),\
                          angle=-math.degrees(PA_axis_moon_z), text='W', fill='cyan')
    draw_moon.create_line(ph_x0+ph_r*math.sin(PA_axis_moon_z+3*math.pi/2),ph_y0-ph_r*math.cos(PA_axis_moon_z+3*math.pi/2),\
                          ph_x0+ph_R*math.sin(PA_axis_moon_z+3*math.pi/2),ph_y0-ph_R*math.cos(PA_axis_moon_z+3*math.pi/2), fill='cyan')

    # Mare in Orthographic projection with rotation
    lon0 = math.degrees(Moon.libration_long)
    lat0 = math.degrees(Moon.libration_lat)
    
    moon_rot = -math.degrees(PA_axis_moon_z) # anti-clockwise
    transform_moon_x = lambda x,y: ph_x0+M_d/2*(math.cos(math.radians(moon_rot))\
                                                *(math.cos(math.radians(y))*math.sin(math.radians(x-lon0)))\
                                                -math.sin(math.radians(moon_rot))\
                                                *(math.cos(math.radians(lat0))*math.sin(math.radians(y))-math.sin(math.radians(lat0))*math.cos(math.radians(y))*math.cos(math.radians(x-lon0)))) 
    transform_moon_y = lambda x,y: ph_y0-M_d/2*(math.sin(math.radians(moon_rot))\
                                                *(math.cos(math.radians(y))*math.sin(math.radians(x-lon0)))\
                                                +math.cos(math.radians(moon_rot))\
                                                *(math.cos(math.radians(lat0))*math.sin(math.radians(y))-math.sin(math.radians(lat0))*math.cos(math.radians(y))*math.cos(math.radians(x-lon0))))
    
    Mare_pt_lon = Mare.groupby('shapeid')['x'].apply(list)
    Mare_pt_lat = Mare.groupby('shapeid')['y'].apply(list)

    Mare_pt_list = Mare.groupby('shapeid')['x'].sum().reset_index()['shapeid']
    mare3 = time.time()
    for i in Mare_pt_list:
        Mare_pt_x = list(map(transform_moon_x, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_pt_y = list(map(transform_moon_y, Mare_pt_lon.loc[i], Mare_pt_lat.loc[i]))
        Mare_poly = list(itertools.chain.from_iterable(zip(Mare_pt_x,Mare_pt_y)))
        draw_moon.create_polygon(Mare_poly,fill='#696e65')
    
    mare4 = time.time()
    print('draw')
    print(mare4-mare3)
    
    # zenith
    if Moon.alt > 0:
        draw_moon.create_line(ph_x0,ph_y0-M_d/2,ph_x0,0, fill='green', arrow=tk.LAST)
        draw_moon.create_text(163,5,text=str(round(Moon.size/60,1))+"'", font=DjV_S_10, fill='orange', justify='right')
    else:
        draw_moon.create_text(134,5,text='below horizon', font=DjV_S_10, fill='orange', justify='right')
    draw_moon.create_text(21,5, text='zenith', font=DjV_S_10, fill='green')
    
    phase_moon = StringVar()
    phase_moon.set('illuminated '+str(round(Moon.phase,2))+'%') # projected 2D apparent area
    if Moon.phase >= 0:
        text_phase_moon = tk.Label(fm_side, textvariable=str(phase_moon), font=DjV_S_10, bg='black', fg='#F0F0F0')
    else:
        text_phase_moon = tk.Label(fm_side, textvariable=str(phase_moon), font=DjV_S_10, bg='black', fg='#94908D')
    text_phase_moon.grid(row=2, column=0, columnspan=4, sticky='EW')

    text_spacer3 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer3.grid(row=3, column=0, columnspan=4, sticky='EW')

def jovian_moons():
    Jupiter.compute(hokoon)
    Io.compute(hokoon)
    Europa.compute(hokoon)
    Ganymede.compute(hokoon)
    Callisto.compute(hokoon)
    
    print('drawing Jupiter')
    prompt_text('drawing Jupiter')
    fm_bottom.update()
    
    text_jov = tk.Label(fm_side, text='Jovian Moons', font=DjV_S_12_, bg='black', fg='white')
    text_jov.grid(row=4, column=0, columnspan=4, sticky='EW')
    
    draw_jov = tk.Canvas(fm_side, width=180, height=70, bg='black')
    draw_jov.grid(row=5, column=0, columnspan=4)
    draw_jov.configure(borderwidth=0, highlightthickness=0)

    jov_x0 = 90
    jov_y0 = 35
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
    
    draw_jov.create_oval(jov_x0+jov_radius,jov_y0-jov_radius,jov_x0-jov_radius,jov_y0+jov_radius, width=0, fill='#C88B3A')
    
    if not (Io.z < 0 and jov_x0-1 < Io.x < jov_x0+1):
        draw_jov.create_oval(jov_x0-Io.x*jov_radius-Io_r,jov_y0+Io.y*jov_radius-Io_r,\
                             jov_x0-Io.x*jov_radius+Io_r,jov_y0+Io.y*jov_radius+Io_r, width=0, fill='#9f9538')
    draw_jov.create_text(jov_x0-Io.x*jov_radius,60,text='I', font=DjV_S_8, fill='#9f9538', justify='center')
    
    if not (Europa.z < 0 and jov_x0-1 < Europa.x < jov_x0+1):
        draw_jov.create_oval(jov_x0-Europa.x*jov_radius-Eu_r,jov_y0+Europa.y*jov_radius-Eu_r,\
                             jov_x0-Europa.x*jov_radius+Eu_r,jov_y0+Europa.y*jov_radius+Eu_r, width=0, fill='#6c5d40')
    draw_jov.create_text(jov_x0-Europa.x*jov_radius,60,text='E', font=DjV_S_8, fill='#6c5d40', justify='center')
    
    if not (Callisto.z < 0 and jov_x0-1 < Callisto.x < jov_x0+1):
        draw_jov.create_oval(jov_x0-Callisto.x*jov_radius-Ca_r,jov_y0+Callisto.y*jov_radius-Ca_r,\
                             jov_x0-Callisto.x*jov_radius+Ca_r,jov_y0+Callisto.y*jov_radius+Ca_r, width=0, fill='#766b5d')
    draw_jov.create_text(jov_x0-Callisto.x*jov_radius,60,text='C', font=DjV_S_8, fill='#766b5d', justify='center')
    
    if not (Ganymede.z < 0 and jov_x0-1 < Ganymede.x < jov_x0+1):
        draw_jov.create_oval(jov_x0-Ganymede.x*jov_radius-Ga_r,jov_y0+Ganymede.y*jov_radius-Ga_r,\
                             jov_x0-Ganymede.x*jov_radius+Ga_r,jov_y0+Ganymede.y*jov_radius+Ga_r, width=0, fill='#544a45')
    draw_jov.create_text(jov_x0-Ganymede.x*jov_radius,60,text='G', font=DjV_S_8, fill='#544a45', justify='center')

    d0 = date(2018,6,1) # http://jupos.privat.t-online.de/index.htm 
    delta = date.today()-d0
    grs_lon = 289+delta.days/365.2425*12*2 # should oftenly update

    if math.degrees(Jupiter.cmlII)-90 < grs_lon < math.degrees(Jupiter.cmlII):
        text_jov = tk.Label(fm_side, text='GRS at east', font=DjV_S_8, bg='black', fg='#C88B3A', justify='center')
    elif grs_lon == math.degrees(Jupiter.cmlII):
        text_jov = tk.Label(fm_side, text='GRS transit', font=DjV_S_8, bg='black', fg='#C88B3A', justify='center')
    elif math.degrees(Jupiter.cmlII) < grs_lon < math.degrees(Jupiter.cmlII)+90:
        text_jov = tk.Label(fm_side, text='GRS at west', font=DjV_S_8, bg='black', fg='#C88B3A', justify='center')
    else:
        text_jov = tk.Label(fm_side, text='no GRS', font=DjV_S_8, bg='black', fg='#C88B3A', justify='center')
    text_jov.grid(row=6, column=1, columnspan=2, sticky='EW')

    text_planet_dir = tk.Label(fm_side, text='\u2190 E', font=DjV_S_10, bg='black', fg='red')
    text_planet_dir.grid(row=6, column=0, sticky='W')
    text_planet_dir = tk.Label(fm_side, text='W \u2192', font=DjV_S_10, bg='black', fg='red')
    text_planet_dir.grid(row=6, column=3, sticky='E')
    
    text_spacer4 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer4.grid(row=7, column=0, columnspan=4, sticky='EW')

def mercury_venus():
    Mercury.compute(hokoon)
    Venus.compute(hokoon)    

    mercury_chi_0 = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Mercury.ra),\
                                            math.sin(Sun.dec)*math.cos(Mercury.dec)-math.cos(Sun.dec)*math.sin(Mercury.dec)*math.cos(Sun.ra-Mercury.ra)))
    if mercury_chi_0<0:
        mercury_chi = mercury_chi_0+360
    else:
        mercury_chi = mercury_chi_0

    venus_chi_0 = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Venus.ra),\
                                          math.sin(Sun.dec)*math.cos(Venus.dec)-math.cos(Sun.dec)*math.sin(Venus.dec)*math.cos(Sun.ra-Venus.ra)))
    if venus_chi_0<0:
        venus_chi = venus_chi_0+360
    else:
        venus_chi = venus_chi_0
        
    print('drawing Mercury and Venus')
    prompt_text('drawing Mercury and Venus')
    fm_bottom.update()
    text_MV = tk.Label(fm_side, text='Mercury & Venus', font=DjV_S_12_, bg='black', fg='white')
    text_MV.grid(row=8, column=0, columnspan=4, sticky='EW')
    
    draw_MV = tk.Canvas(fm_side, width=180, height=50, bg='black')
    draw_MV.grid(row=9, column=0, columnspan=4)
    draw_MV.configure(borderwidth=0, highlightthickness=0)

    Mercury_offsetx = 30
    Venus_offsetx = 120
    MV_offsety = 10
    MV_d = 30
    rot_pa_limb_mercury = mercury_chi-90
    rot_pa_limb_venus = venus_chi-90
    
    if Mercury.phase == 0:
        draw_MV.create_oval(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, fill='black', width=0)
    elif 0 < Mercury.phase < 50:
        draw_MV.create_oval(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, fill='#97979F', width=0)
        draw_MV.create_arc(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, \
                           start=270+rot_pa_limb_mercury, extent=180, fill='black', outline='black', width=0)
        draw_MV.create_polygon(tuple(poly_oval(MV_d*(1-Mercury.phase/100)+Mercury_offsetx,0+MV_offsety,\
                                               MV_d*Mercury.phase/100+Mercury_offsetx,MV_d+MV_offsety, \
                                               rotation=rot_pa_limb_mercury)), fill='black', outline='black', width=0)
    elif Mercury.phase == 50:
        draw_MV.create_oval(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, fill='black', width=0)
        draw_MV.create_arc(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, \
                           start=90+rot_pa_limb_mercury, extent=180, fill='#97979F', outline='#97979F', width=0)
    elif 50 < Mercury.phase < 100:
        draw_MV.create_oval(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, fill='black', width=0)
        draw_MV.create_polygon(tuple(poly_oval(MV_d*(1-Mercury.phase/100)+Mercury_offsetx,0+MV_offsety,\
                                               MV_d*Mercury.phase/100+Mercury_offsetx,MV_d+MV_offsety, \
                                               rotation=rot_pa_limb_mercury)), fill='#97979F', outline='#97979F', width=0)
        draw_MV.create_arc(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, \
                           start=90+rot_pa_limb_mercury, extent=180, fill='#97979F', outline='#97979F', width=0)
    elif Mercury.phase == 100:
        draw_MV.create_oval(0+Mercury_offsetx,0+MV_offsety,MV_d+Mercury_offsetx,MV_d+MV_offsety, fill='#97979F', width=0)

    if Venus.phase == 0:
        draw_MV.create_oval(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, fill='black', width=0)
    elif 0 < Venus.phase < 50:
        draw_MV.create_oval(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, fill='#C18F17', width=0)
        draw_MV.create_arc(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, \
                           start=270+rot_pa_limb_venus, extent=180, fill='black', outline='black', width=0)
        draw_MV.create_polygon(tuple(poly_oval(MV_d*(1-Venus.phase/100)+Venus_offsetx,0+MV_offsety,\
                                               MV_d*Venus.phase/100+Venus_offsetx,MV_d+MV_offsety, \
                                               rotation=rot_pa_limb_venus)), fill='black', outline='black', width=0)
    elif Venus.phase == 50:
        draw_MV.create_oval(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, fill='black', width=0)
        draw_MV.create_arc(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, \
                           start=90+rot_pa_limb_venus, extent=180, fill='#C18F17', outline='#C18F17', width=0)
    elif 50 < Venus.phase < 100:
        draw_MV.create_oval(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, fill='black', width=0)
        draw_MV.create_polygon(tuple(poly_oval(MV_d*(1-Venus.phase/100)+Venus_offsetx,0+MV_offsety,\
                                               MV_d*Venus.phase/100+Venus_offsetx,MV_d+MV_offsety, \
                                               rotation=rot_pa_limb_venus)), fill='#C18F17', outline='#C18F17', width=0)
        draw_MV.create_arc(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, \
                           start=90+rot_pa_limb_venus, extent=180, fill='#C18F17', outline='#C18F17', width=0)
    elif Venus.phase == 100:
        draw_MV.create_oval(0+Venus_offsetx,0+MV_offsety,MV_d+Venus_offsetx,MV_d+MV_offsety, fill='#C18F17', width=0)

    dist_SM = math.degrees(math.acos(math.sin(Sun.dec)*math.sin(Mercury.dec)+math.cos(Sun.dec)*math.cos(Mercury.dec)*math.cos(Sun.ra-Mercury.ra)))
    draw_MV.create_text(MV_d/2+Mercury_offsetx,MV_d/2+MV_offsety,text=str(round(dist_SM,1))+u'\N{DEGREE SIGN}', font=DjV_S_8, fill='#FFCC33', justify='center')
    dist_SV = math.degrees(math.acos(math.sin(Sun.dec)*math.sin(Venus.dec)+math.cos(Sun.dec)*math.cos(Venus.dec)*math.cos(Sun.ra-Venus.ra)))
    draw_MV.create_text(MV_d/2+Venus_offsetx,MV_d/2+MV_offsety,text=str(round(dist_SV,1))+u'\N{DEGREE SIGN}', font=DjV_S_8, fill='#FFCC33', justify='center')

    text_planet_dir = tk.Label(fm_side, text='\u2190 E', font=DjV_S_10, bg='black', fg='red')
    text_planet_dir.grid(row=10, column=0, sticky='W')
    text_MV = tk.Label(fm_side, text=' dist. to Sun', font=DjV_S_8, bg='black', fg='#FFCC33', justify='center')
    text_MV.grid(row=10, column=1, columnspan=2, sticky='EW')
    text_planet_dir = tk.Label(fm_side, text='W \u2192', font=DjV_S_10, bg='black', fg='red')
    text_planet_dir.grid(row=10, column=3, sticky='E')

    text_spacer5 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer5.grid(row=11, column=0, columnspan=4, sticky='EW')

def cloud_detection():
    print('counting cloud')
    prompt_text('counting cloud')
    fm_bottom.update()
    
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
       
    # ASC
    try:
        urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
        asc = Image.open('asc.jpg')
    except ContentTooShortError: # try again
        print('try again')
        urlretrieve('http://www.hokoon.edu.hk/weather/images/astimages/hkneac_asc.jpg', 'asc.jpg')
        asc = Image.open('asc.jpg')        
    except HTTPError:
        asc = Image.open(pathlib.Path.cwd().joinpath('ASC','serverdead.jpg'))

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
        text_sky_con = tk.Label(fm_side, text='っω-) twilight', font=Arial_20B, bg='#9DA5BF', fg='white')
    elif 0 < math.degrees(Sun.alt) <= 15: # low angle
        if math.degrees(Sun.az) < 180:
            text_sky_con = tk.Label(fm_side, text='っω-) sunrise', font=Arial_20B, bg='#FFCC33', fg='white')
        else:
            text_sky_con = tk.Label(fm_side, text='-_-)ﾉｼ sunset', font=Arial_20B, bg='#FD5E53', fg='white')
    elif 15 < math.degrees(Sun.alt): # daytime
        if numpy.percentile(reduced_S_HSI_ASC,85) < 0.05:
            text_sky_con = tk.Label(fm_side, text='(TдT) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%', \
                                    font=Arial_20B, bg='#ADACA9', fg='white')
        else:
            if numpy.percentile(reduced_BR_ratio_ASC,85) <= 0.04:
                text_sky_con = tk.Label(fm_side, text='(ﾟｰﾟ) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%', \
                                        font=Arial_20B, bg='#A7A69D', fg='white')
            else:
                text_sky_con = tk.Label(fm_side, text='(・ω・) '+str(round(sum(i < 0.075 for i in reduced_S_HSI_ASC)*100/len(reduced_S_HSI_ASC)))+'%', \
                                        font=Arial_20B, bg='#002b66', fg='white')
    else: # nighttime
        if numpy.mean(reduced_S_HSI_ASC) < 0.05:
            text_sky_con = tk.Label(fm_side, text='(・ω・) '+str(round(sum(i < 0.1 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%', \
                                    font=Arial_20B, bg='#002b66', fg='white')
        elif 0.05 <= numpy.mean(reduced_S_HSI_ASC) <= 0.07:
            text_sky_con = tk.Label(fm_side, text='(ﾟｰﾟ) '+str(round(sum(i < 0.1 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%', \
                                    font=Arial_20B, bg='#A7A69D', fg='white') 
        else:
            text_sky_con = tk.Label(fm_side, text='(TдT) '+str(round(sum(i < 0.1 for i in reduced_BR_ratio_ASC)*100/len(reduced_BR_ratio_ASC)))+'%', \
                                    font=Arial_20B, bg='#ADACA9', fg='white') 
    text_sky_con.grid(row=12, column=0, columnspan=4, sticky='NESW')

    text_spacer6 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer6.grid(row=13, column=0, columnspan=4, sticky='EW')

def skynow():
    button_refresh_sky = tk.Button(fm_side, text='NOW', font=DjV_S_10, highlightbackground='black', command=refresh_sky)
    button_refresh_sky.grid(row=14, column=0, columnspan=4, sticky='EW')

    text_spacer7 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer7.grid(row=15, column=0, columnspan=4, sticky='EW')    

def ephemeris():
    hokoon.horizon = '0'
    
    text_astro_ephemeris = tk.Label(fm_side, text='Ephemeris', font=DjV_S_12_, justify="center", bg='black', fg='white')
    text_astro_ephemeris.grid(row=16, column=0, columnspan=4, sticky='EW')

    text_rise = tk.Label(fm_side, text='rise', font=DjV_S_10, bg='black', fg='white')
    text_rise.grid(row=17, column=1, sticky='EW')
    text_set = tk.Label(fm_side, text='set', font=DjV_S_10, bg='black', fg='white')
    text_set.grid(row=17, column=2, sticky='EW')
    text_set = tk.Label(fm_side, text='mag', font=DjV_S_10, bg='black', fg='white')
    text_set.grid(row=17, column=3, sticky='EW')
    
    # Moon        
    if moon_chi>180:
        text_Moon = tk.Label(fm_side, text='\u263D', font=DjV_S_10, bg='black', fg='#DAD9D7')
    else:
        text_Moon = tk.Label(fm_side, text='\u263E', font=DjV_S_10, bg='black', fg='#DAD9D7')
    text_Moon.grid(row=18, column=0)
    
    next_rise_moon = StringVar()
    next_rise_moon.set(ephem.localtime(hokoon.next_rising(ephem.Moon())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Moon()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_moon = tk.Label(fm_side, textvariable=str(next_rise_moon), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_moon = tk.Label(fm_side, textvariable=str(next_rise_moon), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_moon.grid(row=18, column=1, sticky='EW')

    next_set_moon = StringVar()
    next_set_moon.set(ephem.localtime(hokoon.next_setting(ephem.Moon())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Moon()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_moon = tk.Label(fm_side, textvariable=str(next_set_moon), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_moon = tk.Label(fm_side, textvariable=str(next_set_moon), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_moon.grid(row=18, column=2, sticky='EW')

    mag_moon = StringVar()
    mag_moon.set(round(Moon.mag,1))
    text_mag_moon = tk.Label(fm_side, textvariable=str(mag_moon), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_moon.grid(row=18, column=3, sticky='E')
    
    # Mercury
    text_Mercury = tk.Label(fm_side, text='\u263F', font=DjV_S_10, bg='black', fg='#97979F')
    text_Mercury.grid(row=19, column=0)
    
    next_rise_mercury = StringVar()
    next_rise_mercury.set(ephem.localtime(hokoon.next_rising(ephem.Mercury())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Mercury()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_mercury = tk.Label(fm_side, textvariable=str(next_rise_mercury), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_mercury = tk.Label(fm_side, textvariable=str(next_rise_mercury), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_mercury.grid(row=19, column=1, sticky='EW')

    next_set_mercury = StringVar()
    next_set_mercury.set(ephem.localtime(hokoon.next_setting(ephem.Mercury())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Mercury()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_mercury = tk.Label(fm_side, textvariable=str(next_set_mercury), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_mercury = tk.Label(fm_side, textvariable=str(next_set_mercury), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_mercury.grid(row=19, column=2, sticky='EW')

    mag_mercury = StringVar()
    mag_mercury.set(round(Mercury.mag,1))
    text_mag_mercury = tk.Label(fm_side, textvariable=str(mag_mercury), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_mercury.grid(row=19, column=3, sticky='E')
    
    # Venus
    text_Venus = tk.Label(fm_side, text='\u2640', font=DjV_S_10, bg='black', fg='#C18F17')
    text_Venus.grid(row=20, column=0)
    
    next_rise_venus = StringVar()
    next_rise_venus.set(ephem.localtime(hokoon.next_rising(ephem.Venus())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Venus()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_venus = tk.Label(fm_side, textvariable=str(next_rise_venus), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_venus = tk.Label(fm_side, textvariable=str(next_rise_venus), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_venus.grid(row=20, column=1, sticky='EW')

    next_set_venus = StringVar()
    next_set_venus.set(ephem.localtime(hokoon.next_setting(ephem.Venus())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Venus()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_venus = tk.Label(fm_side, textvariable=str(next_set_venus), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_venus = tk.Label(fm_side, textvariable=str(next_set_venus), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_venus.grid(row=20, column=2, sticky='EW')

    mag_venus = StringVar()
    mag_venus.set(round(Venus.mag,1))
    text_mag_venus = tk.Label(fm_side, textvariable=str(mag_venus), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_venus.grid(row=20, column=3, sticky='E')
    
    # Mars
    text_Mars = tk.Label(fm_side, text='\u2642', font=DjV_S_10, bg='black', fg='#E27B58')
    text_Mars.grid(row=21, column=0)
    
    next_rise_mars = StringVar()
    next_rise_mars.set(ephem.localtime(hokoon.next_rising(ephem.Mars())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Mars()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_mars = tk.Label(fm_side, textvariable=str(next_rise_mars), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_mars = tk.Label(fm_side, textvariable=str(next_rise_mars), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_mars.grid(row=21, column=1, sticky='EW')

    next_set_mars = StringVar()
    next_set_mars.set(ephem.localtime(hokoon.next_setting(ephem.Mars())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Mars()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_mars = tk.Label(fm_side, textvariable=str(next_set_mars), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_mars = tk.Label(fm_side, textvariable=str(next_set_mars), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_mars.grid(row=21, column=2, sticky='EW')

    mag_mars = StringVar()
    mag_mars.set(round(Mars.mag,1))
    text_mag_mars = tk.Label(fm_side, textvariable=str(mag_mars), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_mars.grid(row=21, column=3, sticky='E')
    
    # Jupiter
    text_Jupiter = tk.Label(fm_side, text='\u2643', font=DjV_S_10, bg='black', fg='#C88B3A')
    text_Jupiter.grid(row=22, column=0)
    
    next_rise_jupiter = StringVar()
    next_rise_jupiter.set(ephem.localtime(hokoon.next_rising(ephem.Jupiter())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Jupiter()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_jupiter = tk.Label(fm_side, textvariable=str(next_rise_jupiter), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_jupiter = tk.Label(fm_side, textvariable=str(next_rise_jupiter), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_jupiter.grid(row=22, column=1, sticky='EW')

    next_set_jupiter = StringVar()
    next_set_jupiter.set(ephem.localtime(hokoon.next_setting(ephem.Jupiter())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Jupiter()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_jupiter = tk.Label(fm_side, textvariable=str(next_set_jupiter), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_jupiter = tk.Label(fm_side, textvariable=str(next_set_jupiter), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_jupiter.grid(row=22, column=2, sticky='EW')

    mag_jupiter = StringVar()
    mag_jupiter.set(round(Jupiter.mag,1))
    text_mag_jupiter = tk.Label(fm_side, textvariable=str(mag_jupiter), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_jupiter.grid(row=22, column=3, sticky='E')
    
    # Saturn
    text_Saturn = tk.Label(fm_side, text='\u2644', font=DjV_S_10, bg='black', fg='#A49B72')
    text_Saturn.grid(row=23, column=0)
    
    next_rise_saturn = StringVar()
    next_rise_saturn.set(ephem.localtime(hokoon.next_rising(ephem.Saturn())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Saturn()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_saturn = tk.Label(fm_side, textvariable=str(next_rise_saturn), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_saturn = tk.Label(fm_side, textvariable=str(next_rise_saturn), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_saturn.grid(row=23, column=1, sticky='EW')

    next_set_saturn = StringVar()
    next_set_saturn.set(ephem.localtime(hokoon.next_setting(ephem.Saturn())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Saturn()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_saturn = tk.Label(fm_side, textvariable=str(next_set_saturn), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_saturn = tk.Label(fm_side, textvariable=str(next_set_saturn), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_saturn.grid(row=23, column=2, sticky='EW')

    mag_saturn = StringVar()
    mag_saturn.set(round(Saturn.mag,1))
    text_mag_saturn = tk.Label(fm_side, textvariable=str(mag_saturn), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_saturn.grid(row=23, column=3, sticky='E')
    
    # Uranus
    text_Uranus = tk.Label(fm_side, text='\u2645', font=DjV_S_10, bg='black', fg='#D5FBFC')
    text_Uranus.grid(row=24, column=0)
    
    next_rise_uranus = StringVar()
    next_rise_uranus.set(ephem.localtime(hokoon.next_rising(ephem.Uranus())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Uranus()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_uranus = tk.Label(fm_side, textvariable=str(next_rise_uranus), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_uranus = tk.Label(fm_side, textvariable=str(next_rise_uranus), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_uranus.grid(row=24, column=1, sticky='EW')

    next_set_uranus = StringVar()
    next_set_uranus.set(ephem.localtime(hokoon.next_setting(ephem.Uranus())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Uranus()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_uranus = tk.Label(fm_side, textvariable=str(next_set_uranus), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_uranus = tk.Label(fm_side, textvariable=str(next_set_uranus), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_uranus.grid(row=24, column=2, sticky='EW')

    mag_uranus = StringVar()
    mag_uranus.set(round(Uranus.mag,1))
    text_mag_uranus = tk.Label(fm_side, textvariable=str(mag_uranus), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_uranus.grid(row=24, column=3, sticky='E')
    
    # Neptune
    text_Neptune = tk.Label(fm_side, text='\u2646', font=DjV_S_10, bg='black', fg='#3E66F9')
    text_Neptune.grid(row=25, column=0)
    
    next_rise_neptune = StringVar()
    next_rise_neptune.set(ephem.localtime(hokoon.next_rising(ephem.Neptune())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Neptune()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_neptune = tk.Label(fm_side, textvariable=str(next_rise_neptune), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_neptune = tk.Label(fm_side, textvariable=str(next_rise_neptune), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_neptune.grid(row=25, column=1, sticky='EW')

    next_set_neptune = StringVar()
    next_set_neptune.set(ephem.localtime(hokoon.next_setting(ephem.Neptune())).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Neptune()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_neptune = tk.Label(fm_side, textvariable=str(next_set_neptune), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_neptune = tk.Label(fm_side, textvariable=str(next_set_neptune), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_neptune.grid(row=25, column=2, sticky='EW')

    mag_neptune = StringVar()
    mag_neptune.set(round(Neptune.mag,1))
    text_mag_neptune = tk.Label(fm_side, textvariable=str(mag_neptune), font=DjV_S_10, bg='black', fg='yellow')
    text_mag_neptune.grid(row=25, column=3, sticky='E')
    
    text_spacer8 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer8.grid(row=26, column=0, columnspan=4, sticky='EW')

    ###################################################################################################################################################
    
    # astronomical twilight
    hokoon.horizon = '-18'
    
    text_astro_twilight = tk.Label(fm_side, text='Astronomical Twilight', font=DjV_S_12_, justify="center", bg='black', fg='white')
    text_astro_twilight.grid(row=27, column=0, columnspan=4, sticky='EW')
    
    text_Sun = tk.Label(fm_side, text='\u263C', font=DjV_S_10, bg='black', fg='#FFCC33')
    text_Sun.grid(row=28, column=0)

    next_rise_sun = StringVar()
    next_rise_sun.set(ephem.localtime(hokoon.next_rising(ephem.Sun(), use_center=True)).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_rising(ephem.Sun()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_rise_sun = tk.Label(fm_side, textvariable=str(next_rise_sun), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_rise_sun = tk.Label(fm_side, textvariable=str(next_rise_sun), font=DjV_S_10, bg='black', fg='orange')
    text_next_rise_sun.grid(row=28, column=1, sticky='EW')

    next_set_sun = StringVar()
    next_set_sun.set(ephem.localtime(hokoon.next_setting(ephem.Sun(), use_center=True)).strftime('%X'))
    if datetime.date(ephem.localtime(hokoon.next_setting(ephem.Sun()))) > datetime.date(ephem.localtime(hokoon.date)):
        text_next_set_sun = tk.Label(fm_side, textvariable=str(next_set_sun), font=DjV_S_10, bg='black', fg='green')
    else:
        text_next_set_sun = tk.Label(fm_side, textvariable=str(next_set_sun), font=DjV_S_10, bg='black', fg='orange')
    text_next_set_sun.grid(row=28, column=2, sticky='EW')

    text_spacer4 = tk.Label(fm_side, text='', font=DjV_S_1, bg='black', fg='white')
    text_spacer4.grid(row=29, column=0, columnspan=4, sticky='EW')
    text_today = tk.Label(fm_side, text='   orange: today', font=DjV_S_8, bg='black', fg='orange')
    text_today.grid(row=30, column=0, columnspan=4, sticky='W')
    text_tomorrow = tk.Label(fm_side, text='green: +1day   ', font=DjV_S_8, bg='black', fg='green')
    text_tomorrow.grid(row=30, column=0, columnspan=4, sticky='E')
    
def fine_adjustment():
    # RA
    text_RA = tk.Label(fm_side, text='zenith RA shift', font=DjV_S_10, bg='black', fg='white')
    text_RA.grid(row=0, column=0, columnspan=3, sticky='EW')

    button_RA_minus = tk.Button(fm_side, text='\u2190', font=DjV_S_10, highlightbackground='black', command=RA_minus)
    button_RA_minus.grid(row=1, column=0, sticky='EW')

    text_RA_value = tk.Label(fm_side, textvariable=str(zenith_shift_ra), font=DjV_S_10, bg='black', fg='white')
    text_RA_value.grid(row=1, column=1)

    button_RA_plus = tk.Button(fm_side, text='\u2192', font=DjV_S_10, highlightbackground='black', command=RA_plus)
    button_RA_plus.grid(row=1, column=2, sticky='EW')

    # Dec
    text_Dec = tk.Label(fm_side, text='zenith Dec shift', font=DjV_S_10, bg='black', fg='white')
    text_Dec.grid(row=2, column=0, columnspan=3, sticky='EW')

    button_Dec_minus = tk.Button(fm_side, text='\u2191', font=DjV_S_10, highlightbackground='black', command=Dec_minus)
    button_Dec_minus.grid(row=3, column=0, sticky='EW')

    text_Dec_value = tk.Label(fm_side, textvariable=str(zenith_shift_dec), font=DjV_S_10, bg='black', fg='white')
    text_Dec_value.grid(row=3, column=1)

    button_Dec_plus = tk.Button(fm_side, text='\u2193', font=DjV_S_10, highlightbackground='black', command=Dec_plus)
    button_Dec_plus.grid(row=3, column=2, sticky='EW')

    # rotate
    text_rotate = tk.Label(fm_side, text='rotation', font=DjV_S_10, bg='black', fg='white')
    text_rotate.grid(row=4, column=0, columnspan=3, sticky='EW')

    button_rotate_minus = tk.Button(fm_side, text='\u21BB', font=DjV_S_10, highlightbackground='black', command=rotate_minus)
    button_rotate_minus.grid(row=5, column=0, sticky='EW')

    text_rotate_value = tk.Label(fm_side, textvariable=str(rotate_angle), font=DjV_S_10, bg='black', fg='white')
    text_rotate_value.grid(row=5, column=1)

    button_rotate_plus = tk.Button(fm_side, text='\u21BA', font=DjV_S_10, highlightbackground='black', command=rotate_plus)
    button_rotate_plus.grid(row=5, column=2, sticky='EW')

    # aspect ratio
    text_rotate = tk.Label(fm_side, text='aspect ratio', font=DjV_S_10, bg='black', fg='white')
    text_rotate.grid(row=6, column=0, columnspan=3, sticky='EW')

    button_aspect_minus = tk.Button(fm_side, text='\u2194', font=DjV_S_10, highlightbackground='black', command=aspect_minus)
    button_aspect_minus.grid(row=7, column=0, sticky='EW')

    text_rotate_value = tk.Label(fm_side, textvariable=str(aspect_ratio), font=DjV_S_10, bg='black', fg='white')
    text_rotate_value.grid(row=7, column=1)

    button_aspect_plus = tk.Button(fm_side, text='\u2195', font=DjV_S_10, highlightbackground='black', command=aspect_plus)
    button_aspect_plus.grid(row=7, column=2, sticky='EW')

    # scale
    text_scale = tk.Label(fm_side, text='scale', font=DjV_S_10, bg='black', fg='white')
    text_scale.grid(row=8, column=0, columnspan=3, sticky='EW')

    button_scale_minus = tk.Button(fm_side, text='-', font=DjV_S_10, highlightbackground='black', command=scale_minus)
    button_scale_minus.grid(row=9, column=0, sticky='EW')

    text_scale_value = tk.Label(fm_side, textvariable=str(plot_scale), font=DjV_S_10, bg='black', fg='white')
    text_scale_value.grid(row=9, column=1)

    button_scale_plus = tk.Button(fm_side, text='+', font=DjV_S_10, highlightbackground='black', command=scale_plus)
    button_scale_plus.grid(row=9, column=2, sticky='EW')

    #x shift
    text_x_shift = tk.Label(fm_side, text='x-shift', font=DjV_S_10, bg='black', fg='white')
    text_x_shift.grid(row=10, column=0, columnspan=3, sticky='EW')

    button_x_shift_minus = tk.Button(fm_side, text='\u2190', font=DjV_S_10, highlightbackground='black', command=x_shift_minus)
    button_x_shift_minus.grid(row=11, column=0, sticky='EW')

    text_x_shift_value = tk.Label(fm_side, textvariable=str(x_shift), font=DjV_S_10, bg='black', fg='white')
    text_x_shift_value.grid(row=11, column=1)

    button_x_shift_plus = tk.Button(fm_side, text='\u2192', font=DjV_S_10, highlightbackground='black', command=x_shift_plus)
    button_x_shift_plus.grid(row=11, column=2, sticky='EW')

    # y shift
    text_y_shift = tk.Label(fm_side, text='y-shift', font=DjV_S_10, bg='black', fg='white')
    text_y_shift.grid(row=12, column=0, columnspan=3, sticky='EW')

    button_y_shift_minus = tk.Button(fm_side, text='\u2193', font=DjV_S_10, highlightbackground='black', command=y_shift_minus)
    button_y_shift_minus.grid(row=13, column=0, sticky='EW')

    text_y_shift_value = tk.Label(fm_side, textvariable=str(y_shift), font=DjV_S_10, bg='black', fg='white')
    text_y_shift_value.grid(row=13, column=1)

    button_y_shift_plus = tk.Button(fm_side, text='\u2191', font=DjV_S_10, highlightbackground='black', command=y_shift_plus)
    button_y_shift_plus.grid(row=13, column=2, sticky='EW')

    text_spacer1 = tk.Label(fm_side, text='', font=('Helvetica', 1), bg='black', fg='white')
    text_spacer1.grid(row=14, column=0, columnspan=3, sticky='EW')

    # save parameters
    save_parameters = tk.Button(fm_side, textvariable=str(save_para), font=DjV_S_10, highlightbackground='black', command=set_para, width=18)
    save_parameters.grid(row=15, column=0, columnspan=3, sticky='EW')

    text_spacer1 = tk.Label(fm_side, text='', font=('Helvetica', 1), bg='black', fg='white')
    text_spacer1.grid(row=16, column=0, columnspan=3, sticky='EW')

    # restore default
    default_button = tk.Button(fm_side, text='restore default', font=DjV_S_10, highlightbackground='black', command=restore_default, width=18)
    default_button.grid(row=17, column=0, columnspan=3, sticky='EW')
    
    text_spacer2 = tk.Label(fm_side, text='', height='2', bg='black', fg='white')
    text_spacer2.grid(row=18, column=0, columnspan=3, sticky='EW')
    
def calibration_images():
    text_calibration = tk.Label(fm_side, text='calibration', font=DjV_S_10, bg='black', fg='white')
    text_calibration.grid(row=19, column=0, columnspan=3, sticky='EW')

    button_moonglow = tk.Button(fm_side, text='Moonglow', font=DjV_S_10, highlightbackground='black', command=moonglow)
    button_moonglow.grid(row=20, column=0, columnspan=3, sticky='EW')

    button_sky_20170215_2131 = tk.Button(fm_side, text='20170215a', font=DjV_S_10, highlightbackground='black', command=sky_20170215_2131)
    button_sky_20170215_2131.grid(row=21, column=0, columnspan=3, sticky='EW')

    button_sky_20170215_2302 = tk.Button(fm_side, text='20170215b', font=DjV_S_10, highlightbackground='black', command=sky_20170215_2302)
    button_sky_20170215_2302.grid(row=22, column=0, columnspan=3, sticky='EW')

    button_sky_20170218_2000 = tk.Button(fm_side, text='20170218', font=DjV_S_10, highlightbackground='black', command=sky_20170218_2000)
    button_sky_20170218_2000.grid(row=23, column=0, columnspan=3, sticky='EW')

    button_sky_20170302_1939 = tk.Button(fm_side, text='20170302', font=DjV_S_10, highlightbackground='black', command=sky_20170302_1939)
    button_sky_20170302_1939.grid(row=24, column=0, columnspan=3, sticky='EW')

    button_sky_20170325_0142 = tk.Button(fm_side, text='20170325', font=DjV_S_10, highlightbackground='black', command=sky_20170325_0142)
    button_sky_20170325_0142.grid(row=25, column=0, columnspan=3, sticky='EW')

    button_sky_20170327_2331 = tk.Button(fm_side, text='20170327', font=DjV_S_10, highlightbackground='black', command=sky_20170327_2331)
    button_sky_20170327_2331.grid(row=26, column=0, columnspan=3, sticky='EW')

    button_sky_20170402_2204 = tk.Button(fm_side, text='20170402', font=DjV_S_10, highlightbackground='black', command=sky_20170402_2204)
    button_sky_20170402_2204.grid(row=27, column=0, columnspan=3, sticky='EW')

    button_sky_20170726_2000 = tk.Button(fm_side, text='20170726', font=DjV_S_10, highlightbackground='black', command=sky_20170726_2000)
    button_sky_20170726_2000.grid(row=28, column=0, columnspan=3, sticky='EW')

    button_sky_20170922_0500 = tk.Button(fm_side, text='20170922', font=DjV_S_10, highlightbackground='black', command=sky_20170922_0500)
    button_sky_20170922_0500.grid(row=29, column=0, columnspan=3, sticky='EW')

def reset_label():
    global ax_label

    try:
        ax_label.remove()
    except:
        print('no labels to remove')
    ax_label = ax0.twiny()
    ax_label.set_position(ax0.get_position())
    ax_label.set_facecolor(ax0.get_facecolor())
    ax_label.set_aspect(ax0.get_aspect())
    ax_label.set_xlim(ax0.get_xlim())
    ax_label.set_ylim(ax0.get_ylim())

    # info
    if button_mode.get() == 1:
        ax_label.annotate('E '+str(hokoon.lon),(hori_xmin,hori_ymin),color='w')
        ax_label.annotate('N '+str(hokoon.lat),(hori_xmin,hori_ymin+15),color='w')
        ax_label.annotate('sky at HKT '+str(ephem.localtime(hokoon.date).strftime('%x %X')),(hori_xmax,hori_ymin),ha='right',color='w')
    
    elif button_mode.get() == 2:
        ax_label.annotate('E',(math.cos(math.radians(rotate_angle.get()))*(x_shift.get()-hori_border/2-labelxy)-math.sin(math.radians(rotate_angle.get()))*y_shift.get(),\
                               math.sin(math.radians(rotate_angle.get()))*(x_shift.get()-hori_border/2-labelxy)+math.cos(math.radians(rotate_angle.get()))*y_shift.get()),\
                          color='w',fontsize=16,horizontalalignment='right',verticalalignment='center')
        ax_label.annotate('W',(math.cos(math.radians(rotate_angle.get()))*(x_shift.get()+hori_border/2+labelxy)-math.sin(math.radians(rotate_angle.get()))*y_shift.get(),\
                               math.sin(math.radians(rotate_angle.get()))*(x_shift.get()+hori_border/2+labelxy)+math.cos(math.radians(rotate_angle.get()))*y_shift.get()),\
                          color='w',fontsize=16,horizontalalignment='left',verticalalignment='center')

def wipe_constellations():
    try:
        lc_west.remove()
        lc_west_z.remove()
        lc_west_dotted.remove()
    except:
        print('no western constellations')
    try:
        lc_C_A.remove()
        lc_C_B.remove()
        lc_C_C.remove()
        lc_C_D.remove()
        lc_C_D_z.remove()
        lc_C_E.remove()
        lc_C_E_z.remove()
        lc_C_F.remove()
        lc_C_F_z.remove()
        lc_C_G.remove()
        lc_C_G_z.remove()
        lc_C_H.remove()
    except:
        print('no chinese constellations')
    try:
        lc_J_A.remove()
        lc_J_B.remove()
        lc_J_C.remove()
        lc_J_D.remove()
        lc_J_D_z.remove()
        lc_J_E.remove()
        lc_J_E_z.remove()
        lc_J_F.remove()
        lc_J_F_z.remove()
        lc_J_G.remove()
        lc_J_G_z.remove()
        lc_J_H.remove()
    except:
        print('no japanese constellations')  

def constellation_west():
    sky_culture.set(0)
    reset_label()
    wipe_constellations()
    manystars.remove()
    star_on.set(1)
    plot_stars()
    plot_constellation()
    plot_MW() # ax_label, put into a single artist in future
    solar_label()
    plt.gcf().canvas.draw()
    print('done')
    prompt_text('done')
    fm_bottom.update()
    
def constellation_chi():
    sky_culture.set(1)
    reset_label()
    wipe_constellations()
    manystars.remove()
    star_on.set(1)
    plot_stars()
    plot_constellation()
    plot_MW() # ax_label, put into a single artist in future
    solar_label()
    plt.gcf().canvas.draw()
    print('done')
    prompt_text('done')
    fm_bottom.update()
    
def constellation_jap():
    sky_culture.set(2)
    reset_label()
    wipe_constellations()
    manystars.remove()
    star_on.set(1)
    plot_stars()
    plot_constellation()
    plot_MW() # ax_label, put into a single artist in future
    solar_label()
    plt.gcf().canvas.draw()
    print('done')
    prompt_text('done')
    fm_bottom.update()

def constellation_radio():
    sky_culture.set(3)
    reset_label()
    wipe_constellations()
    manystars.remove()
    star_on.set(2)
    plot_stars()
    plot_MW() # ax_label, put into a single artist in future
    solar_label()
    plt.gcf().canvas.draw()
    print('done')
    prompt_text('done')
    fm_bottom.update()

def constellation_gamma():
    sky_culture.set(4)
    reset_label()
    wipe_constellations()
    manystars.remove()
    star_on.set(3)
    plot_stars()
    plot_MW() # ax_label, put into a single artist in future
    solar_label()
    plt.gcf().canvas.draw()
    print('done')
    prompt_text('done')
    fm_bottom.update()
    
def sky_cul_select():
    text_skycul = tk.Label(fm_side, text='Sky Culture', font=DjV_S_12_, bg='black', fg='white')
    text_skycul.grid(row=12, column=0, columnspan=4, sticky='EW')

    button_skycul_west = tk.Radiobutton(fm_side, text='Western', font=DjV_S_10, bg='black',fg='white', highlightbackground='black', \
                                        var=sky_culture, value=0, command=constellation_west)
    button_skycul_west.grid(row=13, column=0, columnspan=4, sticky='W')
    
    button_skycul_chi = tk.Radiobutton(fm_side, text='Chinese', font=DjV_S_10, bg='black',fg='white', highlightbackground='black', \
                                        var=sky_culture, value=1, command=constellation_chi)
    button_skycul_chi.grid(row=14, column=0, columnspan=4, sticky='W')
    
    button_skycul_jap = tk.Radiobutton(fm_side, text='Japanese', font=DjV_S_10, bg='black',fg='white', highlightbackground='black', \
                                        var=sky_culture, value=2, command=constellation_jap)
    button_skycul_jap.grid(row=15, column=0, columnspan=4, sticky='W')

    button_skycul_radio = tk.Radiobutton(fm_side, text='Radio', font=DjV_S_10, bg='black',fg='white', highlightbackground='black', \
                                        var=sky_culture, value=3, command=constellation_radio)
    button_skycul_radio.grid(row=16, column=0, columnspan=4, sticky='W')

    button_skycul_gamma = tk.Radiobutton(fm_side, text='3FGL', font=DjV_S_10, bg='black',fg='white', highlightbackground='black', \
                                        var=sky_culture, value=4, command=constellation_gamma)
    button_skycul_gamma.grid(row=17, column=0, columnspan=4, sticky='W')
    
def side_button():
    global moon_chi
    Sun.compute(hokoon)
    Moon.compute(hokoon)
    Mercury.compute(hokoon)
    Venus.compute(hokoon)
    Mars.compute(hokoon)
    Jupiter.compute(hokoon)
    Saturn.compute(hokoon)  
    Uranus.compute(hokoon)
    Neptune.compute(hokoon)
    
    if button_mode.get() == 1:
        moon_phase()
        jovian_moons()
        mercury_venus()
        cloud_detection()

        skynow()
        
        ephemeris()

        #########################

    elif button_mode.get() == 0:
        fine_adjustment()
        calibration_images()
        
        #########################

    elif button_mode.get() == 2:
        sky_cul_select()

#######
# GUI #
#######
# setup side frame
fm_side_height = 800
fm_side_width = 200

def fm_side_monitor():
    global fm_side
    fm_side = tk.Frame(root)
    fm_side.config(bg='black', height=fm_side_height, width=fm_side_width, padx=5)
    fm_side.grid_propagate(0)
    fm_side.grid(row=0, column=0, rowspan=4, sticky='NS')
    fm_side.grid_rowconfigure(index=12, weight=1)

def fm_side_config():
    global fm_side
    fm_side = tk.Frame(root)
    fm_side.config(bg='black', height=fm_side_height, width=fm_side_width, padx=20)
    fm_side.grid_propagate(0)
    fm_side.grid(row=0, column=0, rowspan=4)    

def fm_side_starmap():
    global fm_side
    fm_side = tk.Frame(root)
    fm_side.config(bg='black', height=fm_side_height, width=fm_side_width, padx=5)
    fm_side.grid_propagate(0)
    fm_side.grid(row=0, column=0, rowspan=4)

fm_side_monitor()
fm_prompt = tk.Frame(root)
fm_prompt.config(bg='black')
fm_bottom = tk.Frame(root)
fm_bottom.config(bg='black')

# initial monitor mode
button_mode = tk.IntVar()
button_mode.set(1)

def config_mode():
    global button_mode, fm_side
    button_mode.set(0)
    fm_side.grid_forget()
    fm_side_config()
    side_button()
    
def monitor_mode():
    global button_mode, fm_side
    button_mode.set(1)
    star_on.set(0)
    sky_culture.set(0)
    fm_side.grid_forget()
    fm_side_monitor()
    refresh_sky()

def starmap_mode():
    global button_mode, fm_side
    button_mode.set(2)
    star_on.set(1)
    sky_culture.set(0)
    fm_side.grid_forget()
    fm_side_starmap()
    refresh_sky()
    
choose_mode_config = tk.Radiobutton(fm_bottom, text='Configuration', bg='black',fg='white', var=button_mode, value=0, command=config_mode)
choose_mode_config.grid(row=1, column=0, sticky='E')

choose_mode_monitor = tk.Radiobutton(fm_bottom, text='Monitor mode', bg='black',fg='white', var=button_mode, value=1, command=monitor_mode)
choose_mode_monitor.grid(row=1, column=1)

choose_mode_starmap = tk.Radiobutton(fm_bottom, text='Starmap mode', bg='black',fg='white', var=button_mode, value=2, command=starmap_mode)
choose_mode_starmap.grid(row=1, column=2, sticky='W')

button = tk.Button(fm_bottom, text='Quit', font=DjV_S_10, highlightbackground='black', command=_quit)
button.grid(row=2, column=0, columnspan=3)

# setup other frames
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1)
canvas.get_tk_widget().config(width=720*image_size, height=480*image_size)

toolbarFrame = tk.Frame(master=root)
toolbarFrame.grid(row=1, column=1, sticky='EW')
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
toolbar.config(bg='black')
toolbar._message_label.config(bg='black', fg='white')
toolbar.update()
    
fm_prompt.grid(row=2, column=1, sticky='EW')
fm_bottom.grid(row=3, column=1)

refresh_sky()

end = time.time()
print('took '+str(round((end-start),2))+'s to start')

root.mainloop()

