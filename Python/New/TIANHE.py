#http://celestrak.com/NORAD/elements/

import pathlib
import warnings
from datetime import timedelta
from skyfield import api
from skyfield.api import Star, load, wgs84, EarthSatellite
from skyfield.data import hipparcos, stellarium
from pytz import timezone, common_timezones
import numpy
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.collections import LineCollection
import matplotlib.animation
import matplotlib.cbook
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
import cartopy.io.shapereader as shapereader
import cartopy.io.img_tiles as cimgt

ephem   = load('de421.bsp') #1900-2050 only
##sun     = ephem['sun']
earth   = ephem['earth']
##moon    = ephem['moon']

hokoon  = wgs84.latlon(22+23/60+1/3600, 114+6/60+29/3600)

fig = plt.figure(figsize=(8,10), facecolor='white')

def falling(i):
    global ax0, ax1
    
    ts      = load.timescale()
    tz      = timezone('Asia/Hong_Kong')
    t_now   = ts.now().astimezone(tz)
    t_t     = int(900) #+/-15mins
    t_range = []
    t_range = ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute, ts.now().utc.second+range(-t_t, t_t+1))

    try:
        CZ5B = load.tle_file('https://celestrak.com/satcat/tle.php?CATNR=48275', reload=True)[0]
    except:
        try:
            CZ5B = api.load.tle('https://celestrak.com/NORAD/elements/stations.txt')['CZ-5B R/B']
        except:
            try:
                with open('/home/pi/Desktop/tle.php') as myfile:
                    lines = myfile.read().splitlines()
                    CZ5B = EarthSatellite(lines[1],lines[2],lines[0],ts)
            except:
                pass
            pass
        pass

    try:
        print('orbital elements epoch:\n'+str(CZ5B.epoch.astimezone(tz)))
        print('{:.2f} hours after epoch'.format((ts.now()-CZ5B.epoch)*24))
    except:
        pass

    ra_0, dec_0, edistance_0 = (CZ5B).at(ts.now()).radec()
    ra_5, dec_5, edistance_5 = (CZ5B).at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+5, ts.now().utc.second)).radec()
    ra_10, dec_10, edistance_10 = (CZ5B).at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+10, ts.now().utc.second)).radec()
    ra_15, dec_15, edistance_15 = (CZ5B).at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+15, ts.now().utc.second)).radec()
    ra, dec, edistance = (CZ5B).at(t_range).radec()
    #alt, az, tdistance = (CZ5B - hokoon).at(t_range).altaz()

    terr_orbit  = wgs84.subpoint(CZ5B.at(t_range))
    subpoint_0  = wgs84.subpoint(CZ5B.at(ts.now()))
    subpoint_5  = wgs84.subpoint(CZ5B.at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+5, ts.now().utc.second)))
    subpoint_10 = wgs84.subpoint(CZ5B.at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+10, ts.now().utc.second)))
    subpoint_15 = wgs84.subpoint(CZ5B.at(ts.utc(ts.now().utc.year, ts.now().utc.month, ts.now().utc.day, ts.now().utc.hour, ts.now().utc.minute+15, ts.now().utc.second)))
    geolocator  = Nominatim(user_agent="geoapiExercises")
    overhead    = geolocator.reverse(str(subpoint_0.latitude.degrees)+","+str(subpoint_0.longitude.degrees))

    try:
        print('CZ-5B R/B is now '+str(int(subpoint_0.elevation.km))+'km over '+str(overhead.raw['address'].get('country', '')))
    except:
        print('CZ-5B R/B is now '+str(int(subpoint_0.elevation.km))+'km over Middle of NoWhere')

    #####terr_orbit.elevation.km
        
    print('LAT: '+str(subpoint_0.latitude.dstr())+', LON: '+str(subpoint_0.longitude.dstr()))

    try:
        print(overhead.raw['address'].get('city', ''))
    except:
        pass

    ### plot ###
    try:
        ax0.clear()
    except:
        print('ax0 stuck')
        pass
    try:
        ax1.clear()
    except:
        print('ax1 stuck')
        pass
        
    # altaz plot
    ax0 = plt.subplot(2,1,1,projection=ccrs.PlateCarree())

    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)

    url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
           '/skycultures/western_SnT/constellationship.fab')

    with load.open(url) as f:
        constellations = stellarium.parse_constellations(f)

    edges = [edge for name, edges in constellations for edge in edges]
    edges_star1 = [star1 for star1, star2 in edges]
    edges_star2 = [star2 for star1, star2 in edges]

    FOV = 45.0
    angle = numpy.pi - FOV / 360.0 * numpy.pi
    limit = numpy.degrees(numpy.sin(angle) / (1.0 - numpy.cos(angle)))

    limiting_magnitude = 5.0

    bright_stars = (stars.magnitude <= limiting_magnitude)
    magnitude = stars['magnitude'][bright_stars]
    marker_size = (limiting_magnitude - magnitude) ** 1.5

    xy1 = stars[['ra_degrees', 'dec_degrees']].loc[edges_star1].values
    xy2 = stars[['ra_degrees', 'dec_degrees']].loc[edges_star2].values
    lines_xy = numpy.rollaxis(numpy.array([xy1, xy2]), 1)

    ax0.add_collection(LineCollection(lines_xy, colors=(0.5,0.5,0.5,0.5), zorder=1, transform=ccrs.Geodetic()))
    ax0.scatter(stars['ra_degrees'][bright_stars], stars['dec_degrees'][bright_stars], s=marker_size, color='k', zorder=2, transform=ccrs.Geodetic())
    ax0.plot(ra.hours[0:t_t]*15,dec.degrees[0:t_t],'b-', transform=ccrs.Geodetic())
    ax0.plot(ra.hours[t_t:t_t*2]*15,dec.degrees[t_t:t_t*2],'b--', transform=ccrs.Geodetic())
    ax0.plot(ra_0.hours*15, dec_0.degrees, 'r+', markersize=6, transform=ccrs.Geodetic())
    ax0.plot(ra_5.hours*15, dec_5.degrees, 'g+', markersize=6, transform=ccrs.Geodetic())
    ax0.plot(ra_10.hours*15, dec_10.degrees, 'b+', markersize=6, transform=ccrs.Geodetic())
    ax0.plot(ra_15.hours*15, dec_15.degrees, 'c+', markersize=6, transform=ccrs.Geodetic())
    if dec_5.degrees >= dec_0.degrees:
        ax0.annotate(' now ', xy=(ra_0.hours*15, dec_0.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='right', va='top')
        ax0.annotate(' T+5m ', xy=(ra_5.hours*15, dec_5.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='right', va='top')
        ax0.annotate(' T+10m ', xy=(ra_10.hours*15, dec_10.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='right', va='top')
        ax0.annotate(' T+15m ', xy=(ra_15.hours*15, dec_15.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='right', va='top')
    else:
        ax0.annotate(' now ', xy=(ra_0.hours*15, dec_0.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='left', va='top')
        ax0.annotate(' T+5m ', xy=(ra_5.hours*15, dec_5.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='left', va='top')
        ax0.annotate(' T+10m ', xy=(ra_10.hours*15, dec_10.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='left', va='top')
        ax0.annotate(' T+15m ', xy=(ra_15.hours*15, dec_15.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax0), ha='left', va='top')
#     if ra_0.hours*15-limit*3 >= 180:
#         ax0.set_xlim(ra_0.hours*15-limit*3-360, ra_0.hours*15+limit*3-360)
#     else:
#         ax0.set_xlim(ra_0.hours*15-limit*3, ra_0.hours*15+limit*3)
#     print(ra_0.hours*15-limit*3, ra_0.hours*15+limit*3)
#     ax0.set_ylim(dec_0.degrees-limit*3, dec_0.degrees+limit*3)
    #ax0.set_extent([ra_0.hours*15-limit*3,ra_0.hours*15+limit*3,dec_0.degrees-limit*3,dec_0.degrees+limit*3], crs=ccrs.PlateCarree())
    print([ra_0.hours*15-limit*3,ra_0.hours*15+limit*3,dec_0.degrees-limit*3,dec_0.degrees+limit*3])
    ax0.set_aspect('equal')
    ax0.invert_xaxis()

    #ax0.gridlines(dms=False, draw_labels=False, color='w', crs=ccrs.PlateCarree(), zorder=0)
    
    textstr = ''
    try:
        textstr = ('CZ-5B R/B is now '+str(int(subpoint_0.elevation.km))+'km over '+str(overhead.raw['address'].get('country', ''))+'\n'+
                   'LAT: '+str(subpoint_0.latitude.dstr())+', LON: '+str(subpoint_0.longitude.dstr())+'\n'+
                   str(ts.now().astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'))+' HKT'+'\n'+
                   'orbital elements updated: '+'{:.2f} hours ago'.format((ts.now()-CZ5B.epoch)*24))
    except:
        textstr = ('CZ-5B R/B is now '+str(int(subpoint_0.elevation.km))+'km over Middle of NoWhere'+'\n'+
                   'LAT: '+str(subpoint_0.latitude.dstr())+', LON: '+str(subpoint_0.longitude.dstr())+'\n'+
                   str(ts.now().astimezone(tz).strftime('%d/%m/%Y %H:%M:%S'))+' HKT'+'\n'+
                   'orbital elements updated: '+'{:.2f} hours ago'.format((ts.now()-CZ5B.epoch)*24))

    plt.title(textstr, fontsize=8)
    
    # global plot
    ax1 = plt.subplot(2,1,2,projection=ccrs.Orthographic(central_longitude=subpoint_0.longitude.degrees, central_latitude=subpoint_0.latitude.degrees))
    ax1.coastlines()
    ax1.set_global()
    ax1.gridlines(dms=True,xlocs=[-150,-120,-90,-60,-30,0,30,60,90,120,150,180],xformatter=LONGITUDE_FORMATTER,ylocs=[-60,-30,0,30,60],yformatter=LATITUDE_FORMATTER)
    ax1.plot(terr_orbit.longitude.degrees[0:t_t],terr_orbit.latitude.degrees[0:t_t],'b-',transform=ccrs.Geodetic())
    ax1.plot(terr_orbit.longitude.degrees[t_t:t_t*2],terr_orbit.latitude.degrees[t_t:t_t*2],'b--',transform=ccrs.Geodetic())
    ax1.plot(subpoint_0.longitude.degrees,subpoint_0.latitude.degrees,'r+',markersize=6,transform=ccrs.PlateCarree())
    ax1.plot(subpoint_5.longitude.degrees,subpoint_5.latitude.degrees,'g+',markersize=6,transform=ccrs.PlateCarree())
    ax1.plot(subpoint_10.longitude.degrees,subpoint_10.latitude.degrees,'b+',markersize=6,transform=ccrs.PlateCarree())
    ax1.plot(subpoint_15.longitude.degrees,subpoint_15.latitude.degrees,'c+',markersize=6,transform=ccrs.PlateCarree())
    if subpoint_5.latitude.degrees >= subpoint_0.latitude.degrees:
        ax1.annotate(' now ', xy=(subpoint_0.longitude.degrees,subpoint_0.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='left', verticalalignment='top')
        ax1.annotate(' T+5m ', xy=(subpoint_5.longitude.degrees,subpoint_5.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='left', verticalalignment='top')
        ax1.annotate(' T+10m ', xy=(subpoint_10.longitude.degrees,subpoint_10.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='left', verticalalignment='top')
        ax1.annotate(' T+15m ', xy=(subpoint_15.longitude.degrees,subpoint_15.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='left', verticalalignment='top')
    else:
        ax1.annotate(' now ', xy=(subpoint_0.longitude.degrees,subpoint_0.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='right', verticalalignment='top')
        ax1.annotate(' T+5m ', xy=(subpoint_5.longitude.degrees,subpoint_5.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='right', verticalalignment='top')
        ax1.annotate(' T+10m ', xy=(subpoint_10.longitude.degrees,subpoint_10.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='right', verticalalignment='top')
        ax1.annotate(' T+15m ', xy=(subpoint_15.longitude.degrees,subpoint_15.latitude.degrees),  xycoords=ccrs.PlateCarree()._as_mpl_transform(ax1), horizontalalignment='right', verticalalignment='top')

    plt.tight_layout()
    fig.canvas.draw() 
    fig.canvas.flush_events()
    plt.savefig('Boooom.png')

ani = matplotlib.animation.FuncAnimation(fig, falling, repeat=False, interval=30000, save_count=0)
warnings.filterwarnings('ignore',category=matplotlib.cbook.mplDeprecation)
plt.show()
