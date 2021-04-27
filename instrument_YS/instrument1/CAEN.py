# CAEN els power supply
import pyvisa
import time
import matplotlib.pylab as plt
import numpy as np
import socket
import Tektronix

def opencaen():
    TCP_IP = '192.168.0.10'
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # print("ethernet connected")
    s.send('MON\r'.encode()) # Send command to turn on

def closecaen():
    TCP_IP = '192.168.0.10'
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('MOFF\r'.encode())

def modeCC():
    closecaen()
    TCP_IP = '192.168.0.10'
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('LOOP:I\r'.encode())

def modeCV():
    closecaen()
    TCP_IP = '192.168.0.10'
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('LOOP:V\r'.encode())

def sendI(I):
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(('MWI:' + str(I) + '\r').encode())  # Send current setting
    s.close()  # close socket

    #AWG
    # s.send('WAVEFORM:N_PERIODS:5\r'.encode())
    # s.send('WAVEFORM:POINTS: 1, 0.5, 1\r'.encode())


def sendV(V):
    modeCV()
    opencaen()
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(('MWV:' + str(V) + '\r').encode())

def AWGcaen():
    pass


def sweepI(I1, I2, istep, avg, filename, folder, dualchannel):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('GPIB1::9::INSTR')  #SR830 lock-in amplifier
    current = np.arange(I1, I2+istep, istep)
    # print(current)
    flu = []
    t1 = time.time()

    for i in current:
        print(i)
        sendI(i)
        time.sleep(1)
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
    print("time is: ", t2 - t1)

    if not folder:
        filename = folder + '/' + filename

    np.savetxt(filename+ ".csv", flu, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
    # print((len(flu)))
    plt.plot(current, flu)
    plt.title('EPR Spectrum, '+filename)
    plt.xlabel('Current, A')
    plt.ylabel('Fluorescence intensity, AU')
    plt.show()


def sweepB(CC, B1, B2, Bstep, avg, filename, folder, dualchannel):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('GPIB1::9::INSTR')  #SR830 lock-in amplifier
    Blist = np.arange(B1, B2+istep, Bstep)
    flu = []
    t1 = time.time()

    for B in Blist:
        i = round(B/CC, 4)
        print(i)
        sendI(i)
        time.sleep(1)

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
    print("time is: ", t2 - t1)

    if not folder:
        filename = folder + '/' + filename

    np.savetxt(filename+ ".csv", flu, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
    # print((len(flu)))
    plt.plot(Blist, flu)
    plt.title('EPR Spectrum, '+filename)
    plt.xlabel('Field, G')
    plt.ylabel('Fluorescence intensity, AU')
    plt.show()


if __name__ == "__main__":
    I = 3
    # V=1
    # sendI(I)
    # sendV(V)
    opencaen()
    # closecaen()
    exit()

    # freq = 2914  # MHz  3A high
    freq = 2890  # MHz 1A low
    Tektronix.tekf(freq)
    avg = 5
    folder = ''
    filename = 'ys21030318'
    dualchannel = 1  # 1 double channel, 0 single channel

    I1 = 0
    I2 = 2
    istep = 0.01     #A
    sweepI(I1, I2, istep, avg, filename, folder, dualchannel)

    B1 = 0
    B2 = 30
    Bstep = 0.1
    CC = 13          #coil constant
    sweepB(CC, B1, B2, Bstep, avg, filename, folder, dualchannel)















