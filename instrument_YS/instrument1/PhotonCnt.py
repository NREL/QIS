# Stanford Instrument gated photon counter
import pyvisa
import time
import matplotlib.pylab as plt
import SignalGenRS
import AWG
import numpy as np
import math


def Photoncounter(period_cnt, TSET, pulse1, pulse2, gap, uwpulse, gate, cycle):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('GPIB0::23::INSTR')  ## photon counter
    # print(inst)
    # exit()

    # The parameter i is 0,1,or 2 to select counter A,B, or T
    #
    #     if period_cnt==1000:  #us
    #         TSET='9E3'
    #     elif period_cnt==100:
    #         TSET='9E2'
    #     elif period_cnt==10:
    #         TSET='9E1'
    #     elif period_cnt==1000000:
    #         TSET='9E6'

    # mode
    # ('CI i,j Set counter i to input j; 10 MHz(0), INP 1(1), INP 2(2), TRIG(3).')
    # inst.write('CI 2,3')          #Set T to trigger
    inst.write('CI 2,0')  # T=10 MHz
    inst.write('CP 2,' + TSET)  # Set T SET to 9x10^-7 sec, for trigger period of 1us
    inst.write('NP ' + str(cycle))  # Set number of periods, [1, 2000]
    # AT N = STOP DWELL = EXTERNAL
    # NE j Set end of scan mode to mode j; START(1) or STOP (0).
    inst.write('NE 0')
    inst.write('DT 0')  # Set dwell time to 6sec, external (0)

    # Gate
    k = inst.write('GM 0,1')  # Set GATE i to mode j; CW(0), FIXED(1), or SCAN(2).
    k = inst.write('GD 0,' + str(pulse1 + gap ) + 'E-6')  # Set GATE i DELAY to sec
    # k = inst.write('GM 0,2')  # Set GATE i to mode j; CW(0), FIXED(1), or SCAN(2)
    # k = inst.write('GY 0,5E-3') #GY i,t Set GATE i DELAY scan step to 0 <= t <= 99.92E-3 s.
    k = inst.write('GW 0,' + str(gate) + 'E-6')  # Set GATE i width to sec

    # Level
    k = inst.write('DS 0,0')  # Set A DISC slope=rise
    k = inst.write('DL 0,300E-3')  # Set A DISC LVL=+..mV

    # STORE / RECALL
    # k = inst.write('ST 1')  # Store instrument settings to location 1-9
    # k=inst.write('RC 1')  #Recall instrument settings
    # k=inst.write('RC 0')  #Recall default settings

    inst.write('CR')  # stop, reset

    # read from buffer
    tt = math.ceil(period_cnt*cycle/1000000)
    time.sleep(tt)  # wait until buffer finish, otherwise may return -1.  2 is not enough
    data = [None] * cycle
    total = 0
    for i in range(cycle):
        k = inst.query('QA ' + str(i + 1))
        data[i] = int(k)
        total = total + int(k)

    return total


if __name__ == "__main__":
    t1 = time.time()
    freq = 2870  # center is 2866 2875  2879 2855
    level = -11  #15  # dBm
    # SignalGen.Freqset(freq, level)

    period_cnt = 1000  # us counting period
    TSET = '9E3'  # x10^-7
    pulse1 = 30  # us laser width
    pulse2 = 2  # us laser width
    gaps =[50]  # us delay between two laser pulses
    uws = [50]  # us uW pulse length
    gate = 0.9
    # us photon counter A gate
    cycle = 2000  # measurement repetition  2000

    period1 = 5000  # us channel 1
    period2 = 5000  # us channel 2

    # gaps = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800]
    # gaps = [200, 250, 300, 350, 400, 500, 550, 600, 650, 700]
    gaps = np.arange(50, 650, 50)
    print(gaps)

    scan = 1   #repeat measurements
    div = 1  # total is *2000; 100 need 962.27s=16min, 10.82s/each
    for i in range (scan):
    # uws = np.arange(40, 520, 20)
    # uws = uws * 0.001
    # print(uws)
    # for uwpulse in uws:
        # print(uwpulse)
        uwpulse = uws[0]
        for gap in gaps:
            # print("gap is: " + str(gap))
            AWG.AWG1ch(period1, period2, pulse1, pulse2, gap, uwpulse)
            N = 0
            for j in range(div):
                # print (j)
                N += Photoncounter(period_cnt, TSET, pulse1, pulse2, gap, uwpulse, gate, cycle)
            print(N)
            time.sleep(1)
        print('\nscan #', i + 1, 'done\n')

    t2 = time.time()
    print("time is: ", t2 - t1)

    # more codes:
    # k=inst.write('CH')     #pause
    # k=inst.write('CR')     #stop, reset
    # k=inst.write('CS')     #start

    # k=inst.query('QA')     #works, string
    # k = inst.query('QA 120')  #works, string. If data is not ready, the QA and QB commands return -1.
    # k=inst.query_ascii_values('QA')   #works, string, .0
    # print(int(k))
    # k=inst.query('FA')   #start scan and send current period count)
    # print(k)
