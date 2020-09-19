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

class CG635Instrument:
    # freq_changed_signal = QtCore.pyqtSignal(str)

    def __init__(self, com_format=0, gpib_address=23, com_port='ASRL6::INSTR'):
        self.gpib_address = gpib_address
        self.com_format = com_format
        self.com_port = com_port
        self.comms = None
        self.rm = pyvisa.ResourceManager()
        self.current_freq = None
        self.current_phase = None
        self.max_freq = 2.05E9

        if self.com_format == 0:
            print('CG635 GPIB Stylezz Selected')
        elif self.com_format == 1:
            print('CG635 RS232/USB Stylezzzz')
        else:
            print('unknown com format')

    def test_comms(self):
        try:
            print(self.com_port)
            self.comms = self.rm.open_resource(self.com_port)

            ver_test = self.comms.query('++ver\n')
            print(ver_test)

            self.comms.write('++addr %d\n' % self.gpib_address)
            print('address set: ' + str(self.gpib_address))

            identity = self.comms.query('*IDN?\n')
            print(identity)

            self.comms.before_close()
            self.comms.close()
            comms_failed = False
            traceback = None
        except:
            print('Communications Test Failed')
            traceback = sys.exc_info()
            print(str(sys.exc_info()[:]))
            comms_failed = True
        return comms_failed, traceback

    def check_identity(self):
        self.comms.open()
        self.comms.write('++addr %d\n' % self.gpib_address)
        identity = self.comms.query('*IDN?\n')
        print(identity)

        self.comms.before_close()
        self.comms.close()

    def write_string(self, string_to_write, read=True, manual=False):
        # If the write command is automatic, read must be set correctly on function call
        self.comms.open()
        self.comms.write('++addr %d\n' % self.gpib_address)
        # If there is a question mark in a user write request, it must be treated as a query (unsure if this is
        # sufficient when multiple consecutive commands)

        if manual is True:
            print('manual was true')
            if '?' in string_to_write:
                read = True
            else:
                read = False

        if read is True:
            response = self.comms.query(string_to_write)
        else:
            self.comms.write(string_to_write)
            response = None

        self.comms.before_close()
        self.comms.close()
        return response

    def set_phase(self, phase_to_set):
        print('attempting to set the phase')
        phase_str = 'PHAS ' + str(phase_to_set) + '\n'
        complete = False
        self.comms.write_string(phase_str, read=False)
        # This will work as long as OPC? returns 0 when still going
        ii = 0
        while complete is False and ii < 20:
            print('attempting completion check loop, iteration ' + str(ii))
            complete = bool(self.write_string('*OPC?\n', read=True))
            ii = ii + 1

    def set_phase_as_zero(self):
        self.comms.write_string('RPHS\n', read=False)

    def set_freq_units(self, units_index):
        self.comms.write_string('UNIT 0,%d\n' % units_index, read=False)

    def set_freq(self, freq_to_set: Union[float, int]):
        """ Desired frequency should be input in. Unsure at the moment if units should be included (Hz, kHz, MHz, GHz).
         Scientific notation is ok. Above 10 kHz frequency resolution is
         16 digits, below 10 kHz, frequency resolution is 1 pHz"""
        # Convert freq to string:
        # Truncate to 12 decimal places at low frequency
        print('------------------------------------- Setting Frequency -----------------------------------------------')
        print(freq_to_set)
        if freq_to_set < 10000:
            freq_to_set = '{0:.12f}'.format(freq_to_set)
        # Truncate to 16 digits (decimal -> 17 characters) at high freqs
        # Floats are only stored to 16 digits so will automatically truncate to last nonzero significant digit within 16
        elif 10000 <= freq_to_set <= self.max_freq:
            freq_to_set = "%.17s" % str(freq_to_set)
        else:
            print('Invalid frequency requested')
            freq_to_set = '10000000'                        # Set to 10 MHz if needed

        # Frequencies must be numeric only (in Hz)
        freq_str = 'FREQ ' + str(freq_to_set) + '\n'
        print('freq_str: ' + freq_str + 'writing string')
        self.write_string(freq_str, read=False)
        time.sleep(0.01)    # Large frequency changes have a small changing time
        self.current_freq = self.write_string('FREQ?\n')
        print('returned freq: ' + self.current_freq)
        # Emit a signal saying the current frequency has changed
        # self.freq_changed_signal.emit(self.current_freq)

    def check_for_errors(self):
        pass


if __name__ == '__main__':
    test_instr = CG635Instrument(com_format=0, gpib_address=23, com_port='ASRL6::INSTR')
    comms_failure, traceback = test_instr.test_comms()
    print('comms_failure: ' + str(comms_failure))
    # test_instr.check_identity()
    # identity = test_instr.write_string('*IDN?\n')
    # print("Write_string check: " + str(identity))
    # current_freq = test_instr.write_string('FREQ?\n')
    # print("current_freq: " + str(current_freq))
    # print(type(current_freq))
    test_instr.set_freq(9E6)
    # test_instr.check_for_errors()
    # test_instr.set_phase(10)
    # test_instr.set_phase_as_zero()
