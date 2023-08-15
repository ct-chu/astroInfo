import time
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas
import numpy
import math
#import ephem
from skyfield import almanac
from skyfield.api import load, Topos
from pytz import timezone, common_timezones
from datetime import date, datetime, timedelta
from sys import platform

#####################################
#initial setup
w_year = 2020 #<= which year you want
#####################################

start = time.time()

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

Obs         = hokoon #<= set your observatory

ts          = load.timescale()
##date_UTC    = ts.utc(ts.now().utc_datetime().replace(second=0,microsecond=0))
##date_local  = date_UTC.astimezone(tz)
#####################################

DT_UTC = ts.utc(w_year-1,12,range(31,31+368))
DT_HK = DT_UTC.astimezone(tz)

#convert time to decimal hour
def decimal_hour(datetime):
    return datetime.hour+datetime.minute/60+datetime.second/3600+datetime.microsecond/3600000000
def common_time(x):
    return str(format(int(x),'02d'))+':'+str(format(int((x-int(x))*60),'02d'))

#make slice of plots when over lims range
def unlink_wrap(dat, lims=[-numpy.pi, numpy.pi], thresh = 0.95): #define lim below
    jump = numpy.nonzero(numpy.abs(numpy.diff(dat)) > ((lims[1] - lims[0]) * thresh))[0]
    lasti = 0
    for ind in jump:
        yield slice(lasti, ind + 1)
        lasti = ind + 1
    yield slice(lasti, len(dat))
#https://stackoverflow.com/questions/27138751/preventing-plot-joining-when-values-wrap-in-matplotlib-plots

#####SUN#####
sun_dt, sun_y           = almanac.find_discrete(DT_UTC[0], DT_UTC[-1], almanac.sunrise_sunset(ephem, Obs[0]))

sun_rise                = [(dti.astimezone(tz).date(),decimal_hour(dti.astimezone(tz).time())) for dti, yi in zip(sun_dt, sun_y) if yi == True]
sun_rise_t2             = [t+24 for d,t in sun_rise if t <= 9]
sun_rise_d2             = [d for d,t in sun_rise if t <= 9]

sun_set                 = [(dti.astimezone(tz).date(),decimal_hour(dti.astimezone(tz).time())) for dti, yi in zip(sun_dt, sun_y) if yi == False]
sun_set_t1              = [t for d,t in sun_set if t >= 16]
sun_set_d1              = [d for d,t in sun_set if t >= 16]

#####MARS#####
mars_dt, mars_y         = almanac.find_discrete(DT_UTC[0], DT_UTC[-1], almanac.risings_and_settings(ephem, mars, Obs[0]))

mars_rise               = [(dti.astimezone(tz).date(),decimal_hour(dti.astimezone(tz).time())) for dti, yi in zip(mars_dt, mars_y) if yi == True]
mars_rise_t1            = [t for d,t in mars_rise if t >= 16]
mars_rise_d1            = [d for d,t in mars_rise if t >= 16]
mars_rise_t2            = [t+24 for d,t in mars_rise if t <= 9]
mars_rise_d2            = [d for d,t in mars_rise if t <= 9]

mars_set                = [(dti.astimezone(tz).date(),decimal_hour(dti.astimezone(tz).time())) for dti, yi in zip(mars_dt, mars_y) if yi == False]
mars_set_t1             = [t for d,t in mars_set if t >= 16]
mars_set_d1             = [d for d,t in mars_set if t >= 16]
mars_set_t2             = [t+24 for d,t in mars_set if t <= 9]
mars_set_d2             = [d for d,t in mars_set if t <= 9]

mars_tran_t1            = [23.9150,23.8289,23.7433,23.6581,23.5733,23.4892,23.4053,23.3219,23.2394,23.1572,23.0758,22.9953,22.9153,22.8361,22.7575,
                           22.6797,22.6028,22.5267,22.4511,22.3767,22.3028,22.2300,22.1578,22.0867,22.0161,21.9467,21.8781,21.8103,21.7431,21.6769,
                           21.6117,21.5472,21.4836,21.4208,21.3586,21.2975,21.2369,21.1775,21.1186,21.0603,21.0031,20.9464,20.8903,20.8350,20.7803,
                           20.7264,20.6731,20.6206,20.5683,20.5169,20.4661,20.4158,20.3664,20.3172,20.2686,20.2206,20.1733,20.1264,20.0800,20.0342,
                           19.9886,19.9439,19.8994,19.8556,19.8119,19.7689,19.7264,19.6842,19.6425,19.6011,19.5603,19.5197,19.4794,19.4394,19.4000,
                           19.3611]
