import time
from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import collections as mc
import pylab as pl
import pandas
import numpy
import math
import ephem
from datetime import date, datetime
from matplotlib.figure import Figure
import pathlib
from PIL import Image
import itertools

#####################################
# location information
#exo
exo = ephem.Observer()
exo.lon = str(114+10/60+27.6/3600)
exo.lat = str(-(17+15/60+49/3600))

Obs = exo #<= set your observatory
Obs.date = '2019/06/03 22:00:00'
#####################################

fig, ax0 = plt.subplots(figsize=(7.2,4.8), facecolor='black')
fig.subplots_adjust(0,0,1,1)
ax0.set_facecolor('black')
ax0.set_aspect('equal')
ax0.set_xlim((-350,350))
ax0.set_ylim((-350,350))

zenith_shift_ra     = 0
zenith_shift_dec    = 0
rotate_angle        = 0
aspect_ratio        = 1 #y/x
plot_scale          = 150
x_shift             = 0
y_shift             = 0

plot_alpha          = 0.5

horizon = [0] * 361
horizon = pandas.DataFrame(columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
equator = [0] * 361
equator = pandas.DataFrame(columns=['RA','Dec','x','y']).apply(pandas.to_numeric)
ecliptic = [0] * 361
ecliptic = pandas.DataFrame(columns=['RA','Dec','x','y']).apply(pandas.to_numeric)

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

Sun         = ephem.Sun()
Sun.compute(Obs)
Moon        = ephem.Moon()
Moon.compute(Obs)
Mercury     = ephem.Mercury()
Mercury.compute(Obs)
Venus       = ephem.Venus()
Venus.compute(Obs)
Mars        = ephem.Mars()
Mars.compute(Obs)
Jupiter     = ephem.Jupiter()
Jupiter.compute(Obs)
Io          = ephem.Io()
Io.compute(Obs)
Europa      = ephem.Europa()
Europa.compute(Obs)
Ganymede    = ephem.Ganymede()
Ganymede.compute(Obs)
Callisto    = ephem.Callisto()
Callisto.compute(Obs)
Saturn      = ephem.Saturn()
Saturn.compute(Obs)  
Uranus      = ephem.Uranus()
Uranus.compute(Obs)
Neptune     = ephem.Neptune()
Neptune.compute(Obs)

    
ra0 = math.degrees(Obs.sidereal_time()) + zenith_shift_ra
dec0 = math.degrees(Obs.lat) + zenith_shift_dec

# projection formula (Lambert Azimuthal Equal-Area with rotation)  # for Moonglow ASC
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

# projection formula (Stereographic)  # plot_scale ~ 130
transform_x = lambda x,y: plot_scale\
              *(-2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
              *math.cos(math.radians(y))*math.sin(math.radians(x-ra0))
transform_y = lambda x,y: aspect_ratio*plot_scale\
              *(2/(1+math.sin(math.radians(dec0))*math.sin(math.radians(y))+math.cos(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0))))\
              *(math.cos(math.radians(dec0))*math.sin(math.radians(y))-math.sin(math.radians(dec0))*math.cos(math.radians(y))*math.cos(math.radians(x-ra0)))

# horizon
for i in range(361):
    horizon.loc[i] = [i,math.degrees(math.atan(-math.cos(math.radians(ra0-i))/math.tan(math.radians(dec0)))),0,0]

horizon.x = list(map(transform_x, horizon.RA, horizon.Dec))
horizon.y = list(map(transform_y, horizon.RA, horizon.Dec))

for i in range(len(horizon)-1):
    plt.plot([horizon.x[i],horizon.x[i+1]],[horizon.y[i],horizon.y[i+1]],'g-',zorder=1)

# horizon size
hori_border = max(horizon.x)-min(horizon.x)

# equator
for i in range(361):
    equator.loc[i] = [i,0,0,0]

equator.x = list(map(transform_x, equator.RA, equator.Dec))
equator.y = list(map(transform_y, equator.RA, equator.Dec))

for i in range(len(equator)-1):
    plt.plot([equator.x[i],equator.x[i+1]],[equator.y[i],equator.y[i+1]],'r--',alpha=plot_alpha,zorder=1)

# ecliptic
epsilon_J2000 = 23.4392911
for i in range(361):
    ecliptic.loc[i] = [math.degrees(math.atan2(math.sin(math.radians(i))*math.cos(math.radians(epsilon_J2000)),math.cos(math.radians(i)))),\
                       math.degrees(math.asin(math.sin(math.radians(epsilon_J2000))*math.sin(math.radians(i)))),0,0]

ecliptic.x = list(map(transform_x, ecliptic.RA, ecliptic.Dec))
ecliptic.y = list(map(transform_y, ecliptic.RA, ecliptic.Dec))

for i in range(len(ecliptic)-1):
    plt.plot([ecliptic.x[i],ecliptic.x[i+1]],[ecliptic.y[i],ecliptic.y[i+1]],'y--',alpha=plot_alpha+0.1,zorder=1)
 
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

ax0.annotate('$\u263C$',(Sun_x+2.5,Sun_y+1),color=solar_color[0])
ax0.annotate('$\u263D$',(Moon_x+2.5,Moon_y+1),color=solar_color[1])
ax0.annotate('$\u263F$',(Mercury_x+2.5,Mercury_y+1),color=solar_color[2])
ax0.annotate('$\u2640$',(Venus_x+2.5,Venus_y+1),color=solar_color[3])
ax0.annotate('$\u2642$',(Mars_x+2.5,Mars_y+1),color=solar_color[4])
ax0.annotate('$\u2643$',(Jupiter_x+2.5,Jupiter_y+1),color=solar_color[5])
ax0.annotate('$\u2644$',(Saturn_x+2.5,Saturn_y+1),color=solar_color[6])
ax0.annotate('$\u2645$',(Uranus_x+2.5,Uranus_y+1),color=solar_color[7])
ax0.annotate('$\u2646$',(Neptune_x+2.5,Neptune_y+1),color=solar_color[8])

    
constellation_list = [And,Ant,Aps,Aqr,Aql,Ara,Ari,Aur,Boo,Cae,Cam,Cnc,CVn,CMa,CMi,Cap,Car,Cas,Cen,Cep,\
                      Cet,Cha,Cir,Col,Com,CrA,CrB,Crv,Crt,Cru,Cyg,Del,Dor,Dra,Equ,Eri,For,Gem,Gru,Her,\
                      Hor,Hya,Hyi,Ind,Lac,Leo,LMi,Lep,Lib,Lup,Lyn,Lyr,Men,Mic,Mon,Mus,Nor,Oct,Oph,Ori,\
                      Pav,Peg,Per,Phe,Pic,Psc,PsA,Pup,Pyx,Ret,Sge,Sgr,Sco,Scl,Sct,Ser,Sex,Tau,Tel,Tri,\
                      TrA,Tuc,UMa,UMi,Vel,Vir,Vol,Vul]

for df in constellation_list:
    df.x = list(map(transform_x, df.RA, df.Dec))
    df.y = list(map(transform_y, df.RA, df.Dec))

labelxy = 2

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

for x,y,z in constellation_star:
    plt.scatter(x,y, s=15*(10**(-0.4*z))**0.5, c='white', alpha=plot_alpha, zorder=2)

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
                      constellation_line[i][1][constellation_line[i][2][j][0]]-constellation_line[i][1][constellation_line[i][2][j][1]]) < hori_border/2:
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
constellation_dotted_line = [[(Aur.x[3],Aur.y[3]),(Tau.x[1],Tau.y[1])],[(Aur.x[2],Aur.y[2]),(Tau.x[1],Tau.y[1])],\
                             [(Peg.x[1],Peg.y[1]),(And.x[0],And.y[0])],[(Peg.x[3],Peg.y[3]),(And.x[0],And.y[0])],\
                             [(Ser.x[3],Ser.y[3]),(Oph.x[7],Oph.y[7])],[(Ser.x[2],Ser.y[2]),(Oph.x[3],Oph.y[3])],\
                             [(PsA.x[0],PsA.y[0]),(Aqr.x[18],Aqr.y[18])]]

