import time
import numpy
import math
from skyfield import almanac
from skyfield.api import load, Topos
from skyfield.trigonometry import position_angle_of
from pytz import timezone, common_timezones
from datetime import date, datetime, timedelta

#####################################
#initial setup
w_year = 2020 #<= which year you want
#####################################

start = time.time()

#####################################
# ephem setting
tz          = timezone('Asia/Hong_Kong')

ephem       = load('de421.bsp') #1900-2050 only
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
#####################################

#####################################
# location information
#HKO
Trig_0      = (Topos(str(22+18/60+7.3/3600)+' N', str(114+10/60+27.6/3600)+' E'),\
               22+18/60+7.3/3600,114+10/60+27.6/3600,'22:18:07.3','N','114:10:27.6','E')

#Hokoon
hokoon      = (Topos(str(22+23/60+1/3600)+' N', str(114+6/60+29/3600)+' E'),\
               22+23/60+1/3600,114+6/60+29/3600,'22:23:01','N','114:06:29','E')

Obs         = earth + hokoon[0] #<= set your observatory

ts          = load.timescale()
##date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
##date_local  = date_UTC.astimezone(tz)
#####################################

DT_UTC = ts.utc(w_year,6,26,6,0,range(0,4*60*60))
DT_HK = DT_UTC.astimezone(tz)

#convert time to decimal hour
def decimal_hour(datetime):
    return datetime.hour+datetime.minute/60+datetime.second/3600+datetime.microsecond/3600000000
def common_time(x):
    return str(format(int(x),'02d'))+':'+str(format(int((x-int(x))*60),'02d'))

#####SUN#####
(alt_s,az_s,d_s) = Obs.at(DT_UTC).observe(sun).apparent().altaz()

##print(DT_HK)
##print(*az_s.degrees,sep='\n')

#####MOON#####
(alt_m,az_m,d_m) = Obs.at(DT_UTC).observe(moon).apparent().altaz()

##print(DT_HK)
##print(*d_m.au,sep='\n')

#####MERCURY#####
#####VENUS#####
#####MARS#####
#####JUPITER#####
#####SATURN#####

#sunmoonsep#
sep = Obs.at(DT_UTC).observe(sun).apparent().separation_from(Obs.at(DT_UTC).observe(moon).apparent())

print(*sep.degrees,sep='\n')
