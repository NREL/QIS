#TODO:
# Critical:
# -10. Merge lock-in settings that are shared (like sampling rate)
# -9. Reoptimize lock-in parameters (like sensitivity) after every frequency change (make this a setting?)
# -8. Lock-in delay should be scaled by a factor chosen by the user in settings (usually 10x time constant)
# -7. Get all massive lock-in write/updates into the control module instead of this main window script
# -6. Associate an attribute with every lockin attribute. In that module.
# -5. Should I incorporate a "serial poll" type approach to the errors? (i.e. each bit means something different)
# -4. Incorporate the frequency mismatch warning into a window (At the end of the experiment?)
# -3. Incorporate better error handling into the CG635 module
# -2. Aggressive precision on floats will be a problem since the last digits may be random values(eg.25.000000000000007)
# -1. Laser initialization tests should be updated at the settings window.
# 0. Add laser on indicator light to the MAIN Window as well.
# 0. Add a "check for connectivity" error handler for functions which require it. (e.g. using self.cg635_connected)
# 0a. self.cg635_connected may be better as self.cg635.connected (attribute of the instrument)
# 1. Figure out how to remove dependency-type conflicts (e.g. several instrument control programs have separate Worker
# classes. Importing just the dominant class will probably cause issues)
# 2. Incorporate the mono control functionality
# 3. Each instrument should have it's own error attribute with the same name and type
# (e.g. self.cg635.err, self.toptica.err, which are either None or an integer
# 4. Error checking should be more frequent. All new visa operations should require error input and generate output
# 3. Test the CG635 stuff and finish integrating it
# 4. Incorporate a scan probe wavelength (at set pump mod frequency) option (TA Spectrum)
# 7. Get all the settings windows buttons to work
# 9. Incorporate an "if ...connected" before "set params"
# 10. Get slots for all the CG635 signals (make CG635 control module)
# Niceties:
# 0. Delete the "cancel" button in the settings (a "restore this tab" to default would be better)
# 1. Add live error bars could be put on each point based on standard deviation or something.
# This would be awesome for knowing when to stop an experiment
# 2. Live fitting with uncertainties would be a nice feature
# 3. Add units (and more useful titles) to the column headers (not "Channel 1" and "Channel 2"
# 3. Add a "hide current scan" and/or "hide average scan" to clean up the plot
# 3. Add icons to "constants" to simplify experiment setup (like a thermometer for temp, rainbow for wl, etc)
# 4. Incorporate indicators to show which devices are communicating (also which ones are outputting e.g. laser, u-waves)
# 5. Get displayed steps to print with fewer sig figs
# 6. Find rounding parameters that work for all experiment configurations
# 7. Consider reworking the monocontrol scripts so that everything needed here is in the control module (so importing
# the mono_control_main is only used for single instrument control) (at the least rename the slots so they make more
# sense in the context of this program)
# 8. Get "set_plot_params" fn to do all of the plotting label stuff.
# 9. Make all relevant __init__ properties into settings/ presets instead (put all relevant settings into .ini file
# 10. Make it so the plot doesn't have insane axis limits when 0s are in start and end
# ------------------- AT HOME--------------------------
# 2. Reorganize MainWindow to something logical
# 3. Rename com_port and resource_name variables for consistency
# 4. Alter the instrument instantiation system so that all instruments are treated the same. (I think Toptica has it
# closer to right except the traceback functionality in the other systems is pretty nice)
# 5. Format all the control modules in the same way (to the extent that it's possible to do so)

import os
import sys
import pyvisa
import time
import numpy as np
import pyvisa
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pyvisa.constants import VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD, StopBits

from decorator import decorator
import PyQt5

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QThreadPool, QRunnable  # For multithreading (parallel tasks)
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

import MonochromatorControl.mono_control_main
from MonochromatorControl.mono_control_module import MonoDriver
from MonochromatorControl.mono_control_main import MainWindow as MonoControl
from Toptica.toptica_control_module import TopticaInstr

from Lockin_Amplifier.SRS_control_main import LockinWidget
from Lockin_Amplifier.SR_Lockin_using_Prologix_Module import PrologixAdaptedSRLockin
from FullControl.expt_control_ui import Ui_MainWindow as ExptControlMainWindow
from FullControl.help_window_main import HelpWindowForm
from FullControl.settings_window_main import SettingsWindowForm
from FullControl.plotwidget import PlotWidget
from FullControl.cg635_control_module import CG635Instrument


pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))

# This is for multi-threading:
class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    TO USE THREADING, simply use the following syntax, INSTEAD of just calling your function:

        worker = Worker(self.mono_instance.method_name, arg1, arg2, etc.)  # args, kwargs are passed to the run function

        # Execute
        self.thread_pool.start(worker)

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.fn(*self.args, **self.kwargs)


class SaveApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def save_file_dlg(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, file_type = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                          "CSV Files (*.csv);;Text Files (*.txt)", options=options)

        return file_name, file_type

######################################################################

def calc_steps(step_size, start, end):
    num_steps = int(round((np.abs(end - start)) / step_size)) + 1
    step_pts = []
    if start < end:
        for ii in range(0, num_steps):
            step_pts.append(start + ii*step_size)
    else:
        for ii in range(0, num_steps):
            step_pts.append(start - ii*step_size)
    # step_pts_arr = np.array(step_pts)
    return num_steps, step_pts


def calc_step_size(step_count, start, end):
    step_size = np.abs(end - start) / step_count
    return step_size


def error_message_window(text=None, inform_text=None, details=None):
    # print(str(sys.exc_info()[:]))
    # #print(str(sys.exc_info()[1]))
    # #print(str(sys.exc_info()[2]))
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setInformativeText(inform_text)
    msg.setWindowTitle(' - Warning - ')
    msg.setDetailedText(details)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.buttonClicked.connect(msgbtn)
    msg.exec()

def msgbtn(i):
    print('Button Pressed is: ', i.text())


class Presets:              # Presumably I should incorporate these into the Settings file. It seems silly to have both
    def __init__(self):
        self.probe_wl_start = 400
        self.probe_wl_end = 700
        self.probe_wl_num_steps = 31        # self.probe_wl_step_size = 5

        self.pump_mod_freq_start = 25    # kHz
        self.pump_mod_freq_end = 200000
        self.pump_mod_freq_steps = 3    # later set this to 20 or something

        # self.lockin_sampling_rate = 512     # Hertz
        self.lockin_sampling_duration = 1   # Seconds

        self.temperature = 295
        self.static_field = 0
        self.probe_wl = 513
        self.rf_freq = 9.2


