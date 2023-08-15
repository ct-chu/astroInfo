import time
start = time.time()

import matplotlib
import matplotlib.pyplot as plt
import numpy
import math
from matplotlib.figure import Figure
from matplotlib import collections as mc
import pathlib
from PIL import Image

import ephem
import pandas

#####################################
# location information
#Hokoon
hokoon = ephem.Observer()
hokoon.lon = str(114+6/60+29/3600)
hokoon.lat = str(22+23/60+1/3600)

Obs = hokoon #<= set your observatory
Obs.date = '2017/09/21 21:00:01'
#####################################
# plot parameters
image_size = 1.6
fig, ax = plt.subplots(figsize=(image_size*7.2,image_size*4.8), facecolor='black')
fig.subplots_adjust(0,0,1,1,0,0)

##zenith_shift_ra     = -2.0
##zenith_shift_dec    = -1.5
##rotate_angle        = -2.0
##aspect_ratio        = 0.90 #y/x
##plot_scale          = 175
##x_shift             = -11.5
##y_shift             = 6.0
##
##ra0 = math.degrees(Obs.sidereal_time()) + zenith_shift_ra
##dec0 = math.degrees(Obs.lat) + zenith_shift_dec
##
### projection formula (Lambert Azimuthal Equal-Area with rotation)  # for Moonglow ASC
##transform_x = lambda x,y: x_shift+plot_scale\
##              *(math.cos(math.radians(rotate_angle))\
##               *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
##               *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##               -math.sin(math.radians(rotate_angle))\
##               *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
##               *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
##transform_y = lambda x,y: y_shift+aspect_ratio*plot_scale\
##              *(math.sin(math.radians(rotate_angle))\
##               *(-math.cos(math.radians(y))*math.sin(math.radians(x-ra0)))\
##               *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
##               +math.cos(math.radians(rotate_angle))\
##               *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))\
##               *math.sqrt(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))))
##
##Aur = numpy.zeros(shape=(161,5))
##Aur = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Aur.csv'))
##Boo = numpy.zeros(shape=(154,5))
##Boo = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Boo.csv'))
##CMa = numpy.zeros(shape=(155,5))
##CMa = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CMa.csv'))
##CMi = numpy.zeros(shape=(44,5))
##CMi = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','CMi.csv'))
##Cyg = numpy.zeros(shape=(291,5))
##Cyg = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Cyg.csv'))
##Gem = numpy.zeros(shape=(123,5))
##Gem = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Gem.csv'))
##Hya = numpy.zeros(shape=(246,5))
##Hya = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Hya.csv'))
##Leo = numpy.zeros(shape=(130,5))
##Leo = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Leo.csv'))
##Lyr = numpy.zeros(shape=(83,5))
##Lyr = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Lyr.csv'))
##Ori = numpy.zeros(shape=(225,5))
##Ori = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Ori.csv'))
##PsA = numpy.zeros(shape=(49,5))
##PsA = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','PsA.csv'))
##Sgr = numpy.zeros(shape=(219,5))
##Sgr = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sgr.csv'))
##Sco = numpy.zeros(shape=(174,5))
##Sco = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Sco.csv'))
##Tau = numpy.zeros(shape=(223,5))
##Tau = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Tau.csv'))
##UMa = numpy.zeros(shape=(224,5))
##UMa = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','UMa.csv'))
##Vir = numpy.zeros(shape=(174,5))
##Vir = pandas.read_csv(pathlib.Path.cwd().joinpath('ASC','Vir.csv'))
##
##constellation_list = [Aur,Boo,CMa,CMi,Cyg,Gem,Hya,Leo,Lyr,Ori,PsA,Sgr,Sco,Tau,UMa,Vir]
##
##for df in constellation_list:
##    df.x = list(map(transform_x, df.RA, df.Dec))
##    df.y = list(map(transform_y, df.RA, df.Dec))
##
##Aur_line = [[0,1],[0,3],[0,4],[1,2],[4,5],[4,7]]
##Boo_line = [[0,1],[0,2],[0,6],[0,11],[2,4],[3,5],[3,6],[4,5]]
##CMa_line = [[0,3],[0,6],[0,12],[0,13],[1,7],[2,6],[2,7],[2,8],[4,8],[12,13]]
##CMi_line = [[0,1]]
##Cyg_line = [[0,1],[1,2],[1,3],[1,11],[2,5],[3,9],[4,11],[8,9]]
##Gem_line = [[0,8],[1,12],[3,5],[3,6],[4,5],[7,10],[8,10],[8,12],[9,13],[11,13]]
##Hya_line = [[0,11],[0,12],[1,4],[1,14],[2,5],[2,9],[3,6],[3,8],[4,18],[5,13],[5,17],[6,14],[7,8],[7,12],[9,11],\
##            [13,19],[15,17],[15,19]]
##Leo_line = [[0,5],[0,7],[0,8],[0,10],[1,2],[1,5],[2,17],[3,6],[3,8],[3,17],[4,11],[5,12],[6,11]]
##Lyr_line = [[0,6],[0,12],[1,2],[1,4],[2,6],[4,6],[6,12]]
##Ori_line = [[0,5],[0,6],[1,4],[1,10],[1,17],[2,6],[2,10],[2,34],[3,4],[3,6],[4,5],[8,12],[8,21],[12,13],[13,26],\
##            [17,27],[21,34],[23,24],[23,33],[24,27],[27,33]]
##PsA_line = [[0,1],[0,2],[1,13],[2,5],[3,5],[3,7],[4,7],[4,13]]
##Sgr_line = [[0,2],[0,3],[0,6],[0,7],[1,8],[1,9],[1,11],[2,8],[2,9],[3,4],[3,6],[3,8],[4,8],[4,12],[5,11],\
##            [5,36],[6,20],[9,23],[10,11],[13,24],[13,36],[14,16],[16,17],[16,18],[18,22],[22,27],[23,27]]
##Sco_line = [[0,8],[0,10],[1,5],[2,11],[2,14],[3,8],[3,12],[4,6],[4,9],[4,10],[14,16],[5,7],[5,11],[9,17],[12,16]]
##Tau_line = [[0,3],[0,4],[1,6],[4,9],[5,9],[5,11],[6,12],[7,11],[9,12]]
##UMa_line = [[0,3],[0,10],[1,4],[1,10],[1,15],[2,3],[4,5],[4,17],[5,10],[5,16],[6,7],[6,12],[6,16],[8,9],[9,14],\
##            [9,17],[11,15],[11,17]]
##Vir_line = [[0,2],[0,13],[0,15],[1,3],[2,3],[2,14],[3,5],[4,9],[4,10],[5,9],[5,15],[7,14],[8,11],[10,18],[11,13],\
##            [12,18]]
##    
##constellation_line = [[Aur.x,Aur.y,Aur_line],[Boo.x,Boo.y,Boo_line],[CMa.x,CMa.y,CMa_line],[CMi.x,CMi.y,CMi_line],\
##                      [Cyg.x,Cyg.y,Cyg_line],[Gem.x,Gem.y,Gem_line],[Hya.x,Hya.y,Hya_line],[Leo.x,Leo.y,Leo_line],\
##                      [Lyr.x,Lyr.y,Lyr_line],[Ori.x,Ori.y,Ori_line],[PsA.x,PsA.y,PsA_line],[Sgr.x,Sgr.y,Sgr_line],\
##                      [Sco.x,Sco.y,Sco_line],[Tau.x,Tau.y,Tau_line],[UMa.x,UMa.y,UMa_line],[Vir.x,Vir.y,Vir_line]]
##
### constellation linecollection
##constellation_line_xy1 = [] # (x,y) pair of vertics 1
##constellation_line_xy2 = [] # (x,y) pair of vertics 2
##
##for i in range(len(constellation_line)):
##    for j in range(len(constellation_line[i][2])):
##        constellation_line_xy1.append([(constellation_line[i][0][constellation_line[i][2][j][0]]),(constellation_line[i][1][constellation_line[i][2][j][0]])])
##        constellation_line_xy2.append([(constellation_line[i][0][constellation_line[i][2][j][1]]),(constellation_line[i][1][constellation_line[i][2][j][1]])])
##
##constellation_line_list = zip(constellation_line_xy1,constellation_line_xy2)
##
##lc_west = mc.LineCollection(constellation_line_list, colors='yellow', alpha=0.25, zorder=10+2.5)
##ax.add_collection(lc_west)
        
