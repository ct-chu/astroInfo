#mprof run ASC_mpl.py
#mprof plot

import time

import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
from matplotlib import collections as mc
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
#Obs.date = datetime.utcnow().replace(second=0,microsecond=0)
Obs.date = '2020/02/23 21:42:01' #UTC
#####################################
# plot parameters
image_size = 1.6
fig = plt.figure(figsize=(image_size*3,image_size*3), facecolor='black')
fig.subplots_adjust(0,0,1,1,0,0)

ax1 = plt.subplot()
ax1.set_facecolor('black')
ax1.set_aspect('equal', anchor='NE')

matplotlib.rcParams['savefig.facecolor'] = (0,0,0)

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
    DjV_S_6     = font_manager.FontProperties(fname = '/usr/local/share/fonts/DejaVuSans.ttf', size=6)
    DjV_S_8     = font_manager.FontProperties(fname = '/usr/local/share/fonts/DejaVuSans.ttf', size=8)
    DjV_S_9     = font_manager.FontProperties(fname = '/usr/local/share/fonts/DejaVuSans.ttf', size=9)
    DjV_S_10    = font_manager.FontProperties(fname = '/usr/local/share/fonts/DejaVuSans.ttf', size=10)
    DjV_S_12    = font_manager.FontProperties(fname = '/usr/local/share/fonts/DejaVuSans.ttf', size=12)
    emoji_20    = font_manager.FontProperties(fname = '/usr/local/share/fonts/YuGothB.ttc', size=20)

# log
def timelog(log):
    print(str(datetime.now().time().replace(microsecond=0))+'> '+log)
    
# LROC WAC basemap Shapefile
Mare    = numpy.zeros(shape=(267482,5)) 
Mare    = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_mare.csv'))
Crater  = numpy.zeros(shape=(182111,5))
Crater  = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','moon_crater.csv'))
    
####################
# define functions #
####################

def plot_solar():
    global plot_alpha, Sun, Moon, solar_obj, solar_color, moon_chi

    Sun         = ephem.Sun()
    Sun.compute(Obs)
    Moon        = ephem.Moon()
    Moon.compute(Obs)
    
    # position angle of the Moon's bright limb from North point of the disc of the Moon to East
    moon_chi_0 = math.degrees(math.atan2(math.cos(Sun.dec)*math.sin(Sun.ra-Moon.ra),\
                                     math.sin(Sun.dec)*math.cos(Moon.dec)-math.cos(Sun.dec)*math.sin(Moon.dec)*math.cos(Sun.ra-Moon.ra)))
    if moon_chi_0 < 0:
        moon_chi = moon_chi_0+360
    else:
        moon_chi = moon_chi_0

    # alpha
    if math.degrees(Sun.alt) >= 0:
        plot_alpha = 0.2
    else:
        plot_alpha = 0.1
    
    timelog('plotting solar system objects')
           
    solar_color = ['#FFCC33','#DAD9D7']
   
def moon_phase(): #ax1
    global moon_chi
    Moon.compute(Obs)

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

    # zenith up
    zenithup = 0
    if zenithup == 1:
        MP = Moon.parallactic_angle()
    elif zenithup == 0:
        MP = PA_axis_moon_N #selenographic north up
    elif zenithup == -1:
        MP = 0 #equatorial north up

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
        moondisc2 = patches.Wedge((0,0), M_d/2, 270+rot_pa_limb_moon-math.degrees(MP), 90+rot_pa_limb_moon-math.degrees(MP), color='#94908D')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon.phase/50), M_d, angle=rot_pa_limb_moon-math.degrees(MP), color='#94908D')
    elif Moon.phase == 50:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(MP), 270+rot_pa_limb_moon-math.degrees(MP), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#F0F0F0') #dummy
    elif 50 < Moon.phase < 100:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(MP), 270+rot_pa_limb_moon-math.degrees(MP), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon.phase/50), M_d, angle=rot_pa_limb_moon-math.degrees(MP), color='#F0F0F0')
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
        ax1.annotate('N',(ph_l*math.sin(MP),ph_l*math.cos(MP)),\
                     xycoords=('data'),rotation=-math.degrees(MP),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(MP),ph_R*math.sin(MP)],\
                 [ph_r*math.cos(MP),ph_R*math.cos(MP)],color='red')
        
        ax1.annotate('E',(ph_l*math.sin(MP+3*math.pi/2),ph_l*math.cos(MP+3*math.pi/2)),\
                     xycoords=('data'),rotation=-math.degrees(MP),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(MP+3*math.pi/2),ph_R*math.sin(MP+3*math.pi/2)],\
                 [ph_r*math.cos(MP+3*math.pi/2),ph_R*math.cos(MP+3*math.pi/2)],color='red')
        
        ax1.annotate('S',(ph_l*math.sin(MP+math.pi),ph_l*math.cos(MP+math.pi)),\
                     xycoords=('data'),rotation=-math.degrees(MP),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(MP+math.pi),ph_R*math.sin(MP+math.pi)],\
                 [ph_r*math.cos(MP+math.pi),ph_R*math.cos(MP+math.pi)],color='red')
        
        ax1.annotate('W',(ph_l*math.sin(MP+math.pi/2),ph_l*math.cos(MP+math.pi/2)),\
                     xycoords=('data'),rotation=-math.degrees(MP),ha='center',va='center',color='red')
        ax1.plot([ph_r*math.sin(MP+math.pi/2),ph_R*math.sin(MP+math.pi/2)],\
                 [ph_r*math.cos(MP+math.pi/2),ph_R*math.cos(MP+math.pi/2)],color='red')

    ax1.annotate('eq \ncoord.',(-90,-70),xycoords=('data'),ha='left',va='bottom',fontproperties=DjV_S_9,color='red')

    # selenographic
    ax1.annotate('seleno-\ngraphic',(90,-70),xycoords=('data'),ha='right',va='bottom',fontproperties=DjV_S_9,color='cyan')

    PA_axis_moon_z  = MP-PA_axis_moon_N # clockwise
    
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

    #if math.sin(math.radians(lat0))*math.sin(math.radians(y))+math.cos(math.radians(lat0))*math.cos(math.radians(y))*math.cos(math.radians(x-lon0)) >= 0:

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

plot_solar()
moon_phase()

# plot
fig.canvas.draw() 
fig.canvas.flush_events()
plt.savefig('moon.eps')

plt.show()

