import numpy as np
import pyvisa
import sys
import time
from pyvisa.constants import VI_WRITE_BUF_DISCARD, VI_READ_BUF_DISCARD
from PyQt5 import QtCore
import zhinst
import zhinst.utils

#TODO:
# 1. Get all the important settings incorporated
# 2. Incorporate into the GUI
# 3. Mimic existing instrument control scripts
# 4. Get poll working and consistent with the data collection for the other lock-ins
# 5. Figure out how to check for errors

class ErrorCluster:
    def __init__(self, status=False, code=0, details=''):
        self.status = status
        self.code = code
        self.details = details

class DemodulatorSettings:
    def __init__(self):
        self.idx = None
        self.sigin = None
        self.inpz = None
        self.range = None
        self.coupling = None
        self.ref_mode = None
        self.osc_idx = None
        self.filter_order_idx = None
        self.time_constant = None
        self.data_out_idx = None

class ZiLockinSettings:
    def __init__(self, props=None):
        # The ones I think are important:
        self.demod1 = DemodulatorSettings()
        self.demod2 = DemodulatorSettings()

        # Copied some from other lockin script:

        self.outputs = None
        self.settling_delay_factor = None
        self.sensitivity = None
        self.filter_slope = None
        # self.time_constant = None
        # self.time_constant_value = None
        self.sampling_rate = None
        self.input_impedance = None
        self.reference_impedance = None
        self.reference_source = None
        self.twoF_detect_mode = None
        self.harmonic = None
        self.phase = 0
        self.expand = None

        self.sens_list = None
        self.tc_list = None
        self.tc_numeric_list = None
        self.slope_list = None

        # These were specific for this one
        self.out_channel = 0
        if props is not None:
            self.out_mixer_channel = zhinst.utils.default_output_mixer_channel(props)
        self.in_channel = 0
        self.demod_index = 3  # Only demodulator 4 and 8 can use external referencing (index 3 and 7)
        self.osc_index = 0  # demodulator 4 is tied to oscillator 1
        self.demod_rate = 10e3
        self.time_constant = 1e-6
        self.settling_factor = 10
        self.amplitude = 0.1
        self.filter_order = 3  # 3 is 18 dB/oct


