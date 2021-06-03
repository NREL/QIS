import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore


class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class LockinSettings:
    def __init__(self):
        self.resource = None
        self.gpib_address = None

        self.model = None
        self.outputs = None
        self.settling_delay_factor = None
        self.sensitivity = None
        self.filter_slope = None
        self.time_constant = None
        self.time_constant_value = None
        self.wide_reserve = None
        self.close_reserve = None
        self.dynamic_reserve = None
        self.sampling_rate = None
        self.sampling_rate_idx = None
        self.input_impedance = None
        self.reference_impedance = None
        self.reference_source = None
        self.twoF_detect_mode = None
        self.harmonic = None
        self.frequency = None
        self.phase = 0
        self.expand = None
        self.is_averaging_pts = False

        self.sens_list = None
        self.tc_list = None
        self.tc_numeric_list = None
        self.slope_list = None

        self.sr844_sens_list = ['100 nV', '300 nV', '1 µV', '3 µV', '10 µV', '30 µV', '100 µV', '300 µV',
                                '1 mV', '3 mV', '10 mV', '30 mV', '100 mV', '300 mV', '1 V']

        self.sr844_tc_list = ['100 µs', '300 µs', '1 ms', '3 ms', '10 ms', '30 ms', '100 ms', '300 ms', '1 s',
                              '3 s', '10 s', '30 s', '100 s', '300 s', '1 ks', '3 ks', '10 ks', '30 ks']

        self.sr830_sens_list = ['2 nV', '5 nV', '10 nV', '20 nV', '50 nV', '100 nV', '200 nV', '500 nV', '1 µV',
                                '2 µV', '5 µV', '10 µV', '20 µV', '50 µV', '100 µV', '200 µV', '500 µV', '1 mV',
                                '2 mV', '5 mV', '10 mV', '20 mV', '50 mV', '100 mV', '200 mV', '500 mV', '1 V']

        self.sr830_tc_list = ['10 µs', '30 µs', '100 µs', '300 µs', '1 ms', '3 ms', '10 ms', '30 ms', '100 ms',
                              '300 ms', '1 s', '3 s', '10 s', '30 s', '100 s', '300 s', '1 ks', '3 ks', '10 ks',
                              '30 ks']

        self.sr844_slope_list = ['No Filter', '6 dB/Oct', '12 dB/Oct', '18 dB/Oct', '24 dB/Oct']

        self.sr830_slope_list = ['6 dB/Oct', '12 dB/Oct', '18 dB/Oct', '24 dB/Oct']

        self.sr844_tc_options = [100E-6, 300E-6, 1E-3, 3E-3, 10E-3, 30E-3, 100E-3, 300E-3,
                                1, 3, 10, 30, 100, 300, 1000, 3000, 10E3, 30E3]

        self.sr830_tc_options = [10E-6, 30E-6, 100E-6, 300E-6, 1E-3, 3E-3, 10E-3, 30E-3, 100E-3, 300E-3,
                                1, 3, 10, 30, 100, 300, 1000, 3000, 10E3, 30E3]

        # self.sampling_rate_list = [62.5E-3, 125E-3, 250E-3, 500E-3, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


