#Stanford Instrument gated photon counter
# https://pyvisa.readthedocs.io/en/latest/

import pyvisa
import time
import matplotlib.pylab as plt
import SignalGen
import PhotonCnt


if __name__ == "__main__":
    folder = '/Users/yshi2/Documents/2020.8.14/'
    filename = 'test'
    # freq = 2875  # MHz
    level = 12   # dBm
    start = 2820 # MHz
    stop = 2920  # MHz
    step = 1     # MHz
    # dwell = 500  # ms

    set=1  #set parameters
    period_cnt = 1000  # us this word reserved for photoncounter
    pulse1 = 3     # us width
    pulse2 = 3     # us width
    gap = 450      # us delay between two pulses
    uwpulse = 25     # us uW pulse length
    gate=0.8         # us photon counter A gate
    cycle = 200    # measurement repetition  2000, 20min

    freq = np.arange(start,stop+step,step)
    y=[]
    for i in freq:
        SignalGen.Freqset(i)
        print(i)
        y.append(PhotonCnt.Photoncounter(period_cnt, pulse1, pulse2, gap, uwpulse, gate, cycle))

    print(y)
    np.savetxt(folder + filename + ".csv", a, delimiter=",", fmt='%f')
    plt.plot(freq, y)
    plt.xlabel('Frequency, MHz')
    plt.ylabel('Signal Amplitude, AU')
    plt.title('ODMR ')
    plt.show()
