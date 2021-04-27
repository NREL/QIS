#Tektronix 6GHz RF source
import pyvisa
import time
import matplotlib.pylab as plt
import numpy as np


def tekf(freq):
    rm = pyvisa.ResourceManager()
    inst=rm.open_resource('ASRL6::INSTR')                         #RS232 cable, tektronix
    inst.write('FREQ ' + str(freq) + ' MHz')

def tekp(power):
    rm = pyvisa.ResourceManager()
    inst=rm.open_resource('ASRL6::INSTR')                         #RS232 cable, tektronix
    inst.write('AMPR ' + str(power))  #default to dBm

if __name__ == "__main__":
    t1 = time.time()
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('GPIB1::9::INSTR')  #SR830 lock-in amplifier
    start = 2700  # MHz
    end = 3000  # MHz
    step = 1  # MHz
    dualchannel = 1  #1: dual channels; 0: one channel
    # point = int((end - start) / step)
    # print(point)
    mag = np.arange(start, end+step, step)
    print(len(mag))

    flu = []
    avg = 5
    filename = 'ys21042045'
    folder = 'testdata'
    if folder:
        filename = folder + '\n'+filename
    tekp(-30)
    # tekf(2700)
    # exit()

    for i in mag:
        if i%10 == 0:
            print(i)

        tekf(i)
        x1 = []
        y1 = []
        for j in range (avg):
            k = inst.query('OUTP? 1')
            x1.append(float(k)*1000)
            if dualchannel:
                k = inst.query('OUTP? 2')
                y1.append(float(k)*1000)

        x = np.mean(x1)
        if dualchannel:
            y = np.mean(y1)
            flu.append(-(x ** 2 + y ** 2) ** 0.5)
        else:
            flu.append(x)

    t2 = time.time()
    print("time is: ", t2 - t1)  # 124s, 69s

    np.savetxt(filename+".csv", flu, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
    print((len(flu)))
    plt.plot(mag, flu)
    plt.title('ODMR Spectrum, NV diamond '+filename)
    plt.xlabel('Microwave Frequency, MHz')
    plt.ylabel('Fluorescence Signal Amplitude, AU')
    plt.show()





