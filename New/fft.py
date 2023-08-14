from scipy.fft import rfft, rfftfreq
from scipy.interpolate import interp1d
import numpy
import matplotlib.pyplot as plt
import pandas
import pathlib

#Data320 = pandas.read_excel(pathlib.Path.cwd().joinpath('hokoon','20200320-170354_TPI-PROJ01-AZEL_02#_01#_t1.xlsx'))
#Data424 = pandas.read_excel(pathlib.Path.cwd().joinpath('hokoon','20200424-135611_TPI-PROJ01-AZEL_01#_01#_t1.xlsx'))
#Data427 = pandas.read_excel(pathlib.Path.cwd().joinpath('hokoon','20200427-103039_TPI-PROJ01-AZEL_01#_01#_t1.xlsx'))
Data428 = pandas.read_excel(pathlib.Path.cwd().joinpath('hokoon','20200428-084209_TPI-PROJ01-AZEL_02#_01#_t1.xlsx'))

#select data
Data = Data428 #<--input
JD_data = 2458967.5 #<--input
filename = '20200428-084209_TPI-PROJ01-AZEL_02#_01#_t1' #<--input

x = (Data.JD-JD_data)*24*3600
y = Data.u11

#interpolation function
f = interp1d(x,y,'nearest')

#evenly-spaced data, must do before FFT
x_even = numpy.linspace((Data.JD.iat[0]-JD_data)*24*3600, (Data.JD.iat[-1]-JD_data)*24*3600, len(Data.JD))
y_even = f(x_even)

#FFT
start = 14500 #FFT of selected section only #<--input
N = len(Data.JD)
end = 21000 #<--input
T = (Data.JD.iat[-1]-Data.JD.iat[0])*24*3600/N #time step
yf = rfft(y_even[start:end]) #drop imaginary part
xf = rfftfreq(len(y_even[start:end]), T)

#plots
fig = plt.figure(figsize=[14,8])
grid = plt.GridSpec(3,3)

ax0 = plt.subplot(grid[0,0])
ax0.plot((x_even-(Data.JD.iat[0]-JD_data)*24*3600)/60,y_even)
ax0.set_xticks(numpy.arange(0, 100, 1), minor=True)
ax0.set_xlim(start*T/60,end*T/60)
ax0.set_title('raw data zoom in', fontweight="bold")
ax0.set_xlabel('time (min)')
ax0.grid(which='both')

ax1 = plt.subplot(grid[0,1:])
ax1.plot((x_even-(Data.JD.iat[0]-JD_data)*24*3600)/60,y_even)
p1 = plt.Rectangle((start*T/60, 0), (end-start)*T/60, ax1.get_ylim()[1], facecolor="g", fill=True, alpha=0.5, zorder=3)
ax1.add_patch(p1)
ax1.set_title('raw data '+str(filename), fontweight="bold")
ax1.set_xlabel('time (min)')
ax1.grid()

ax2 = fig.add_subplot(grid[1,0:])
ax2.plot(xf[1:],numpy.abs(yf[1:]))
ax2.set_xlim(0,0.02)
ax2.set_title('FFT of zoomed region in frequency', fontweight="bold")
ax2.set_xlabel('frequency (Hz)')
ax2.grid()

ax3 = fig.add_subplot(grid[2,0:])
ax3.plot(1/xf[1:]/60,numpy.abs(yf[1:]))
ax3.set_xticks(numpy.arange(0, 20, 1))
ax3.set_xticks(numpy.arange(0, 20, 1/6), minor=True)
ax3.set_xlim(0,10)
ax3.set_title('FFT of zoomed region in period', fontweight="bold")
ax3.set_xlabel('period (min)')
ax3.grid(which='both')

fig.tight_layout()
plt.show()
