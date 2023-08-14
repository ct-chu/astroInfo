import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas
import numpy
import math
from skyfield import almanac
from skyfield.api import load, Topos
from skyfield.magnitudelib import planetary_magnitude
from pytz import timezone, common_timezones
from datetime import date, datetime, timedelta
from sys import platform

#####################################
#initial setup
w_year = 2020 #<= which year you want
#####################################

#set font
if platform == 'win32':
    chara_chi_6 = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/FZHTB.TTF', size=6)
    chara_chi_15 = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/FZHTB.TTF', size=15)
    chara_chi_22 = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/FZHTB.TTF', size=22)
    chara_eng_15 = font_manager.FontProperties(fname = 'C:/WINDOWS/Fonts/HELR45W.ttf', size=15)
else:
    chara_chi_6 = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF', size=6)
    chara_chi_15 = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF', size=15)
    chara_chi_22 = font_manager.FontProperties(fname = '/Library/Fonts/SIMHEI.TTF', size=22)
    chara_eng_15 = font_manager.FontProperties(fname = '/Library/Fonts/Helvetica.ttc', size=15)

#force use TrueType font instead of Type3 font
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

#savefig has its default bg color as white, override it
matplotlib.rcParams['savefig.facecolor'] = (3/255,0/255,45/255)

#default save as pdf
matplotlib.rcParams['savefig.format'] = 'pdf'

#####################################
# ephem setting
tz          = timezone('Asia/Hong_Kong')

ephem       = load('de421.bsp') #1900-2050 only
#ephem      = load('de422.bsp') #-3000-3000 only
#ephem      = load('de430t.bsp') #1550-2650 only
#sun         = ephem['sun']
#mercury     = ephem['mercury']
#venus       = ephem['venus']
#earthmoon   = ephem['earth_barycenter']
earth       = ephem['earth']
#moon        = ephem['moon']
mars        = ephem['mars']
#jupiter     = ephem['jupiter_barycenter']
#saturn      = ephem['saturn_barycenter']
#uranus      = ephem['uranus_barycenter']
#neptune     = ephem['neptune_barycenter']
#pluto       = ephem['pluto_barycenter']
#####################################

#####################################
# location information
#HKO
Trig_0      = (Topos(str(22+18/60+7.3/3600)+' N', str(114+10/60+27.6/3600)+' E'),\
               22+18/60+7.3/3600,114+10/60+27.6/3600,'22:18:07.3','N','114:10:27.6','E')

#Hokoon
hokoon      = (Topos(str(22+23/60+1/3600)+' N', str(114+6/60+29/3600)+' E'),\
               22+23/60+1/3600,114+6/60+29/3600,'22:23:01','N','114:06:29','E')

Obs         = hokoon #<= set your observatory

ts          = load.timescale()
##date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
##date_local  = date_UTC.astimezone(tz)
#####################################

DT_UTC = ts.utc(w_year,9,range(30,124))
DT_HK = DT_UTC.astimezone(tz)

DT_UTC1 = ts.utc(w_year,9,30,range(0,24*93),45,0)
DT_HK1 = DT_UTC1.astimezone(tz)

#####MARS#####
##mars_dt, mars_y         = almanac.find_discrete(DT_UTC[0], DT_UTC[-1], almanac.risings_and_settings(ephem, mars, Obs[0]))
##
##mars_rise               = [(dti.astimezone(tz).strftime('%m/%d/%Y, %H:%M:%S')) for dti, yi in zip(mars_dt, mars_y) if yi == True]
##
##mars_set                = [(dti.astimezone(tz).strftime('%m/%d/%Y, %H:%M:%S')) for dti, yi in zip(mars_dt, mars_y) if yi == False]
##
malt,maz,mau            = (earth+hokoon[0]).at(DT_UTC1).observe(mars).apparent().altaz()

mars_transit            = [(DT_HK1i.strftime('%m/%d/%Y, %H:%M:%S'),aui) for DT_HK1i,aui in zip(DT_HK1,mau.km)]

#print(mars_rise)
#print(mars_set)
print(mars_transit)
#####################################

#####################################
ax0 = plt.subplot(projection='polar')
ax0.set_theta_zero_location("N")
ax0.set_ylim([0,12])
ax0.axis('off')

#month dial
moct = [169.21,160.37,151.54,142.71,133.89,125.08,116.27,107.47, 98.67, 89.87,
         81.08, 72.29, 63.49, 54.70, 45.90, 37.11, 28.31, 19.50, 10.69,  1.88,
        353.05,344.22,335.39,326.54,317.68,308.82,299.94,291.05,282.15,273.24,
        264.31,255.38]

mnov = [255.38,246.43,237.46,228.49,219.50,210.49,201.47,192.44,183.39,174.33,
        165.26,156.17,147.06,137.94,128.81,119.66,110.50,101.32, 92.13, 82.93,
         73.71, 64.48, 55.23, 45.97, 36.70, 27.42, 18.12,  8.81,359.49,350.16,
        340.82]

mdec = [340.82,331.46,322.10,312.72,303.34,293.94,284.54,275.12,265.70,256.27,
        246.83,237.38,227.92,218.45,208.97,199.49,190.00,180.50,171.00,161.48,
        151.96,142.44,132.91,123.37,113.83,104.28, 94.72, 85.16, 75.60, 66.03,
         56.45, 46.87]

ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[4.5]*3600)
for i in range(len(moct)):
    ax0.plot([math.radians(moct[i]),math.radians(moct[i])],[4.5,5])
    
ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[5]*3600)
for i in range(len(mnov)):
    ax0.plot([math.radians(mnov[i]),math.radians(mnov[i])],[5,5.5])
    
ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[5.5]*3600)
for i in range(len(mdec)):
    ax0.plot([math.radians(mdec[i]),math.radians(mdec[i])],[5.5,6])

ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[6]*3600)

#2hr grid
ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[9]*3600)
for i in range(12):
    ax0.plot([math.radians(30*i+15),math.radians(30*i+15)],[6,12])

ax0.plot((numpy.pi/180)*numpy.arange(0,360,0.1),[12]*3600)

#window
offset = 9
r_win = 2
r1 = [0]*1800
t1 = [0]*1800
r2 = [0]*1800
t2 = [0]*1800
for i in range(1800):
    deter = r_win*r_win-offset*offset*math.sin(math.radians(i/10+270))*math.sin(math.radians(i/10+270))
    if deter>=0:
        r1[i] = offset*math.cos(math.radians(i/10+270))+math.sqrt(deter)
        r2[i] = offset*math.cos(math.radians(i/10+270))-math.sqrt(deter)
        t1[i] = math.radians(i/10+270)
        t2[i] = math.radians(i/10+270)
    else:
        pass

win1 = zip(t1,r1)
win1 = filter(lambda item: item[1] != 0, win1)
t1,r1 = map(list,zip(*win1))

win2 = zip(t2,r2)
win2 = filter(lambda item: item[1] != 0, win2)
t2,r2 = map(list,zip(*win2))

ax0.plot(t1,r1)
ax0.plot(t2,r2)



#plt.show()
