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

from PyQt5.QtCore import QRunnable, QThreadPool

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
class MonoDriver(QRunnable):
    def __init__(self, resource, groove_density):
        """ initializes Mono
        Error Messages: -1073807298 (also read error) is device is turned off (or unplugged?)
         -1073807246 occurs when device has been initialized by labview already (solution is
         to close labview, turn off, unplug, replug and turn on)
         -1073807343 indicates device has not been plugged in ever
         whereas -1073807194 seems to occur if it has been unplugged recently
         Also can be fixed sometimes by restarting spyder
         timeout -1073807339 (still to be incorporated)"""

        self.last_wavelength = 0
        self.resource = resource        #Visa resource e.g. 'ASRL4::INSTR'
        self.error_code = 1
        self.error_message = 0
        self.connected = False
        self.readout = None
        self.k_number = 0
        self.groove_density = groove_density
        self.speed = 500
        self.status_message = None
        self.calibration_wavelength = 0
        self.current_wavelength = 0
        self.move_cfm_iteration_timeout = 150
        self.stop_motion_bool = False
        self.continue_updating = False
        self.stop_moving = False
        self.busy = False
        # Run instantiation Functions
        self.get_k_number()
        self.in_motion = False

        # End __init__ def ---------------------------------------------------
        
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------- HIGH LEVEL FUNCTIONS -------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

    def establish_comms(self):  # Add a return response or something so that we can see the response?
        self.open_visa()

        try:
            self.comm.write("*IDN?")
            time.sleep(0.1)
            num_bytes = self.comm.bytes_in_buffer
            response = self.comm.read_bytes(num_bytes)
            if sys.getsizeof(response) > 13:
                self.connected = True
                self.error_code = 0
                self.error_message = "Mono connection test passed"
                self.status_message = self.error_message
                print('mono connection test passed')
        except pyvisa.VisaIOError as eCode:
            eCode = str(eCode)
            eCode = eCode.partition("(")[2]
            eCode = eCode.partition(")")[0]
            eCode = int(eCode)
            if eCode == -1073807298:
                self.error_message = "Mono Could not Connect - Loc 2"
            elif eCode == -1073807246:
                self.error_message = "Mono Could not Connect - Loc 2"
            elif eCode == -1073807194 or eCode == -1073807343:
                self.error_message = "Mono Could not Connect - Loc 2"
            elif eCode == -1073807339:
                self.error_message = "Communication with Mono failed - timeout Error"
            print(self.error_message, "Error Code =", eCode)
            self.error_code = eCode
            self.connected = False
        except Exception as err:
            print("Unknown Error - Mono")
            print('Error: ' + str(err))
            print(str(sys.exc_info()[0]))
            print(str(sys.exc_info()[1]))
            print(str(sys.exc_info()[2]))
            self.error_code = 1
            self.connected = False
        self.close_visa()

    def initialize_mono(self):
        """ This one has the code for the rest of the initialization (homing, etc.) """
        self.status_message = 'Establishing Communications'
        self.establish_comms()
        self.status_message = 'Communications Established'
        print('comms established')
        if self.error_code == 1:
            print('error_code was 1')
            self.status_message = self.error_message
            return
        elif self.error_code == 0:
            print('error_code was 0')
            # This is the "communication success" section
            self.status_message = 'Homing Monochromator'
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
            self.status_message = 'Homing Complete, Setting Current Position = 0 nm'
            time.sleep(0.25)
            self.set_zero_position()
            time.sleep(0.25)
            time.sleep(0.25)
        else:
            self.status_message = self.error_message
            return
        print('--------------------------------------------------------------------------------------')

    def go_to_wavelength(self, destination, speed, backlash_amount, backlash_bool):
        # Decide which direction the move is:
        # print('current wavelength: ' + str(self.current_wavelength))
        self.status_message = 'Moving to ' + str(destination) + ' nm'
        print('Moving to: ' + str(destination))
        if destination < self.current_wavelength:
            direction = 'Down'
        elif destination > self.current_wavelength:
            direction = 'Up'
        else:
            self.status_message = 'No Wavelength Change Requested'
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
        if self.connected:
            num_steps = round(amount_nm * self.k_number)
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
            try:
                # Response to this will be before_str = 'b\r\r\n' and after_str = '0\r\n*' (0 may be 0,1,2, or 5, where
                # 0 indicates motion is complete')
                [before_str, after_str] = self.readout.split('X,-8,', 1)
            except ValueError as err:  # In the case that there is only one output (parse string not found)
                try:
                    before_str = self.readout.split('X,-8', 1)[0]
                    after_str = ''  # Might it be better to use a 0?
                    print('Pretty sure this shouldnt have happened')
                except ValueError as err:   # In case somehow there was a different issue
                    print('Not sure how this happened, move_cfm aborted')
                    print(str(sys.exc_info()[0]))
                    print(str(sys.exc_info()[1]))
                    print(str(sys.exc_info()[2]))
                    self.close_visa()
                    return

            try:
                # The prefix r is to force the search string to be treated as "raw" rather than escape sequence
                before_str_2 = after_str.split(r'\r\n', 1)[0]  # We don't need the after string here
            except ValueError as err:
                print('Not sure how this happened, move_cfm aborted')
                self.close_visa()
                print(str(sys.exc_info()[0]))
                print(str(sys.exc_info()[1]))
                print(str(sys.exc_info()[2]))
                return

            try:
                move = int(before_str_2)  # To match the labview, 0 must be output if non-numeric/empty string remains
            except ValueError:
                #move = 0
                print('Value error on trying to convert to int')
                print(str(sys.exc_info()[0]))
                print(str(sys.exc_info()[1]))
                print(str(sys.exc_info()[2]))
                return

            if move == 0:
                move_bool = True
            else:
                move_bool = False

            if move_bool is True and i > 6:
                move_done_bool = True
            else:
                move_done_bool = False

            if move_done_bool is True or self.error_code != 0:  # A stop button may also be added here?
                self.in_motion = False
                break

            if i >= (self.move_cfm_iteration_timeout - 1):
                self.status_message = 'Initialization Failed'
                print(str(self.status_message))
                self.error_code = 1
                self.error_message = self.status_message
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

            r_number = round(speed * self.k_number)
            tmp_string = ('X' + str(r_number) + 'R')
            self.speed = speed

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

    def get_current_pos(self):
        # self.open_visa()   # Is this needed?
        self.write_str('X-1?', read=True)
        # self.close_visa()

        response = self.readout
        partially_parsed = response.split('X,-1,', 1)[1]
        current_step_position = partially_parsed.split(r'\r\n', 1)[0]
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
        if self.connected:
            try:
                self.comm.write(str(command))
                time.sleep(0.1)

                if read is True:
                    num_bytes = self.comm.bytes_in_buffer
                    self.readout = str(self.comm.read_bytes(num_bytes))
                    print('readout: ' + str(self.readout))

                else:
                    self.readout = None
                self.error_message = "Command Sent"
                self.error_code = 0

            except pyvisa.VisaIOError as eCode:
                eCode = str(eCode)
                eCode = eCode.partition("(")[2]
                eCode = eCode.partition(")")[0]
                eCode = int(eCode)
                if eCode == -1073807298:
                    self.error_message = "Could not Connect - Loc 3"
                elif eCode == -1073807246:
                    self.error_message = "Could not Connect - Loc 3"
                elif eCode == -1073807194 or eCode == -1073807343:
                    self.error_message = "Could not Connect - Loc 3"
                elif eCode == -1073807339:
                    self.error_message = "Communication failed - timeout Error"
                print("Error Code =", eCode)
                self.error_code = eCode
                self.connected = False
                self.readout = None

            except:
                self.error_message = "unknown error"
                print(self.error_message)
                print(str(sys.exc_info()[0]))
                print(str(sys.exc_info()[1]))
                print(str(sys.exc_info()[2]))
                self.error_code = 1
                self.connected = False
                self.readout = None
        else:
            self.error_message = "Write Aborted - Device Communication Not Established"
            print(self.error_message)
            self.error_code = 1
            self.readout = None
        print('made it to the end of write_str')
        # End IF statement-------
        return  # self.connected, self.readout, self.error_message, self.error_code
    # End write to Mono --------------------------------------------------------

    def open_visa(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()

        ## Catch Exceptions
        self.error_code = 1
        try:
            self.comm = rm.open_resource(self.resource, baud_rate=9600, data_bits=8,
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

        except pyvisa.VisaIOError as eCode:
            eCode = str(eCode)
            eCode = eCode.partition("(")[2]
            eCode = eCode.partition(")")[0]
            self.error_message = ("Mono Could not Connect - Loc 1" + eCode)
            eCode = int(eCode)
            print(eCode)
            return self.error_message

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
        if self.groove_density == 2400:
            self.k_number = 64
        elif self.groove_density == 1800:
            self.k_number = 48
        elif self.groove_density == 1200:
            self.k_number = 32
        elif self.groove_density == 600:
            self.k_number = 16
        elif self.groove_density == 300:
            self.k_number = 8
        elif self.groove_density == 150:
            self.k_number = 4
        # End get_k_number--------------

    def convert_wl_to_steps_absolute(self, wavelength):
        steps = round((wavelength - self.calibration_wavelength) * self.k_number)
        steps = int(steps)
        return steps

    def convert_steps_absolute_to_wavelength(self, steps):
        wavelength = ((steps / self.k_number) + self.calibration_wavelength)
        return wavelength
#--------------------------END CLASS DEFINITIONS-------------------------------


