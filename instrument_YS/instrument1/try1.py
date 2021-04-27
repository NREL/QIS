
import pyvisa
import time
import matplotlib.pylab as plt
import numpy as np
import seabreeze
from seabreeze.spectrometers import Spectrometer


def checkeq(friend = 'snake'):
    print(friend, 'and crocodile')




if __name__ == "__main__":
    # f = 'bear'
    # checkeq(f)


    # def is_interface_up(interface):
    #     addr = netifaces.ifaddresses(interface)
    #     return netifaces.AF_INET in addr
    #
    #
    # interface = '192.168.0.10'
    # print(is_interface_up(interface))

    # start = 2700  # MHz   1A
    # stop = 3000  # MHz
    # step = 1  # MHz
    # point = int((stop - start) / step)
    # x = np.arange(start, stop, step)
    # print(x)

    # I1=2
    # I2=4
    # current = np.linspace(I1, I2, 21)
    # print( current)

    a=[[1,2], [3,4], [5, 6]]
    print(len(a))

    # start = 2700  # MHz
    # end = 3000  # MHz
    # step = 1  # MHz
    # # point = int((end - start) / step)
    # # print(point)
    # mag = np.arange(start, end+step, step)
    # print(mag)
    # print(len(mag))

    # try:
    #     f = open('/Users/yshi2/Desktop/UI/par/par0.txt', "r")
    #     temp = f.read().splitlines()
    #     print(temp[2])
    # except:
    #     f = open('/Users/yshi2/Desktop/UI/par/par0.txt', "r")
    #     temp = f.read().splitlines()
    #     print(len(temp))
    #     print("load previous parameters fail; load default values.")



    pts = int(abs(2 - 4) / 0.1) + 1
    current = np.linspace(2, 4, pts)
    print(current)

    a = decimal.Decimal('56.9554362669143476');
    print(a)



# rm = pyvisa.ResourceManager('C:/windows/system32/visa64.dll')
# print(rm.list_resources())
# print(rm)    #visa location

# USB0::0x0AAD::0x0054::181799::INSTR,      #USB-B cable, Rohde&Schwarz
# USB0::0x0957::0x4108::MY53821982::INSTR,  #USB-B cable, Keysight 81150A Pulse Function Arbitrary Generator
# ASRL6::INSTR,                             ##RS232 cable, Tektronix
# GPIB0::23::INSTR,                         ##GBIP cable, Stanford research photon counter
# GPIB1::9::INSTR,                          ##GBIP cable, Stanford research lock-in amplifier
# <SeaBreezeDevice USB2000PLUS:FLMS15575>   ##spectrometer

# GPIB0::28::INSTR                          #GBIP cable, Rohde&Schwarz
# GPIB0::7::INSTR                           #GBIP cable, Agilent infiniium scope




