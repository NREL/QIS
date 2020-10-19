# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 21:37:38 2020
Note for later - merge message and error_message if possible into a single
progress update thing

This file contains all of the important commands for controlling the monochromator. Initialization must be done first
as it contains the establishment of communications with the device. Ideally anything can be done in any order after that
Since it should ready all attributes and set necessary settings as well as homing the device.

@author: Ryan
"""

# from PyQt5.QtCore import QRunnable, QThreadPool
from PyQt5 import QtCore

import pyvisa
from pyvisa.constants import StopBits, VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD
import time
import sys
from decorator import decorator

from tkinter import *

# To work on next:
# 1. Figure out the scan tab
# 2. Associate all buttons with actual functionality
# 3. See if error_messages can be merged
# 4. General Cleanup
# 5. Make sure backlash correction is done correctly


# Changes you can make soon:

# Questions:
# Is it better to open and close the visa resource within the write string command? Or in each function separately?
# do decorators up here get used if my main program just imports MonoDriver? I guess I have to import them too...?
# For error handling can I just use the sys.exc_info()[0] command instead of doing all this parsing stuff?

# Changes to make when we can actually use the driver
# 1 - I think that in the initialize function, the "return self.x, self.y can just be replaced with returns
# since Class attributes are not forgotten.

# Notes -
# 1. After a write (at least when writing *IDN?, it seems like 0.1 seconds is the minimum round number wait time
# to get the full response. The number of bytes is something like 85 so at a baud rate of 9600 bits/sec (1200 bytes/sec)
# 85 bytes would take 0.071 sec

# @decorator
# def check_write_success(f, instance_name, *args, **kwargs):
#     """ After an attempted write function, check if the write was successful
#      It's possible this is more general (since It just checks the error code)"""
#     result = f(instance_name, *args, **kwargs)
#     if instance_name.error_code == 0:
#         instance_name.status_message = 'Write Success'
#     elif instance_name.error_code == 1:
#         instance_name.status_message = 'Write Failed'
#     else:
#         instance_name.status_message = instance_name.error_message
#     return result


# ------------------------ BEGIN CLASS DEFINITIONS -----------------------------
class MD2000InvalidValueException(BaseException):
    pass


class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class MonoSettings:
    def __init__(self):
        self.com_port = None
        self.speed = 500
        self.gr_dens_idx = None
        self.gr_dens_opts = [2400, 1800, 1200, 600, 300, 150]
        self.gr_dens_val = None
        self.k_number = None
        self.cal_wl = 0
        self.cur_wl = 0
        self.connected = False
        self.bl_amt = 10.0
        self.bl_bool = True


