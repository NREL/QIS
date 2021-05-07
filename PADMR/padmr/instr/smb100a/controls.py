import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import StopBits, VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore
from typing import Union


class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class SMB100ASettings:
    def __init__(self):
        self.current_freq = None
        self.freq_units = None
        self.current_power = None
        self.output_enabled_status = None
        self.mod_source = 'INT'         # INT or EXT
        self.mod_freq = None
        self.pulse_mod_status = None
        self.pulse_period = None
        self.pulse_width = None
        self.frequency_scale = 0
        self.current_phase = None
        self.max_freq = 2.05E9
        self.frequency_tolerance = 0.00000001  # As a percent deviation from intended frequency

        self.run_status = None

        self.gpib_address = None
        self.com_port = None

class SMB100AInstrument(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    freq_changed_signal = QtCore.pyqtSignal(str)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])

    def __init__(self, *args, **kwargs):
        """
        Currently only GPIB communication is supported
        """
        super(SMB100AInstrument, self).__init__(*args, **kwargs)
        self.error_dict = {'Status': False, 'Code': 0, 'Details': ''}
        self.error = ErrorCluster(status=True, code=8999, details='Communication with SMB100A has not been established')

        self.settings = SMB100ASettings()

        self.connected = False
        self.comms = None

        self.rm = pyvisa.ResourceManager()

    def start_comms(self, com_port='USB0::0x0AAD::0x0054::181799::INSTR'):
        print('Attempting Communication with SMB100A...')
        self.settings.com_port = com_port
        self.open_comms()
        if not self.error.code == 8000:
            try:
                identity = self.comms.query('*IDN?')
                print('CG635 Instrument ID: ' + identity)

                if 'Rohde&Schwarz' in identity:
                    self.connected = True
                    self.error = ErrorCluster(status=False, code=0,
                                              details='')
                else:
                    print('Unexpected ID for RnS Instrument... Communication Failed')
                    self.connected = False
                    self.error = ErrorCluster(status=True, code=8000,
                                              details='Unexpected Identity for RnS Instrument: ' + str(identity))
                    self.send_error_signal.emit(self.error)

            except pyvisa.VisaIOError as err:
                print('Error Establishing Comms with SMB100A:\n' + str(err))
                self.error = ErrorCluster(status=True, code=8000,
                                          details='Error establishing communication with SMB100A.' + str(err))
                self.send_error_signal.emit(self.error)

            self.close_comms()
        return not self.connected

    def close_comms(self):
        print('Closing Comms')
        if self.comms is not None:
            try:
                self.comms.before_close()
                self.comms.close()
            except pyvisa.VisaIOError as err:
                self.connected = False
                if not self.error.status:  # If no preexisting error, generate a new one
                    self.error = ErrorCluster(status=True, code=8001,
                                              details='Error closing communications with SMB100A' + str(err))
                    self.send_error_signal.emit(self.error)
        print('Comms Closed')

    def run(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('OUTP ON; *WAI', read=False)
            response = self.write_string('OUTP?', read=True)

            self.property_updated_signal.emit('output_enabled_status', int(response))
            print('Response: ' + str(response))

    def stop(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('OUTP OFF; *WAI', read=False)
            response = self.write_string('OUTP?', read=True)

            self.property_updated_signal.emit('output_enabled_status', int(response))
            print('Response: ' + str(response))

    def calc_pulse_mod_params(self, target_freq=None, freq_units='Hz'):
        if target_freq is not None:
            if freq_units == 'Hz':
                pass
            elif freq_units == 'kHz':
                target_freq = target_freq * 1000
            elif freq_units == 'MHz':
                target_freq = target_freq * 1E6
            elif freq_units == 'GHz':
                target_freq == target_freq * 1E9
            else:
                pass

            self.settings.mod_freq = target_freq
            self.settings.pulse_period = 1 / self.settings.mod_freq
            self.settings.pulse_width = self.settings.pulse_period / 2

    def set_pulse_mod_freq(self, target_freq, freq_units):
        self.calc_pulse_mod_params(target_freq, freq_units)
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('SOUR:PULM:PERiod ' + str(self.settings.pulse_period), read=False)
            self.write_string('SOUR:PULM:WIDth ' + str(self.settings.pulse_width), read=False)

    def set_pulse_mod_settings(self, mod_source=None):
        if mod_source is None:
            mod_source = self.settings.mod_source

        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            if mod_source == 'INT':
                self.write_string('SOUR:PULM:SOUR INT', read=False)
                self.write_string('SOUR:PULM:TRIG:MODE AUTO', read=False)
                self.write_string('SOUR:PULM:MODE SINGle', read=False)

            elif mod_source == 'EXT':
                self.write_string('SOUR:PULM:SOUR EXT', read=False)
                self.write_string('SOUR:PULM:POLarity Normal', read=False)
                self.write_string('SOUR:PULM:TRIG:EXT:IMPedance G50', read=False)
    #
    # def start_pulse_modulation(self):
    #     if self.error.status:
    #         self.send_error_signal.emit(self.error)
    #     else:
    #         print('Starting Pulse Modulation...')
    #         self.set_pulse_mod_freq(target_freq=self.settings.mod_freq, freq_units=self.settings.freq_units)
    #         self.set_pulse_mod_settings()
    #
    #         self.write_string('SOUR:PGEN:OUTP:STAT 1', read=False)
    #         self.write_string('SOUR:PULM:STAT 1', read=False)
    #
    # def stop_pulse_modulation(self):
    #     if self.error.status:
    #         self.send_error_signal.emit(self.error)
    #     else:
    #         print('Stopping Pulse Modulation...')
    #         self.write_string('SOUR:PGEN:OUTP:STAT 0', read=False)
    #         self.write_string('SOUR:PULM:STAT 0', read=False)

    def reset(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('*RST; *CLS', read=False)

    def write_string(self, string_to_write, read=True, manual=False):
        response = None
        self.open_comms()
        print('opened comms')
        if self.error.status:
            print('Error Status')
            self.send_error_signal.emit(self.error)
        else:
            if manual is True:
                print('manual was true')
                if '?' in string_to_write:
                    read = True
                else:
                    read = False
            try:
                if read is True:
                    response = self.comms.query(string_to_write)
                else:
                    self.comms.write(string_to_write)

            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=8003,
                                          details='Error writing command to SMB100A.' + str(err))
                self.send_error_signal.emit(self.error)

        self.close_comms()
        return response

    def get_freq(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            response = self.write_string('SOUR:FREQ?; *WAI', read=True)
            self.property_updated_signal.emit('current_freq', float(response))
            return float(response)

    def get_power(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            response = self.write_string('SOUR:POW?; *WAI', read=True)
            self.property_updated_signal.emit('current_power', int(response))

    def toggle_modulation(self, is_checked):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            if is_checked:
                print('Starting Pulse Modulation...')
                self.write_string('SOUR:PGEN:OUTP:STAT 1', read=False)
                self.write_string('SOUR:PULM:STAT 1', read=False)
            elif not is_checked:
                print('Stopping Pulse Modulation...')
                self.write_string('SOUR:PGEN:OUTP:STAT 0', read=False)
                self.write_string('SOUR:PULM:STAT 0', read=False)

    def get_current_settings(self):
        print('---------------------------------- Getting Instrument Settings ----------------------------------------')
        self.open_comms()

        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            freq = self.write_string('SOUR1:FREQ?', read=True)
            self.property_updated_signal.emit('current_freq', float(freq))

            p_width = self.write_string('SOUR:PULM:WIDTh?', read=True)
            # self.property_updated_signal.emit('pulse_width', float(p_width))      # Not needed (calc_pulse_mod_params)

            p_period = self.write_string('SOUR:PULM:PERiod?', read=True)
            # self.property_updated_signal.emit('pulse_period', float(p_period))

            mod_freq = 1 / float(p_period)
            self.property_updated_signal.emit('mod_freq', float(mod_freq))

            level = self.write_string('SOUR:POW:LEV?', read=True)
            self.property_updated_signal.emit('current_power', float(level))

            response = self.write_string('SOUR:PULM:STAT?', read=True)
            self.property_updated_signal.emit('pulse_mod_status', int(response))
            #
            # response = self.write_string('SOUR:PULM:SOUR?', read=True)
            # self.property_updated_signal.emit('trigger_source', int(response))

    def set_freq(self, freq_to_set: Union[float, int], units):
        # Check for out of range
        if units == 'Hz':
            if freq_to_set < 100E3:
                freq_to_set = 100E3
            elif freq_to_set > 12.75E9:
                freq_to_set = 12.75E9
        elif units == 'kHz':
            if freq_to_set < 100:
                freq_to_set = 100
            elif freq_to_set > 12.75E6:
                freq_to_set = 12.75E6
        elif units == 'MHz':
            if freq_to_set < 100E-3:
                freq_to_set = 0.1
            elif freq_to_set > 12.75E3:
                freq_to_set = 12.75E3
        elif units == 'GHz':
            if freq_to_set < 100E-6:
                freq_to_set = 100E-6
            elif freq_to_set > 12.75:
                freq_to_set = 12.75

        print('----------------------------------- Setting SMB100A Frequency -----------------------------------------')
        print(str(freq_to_set) + ' ' + units)

        self.open_comms()

        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            freq_str = 'SOUR1:FREQ ' + str(freq_to_set) + units + '; *WAI'
            self.write_string(freq_str, read=False)
            response = self.write_string('SOUR1:FREQ?; *WAI', read=True)
            self.property_updated_signal.emit('current_freq', float(response))

    def set_power(self, target_power):
        print('----------------------------------- Setting SMB100A Power -----------------------------------------')
        print('Target Power: ' + str(target_power))

        self.open_comms()

        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            comm_str = 'SOUR:POW:LEV:IMM:AMPL ' + str(target_power)
            self.write_string(comm_str, read=False)
            response = self.write_string('SOUR:POW?; *WAI', read=True)
            self.property_updated_signal.emit('current_power', float(response))

    # def set_attenuation(self, target_atten):
    #     print('---------------------------------- Setting SMB100A Attenuation ----------------------------------------')
    #     print('Target Power: ' + str(target_atten))
    #
    #     self.open_comms()
    #
    #     if self.error.status:
    #         self.send_error_signal.emit(self.error)
    #     else:
    #         comm_str = 'SOUR:POW:LEV:IMM:AMPL ' + str(target_atten)
    #         self.write_string(comm_str, read=False)
    #         response = self.write_string('SOUR:POW?', read=True)
    #         self.property_updated_signal.emit('current_power', float(response))


    def check_identity(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            response = self.write_string('*IDN?', read=True)
            print('SMB100A Identity: ' + str(response))

    def open_comms(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()

        try:
            self.comms = rm.open_resource(self.settings.com_port)
            time.sleep(0.05)

            self.comms.write_termination = None
            self.comms.read_termination = '\n'

            # Clear the read and write buffers so you start with a clean slate
            self.comms.flush(VI_WRITE_BUF_DISCARD)
            self.comms.flush(VI_READ_BUF_DISCARD)
            self.connected = True
        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=8000,
                                      details='VISA error while opening communications with SMB100A\n\nDetails:'
                                              + str(err))
            self.send_error_signal.emit(self.error)


if __name__ == '__main__':
    test_instr = SMB100AInstrument()
    print('Instantiated')
    did_comms_fail = test_instr.start_comms()
    print('Comms Failure? ' + str(did_comms_fail))

    test_instr.set_freq(100, 'MHz')


