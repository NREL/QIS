#Stanford Instrument gated photon counter
# https://pyvisa.readthedocs.io/en/latest/

import pyvisa
import time
import matplotlib.pylab as plt
import SignalGen

def phtoncounter(period_cnt, pulse1, pulse2, gap, uwpulse, gate,cycle):
    rm = pyvisa.ResourceManager()
    # rm = pyvisa.ResourceManager('C:/windows/system32/visa64.dll')
    # print(rm.list_resources())
    # print(rm)  #visa location
    # exit()
    inst=rm.open_resource('GPIB0::23::INSTR')   ## photon counter
    # print(inst)

    # The parameter i is 0,1,or 2 to select counter A,B, or T
    if (set):
        # print('set parameters')

        if period_cnt==1000:  #us
            TSET='9E3'
        elif period_cnt==100:
            TSET='9E2'
        elif period_cnt==10:
            TSET='9E1'
        elif period_cnt==1000000:
            TSET='9E6'


        # mode
        # ('CI i,j Set counter i to input j; 10 MHz(0), INP 1(1), INP 2(2), TRIG(3).')
        # inst.write('CI 2,3')          #Set T to trigger
        inst.write('CI 2,0')            # T=10 MHz
        inst.write('CP 2,'+TSET)          # Set T SET to 9x10^-7 sec, for trigger period of 1us
        inst.write('NP ' + str(cycle))  # Set number of periods, [1, 2000]
        # AT N = STOP DWELL = EXTERNAL
        # NE j Set end of scan mode to mode j; START(1) or STOP (0).
        inst.write('NE 0')
        inst.write('DT 0')  # Set dwell time to 6sec, external (0)

        # Gate
        k = inst.write('GM 0,1')  # Set GATE i to mode j; CW(0), FIXED(1), or SCAN(2).
        k = inst.write('GD 0,' + str(pulse1 + gap) + 'E-6')  # Set GATE i DELAY to sec
        k = inst.write('GW 0,' + str(gate) + 'E-6')  # Set GATE i width to sec

        # Level
        k = inst.write('DS 0,0')  # Set A DISC slope=rise
        k = inst.write('DL 0,300E-3')  # Set A DISC LVL=+..mV

        # STORE / RECALL
        k = inst.write('ST 1')  # Store instrument settings to location 1-9
        # k=inst.write('RC 1')  #Recall instrument settings
        # k=inst.write('RC 0')  #Recall default settings

    inst.write('GD 0,' + str(pulse1 + gap) + 'E-6')  # Set GATE i DELAY to sec
    inst.write('CR')  # stop, reset

    # read from buffer
    time.sleep(2)           #wait until buffer finish, otherwise may return -1
    data = [None] * cycle
    total = 0
    for i in range(cycle):
        k = inst.query('QA ' + str(i + 1))
        data[i] = int(k)
        total = total + int(k)

    print(data)
    # print(len(data))
    print(total)
    return (total)

# def RS(freq):
#     rm = pyvisa.ResourceManager()
#     inst1 = rm.open_resource('USB0::0x0AAD::0x0054::181799::INSTR')    #USB-B cable
#     inst1.write('FREQ '+str(freq)+' MHz')   ##'SOUR1: FREQ 2.8 GHz' SOUR can be omitted


if __name__ == "__main__":

    freq = 2825  #center is 2875
    level = 12  #dBm
    SignalGen.Freqset(freq)

    set=1  #set parameters
    period_cnt = 1000  # us this word reserved for photoncounter
    pulse1 = 3     # us width
    pulse2 = 3     # us width
    gap = 450      # us delay between two pulses
    uwpulse = 25     # us uW pulse length
    gate=0.8         # us photon counter A gate
    cycle = 200    # measurement repetition  2000, 20min
    phtoncounter(period_cnt, pulse1, pulse2, gap, uwpulse, gate,cycle)
    exit()

    x=[None]*101
    for i in range (101):
        RS(freq+i)
        print(freq+i)
        x[i]=phtoncounter(period_cnt, pulse1, pulse2, gap, uwpulse, gate, cycle)

    print(x)
    plt.plot(x)
    plt.xlabel('Frequency, MHz')
    plt.ylabel('Signal Amplitude, AU')
    plt.title('ODMR ')
    plt.show()

    #more codes:
    # k=inst.write('CH')     #pause
    # k=inst.write('CR')     #stop, reset
    # k=inst.write('CS')     #start

    # k=inst.query('QA')     #works, string
    # k = inst.query('QA 120')  #works, string. If data is not ready, the QA and QB commands return -1.
    # k=inst.query_ascii_values('QA')   #works, string, .0
    # print(int(k))
    # k=inst.query('FA')   #start scan and send current period count)
    # print(k)
