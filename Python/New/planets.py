from skyfield.api import load, Topos
from datetime import datetime
from pytz import timezone, common_timezones
#from astropy.coordinates import SkyCoord, Angle
import matplotlib
import matplotlib.pyplot as plt
import math

tz = timezone('Asia/Hong_Kong')

ephem = load('de421.bsp') #1900-2050 only
#ephem = load('de422.bsp') #-3000-3000 only
#ephem = load('de430t.bsp') #1550-2650 only
sun         = ephem['sun']
mercury     = ephem['mercury']
venus       = ephem['venus']
earthmoon   = ephem['earth_barycenter']
earth       = ephem['earth']
moon        = ephem['moon']
mars        = ephem['mars']
jupiter     = ephem['jupiter_barycenter']
saturn      = ephem['saturn_barycenter']
uranus      = ephem['uranus_barycenter']
neptune     = ephem['neptune_barycenter']
pluto       = ephem['pluto_barycenter']

hokoon      = earth + Topos(str(22+23/60+1/3600)+' N', str(114+6/60+29/3600)+' E')

ts = load.timescale()

mercury_color   = [105/255,189/255,69/255]
venus_color     = [111/255,204/255,221/255]
moon_color      = [255/255,255/255,0/255]
mars_color      = [237/255,31/255,36/255]
jupiter_color   = [139/255,137/255,137/255]
saturn_color    = [185/255,82/255,159/255]

hours = list(range(30*24))

DT_UTC = ts.utc(2020, 12, 2, hours, 00, 00)

#DT_UTC = ts.utc(2021, 2, 6, 4, list(range(4*60)), 00)

#DT_UTC = ts.utc(2021, 12, 2, 23, 33, 00)

DT_HK = DT_UTC.astimezone(tz)

mercury_vector = hokoon.at(DT_UTC).observe(mercury).apparent()
venus_vector = hokoon.at(DT_UTC).observe(venus).apparent()
moon_vector = hokoon.at(DT_UTC).observe(moon).apparent()
mars_vector = hokoon.at(DT_UTC).observe(mars).apparent()
jupiter_vector = hokoon.at(DT_UTC).observe(jupiter).apparent()
saturn_vector = hokoon.at(DT_UTC).observe(saturn).apparent()

##print(DT_HK)
##print(moon_vector.radec(epoch='date')[0],moon_vector.radec(epoch='date')[1])
##print(mars_vector.radec(epoch='date')[0],mars_vector.radec(epoch='date')[1])
#ra2, dec2, distance2 = moon_vector.radec(ts.J2000)
#ra3, dec3, distance3 = astrometric3.radec(ts.J2000)
#print(DT_HK, ra2, dec2)

def moon_size(utc):
    MOON_RADIUS = 1737.1 # km
    appR = 180 / math.pi * math.atan(MOON_RADIUS / hokoon.at(utc).observe(moon).distance().km)
    return appR

ref_vector = saturn_vector

sep_m = mercury_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if mercury_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_m[i]=-1*sep_m[i]
    
sep_v = venus_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if venus_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_v[i]=-1*sep_v[i]

sep_mm = moon_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if moon_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_mm[i]=-1*sep_mm[i]

sep_ma = mars_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if mars_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_ma[i]=-1*sep_ma[i]

sep_j = jupiter_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if jupiter_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_j[i]=-1*sep_j[i]

sep_s = saturn_vector.separation_from(ref_vector).degrees
for i in range(len(DT_UTC)):
    if saturn_vector.radec(epoch='date')[0].hours[i] >= ref_vector.radec(epoch='date')[0].hours[i]:
        pass
    else:
        sep_s[i]=-1*sep_s[i]

#print(sep_ma)

matplotlib.rcParams['timezone'] = tz #tz of plot should be set here

plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_m,color=mercury_color,linestyle='-',linewidth=1,marker='None')
plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_v,color=venus_color,linestyle='-',linewidth=1,marker='None')
plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_mm,color=moon_color,linestyle='-',linewidth=1,marker='None')

moon_sizes = [0]*len(DT_UTC)
for i in range(len(DT_UTC)):
    moon_sizes[i] = moon_size(DT_UTC[i])
plt.plot_date(matplotlib.dates.date2num(DT_UTC),moon_sizes,color=moon_color,linestyle='-',linewidth=1,marker='None')

plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_ma,color=mars_color,linestyle='-',linewidth=1,marker='None')
plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_j,color=jupiter_color,linestyle='-',linewidth=1,marker='None')
plt.plot_date(matplotlib.dates.date2num(DT_UTC),sep_s,color=saturn_color,linestyle='-',linewidth=1,marker='None')
plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m-%d %H:%M'))
plt.gcf().autofmt_xdate()
#plt.ylim(-120,120)
plt.show()

##for i in range(len(DT_HK)):
##    print(DT_HK[i].strftime('%H:%M'),sep_s[i])