class MonoDriver(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    status_message_signal = QtCore.pyqtSignal(str)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])

    def __init__(self, *args, **kwargs):
        """ initializes Mono
        Error Messages: -1073807298 (also read error) is device is turned off (or unplugged?)
         -1073807246 occurs when device has been initialized by labview already (solution is
         to close labview, turn off, unplug, replug and turn on)
         -1073807343 indicates device has not been plugged in ever
         whereas -1073807194 seems to occur if it has been unplugged recently
         Also can be fixed sometimes by restarting spyder
         timeout -1073807339 (still to be incorporated)"""
        # QtCore.QObject.__init__(*args, **kwargs)
        super(MonoDriver, self).__init__(*args, **kwargs)
        self.error = ErrorCluster(status=True, code=6999, details='Communication has not been established with md2000')

        self.settings = MonoSettings()

        self.last_wavelength = 0
        # self.settings.com_port = None       #Visa resource e.g. 'ASRL4::INSTR'
        self.error_code = 1
        self.error_message = 0
        # self.settings.connected = False
        self.readout = None
        # self.settings.k_number = 0
        # self.settings.gr_dens = None
        # self.settings.speed = 500
        self.status_message = None
        self.calibration_wavelength = 0
        self.current_wavelength = 0
        self.move_cfm_iteration_timeout = 150
        self.stop_motion_bool = False
        self.continue_updating = False
        self.stop_moving = False
        self.busy = False
        # Run instantiation Functions
        # self.get_k_number()
        self.in_motion = False

        # End __init__ def ---------------------------------------------------
        
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------- HIGH LEVEL FUNCTIONS -------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

    def establish_comms(self, com_port):  # Add a return response or something so that we can see the response?
        self.settings.com_port = com_port
        self.open_visa()

        if not self.error.code == 6000:
            try:
                self.comm.write("*IDN?")
                time.sleep(0.1)
                num_bytes = self.comm.bytes_in_buffer
                response = self.comm.read_bytes(num_bytes)
                print('Mono IDN response:\n'+ str(response.decode('UTF-8')))
                if b'\r\nX,' in response:
                    self.error = ErrorCluster(status=False, code=0, details='')
                    self.settings.connected = True
                else:
                    print('size of response: ' + str(sys.getsizeof(response)))
                    self.error = ErrorCluster(status=True, code=6005,
                                              details='Incorrect Response from MD2000 Identification Query.\n'
                                                      'Check that device is turned on.\n'
                                                      'Power cycle device.\n '
                                                      'Check that Com Ports for all instruments are assigned correctly')
                    self.send_error_signal.emit(self.error)
            except pyvisa.VisaIOError as err:
                print('error in est comms')
                self.error = ErrorCluster(status=True, code=6001,
                                          details='VISA error while trying to establish comms with md2000')
                self.send_error_signal.emit(self.error)

            self.close_visa()

    def initialize_mono(self, com_port):
        """ This one has the code for the rest of the initialization (homing, etc.) """
        self.settings.com_port = com_port
        self.get_k_number()
        self.status_message_signal.emit('Establishing Communications with MD2000')
        self.establish_comms(self.settings.com_port)
        # self.status_message = 'Communications Established'
        print('comms established')
        if self.error.status:
            print('preexisting md2000 error')
            return
        else:
            print('error_code was 0')
            # This is the "communication success" section
            # self.status_message = 'Homing Monochromator'
            self.status_message_signal.emit('Homing Monochromator')
            time.sleep(0.25)
            # Move Negative (Moves it to ~ 200 nm)
            self.move_cfm('X0W0T4800R-38000S')  # Add the check for failure situation to this one
            print('made it past first move_cfm')
            time.sleep(0.25)  # I don't know if these are needed after each command. In labview they are parallel waits
            # Move Negative 2
            self.move_cfm('X2W15T4800R-640S')
            time.sleep(0.25)
            # Move Positive
            self.move_cfm('X2W0T640R+12200S')
            self.status_message_signal.emit('Homing Complete, Setting Current Position = 0 nm')
            # self.status_message = 'Homing Complete, Setting Current Position = 0 nm'
            time.sleep(0.25)
            self.set_zero_position()
            time.sleep(0.25)
            time.sleep(0.25)
            self.set_speed(self.settings.speed)

    def go_to_wavelength(self, destination, backlash_amount, backlash_bool):
        # Decide which direction the move is:
        # print('current wavelength: ' + str(self.current_wavelength))
        # self.status_message = 'Moving to ' + str(destination) + ' nm'
        self.status_message_signal.emit('Moving Mono to ' + str(destination) + ' nm')
        print('Moving to: ' + str(destination))
        if destination < self.current_wavelength:
            direction = 'Down'
        elif destination > self.current_wavelength:
            direction = 'Up'
        else:
            self.status_message_signal.emit('No Wavelength Change Requested')
            # self.status_message = 'No Wavelength Change Requested'
            return

        # First generate the string you need to write
        steps = self.convert_wl_to_steps_absolute(destination)
        tmp_string = ('X' + str(steps) + 'G')

        # Then go there
        self.open_visa()
        self.write_str(tmp_string)
        self.check_position_loop()
        print('Finished check position loop')
        self.close_visa()
        print('closed visa in go to wl')
        if direction == 'Down' and backlash_bool is True and self.stop_moving is False:
            print('attempting to correct')
            self.status_message = 'Correcting for Backlash'
            self.nudge(backlash_amount, higher=False, stop_updating_at_finish=False)

            self.nudge(backlash_amount, higher=True, stop_updating_at_finish=False)

        time.sleep(0.01)
        self.continue_updating = False
        self.busy = False
        self.status_message = 'Movement Complete'
        print('Movement Complete')

    def nudge(self, amount_nm, higher, stop_updating_at_finish=True):
        """Give amount in nm, higher as a boolean (true for higher false for lower), and speed
        in nm/sec"""
        self.continue_updating = True
        if self.settings.connected:
            num_steps = round(amount_nm * self.settings.k_number)
            if higher:
                nudge_str = ("X" + str(num_steps) + "S")
                self.status_message = ('Nudging ' + str(num_steps) + ' up (~' + str(amount_nm) + ' nm)')
                self.open_visa()
                self.write_str(nudge_str)
                self.check_position_loop()
                self.close_visa()
            elif not higher:
                nudge_str = ("X-" + str(num_steps) + "S")
                self.status_message = ('Nudging ' + str(num_steps) + ' down (~' + str(amount_nm) + ' nm)')
                self.open_visa()
                self.write_str(nudge_str)
                self.check_position_loop()
                self.close_visa()
            else:
                self.error_code = 1
                self.error_message = "Invalid Write String (direction)"
                self.status_message = self.error_message
        else:
            self.status_message = 'WRITE ABORTED - MONOCHROMATOR NOT AVAILABLE'
            return              # more needs to go here obviously

        if stop_updating_at_finish is True:
            time.sleep(0.01)
            self.continue_updating = False
        self.busy = False
        self.status_message = 'Nudge Completed'

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------- MID LEVEL FUNCTIONS ------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def move_cfm(self, command):
        """ Move_Check_for_motion. This function is for writing a command and then waiting until motion is complete
        Before moving on. It's possible that if speed is set very low the number of loop iterations will run out
        before motion is done."""
        self.open_visa()
        self.write_str(command, read=False)

        self.in_motion = True
        i = 1
        while i < self.move_cfm_iteration_timeout:

            self.write_str('X-8?', read=True)  # This is the command for check for movement i guess

            print(str(i) + ' ..... Readout: ' + str(self.readout))

            check_val = int(self.readout.split('X,-8,', 1)[1].split('\r\n', 1)[0])

            # try:
            #     # Response to this will be before_str = 'b\r\r\n' and after_str = '0\r\n*' (0 may be 0,1,2, or 5, where
            #     # 0 indicates motion is complete')
            #     [before_str, after_str] = self.readout.split('X,-8,', 1)
            #     print('before_str: ' + str(before_str))
            # except ValueError as err:  # In the case that there is only one output (parse string not found)
            #     try:
            #         before_str = self.readout.split('X,-8', 1)[0]
            #         after_str = ''  # Might it be better to use a 0?
            #         print('Pretty sure this shouldnt have happened')
            #     except ValueError as err:   # In case somehow there was a different issue
            #         print('Not sure how this happened, move_cfm aborted')
            #         print(str(sys.exc_info()[0]))
            #         print(str(sys.exc_info()[1]))
            #         print(str(sys.exc_info()[2]))
            #         self.close_visa()
            #         return
            #
            # try:
            #     # The prefix r is to force the search string to be treated as "raw" rather than escape sequence
            #     before_str_2 = after_str.split(r'\r\n', 1)[0]  # We don't need the after string here
            # except ValueError as err:
            #     print('Not sure how this happened, move_cfm aborted')
            #     self.close_visa()
            #     print(str(sys.exc_info()[0]))
            #     print(str(sys.exc_info()[1]))
            #     print(str(sys.exc_info()[2]))
            #     return

            try:
                move = int(check_val)  # To match the labview, 0 must be output if non-numeric/empty string remains
            except ValueError:
                # move = 0
                print('Value error on trying to convert to int')
                print(str(sys.exc_info()[:]))
                return

            if move == 0:
                move_bool = True
            else:
                move_bool = False

            if move_bool is True and i > 6:
                move_done_bool = True
            else:
                move_done_bool = False

            if move_done_bool is True or self.error.status:  # A stop button may also be added here?
                self.in_motion = False
                break

            if i >= (self.move_cfm_iteration_timeout - 1):
                self.error = ErrorCluster(status=True, code=6004, details='Mono Initialization Failed')
                self.send_error_signal.emit(self.error)
                # self.status_message_signal.emit(self.error.details)
                self.in_motion = False
                break

            i += 1
        self.in_motion = False
        self.close_visa()
        self.busy = False

    def set_speed(self, speed):
        """ speed is given in nm/sec, a string is output and sent to the stepper"""
        self.status_message = 'Setting Speed'
        if isinstance(speed, (int, float)):
            if speed > 1000:
                speed = 1000
            elif speed < 0:
                speed = 0

            r_number = round(speed * self.settings.k_number)
            tmp_string = ('X' + str(r_number) + 'R')
            self.settings.speed = speed

            self.open_visa()
            self.write_str(tmp_string, read=True)
            self.close_visa()
        else:
            self.status_message = 'Speed Request Invalid - Enter a Numeric Value Between 0 and 1000'

    def set_zero_position(self):  # Unsure if this is needed since it is done in the initialization.
        self.open_visa()
        self.write_str('X0=15T', read=True)
        self.current_wavelength = self.get_current_pos()
        self.close_visa()

        self.status_message = 'Stepper Position set to ' + str(self.current_wavelength) + ' nm'

    def set_home_position(self, home_wl):
        # self.zero_wavelength = self.ui.calib_wl_spinner.value()
        self.settings.cal_wl = home_wl
        self.set_zero_position()
        cur_wl = self.settings.cal_wl
        print('Home wavelength is: ' + str(self.settings.cal_wl))
        self.property_updated_signal[str, float].emit('cur_wl', cur_wl)
        self.status_message_signal.emit('Home Wavelength Set')

    def get_current_pos(self):
        """ for internal use. must open and close visa surrounding this function """
        # self.open_visa()   # Is this needed?
        self.write_str('X-1?', read=True)
        # self.close_visa()

        response = self.readout
        # partially_parsed = response.split('X,-1,', 1)[1]
        current_step_position = response.split('X,-1,', 1)[1].split('\r\n', 1)[0]
        print('wavelength in steps: ' + str(current_step_position))
        current_step_position = int(current_step_position)
        wavelength = self.convert_steps_absolute_to_wavelength(current_step_position)
        wavelength = round(wavelength, 2)
        print('wavelength calculated from steps: ' + str(wavelength))
        return wavelength

    def stop_motion(self):  # This function is likely unnecessary altogether and should be a condition in if statements
        self.stop_moving = True
        time.sleep(0.1)
        self.open_visa()
        self.write_str('XZ', read=False)
        print('wrote stop motion command')
        self.continue_updating = False
        time.sleep(0.1)
        self.close_visa()
        print('closed visa after stop motion')

        # try:
        #     self.close_visa()
        # except:
        #     print(sys.exc_info()[0])
        #     print(sys.exc_info()[1])
        #     print(sys.exc_info()[2])

        self.stop_moving = False
        self.status_message = 'Move Aborted'
        time.sleep(0.1)
        self.open_visa()
        print('getting current position...')
        self.current_wavelength = self.get_current_pos()
        print('closing visa after getting position')
        self.close_visa()

    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------- LOW LEVEL FUNCTIONS ------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def write_str(self, command, read=True):        # Should the open and close be INSIDE here? I keep forgetting them..
        """ """
        print('got inside write_str ' + str(command))
        if self.settings.connected:
            try:
                self.comm.write(str(command))
                time.sleep(0.1)

                if read is True:
                    num_bytes = self.comm.bytes_in_buffer
                    readout = self.comm.read_bytes(num_bytes)
                    self.readout = readout.decode('UTF-8')
                    print('readout: ' + str(self.readout))

                else:
                    self.readout = None
                # self.error_message = "Command Sent"
                # self.error_code = 0

            except pyvisa.VisaIOError as err:
                self.error = ErrorCluster(status=True, code=6002,
                                          details='VISA Error while trying to write command to MD2000\n' + str(err))
                self.send_error_signal.emit(self.error)
                self.settings.connected = False
                self.readout = None

        else:
            self.error = ErrorCluster(status=True, code=6003,
                                      details='Write Aborted - MD2000 Communication Not Established')
            self.send_error_signal.emit(self.error)
            self.readout = None
        print('made it to the end of write_str')
        # End IF statement-------
        return  # self.settings.connected, self.readout, self.error_message, self.error_code
    # End write to Mono --------------------------------------------------------

    def open_visa(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()

        try:
            self.comm = rm.open_resource(self.settings.com_port, baud_rate=9600, data_bits=8,
                                         stop_bits=StopBits.one, timeout=1000)
            time.sleep(0.05)
            # self.comm.query_delay = 0.05  # The labview code used 50ms between r/w
            # These are important, if the write termination is set incorrectly (default is '\r\n'), response will just
            # be a string that looks like:  '\r\r\r\r\r\n'
            self.comm.write_termination = None
            self.comm.read_termination = None

            # Clear the read and write buffers so you start with a clean slate
            self.comm.flush(VI_WRITE_BUF_DISCARD)
            self.comm.flush(VI_READ_BUF_DISCARD)
        except pyvisa.VisaIOError as err:
            self.error = ErrorCluster(status=True, code=6000,
                                      details='VISA error while opening communications with Mono driver\n\nDetails:\n'
                                              + str(err))
            self.send_error_signal.emit(self.error)

    def close_visa(self):
        self.comm.before_close()
        self.comm.close()

    def check_position_loop(self):
        self.last_wavelength = 0
        print('starting to check position')
        ii = 0
        while (self.current_wavelength - self.last_wavelength) != 0 or ii < 6:
            if self.stop_moving is False:
                # print('got inside while  measuring posn')
                # time.sleep(0.01)
                self.last_wavelength = self.current_wavelength
                current_wl = self.get_current_pos()
                print('current_wl: ' + str(current_wl))
                self.current_wavelength = current_wl
            else:
                break
            ii += 1

        print('Finishing check position')

    def get_k_number(self):
        if self.settings.gr_dens_val == 2400:
            k_number = 64
        elif self.settings.gr_dens_val == 1800:
            k_number = 48
        elif self.settings.gr_dens_val == 1200:
            k_number = 32
        elif self.settings.gr_dens_val == 600:
            k_number = 16
        elif self.settings.gr_dens_val == 300:
            k_number = 8
        elif self.settings.gr_dens_val == 150:
            k_number = 4
        self.property_updated_signal[str, int].emit('k_number', k_number)
        # End get_k_number--------------

    def convert_wl_to_steps_absolute(self, wavelength):
        steps = round((wavelength - self.settings.cal_wl) * self.settings.k_number)
        steps = int(steps)
        return steps

    def convert_steps_absolute_to_wavelength(self, steps):
        wavelength = ((steps / self.settings.k_number) + self.settings.cal_wl)
        return wavelength
#--------------------------END CLASS DEFINITIONS-------------------------------