class ZiLIA(QtCore.QObject):
    send_error_signal = QtCore.pyqtSignal(object)
    property_updated_signal = QtCore.pyqtSignal([str, int], [str, float])
    tc_updated_primary_signal_zi = QtCore.pyqtSignal(float)
    tc_updated_secondary_signal_zi = QtCore.pyqtSignal(float)
    settings_checked_signal = QtCore.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(ZiLIA, self).__init__(*args, **kwargs)
        print('Instantiation begins')
        self.error = ErrorCluster()

        self.connected = False
        self.comms = None

        self.error = ErrorCluster(status=True, code=9999,
                                  details='Communications with UHF LI have not yet been established\n')
        # self.settings = LockinSettings()

        self.rm = pyvisa.ResourceManager()

    def start_comms(self, device_id='dev2025'):
        api_level = 6   # This is required for the UHF instrument
        err_msg = "Only supports instruments with demodulators"

        try:
            print('starting comms')
            # connect to the instrument
            # self.daq is the actual communication object, self.device and props are both attributes related to the communications
            (self.daq, self.device, props) = zhinst.utils.create_api_session(
                device_id, api_level, required_devtype=".*LI|.*IA|.*IS", required_err_msg=err_msg
            )

            zhinst.utils.api_server_version_check(self.daq)

            self.settings = ZiLockinSettings(props)
            # Set self.device configuration ----------------------------------
            print('setting settings')
            # Create a base configuration: Disable all available outputs, awgs, demods, scopes,...
            zhinst.utils.disable_everything(self.daq, self.device)

            # Settings are specified by a "path" and a "value". Path IDs the setting name and value is what it sounds like
            # ex: ['/dev2025/sigouts/1/on', 1] is a [path, value] pair.
            # Must be a list of pair(s)
            demod = self.settings.demod_index
            sig_in = self.settings.in_channel
            exp_setting = [
                ["/%s/sigins/%d/ac" % (self.device, sig_in), 0],   # not AC coupling (no highpass filter)
                ["/%s/sigins/%d/range" % (self.device, sig_in), 1.5],  # Init to max so no overloads
                ["/%s/demods/%d/enable" % (self.device, demod), 1],  # Enable the demodulator
                ["/%s/demods/%d/rate" % (self.device, demod), self.settings.demod_rate],  # Data transfer rate
                ["/%s/demods/%d/adcselect" % (self.device, demod), sig_in],               # Demod input signal
                ["/%s/demods/%d/order" % (self.device, demod), self.settings.filter_order],  # Sets LPF slope (6 dB/oct -> 48)
                ["/%s/demods/%d/timeconstant" % (self.device, demod), self.settings.time_constant],
                ["/%s/demods/%d/oscselect" % (self.device, demod), self.settings.osc_index],   # Seems unnecessary. Unsure
                ["/%s/demods/%d/harmonic" % (self.device, demod), 1],            # Measure at the fundamental
            ]
            self.daq.set(exp_setting)

            # time.sleep(self.settings.settling_factor * self.settings.time_constant_value)

            self.daq.sync()
            self.error = ErrorCluster(status=False, code=0, details='')
            did_comms_fail = False
            self.connected = True

        except RuntimeError as err:
            self.error = ErrorCluster(status=True, code=9000,
                                      details='Could not connect to UHF LI\n' + str(err))
            self.send_error_signal.emit(self.error)
            did_comms_fail = True
            self.connected = False
        except Exception as err:
            self.error = ErrorCluster(status=True, code=9001,
                                      details='Could not connect to UHF LI\n' + str(err))
            self.send_error_signal.emit(self.error)
            did_comms_fail = True
            self.connected = False
        return did_comms_fail

    def get_current_settings(self, demodulator):
        demod_idx = demodulator - 1

        if demod_idx > 3:
            osc_idx = 1
        else:
            osc_idx = 0

        input_idx = int(self.daq.getDouble("/%s/demods/%d/adcselect" % (self.device, demod_idx)))

        if demod_idx == 3:
            tf_ext_trig = bool(self.daq.getDouble("/%s/extrefs/%d/enable" % (self.device, 0)))
            automode_idx = int(self.daq.getDouble("/%s/extrefs/%d/automode" % (self.device, 0)))
        elif demod_idx == 7:
            tf_ext_trig = bool(self.daq.getDouble("/%s/extrefs/%d/enable" % (self.device, 1)))
            automode_idx = int(self.daq.getDouble("/%s/extrefs/%d/automode" % (self.device, 1)))
        else:
            tf_ext_trig = False
            automode_idx = 0

        current_settings = {
            "input_idx": input_idx,
            "tf_50ohm": bool(self.daq.getDouble("/%s/sigins/%d/imp50" % (self.device, input_idx))),
            "range": self.daq.getDouble("/%s/sigins/%d/range" % (self.device, input_idx)),
            "coupling": int(self.daq.getDouble("/%s/sigins/%d/ac" % (self.device, input_idx))),
            "tf_ext_trig": tf_ext_trig,
            "automode_idx": automode_idx,
            "ref_freq": self.daq.getDouble("/%s/oscs/%d/freq" % (self.device, osc_idx)),
            "harmonic": int(self.daq.getDouble("/%s/demods/%d/harmonic" % (self.device, demod_idx))),
            "phase": self.daq.getDouble("/%s/demods/%d/phaseshift" % (self.device, demod_idx)),
            "filter_order": int(self.daq.getDouble("/%s/demods/%d/order" % (self.device, demod_idx))) - 1,
            "time_constant": self.daq.getDouble("/%s/demods/%d/timeconstant" % (self.device, demod_idx)),
            "tf_sinc_filter": bool(self.daq.getDouble("/%s/demods/%d/sinc" % (self.device, demod_idx)))
        }
        print('Current Settings\n' + str(current_settings))
        self.settings_checked_signal.emit(current_settings)
        return current_settings

    def save_settings(self, filename):
        if filename is not None:
            print("Saving settings...")
            zhinst.utils.save_settings(self.daq, self.device, filename)
            print("Done.")

    def load_settings(self, filename):
        # Load settings.
        if filename is not None:
            print("Loading settings...")
            zhinst.utils.load_settings(self.daq, self.device, filename)
            print("Done.")

    def collect_sample(self):
        # Perform a "global synchronization". Must happen AFTER low-pass settling delay
        self.daq.sync()
        # Obtain one demodulator sample via ziself.daqServer's low-level getSample()
        # method - for extended data acquisition it's preferable to use
        # ziDAQServer's poll() method or the ziDAQRecorder class.

        sample = self.daq.getSample("/%s/demods/%d/sample" % (self.device, self.settings.demod_index))
        # Calculate the demodulator's magnitude and phase and add them to the sample
        # dict.
        sample["R"] = np.abs(sample["x"] + 1j * sample["y"])
        sample["theta"] = np.angle(sample["x"] + 1j * sample["y"], deg=True)
        print(f"Measured RMS amplitude is {sample['R'][0]:.3e} V.\n"
              f"Phase is {sample['theta'][0]:.3e} Degrees")
        for key in sample:
            sample[key] = sample[key][0]

        return sample

    def record_data(self, duration):
        # First check that all settings are correct

        # Unsubscribe any streaming data.
        self.daq.unsubscribe("*")

        # Wait for the demodulator filter to settle.
        time.sleep(self.settings.settling_factor * self.settings.time_constant)

        # Perform a global synchronisation between the device and the data server:
        # Ensure that 1. the settings have taken effect on the device before issuing
        # the poll() command and 2. clear the API's data buffers. Note: the sync()
        # must be issued after waiting for the demodulator filter to settle above.
        self.daq.sync()

        # Subscribe to the demodulator's sample node path.
        path = "/%s/demods/%d/sample" % (self.device, self.settings.demod_index)
        self.daq.subscribe(path)

        # Poll the subscribed data from the data server. Poll will block and record
        # for poll_length seconds. (any data stored since the subscribe command will also be recorded)
        poll_length = duration  # [s]
        poll_timeout = 500  # [ms]
        poll_flags = 0
        poll_return_flat_dict = True
        data = self.daq.poll(poll_length, poll_timeout, poll_flags, poll_return_flat_dict)

        # Unsubscribe from all paths.
        self.daq.unsubscribe("*")

        sample = data[path]
        x_data = sample['x']
        y_data = sample['y']
        x_ave = np.average(x_data)
        y_ave = np.average(y_data)
        return x_ave, y_ave

    def change_setting(self):
        pass

    def auto_sens(self):
        pass

    def check_for_errors(self):
        pass

    def toggle_output(self, which_output=0, state=0):
        command = [["/%s/sigouts/%d/on" % (self.device, which_output), state]]
        self.daq.set(command)

    # def update_tc(self, demod_idx, tc):
    #     exp_setting = [
    #         ["/%s/demods/%d/timeconstant" % (self.device, demod_idx), self.settings.time_constant]
    #     ]
    #     self.daq.set(exp_setting)
    #
    #     tc_out = self.daq.getDouble("/%s/demods/%d/timeconstant" % (self.device, demod_idx))
    #     return tc_out

    def set_input(self, demod_idx, input_idx):
        exp_setting = [
            ["/%s/demods/%d/adcselect" % (self.device, demod_idx-1), input_idx],  # Demod input signal
        ]
        self.daq.set(exp_setting)

    def set_range(self, input_idx, input_range):
        exp_setting = [
            ["/%s/sigins/%d/range" % (self.device, input_idx), input_range]
        ]
        self.daq.set(exp_setting)

    def set_input_impedance(self, input_idx, desired_imp_idx):
        if desired_imp_idx == 0:
            is_50_ohm = 1
        elif desired_imp_idx == 1:
            is_50_ohm = 0

        exp_setting = [
            ["/%s/sigins/%d/imp50" % (self.device, input_idx), is_50_ohm]
        ]
        self.daq.set(exp_setting)

    def set_input_coupling(self, input_idx, desired_coupling_idx):
        exp_setting = [
            ["/%s/sigins/%d/ac" % (self.device, input_idx), desired_coupling_idx]
        ]
        self.daq.set(exp_setting)

    def set_harmonic(self, demod_idx=4, harmonic=1):
        exp_setting = [
            ["/%s/demods/%d/harmonic" % (self.device, demod_idx-1), harmonic]
        ]
        self.daq.set(exp_setting)

    def set_phase(self, demod_idx=4, target_phase=0):
        exp_setting = [
            ["/%s/demods/%d/phaseshift" % (self.device, demod_idx-1), target_phase]
        ]
        self.daq.set(exp_setting)

    def set_filter_order(self, demod_idx=4, filter_order=3):
        exp_setting = [
            ["/%s/demods/%d/order" % (self.device, demod_idx - 1), filter_order]
        ]
        self.daq.set(exp_setting)

    def set_time_constant(self, tf_primary=True, demod_idx=4, target_tc=0.1):
        exp_setting = [
            ["/%s/demods/%d/timeconstant" % (self.device, demod_idx-1), target_tc]
        ]
        self.daq.set(exp_setting)

        tc_out = self.daq.getDouble("/%s/demods/%d/timeconstant" % (self.device, demod_idx-1))

        if tf_primary:
            self.tc_updated_primary_signal_zi.emit(tc_out)
        elif not tf_primary:
            self.tc_updated_secondary_signal_zi.emit(tc_out)

    def toggle_sinc_filter(self, demod_idx=4, tf_enable_sinc=False):
        exp_setting = [
            ["/%s/demods/%d/sinc" % (self.device, demod_idx - 1), tf_enable_sinc]
        ]
        self.daq.set(exp_setting)

    def set_ref_freq(self, demod_idx=4, target_freq=100E3):
        if 1 <= demod_idx <= 4:
            osc_idx = 0
        elif 4 < demod_idx:
            osc_idx = 1

        exp_setting = [
            ["/%s/oscs/%d/freq" % (self.device, osc_idx), target_freq]
        ]
        self.daq.set(exp_setting)

    def set_mode(self, demod_idx=4, trigger_mode_idx=1):
        """
        If demodulator 4 is used, external reference must be connected at Ref 1 (ext_ref_idx=0).
        If demodulator 8 is used, external reference must be connected at Ref 2 (ext_ref_idx=1).
        """
        if demod_idx == 4:
            ext_ref_idx = 0
        elif demod_idx == 8:
            ext_ref_idx = 1

        if trigger_mode_idx == 0:
            # "Manual" (Internal) Triggering
            exp_setting = [
                ["/%s/extrefs/%d/enable" % (self.device, ext_ref_idx), 0]
            ]
        elif trigger_mode_idx == 1:
            # External Triggering, automatic bandwidth selection
            exp_setting = [
                ["/%s/extrefs/%d/enable" % (self.device, ext_ref_idx), 1],
                ["/%s/extrefs/%d/automode" % (self.device, ext_ref_idx), 4]
            ]
        elif trigger_mode_idx == 2:
            exp_setting = [
                ["/%s/extrefs/%d/enable" % (self.device, ext_ref_idx), 1],
                ["/%s/extrefs/%d/automode" % (self.device, ext_ref_idx), 2]
            ]
        elif trigger_mode_idx == 3:
            exp_setting = [
                ["/%s/extrefs/%d/enable" % (self.device, ext_ref_idx), 1],
                ["/%s/extrefs/%d/automode" % (self.device, ext_ref_idx), 3]
            ]

        self.daq.set(exp_setting)

    def update_all(self):
        zhinst.utils.disable_everything(self.daq, self.device)

        # Settings are specified by a "path" and a "value". Path IDs the setting name and value is what it sounds like
        # ex: ['/dev2025/sigouts/1/on', 1] is a [path, value] pair.
        # Must be a list of pair(s)
        demod = self.settings.demod_index
        sig_in = self.settings.in_channel
        exp_setting = [
            ["/%s/sigins/%d/imp50" % (self.device, sig_in), 1],
            ["/%s/sigins/%d/ac" % (self.device, sig_in), 0],  # not AC coupling (no highpass filter)
            ["/%s/sigins/%d/range" % (self.device, sig_in), 1.5],  # Init to max so no overloads
            ["/%s/demods/%d/enable" % (self.device, demod), 1],  # Enable the demodulator
            ["/%s/demods/%d/rate" % (self.device, demod), self.settings.demod_rate],  # Data transfer rate
            ["/%s/demods/%d/adcselect" % (self.device, demod), sig_in],  # Demod input signal
            ["/%s/demods/%d/order" % (self.device, demod), self.settings.filter_order],
            # Sets LPF slope (6 dB/oct -> 48)
            ["/%s/demods/%d/timeconstant" % (self.device, demod), self.settings.time_constant],
            ["/%s/demods/%d/oscselect" % (self.device, demod), self.settings.osc_index],  # Seems unnecessary. Unsure
            ["/%s/demods/%d/harmonic" % (self.device, demod), 1],  # Measure at the fundamental
        ]
        self.daq.set(exp_setting)

        # Read the actual settings and update self.settings to match
        tc_out = self.daq.getDouble("/%s/demods/%d/timeconstant" % (self.device, demod))

        print('Actual time constant: ' + str(tc_out))
        self.settings.time_constant_value = tc_out