class PrologixAdaptedSRLockin(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])

    def __init__(self, *args, **kwargs):
        """
        Some basic communication functions for controlling SRS lock-in amplifiers SR844 and SR830 (possibly others too)
        through the Prologix USB-GPIB adapter.

        TO USE:
        1. instantiate your instrument object (e.g. sr844 = PrologixAdaptedSRLockin())
        2. Establish/test VISA comms with the instrument
            (e.g. sr844.start_comms(resource='ASRL6::INSTR', gpib_address=8, model='SR844') )
        3. ONLY AFTER communications are established, other methods may be used

        NOTES:
        CG635 and the Lock-ins are wired through the same prologix adapter, meaning that the GPIB address must be
        changed whenever the instrument being addressed changes
        """
        super(PrologixAdaptedSRLockin, self).__init__(*args, **kwargs)
        self.error = ErrorCluster(status=True, code=3999,
                                  details='Communication with the LIA has not been established')

        self.settings = LockinSettings()

        self.connected = False
        self.comms = None

        self.rm = pyvisa.ResourceManager()
        self.tc_options = None
        # Etc...

    def start_comms(self, resource, gpib_address=8, model='SR844'):
        """
        Prepares the lockin instance for later communications, and tests that some basic commands are working
        """
        self.settings.resource = resource
        self.settings.model = model
        self.settings.gpib_address = int(gpib_address)

        self.connected = False

        if model == 'SR844':
            self.settings.tc_numeric_list = self.settings.sr844_tc_options
        elif model == 'SR830':
            self.settings.tc_numeric_list = self.settings.sr830_tc_options

        if self.error.status and self.error.code != 3999:   # i.e. if there's an error other than "comms not est'd yet"
            print('Preexisting Error Found')
            self.send_error_signal.emit(self.error)
        elif not self.error.status or self.error.code == 3999:
            try:
                print('About to open resource for lockin at: ' + str(self.settings.resource))
                self.comms = self.rm.open_resource(self.settings.resource)
                ver_test = self.comms.query('++ver\n')
                print('ver_test: ' + str(ver_test))
                self.comms.write('++addr %d\n' % self.settings.gpib_address)
                print('Prologix GPIB address set: ' + str(self.settings.gpib_address))

                self.comms.write('OUTX 1\n')

                identity = self.comms.query('*IDN?\n')
                print('Lockin Identified: ' + identity)

                self.connected = True
                self.error = ErrorCluster(status=False, code=0, details='')
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=3000,
                                          details='Error attempting to start communications with lock-in.\n'
                                                  'Check com port and GPIB Address.\n\n'
                                                  'Details: \n' + str(err))
                self.send_error_signal.emit(self.error)

            self.close_comms()
        return not self.connected

    def close_comms(self):
        print('made it inside close_comms')
        if self.comms is not None:
            try:
                self.comms.before_close()
                self.comms.close()
            except pyvisa.VisaIOError as err:
                print('made it inside second exception')
                self.connected = False
                self.error.status = True
                self.error.code = 3001
                self.error.details = 'Error attempting to close communication with lock-in.\n' + str(err)
                self.send_error_signal.emit(self.error)
                print('made it to the end of the second exception')

    def open_comms(self):
        """
        Open VISA communications and set the GPIB address so the Prologix adapter knows who to communicate with.
        The latter would be unnecessary if only one Prologix/GPIB connected instrument was used "simultaneously".
        """
        if not self.error.status:
            try:
                self.comms.open()
                self.comms.write('++addr %d\n' % self.settings.gpib_address)
                print('Opened Communications')
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=3002,
                                          details='Error attempting to reopen communication with lock-in.\n' + str(err))
                self.send_error_signal.emit(self.error)

    def write_string(self, string_to_write, read=True):
        response = None
        if not self.error.status:
            try:
                self.comms.open()
                self.comms.write('++addr %d\n' % self.settings.gpib_address)
                self.comms.write(string_to_write)
                if read is True:
                    time.sleep(0.1)
                    response = self.comms.read()
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=3003,
                                          details='Error attempting to write to lock-in.\n' + str(err))
                self.send_error_signal.emit(self.error)
            self.close_comms()
        return response

    # def test_comms(self):
    #     if not self.error.status:
    #         try:
    #             self.comms = self.rm.open_resource(self.settings.resource)
    #             ver_test = self.comms.query('++ver\n')
    #             self.comms.write('++addr %d\n' % self.settings.gpib_address)
    #             print('Prologix GPIB address set: ' + str(self.settings.gpib_address))
    #             self.comms.write('OUTX 1\n')
    #             identity = self.comms.query('*IDN?\n')
    #             print('Lockin Identified: ' + identity)
    #             self.comms.before_close()
    #             self.comms.close()
    #             comms_failed = False
    #         except pyvisa.VisaIOError as err:
    #             self.error.status = True
    #             self.error.code = 3004
    #             self.error.details = 'Error attempting to start communications with lock-in.\n' + str(err)
    #             self.send_error_signal.emit(self.error_dict)
    #             comms_failed = True
    #     else:       # An error occurred before the function was called
    #         comms_failed = True
    #
    #     return comms_failed

    def check_status(self):
        """
        Check the lock-in amplifier status register ('LIAS?\n'). Response is a 12-bit integer

        LIAS? reports whether there are over/underloads or if the internal reference oscillator is unlocked from the
         external reference input. Each bit in the response integer means something different, but if any of them are
          nonzero, an error has occurred.

        Status register flags remain until cleared by reading the status register the ...write('*CLS\n') command.

        Responses:
        -1 - Communication error
        0 - No error. Lock-in status register flags zero problems
        1-4095 - Various LIAS status flags. See manual for details. Bit zero is the least significant bit
        (i.e. if only bit0 = 1, then the return value will be 1, if bit0 and bit1 both = 1, the response will be 3)
        Common Flags:
        bit0(1) - Reference Unlocked; bit1(2) - Ext Ref frequency out of range; bit7(128) - Ref Frequency changed by >1%
        """
        # If no preexisting error, then try to query the lia status. If that fails then abort and let the error know.
        # If status is successfully read, then check if the status is zero. If not, then these types of lock-in "errors"
        # have occured (PLL unlocked, massive frequency change, etc.).
        if not self.error.status:
            try:
                status = self.comms.query('LIAS?\n')
                status = int(status)
                print('Lock-in Status Register: ' + str(status))
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=3004,
                                          details='Communication error while querying lock-in status.\n' + str(err))
                self.send_error_signal.emit(self.error)
                return -1
                # self.error = 'VISA Error'
                # return self.error

            # if not status == 0:
            #     # This is not really an error, so I will not treat it as one.
            #     # print('LIAS Error')
            #     # self.error = 'LIAS Status' + str(status)
            # else:
            #     self.error = None
        else:
            # No new signal emits from here because if there is a preexisting error it should already have emitted
            # (and if this is in a careless loop, you would get cascading error window)
            print('Preexisting error prevented command')
            return -1
        return status

    def clear_buffers(self):
        """
        Clears the read and write buffers of data, so you can start with a fresh clean slate.
        Note that errors are not cleared. I'm not sure why, but I've found that clearing once is not always sufficient.
        """
        if not self.error.status:
            try:
                self.comms.flush(VI_WRITE_BUF_DISCARD)
                self.comms.flush(VI_READ_BUF_DISCARD)
                self.comms.flush(VI_WRITE_BUF_DISCARD)
                self.comms.flush(VI_READ_BUF_DISCARD)
                print('Cleared Buffers')
            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=3005,
                                          details='Error while attempting to clear buffers.\n' + str(err))
                self.send_error_signal.emit(self.error)

    # ----------------------------------------------- SINGLE COMMANDS --------------------------------------------------
    @QtCore.pyqtSlot()
    def auto_sens(self):
        """
        As it stands this will fail if self.comms.open is not used before calling this function. This is intentional
        so as to make it as fast as possible.
        """
        self.comms.write('AGAN\n', read=False)
        ifc_ready = 0
        time_zero = time.time()
        wait_dur = time_zero
        while ifc_ready == 0 and wait_dur < 10:     # I don't know if this is a long enough wait time if high time const
            ifc_ready = int(self.comms.query('*STB? 1\n'))
        new_value = int(self.comms.query('SENS?\n'))
        self.property_updated_signal.emit('sensitivity', new_value)

    @QtCore.pyqtSlot()
    def auto_crsrv(self):
        print('updating something')
        self.write_string('ACRS\n', read=False)

    @QtCore.pyqtSlot()
    def auto_dyn_rsrv(self):
        print('updating something')
        self.write_string('ARSV\n', read=False)

    @QtCore.pyqtSlot()
    def auto_wrsrv(self):
        print('updating something')
        self.write_string('AWRS\n', read=False)
        new_value = int(self.write_string('WRSV?\n', read=True))
        self.property_updated_signal.emit('wide_reserve', new_value)

    @QtCore.pyqtSlot()
    def auto_offset(self):
        """Offsets R"""
        print('updating something')
        if self.settings.model == 'SR844':
            self.write_string('AOFF 1, 1\n', read=False)
        elif self.settings.model == 'SR830':
            self.write_string('AOFF 3\n', read=False)

    @QtCore.pyqtSlot()
    def auto_phase(self):
        print('updating something')
        self.write_string('APHS\n', read=False)
        new_value = self.write_string('PHAS?\n', read=True)
        self.property_updated_signal.emit('phase', new_value)