def cursor_info():
    global asc
    #asc[y,x]
    #asc x count from left to right [0,719]
    #asc y count from top to bottom [0,479]
    #pixel data are int8, avoid over 256
    numpy.seterr(divide='ignore', invalid='ignore') #ignore /0 or nan error
    ax.format_coord = lambda x,y : "x=%.3f y=%.3f [%03d %03d %03d] S=%.3f B/R=%.3f" \
                       % (x, y, asc[int(y+.5),int(-x+.5),0], asc[int(y+.5),int(-x+.5),1], asc[int(y+.5),int(-x+.5),2], \
                          1-min(asc[int(y+.5),int(x+.5),0], asc[int(y+.5),int(x+.5),1], asc[int(y+.5),int(x+.5),2])/\
                          (asc[int(y+.5),int(x+.5),0]/3+asc[int(y+.5),int(x+.5),1]/3+asc[int(y+.5),int(x+.5),2]/3), \
                          (asc[int(y+.5),int(x+.5),2]/2-asc[int(y+.5),int(x+.5),0]/2)/(asc[int(y+.5),int(x+.5),2]/2+asc[int(y+.5),int(x+.5),0]/2))

#asc = plt.imread('W:\Thomas\ASIM\Hokoon_ASIM_2019_01_30-02_00_47.png')
#asc = plt.imread(r'C:\Users\Thomas\Dropbox\Hokoon_ASIM.png')
asc = plt.imread(r'C:\Users\Thomas\Dropbox\ASIM\hkneac_asc (5).jpg')

asc_HSV = matplotlib.colors.rgb_to_hsv(asc)

R_stat = asc[:,:,0].reshape(720*480)
G_stat = asc[:,:,1].reshape(720*480)
B_stat = asc[:,:,2].reshape(720*480)
H_stat = asc_HSV[:,:,0].reshape(720*480)
S_stat = asc_HSV[:,:,1].reshape(720*480)
V_stat = asc_HSV[:,:,2].reshape(720*480)

BR_stat = (B_stat/256-R_stat/256)/(B_stat/256+R_stat/256+0.0000000000000000001) # avoid divide 0

V_sc = -6.28*R_stat+0.454*G_stat-4.11*B_stat-1.81*S_stat+8.88*V_stat+1.53*BR_stat+0.586 #https://www.jstage.jst.go.jp/article/sola/13/0/13_2017-043/_pdf
#plt.hist([V_sc],bins=255)

#plt.hist([R_stat,G_stat,B_stat],bins=255,stacked=True,color=['r','g','b'])
#plt.hist([H_stat,S_stat,V_stat],bins=255,stacked=True,color=['r','g','b'])

print(sum(i < 0 for i in V_sc)*100/len(V_sc)) # now without mask

ax.imshow(asc, extent=[-360, 360, -240, 240])
#ax.set_xlim((-360,360))
#ax.set_ylim((-240,240))

#cursor_info()

plt.show()