mars_tran_d1            = [date(2020,10,17),date(2020,10,18),date(2020,10,19),date(2020,10,20),date(2020,10,21),\
                           date(2020,10,22),date(2020,10,23),date(2020,10,24),date(2020,10,25),date(2020,10,26),\
                           date(2020,10,27),date(2020,10,28),date(2020,10,29),date(2020,10,30),date(2020,10,31),\
                           date(2020,11, 1),date(2020,11, 2),date(2020,11, 3),date(2020,11, 4),date(2020,11, 5),\
                           date(2020,11, 6),date(2020,11, 7),date(2020,11, 8),date(2020,11, 9),date(2020,11,10),\
                           date(2020,11,11),date(2020,11,12),date(2020,11,13),date(2020,11,14),date(2020,11,15),\
                           date(2020,11,16),date(2020,11,17),date(2020,11,18),date(2020,11,19),date(2020,11,20),\
                           date(2020,11,21),date(2020,11,22),date(2020,11,23),date(2020,11,24),date(2020,11,25),\
                           date(2020,11,26),date(2020,11,27),date(2020,11,28),date(2020,11,29),date(2020,11,30),\
                           date(2020,12, 1),date(2020,12, 2),date(2020,12, 3),date(2020,12, 4),date(2020,12, 5),\
                           date(2020,12, 6),date(2020,12, 7),date(2020,12, 8),date(2020,12, 9),date(2020,12,10),\
                           date(2020,12,11),date(2020,12,12),date(2020,12,13),date(2020,12,14),date(2020,12,15),\
                           date(2020,12,16),date(2020,12,17),date(2020,12,18),date(2020,12,19),date(2020,12,20),\
                           date(2020,12,21),date(2020,12,22),date(2020,12,23),date(2020,12,24),date(2020,12,25),\
                           date(2020,12,26),date(2020,12,27),date(2020,12,28),date(2020,12,29),date(2020,12,30),\
                           date(2020,12,31)]
mars_tran_t2            = [25.3753,25.2917,25.2078,25.1231,25.0381,24.9528,24.8669,24.7808,24.6947,24.6081,24.5214,24.4347,24.3478,24.2611,24.1742,24.0875,24.0011]
mars_tran_d2            = [date(2020,10, 1),date(2020,10, 2),date(2020,10, 3),date(2020,10, 4),date(2020,10, 5),\
                           date(2020,10, 6),date(2020,10, 7),date(2020,10, 8),date(2020,10, 9),date(2020,10,10),\
                           date(2020,10,11),date(2020,10,12),date(2020,10,13),date(2020,10,14),date(2020,10,15),\
                           date(2020,10,16),date(2020,10,17)]

#plot
fig, ax1 = plt.subplots(figsize=(2.51032*1.215*2,4.54653*1.215*2))
fig.set_facecolor((3/255,0/255,45/255))
ax1.set_facecolor((31/255,27/255,79/255))

sun_color       = [254/255,215/255,0/255]
mars_color      = [237/255,31/255,36/255]

Asunset1,       = ax1.plot(sun_set_t1,sun_set_d1, color=sun_color,linestyle='--',linewidth=1,zorder=2.5)

for slc in unlink_wrap(mars_rise_t1, [17,24]):
    Amarsrise1,     = ax1.plot(mars_rise_t1[slc],mars_rise_d1[slc], color=mars_color,linestyle='-',linewidth=1,zorder=3)
for slc in unlink_wrap(mars_set_t1, [17,24]):
    Amarsset1,      = ax1.plot(mars_set_t1[slc],mars_set_d1[slc], color=mars_color,linestyle='--',linewidth=1,zorder=3)
for slc in unlink_wrap(mars_tran_t1, [17,24]):
    Amarstran1,     = ax1.plot(mars_tran_t1[slc],mars_tran_d1[slc], color=mars_color,linestyle='-.',linewidth=1,zorder=3)

ax2 = ax1.twinx()

Asunrise2,      = ax2.plot(sun_rise_t2,sun_rise_d2, color=sun_color,linestyle='-',linewidth=1,zorder=2.5)

for slc in unlink_wrap(mars_rise_t2, [24,32]):
    Amarsrise2,     = ax2.plot(mars_rise_t2[slc],mars_rise_d2[slc], color=mars_color,linestyle='-',linewidth=1,zorder=3)
for slc in unlink_wrap(mars_set_t2, [24,32]):
    Amarsset2,      = ax2.plot(mars_set_t2[slc],mars_set_d2[slc], color=mars_color,linestyle='--',linewidth=1,zorder=3)
