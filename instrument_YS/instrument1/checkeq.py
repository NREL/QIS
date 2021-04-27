import socket
import pyvisa
import time
import seabreeze
from seabreeze.spectrometers import Spectrometer


def checkvisa():
    rm = pyvisa.ResourceManager()
    equipment = rm.list_resources()
    # rm = pyvisa.ResourceManager('C:/windows/system32/visa64.dll')
    # print(equipment)
    # print(len(equipment))
    # exit()
    eqlist = ',\n\n'.join(equipment)
    eqnum = len(equipment)

    k = seabreeze.spectrometers.list_devices()

    if len(k) != 0:
        eqlist = eqlist + ',\n\n' + str(k[0])
        eqnum +=1

    return eqlist, eqnum


def checkip():
    TCP_IP = '192.168.0.10'
    TCP_PORT = 10001
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((TCP_IP, TCP_PORT))     ##old method, took>1min to time out

    try:
        socket.create_connection((TCP_IP, TCP_PORT), 5)  #only try 5s time out
        return "power suppy", 1
    except:
        return "", 0

if __name__ == "__main__":
    # a, b = checkvisa()
    # print(a)
    # print(b)

    c = checkip()
    print(c[1])



# USB0::0x0AAD::0x0054::181799::INSTR,      #USB-B cable, Rohde&Schwarz
# USB0::0x0957::0x4108::MY53821982::INSTR,  #USB-B cable, Keysight 81150A Pulse Function Arbitrary Generator
# ASRL6::INSTR,                             ##RS232 cable, Tektronix Signal generator
# GPIB0::23::INSTR,                         ##GBIP cable, Stanford research photon counter
# GPIB1::9::INSTR,                          ##GBIP cable, Stanford research lock-in amplifier
# <SeaBreezeDevice USB2000PLUS:FLMS15575>   ##spectrometer

# GPIB0::28::INSTR                          #GBIP cable, Rohde&Schwarz
# GPIB0::7::INSTR                           #GBIP cable, Agilent infiniium scope




