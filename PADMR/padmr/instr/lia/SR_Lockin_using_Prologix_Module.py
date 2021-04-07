import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore


class LockinError(BaseException):
    pass


class PrologixAdaptedSRLockin:
    send_error_signal = QtCore.pyqtSignal(dict)
    def __init__(self):
        self.error_dict = {'Status': False, 'Code': 0, 'Details': ''}

        self.connected = False
        self.resource = None
        self.lockin_model = None
        self.gpib_address = None

        self.comms = None
        self.time_constant = None
        self.sensitivity = None
        self.outputs = None
        self.filter_slope = None

        self.tc_options = None
        # Etc...

    def open(self):
        """
        Open VISA communications and set the GPIB address so the Prologix adapter knows who to communicate with.
        The latter would be unnecessary if only one Prologix/GPIB connected instrument was used "simultaneously".
        """
        if self.error_dict['Status'] == False:
            try:
                self.comms.open()
                self.comms.write('++addr %d\n' % self.gpib_address)
                print('Opened Communications')
            except pyvisa.VisaIOError as err:
                self.error_dict['Status'] = True
                self.error_dict['Code'] = 3001
                self.error_dict['Details'] = 'Error attempting to reopen communication with lock-in.\n' + str(err)
                self.send_error_signal.emit(self.error_dict)

    def write_string(self, string_to_write, read=True):
        response = None
        if not self.error_dict['Status']:
            try:
                self.comms.open()
                self.comms.write('++addr %d\n' % self.gpib_address)
                self.comms.write(string_to_write)
                if read is True:
                    time.sleep(0.1)
                    response = self.comms.read()
            except pyvisa.VisaIOError as err:
                self.error_dict['Status'] = True
                self.error_dict['Code'] = 3002
                self.error_dict['Details'] = 'Error attempting to write to lock-in.\n' + str(err)
                self.send_error_signal.emit(self.error_dict)
        else:       # An error existed before the function call
            return response

        # The following is separate because I think we should attempt to close communications even if an error occurs
        try:
            self.comms.before_close()
            self.comms.close()
        except pyvisa.VisaIOError as err:
            self.error_dict['Status'] = True
            self.error_dict['Code'] = 3003
            self.error_dict['Details'] = 'Error attempting to close lock-in.\n' + str(err)
            self.send_error_signal.emit(self.error_dict)

        return response

    # def test_comms(self):
    #     if not self.error_dict['Status']:
    #         try:
    #             self.comms = self.rm.open_resource(self.resource)
    #             ver_test = self.comms.query('++ver\n')
    #             self.comms.write('++addr %d\n' % self.gpib_address)
    #             print('Prologix GPIB address set: ' + str(self.gpib_address))
    #             self.comms.write('OUTX 1\n')
    #             identity = self.comms.query('*IDN?\n')
    #             print('Lockin Identified: ' + identity)
    #             self.comms.before_close()
    #             self.comms.close()
    #             comms_failed = False
    #         except pyvisa.VisaIOError as err:
    #             self.error_dict['Status'] = True
    #             self.error_dict['Code'] = 3004
    #             self.error_dict['Details'] = 'Error attempting to start communications with lock-in.\n' + str(err)
    #             self.send_error_signal.emit(self.error_dict)
    #             comms_failed = True
    #     else:       # An error occurred before the function was called
    #         comms_failed = True
    #
    #     return comms_failed

    def start_comms(self, resource, gpib_address=8, lockin_model='SR844'):
        self.resource = resource
        self.lockin_model = lockin_model
        self.gpib_address = int(gpib_address)

        if lockin_model == 'SR844':
            self.tc_options = [100E-6, 300E-6, 1E-3, 3E-3, 10E-3, 30E-3, 100E-3, 300E-3,
                               1, 3, 10, 30, 100, 300, 1000, 3000, 10E3, 30E3]
        elif lockin_model == 'SR830':
            self.tc_options = [10E-6, 30E-6, 100E-6, 300E-6, 1E-3, 3E-3, 10E-3, 30E-3, 100E-3, 300E-3,
                               1, 3, 10, 30, 100, 300, 1000, 3000, 10E3, 30E3]

        self.rm = pyvisa.ResourceManager()

        if not self.error_dict['Status']:
            try:
                self.comms = self.rm.open_resource(self.resource)
                # ver_test = self.comms.query('++ver\n')
                self.comms.write('++addr %d\n' % self.gpib_address)
                print('Prologix GPIB address set: ' + str(self.gpib_address))
                self.comms.write('OUTX 1\n')
                identity = self.comms.query('*IDN?\n')
                print('Lockin Identified: ' + identity)
                self.comms.before_close()
                self.comms.close()
                comms_failed = False
                self.connected = True
            except pyvisa.VisaIOError as err:
                self.error_dict['Status'] = True
                self.error_dict['Code'] = 3004
                self.error_dict['Details'] = 'Error attempting to start communications with lock-in.\n' + str(err)
                self.send_error_signal.emit(self.error_dict)
                comms_failed = True
        else:  # An error occurred before the function was called
            comms_failed = True

        return comms_failed

    def check_status(self):
        try:
            status = self.comms.query('LIAS?\n')
        except pyvisa.VisaIOError:
            self.error = 'VISA Error'
            return self.error

        status = int(status)
        print('Lock-in Status: ' + str(status))

        if not status == 0:
            print('LIAS Error')
            self.error = 'LIAS Status' + str(status)
        else:
            self.error = None

        return self.error

    def clear_buffers(self):
        self.comms.flush(VI_WRITE_BUF_DISCARD)
        self.comms.flush(VI_READ_BUF_DISCARD)
        self.comms.flush(VI_WRITE_BUF_DISCARD)
        self.comms.flush(VI_READ_BUF_DISCARD)
        print('Cleared Buffers')

    def collect_data(self, duration, sampling_rate_idx, record_both_channels=True):
        """ Sampling rate must be a power of 2 (or it will round). This function should be run as a separate thread
        unless the duration is very short"""
        # Clear the buffers (self.comms first, then clear the SR844 buffers)
        self.comms.flush(VI_WRITE_BUF_DISCARD)
        self.comms.flush(VI_READ_BUF_DISCARD)
        self.comms.flush(VI_WRITE_BUF_DISCARD)
        self.comms.flush(VI_READ_BUF_DISCARD)
        self.comms.write('REST\n')

        self.comms.timeout = 3000

        # sampling_rate_index = int(round(np.log2(sampling_rate)) + 4) # See SR844 manual p 4-24

        self.comms.write('SRAT %d\n' % sampling_rate_idx)  # Set the data sample rate to the desired rate

        self.comms.write('STRT\n')  # Start a scan
        time.sleep(duration)  # Wait while SR844 collects data

        self.comms.write('PAUS\n')  # Pause the scan

        print('Scan Paused')
        # Transfer rates:
        # TRCL - 0.66 ms per sample (1 channel)
        # TRCB - 1.04 ms per sample (1 channel)
        # TRCA - 10.3 ms per sample (1 channel) - DO NOT USE THIS!!
        # SNAP - ~30-40 ms per sample ("2 channels") - Good for real time data tracking but not optimal for DAQ
        # I tried getting FAST transfer to work but the transfer would fail above 64 Hz (not sure why)
        # TRCL at least allows for X/Y sampling > 256 Hz on average (including data transfer and conversion)

        if self.lockin_model == 'SR844' or self.lockin_model == 'SR830':
            print('SR844 or SR830')
            samples_to_read = int(self.comms.query('SPTS?\n'))

            # Assumes 1 millisecond to read each sample (actual is ~0.66 ms), want at least 1 second if few samples
            sampling_rate = 2**(sampling_rate_idx - 4)
            self.comms.timeout = 1000 + 1 * (duration*sampling_rate)

            # Transfer the channel 1 data stored in the buffer
            data_bytes = []
            print('----------------------------------- TRANSFERRING DATA TO COMPUTER ---------------------------------')
            self.comms.write('TRCL? 1,0,%d\n' % samples_to_read)
            for ii in range(0, samples_to_read):
                try:
                    appendix = self.comms.read_bytes(4)
                    data_bytes.append(appendix)
                except:
                    print(sys.exc_info()[:])
                    break
            # Now the data has been read by the computer
            # Now convert these values into something useful (the format for TRCL is quite strange but is much faster):
            mantissas_ch1 = []
            exponents_ch1 = []
            values_ch1 = []
            for ii in range(0, len(data_bytes)):
                mantissas_ch1.append(int.from_bytes(data_bytes[ii][0:2], 'little', signed=True))  # Get bytes 0 & 1 (not 2)
                exponents_ch1.append(int.from_bytes(data_bytes[ii][2:4], 'little', signed=True))  # Get bytes 2 & 3 (4 DNE)

                values_ch1.append(mantissas_ch1[ii] * 2 ** (exponents_ch1[ii] - 124))

            values_ch1_arr = np.array(values_ch1)

            if record_both_channels:
                data_bytes_ch2 = []
                self.comms.write('TRCL? 2,0,%d\n' % samples_to_read)
                for ii in range(0, samples_to_read):
                    try:
                        appendix = self.comms.read_bytes(4)
                        data_bytes_ch2.append(appendix)
                    except:
                        print(sys.exc_info()[:])
                        break

                ## Now convert these values into something useful:
                mantissas_ch2 = []
                exponents_ch2 = []
                values_ch2 = []
                for ii in range(0, len(data_bytes)):
                    mantissas_ch2.append(
                        int.from_bytes(data_bytes_ch2[ii][0:2], 'little', signed=True))  # Get bytes 0 & 1 (not 2)
                    exponents_ch2.append(
                        int.from_bytes(data_bytes_ch2[ii][2:4], 'little', signed=True))  # Get bytes 2 & 3 (4 DNE)

                    values_ch2.append(mantissas_ch2[ii] * 2 ** (exponents_ch2[ii] - 124))

                values_ch2_arr = np.array(values_ch2)
            else:
                values_ch2_arr = None

            self.comms.timeout = 3000
            self.comms.before_close()
            self.comms.close()
        return values_ch1_arr, values_ch2_arr
