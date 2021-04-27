# Agilent infiniium scope
# Export data using GPIB cable
# Write down time resolution, us/div, Or check the saved csv file

import pyvisa
# from pyvisa.constants import StopBits, Parity
import time
import matplotlib.pylab as plt
import numpy as np

def InfiniiumScope(channel, tb, folder, filename, title):
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    # print(rm)
    inst = rm.open_resource('GPIB1::7::INSTR')  ##GBIP, Agilent infiniium scope, 1GBIP cable,0; 2 GBIP cables,1
    # print(inst)

    y = inst.query(":WAVEFORM:PREAMBLE?")
    print("data", y)  # format, type,
    print("# points: " + y[4:11])
    print("x time base, s: " + y[13:28])
    # print("counts (averages): " + y[3])

    inst.write(":WAVeform:SOURce CHANnel"+str(channel))
    # inst.write(":ACQuire:COUNt 10")
    x = inst.query(":WAV:DATA?")  ##only reads 1 channel

    fn = filename
    if folder:
        filename = folder + '/' + filename

    with open(filename + ".txt", "w") as txt_file:
        for line in x:
            txt_file.write(" ".join(line))  # space doesn't matter, use + "\n"

    flu = np.genfromtxt(filename + '.txt', delimiter=',')  #, fmt='%f'
    pts = len(flu)
    axis_x = np.linspace(0, tb * pts - tb, pts)

    plt.plot(axis_x, flu)
    plt.xlabel('Time, ns')
    plt.ylabel('Signal Amplitude, AU')
    plt.title(title + ' Channel ' + str(channel) + ',' + fn)
    plt.show()


def scopeplot(tb, folder, filename, title):
    fn = filename
    if folder:
        filename = folder + '/' + filename

    flu = np.genfromtxt(filename + '.txt', delimiter=',')  #, fmt='%f'
    pts = len(flu)
    axis_x = np.linspace(0, tb * pts - tb, pts)

    plt.plot(axis_x, flu)
    plt.xlabel('Time, ns')
    plt.ylabel('Signal Amplitude, AU')
    plt.title(title + ', ' + fn)
    plt.show()


if __name__ == "__main__":
    folder = '/Users/yshi2/Documents/2020.8.20'
    # folder = ''   #current folder
    filename = 'ys20082014'
    title = 'Infiniium Oscilloscope Ouput'
    channel = 4
    tb = 1000 #ns time base
    # InfiniiumScope(channel, tb, folder, filename, title)
    scopeplot(tb, folder, filename, title)



##  ":WAVEFORM:PREAMBLE?" return:
# FORMAT        : int16 - 0 = BYTE, 1 = WORD, 2 = ASCII.
# TYPE          : int16 - 0 = NORMAL, 1 = PEAK DETECT, 2 = AVERAGE
# POINTS        : int32 - number of data points transferred.
# COUNT         : int32 - 1 and is always 1.
# XINCREMENT    : float64 - time difference between data points.
# XORIGIN       : float64 - always the first data point in memory.
# XREFERENCE    : int32 - specifies the data point associated with XORIGIN
# YINCREMENT    : float32 - voltage diff between data points.
# YORIGIN       : float32 - value is the voltage at center screen.
# YREFERENCE    : int32 - specifies the data point where y-origin occurs



   # file = open(folder + filename + ".txt", 'r')  ##400730 pts
    # for line in file.readlines():
    #     fname = line.split(',')  # , \t
    # n = len(fname)  ## n=200 3336, 80 1336, 801457, 400730 same as saved csv on scope, but need to write down points and x-axis
    # print("# points: ", n)
    # flu = [None] * n
    # for k in range(n):
    #     flu[k] = float(fname[k])
