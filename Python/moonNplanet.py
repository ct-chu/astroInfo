import time
from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, ContentTooShortError
import socket
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('TkAgg')
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
image_size = 1.6

fig = plt.figure(figsize=(image_size*3,image_size*10.5), facecolor='black')
fig.subplots_adjust(0,0,1,1,0,0)

gs = matplotlib.gridspec.GridSpec(5, 1, wspace=0, hspace=0, width_ratios=[1], height_ratios=[4,2,2,6,0.3])

ax1 = plt.subplot(gs[0, 0])
ax1.set_facecolor('black')
ax1.set_aspect('equal', anchor='N')
ax1.axis('off')

ax2 = plt.subplot(gs[1, 0])
ax2.set_facecolor('black')
ax2.set_aspect('equal', anchor='N')
ax2.axis('off')

ax3 = plt.subplot(gs[2, 0])
ax3.set_facecolor('black')
ax3.set_aspect('equal', anchor='N')
ax3.axis('off')

ax4 = plt.subplot(gs[3, 0])
ax4.set_facecolor('black')
ax4.set_aspect('equal', anchor='N')
ax4.axis('off')

ax5 = plt.subplot(gs[4, 0])
ax5.set_facecolor('black')
ax5.set_aspect('equal', anchor='N')
ax5.axis('off')
    
matplotlib.rcParams['savefig.facecolor'] = (0,0,0)

plot_scale          = 150

Sans_6     = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=9)
Sans_8     = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=10.5)
Sans_B_8   = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Black.otf', size=10.5)
Sans_9     = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=12)
Sans_10    = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=12)
Sans_11    = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=15)
Sans_B_11  = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Black.otf', size=15)
Sans_12    = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Regular.otf', size=16)
Sans_title = font_manager.FontProperties(fname = 'fonts/NotoSansHK-Black.otf', size=16)
icon_11    = font_manager.FontProperties(fname = 'fonts/DejaVuSans.ttf', size=15)
emoji_20   = font_manager.FontProperties(fname = 'fonts/YuGothB.ttc', size=16)

# raw data
horizon     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
twlight     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
equator     = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
ecliptic    = pandas.DataFrame(0,index=range(360),columns=['RA','Dec','x','y']).apply(pandas.to_numeric)

# log
def timelog(log):
    print(str(datetime.now().time().replace(microsecond=0))+'> '+log)

def solSysData():
    global moon_vector, moon_chi, sun_vector, sidereal_time, mercury_vector, venus_vector, jupiter_vector, saturn_vector, uranus_vector, neptune_vector, pluto_vector

    sidereal_time = date_UTC.gmst+OBS[2]/15
    sun_vector      = OBS[0].at(date_UTC).observe(sun).apparent()
    moon_vector     = OBS[0].at(date_UTC).observe(moon).apparent()
    mercury_vector  = OBS[0].at(date_UTC).observe(mercury).apparent()
    venus_vector    = OBS[0].at(date_UTC).observe(venus).apparent()
    jupiter_vector  = OBS[0].at(date_UTC).observe(jupiter).apparent()
    saturn_vector   = OBS[0].at(date_UTC).observe(saturn).apparent()
    uranus_vector   = OBS[0].at(date_UTC).observe(uranus).apparent()
    neptune_vector  = OBS[0].at(date_UTC).observe(neptune).apparent()
    pluto_vector    = OBS[0].at(date_UTC).observe(pluto).apparent()
    
    # position angle of the Moon's bright limb from North point of the disc of the Moon to East
    moon_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-moon_vector.radec()[0].radians),\
                                       math.sin(sun_vector.radec()[1].radians)*math.cos(moon_vector.radec()[1].radians)-\
                                       math.cos(sun_vector.radec()[1].radians)*math.sin(moon_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-moon_vector.radec()[0].radians)))
   
    if moon_chi < 0:
        moon_chi = moon_chi+360


