from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
import PyDAQmx as nidaq
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import os
import concurrent.futures
from seabreeze.spectrometers import Spectrometer

style.use('fivethirtyeight')

#for uW source
start=2820      #MHz
end=2920        #MHz
step=0.5          #MHz
dwelltime=1000   #ms how long
point=int((end-start)/step)   #points on uW source
mag=np.arange(start, end,step)
# sw=end-start              #sweep width, MHz
print(len(mag))
print (point)
scannum = 1          #number of scan, make sure same as E500
filename = 'ys20032316'
wait = 5           #time to wait to start next scan, more time for long sweep/go to low field
dt=point*dwelltime/1000
# print(dt)
dt=int(dt)
print("data acquisition time: ", dt,'s')   #has to be integer
# exit()

# for pulse
period = 1.  # pulse period,s
duty_cycle = 0.5  # pulse length

#ocean view setup
# ingt = 1000000   # integration time, micro sec, same as dwell time
ingt = dwelltime*1000
# wavelength = [635,645]  #the region of wavelength you want to accumulate
wavelength = [550,800]
spec = Spectrometer.from_first_available()
spec.integration_time_micros(ingt)
x = spec.wavelengths()
y = spec.intensities()
x = x[30:]   #delete the first pseudo peak
y = y[30:]
plt.plot(x,y)
plt.title('Flame-S \n close this plot to start experiment')
plt.xlabel('Wavelength, nm')
plt.ylabel('Signal Amplitude, AU')
plt.show()
if y.max() > 65500:
    print("Flame is saturated, please reduce integration time")
    exit()
# exit()

step = abs(x[1] - x[0])
p = np.where(abs(x-wavelength[0])<step)[0][0]   #index of wavelength region
q = np.where(abs(x-wavelength[1])<step)[0][0]
# print(p, q)

def a():
    print(time.time())
    t = nidaq.Task()
    t.CreateCOPulseChanFreq("Dev1/ctr0", "", nidaq.DAQmx_Val_Hz, nidaq.DAQmx_Val_Low, 0.0, 1 / float(period), duty_cycle)
    t.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
    t.StartTask()
    print("snake")

def b():
    t1 = time.time()
    print(t1)
    amp = []

    def flame():
        # print(time.time())
        spec.integration_time_micros(ingt)
        y = spec.intensities()
        sumamp= y[p:q].sum()
        amp.append(sumamp)
        # with open(filename+'.txt', 'a') as f:      #use txt
        #     f.write(str(sumamp) + ',' + '\n')

    # while True:
    #     flame()
    #     t2=time.time()
    #     if round(t2,1) == round(t1,1)+dt:
    #         print(t2)
    #         print('bear')
    #         break
    # return amp

    for i in range(point):
        flame()
    return amp

if __name__ == "__main__":
    # if os.path.isfile(filename+'.txt'):    #use txt
    #     os.remove(filename+'.txt')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(a)
        bb = executor.submit(b)
        amp = bb.result()
        amp=np.array(amp)
    print('Scan #', 1, ' is done.')
    np.savetxt(filename+'.csv', amp, delimiter=",", fmt="%f6")  #6 decimals

    if scannum >1:
        for i in range(scannum-1):
            time.sleep(5)   #reset a new cycle
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(a)
                bb=executor.submit(b)
                data = bb.result()
                data = np.array(data)
                amp = amp + data
            print('Scan #',i+2,' is done.')
            np.savetxt(filename+'.csv', amp, delimiter=",", fmt="%f6")  #6 decimals

    print("OOflame sample taken: ", len(amp))   #fairly accurate

    plt.plot(mag, amp)
    plt.title('Flame-S '+filename)
    plt.xlabel('Magnetic Field, G')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()






