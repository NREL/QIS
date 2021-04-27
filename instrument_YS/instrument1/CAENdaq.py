# CAEN els power supply, use DAQ to record data

import pyvisa
import time
import matplotlib.pylab as plt
import numpy as np
import PyDAQmx as nidaq
import socket
import Tektronix

def opencaen():
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    # print("ethernet connected")
    s.send('MON\r'.encode()) # Send command to turn on

def closecaen():
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('MOFF\r'.encode())

def modeCC():
    closecaen()
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('LOOP:I\r'.encode())

def modeCV():
    closecaen()
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send('LOOP:V\r'.encode())

def sendI(I):  # center field, coil constant
    # modeCC()
    # opencaen()
    # Open and Configure Socket
    TCP_IP = '192.168.0.10'  #CAEN power supply
    TCP_PORT = 10001
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    # Send Parameters
    # data = s.recv(BUFFER_SIZE)
    # s.send('MON\r'.encode()) # Send command to turn on
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
    # s. send('MON\r'.encode())  # Send command to turn on
    s.send(('MWV:' + str(V) + '\r').encode())
    # s.close()  # close socket

def AWGcaen():
    pass


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    # inst = rm.open_resource('GPIB1::9::INSTR')  #SR830 lock-in amplifier
    # # rm = pyvisa.ResourceManager('C:/windows/system32/visa64.dll')
    # print(rm.list_resources())
    # print(rm)    #visa location
    # exit()

    t1 = time.time()
    # field = 10
    # cc = 13
    # I = field/cc
    I = 3
    # V=1
    # sendI(I)
    # sendV(V)
    # opencaen()
    closecaen()
    exit()

    # freq = 2914  # MHz  3A high
    freq = 2890  # MHz 1A low
    # Tektronix.tekt(freq)
    I1 = 0
    I2 = 2
    istep = 0.01  #A
    current = np.arange(I1, I2+istep, istep)
    # print(current)
    # exit()
    flu = []
    avg = 1
    filename = 'ys21030319'
    rate = 1000
    num = 1000
    dt =1

    for i in current:
        print(i)
        sendI(i)
        time.sleep(1)

        t = nidaq.Task()
        t.CreateAIVoltageChan("Dev1/ai1", None, nidaq.DAQmx_Val_RSE, 0, 10, nidaq.DAQmx_Val_Volts, None)
        t.CfgSampClkTiming("", rate, nidaq.DAQmx_Val_Rising, nidaq.DAQmx_Val_FiniteSamps, num)
        t.StartTask()

        time.sleep(1)  # read from buffer, otherwise data not available error
        data = np.zeros((num,), dtype=np.float64)
        read = nidaq.int32()
        t.ReadAnalogF64(num, dt, nidaq.DAQmx_Val_GroupByChannel, data, len(data), nidaq.byref(read), None)
        # print("bear")
        t.StopTask()
        t.ClearTask()

        flu.append(np.mean(data))


    t2 = time.time()
    print("time is: ", t2 - t1)

    np.savetxt(filename+".csv", flu, delimiter=",", fmt="%f6")  #save fluorescence signal,6 decimals
    print((len(flu)))
    plt.plot(current, flu)
    plt.title('fluorescence signal, 2.89GHz '+filename)
    plt.xlabel('Current, A')
    plt.ylabel('Signal Amplitude, AU')
    plt.show()













