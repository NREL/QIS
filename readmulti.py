
import os
import numpy as np
import scipy as sp
import matplotlib.pylab as plt
import csv
import math
import cmath
import struct
import numpy.matlib

if __name__ == '__main__':

    start = 6000  # MHz
    end = 12000  # MHz
    # step = 1  # MHz   dwell=100ms
    step=0.01
    freq = np.arange(start, end, step)
    print(len(freq))

    filename='res1_6to12GHz'
    file = open(filename+'.csv', 'r')  ##400730 pts
    flu = []
    for line in file.readlines():
        fname = line.split(',')  # , \t
        flu.append(fname)

    n = len(flu)
    print(n)
    # print(flu)
    for k in range(n):
        flu[k] = float(flu[k][0])
    for k in range(n):
        if flu[k]<0:
            flu[k]=flu[k-1]
    res1=flu
    # plt.plot(res1)
    # plt.show()
    # exit()

    filename='res2_6to12GHz'
    file = open(filename+'.csv', 'r')  ##400730 pts
    flu = []
    for line in file.readlines():
        fname = line.split(',')  # , \t
        flu.append(fname)

    n = len(flu)
    print(n)
    # print(flu)
    for k in range(n):
        flu[k] = float(flu[k][0])
    for k in range(n):
        if flu[k]<0:
            flu[k]=flu[k-1]
    res2=flu
    # plt.plot(res2)
    # plt.show()
    # exit()

    filename='res3_6to12GHz'
    file = open(filename+'.csv', 'r')  ##400730 pts
    flu = []
    for line in file.readlines():
        fname = line.split(',')  # , \t
        flu.append(fname)

    n = len(flu)
    print(n)
    # print(flu)
    for k in range(n):
        flu[k] = float(flu[k][0])
    for k in range(n):
        if flu[k]<0:
            flu[k]=flu[k-1]
    res3=flu
    print(len(res3))
    # plt.plot(res3)
    # plt.show()
    # exit()


    # print(flu)
    plt.plot(freq,res1,freq,res2,freq, res3)
    plt.xlabel('Frequency, MHz')
    plt.ylabel('Voltage, V')
    plt.title('Resonator 1, 2, 3 ')
    plt.legend(['resonator1', 'resonator2', 'resonator3'])
    plt.show()