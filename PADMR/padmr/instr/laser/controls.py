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


class TopticaInvalidValueException(BaseException):
    pass

class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class TopticaSettings:
    def __init__(self):
        self.connected = False
        self.com_port = None
        self.diode_temp = None
        self.timeout = 3
        self.power = 0
        self.bias_power = 0
        self.laser_status = 0   # 0 is off, 1 is on
        self.mod_on = 0


class TopticaInstr(QtCore.QObject):
    """
    Error Codes are 5000-5999
    """
    send_error_signal = QtCore.pyqtSignal(object)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])

    def __init__(self, *args, **kwargs):
        super(TopticaInstr, self).__init__(*args, **kwargs)
        self.error = ErrorCluster(status=True, code=5999,
                                  details='Communication with the Toptica laser has not been established')
        self.settings = TopticaSettings()

        self.settings.connected = False
        self.comms = None

        self.settings.com_port = None

        self.current_freq = None
        self.comm_error = None
        self.timeout = 3

        self.rm = pyvisa.ResourceManager()

    def start_comms(self, com_port):
        print('----------------------------------- INITIALIZING LASER -------------------------------------')
        # Open communications:
        self.settings.com_port = com_port
        self.open_comms()
        if self.error.status:
            print('Toptica Initialization Aborted due to pre-existing error')
            return
        else:
            print('Comms Initiated')
            self.settings.serial = self.ask('serial')
            self.settings.version = self.ask('ver')
            status = self.ask('status laser')
            if status == 'OFF':
                status_idx = 0
            elif status == 'ON':
                status_idx = 1
            self.ask('di ext')
            self.settings.sys_temp = self.ask('show temp system')
            self.settings.osc_stat = self.ask('sta osc')
            self.settings.talk_status = self.ask('talk')
            self.settings.up_time = self.ask('show timer')
            self.settings.channel = self.ask('show channel')
            self.settings.status_temp = self.ask('status temp')
            self.close_comms()

            self.property_updated_signal[str, int].emit('laser_status', status_idx)

            if not self.error.status:
                print('\nSerial: ' + self.settings.serial)
                print('Version: ' + self.settings.version)
                print('Laser Status: ' + status)
                print('baseplate temperature: ' + str(self.settings.sys_temp))
                print('sta osc: ' + str(self.settings.osc_stat))
                print('talk status: ' + self.settings.talk_status)
                print('Timer: ' + str(self.settings.up_time))
                print('Show channel: ' + self.settings.channel)
                print('Status temp: ' + self.settings.status_temp)

    def close_comms(self):
        print('Closing toptica communications...')
        if self.comms is None:
            print('self.comms was none')
            return
        else:
            try:
                self.comms.before_close()
                self.comms.close()
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=5006,
                                          details='VISA error while closing communication with Toptica\n' + str(err))
                self.send_error_signal.emit(self.error)

    def open_comms(self):
        print('Opening Toptica Comms...')
        try:
            self.comms = self.rm.open_resource(self.settings.com_port, baud_rate=115200, data_bits=8,
                                               stop_bits=StopBits.one)
            self.comms.write_termination = '\r\n'
            self.comm_error = None
            self.error = ErrorCluster(status=False, code=0, details='')
        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=5001,
                                      details='VISA error while trying to open communication with Toptica\n' + str(err))
            self.send_error_signal.emit(self.error)

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

    def ask(self, ask_str):
        print('---------------------------------' + ask_str)
        # If there is already an error, don't allow further questions
        if self.error.status:
            print('Initial error')
            response = None
        elif self.comms is None:
            print('self.comms is None')

            response = None
            self.error = ErrorCluster(status=True, code=5002,
                                      details='Communication with Toptica failed because communications have'
                                              ' not yet been established')
            self.send_error_signal.emit(self.error)
        else:
            try:
                self.comms.write(ask_str)
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=5003,
                                          details='VISA error while trying to write command to Toptica\n' + str(
                                              err))
                self.send_error_signal.emit(self.error)

            response = self.wait_for_response()
        return response

    def wait_for_response(self):
        print('Waiting for response...')
        num_bytes = 0

        wait_time = 0
        t0 = time.time()
        try:
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

            print('raw response: ' + str(response))
            if b'CMD>' not in response:
                print('Laser Communication Error. Prompt not recieved')
                self.error = ErrorCluster(status=True, code=5004,
                                          details='Toptica Communication Error - Prompt not Received\n')
                self.send_error_signal.emit(self.error)
            else:
                # Now remove the command echo and prompt from the response (and convert to string)
                response = response.split(b'\r\n', 1)[1].split(b'\r\nCMD>')[0].decode('utf-8')
        except pyvisa.VisaIOError as err:
            response = None
            self.error = ErrorCluster(status=True, code=5005,
                                      details='VISA error while trying to wait for response from Toptica\n' + str(err))
            self.send_error_signal.emit(self.error)

        return response

    # ----------------------------------------- LASER CONTROL FUNCTIONS ------------------------------------------------

    def check_laser_status(self):
        print('inside the function')
        self.open_comms()
        response = self.ask('sta la')
        print('Laser Status: ' + response)
        self.close_comms()

    def laser_enable(self):
        print('----------------------------- ENABLING LASER (BIAS/LOW LEVEL) -----------------------------------------')
        self.open_comms()
        print('made it past self.open_comms')
        response = self.ask('laser on')
        print('Laser on Response: ' + response)
        status = self.ask('status laser')
        self.close_comms()
        if status == 'OFF':
            print('status was off')
            status_ind = 0
        elif status == 'ON':
            print('status was on')
            status_ind = 1
        self.property_updated_signal[str, int].emit('laser_status', status_ind)

    def laser_start(self):
        print('---------------------------- STARTING LASER (NORMAL/HIGH LEVEL) ---------------------------------------')
        self.open_comms()
        response = self.ask('enable 2')
        print('Laser START Response: ' + response)
        status = self.ask('status laser')

        power_str = self.ask('show power')      # Should look like: '%SYS-I-077, scaled\r\nPIC  = 012000 uW  '
        power_val = float(power_str.split()[4])

        self.close_comms()
        if status == 'OFF':
            print('status was off')
            status_ind = 0
        elif status == 'ON':
            print('status was on')
            status_ind = 1
        self.property_updated_signal[str, int].emit('laser_status', status_ind)
        self.property_updated_signal[str, float].emit('power', power_val)

    def laser_disable(self):
        print('---------------------------------- STOPPING LASER OUTPUT ----------------------------------------------')
        self.open_comms()
        response = self.ask('disable 2')
        print('disable 2 response: ' + response)
        response = self.ask('laser off')
        print('laser off response: ' + response)
        status = self.ask('status laser')
        self.close_comms()
        if status == 'OFF':
            print('status was off')
            status_ind = 0
        elif status == 'ON':
            print('status was on')
            status_ind = 1
        self.property_updated_signal[str, int].emit('laser_status', status_ind)

    def set_power(self, power_value, units_idx=1):
        """
        The units_idx is either 0 for microwatts or 1 for mW
        """
        print('This functionality not set up')
        self.open_comms()
        if units_idx == 0:      # microwatts
            units_str = ' mic'
            if power_value > 150000:
                power_value = 150000
                print('Power has been trimmed to 150 mW (max output)')
        elif units_idx == 1:    # milliwatts
            units_str = ''
            if power_value > 150:
                power_value = 150
                print('Power has been trimmed to 150 mW (max output)')
        else:
            raise TopticaInvalidValueException(units_idx)

        pow_str = 'ch2 pow ' + str(power_value) + units_str
        response = self.ask(pow_str)
        print('set power response: ' + response)
        act_pow_str = self.ask('show power')
        power_val = float(act_pow_str.split()[4])
        self.close_comms()
        self.property_updated_signal[str, float].emit('power', power_val)

    def set_bias_power(self, power_value, units_idx=1):
        print('this functionality not set up yet')
        self.open_comms()
        if units_idx == 0:
            units_str = ' mic'
            if power_value > 150000:
                power_value = 150000
                print('Power has been trimmed to 150 mW (max output)')
        elif units_idx == 1:
            units_str = ''
            if power_value > 150:
                power_value = 150
                print('Power has been trimmed to 150 mW (max output)')
        else:
            raise TopticaInvalidValueException(units_idx)

        pow_str = 'ch1 pow ' + power_value + units_str
        response = self.ask(pow_str)
        print('set_bias_power response: ' + response)
        # act_bias_pow = float(self.ask())
        self.close_comms()
        # self.property_updated_signal[str, float].emit('bias_power', act_bias_pow)

    def start_digital_modulation(self):
        self.open_comms()
        response = self.ask('enable ext')
        print('enable ext response: ' + response)
        self.close_comms()
        self.property_updated_signal[str, int].emit('mod_on', 1)

    def stop_digital_modulation(self):
        self.open_comms()
        response = self.ask('disable ext')
        print('disable ext response: ' + response)
        self.close_comms()
        self.property_updated_signal[str, int].emit('mod_on', 0)

if __name__ == '__main__':
    test_instr = TopticaInstr()
    test_instr.start_comms('ASRL3::INSTR')
    test_instr.check_laser_status()
    test_instr.open_comms()
    power = test_instr.ask('show power')
    print(power)
    responsei = test_instr.ask('show ch')
    test_instr.close_comms()
    # test_instr.stop_digital_modulation()
    # test_instr.laser_disable()
    # test_instr.open_comms()
    # resp = test_instr.ask('show limit')
    # print(resp)
    # test_instr.close_comms()
    # test_instr.laser_enable()
    # time.sleep(0.3)
    # test_instr.laser_start()
    # print('starting laser in normal mode')
    # time.sleep(3)
    # print('starting digital modulation')
    # test_instr.start_digital_modulation()
    # time.sleep(20)
    # test_instr.stop_digital_modulation()
    # test_instr.laser_disable()
