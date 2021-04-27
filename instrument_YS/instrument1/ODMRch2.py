from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
import PyDAQmx as nidaq
import numpy as np
import matplotlib.pylab as plt
import time
import concurrent.futures
import SignalGenRS


def ODMR(start, stop, step, dwelltime, rate, scannum, period, duty_cycle, filename, folder, title, ch2):
    point = int((stop - start) / step)
    x = np.arange(start, stop, step)
    # print(len(x))
    # print(point)

    dt = int(point * dwelltime / 1000)
    print("data acquisition time/scan: ", dt, 's')  # has to be integer
    num = dt * rate  # total sample acquired  #must be int

    def a():  #send trigger
        print(time.time())
        t = nidaq.Task()
        t.CreateCOPulseChanFreq("Dev1/ctr0", "", nidaq.DAQmx_Val_Hz, nidaq.DAQmx_Val_Low, 0.0, 1 / float(period),
                                duty_cycle)
        t.CfgImplicitTiming(DAQmx_Val_ContSamps, 1000)
        t.StartTask()
        print("trigger sent")

    def b(): #start data acquisition
        print(time.time())
        t = nidaq.Task()
        t.CreateAIVoltageChan("Dev1/ai1, Dev1/ai2", None, nidaq.DAQmx_Val_RSE, 0, 10, nidaq.DAQmx_Val_Volts, None)
        t.CfgSampClkTiming("", rate, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, num)
        t.StartTask()

        time.sleep(1)  # read from buffer, otherwise data not available error
        data = np.zeros((num * 2,), dtype=np.float64)
        read = nidaq.int32()
        t.ReadAnalogF64(num, dt, nidaq.DAQmx_Val_GroupByChannel, data, len(data), nidaq.byref(read), None)
        # print("bear")
        t.StopTask()
        t.ClearTask()
        return data

    t1=time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(a)
        bb = executor.submit(b)
        amp = np.array(bb.result())
    time.sleep(2)
    print('Scan #', 1, ' is done.')

    if scannum > 1:
        for i in range(scannum - 1):
            time.sleep(1)  # reset a new cycle
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(a)
                bb = executor.submit(b)
                data = np.array(bb.result())
                amp = amp + data
            print('Scan #', i + 2, ' is done.')

    np.savetxt(folder + '/' + filename+".csv", amp, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
    t2=time.time()
    print('time total used, s: ', t2-t1)
    # print(len(amp))

    flu=[]   #averaged fluorense intensity
    n=0
    a= rate*dwelltime/1000  #every frequency position on uW source has data on USB6211
    a=int(a)
    for i in range (point):
        d = np.mean(amp[n:n+a])
        n = n + a
        flu.append(d)
    print('x data points: ', len(flu))

    # for double channel
    if ch2:
        for i in range(point):
            d = np.mean(amp[n:n + a])
            n = n + a
            flu[i] = -(flu[i] ** 2 + d ** 2) ** 0.5  # add y channel,however square makes positive value, invert

    plt.plot(x,flu)
    plt.title(title + ' ' + filename)
    plt.xlabel('Microwave Frequency, MHz')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()


if __name__ == "__main__":

    # for uW source
    # start = 2500  # MHz  5A
    # stop = 3200   # MHz
    # start = 2550      # MHz  10A
    # stop = 3300       # MHz
    start = 2700  # MHz   1A
    stop = 3000  # MHz
    step = 1  # MHz
    dwelltime = 100  # ms how long
    point = int((stop - start) / step)
    scannum = 1  # number of scan, make sure same as E500
    dt = int(point * dwelltime / 1000)
    print("data acquisition time/scan: ", dt, 's')  # has to be integer
    # exit()

    # for pulse
    period = 1.  # pulse period,s
    duty_cycle = 0.5  # pulse length
    # for DAQ
    rate = 5000  # fluorescence data rate, samples/s
    filename = 'ys21022301'
    folder = 'C:/Users/ODMR/Documents/Yilin/UI/temp'
    title = 'ODMR Spectrum'
    level = -11   # dBm
    ch2 = 1  #double channels

    SignalGenRS.Freqsweep(start, stop, step, dwelltime, level)
    ODMR(start, stop, step, dwelltime, rate, scannum, period, duty_cycle, filename, folder, title, ch2)






