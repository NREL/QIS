import numpy as np
import pyvisa
import socket
from padmr.instr.cryostat import CryostationComm
import sys
import time
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore
from typing import Union
from decimal import Decimal
#TODO: stability_max_time might be referenced before assignment


class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details


class CryostatSettings:
    def __init__(self):
        self.connected = False
        #temp
        self.target_cooldown_platform_temp = None
        self.target_platform_stability = None
        self.temp_stepup_size = None
        self.maximum_platform_stepup_target_temp = None
        self.cooldown_timeout = None
        self.stepup_timeout = None
        self.stability_timeout = None
        self.current_temp = None
        self.enable_status = None

        # Field
        self.current_field = None


class CryostatInstr(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    freq_changed_signal = QtCore.pyqtSignal(str)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])

    def __init__(self, *args, **kwargs):
        """

        """
        super(CryostatInstr, self).__init__(*args, **kwargs)
        self.error = {'Status': False, 'Code': 0, 'Details': ''}
        self.error = ErrorCluster(status=True, code=7999, details='Communication with cryostat has not been established')

        self.settings = CryostatSettings()

        self.comms = None

    def start_comms(self, cryostation_ip='169.254.65.20', cryostation_port='7773'):
        try:
            self.comms = CryostationComm.CryoComm(cryostation_ip, cryostation_port)
            self.error = ErrorCluster(status=False, code=0, details='')
            return False
        except Exception as err:
            self.error = ErrorCluster(status=True, code=7000,
                                      details='Error establishing communication with Cryostation.\n' + str(err))
            self.send_error_signal.emit(self.error)
            return True

    def enable_magnet(self):
        print('Attempting to enable Magnet')
        if self.error.status:
            print('preexisting cryostat error prevents enabling magnet')
            self.error = ErrorCluster(status=True, code=7015,
                                      details='Could not enable magnet due to preexisting error.\n')
            enabled = False
        elif not self.error.status:
            # First check that the magnet is not already enabled:
            response = self.comms.send_command_get_response('GMS')
            if 'ENABLED' in response:
                enabled = True
                return enabled

            response = self.comms.send_command_get_response('SME')
            print('REsponse: ' + str(response))
            if response.startswith('OK'):
                print('Command sent successfully...')
                if 'DISABLED' in response:
                    print('Magnet communicated normally but status is \"DISABLED\"')
                    enabled = False
                elif 'ENABLED' in response:
                    print('Magnet enabled')
                    enabled = True
                else:
                    print('e.g. Safe Mode')
                    enabled = False
            else:
                print('error case 7016')
                self.error = ErrorCluster(status=True, code=7016,
                                          details='Could not enable magnet. Cryostat response:\n' + response + '\n')
                self.send_error_signal.emit(self.error)
                enabled = False
        return enabled

    def disable_magnet(self):
        print('Attempting to disable magnet')
        if self.error.status:
            print('preexisting cryostat error prevents disabling magnet')
            self.error = ErrorCluster(status=True, code=7017,
                                      details='Could not enable magnet due to preexisting error.\n')
            return
        elif not self.error.status:
            response = self.comms.send_command_get_response('SMD')
            print('Response: ' + str(response))
            if response.startswith('OK'):
                if 'DISABLED' in response:
                    print('Magnet disabled')
                    enabled = False
                elif 'ENABLED' in response:
                    # I think this will never happen
                    print('Magnet communicated normally but status is \"ENABLED\"')
                    enabled = True
            else:
                print('error case 7018')
                self.error = ErrorCluster(status=True, code=7018,
                                          details='Could not disable magnet. Cryostat response:\n' + response + '\n')
                self.send_error_signal.emit(self.error)

    def set_field(self, target_field):
        # Check that the input is valid
        if type(target_field) is not (float or int):
            try:
                target_field = float(target_field)
            except Exception as err:
                self.error = ErrorCluster(status=True, code=7011,
                                          details='Could not set field due to invalid input type.\n' + str(err))
                self.send_error_signal.emit(self.error)
                return

        # Check that there are no pre-existing errors
        if self.error.status:
            print('preexisting cryostat error prevents setting field')
            return
        else:
            # Convert target_field to Tesla, generate command string
            set_point = target_field / 10000
            # Check that field is within allowed range
            if not -2 < set_point < 2:
                self.error = ErrorCluster(status=True, code=7012,
                                          details='Field set point outside of allowed range.\n')
                self.send_error_signal.emit(self.error)
            else:
                print('Conditions met, enabling magnet...')
                com_str = 'SMTF{setp:.6f}'.format(setp=set_point)
                try:
                    # Try to enable the magnet. If it fails, try again a few times before giving up
                    enabled = self.enable_magnet()
                    ii = 0
                    while (not enabled) and ii < 3:
                        enabled = self.enable_magnet()
                        ii += 1

                    if not enabled:
                        print('Magnet failed to enable, cannot set field\n')
                        self.error = ErrorCluster(status=True, code=7019,
                                                  details='Field set point outside of allowed range.\n')
                        self.send_error_signal.emit(self.error)
                        return

                    response = self.comms.send_command_get_response(com_str)
                    print('REsponse: ' + str(response))
                    if response.startswith('OK'):
                        self.settings.current_field = 10000 * float(self.comms.send_command_get_response('GMTF'))
                        self.property_updated_signal.emit('current_field', self.settings.current_field)
                    else:
                        print('error case 1')
                        self.error = ErrorCluster(status=True, code=7013,
                                                  details='Could not set field. Cryostat response:\n' + response + '\n')
                        self.send_error_signal.emit(self.error)
                except Exception as err:
                    self.error = ErrorCluster(status=True, code=7014,
                                              details='Could not set field.\n' + str(err))
                    self.send_error_signal.emit(self.error)
        return

    def check_instrument(self):
        pass

    def set_target_platform_temp(self, set_point, timeout=10):
        """
        Set the target platform temp.
        """

        print("Set target platform temp {0}".format(set_point))

        timeout = time.time() + timeout  # Determine timeout

        target_temp = self.send_target_platform_temp(set_point)

        while round(target_temp, 2) != round(set_point, 2):
            if timeout > 0:
                if time.time() > timeout:  # If we pass the timeout, give up.
                    self.error = ErrorCluster(status=True, code=7001,
                                              details='Error setting target platform temp.\n')
                    self.send_error_signal.emit(self.error)
                    return False
            time.sleep(1)
            target_temp = self.send_target_platform_temp(set_point)

        return True

    def send_target_platform_temp(self, set_point):
        """
        Send the target platform temp to the Cryostation.  Read it back to verify the set operation
        """

        print("Send target platform temp {0}".format(set_point))

        target_temp_decimal = 0.0
        target_temp_string = ''

        try:
            if self.comms.send_command_get_response("STSP" + str(set_point)).startswith("OK"):
                target_temp_string = self.comms.send_command_get_response("GTSP")
        except Exception as err:
            self.error = ErrorCluster(status=True, code=7002,
                                      details='Failed to send target platform temp.\n' + str(err))
            self.send_error_signal.emit(self.error)

        try:
            target_temp_decimal = Decimal(target_temp_string)
        except Exception as err:
            target_temp_decimal = 0.0
        return target_temp_decimal

    def initiate_cooldown(self):
        """
        Set the target platform temp and initiate cooldown.
        """

        print("Set cooldown target temp")
        if not self.set_target_platform_temp(self.comms, self.settings.target_cooldown_platform_temp):
            self.error = ErrorCluster(status=True, code=7003,
                                      details='Timeout while setting cooldown target platform temp.\n')
            self.send_error_signal.emit(self.error)

        print("Initiate cooldown")
        try:
            if self.comms.send_command_get_response("SCD") != "OK":
                self.error = ErrorCluster(status=True, code=7004,
                                          details='Failed to initiate cooldown.\n')
                self.send_error_signal.emit(self.error)
        except Exception as err:
            self.error = ErrorCluster(status=True, code=7005,
                                      details='Failed to initiate cooldown.\n' + str(err))
            self.send_error_signal.emit(self.error)

    def wait_for_cooldown_and_stability(self):
        """
        Wait for the Cryostation system to cooldown and stabilize.
        """

        print("Wait for cooldown temp")
        if self.settings.cooldown_timeout > 0:  # If cooldown timeout enabled
            cooldown_max_time = time.time() + self.settings.cooldown_timeout  # Determine cooldown timeout
        while True:
            time.sleep(3)
            if self.settings.cooldown_timeout > 0:
                if time.time() > cooldown_max_time:  # If we pass the cooldown timeout, give up.
                    self.error = ErrorCluster(status=True, code=7006,
                                              details='Failed to initiate cooldown.\n')
                    self.send_error_signal.emit(self.error)
                    return False
            try:
                self.current_temp = float(self.comms.send_command_get_response("GPT"))
            except Exception as err:
                self.current_temp = 0.0
            if self.settings.target_cooldown_platform_temp >= self.current_temp > 0:
                # Wait until platform temp reaches target
                break

        print("Wait for cooldown stability")
        if self.settings.stability_timeout > 0:  # If stability timeout enabled
            stability_max_time = time.time() + self.settings.stability_timeout  # Determine stability timeout
        while True:
            time.sleep(3)
            if self.settings.stability_timeout > 0:
                if time.time() > stability_max_time:  # If we pass the stability timeout, give up.
                    self.error = ErrorCluster(status=True, code=7007,
                                              details='Timed out while waiting for cooldown to stabilize.\n')
                    self.send_error_signal.emit(self.error)
                    return False
            try:
                current_stability = float(self.comms.send_command_get_response("GPS"))
            except Exception as err:
                current_stability = 0.0
            if self.settings.target_platform_stability >= current_stability > 0:
                # Wait until platform stability reaches target
                return True

    def step_up(self):
        """
        Step-up the temp, waiting for stability at each step.
        """

        self.current_temp = 0.0

        # Get current target to step-up from
        step_target = -1.0
        while step_target < 0:
            try:
                step_target = float(self.comms.send_command_get_response("GTSP"))  # Get target set point
            except Exception as err:
                step_target = -1.0
            time.sleep(1)

        # Calculate initial step-up target
        step_target += self.settings.temp_stepup_size
        # Step-up until the maximum is reached
        while round(step_target, 2) <= round(self.settings.maximum_platform_stepup_target_temp, 2):

            # Set the step-up target platform temp
            print("\nStep-up the target platform temp")
            if not self.set_target_platform_temp(self.comms, step_target):
                self.error = ErrorCluster(status=True, code=7008,
                                          details='Timed out while setting step-up target platform temp {0}\n'.format(step_target))
                self.send_error_signal.emit(self.error)
                return

            # Wait for the step-up target platform temp to be reached
            print("Wait for step-up target temp of {0}".format(step_target))
            if self.settings.stepup_timeout > 0:  # If step-up timeout enabled
                stepup_max_time = time.time() + self.settings.stepup_timeout  # Determine step-up timeout
            while True:
                if self.settings.stepup_timeout > 0:
                    if time.time() > stepup_max_time:  # If we pass the timeout, give up.
                        self.error = ErrorCluster(status=True, code=7009,
                                                  details='Timed out waiting for step-up target platform temp\n')
                        self.send_error_signal.emit(self.error)
                        return False
                try:
                    self.current_temp = float(self.comms.send_command_get_response("GPT"))
                except Exception as err:
                    self.current_temp = 0.0
                if self.current_temp >= step_target and self.current_temp > 0.0:
                    break
                time.sleep(3)

            # Wait for the step-up target platform temp to stabilize
            print("Wait for step-up target temp stability")
            if self.settings.stability_timeout > 0:  # If stability timeout enabled
                stability_max_time = time.time() + self.settings.stability_timeout  # Determine stability timeout
            while True:
                if self.settings.stability_timeout > 0:
                    if time.time() > stability_max_time:  # If we pass the timeout, give up.
                        self.error = ErrorCluster(status=True, code=7010,
                                                  details='Timed out waiting for target platform stability\n')
                        self.send_error_signal.emit(self.error)
                        return False
                try:
                    current_stability = float(self.comms.send_command_get_response("GPS"))
                except Exception as err:
                    current_stability = 0.0
                if self.settings.target_platform_stability >= current_stability > 0.0:
                    break
                time.sleep(3)

            # Calculate next step-up target
            step_target += self.settings.temp_stepup_size

        return True


if __name__ == '__main__':
    test_instr = CryostatInstr()
    cryostat_ip = "123"
    cryostat_port = 7773
    comms_failure = test_instr.start_comms(cryostat_ip, cryostat_port)
    if comms_failure:
        print('Comms Failure')
