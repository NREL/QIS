# coding= latin-1

from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
import PyDAQmx as nidaq
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import concurrent.futures

#for uW source
start=2820      #MHz
end=2920        #MHz
step=0.5          #MHz
dwelltime=1000   #ms how long
point=int((end-start)/step)
mag=np.arange(start, end,step)
print(len(mag))
print (point)
# sw=end-start              #sweep width, GHz
scannum =1          #number of scan, make sure same as E500
filename = 'ys20032305'
wait = 10           #time to wait to start next scan
dt=point*dwelltime/1000
# print(dt)
dt=int(dt)
print("data acquisition time: ", dt,'s')   #has to be integer
# exit()

#for pulse
period=1.  #pulse period,s
duty_cycle=0.5  #pulse length
#for APD photodetector
rate = 1000 #fluorescence data rate, samples/s
num = dt*rate       #total sample acquired  #must be int
time.sleep(2)

def a():
    print(time.time())
    t = nidaq.Task()
    t.CreateCOPulseChanFreq("Dev1/ctr0", "", nidaq.DAQmx_Val_Hz, nidaq.DAQmx_Val_Low, 0.0, 1 / float(period), duty_cycle)
    t.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
    t.StartTask()
    print("snake")
    # a = input("Generating pulse train. Press Enter to interrupt\n")
    # t.StopTask()
    # t.ClearTask()

def b():
    print(time.time())
    t = nidaq.Task()
    t.CreateAIVoltageChan("Dev1/ai1", None, nidaq.DAQmx_Val_RSE, 0, 10, nidaq.DAQmx_Val_Volts, None)
    t.CfgSampClkTiming("", rate, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, num)
    t.StartTask()

    data = np.zeros((num,), dtype=np.float64)
    read = nidaq.int32()
    t.ReadAnalogF64(num, dt, nidaq.DAQmx_Val_GroupByChannel,
                    data, len(data), nidaq.byref(read), None)

    # np.savetxt("foo1.csv", data, delimiter=",")
    print("bear")
    t.StopTask()
    t.ClearTask()
    return data

if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(a)
        bb=executor.submit(b)
        amp = np.array(bb.result())
    print('Scan #', 1, ' is done.')
    np.savetxt(filename+".csv", amp, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals


    if scannum > 1:
        for i in range(scannum - 1):
            time.sleep(wait)  # reset a new cycle
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(a)
                bb = executor.submit(b)
                data = np.array(bb.result())
                amp = amp + data
            print('Scan #', i + 2, ' is done.')
            np.savetxt(filename + str(i+2) +".csv", amp, delimiter=",", fmt="%f6")  # save fluorescence signal,6 decimals

    # amp = np.genfromtxt(filename + '.csv', delimiter=',')
    # amp[0] = amp[1]

    flu=[]   #averaged fluorense intensity
    n=0
    a= rate*dwelltime/1000  #every frequency position on uW source has data on USB6211
    a=int(a)
    for i in range (point):
        d = np.mean(amp[n:n+a])
        n = n + a
        flu.append(d)

    # flu.append(d)
    print(len(flu))

    plt.plot(mag,flu)
    plt.title('fluorescence signal '+filename)
    plt.xlabel('Microwave Frequency, MHz')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()