#######################
    @QtCore.pyqtSlot(int)
    def update_crsrv(self, idx):
        print('updating something')
        self.write_string('CRSV %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('close_reserve', idx)

    @QtCore.pyqtSlot(int)
    def update_wrsrv(self, idx):
        print('updating wide reserve')
        print('new idx is: ' + str(idx))
        self.write_string('WRSV %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('wide_reserve', idx)

    @QtCore.pyqtSlot(int)
    def update_dyn_rsrv(self, idx):
        print('updating something')
        self.write_string('RMOD %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('dynamic_reserve', idx)

    @QtCore.pyqtSlot(int)
    def update_expand(self, idx):
        print('updating something')
        print('self.settings.model: ' + str(self.settings.model))
        if self.settings.model == 'SR844' and self.settings.outputs == 0:
            self.write_string('DEXP 1,1,%d\n' % idx, read=False)
            self.write_string('DEXP 2,1,%d\n' % idx, read=False)
        elif self.settings.model == 'SR844' and self.settings.outputs == 1:
            self.write_string('DEXP 1,0,%d\n' % idx, read=False)
            # self.write_string('DEXP 2,0,%d\n' % self.settings.sr844_expand, read=False)
        elif self.settings.model == 'SR830' and self.settings.outputs == 0:
            self.write_string('OEXP 3,0,%d\n' % idx, read=False)
        elif self.settings.model == 'SR830' and self.settings.outputs == 1:
            self.write_string('OEXP 1,0,%d\n' % idx, read=False)
            self.write_string('OEXP 2,0,%d\n' % idx, read=False)

        if not self.error.status:
            self.property_updated_signal[str, int].emit('expand', idx)

    @QtCore.pyqtSlot(int)
    def update_filter_slope(self, idx):
        print('updating filter slope')
        self.write_string('OFSL%d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('filter_slope', idx)

    @QtCore.pyqtSlot(int)
    def update_2f(self, idx):
        print('Updating 2f detect mode')
        self.write_string('HARM %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('twoF_detect_mode', idx)

        self.property_updated_signal.emit('twoF_detect_mode', idx)

    @QtCore.pyqtSlot(int)
    def update_harmonic(self, value):
        print('updating harmonic')
        self.write_string('HARM %d\n' % value, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('harmonic', value)

    @QtCore.pyqtSlot(float)
    def update_phase(self, phase_to_set):
        print('updating something')
        self.write_string('PHAS %d\n' % phase_to_set, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('phase', phase_to_set)

    @QtCore.pyqtSlot(int)
    def update_input_impedance(self, idx):
        print('updating something')
        self.write_string('INPZ %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('phase', idx)

    @QtCore.pyqtSlot(int)
    def update_outputs(self, idx):
        print('updating outputs')
        if self.settings.model == 'SR844' and idx == 0 and self.connected is True:
            print('attempting to set outputs to R and Theta')
            self.write_string('DDEF 1, 1\n', read=False)
            self.write_string('DDEF 2, 1\n', read=False)
        elif self.settings.model == 'SR844' and idx == 1:
            print('Attempting to set outputs to X and Y')
            self.write_string('DDEF 1, 0\n', read=False)
            self.write_string('DDEF 2, 0\n', read=False)
        elif self.settings.model == 'SR844' and idx == 2:
            print('Attempting to set channel 1 to Aux In 1...')
            print('Channel 2 will be left as is.')
            self.write_string('DDEF 1, 4\n', read=False)
        elif self.settings.model == 'SR830' and idx == 0:
            print('Attempting to set outputs to R and Theta')
            self.write_string('DDEF 1, 1, 0\n', read=False)
            self.write_string('DDEF 2, 1, 0\n', read=False)
        elif self.settings.model == 'SR830' and idx == 1:
            print('Attempting to set outputs to X and Y')
            self.write_string('DDEF 1, 0, 0\n', read=False)
            self.write_string('DDEF 2, 0, 0\n', read=False)
        elif self.settings.model == 'SR830' and idx == 2:
            print('Attempting to set channel 1 to Aux In 1...')
            print('Channel 2 will not be recorded.')
            self.write_string('DDEF 1, 3, 0\n', read=False)

        if not self.error.status:
            self.property_updated_signal.emit('outputs', idx)

    @QtCore.pyqtSlot(int)
    def update_ref_impedance(self, idx):
        print('updating something')
        self.write_string('REFZ %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('reference_impedance', idx)

    @QtCore.pyqtSlot(int)
    def update_ref_source(self, idx):
        print('updating something')
        self.write_string('FMOD %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('reference_source', idx)

    @QtCore.pyqtSlot(int)
    def update_freq(self, target_freq):
        print('updating reference frequency...')
        if (self.settings.model == 'SR844' or self.settings.model == 'SR830') and self.connected is True:
            self.write_string('FREQ %d\n' % target_freq, read=False)
            new_value = float(self.write_string('FREQ?\n', read=True))
            self.settings.frequency = new_value
            if not self.error.status:
                self.property_updated_signal.emit('frequency', new_value)
        else:
            print('Sorry, this case not coded yet...')

    @QtCore.pyqtSlot(int)
    def update_sampling_rate(self, idx):
        print('updating something')
        self.write_string('SRAT %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('sampling_rate_idx', idx)
            srat = 2**(idx-4)
            self.property_updated_signal.emit('sampling_rate', srat)

    @QtCore.pyqtSlot(int)
    def update_sensitivity(self, idx):
        print('updating something')
        self.write_string('SENS %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal.emit('sensitivity', idx)

    @QtCore.pyqtSlot(int)
    def update_time_constant(self, idx):
        print('updating time constant')
        self.write_string('OFLT %d\n' % idx, read=False)
        if not self.error.status:
            self.property_updated_signal[str, int].emit('time_constant', idx)
            new_tc = self.settings.tc_numeric_list[idx]
            print('new_tc: ' + str(new_tc))
            self.property_updated_signal[str, float].emit('time_constant_value', new_tc)
            print('self.settings.time_constant_value: ' + str(self.settings.time_constant_value))

    def update_all(self):
        print('Updating All Lock-in Parameters')
        print(str(self.settings.expand))
        print(type(self.settings.expand))
        self.update_expand(self.settings.expand)
        self.update_filter_slope(self.settings.filter_slope)
        self.update_phase(self.settings.phase)
        self.update_outputs(self.settings.outputs)
        self.update_ref_source(self.settings.reference_source)
        self.update_sampling_rate(self.settings.sampling_rate_idx)
        self.update_sensitivity(self.settings.sensitivity)
        self.update_time_constant(self.settings.time_constant)

        if self.settings.model == 'SR844':
            self.update_crsrv(self.settings.close_reserve)
            self.update_wrsrv(self.settings.wide_reserve)
            self.update_2f(self.settings.twoF_detect_mode)
            self.update_input_impedance(self.settings.input_impedance)
            self.update_ref_impedance(self.settings.reference_impedance)
        elif self.settings.model == 'SR830':
            self.update_dyn_rsrv(self.settings.dynamic_reserve)
            self.update_harmonic(self.settings.harmonic)
        else:
            print('Invalid Lock-in Model')
            self.error = ErrorCluster(status=True, code=3007,
                                      details='Lock-in model is invalid\n')
            self.send_error_signal.emit(self.error)

    def collect_snapshot(self):
        if self.error.status:
            return None, None

        self.clear_buffers()

        try:
            self.comms.write('REST\n')
            self.comms.timeout = 3000

            if self.settings.model == 'SR844' and not self.settings.outputs == 2:
                output_str = 'SNAP? ' + '9,10\n'      # Read whatever is on the display
            elif self.settings.model == 'SR830' and not self.settings.outputs == 2:
                output_str = 'SNAP? ' + '10,11\n'     # Read whatever is on the display
            elif self.settings.model == 'SR844' and self.settings.outputs == 2:
                output_str = 'SNAP? ' + '6\n'         # Aux In 1
            elif self.settings.model == 'SR830' and self.settings.outputs == 2:
                output_str = 'SNAP? ' + '5\n'         # Aux In 1

            response = self.comms.query(output_str)
            [str1, str2] = response.split('\n')[0].split(',')
            ch1 = float(str1)
            ch2 = float(str2)

        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=3008,
                                      details='Error while attempting to collect data.\n' + str(err))
            self.send_error_signal.emit(self.error)
            ch1 = None
            ch2 = None

        self.comms.timeout = 3000
        self.close_comms()
        return ch1, ch2

    def collect_data(self, duration, sampling_rate_idx, record_both_channels=True):
        """
        This function should be run in a separate thread
        unless the duration is very short
        """
        if self.error.status:
            return None, None
        # Clear the buffers (self.comms first, then clear the SR844 buffers)
        #     self.comms.flush(VI_WRITE_BUF_DISCARD)
        #     self.comms.flush(VI_READ_BUF_DISCARD)
        #     self.comms.flush(VI_WRITE_BUF_DISCARD)
        #     self.comms.flush(VI_READ_BUF_DISCARD)
        self.clear_buffers()

        try:
            self.comms.write('REST\n')
            self.comms.timeout = 3000

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

            errors = self.comms.query('ERRS?\n')
            print('Lockin Error Register: ' + str(errors))

            if self.settings.model == 'SR844' or self.settings.model == 'SR830':
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

                errors = self.comms.query('ERRS?\n')
                print('Lockin Error Register: ' + str(errors))

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
        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=3006,
                                      details='Error while attempting to collect data.\n' + str(err))
            self.send_error_signal.emit(self.error)
            values_ch1_arr = None
            values_ch2_arr = None

        self.comms.timeout = 3000
        self.close_comms()
        return values_ch1_arr, values_ch2_arr


if __name__ == '__main__':
    test = PrologixAdaptedSRLockin()
    did_comms_fail = test.start_comms('ASRL6::INSTR', gpib_address=8, model='SR844')
