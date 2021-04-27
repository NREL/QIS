# https://pythonhosted.org/PyDAQmx/
# https://www.pythonforthelab.com/blog/controlling-a-national-instruments-card-with-python/
# https://pythonhosted.org/PyDAQmx/callback.html

# from PyDAQmx.DAQmxFunctions import *
# from PyDAQmx.DAQmxConstants import *
import PyDAQmx as nidaq
import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import concurrent.futures

#pinhole
#trigger: 6, ground: 5
#channel1: 17, channel2: 19, ground: 28

def singletrigger(freq_NI, delay, duty_cycle):
    print(time.time())
    t = nidaq.Task()
    t.CreateCOPulseChanFreq("Dev1/ctr0", "", nidaq.DAQmx_Val_Hz, nidaq.DAQmx_Val_High, delay, freq_NI, duty_cycle)#delay,f, duty cycle
    # below 1 lines for trigger USB6211, in pinhole 1(PFI0), 11(D GND)
    # t.CfgDigEdgeStartTrig("/Dev1/PFI0",nidaq.DAQmx_Val_Rising)
    # t.CfgSampClkTiming("/Dev1/PFI0", 10000, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_ContSamps, 1000)  #error
    t.CfgImplicitTiming(nidaq.DAQmx_Val_ContSamps, 1000)
    t.StartTask()
    # print("snake")
    # a = input("Generating printulse train. Press Enter to interrupt\n")

def continuetrigger(freq_NI, delay, duty_cycle):
    t = nidaq.Task()
    t.CreateCOPulseChanFreq("Dev1/ctr0", "", nidaq.DAQmx_Val_Hz, nidaq.DAQmx_Val_High, delay, freq_NI, duty_cycle)#delay,f, duty cycle
    # below 1 lines for trigger USB6211, in pinhole 1(PFI0), 11(D GND)
    # t.CfgDigEdgeStartTrig("/Dev1/PFI0",nidaq.DAQmx_Val_Rising)
    # t.CfgSampClkTiming("/Dev1/PFI0", 10000, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_ContSamps, 1000)  #error
    t.CfgImplicitTiming(nidaq.DAQmx_Val_ContSamps, 1000)
    t.StartTask()
    print("snake")
    a = input("Generating pulse train. Press Enter to interrupt\n")

def recorddata(rate, num):
    print(time.time())
    t = nidaq.Task()
    t.CreateAIVoltageChan("Dev1/ai1", None, nidaq.DAQmx_Val_RSE, 0, 10, nidaq.DAQmx_Val_Volts, None)
    t.CfgSampClkTiming("", rate, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, num)
    t.StartTask()

    data = np.zeros((num,), dtype=np.float64)
    read = nidaq.int32()
    t.ReadAnalogF64(num, dt, nidaq.DAQmx_Val_GroupByChannel, data, len(data), nidaq.byref(read), None)

    # np.savetxt("foo1.csv", data, delimiter=",")
    print("bear")
    raw_input('Acquiring samples continuously. Press Enter to interrupt\n')
    t.StopTask()
    t.ClearTask()
    return data

if __name__ == "__main__":

    freq_NI = 200  # 1000 is T=1ms  #0.5 is T=2s 50Hz is 20ms  #Hz, try to give integer
    # period=10e-6  #pulse period,s
    # freq=float(1/period)  #not accurate, try to use above line
    duty_cycle = 0.1  # pulse length, %
    delay = 0  # s
    rate = 5000  #sampling rate, sample/s
    num = 5000   #number of samples

    # singletrigger(freq_NI, delay, duty_cycle)
    continuetrigger(freq_NI, delay, duty_cycle)
    # recorddata(rate, num)



