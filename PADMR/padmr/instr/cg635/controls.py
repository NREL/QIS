import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore
from typing import Union


# Notes:
# When GPIB not set on instrument:
# pyvisa.errors.VisaIOError: VI_ERROR_INV_OBJECT (-1073807346):


class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class CG635Settings:
    def __init__(self):
        self.current_freq = None
        self.frequency_scale = 0
        self.current_phase = None
        self.max_freq = 2.05E9
        self.frequency_tolerance = 0.00000001  # As a percent deviation from intended frequency

        self.run_status = None

        self.gpib_address = None
        self.com_format = None
        self.com_port = None


class CG635Instrument(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    freq_changed_signal = QtCore.pyqtSignal(str)
    property_updated_signal = QtCore.pyqtSignal(str, int)

    def __init__(self, *args, **kwargs):
        """
        Currently only GPIB communication is supported, though com_format=0 or 1 exists in case there is need to switch
        to RS232 communications later.
        """
        super(CG635Instrument, self).__init__(*args, **kwargs)
        self.error_dict = {'Status': False, 'Code': 0, 'Details': ''}
        self.error = ErrorCluster(status=True, code=4999, details='Communication with cg635 has not been established')

        self.settings = CG635Settings()

        self.connected = False
        self.comms = None

        # self.gpib_address = None
        # self.com_format = None
        # self.com_port = None

        # self.current_freq = None
        # self.current_phase = None
        # self.max_freq = 2.05E9
        # self.frequency_tolerance = 0.00000001   # As a percent deviation from intended frequency

        self.rm = pyvisa.ResourceManager()

    def start_comms(self, com_format=0, gpib_address=23, com_port='ASRL6::INSTR'):
        self.connected = False
        self.gpib_address = gpib_address
        self.com_format = com_format
        self.com_port = com_port
        if self.com_format == 0:
            print('CG635 GPIB Style Selected')
        elif self.com_format == 1:
            print('CG635 RS232/USB Style')
        else:
            print('unknown com format')

        try:
            self.comms = self.rm.open_resource(self.com_port)
            print('CG635 Resource Opened')

            ver_test = self.comms.query('++ver\n')
            print('Prologix Version: ' + ver_test)

            self.comms.write('++addr %d\n' % self.gpib_address)
            print('Prologix GPIB address set: ' + str(self.gpib_address))

            identity = self.comms.query('*IDN?\n')
            print('CG635 Instrument ID: ' + identity)

            current_freq = self.comms.query('FREQ?\n')
            print('Current Frequency: ' + str(current_freq))
            self.property_updated_signal.emit('current_freq', current_freq)

            instrument_errors = self.comms.query('LERR?\n')
            print('CG635 Errors (0 means none): ' + instrument_errors)
            self.connected = True
            self.error = ErrorCluster(status=False, code=0,
                                      details='')
        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=4000,
                                      details='Error establishing communication with CG635.\n' + str(err))
            self.send_error_signal.emit(self.error)

        self.close_comms()
        return not self.connected

    def close_comms(self):
        try:
            self.comms.before_close()
            self.comms.close()
        except pyvisa.VisaIOError as err:
            self.connected = False
            if not self.error.status:  # If no preexisting error, generate a new one
                self.error = ErrorCluster(status=True, code=4001,
                                          details='Error closing communications with CG635.\n' + str(err))
                self.send_error_signal.emit(self.error)

    def open_comms(self):
        """
        Reopens communications and resets the Prologix GPIB address
        """
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            try:
                self.comms.open()
                self.comms.write('++addr %d\n' % self.gpib_address)
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=4002,
                                          details='Error reopening communications with CG635.\n' + str(err))
                self.send_error_signal.emit(self.error)

    def write_string(self, string_to_write, read=True, manual=False):
        # If the write command is automatic, read must be set correctly on function call
        self.open_comms()
        # self.comms.open()
        # self.comms.write('++addr %d\n' % self.gpib_address)
        # If there is a question mark in a user write request, it must be treated as a query (unsure if this is
        # sufficient when multiple consecutive commands)
        if self.error.status:
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
                    response = None
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=4003,
                                          details='Error writing command to CG635.\n' + str(err))
                self.send_error_signal.emit(self.error)

        self.close_comms()
        # self.comms.before_close()
        # self.comms.close()
        return response

    def check_identity(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.open_comms()
            try:
                # self.comms.open()
                # self.comms.write('++addr %d\n' % self.gpib_address)
                identity = self.comms.query('*IDN?\n')
                print(identity)
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=4004,
                                          details='Error checking identity of CG635.\n' + str(err))
                self.send_error_signal.emit(self.error)
            self.close_comms()


        # self.comms.before_close()
        # self.comms.close()

    def set_freq(self, freq_to_set: Union[float, int], scaling_factor):
        """ Desired frequency should be input in Hz.
         Scientific notation is ok. Above 10 kHz frequency resolution is
         16 digits, below 10 kHz, frequency resolution is 1 pHz"""
        # Convert freq to string:
        # Truncate to 12 decimal places at low frequency
        print('------------------------------------- Setting Frequency -----------------------------------------------')
        print(freq_to_set)
        print('scaling factor: ' + str(scaling_factor))
        freq_to_set = freq_to_set * scaling_factor
        print('scaled freq_to_set: ' + str(freq_to_set))
        if freq_to_set < 10000:
            freq_adjusted = '{0:.12f}'.format(freq_to_set)
        # Truncate to 16 digits (decimal -> 17 characters) at high freqs
        # Floats are only stored to 16 digits so will automatically truncate to last nonzero significant digit within 16
        elif 10000 <= freq_to_set <= self.settings.max_freq:
            freq_adjusted = "%.17s" % str(freq_to_set)
        else:
            print('Invalid frequency requested')
            freq_adjusted = '10000000'                        # Set to 10 MHz if needed

        # Frequencies must be numeric only (in Hz)
        freq_str = 'FREQ ' + str(freq_adjusted) + '\n'
        print('freq_str: ' + freq_str + 'writing string')
        # self.write_string(freq_str, read=False)
        self.open_comms()

        if self.error.status:
            pass
            # self.send_error_signal.emit(self.error)
        else:
            # self.comms.open()
            # self.comms.write('++addr %d\n' % self.gpib_address)
            try:
                self.comms.write(freq_str)
                pll_locked = False
                ii = 0
                # self.comms.write('*CLS')
                while pll_locked is False and ii < 20:
                    print('loop iteration: ' + str(ii))
                    pll_lock_status = self.comms.query('LCKR?\n')
                    print('pll_lock_status: ' + str(pll_lock_status))
                    if int(pll_lock_status) == 0:
                        print('pll_locked')
                        pll_locked = True
                    ii = ii+1

                if pll_locked is False:
                    print('PLL never locked. Final LCKR? Response: ' + str(pll_lock_status))
                    self.error = ErrorCluster(status=True, code=4006,
                                              details='CG635, Phase Locked Loop never locked to reference oscillator.\n'
                                                      'Output may be stopped')
                    self.send_error_signal.emit(self.error)

                self.settings.current_freq = self.comms.query('FREQ?\n')   # This adds time and may not be needed
                current_freq_float = float(self.settings.current_freq)
                print('returned freq: ' + self.settings.current_freq)

                if not (freq_to_set - (freq_to_set*self.settings.frequency_tolerance)) < current_freq_float <\
                        (freq_to_set + (freq_to_set*self.settings.frequency_tolerance)):
                    # self.warning = 'Actual Frequency Deviates Significantly from Desired Frequency'
                    # print(self.warning)
                    self.error = ErrorCluster(status=True, code=4007,
                                              details='CG635, Actual Frequency Deviates Significantly from Desired.')
                    self.send_error_signal.emit(self.error)

            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=4005,
                                          details='VISA error adjusting frequency of CG635.\n' + str(err))
                self.send_error_signal.emit(self.error)

            self.close_comms()
            # self.comms.before_close()
            # self.comms.close()
            # Emit a signal saying the current frequency has changed
            self.freq_changed_signal.emit(self.settings.current_freq)
        return

    # def set_phase(self, phase_to_set):
    #     self.write_string('PHAS %d; *WAI\n' % phase_to_set, read=False)
    #     new_phase = self.write_string('PHAS?\n', read=True)
    #     self.property_updated_signal.emit('phase', float(new_phase))

    def set_phase(self, phase_to_set):
        print('attempting to set the phase')
        phase_str = 'PHAS ' + str(phase_to_set) + '\n'
        complete = False
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            # self.comms.open()
            # self.comms.write('++addr %d\n' % self.gpib_address)
            self.comms.write_string(phase_str, read=False)
            # This will work as long as OPC? returns 0 when still going
            ii = 0
            while complete is False and ii < 20:
                print('attempting completion check loop, iteration ' + str(ii))
                complete = bool(self.write_string('*OPC?\n', read=True))
                ii = ii + 1
            new_phase = self.write_string('PHAS?\n', read=True)
            self.property_updated_signal.emit('phase', float(new_phase))

    @QtCore.pyqtSlot()
    def set_phase_as_zero(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('RPHS\n', read=False)

    @QtCore.pyqtSlot(int)
    def set_freq_units(self, units_index):
        self.settings.frequency_scale = 10 ** (3 * units_index)
        self.settings.frequency_scale_idx = units_index
        self.property_updated_signal.emit('frequency_scale', int(self.settings.frequency_scale))
        self.property_updated_signal.emit('frequency_scale_idx', int(self.settings.frequency_scale_idx))
        # self.write_string('UNIT 0,%d\n' % units_index, read=False)

    @QtCore.pyqtSlot(float)
    def set_max_freq(self, new_max_freq):
        self.settings.max_freq = new_max_freq
        self.property_updated_signal.emit('max_freq', float(self.settings.max_freq))

    def check_pll_status(self):
        # Clear the status bytes
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('*CLS\n', read=False)
            response = self.write_string('LCKR?\n', read=True)
            if not int(response) == 0:
                self.error = ErrorCluster(status=True, code=4008,
                                          details='PLL Lock Status Register Indicates Locking Has Been Lost.\n\n'\
                                             + 'Register Byte Value: ' + response)
                self.send_error_signal.emit(self.error)

    @QtCore.pyqtSlot()
    def run(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('RUNS 1\n', read=False)
            response = self.write_string('RUNS?\n', read=True)
            self.property_updated_signal.emit('run_status', int(response))

    @QtCore.pyqtSlot()
    def stop(self):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('RUNS 0\n', read=False)
            response = self.write_string('RUNS?\n', read=True)
            self.property_updated_signal.emit('run_status', int(response))

    @QtCore.pyqtSlot(int)
    def change_units(self, idx):
        if self.error.status:
            self.send_error_signal.emit(self.error)
        else:
            self.write_string('UNIT %d\n' % idx, read=False)
            response = self.write_string('UNIT?\n', read=True)
            self.property_updated_signal.emit('display_units', int(response))


if __name__ == '__main__':
    test_instr = CG635Instrument()
    comms_failure, traceback = test_instr.start_comms(com_format=0, gpib_address=23, com_port='ASRL6::INSTR')
    print('comms_failure: ' + str(comms_failure))
    # test_instr.check_identity()
    # identity = test_instr.write_string('*IDN?\n')
    # print("Write_string check: " + str(identity))
    # current_freq = test_instr.write_string('FREQ?\n')
    # print("current_freq: " + str(current_freq))
    # print(type(current_freq))
    error = test_instr.set_freq(1000)
    # test_instr.check_for_errors()
    # test_instr.set_phase(10)
    # test_instr.set_phase_as_zero()