def moon_phase(): #ax1
    Tmp0 = time.time()
    global ax1_moon

    timelog('drawing Moon')
    
    ax1.set_xlim((-90,90))
    ax1.set_ylim((-85,95))
    ax1.axis('off')
    ax1.add_patch(patches.Rectangle((-90,-85),180,180,fc='none',ec=(1,1,0,0.75),lw=2))
    
    # Moon phase
    ax1.annotate('月相 Moon Phase',(0,90),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')

    moon_size = math.degrees(3474.2/moon_vector.radec()[2].km)*3600

    M_d  = moon_size/2100*110
    ph_r = 50*moon_size/2100 # line inner radius
    ph_R = 60*moon_size/2100 # line outer radius
    ph_l = 68*moon_size/2100 # text radius
    
    # illuminated percentage
    Moon_percent = almanac.fraction_illuminated(ephem, 'moon', date_UTC)
    
    # rotate for position angle of the Moon's bright limb
    rot_pa_limb_moon = moon_chi-90

    # rotation angle from zenith to equatorial north clockwise
    Moon_parallactic_angle = math.atan2(math.sin(math.radians(sidereal_time*15)-moon_vector.radec()[0].radians),
                                        math.tan(OBS[1])*math.cos(moon_vector.radec()[1].radians)-math.sin(moon_vector.radec()[1].radians)*math.cos(math.radians(sidereal_time*15)-moon_vector.radec()[0].radians))

    ##brightLimbAngle = (moon_chi - math.degrees(Moon_parallactic_angle))%360
    
    moondisc0 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
    if Moon_percent == 0:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), 0, 0, 0, color='#94908D') #dummy
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#94908D') #dummy
    elif 0 < Moon_percent < 0.5:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
        moondisc2 = patches.Wedge((0,0), M_d/2, 270+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), 90+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), color='#94908D')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon_percent/0.5), M_d, angle=rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), color='#94908D')
    elif Moon_percent == 0.5:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), 270+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#F0F0F0') #dummy
    elif 0.5 < Moon_percent < 1:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#94908D')
        moondisc2 = patches.Wedge((0,0), M_d/2, 90+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), 270+rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), color='#F0F0F0')
        moondisc3 = patches.Ellipse((0,0), M_d*(1-Moon_percent/0.5), M_d, angle=rot_pa_limb_moon-math.degrees(Moon_parallactic_angle), color='#F0F0F0')
    elif Moon_percent == 1:
        moondisc1 = patches.Circle((0,0), M_d/2, color='#F0F0F0')
        moondisc2 = patches.Wedge((0,0), 0, 0, 0,color='#F0F0F0') #dummy
        moondisc3 = patches.Ellipse((0,0), 0, 0, 0, color='#F0F0F0') #dummy
    
    ax1.add_patch(moondisc0)
    ax1.add_patch(moondisc1)
    ax1.add_patch(moondisc2)
    ax1.add_patch(moondisc3)
    
    #libration
    Mlat, Mlon, distance = (earth - moon).at(date_UTC).frame_latlon(frame)

    T               = (date_UTC.tdb-2451545)/36525 # should use Julian Emphemeris Date instead
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

    PA_axis_moon_N  = math.asin(math.sqrt(X_m*X_m+Y_m*Y_m)*math.cos(moon_vector.radec()[0].radians-omega)/math.cos(Mlon.radians))
            
    PA_axis_moon_z  = Moon_parallactic_angle-PA_axis_moon_N # clockwise, radians
    
    moon_rot = -math.degrees(PA_axis_moon_z) # anti-clockwise
    
    # Mare in Orthographic projection with rotation shown on ax1_moon
    lon0 = Mlon.degrees
    lat0 = Mlat.degrees
    
    if count != 1:
        ax1_moon.remove()
        
    fig0 = plt.figure(0)
    ax_moon_img = plt.axes(projection=ccrs.Orthographic(central_longitude=lon0,central_latitude=lat0))
    ax_moon_img.set_facecolor('none')
    ax_moon_img.axis('off')
    ax_moon_img.imshow(plt.imread('data/moon/moonmap.png'), extent=(-180,180,-90,90), transform=ccrs.PlateCarree())
    #ax_moon_img.gridlines(crs=ccrs.PlateCarree(), color='c')
    #ax_moon_img.set_global()
    #ax_moon_img.background_patch.set_fill(False)
    #ax_moon_img.outline_patch.set_alpha(0)
    fig0.tight_layout(pad=0)
    fig0.savefig('moon_proj.png', bbox_inches='tight', transparent=True)
    plt.close(fig0)
    
#     src = cv2.imread('moon_proj.png',1)
#     tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
#     _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
#     b,g,r = cv2.split(src)
#     rgba = [b,g,r,alpha]
#     dst = cv2.merge(rgba,4)
#     cv2.imwrite('moon_proj_proj.png',dst)
    
    ax1_moon = fig.add_axes([ax1.get_position().x0,ax1.get_position().y0,
                              ax1.get_position().width,ax1.get_position().height], projection=ccrs.Orthographic(central_longitude=lon0,central_latitude=lat0))
    ax1_moon.set_facecolor('none')
    ax1_moon.set_xlim((-90,90))
    ax1_moon.set_ylim((-85,95))
    ax1_moon.axis('off')
    