for slc in unlink_wrap(mars_tran_t2, [24,32]):
    Amarstran2,     = ax2.plot(mars_tran_t2[slc],mars_tran_d2[slc], color=mars_color,linestyle='-.',linewidth=1,zorder=3)

#gradient fill area
g_step = 250
for i in range(g_step):
    ax1.fill_betweenx(sun_set_d1,[x-3/g_step*i for x in sun_set_t1],[x-3/g_step*(i+1) for x in sun_set_t1],\
                      color=[250/255-(i/g_step)*(250-30)/255,250/255-(i/g_step)*(250-180)/255,100/255+(i/g_step)*(230-100)/255],zorder=1)
    ax2.fill_betweenx(sun_rise_d2,[x+3/g_step*i for x in sun_rise_t2],[x+3/g_step*(i+1) for x in sun_rise_t2],\
                      color=[250/255-(i/g_step)*(250-30)/255,250/255-(i/g_step)*(250-180)/255,100/255+(i/g_step)*(230-100)/255],zorder=1)
    print(str(i+1)+'/'+str(g_step)+' plotted')
#tune darker
ax1.fill_betweenx(sun_set_d1,sun_set_t1,17,color=[0,0,0],alpha=0.25,zorder=1.5)
ax2.fill_betweenx(sun_rise_d2,sun_rise_t2,32,color=[0,0,0],alpha=0.25,zorder=1.5)

#brightest 13/10
e_sunset    = min(sun_set, key=lambda x: x[1]) # minmax only read [0], shift it to [1] https://dbader.org/blog/python-min-max-and-nested-lists

ax1.annotate('全年最早日落 '+ e_sunset[0].strftime('%d/%m ') + common_time(e_sunset[1]),\
             (0.125,0),xycoords=('axes fraction','figure fraction'),\
             xytext=(0,30),textcoords='offset points',\
             ha='center',va='bottom', fontproperties=chara_chi_6,color='white')
ax2.scatter(24.3478,date(2020,10,13), marker='1', color=sun_color, zorder=5)

#axis setting
ax1.set_xlim((17,32))
ax1.set_ylim((str(w_year)+'/12/31',str(w_year)+'/01/01'))
ax2.set_ylim((str(w_year+1)+'/01/01',str(w_year)+'/01/02'))

ax1.yaxis.tick_left()
ax1.yaxis.set_major_locator(matplotlib.dates.MonthLocator(bymonth=range(1,13), bymonthday=1, interval=1))
ax1.set_yticklabels([])
ax1.yaxis.set_minor_locator(matplotlib.dates.DayLocator(bymonthday=range(1,32), interval=1))
ax1.tick_params(which='both',color='white',labelcolor='white',width=0.25)
ax1.tick_params(which='major',length=6.5)

ax2.yaxis.tick_right()
ax2.yaxis.set_major_locator(matplotlib.dates.MonthLocator(bymonth=range(1,13), bymonthday=1, interval=1))
ax2.set_yticklabels([])
ax2.yaxis.set_minor_locator(matplotlib.dates.DayLocator(bymonthday=range(1,32), interval=1))
ax2.tick_params(which='both',color='white',labelcolor='white',width=0.25)
ax2.tick_params(which='major',length=6.5)

#gridlines
matplotlib.rcParams['lines.dotted_pattern'] = [4, 8]
ax1.xaxis.grid(which='major', linestyle='dotted',linewidth=0.25)
ax1.xaxis.set_ticks_position('none') 
ax1.set_xticklabels(['','18','20','22','24','02','04','06'], fontsize=15, color='white')

for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(0.25)
    ax1.spines[axis].set_color('white')
    ax2.spines[axis].set_linewidth(0.25)
    ax2.spines[axis].set_color('white')
 
