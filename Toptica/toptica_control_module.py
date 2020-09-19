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

    def laser_enable(self):
        print('----------------------------- ENABLING LASER (BIAS/LOW LEVEL) -----------------------------------------')
        self.timeout = 15
        self.open()
        print('made it past self.open')
        response, self.comm_error = self.ask('laser on\n', self.comm_error)
        print('Laser on Response: ' + response.decode('utf-8'))
        self.close()
        self.timeout = 3

    def laser_start(self):
        print('---------------------------- STARTING LASER (NORMAL/HIGH LEVEL) ---------------------------------------')
        self.open()
        response, self.comm_error = self.ask('enable 2\n', self.comm_error)
        print('Laser START Response: ' + response.decode('utf-8'))
        self.close()

    def laser_disable(self):
        print('---------------------------------- STOPPING LASER OUTPUT ----------------------------------------------')
        self.open()
        response, self.comm_error = self.ask('disable 2\n', self.comm_error)
        print('disable 2 response: ' + response.decode('utf-8'))
        response = self.ask('laser off')
        print('laser off response: ' + response.decode('utf-8'))
        self.close()

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
                wait_time = time.time() - t0

            if b'CMD>' not in response:
                print('Laser Communication Error. Prompt not recieved')
                self.comm_error = 3
                response = response.decode('utf-8')
                return response, self.comm_error
            else:
                self.comm_error = None

            # print('Full response: ' + str(response))
            # Now remove the command echo and prompt from the response (and convert to string)
            # response = response.split(b'\r\n')[1].decode('utf-8') # This worked until some responses had many lines
            response = response.split(b'\r\n', 1)[1].split(b'\r\nCMD>')[0].decode('utf-8')
            return response, self.comm_error

    def open(self):
        print('made it inside open')
        if self.comms is None:
            return
        else:
            self.comms.open()

    def close(self):
        if self.comms is None:
            return
        else:
            self.comms.before_close()
            self.comms.close()

    def write(self):
        if self.comms is None:
            return
        else:
            self.comms.write()

    def read(self):
        if self.comms is None:
            return
        else:
            self.comms.read()

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

    def start_comms(self, com_port):
        print('----------------------------------- INITIALIZING LASER -------------------------------------')
        # Open communications:
        try:
            self.comms = self.rm.open_resource(com_port, baud_rate=115200, data_bits=8, stop_bits=StopBits.one)
            self.comm_error = None
        except pyvisa.VisaIOError:
            self.comm_error = 1
            print('Failed at open_resource (self.comm_error=1)')
            print(sys.exc_info()[:])

        print('Comms Initiated')

        serial, self.comm_error = self.ask('serial\n', self.comm_error)
        version, self.comm_error = self.ask('ver\n', self.comm_error)
        laser_status, self.comm_error = self.ask('status laser\n', self.comm_error)
        print('\nSerial: ' + serial)
        print('Version: ' + version)
        print('Laser Status: ' + laser_status)
        init_response, self.comm_error = self.ask('ini dac\n', self.comm_error)
        print('Init dac response: ' + init_response)
        init_response, self.comm_error = self.ask('ini laser\n', self.comm_error)
        print('init la response: ' + init_response)
        init_response, self.comm_error = self.ask('show temp system\n', self.comm_error)
        print('baseplate temperature: ' + str(init_response))
        init_response, self.comm_error = self.ask('show temp\n', self.comm_error)
        print('Laser Diode Temperature: ' + str(init_response))
        init_response, self.comm_error = self.ask('show timer\n', self.comm_error)
        print('Timer: ' + str(init_response))
        init_response, self.comm_error = self.ask('show channel\n', self.comm_error)
        print('Show channel: ' + init_response)
        init_response, self.comm_error = self.ask('status temp\n', self.comm_error)
        print('Status temp: ' + init_response)
        self.close()

        return self.comm_error

    def clear_buffers(self):
        # NOTE: THIS FUNCTION CAUSES PROBLEMS. WILL NEED TROUBLESHOOTING IF UTILIZED
        if self.comms is None:
            return
        else:
            self.comms.open()
            self.comms.flush(VI_WRITE_BUF_DISCARD)
            self.comms.flush(VI_READ_BUF_DISCARD)
            self.comms.before_close()
            self.comms.close()

    def start_digital_modulation(self):
        pass


if __name__ == '__main__':
    test_instr = TopticaInstr()
    test_instr.start_comms('ASRL3::INSTR')