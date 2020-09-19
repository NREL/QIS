import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import StopBits
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore
from typing import Union

#TODO:
# 1. Incorporate a "check laser status" (ideally this would live update when the settings window is open to that tab)


class TopticaInstr:
    def __init__(self):
        self.comms = None
        self.rm = pyvisa.ResourceManager()
        self.current_freq = None
        self.comm_error = None
        self.timeout = 3
        self.com_port = None

    # --------------------------------- Basic Communication Functions---------------------------------------------------
    def open(self):
        print('made it inside open')
        try:
            self.comms = self.rm.open_resource(self.com_port, baud_rate=115200, data_bits=8, stop_bits=StopBits.one)
            self.comms.write_termination = '\r\n'
            self.comm_error = None
        except pyvisa.VisaIOError:
            self.comm_error = 1
            print('Failed at open_resource (self.comm_error=1)')
            print(sys.exc_info()[:])
        return

    def close(self):
        print('Inside Close')
        if self.comms is None:
            print('self.comms was none')
            return
        else:
            self.comms.before_close()
            self.comms.close()

    def read(self):
        if self.comms is None:
            return
        else:
            self.comms.read()

    def write(self):
        if self.comms is None:
            return
        else:
            self.comms.write()

    def ask(self, ask_str, input_comm_error):
        print('---------------------------------' + ask_str)
        # If there is already an error, don't allow further questions
        if input_comm_error is not None:
            print('Initial error')
            output_comm_error = input_comm_error
            response = None
            return response, output_comm_error
        elif self.comms is None:
            print('self.comms is None')
            output_comm_error = 2
            response = None
            return response, output_comm_error
        else:
            self.comms.write(ask_str)
            response, output_comm_error = self.wait_for_response()
            return response, output_comm_error

    def wait_for_response(self):
        if self.comms is None:
            self.comm_error = 2
            print('self.comms is None')
            response = None
            return response, self.comm_error
        else:
            print('Waiting for response')
            num_bytes = 0

            wait_time = 0
            t0 = time.time()
            while wait_time < 0.05 and num_bytes == 0:  # If timeout (> 50 ms), or num_bytes > 0, move on
                # Took ~9-10 ms for this loop (which was 255 iterations)
                num_bytes = self.comms.bytes_in_buffer
                wait_time = time.time() - t0

            response = b''  # empty bytes object
            wait_time = 0
            t0 = time.time()
            while b'CMD>' not in response and wait_time < self.timeout:          # 'CMD>' is the toptica "prompt"
                time.sleep(0.001)
                num_bytes = self.comms.bytes_in_buffer
                response = response + self.comms.read_bytes(num_bytes)
                # print(str(response))
                wait_time = time.time() - t0

            if b'CMD>' not in response:
                print('Laser Communication Error. Prompt not recieved')
                self.comm_error = 3
                # response = response.decode('utf-8')
                return response, self.comm_error
            else:
                self.comm_error = None

            # print('Full response: ' + str(response))
            # Now remove the command echo and prompt from the response (and convert to string)
            # response = response.split(b'\r\n')[1].decode('utf-8') # This worked until some responses had many lines
            response = response.split(b'\r\n', 1)[1].split(b'\r\nCMD>')[0].decode('utf-8')
            return response, self.comm_error

    # ----------------------------------------- LASER CONTROL FUNCTIONS ------------------------------------------------

    def start_comms(self, com_port):
        print('----------------------------------- INITIALIZING LASER -------------------------------------')
        # Open communications:
        self.com_port = com_port
        self.open()

        print('Comms Initiated')

        self.serial, self.comm_error = self.ask('serial', self.comm_error)
        self.version, self.comm_error = self.ask('ver', self.comm_error)
        self.laser_status, self.comm_error = self.ask('status laser', self.comm_error)
        print('\nSerial: ' + self.serial)
        print('Version: ' + self.version)
        print('Laser Status: ' + self.laser_status)
        self.sys_temp, self.comm_error = self.ask('show temp system', self.comm_error)
        print('baseplate temperature: ' + str(self.sys_temp))
        self.osc_stat, self.comm_error = self.ask('sta osc', self.comm_error)
        print('sta osc: ' + str(self.osc_stat))
        self.talk_status, self.comm_error = self.ask('talk', self.comm_error)
        print('talk status: ' + self.talk_status)
        self.diode_temp, self.comm_error = self.ask('show temp', self.comm_error)
        print('Laser Diode Temperature: ' + str(self.diode_temp))
        self.up_time, self.comm_error = self.ask('show timer', self.comm_error)
        print('Timer: ' + str(self.up_time))
        self.channel, self.comm_error = self.ask('show channel', self.comm_error)
        print('Show channel: ' + self.channel)
        self.status_temp, self.comm_error = self.ask('status temp', self.comm_error)
        print('Status temp: ' + self.status_temp)
        self.close()
        return self.comm_error

    def check_laser_status(self):
        print('inside the function')
        self.open()
        response, self.comm_error = self.ask('sta la', self.comm_error)
        print('Laser Status: ' + response)
        self.close()

    def laser_enable(self):
        print('----------------------------- ENABLING LASER (BIAS/LOW LEVEL) -----------------------------------------')
        self.open()
        print('made it past self.open')
        response, self.comm_error = self.ask('laser on', self.comm_error)
        print('Laser on Response: ' + response)
        self.close()

    def laser_start(self):
        print('---------------------------- STARTING LASER (NORMAL/HIGH LEVEL) ---------------------------------------')
        self.open()
        response, self.comm_error = self.ask('enable 2', self.comm_error)
        print('Laser START Response: ' + response)
        self.close()

    def laser_disable(self):
        print('---------------------------------- STOPPING LASER OUTPUT ----------------------------------------------')
        self.open()
        response, self.comm_error = self.ask('disable 2', self.comm_error)
        print('disable 2 response: ' + response)
        response, self.comm_error = self.ask('laser off', self.comm_error)
        print('laser off response: ' + response)
        self.close()

    def start_digital_modulation(self):
        pass


if __name__ == '__main__':
    test_instr = TopticaInstr()
    test_instr.start_comms('ASRL3::INSTR')
    test_instr.check_laser_status()
    # test_instr.laser_enable()
    # time.sleep(0.3)
    # test_instr.laser_disable()