for DM in [str(w_year)+'/02/01',str(w_year)+'/03/01',str(w_year)+'/04/01',str(w_year)+'/05/01',str(w_year)+'/06/01',\
           str(w_year)+'/07/01',str(w_year)+'/08/01',str(w_year)+'/09/01',str(w_year)+'/10/01',str(w_year)+'/11/01',str(w_year)+'/12/01']:
    ax1.hlines(DM, 17, 24, colors='grey', linewidth=0.25, zorder=2)
    ax2.hlines(DM, 24, 32, colors='grey', linewidth=0.25, zorder=2)
    for DT in [19,21,23]:
        ax1.vlines(DT, str(datetime.strptime(DM,'%Y/%m/%d').date()+timedelta(days=1)),\
                   str(datetime.strptime(DM,'%Y/%m/%d').date()-timedelta(days=1)), colors='grey', linewidth=0.25, zorder=2)
        ax1.vlines(DT, str(w_year)+'/01/01',str(w_year)+'/01/03', colors='grey', linewidth=0.25, zorder=2)
        ax1.vlines(DT, str(w_year)+'/12/29',str(w_year)+'/12/31', colors='grey', linewidth=0.25, zorder=2)
    for DT in [25,27,29,31]:
        ax2.vlines(DT, str(datetime.strptime(DM,'%Y/%m/%d').date()+timedelta(days=1)),\
                   str(datetime.strptime(DM,'%Y/%m/%d').date()-timedelta(days=1)), colors='grey', linewidth=0.25, zorder=2)
        ax2.vlines(DT, str(w_year)+'/01/02',str(w_year)+'/01/04', colors='grey', linewidth=0.25, zorder=2)
        ax2.vlines(DT, str(w_year)+'/12/30',str(w_year+1)+'/01/01', colors='grey', linewidth=0.25, zorder=2)

#ax1.legend([Asunrise2,Asunset1,Amarsrise2,Amarsset1],['sunrise','sunset','marsrise','marsset'])

#Y-label
month_lab_E = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
month_lab_C = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']

ax1.annotate('十二月',(17,(ax1.yaxis.get_minorticklocs()[-1]+ax1.yaxis.get_majorticklocs()[11])/2),\
             xytext=(-20,0),textcoords='offset points',fontproperties=chara_chi_15,\
             ha='center',va='center', rotation=270,color='white')
ax2.annotate('JAN',(32,(ax2.yaxis.get_minorticklocs()[0]+ax2.yaxis.get_majorticklocs()[0])/2),\
             xytext=(20,0),textcoords='offset points',fontproperties=chara_eng_15,\
             ha='center',va='center', rotation=90,color='white')

for i in range(11):
    ax1.annotate(month_lab_C[i],(17,(ax1.yaxis.get_majorticklocs()[i]+ax1.yaxis.get_majorticklocs()[i+1])/2),\
                 xytext=(-20,0),textcoords='offset points',fontproperties=chara_chi_15,\
                 ha='center',va='center', rotation=270,color='white')
for i in range(11):
    ax2.annotate(month_lab_E[i+1],(32,(ax2.yaxis.get_majorticklocs()[i]+ax2.yaxis.get_majorticklocs()[i+1])/2),\
                 xytext=(20,0),textcoords='offset points',fontproperties=chara_eng_15,\
                 ha='center',va='center', rotation=90,color='white')

#header
logo = plt.text(0, 1.01, 'LOGO\nHERE', color='white', size=14,\
                ha='left',ma='right',va='bottom', transform=ax1.transAxes, bbox=dict(pad=0,alpha=0.5))

title = plt.text(1.0, 1.05668919, str(w_year)+'年香港日月行星出沒時間表',fontproperties=chara_chi_22,\
         color='white', ha='right',va='top', transform=ax1.transAxes, bbox=dict(pad=0,alpha=0))

def latlon(x):
    return str(x).split(':')[0]+'$\degree$'+str(x).split(':')[1]+"'"

site = plt.text(0.14135201, 1.01, '東經'+Obs[5].split(':')[0]+r'$\degree$'+Obs[5].split(':')[1]+'\''+\
                ' 北緯'+Obs[3].split(':')[0]+r'$\degree$'+Obs[3].split(':')[1]+'\''+' UTC+8.0',\
                fontproperties=chara_chi_6, color='white', ha='left', va='bottom',\
                transform=ax1.transAxes, bbox=dict(pad=0,alpha=0))

web = plt.text(0.85, 1.01, 'http://www.hokoon.edu.hk/',\
               fontproperties=chara_chi_6, color='white', ha='right', va='bottom',\
               transform=ax1.transAxes, bbox=dict(pad=0,alpha=0))

##fig.patches.extend([plt.Rectangle((0,1.01),0.25142,0.20608,color='g', alpha=0.5, zorder=1000,\
##                                  transform=ax1.transAxes)])

#footer

end = time.time()
print(str(round(end-start,2))+'s of your life is wasted.')

#plt.tight_layout()
plt.show()

#bbox properties can only be retrived after draw()
print(title.get_bbox_patch())
print(site.get_bbox_patch())
print(ax1.transAxes.inverted().transform(title.get_bbox_patch().get_extents()))
print(ax1.transAxes.inverted().transform(logo.get_bbox_patch().get_extents()))