#     rgba = numpy.array(Image.open(pathlib.Path.cwd().joinpath('moon_proj.png')))
#     rgba[rgba[255,255,255,...]==1] = [0,0,0,0]
#     #print(rgba[rgba[255,255,255,...]==1])
#     print(rgba)
#     Image.fromarray(rgba).save('moon_proj_proj.png')

    moon_proj = Image.open(pathlib.Path.cwd().joinpath('moon_proj.png')).rotate(moon_rot)
    mscale = 1.045
    ax1_moon.imshow(moon_proj, extent=[-M_d/2*mscale,M_d/2*mscale,-M_d/2*mscale,M_d/2*mscale])

    # eq. coord.
    if moon_vector.altaz()[0].degrees > 0:
        ax1_moon.annotate('N',(ph_l*math.sin(Moon_parallactic_angle),ph_l*math.cos(Moon_parallactic_angle)),\
                          xycoords=('data'),rotation=-math.degrees(Moon_parallactic_angle),ha='center',va='center',color='red')
        ax1_moon.plot([ph_r*math.sin(Moon_parallactic_angle),ph_R*math.sin(Moon_parallactic_angle)],\
                      [ph_r*math.cos(Moon_parallactic_angle),ph_R*math.cos(Moon_parallactic_angle)],color='red',zorder=10)
        
        ax1_moon.annotate('E',(ph_l*math.sin(Moon_parallactic_angle+3*math.pi/2),ph_l*math.cos(Moon_parallactic_angle+3*math.pi/2)),\
                          xycoords=('data'),rotation=-math.degrees(Moon_parallactic_angle),ha='center',va='center',color='red')
        ax1_moon.plot([ph_r*math.sin(Moon_parallactic_angle+3*math.pi/2),ph_R*math.sin(Moon_parallactic_angle+3*math.pi/2)],\
                      [ph_r*math.cos(Moon_parallactic_angle+3*math.pi/2),ph_R*math.cos(Moon_parallactic_angle+3*math.pi/2)],color='red',zorder=10)
        
        ax1_moon.annotate('S',(ph_l*math.sin(Moon_parallactic_angle+math.pi),ph_l*math.cos(Moon_parallactic_angle+math.pi)),\
                          xycoords=('data'),rotation=-math.degrees(Moon_parallactic_angle),ha='center',va='center',color='red')
        ax1_moon.plot([ph_r*math.sin(Moon_parallactic_angle+math.pi),ph_R*math.sin(Moon_parallactic_angle+math.pi)],\
                      [ph_r*math.cos(Moon_parallactic_angle+math.pi),ph_R*math.cos(Moon_parallactic_angle+math.pi)],color='red',zorder=10)
        
        ax1_moon.annotate('W',(ph_l*math.sin(Moon_parallactic_angle+math.pi/2),ph_l*math.cos(Moon_parallactic_angle+math.pi/2)),\
                          xycoords=('data'),rotation=-math.degrees(Moon_parallactic_angle),ha='center',va='center',color='red')
        ax1_moon.plot([ph_r*math.sin(Moon_parallactic_angle+math.pi/2),ph_R*math.sin(Moon_parallactic_angle+math.pi/2)],\
                      [ph_r*math.cos(Moon_parallactic_angle+math.pi/2),ph_R*math.cos(Moon_parallactic_angle+math.pi/2)],color='red',zorder=10)

    ax1.annotate('equatorial\ncoordinate',(-88,-70),xycoords=('data'),ha='left',va='bottom',fontproperties=Sans_9,color='red')

    # selenographic
    ax1.annotate('selenographic\ncoordinate',(88,-70),xycoords=('data'),ha='right',va='bottom',fontproperties=Sans_9,color='cyan')

    ax1_moon.annotate('N',(ph_l*math.sin(PA_axis_moon_z),ph_l*math.cos(PA_axis_moon_z)),\
                      xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1_moon.plot([ph_r*math.sin(PA_axis_moon_z),ph_R*math.sin(PA_axis_moon_z)],\
                  [ph_r*math.cos(PA_axis_moon_z),ph_R*math.cos(PA_axis_moon_z)],color='cyan',zorder=10)
    
    ax1_moon.annotate('E',(ph_l*math.sin(PA_axis_moon_z+math.pi/2),ph_l*math.cos(PA_axis_moon_z+math.pi/2)),\
                      xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1_moon.plot([ph_r*math.sin(PA_axis_moon_z+math.pi/2),ph_R*math.sin(PA_axis_moon_z+math.pi/2)],\
                  [ph_r*math.cos(PA_axis_moon_z+math.pi/2),ph_R*math.cos(PA_axis_moon_z+math.pi/2)],color='cyan',zorder=10)
    
    ax1_moon.annotate('S',(ph_l*math.sin(PA_axis_moon_z+math.pi),ph_l*math.cos(PA_axis_moon_z+math.pi)),\
                      xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1_moon.plot([ph_r*math.sin(PA_axis_moon_z+math.pi),ph_R*math.sin(PA_axis_moon_z+math.pi)],\
                  [ph_r*math.cos(PA_axis_moon_z+math.pi),ph_R*math.cos(PA_axis_moon_z+math.pi)],color='cyan',zorder=10)
    
    ax1_moon.annotate('W',(ph_l*math.sin(PA_axis_moon_z+3*math.pi/2),ph_l*math.cos(PA_axis_moon_z+3*math.pi/2)),\
                      xycoords=('data'),rotation=-math.degrees(PA_axis_moon_z),ha='center',va='center',color='cyan')
    ax1_moon.plot([ph_r*math.sin(PA_axis_moon_z+3*math.pi/2),ph_R*math.sin(PA_axis_moon_z+3*math.pi/2)],\
                  [ph_r*math.cos(PA_axis_moon_z+3*math.pi/2),ph_R*math.cos(PA_axis_moon_z+3*math.pi/2)],color='cyan',zorder=10)
    
    # zenith
    if moon_vector.altaz()[0].degrees > 0:
        ax1.arrow(0,M_d/2,0,10,color='green',head_width=5, head_length=5)
        ax1.annotate('diameter = '+str(round(moon_size/60,1))+"'\nelevation = "+str(round(moon_vector.altaz()[0].degrees,1))+u'\N{DEGREE SIGN}',
                     (40,70),xycoords=('data'),ha='left',va='top',fontproperties=Sans_9,color='orange')
    else:
        ax1.annotate('below horizon',(88,70),xycoords=('data'),ha='right',va='top',fontproperties=Sans_9,color='orange')
    ax1.annotate('天頂 ',(0,70),xycoords=('data'),ha='right',va='center',fontproperties=Sans_9,fontsize=11,color='green')
    ax1.annotate(' zenith',(0,70),xycoords=('data'),ha='left',va='center',fontproperties=Sans_9,color='green')
    
    phase_moon = 'illuminated '+str(round(Moon_percent*100,2))+'%' # projected 2D apparent area
    if Moon_percent >= 0:
        ax1.annotate(phase_moon,(0,-80),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_9,color='#F0F0F0')
    else:
        ax1.annotate(phase_moon,(0,-80),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_9,color='#94908D')

    Tmp1 = time.time()
    #print(Tmp1-Tmp0)

def jovian_moons(): #ax2
    Tj0 = time.time()

    timelog('drawing Jupiter')

    ax2.set_xlim((-90,90))
    ax2.set_ylim((-45,45))
    ax2.axis('off')
    ax2.add_patch(patches.Rectangle((-90,-45),180,90,fc='none',ec=(1,1,0,0.75),lw=2))

    ax2.annotate('木星衛星 Jovian Moons',(0,40),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')

    ra_J, dec_J, dis_J = OBS[0].at(date_UTC).observe(jupiterJ).apparent().radec()

    ra_io, dec_io, dis_io = OBS[0].at(date_UTC).observe(io).apparent().radec()
    ra_eu, dec_eu, dis_eu = OBS[0].at(date_UTC).observe(europa).apparent().radec()
    ra_ga, dec_ga, dis_ga = OBS[0].at(date_UTC).observe(ganymede).apparent().radec()
    ra_ca, dec_ca, dis_ca = OBS[0].at(date_UTC).observe(callisto).apparent().radec()
    
    Io_x        = (ra_io.radians - ra_J.radians)*math.cos(dec_J.radians)*dis_J.km/71492
    Io_y        = (dec_io.radians - dec_J.radians)*dis_J.km/71492
    Europa_x    = (ra_eu.radians - ra_J.radians)*math.cos(dec_J.radians)*dis_J.km/71492
    Europa_y    = (dec_eu.radians - dec_J.radians)*dis_J.km/71492
    Ganymede_x  = (ra_ga.radians - ra_J.radians)*math.cos(dec_J.radians)*dis_J.km/71492
    Ganymede_y  = (dec_ga.radians - dec_J.radians)*dis_J.km/71492
    Callisto_x  = (ra_ca.radians - ra_J.radians)*math.cos(dec_J.radians)*dis_J.km/71492
    Callisto_y  = (dec_ca.radians - dec_J.radians)*dis_J.km/71492
        
    Io_radius = 1821.6/71492
    Europa_radius = 1560.8/71492
    Ganymede_radius = 2410.3/71492
    Callisto_radius = 2634.1/71492
    jov_radius = 88/(1+max(abs(Io_x-Io_radius),abs(Io_x+Io_radius),
                           abs(Europa_x-Europa_radius),abs(Europa_x+Europa_radius),
                           abs(Ganymede_x-Ganymede_radius),abs(Ganymede_x+Ganymede_radius),
                           abs(Callisto_x-Callisto_radius),abs(Callisto_x+Callisto_radius)))
    
    Io_r = 5*Io_radius*jov_radius
    Eu_r = 5*Europa_radius*jov_radius
    Ga_r = 5*Ganymede_radius*jov_radius
    Ca_r = 5*Callisto_radius*jov_radius
    
    Jupdisc = patches.Circle((0,0), jov_radius, color='#C88B3A', zorder=-dis_J.km)
    Iodisc = patches.Circle((-Io_x*jov_radius,Io_y*jov_radius), Io_r, color='#9f9538', zorder=-dis_io.km)
    Europadisc = patches.Circle((-Europa_x*jov_radius,Europa_y*jov_radius), Eu_r, color='#6c5d40', zorder=-dis_eu.km)
    Ganymededisc = patches.Circle((-Ganymede_x*jov_radius,Ganymede_y*jov_radius), Ga_r, color='#544a45', zorder=-dis_ga.km)
    Callistodisc = patches.Circle((-Callisto_x*jov_radius,Callisto_y*jov_radius), Ca_r, color='#766b5d', zorder=-dis_ca.km)
    
    ax2.annotate('I',(-Io_x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_12,color='#9f9538')
    ax2.annotate('E',(-Europa_x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_12,color='#6c5d40')
    ax2.annotate('G',(-Ganymede_x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_12,color='#544a45')
    ax2.annotate('C',(-Callisto_x*jov_radius,-30),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_12,color='#766b5d')
    
    ax2.add_patch(Jupdisc)
    ax2.add_patch(Iodisc)
    ax2.add_patch(Europadisc)
    ax2.add_patch(Ganymededisc)
    ax2.add_patch(Callistodisc)
    
    ax2.annotate('\u2190 E',(-88,-40),xycoords=('data'),ha='left',va='bottom',fontproperties=Sans_9,color='red')
    ax2.annotate('W \u2192',(88,-40),xycoords=('data'),ha='right',va='bottom',fontproperties=Sans_9,color='red')
    
    #FOV 5 arcmin
    for i in range(5):
        ax2.add_patch(patches.Circle((0,0),i*5*math.pi/180/60/2*dis_J.km/71492*jov_radius,
                                     fc='none',ec=(1,0,0,0.35),ls='--',zorder=-dis_J.km*2))
        ax2.annotate(str(5*i)+"'",(i*5*math.pi/180/60/2*dis_J.km/71492*jov_radius*math.cos(math.radians(25)),
                                   i*5*math.pi/180/60/2*dis_J.km/71492*jov_radius*math.sin(math.radians(25))),
                     rotation=-65,ha='center',va='center',color=(1,0,0,0.75), backgroundcolor= 'black', zorder=-dis_J.km*2+1)

    Tj1 = time.time()
    #print(Tj1-Tj0)

def mercury_venus(): #ax3
    Tmv0 = time.time()

    timelog('drawing Mercury and Venus')
    
    ax3.set_xlim((-90,90))
    ax3.set_ylim((-45,45))
    ax3.axis('off')
    ax3.add_patch(patches.Rectangle((-90,-45),180,90,fc='none',ec=(1,1,0,0.75),lw=2))

    mercury_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-mercury_vector.radec()[0].radians),
                                          math.sin(sun_vector.radec()[1].radians)*math.cos(mercury_vector.radec()[1].radians)
                                          -math.cos(sun_vector.radec()[1].radians)*math.sin(mercury_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-mercury_vector.radec()[0].radians))) % 360

    venus_chi = math.degrees(math.atan2(math.cos(sun_vector.radec()[1].radians)*math.sin(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians),
                                        math.sin(sun_vector.radec()[1].radians)*math.cos(venus_vector.radec()[1].radians)
                                        -math.cos(sun_vector.radec()[1].radians)*math.sin(venus_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians))) % 360

    Mercury_offsetx = -45
    Venus_offsetx = 45
    MV_d = 30
    rot_pa_limb_mercury = mercury_chi-90
    rot_pa_limb_venus = venus_chi-90

    ax3.annotate('水星 Mercury',(Mercury_offsetx,40),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')
    ax3.annotate('金星 Venus',(Venus_offsetx,40),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')

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
    ax3.annotate(str(round(dist_SM,1))+u'\N{DEGREE SIGN}\nfrom Sun',(Mercury_offsetx,-25),xycoords=('data'),
                 ha='center',va='center',fontproperties=Sans_6,color='#FFCC33')
    if rot_pa_limb_mercury != 0:
        ax3.arrow((MV_d/2-2)*math.sin(math.radians(270-rot_pa_limb_mercury))+Mercury_offsetx,(MV_d/2-2)*math.cos(math.radians(270-rot_pa_limb_mercury)),\
                  (dist_SM/3+2)*math.sin(math.radians(270-rot_pa_limb_mercury)),(dist_SM/3+2)*math.cos(math.radians(270-rot_pa_limb_mercury)),
                  shape='full',length_includes_head=True,head_width=1,color='#FFCC33')
        ax3.annotate('$\u263C$',((MV_d/2+dist_SM/3+5)*math.sin(math.radians(270-rot_pa_limb_mercury))+Mercury_offsetx,
                     (MV_d/2+dist_SM/3+5)*math.cos(math.radians(270-rot_pa_limb_mercury))),
                     xycoords=('data'),ha='center',va='center',fontproperties=Sans_8,color='#FFCC33')
    
    dist_SV = math.degrees(math.acos(math.sin(sun_vector.radec()[1].radians)*math.sin(venus_vector.radec()[1].radians)+math.cos(sun_vector.radec()[1].radians)*math.cos(venus_vector.radec()[1].radians)*math.cos(sun_vector.radec()[0].radians-venus_vector.radec()[0].radians)))
    ax3.annotate(str(round(dist_SV,1))+u'\N{DEGREE SIGN}\nfrom Sun',(Venus_offsetx,-25),xycoords=('data'),
                 ha='center',va='center',fontproperties=Sans_6,color='#FFCC33')
    if rot_pa_limb_venus != 0:
        ax3.arrow((MV_d/2-2)*math.sin(math.radians(270-rot_pa_limb_venus))+Venus_offsetx,(MV_d/2-2)*math.cos(math.radians(270-rot_pa_limb_venus)),\
                  (dist_SV/3+2)*math.sin(math.radians(270-rot_pa_limb_venus)),(dist_SV/3+2)*math.cos(math.radians(270-rot_pa_limb_venus)),
                  shape='full',length_includes_head=True,head_width=1,color='#FFCC33')
        ax3.annotate('$\u263C$',((MV_d/2+dist_SV/3+5)*math.sin(math.radians(270-rot_pa_limb_venus))+Venus_offsetx,
                     (MV_d/2+dist_SV/3+5)*math.cos(math.radians(270-rot_pa_limb_venus))),
                     xycoords=('data'),ha='center',va='center',fontproperties=Sans_8,color='#FFCC33')
    
    ax3.annotate('illuminated '+str(round(Mercury_precent*100,2))+'%',(Mercury_offsetx,-37),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_8,color='#F0F0F0')
    ax3.annotate('illuminated '+str(round(Venus_percent*100,2))+'%',(Venus_offsetx,-37),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_8,color='#F0F0F0')
    
    ax3.annotate('\u2190 E',(-88,-40),xycoords=('data'),ha='left',va='bottom',fontproperties=Sans_9,color='red')
    #ax3.annotate('dist. from Sun',(0,-40),xycoords=('data'),ha='center',va='bottom',fontproperties=Sans_8,color='#FFCC33')
    ax3.annotate('W \u2192',(88,-40),xycoords=('data'),ha='right',va='bottom',fontproperties=Sans_9,color='red')

    Tmv1 = time.time()
    #print(Tmv1-Tmv0)

def ephemeris(): #ax4
    Tep0 = time.time()

    # PyEphem, as skyfield cant compute all mag
    import ephem as PyEphem
    PyEphem.Observer().lon = str(114+6/60+29/3600)
    PyEphem.Observer().lat = str(22+23/60+1/3600)
    PyEphem.Observer().date = datetime.utcnow().replace(second=0,microsecond=0)

    timelog('Ephemeris')

    ax4.set_xlim((-93.5,93.5))
    ax4.set_ylim((-140,140))
    ax4.add_patch(patches.Rectangle((-93.5,-135),187,276,fc='none',ec=(1,1,0,0.75),lw=2))
    
    ax4.annotate('曆表 Ephemeris',(0,135),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')

    sym_x = -85
    rise_x = -20
    set_x = 27
    mag_x = 87.5
    ax4.annotate('出 rise',(rise_x,105),xycoords=('data'),ha='center',va='center',fontproperties=Sans_11,color='white')
    ax4.annotate('沒 set',(set_x,105),xycoords=('data'),ha='center',va='center',fontproperties=Sans_11,color='white')
    ax4.annotate('星等 mag',(mag_x,105),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='white')
    
    # Moon
    moon_y = 85
    if moon_chi>180:
        ax4.annotate('\u263D Moon',(sym_x,moon_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#DAD9D7')
    else:
        ax4.annotate('\u263E Moon',(sym_x,moon_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#DAD9D7')

    t_moon, updown_moon = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, moon, OBS[0]-earth, radius_degrees=0.25))
    for ti, udi in list(zip(t_moon, updown_moon))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,moon_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

##    ax4.annotate(str(round(Moon.mag,1)),(mag_x,moon_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')
    moon_PE = PyEphem.Moon()
    moon_PE.compute(PyEphem.Observer())  
    ax4.annotate(str(round(moon_PE.mag,1)),(mag_x,moon_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Mercury
    mercury_y = 65
    ax4.annotate('\u263F Mercury',(sym_x,mercury_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#97979F')
    
    t_mercury, updown_mercury = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, mercury, OBS[0]-earth))
    for ti, udi in list(zip(t_mercury, updown_mercury))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,mercury_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

    ax4.annotate(str(round(planetary_magnitude(mercury_vector),1)),(mag_x,mercury_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Venus
    venus_y = 45
    ax4.annotate('\u2640 Venus',(sym_x,venus_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#C18F17')
    
    t_venus, updown_venus = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, venus, OBS[0]-earth))
    for ti, udi in list(zip(t_venus, updown_venus))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,venus_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

    ax4.annotate(str(round(planetary_magnitude(venus_vector),1)),(mag_x,venus_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Mars
    mars_y = 25
    ax4.annotate('\u2642 Mars',(sym_x,mars_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#E27B58')
    
    t_mars, updown_mars = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, mars, OBS[0]-earth))
    for ti, udi in list(zip(t_mars, updown_mars))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,mars_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

##    ax4.annotate(str(round(planetary_magnitude(mars_vector),1)),(mag_x,mars_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')
    mars_PE = PyEphem.Mars()
    mars_PE.compute(PyEphem.Observer())  
    ax4.annotate(str(round(mars_PE.mag,1)),(mag_x,mars_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Jupiter
    jupiter_y = 5
    ax4.annotate('\u2643 Jupiter',(sym_x,jupiter_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#C88B3A')
    
    t_jupiter, updown_jupiter = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, jupiter, OBS[0]-earth))
    for ti, udi in list(zip(t_jupiter, updown_jupiter))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,jupiter_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

    ax4.annotate(str(round(planetary_magnitude(jupiter_vector),1)),(mag_x,jupiter_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Saturn
    saturn_y = -15
    ax4.annotate('\u2644 Saturn',(sym_x,saturn_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#A49B72')
    
    t_saturn, updown_saturn = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, saturn, OBS[0]-earth))
    for ti, udi in list(zip(t_saturn, updown_saturn))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,saturn_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

##    ax4.annotate(str(round(planetary_magnitude(saturn_vector),1)),(mag_x,saturn_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')
    saturn_PE = PyEphem.Saturn()
    saturn_PE.compute(PyEphem.Observer())  
    ax4.annotate(str(round(saturn_PE.mag,1)),(mag_x,saturn_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Uranus
    uranus_y = -35
    ax4.annotate('\u2645 Uranus',(sym_x,uranus_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#D5FBFC')
    
    t_uranus, updown_uranus = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, uranus, OBS[0]-earth))
    for ti, udi in list(zip(t_uranus, updown_uranus))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,uranus_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

    ax4.annotate(str(round(planetary_magnitude(uranus_vector),1)),(mag_x,uranus_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    # Neptune
    neptune_y = -55
    ax4.annotate('\u2646 Neptune',(sym_x,neptune_y),xycoords=('data'),ha='left',va='center',fontproperties=icon_11,color='#3E66F9')
    
    t_neptune, updown_neptune = find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),risings_and_settings(ephem, neptune, OBS[0]-earth))
    for ti, udi in list(zip(t_neptune, updown_neptune))[:2]:
        if udi == 1:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
        elif udi == 0:
            ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,neptune_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))

##    ax4.annotate(str(round(planetary_magnitude(neptune_vector),1)),(mag_x,neptune_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')
    neptune_PE = PyEphem.Neptune()
    neptune_PE.compute(PyEphem.Observer())  
    ax4.annotate(str(round((neptune_PE.mag),1)),(mag_x,neptune_y),xycoords=('data'),ha='right',va='center',fontproperties=Sans_11,color='yellow')

    ###################################################################################################################################################
    
    # astronomical twilight

    ax4.annotate('天文曙光 Astronomical Twilight',(0,-75),xycoords=('data'),ha='center',va='top',fontproperties=Sans_title,color='white')

    sun_y = -105

    t_twilight, updown_twilight = almanac.find_discrete(ts.utc(ts.now().utc_datetime()),ts.utc(ts.now().utc_datetime()+timedelta(days=1.5)),
                                                        almanac.dark_twilight_day(ephem, OBS[0]-earth))

    for ti, udi in list(zip(t_twilight, updown_twilight))[:8]:
        if udi == 1:
            if ti.astimezone(tz).hour <12:
                ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(rise_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
            else:
                ax4.annotate(str(ti.astimezone(tz).strftime('%X')),(set_x,sun_y),xycoords=('data'),ha='center',va='center',fontproperties=(Sans_B_11 if ti.astimezone(tz).date() > date_local.date() else Sans_11),color=('green' if ti.astimezone(tz).date() > date_local.date() else 'orange'))
                
    ax4.annotate('orange: today   ',(0,-125),xycoords=('data'),ha='right',va='center',fontproperties=Sans_8,color='orange')
    ax4.annotate('   green & bold: +1day',(0,-125),xycoords=('data'),ha='left',va='center',fontproperties=Sans_B_8,color='green')

    Tep1 = time.time()
    #print(Tep1-Tep0)

def updateTime():
    ax5.set_xlim((-90,90))
    ax5.set_ylim((-85,85))
    ax5.axis('off')
    ax5.annotate(str(date_local.strftime('Updated time: %d/%m/%Y %H:%M:%S')),(5,10),ha='center',va='center',fontproperties=Sans_11, color='white')

def moonNplanet():
    solSysData()
    moon_phase()
    jovian_moons()
    mercury_venus()
    ephemeris()
    updateTime()

def refresh_data(i):
    global fig, count, date_UTC, date_local

    ###########
    # removal #
    ###########
    start = time.time()
    count = count + 1

    # clear the world
    gc.collect()
    try:
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        timelog('cleared moon & planet data')
    except:
        timelog('survivor')

    ##########
    # update #
    ##########

    # update time
    date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
    date_local  = date_UTC.astimezone(tz)

    moonNplanet()

    # plot
    fig.canvas.draw() 
    fig.canvas.flush_events()
    plt.savefig('output/moonNplanet.png', dpi=200, pad_inches=0)

    # make red version
    img = Image.open("output/moonNplanet.png").convert("RGB")
    width, height = img.size
    pixels = img.load()
    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            newR = round((r+g+b)/3.5) if ((r+g+b)/3)>200 else round((r+g+b)/3+(r+g)/2.5)
            newG = 0
            newB = 0
            pixels[px, py] = (newR, newG, newB)
    img.save("output/moonNplanet_red.png")

    #upload to SFTP
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    userfile = open("id.txt", "r")
    user = userfile.read()
    pwfile = open("pw.txt", "r")
    password = pwfile.read()
    with pysftp.Connection('192.168.1.223', username=user, password=password, cnopts=cnopts) as sftp:
        sftp.cwd("/var/www/html/astroInfo/images")
        sftp.put("./output/moonNplanet.png", "./moonNplanet.png")
        sftp.put( "./output/moonNplanet_red.png", "./moonNplanet_red.png")
        sftp.close()

    timelog('ftp upload job done')

    end = time.time()
    timelog(str(round(end-start,2))+'s wasted')

def refresh_refresh_data(i):
    try:
        refresh_data(i)
    except Exception as e:
        print(e)
        pass
    
if platform == 'win32':
    ani = matplotlib.animation.FuncAnimation(fig, refresh_refresh_data, repeat=False, interval=10000, save_count=0)
else:
    ani = matplotlib.animation.FuncAnimation(fig, refresh_refresh_data, repeat=False, interval=25000, save_count=0)

timelog('backend is '+str(matplotlib.get_backend()))

plt.get_current_fig_manager().window.wm_geometry('-5-25')

plt.show()