constellation_dotted_line_list = []
for i in range(len(constellation_dotted_line)):
    if math.hypot(constellation_dotted_line[i][0][0]-constellation_dotted_line[i][1][0],\
                  constellation_dotted_line[i][0][1]-constellation_dotted_line[i][1][1]) < hori_border/2:
        constellation_dotted_line_list.append(constellation_dotted_line[i])

lc_west_dotted = mc.LineCollection(constellation_dotted_line_list, colors='white', linestyles='dashed',zorder=10+2.5)
lc_west_dotted.set_alpha(plot_alpha)
ax0.add_collection(lc_west_dotted)

# annotation
for x,y,z,n in constellation_line:
    if math.hypot(numpy.mean(x)-x_shift,numpy.mean(y)-y_shift) \
       < math.sqrt(((hori_border/2)**2)-(1-aspect_ratio**2)*((numpy.mean(y)-y_shift)/aspect_ratio)**2) \
       and max(x)-min(x) < hori_border:
        if n in set(['$\u2652$','$\u2648$','$\u264B$','$\u2651$','$\u264A$','$\u264C$','$\u264E$','$\u2653$','$\u2650$','$\u264F$','$\u2649$','$\u264D$']):
            ax0.annotate(str(n),(numpy.mean(x),numpy.mean(y)-labelxy),color='y')
        else:
            ax0.annotate(str(n),(numpy.mean(x),numpy.mean(y)-labelxy),color='w')

# milkyway
MW_list = [MW_southernedge,MW_MonPer,MW_CamCas,MW_Cep,MW_CygOph,MW_OphSco,MW_LupVel,MW_VelMon,\
           dark_PerCas,dark_CasCep,dark_betaCas,dark_CygCep,dark_CygOph,dark_thetaOph,dark_lambdaSco,dark_ScoNor,dark_Coalsack,dark_Vel,\
           MW_LMC1,MW_LMC2,MW_SMC]

MW_line_list = []
for df in MW_list:
    df.x = list(map(transform_x, df.RA, df.Dec))
    df.y = list(map(transform_y, df.RA, df.Dec))
    for i in range(len(df)-1):
        MW_line_list.append([(df.x[i],df.y[i]),(df.x[i+1],df.y[i+1])])

lc_MW = mc.LineCollection(MW_line_list, colors='b',alpha=plot_alpha, zorder=1+2.5)
ax0.add_collection(lc_MW)

plt.show()