class MainWindow(QMainWindow):
    lockin_error_signal = QtCore.pyqtSignal(str)
    general_error_signal = QtCore.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the ui.py file and prepare the UI
        self.ui = ExptControlMainWindow()
        self.ui.setupUi(self)

        # ------------------------------- initialize attribute values - ------------------------------------------------
        # These are attributes of the MainWindow class, not of the ui instance
        # They are used as attributes of the program.
        # Many of these should be settings or presets instead of here
        self.step_pts = None

        self.sr830_connected = False
        self.sr844_connected = False
        self.cg635_connected = False
        self.md2000_connected = False
        self.smb100a_connected = False
        self.montana_instr_connected = False
        self.toptica_connected = False

        # self.cg635 = None
        self.presets = Presets()

        self.abort_scan = False
        self.log_spacing = False         # Change this to be either a preset or a setting?
        self.start = None
        self.end = None
        self.step_count = None
        self.lockin_delay = 0

        self.scaling_pref = 'linear'
        self.x_axis_label = None
        self.axis_1 = self.ui.PlotWidget.canvas.axes_main
        self.axis_2 = self.ui.PlotWidget.canvas.axes_main.twinx()
        self.scan_range = None
        self.output_variables = 'R/Theta'
        self.column_headers = ['Independent Variable', 'Channel 1', 'Channel 2']
        self.abscissa_1 = None

        # ----------------------------- INSTANTIATE LARGE SCALE OBJECTS (CLASSES/WINDOWS) ------------------------------
        # Create the settings window (but don't show it)
        self.settings = SettingsWindowForm()
        self.toptica = TopticaInstr()

        # ---------------------------------- CONNECT INTER-WINDOW SIGNALS AND SLOTS ------------------------------------
        self.lockin_error_signal.connect(self.lockin_error_window)
        self.general_error_signal.connect(self.general_error_window)
        self.settings.update_all_signal.connect(self.update_all_slot)
        self.settings.update_tab_signal.connect(self.update_tab_slot)
        self.settings.cg635_set_freq_signal.connect(self.cg635_set_freq_slot)
        self.settings.connect_instr_signal.connect(self.connect_instruments)
        self.settings.toptica_enable_signal.connect(self.toptica.laser_enable)
        self.settings.toptica_start_signal.connect(self.toptica.laser_start)
        self.settings.toptica_stop_signal.connect(self.toptica.laser_disable)

        # self.settings.update_signal.connect(self.update_slot)
        # self.settings_window.initialize_settings_window()

        # ------------------------------- Initialize GUI Object States -------------------------------------------------

        self.addToolBar(NavigationToolbar2QT(self.ui.PlotWidget.canvas, self), )
        self.ui.log_spacing_checkbox.setChecked(False)
        # --------------------------- Initialize Communications with Instruments ---------------------------------------


        # ------------------------------------ Run any initialization Functions ----------------------------------------

        # ------------------------ MULTI-THREADING STUFF ---------------------------------------------------------------
        self.thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.thread_pool.maxThreadCount())
    # -------------------------------------------NON-SLOT METHODS--------------------------------------------------

    def set_lockin_settings(self):
        #TODO:
        # 1. Add an else case for manual outputs?
        print('attempting to set lockin settings')
        print('First Determine which Lock-in we want to use')
        if self.settings.lockin_model_preference == 'SR830' and self.sr830_connected is True:
            print('SR830 Is Selected')
            # Disable SR844 Stuff
            # Set Settings:
            if self.settings.lockin_outputs == 0:
                print('attempting to set outputs to R and Theta')
                self.lockin.write_string('DDEF 1, 1, 0\n', read=False)
                self.lockin.write_string('DDEF 2, 1, 0\n', read=False)

                # self.lockin.write_string('TRCD 1, 3, 0, 0, 1\n', read=False)
                # self.lockin.write_string('TRCD 2, 4, 0, 0, 1\n', read=False)
            elif self.settings.lockin_outputs == 1:
                print('attempting to set Outputs to X and Y')
                self.lockin.write_string('DDEF 1, 0, 0\n', read=False)
                self.lockin.write_string('DDEF 2, 0, 0\n', read=False)

                # self.lockin.write_string('TRCD 1, 1, 0, 0, 1\n', read=False)
                # self.lockin.write_string('TRCD 2, 2, 0, 0, 1\n', read=False)

            print('setting sensitivity and filter slope')
            self.lockin.write_string('SENS %d; OFSL%d\n' % (self.settings.sr830_sensitivity,
                                                            self.settings.sr830_filter_slope), read=False)

            print('setting the TC')
            print(self.settings.sr830_time_constant)
            self.lockin.write_string('OFLT %d\n' % self.settings.sr830_time_constant, read=False)
            self.lockin.time_constant = self.lockin.tc_options(self.settings.sr830_time_constant)

            print('seting dynamic reserve')
            self.lockin.write_string('RMOD %d\n' % self.settings.sr830_dyn_reserve_mode, read=False)

            print('setting the sampling rate')
            self.lockin.write_string('SRAT %d\n' % self.settings.sr830_sampling_rate, read=False)

            print('Setting Ref source')
            self.lockin.write_string('FMOD %d\n' % self.settings.sr830_ref_source, read=False)

            print('setting harmonic mode')
            self.lockin.write_string('HARM %d\n' % self.settings.sr830_harmonic_mode, read=False)
            print('lockin settings set')
        elif self.settings.lockin_model_preference == 'SR844' and self.sr844_connected is True:
            print('SR844 is Selected')
            # Disable SR830 Stuff

            if self.settings.lockin_outputs == 0:
                print('attempting to set outputs to R and Theta')
                self.lockin.write_string('DDEF 1, 1\n', read=False)
                self.lockin.write_string('DDEF 2, 1\n', read=False)
            elif self.settings.lockin_outputs == 1:
                self.lockin.write_string('DDEF 1, 0\n', read=False)
                self.lockin.write_string('DDEF 2, 0\n', read=False)

            print('setting the sensitivity and filter slope')
            # Set the sensitivity and filter slope
            self.lockin.write_string('SENS %d; OFSL%d\n' % (self.settings.sr844_sensitivity,
                                                            self.settings.sr844_filter_slope), read=False)
            print('setting the time constant')
            # Set the time constant
            self.lockin.write_string('OFLT %d\n' % self.settings.sr844_time_constant, read=False)
            self.lockin.time_constant = self.lockin.tc_options[self.settings.sr844_time_constant]

            print('setting the reserves')
            self.lockin.write_string('WRSV %d; CRSV %d\n' % (self.settings.sr844_wide_reserve,
                                                             self.settings.sr844_close_reserve), read=False)
            print('setting the sampling rate')
            self.lockin.write_string('SRAT %d\n' % self.settings.sr844_sampling_rate, read=False)
            print('setting impedances')
            self.lockin.write_string('INPZ %d; REFZ %d\n' % (self.settings.sr844_input_impedance,
                                                             self.settings.sr844_ref_impedance), read=False)
            print('Setting 2F mode')
            if self.settings.sr844_harmonic is 1:
                self.lockin.write_string('HARM 1\n', read=False)
                print('2F detect mode turned on')
            elif self.settings.sr844_harmonic is 0:
                self.lockin.write_string('HARM 0\n', read=False)
                print('2F detect mode turned off')

            print('setting ref source')
            if self.settings.sr844_ref_source is 0:
                self.lockin.write_string('FMOD 0\n', read=False)
                print('External Reference Mode')
            elif self.settings.sr844_ref_source is 1:
                self.lockin.write_string('FMOD 1\n', read=False)
                print('Internal Reference Mode')

            print('setting Expand')
            self.lockin.write_string('DEXP %d\n' % self.settings.sr844_expand, read=False)
            print('lockin settings set')
        else:
            print('Invalid Lockin Preference')
            # error_message_window(text='Lock-in Could Not Be Updated',
            #                      inform_text='Check that selected lock-in is connected and powered on,'
            #                                  ' then reestablish communications')
            self.general_error_signal.emit({'Title': ' - Warning - ',
                                       'Text': 'Lock-in could not be updated',
                                       'Informative Text': 'Check that selected lock-in is connected and powered on,'
                                                           ' then reestablish communications',
                                       'Details': None})
        # Select the outputs displayed on the lock-in display
        self.lockin_delay = self.lockin.time_constant * self.settings.lockin_delay_scaling_factor


    # -------------------------------------------SLOT DEFINITIONS ------------------------------------------------------


    # @QtCore.pyqtSlot()
    # def lockin_model_changed(self):
    #     print('does nothing atm')

    @QtCore.pyqtSlot(bool)
    def update_all_slot(self):
        print('update all slot engaged')
        for ii in range(0, self.settings.ui.tab_widget.count()):
            self.update_tab_slot(which_tab=ii)

    @QtCore.pyqtSlot(float)
    def cg635_set_freq_slot(self, freq_to_set):
        print('Setting Frequency')
        self.cg635.set_freq(freq_to_set)

    @QtCore.pyqtSlot(int)
    def update_tab_slot(self, which_tab=None):
        print('Not set up. For now update all instead')
        print('which tab to update: ' + str(which_tab))
        if which_tab == 0:
            print('General tb not set up')
        elif which_tab == 1:
            print('updating lockin')
            if self.sr830_connected is False and self.sr844_connected is False:
                self.connect_lockin()
            self.set_lockin_settings()
        else:
            print('these tabs not set up yet')

    @QtCore.pyqtSlot()
    def connect_lockin(self):
        print(self.settings.lockin_model_preference)
        print(type(self.settings.lockin_model_preference))
        # Currently this creates a lock-in "Window" but doesn't show it:
        if self.settings.lockin_model_preference == 'SR844':
            print('setting up SR844')
            self.settings.ui.status_ind_sr830.setText(self.settings.off_led_str)
            self.sr830_connected = False

            self.lockin = PrologixAdaptedSRLockin(self.settings.prologix_com_port,
                                                  gpib_address=self.settings.sr844_gpib_address,
                                                  lockin_model='SR844')

            # Test comms and set instrument settings
            did_comms_fail, traceback = self.lockin.test_comms()
            print('Comms_failed? ' + str(did_comms_fail))
            if did_comms_fail is True:
                self.sr844_connected = False
                self.settings.ui.status_ind_sr844.setText(self.settings.red_led_str)
            else:
                self.sr844_connected = True
                self.settings.ui.sr844_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr844.setText(self.settings.grn_led_str)

        elif self.settings.lockin_model_preference == 'SR830':
            print('setting up SR830')
            self.settings.ui.status_ind_sr844.setText(self.settings.off_led_str)
            self.sr844_connected = False

            self.lockin = PrologixAdaptedSRLockin(self.settings.prologix_com_port,
                                                  gpib_address=self.settings.sr830_gpib_address,
                                                  lockin_model='SR830')
            # Test comms and set instrument settings
            did_comms_fail, traceback = self.lockin.test_comms()
            print('Comms_failed? ' + str(did_comms_fail))
            if did_comms_fail is True:
                self.sr830_connected = False
                self.settings.ui.status_ind_sr830.setText(self.settings.red_led_str)
            else:
                self.sr830_connected = True
                self.settings.ui.sr830_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr830.setText(self.settings.grn_led_str)
        else:
            did_comms_fail = True
            print('else case')

        if did_comms_fail is False:
            try:
                self.set_lockin_settings()
                print('Lockin Settings Set')
            except:
                # error_message_window(text='Lock-in Settings Could Not Be Set!',
                #                      inform_text='Unknown error',
                                     # details=str(sys.exc_info()[:]))
                # self.general_error_signal.emit([' - Warning - ', 'Lock-in Settings Could Not be Set!', 'Unknown Error',
                #                                 str(sys.exc_info)[:]])
                self.general_error_signal.emit({'Title': ' - Warning - ', 'Text': 'Lock-in Settings Could not be Set!',
                                                'Informative Text': 'Unknown Error', 'Details': str(sys.exc_info()[:])})
                print(sys.exc_info()[:])
        elif did_comms_fail is True:
            # error_message_window(text='Communication with Lock-in Failed!',
            #                      inform_text='Check that selected lock-in model is connected and powered on',
            #                      details=str(traceback[:]))
            self.general_error_signal.emit({'Title': ' - Warning - ', 'Text': 'Communication with Lock-in Failed!',
                                           'Informative Text': 'Check that selected lock-in model is connected and powered on',
                                           'Details': str(sys.exc_info()[:])})

    def connect_md2000(self):
        try:
            self.mono_controller = MonoControl()
            self.mono_controller.resource = self.settings.mono_resource_name
            self.mono_controller.gr_dens = self.settings.mono_groove_density
            # self.monochromator = MonoDriver(self.settings.mono_resource_name, self.settings.mono_groove_density)

            self.mono_controller.clicked_initialize_button()
            self.ui.statusbar.showMessage('Initializing Monochromator...')

            initialization_thread = Worker(self.mono_controller.initialization_tasks_thread())
            self.thread_pool.start(initialization_thread)
            self.settings.instrument_status_changed('md2000', 1)

        except pyvisa.VisaIOError:
            print(sys.exc_info()[:])
            self.settings.instrument_status_changed('md2000', 2)
            self.general_error_signal.emit({'Title': ' - Warning - ', 'Text': 'Communication with Mono Failed!',
                                            'Informative Text': 'Check that instrument is connected and powered on',
                                            'Details': str(sys.exc_info()[:])})

    def connect_toptica(self):
        print('---------------------------------- CONNECTING TOPTICA LASER -------------------------------------------')
        comms_error = self.toptica.start_comms(self.settings.toptica_com_port)
        print('Toptica Comm error: ' + str(comms_error))
        if comms_error is not None:
            self.toptica_connected = False
            self.settings.instrument_status_changed('toptica', 2)
            self.general_error_signal.emit({'Title': ' - Warning - ', 'Text': 'Communication with Laser Failed!',
                                            'Informative Text': 'Check that instrument is connected and powered on',
                                            'Details': str(sys.exc_info()[:])})
        else:
            self.toptica_connected = True
            self.settings.instrument_status_changed('toptica', 1)

    def connect_cg635(self):
        print('-------------------------------------- CONNECTING CG635 -----------------------------------------------')
        self.cg635 = CG635Instrument(com_format=self.settings.cg635_com_format,
                                     gpib_address=self.settings.cg635_gpib_address,
                                     com_port=self.settings.cg635_resource_name)
        # Connections seem like they should be in __init__, but to do so would require moving the instantiation of the
        # class there as well.
        # self.cg635.freq_changed_signal.connect(self.cg635_freq_changed_slot)
        did_comms_fail, traceback = self.cg635.test_comms()
        print('CG635 Comms_failed? ' + str(did_comms_fail))

        if did_comms_fail is True:
            self.cg635_connected = False
            self.settings.instrument_status_changed('cg635', 2)
            # error_message_window(text='Communication with CG635 Failed!',
            #                      inform_text='Check that instrument is connected and powered on.\n\n'
            #                                  'Check that GPIB/RS232 control is enabled on device.\n\n'
            #                                  'Check GPIB address and COM port are correct (settings)',
            #                      details=str(traceback[:]))
            self.general_error_signal.emit({'Title': ' - Warning - ', 'Text': 'Communication with CG635 Failed!',
                                            'Informative Text': 'Check that instrument is connected and powered on.\n\n'
                                             'Check that GPIB/RS232 control is enabled on device.\n\n'
                                             'Check GPIB address and COM port are correct (settings)',
                                            'Details': str(traceback[:])})
        else:
            self.cg635_connected = True
            self.settings.instrument_status_changed('cg635', 1)

    def connect_instruments_worker(self):
        print('------------------------------------- CONNECTING INSTRUMENTS --------------------------------------\n\n')
        if self.settings.ui.md2000_checkbox.isChecked():  # Initialize Monochromator
            self.connect_md2000()
        if self.settings.ui.sr830_checkbox.isChecked() or self.settings.ui.sr844_checkbox.isChecked():  # Initialize Lock-in
            self.connect_lockin()
        if self.settings.ui.cg635_checkbox.isChecked():
            self.connect_cg635()
        if self.settings.ui.toptica_checkbox.isChecked():
            self.connect_toptica()

    @QtCore.pyqtSlot()
    def connect_instruments(self):
        self.settings.ui.status_ind_smb100a.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_toptica.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_sr844.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_sr830.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_md2000.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_cg635.setText(self.settings.off_led_str)
        self.settings.ui.status_ind_cryostat.setText(self.settings.off_led_str)
        connect_worker = Worker(self.connect_instruments_worker)
        self.thread_pool.start(connect_worker)

    @QtCore.pyqtSlot(str)
    def cg635_freq_changed_slot(self, new_freq):
        self.settings.ui.cg635_set_freq_spinner.setValue(float(new_freq))
        self.ui.pump_mod_freq_spinner.setValue(float(new_freq))

    # ----------------------------------------- Other Window Slots ---------------------------------------------------
    @QtCore.pyqtSlot()
    def open_mono_window(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def open_RnS_window(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def open_cryostat_window(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def open_lockin_window(self):
        self.lockin_window = LockinWidget()
        self.lockin_window.show()

    @QtCore.pyqtSlot()
    def open_help_window(self):
        self.help_window = HelpWindowForm()
        self.help_window.show()

    @QtCore.pyqtSlot()
    def open_settings_window(self):
        # self.settings_window = SettingsWindowForm()
        self.settings.show()

    def data_collection_tasks(self, filename=None, filetype=None):
        #TODO: Incorporate 2D Data
        # 1. SAMPLING Rate for the SR844 is currently used no matter which lock-in you choose (bad)
        print('---------------------------------- BEGINNING EXPERIMENT THREAD ----------------------------------------')
        print('----------------------------------- Preparing Data Storage Arrays -------------------------------------')

        # -------------------------------------- PREPARE DATA STORAGE VARIABLES ----------------------------------------
        num_steps = self.ui.num_steps_spinner.value()
        duration = self.ui.averaging_time_spinner.value()

        num_scans = self.ui.num_scans_spinner.value()
        # To do 2D, I think we'll want to add another layer to the loop (one for each axis). This extra layer contains
        # all of the same stuff as the if/elif statement in the inner loop, except it is operating on abscissa 2
        # Changes will need to be made to the save data stuff of course as well.

        # To loop over scans, change 1 to num_scans, then ch_1_ave is an 2d array, each scan is along a column/row)
        # averaging will have to be done over the lock-in data but also over the scans dimension
        ch_1_ave = np.zeros((num_scans, num_steps))
        ch_2_ave = np.zeros((num_scans, num_steps))

        ch_1_array_average = np.zeros((num_steps, 1))
        ch_2_array_average = np.zeros((num_steps, 1))

        stored_ave_data_matrix = np.zeros((num_steps, 3))
        current_scan_data_matrix = np.zeros((num_steps, 3))
        current_scan_col_headers = [self.column_headers[0], 'Channel 1', 'Channel 2']

        stored_ch1_data_matrix = np.zeros((num_steps, num_scans + 1))  # I think I could rid myself of this..  but 4 now
        stored_ch2_data_matrix = np.zeros((num_steps, num_scans + 1))

        actual_x_values = np.zeros((num_steps, 1))
        ch_1_col_headers = [self.column_headers[0]] + (np.arange(1, num_scans + 1)).tolist()
        ch_2_col_headers = [self.column_headers[0]] + (np.arange(1, num_scans + 1)).tolist()

        steps_array = np.array(self.step_pts)

        self.axis_1.clear()
        self.axis_2.clear()
        self.set_plot_properties()

        print('---------------------------------- BEGINNING MAIN EXPERIMENT LOOP -------------------------------------')
        for jj in range(0, num_scans):
            print('---------------------------------------- SCAN %d ---------------------------------------------' % jj)
            if self.abort_scan is True:
                break
            else:
                for ii in range(0, num_steps):
                    t0_ii_loop = time.time()
                    if self.abort_scan is True:
                        break
                    else:
                        next_step = self.step_pts[ii]
                        print('Next Step is: ' + str(next_step) + '(Step ' + str(ii+1) + ' of ' + str(num_steps) + ')')

                        if self.abscissa_1 is 0:  # Empty Header line
                            pass
                        elif self.abscissa_1 is 1:  # Pump Modulation Frequency
                            print('------------------------ SETTING CG635 MODULATION FREQUENCY -----------------------')

                            if self.cg635_connected is False:
                                print('Cg635 was not connected')

                                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                                'Text': ' Experiment Aborted',
                                                                'Informative Text': 'CG635 Communication is not set up',
                                                                'Details': None})
                                return
                            else:
                                error = self.cg635.set_freq(freq_to_set=next_step)
                                if error is not None:
                                    # error_message_window('Scan Aborted, CG635 Error', inform_text=error)
                                    self.general_error_signal.emit({'Title': ' - Warning - ',
                                                                    'Text': 'Scan Aborted, CG635 Error',
                                                                    'Informative Text': error})
                                    return
                                print('Frequency is now at: ' + str(self.cg635.current_freq))
                                if jj == 0:
                                    actual_x_values[ii] = self.cg635.current_freq

                        elif self.abscissa_1 is 2:  # Probe Wavelength
                            print('Setting Probe Wavelength')
                            # --------------- SET THE PROBE WAVELENGTH ----------------------------

                        elif self.abscissa_1 is 3:  # Static Magnetic Field
                            print('This case has not been coded yet')
                        elif self.abscissa_1 is 4:  # RF Carrier Frequency
                            print('This case has not been coded yet')
                        elif self.abscissa_1 is 5:  # RF Modulation Frequency
                            print('This case has not been coded yet')
                        elif self.abscissa_1 is 6:  # TBD
                            print('This case has not been coded yet')
                        else:
                            print('there are this many possible abscissae?')

                        dt_set_freq = time.time() - t0_ii_loop
                        print('dt_set_freq: ' + str(dt_set_freq))

                        print('---------------------------- CHECKING FOR LOCKIN ISSUES -------------------------------')
                        # As in overloads, phase locking to reference.
                        self.lockin.open()      # Open also sets the correct GPIB address
                        self.lockin.lockin_instance.write('*CLS\n')
                        self.lockin.clear_buffers()
                        lia_error = self.lockin.check_status()
                        kk = 0
                        # It may take some time for the lockin internal oscillator  to lock to the reference freq
                        while lia_error is not None and kk < 200:
                            lia_error = self.lockin.check_status()
                            # print('lia error' + str(lia_error))
                            # print('loop iteration: ' + str(kk))
                            time.sleep(0.001)
                            kk = kk+1

                        if lia_error is not None:
                            self.lockin_error_signal.emit(str(lia_error))
                        dt_check_lia = (time.time() - t0_ii_loop) - dt_set_freq
                        print('dt_check_lia' + str(dt_check_lia))

                        t0_record_data = time.time()
                        # ---------------------- RECORD THE LOCKIN RESULTS ----------------------------
                        print('----------------------------- PAUSING FOR LOCK-IN SETTLING ----------------------------')
                        time.sleep(self.lockin_delay)   # Wait for the lock-in output to settle
                        print('------------------------------- COLLECTING DATA ---------------------------------------')
                        ch1_data, ch2_data = self.lockin.collect_data(duration, self.settings.sr844_sampling_rate,
                                                                      record_both_channels=True)
                        print('-------------------------- AVERAGING AND PLOTTING NEW DATA ----------------------------')

                        # Average all the data in each channel
                        try:
                            ch_1_current_result = np.average(ch1_data)
                            ch_2_current_result = np.average(ch2_data)

                            print('ch_1 result: ' + str(ch_1_current_result))
                            print('ch_2 result: ' + str(ch_2_current_result))

                            # Build the array of average values (I think replace vs append is better for many scan averaging?)
                            # Actually I guess if you run many scans you'll usually want to save each scan as well as the ave
                            ch_1_ave[jj, ii] = ch_1_current_result
                            ch_2_ave[jj, ii] = ch_2_current_result

                            # To incorporate many scans, we'll want to create a matrix

                        except:
                            print(sys.exc_info()[:])
                            break
                        dt_record_data = time.time() - t0_record_data
                        print('dt_record_data: ' + str(dt_record_data))

                        t0_plot_data = time.time()

                        # Plot the lock-in results
                        mod_freqs = steps_array[0:ii+1].flatten()
                        all_mod_freqs = steps_array.flatten()

                        actual_x_values_current = actual_x_values[0:ii+1].flatten()
                        actual_x_values_all = actual_x_values.flatten()

                        ch_1_array_current = ch_1_ave[jj, 0:ii+1].flatten()  # If multiple scans are along the 2nd dimension this won't work
                        ch_2_array_current = ch_2_ave[jj, 0:ii+1].flatten()  # But for now it seems like a viable option.

                        # print('ch_1_ave_flattened' + str(ch_1_array_current))
                        # print('ch_2_ave_flattened' + str(ch_2_array_current))
                        # print('mod_freqs_flattened' + str(mod_freqs))
                        print('actual x values: ' + str(actual_x_values))
                        # print('actual x values ALL: ' + str(actual_x_values_all))
                        # print('actual x values_SC!: ' + str(actual_x_values_current))

                        ch_1_array_average[ii] = np.average(ch_1_ave[0:jj+1, ii], 0).flatten()
                        ch_2_array_average[ii] = np.average(ch_2_ave[0:jj+1, ii], 0).flatten()

                        # print('shape of ch_1_Array_ave: ' + str(np.shape(ch_1_array_average)))
                        #
                        # print('')
                        # print('Array AVerages:')
                        # print(ch_1_array_average)
                        # print(ch_2_array_average)
                        #
                        # print('plot cleared')

                        color1 = '#0000FF'  # Blue
                        color2 = '#FF0000'  # Red
                        self.axis_1.set_xlabel(self.column_headers[0])
                        self.axis_1.set_ylabel(self.column_headers[1], c=color1)

                        self.axis_1.tick_params(axis='y', labelcolor=color1)

                        self.axis_2.set_ylabel(self.column_headers[2], c=color2)

                        self.axis_2.tick_params(axis='y', labelcolor=color2)

                        if jj == 0:
                            if ii > 0:
                                line1.remove()
                                line2.remove()

                            color_plot1 = '#0000FF'  # Blue
                            color_plot2 = '#FF0000'  # Red
                            line1, = self.axis_1.plot(actual_x_values_current, ch_1_array_current, ls='None', marker='o',
                                                      markersize=5, c=color_plot1, label='Current Scan')
                            line2, = self.axis_2.plot(actual_x_values_current, ch_2_array_current, ls='None', marker='o',
                                                      markersize=5, c=color_plot2, label='Current Scan')
                            self.axis_1.legend(loc=2)
                            self.axis_2.legend(loc=1)
                        elif jj > 0:
                            line1.remove()
                            line2.remove()

                            if ii > 0 or jj > 1:
                                line3.remove()
                                line4.remove()

                            color_plot1 = '#AFAFFF'
                            color_plot2 = '#FFAFAF'

                            line1, = self.axis_1.plot(actual_x_values_current, ch_1_array_current, ls='None', marker='o',
                                                      markersize=5, c=color_plot1, label='Current Scan')
                            line2, = self.axis_2.plot(actual_x_values_current, ch_2_array_current, ls='None', marker='o',
                                                      markersize=5, c=color_plot2, label='Current Scan')
                            # Averages
                            line3, = self.axis_1.plot(actual_x_values_all, ch_1_array_average, ls='None', marker='o',
                                                      markersize=5, c='#0000FF', label='Average')
                            line4, = self.axis_2.plot(actual_x_values_all, ch_2_array_average, ls='None', marker='o',
                                                      markersize=5, c='#FF0000', label='Average')

                            self.axis_1.legend(loc=2)
                            self.axis_2.legend(loc=1)

                        self.ui.PlotWidget.canvas.draw()
                        dt_plot_data = time.time() - t0_plot_data
                        print('dt_plot_data: ' + str(dt_plot_data))
                        dt_full_ii = time.time() - t0_ii_loop
                        print('dt_full_ii: ' + str(dt_full_ii))

                if filename is None:
                    pass
                else:
                    # current_scan_data_matrix[:, 0] = all_mod_freqs
                    current_scan_data_matrix[:, 0] = actual_x_values_all
                    current_scan_data_matrix[:, 1] = ch_1_array_current.flatten()
                    current_scan_data_matrix[:, 2] = ch_2_array_current.flatten()
                    current_scan_data_frame = pd.DataFrame(data=current_scan_data_matrix,
                                                           columns=current_scan_col_headers)
                    self.save_data(data_frame=current_scan_data_frame, filename=(filename + ', Scan ' + str(jj+1)),
                                   filetype=filetype)



        # Prepare/store the data in case of saving
        stored_ave_data_matrix[:, 0] = all_mod_freqs
        # stored_ch1_data_matrix[:, 0] = all_mod_freqs
        # stored_ch2_data_matrix[:, 0] = all_mod_freqs

        print('Stored average data: ')
        print('first column: ' + str(stored_ave_data_matrix[:, 0]))
        print('full stored_ave_data: ' + str(stored_ave_data_matrix))
        print(np.shape(ch_1_array_average))
        print(np.shape(stored_ave_data_matrix[:, 1]))
        stored_ave_data_matrix[:, 1] = ch_1_array_average.flatten()
        stored_ave_data_matrix[:, 2] = ch_2_array_average.flatten()
        print('stored arrays too')
        print(stored_ave_data_matrix[:, 0])
        print(stored_ave_data_matrix[:, 1])
        print(stored_ave_data_matrix[:, 2])

        print('preloop checks')
        print('shape ch_1_ave: ' + str(np.shape(ch_1_ave[0, :])))  # (3,)
        print(ch_1_ave[0, :])   # [0. 0. 0.]
        print('shape stored_ch1_data_matrix: ' + str(np.shape(stored_ch1_data_matrix[:, 1])))  # (3,)

        print('about to enter loop')
        # for jj in range(0, num_scans):
        #     print('jj: ' + str(jj))
        #     stored_ch1_data_matrix[:, jj+1] = ch_1_ave[jj, :]
        #     stored_ch2_data_matrix[:, jj+1] = ch_2_ave[jj, :]

        print('loop finished')
        print('stored ave data matrix:')
        print(stored_ave_data_matrix)
        # print('shape of SADM: ' + str(np.shape(stored_ave_data_matrix)))
        # print('column headers: ')
        # print(self.column_headers)
        # print(ch_1_col_headers)
        self.stored_ave_data_frame = pd.DataFrame(data=stored_ave_data_matrix, columns=self.column_headers)
        print('first frame done')
        # self.stored_ch1_data_frame = pd.DataFrame(data=stored_ch1_data_matrix, columns=ch_1_col_headers)
        # print('second frame done')
        # self.stored_ch2_data_frame = pd.DataFrame(data=stored_ch2_data_matrix, columns=ch_2_col_headers)

        print('created data frames')
        print(self.stored_ave_data_frame)
        # print(self.stored_ch1_data_frame)
        # print(self.stored_ch2_data_frame)
        print('ch1_data_matrix:')
        # print(stored_ch1_data_matrix)
        if filename is None:
            pass
        else:
            print('attempting to save data')
            # The dialog box MUST NOT OCCUR IN THE THREAD
            self.save_data(data_frame=self.stored_ave_data_frame, filename=(filename + ', Ave'), filetype=filetype)
        self.abort_scan = False

    @QtCore.pyqtSlot(dict)
    def general_error_window(self, window_details):
        """
        Expected details(/format) are(/is): {'Title': '<INSERT TITLE HERE>', 'Text': '<INSERT TEXT HERE>',
         'Informative Text': '<INSERT TEXT HERE>', 'Details': '<INSERT DETAILS HERE>'}
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(window_details['Title'])
        msg.setText(window_details['Text'])
        msg.setInformativeText(window_details['Informative Text'])
        msg.setDetailedText(window_details['Details'])
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        ret_val = msg.exec()

    @QtCore.pyqtSlot(str)
    def lockin_error_window(self, error_message):
        print('Trying to generate error_message_window')
        # error_message_window('WARNING - Lock-in Status Issues',
        #                      inform_text='Something is wrong with the lockin.\n LIAS? Response is: '
        #                                  + str(error_message) + '\nContinue Anyway?')

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText('Lock-in Status Issues')
        msg.setInformativeText('Something is wrong with the lockin.\n LIAS? Response is: ' +
                               str(error_message) + '\nContinue Anyway?')
        msg.setWindowTitle(' - Warning - ')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Abort)
        # msg.buttonClicked.connect(msgbtn)
        return_value = msg.exec()
        print('msg.clickedButton(): ' + str(msg.clickedButton()))
        print('msg box return value: ' + str(return_value))
        if return_value == QtWidgets.QMessageBox.Abort:
            self.abort_scan = True

    def save_file_dialog(self):
        #TODO: Check what happens when no file is selected
        print('inside save file dialog')
        tc = self.thread_pool.activeThreadCount()
        print('Active threads: ' + str(tc))
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, file_type = QFileDialog.getSaveFileName(self, "Save File As:", "",
                                                           "CSV Files (*.csv);;Text Files (*.txt);;All Files (*.*)",
                                                           options=options)
        file_name = file_name.split('.txt')[0].split('.csv')[0]  # In case the user included the extension
        return file_name, file_type

    @QtCore.pyqtSlot()
    def save_data(self, data_frame=None, filename=None, filetype=None):
        # TODO: Do the strings need to be raw? Test with spaces and wierd characters
        print('inside save data')
        if filename is None:
            filename, filetype = self.save_file_dialog()
        else:
            pass
        print('save_file_dialog happened')
        if filename is None:
            pass
        else:
            if filetype == 'CSV Files (*.csv)':
                print('generating csv files')
                ch1_filename = filename + '_ch1_scans.csv'
                ch2_filename = filename + '_ch2_scans.csv'
                filename = filename + '.csv'
                data_frame.to_csv(filename, index=None)
                # self.stored_ave_data_frame.to_csv(filename, index=None)
                # self.stored_ch1_data_frame.to_csv(ch1_filename, index=None)
                # self.stored_ch2_data_frame.to_csv(ch2_filename, index=None)
            elif filetype == 'Text Files (*.txt)':
                print('generating .txt files')
                ch1_filename = filename + '_ch1_scans.txt'
                ch2_filename = filename + '_ch2_scans.txt'
                filename = filename + '.txt'
                data_frame.to_csv(filename, sep='\t', index=None)
                # self.stored_ave_data_frame.to_csv(filename, sep='\t', index=None)
                # self.stored_ch1_data_frame.to_csv(ch1_filename, sep='\t', index=None)
                # self.stored_ch2_data_frame.to_csv(ch2_filename, sep='\t', index=None)

        # Prepare the data (make sure the data is still stored in case cancel is accidentally hit)
        # Open a save file/directory selection dialog box

    @QtCore.pyqtSlot()
    def start_btn_clicked(self):
        #TODO: Save notes and details to file before the worker
        print('------------------------------------ STARTING EXPERIMENT ----------------------------------------------')
        self.abscissa_1 = self.ui.variable_1_combobox.currentIndex()
        print('x axis is index: ' + str(self.abscissa_1))

        # This MUST OCCUR BEFORE THE THREAD
        if self.ui.autosave_checkbox.isChecked():
            filename, filetype = self.save_file_dialog()
        else:
            filename=None
            filetype=None

        self.abort_scan = False     # This should probably go before the if/elif statement

        # Add here a save Experiment Notes and details to file
        if self.settings.lockin_outputs == 0:       # 0 is R/Theta
            self.column_headers[1] = 'R (V)'
            self.column_headers[2] = 'Theta (Degrees)'
        elif self.settings.lockin_outputs == 1:
            self.column_headers[1] = 'X (V)'
            self.column_headers[2] = 'Y (V)'
        else:
            self.column_headers[1] = 'Channel 1 Display'
            self.column_headers[2] = 'Channel 2 Display'
        print('Lockin time Constant: ' + str(self.lockin.time_constant))
        self.lockin_delay = self.settings.lockin_delay_scaling_factor * self.lockin.time_constant
        print('lockin_delay: ' + str(self.lockin_delay))
        data_collection_worker = Worker(self.data_collection_tasks, filename, filetype)
        self.thread_pool.start(data_collection_worker)


    def enable_all_ui_objects(self):
        self.ui.variable_2_combobox.setEnabled(True)
        self.ui.sweep_end_spinner_var_2.setEnabled(True)
        self.ui.num_steps_spinner_var_2.setEnabled(True)
        self.ui.sweep_start_spinner_var_2.setEnabled(True)

        self.ui.temp_spinner.setEnabled(True)
        self.ui.probe_wl_spinner.setEnabled(True)
        self.ui.rf_freq_spinner.setEnabled(True)
        self.ui.static_field_spinner.setEnabled(True)
        self.ui.pump_mod_freq_spinner.setEnabled(True)
        self.ui.rf_mod_freq_spinner.setEnabled(True)

    def set_plot_properties(self):
        print('inside set_plot_properties')
        print('self.scaling_pref = ' + str(self.scaling_pref))
        self.axis_1.set_xscale(self.scaling_pref)
        print('set xscale')
        if self.step_count is not 1:
            print('self.step_count was not 1')
            if self.start < self.end:
                print('start < end')
                if self.scaling_pref == 'linear':
                    print('linear case')
                    self.axis_1.set_xlim(left=(self.start - 0.05 * self.scan_range),
                                         right=(self.end + 0.05 * self.scan_range))
                elif self.scaling_pref == 'log':
                    print('log case')
                    self.axis_1.set_xlim(left=(self.start - 0.1 * self.start),
                                         right=(self.end + 0.1 * self.end))
            elif self.start > self.end:
                print('start > end')
                if self.scaling_pref == 'linear':
                    print('linear case')
                    self.axis_1.set_xlim(left=(self.end - 0.05 * self.scan_range),
                                         right=(self.start + 0.05 * self.scan_range))
                elif self.scaling_pref == 'log':
                    print('log case')
                    self.axis_1.set_xlim(left=(self.end - 0.1 * self.end),
                                         right=(self.start + 0.1 * self.start))
        print('limits set')
        self.axis_1.set_xlabel(self.x_axis_label)
        print('label set')
        if self.output_variables == 'R/Theta':
            self.axis_2.set_ylim(bottom=-180, top=180)

        # self.axis_1.set_ylabel(self.y_axis_1_label)
        # self.axis_2.set_ylabel(self.y_axis_2_label)

        self.ui.PlotWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def calc_steps_from_num(self):
        print('inside calc_from_num')
        self.scale = 10**(3*self.ui.sweep_units_combobox.currentIndex())
        self.end = (self.ui.sweep_end_spinner.value()) * self.scale
        self.start = (self.ui.sweep_start_spinner.value()) * self.scale
        self.step_count = self.ui.num_steps_spinner.value()
        self.scan_range = self.end - self.start

        if self.log_spacing:
            print('inside log case')
            self.scaling_pref = 'log'
            self.ui.step_size_display.setText('N/A')
            log_start = np.log10(self.start)
            log_end = np.log10(self.end)
            try:
                if self.step_count is not 1:
                    log_step_size = np.abs(log_end - log_start) / (self.step_count - 1)
                    step_pts = []

                    if self.start < self.end:
                        for ii in range(0, self.step_count):
                            log_next_step = log_start + (ii * log_step_size)
                            step_pts.append(10 ** log_next_step)

                    else:
                        print('attempting inverted scan direction (log scaling')
                        for ii in range(0, self.step_count):
                            log_next_step = log_start - (ii * log_step_size)
                            step_pts.append(10 ** log_next_step)

                    self.step_pts = step_pts

                else:
                    self.step_pts = [self.start]

                steps_to_display = str(np.round(np.array(self.step_pts), 3).tolist()).replace(',', '\r')
                self.ui.steps_display.setText(steps_to_display)

            except:
                print(sys.exc_info()[:])

        else:
            print('inside linear case')
            self.scaling_pref = 'linear'

            try:
                if self.step_count is not 1:
                    step_size = np.abs(self.end - self.start) / (self.step_count - 1)
                    self.step_size = step_size
                    self.ui.step_size_display.setText(str(round(step_size / self.scale, 4)))
                    step_pts = []
                    if self.start < self.end:
                        for ii in range(0, self.step_count):
                            step_pts.append(self.start + ii * step_size)

                    else:
                        for ii in range(0, self.step_count):
                            step_pts.append(self.start - ii * step_size)

                    self.step_pts = step_pts
                    # Update plot
                else:
                    self.step_pts = [self.start]

                steps_to_display = str(np.round(np.array(self.step_pts), 3).tolist()).replace(',', '\r')
                self.ui.steps_display.setText(steps_to_display)

            except:
                print(sys.exc_info()[:])

            print('about to rescale plot')
        # self.axis_1.set_xscale(self.scaling_pref)
        # self.ui.PlotWidget.canvas.draw()
        # Estimate Experiment duration
        averaging_time = self.ui.averaging_time_spinner.value()
        data_transfer_time = self.settings.sr844_sampling_rate*averaging_time*0.00132   #This estimate is good
        # 0.00132 is for transferring both channels using TRCL (1.32 ms per sample)
        freq_set_delay = 0.44           # Estimated using the CG635
        check_lia_delay = 0.44          # Very rough estimate. This one depends a lot on situation
        plot_data_delay = 0.16
        record_data_delay = self.lockin_delay + averaging_time + data_transfer_time + 0.139
        num_scans = self.ui.num_scans_spinner.value()
        print('--------------------- Expt Duration Estimate-----------------')
        print('lockin_delay: ' + str(self.lockin_delay))
        print('ave_time: ' + str(averaging_time))
        print('Sampling rate: ' + str(self.settings.sr844_sampling_rate))
        print("num_scans: " + str(num_scans))
        print('self.step_count: ' + str(self.step_count))
        expt_duration_estimate = self.step_count*num_scans*(freq_set_delay + check_lia_delay +
                                                            record_data_delay + plot_data_delay)

        self.ui.experiment_duration_lineedit.setText(str(expt_duration_estimate) + 'Sec')
        self.set_plot_properties()

    @QtCore.pyqtSlot(bool)
    def autosave_checkbox_toggled(self, autosave_on):
        print('autosave on: ' + str(autosave_on))

    @QtCore.pyqtSlot(bool)
    def log_spacing_checkbox_toggled(self, log_spacing_on):
        self.log_spacing = log_spacing_on
        print('log_spacing on: ' + str(log_spacing_on))
        self.calc_steps_from_num()

    @QtCore.pyqtSlot(str)
    def primary_indep_var_combobox_activated(self, indep_variable_str):
        print('abscissa 1 activated')
        print(indep_variable_str)

        if indep_variable_str == 'Pump Modulation Frequency':
            print('Pump Mod Selected')
            self.x_axis_label = 'Pump Modulation Frequency (Hz)'
            self.column_headers[0] = self.x_axis_label

            try:
                self.ui.sweep_start_spinner.setValue(self.presets.pump_mod_freq_start)
                self.ui.sweep_end_spinner.setValue(self.presets.pump_mod_freq_end)
                self.ui.num_steps_spinner.setValue(self.presets.pump_mod_freq_steps)

                self.ui.sweep_units_combobox.clear()
                self.ui.sweep_units_combobox.addItems(['Hz', 'kHz', 'MHz', 'GHz'])
                self.ui.sweep_units_combobox.setCurrentIndex(1)

                self.ui.log_spacing_checkbox.setChecked(True)
                self.log_spacing = True

                self.calc_steps_from_num()
            except:
                print(sys.exc_info()[:])
            # self.set_plot_properties()
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Pump Modulation Frequency (kHz)')
            # self.ui.PlotWidget.canvas.draw()        # Will the axis label disappear when cleared again? Yes

        if indep_variable_str == 'Probe Wavelength':
            print('Probe wl selected')
            self.x_axis_label = 'Probe Wavelength (nm)'
            self.column_headers[0] = self.x_axis_label

            try:
                print('disabled second set')
                self.ui.sweep_start_spinner.setValue(self.presets.probe_wl_start)
                print('first value worked')
                self.ui.sweep_end_spinner.setValue(self.presets.probe_wl_end)
                print('second value worked')
                self.ui.num_steps_spinner.setValue(self.presets.probe_wl_num_steps)
                # self.ui.step_size_display.setText(str(self.presets.probe_wl_step_size))
                print('set presets')
                self.ui.log_spacing_checkbox.setChecked(False)

                self.calc_steps_from_num()
            except:
                print(sys.exc_info()[:])
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Probe Wavelength (nm)')

        if indep_variable_str == 'Static Magnetic Field':
            print('Static Field Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Static Magnetic Field (Gauss)')

        if indep_variable_str == 'RF Carrier Frequency':
            print('RF Carrier Freq Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Carrier Frequency (GHz)')

        if indep_variable_str == 'RF Modulation Frequency':
            print('RF Mod Freq Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Modulation Frequency (Hz)')

    @QtCore.pyqtSlot(str)
    def secondary_indep_var_combobox_activated(self, indep_variable_str):
        print(indep_variable_str)

        if indep_variable_str == 'Pump Modulation Frequency':
            print('Pump Mod Selected')

        if indep_variable_str == 'Probe Wavelength':
            print('Probe wl selected')

        if indep_variable_str == 'Static Magnetic Field':
            print('Static Field Selected')

        if indep_variable_str == 'RF Carrier Frequency':
            print('RF Carrier Freq Selected')

        if indep_variable_str == 'RF Modulation Frequency':
            print('RF Mod Freq Selected')

    @QtCore.pyqtSlot(str)
    def experiment_preset_combobox_activated(self, experiment_str):
        print(experiment_str)
        if experiment_str == '-Manual Setup-':
            self.enable_all_ui_objects()
        elif experiment_str == 'Optical Absorption Spectrum':
            self.enable_all_ui_objects()
            self.ui.variable_1_combobox.setCurrentIndex(2)
            self.ui.variable_2_combobox.setEnabled(False)
            self.ui.rf_freq_spinner.setEnabled(False)
            self.ui.rf_mod_freq_spinner.setEnabled(False)

            self.ui.sweep_start_spinner_var_2.setEnabled(False)
            self.ui.sweep_end_spinner_var_2.setEnabled(False)
            self.ui.num_steps_spinner_var_2.setEnabled(False)
            print('Completed Experiment Preset Setup')

        elif experiment_str == 'PL Lifetime':
            self.enable_all_ui_objects()
            self.ui.variable_1_combobox.setCurrentIndex(1)                               # Pump Modulation Frequency = 1
            self.ui.variable_2_combobox.setEnabled(False)
            self.ui.rf_freq_spinner.setEnabled(False)
            self.ui.rf_mod_freq_spinner.setEnabled(False)
            print('Disabled First Set')

            self.ui.sweep_start_spinner_var_2.setEnabled(False)
            self.ui.sweep_end_spinner_var_2.setEnabled(False)
            self.ui.num_steps_spinner_var_2.setEnabled(False)

            print('Completed PL Lifetime Preset Setup')

        elif experiment_str == 'PA Lifetime':
            print('experiment not set up yet')
        elif experiment_str == 'PA Lifetime (Single WL)':
            print('experiment not set up yet')
        else:
            print('experiment/case not set up yet')

    @QtCore.pyqtSlot()
    def pause_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def stop_btn_clicked(self):
        self.abort_scan = True
        print('Aborting Scan')

    @QtCore.pyqtSlot()
    def go_to_temp_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_probe_wl_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_rf_freq_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_static_field_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_pump_mod_freq_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_rf_mod_freq_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def set_all_constants_btn_clicked(self):
        print('Button Does nothing yet')

    @QtCore.pyqtSlot()
    def go_to_temp_btn_clicked(self):
        print('Button Does nothing yet')


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)            # Defines the instance of the whole application
    app.setStyle('Fusion')                  # I like the way fusion looks
    expt_control_window = MainWindow()      # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    expt_control_window.show()
    sys.exit(app.exec_())
