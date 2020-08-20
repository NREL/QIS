# Keysight 81150A Pulse Function Arbitrary Generator
# instrument website:
# https://www.keysight.com/main/techSupport.jspx?cc=US&lc=eng&nid=-536902255.748669&pid=1287544&pageMode=PL# Manual:
# download manual and page 340 provide the code
# https://pyvisa.readthedocs.io/en/latest/

import pyvisa
import time
import matplotlib.pylab as plt
import numpy as np


def AWG(period1, period2, pulse1, pulse2, gap, uwpulse):
    rm = pyvisa.ResourceManager()
    # rm = pyvisa.ResourceManager('C:/windows/system32/visa64.dll')
    print(rm.list_resources())
    print(rm)    #visa location
    exit()
    # inst=rm.open_resource('GPIB0::28::INSTR')                         #GBIP cable, Rohde&Schwarz
    # inst = rm.open_resource('USB0::0x0AAD::0x0054::181799::INSTR')    #USB-B cable, Rohde&Schwarz
    # inst = rm.open_resource('GPIB0::7::INSTR')                        #GBIP cable, Agilent infiniium scope
    inst = rm.open_resource('USB0::0x0957::0x4108::MY53821982::INSTR')  #USB-B cable, Keysight 81150A Pulse Function Arbitrary Generator
    print(inst)

    #trigger
    inst.write(':ARM:SOUR2 EXT')  # INT2 INT  EXT MAN
    inst.write(':ARM:SOUR1 EXT')

    # channel 1 double pulse for laser
    inst.write(':PULS:PER ' + str(period1) + 'US')
    x = inst.query(':APPL?')  # The function, frequency, amplitude, and offset are returned
    print(x)

    wave = [-8192] * period1
    for i in range(pulse1):
        wave[i] = 8192
    for i in range(pulse1 + gap, pulse1 + gap + pulse2):
        wave[i] = 8192
    temp = str(wave)
    temp = temp.replace('[', '')
    waveform = temp.replace(']', '')
    inst.write(":DATA:DAC VOLATILE," + waveform)

    #channel 2 single pulse for uW
    inst.write(':PULS:PER2 '+str(period2)+'US')
    inst.write(':PULS:DEL2 '+ str(pulse1+gap-uwpulse)+'US')    # delay: second S, microsecond US, nanosecond NS
    inst.write(':PULS:WIDT2 '+str(uwpulse) +'US')    # width

    inst.write(':OUT1')
    inst.write(':OUT2')



if __name__ == "__main__":
    #parameters
    period1 = 1000  # us channel 1
    period2 = 1000  # us channel 2
    pulse1 = 3  # us width
    pulse2 = 3  # us width
    gap = 450    # us delay between two pulses
    uwpulse = 25  # us uW pulse length

    AWG(period1, period2, pulse1, pulse2, gap, uwpulse)


    #more sample code:
    # inst.write(':FREQuency 1kHz')
    # inst.write(':APPL2:SQU 10kHz')   #SQU, SIN, RAMP, NOIS, DC, PULS
    # inst.write(':FUNC2:PULS:DCYC 20PCT')  #duty cycle
    # inst.write(':FUNC2 PULS')
    # inst.write(':PULS:FREQ2 1kHz')



