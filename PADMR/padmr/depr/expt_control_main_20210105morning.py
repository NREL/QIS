#TODO:
# Priorities:
# 2. Toptica signals/slots/error handling
# 2b. Get laser to turn on and off with experiment (And also add a "modulation enabled" indicator)
# 3. Test fluorescence lifetime experiment
# 4. Get probe wavelength scanning working
# 5. Finish setting up 2D experiments
# Various:
# -76. Attempting to restart experiment after aborting due to lock-in not locking, caused crash
# -75. Reset Scan Entries when Abscissa is set to 0 (also rename this to ' - None - ' ?)
# -74. Move number of scans to the respective abscissa block (ui objects)
# -73. Change saving so that if only 1 scan, Ave Data is saved (rather than scans)
# -72. Retest saving data (including 2D with > 1 scan)
# -71. The laser power buttons lost their arrows. Also, the uW/mW thing is confused.
# -70. Figure out the settings window laser buttons (they seem to be redundant)
# -69. Find a good way to average multiple 2d scans together (perhaps create the "Scans" file, and treat both
# scan dimensions the same as is currently done for 1d scans)
# -67. Measure the ACTUAL time waited before the lock-in measures the results
# -65. Consolidate error signals (don't need to rewrite title every time)
# -61. Does the "clear errors" need to be matched in self.settings.instr ?
# -60. Get all instruments to use statusbar
# -59. Forbid changing experiment parameters during experiment
# -58. Improve the start experiment conditionality statement to include all instruments that will be used.
# -57. 2D data is getting plotted wierdly after the second dimension moves for the first time
# (because chX_scan is removing the x axis values)
# -53. Getting a "PLL never locked" error
# -52. Incorporate a "busy" functionality to prevent fast clickers from crashing the program
# -51. Change y scales to keep legends out of the way (or place legends outside plot area)
# -50. Gray out text associated with secondary variable as well so it's not confusing
# -49. Incorporate a check: check lock-in frequency matches expected frequency (not just that it is locked)
# -47. Measure function durations as a wrapper around most functions?
# -46. Why does the lock-in light come on before all the properties are done setting?
# -44. Figure out this stupid led_icons_rc file issue
# -43. Make error handling in Mono_control_module consistent.
# -42. Put the mono __init__ attributes into the .ini file
# -41. Consolidate redundant tasks in all scripts (e.g. wrappers)
# -40. Provide some notification that the experiment is over.
# -39. Don't save "scan 1" separately from ave if only one scan
# -38. Update Current frequency in the settings tab to always be the current frequency
# -37. Make self.....connected consistent between instruments after determining if it is at all useful.
# -36. Make "instrument_status_changed" consistent between instruments
# - 35. Move shared classes into a folder and import.
# -34. Get the current frequency/wl/whatever property displayed above the plot
# -33. When experiment preset selected, automatically check relevant instrument boxes
# -32. Get the legends to be less stupid (overlap)
# -31. Find a way to get the corresponding settings objects to update whenever "property_updated_signal" emitted.
#   E.g. current freq
# -30. Break up collect_data into 2 or three sub-functions
# -29. Figure out a good way to save data when doing 2D experiments
# -27. Make a "fast" and "slow" mode for lock-in functions (in fast mode, open must be done BEFOREHAND)?
# -26. Add signals to the relevant com port settings (and others) in settings_window_main
# -25. Merge all the update...property functions into one
# -23. Set up signals/slots and error handling for toptica
# -22. Consolidate connect_lockin (I don't think there needs to be a large if/else statement)
# -21. Replace signal/slots telephone game with the connect function (improve using lambda. Including CG635 "send" btns)
# -18. Should the error cluster also contain a type (warning vs error) that determines level of reaction?
# -16. If error handling works nicely with lockin and cg635, apply also to other modules (including the QObject thing)
# -15. Does self.connected need to be set to False whenever a communication error occurs?
# -14. Add a "collect_data_array" function to the lockin control module (so you can look for oscillations)
# -12. Add docstrings to every function
# -11. Do I really need the \n in the write commands? It would be nice to be consistent
# -4. Incorporate the frequency mismatch warning into a window (At the end of the experiment?)
# -2. Aggressive precision on floats will be a problem since the last digits may be random values(eg.25.000000000000007)
# -1. Laser initialization tests should be updated at the settings window.
# 0. Add laser on indicator light to the MAIN Window as well.
# 0. Add a "check for connectivity" error handler for functions which require it. (e.g. using self.cg635_connected)
# 0a. self.cg635_connected may be better as self.cg635.connected (attribute of the instrument)
# 4. Incorporate a scan probe wavelength (at set pump mod frequency) option (TA Spectrum)
# 9. Incorporate an "if ...connected" before "set params"
# -1. Rename variables to decrease length and increase self-consistency
# 0. Restore to defaults btn
# 1. Add live error bars could be put on each point based on standard deviation or something.
# This would be awesome for knowing when to stop an experiment (alternatively, plot all previous scans in pale color?)
# 2. Live fitting with uncertainties would be a nice feature
# 3. Add a "hide current scan" and/or "hide average scan" to clean up the plot
# 3. Add icons to "constants" to simplify experiment setup (like a thermometer for temp, rainbow for wl, etc)
# 4. Incorporate indicators to show which devices are outputting e.g. laser, u-waves
# 5. Get displayed steps to print with fewer sig figs
# 6. Find rounding parameters that work for all experiment configurations
# 7. Consider reworking the monocontrol scripts so that everything needed here is in the control module (so importing
# the mono_control_main is only used for single instrument control) (at the least rename the slots so they make more
# sense in the context of this program)
# 8. Get "set_plot_params" fn to do all of the plotting label stuff.
# 10. Make it so the plot doesn't have insane axis limits when 0s are in start and end
# 2. Reorganize MainWindow to something logical
# 3. Rename com_port and resource_name variables for consistency
# 5. Format all the control modules in the same way (to the extent that it's possible to do so)

import os
import sys
import time
import csv
from typing import Union

import numpy as np
import pyvisa
import pandas as pd
import matplotlib.pyplot as plt
from pyvisa.constants import VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD, StopBits
from decorator import decorator
import PyQt5

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QThreadPool, QRunnable  # For multithreading (parallel tasks)
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

import padmr.instr.mono.main
from padmr.instr.mono.controls import MonoDriver
from padmr.instr.mono.main import MainWindow as MonoControl
from padmr.instr.laser.controls import TopticaInstr

from padmr.instr.lia.main import LockinWidget
from padmr.instr.lia.controls import PrologixAdaptedSRLockin, ErrorCluster
from padmr.instr.zurich_lia.controls import ZiLIA, ErrorCluster
from padmr.gui import Ui_MainWindow as ExptControlMainWindow

from padmr.supp.help_window.main import HelpWindowForm
from padmr.supp.settings.main import SettingsWindowForm
from padmr.instr.cg635.controls import CG635Instrument
from padmr.supp.label_strings import LabelStrings
from padmr.supp import helpers

pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))

class PlottedData:
    def __init__(self, dims=1, output_names=['R(Volts)', 'Theta(Degrees)'], num_scans=[1, 1], notes='',
                 instr_settings=None):
        self.num_dims = dims
        self.output_names = output_names
        self.num_scans = num_scans
        self.details = notes
        self.instr_settings = instr_settings

class MainWindow(QMainWindow):
    lockin_status_warning_signal = QtCore.pyqtSignal(str)
    general_error_signal = QtCore.pyqtSignal(dict)
    status_message_signal = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the ui.py file and prepare the UI
        self.ui = ExptControlMainWindow()
        self.ui.setupUi(self)


        # ------------------------------- initialize attribute values - ------------------------------------------------
        # These are attributes of the MainWindow class, not of the ui instance
        # They are used as attributes of the program.
        # Many of these should be settings or presets instead of here
        # self.step_pts = None

        # self.sr830_connected = False
        # self.sr844_connected = False
        self.cg635_connected = False
        self.md2000_connected = False
        self.smb100a_connected = False
        self.montana_instr_connected = False
        # self.toptica_connected = False

        self.offset_each = False
        self.label_strings = LabelStrings()

        self.abort_scan = False
        self.pause_scan = False

        self.lockin_delay = 0

        self.x_axis_label = None
        self.abscissa_name = ['Indep Var 1', 'Indep Var 2']
        self.output_name = ['Channel 1', 'Channel 2']
        self.axis_1 = self.ui.PlotWidget.canvas.axes_main
        self.axis_2 = self.ui.PlotWidget.canvas.axes_main.twinx()
        # self.scan_range = None
        self.output_variables = 'R/Theta'
        self.column_headers = ['Independent Variable', 'Channel 1', 'Channel 2']
        self.data_details = None

        self.abscissae = [None, None]
        self.units = [None, None]
        abs_set_delay = [0, 0]

        self.num_dims = 1
        self.num_scans = [1, 1]
        self.averaging_time = 0

        self.scale_factor = [1, 1]
        self.end = [0, 0]
        self.start = [0, 0]
        self.step_count = [1, 1]
        self.scan_range = [0, 0]
        self.current_position = [None, None]
        self.log_spacing = [False, False]
        self.step_pts = [None, None]
        self.scaling_pref = ['linear', 'linear']
        self.step_range = [0, 0]
        self.step_size = [0, 0]

        self.ch1_scans_df = None
        self.ch2_scans_df = None
        self.ave_data_df = None
        self.ave_data_ch1_df = None
        self.ave_data_ch2_df = None

        self.log_spacing_checkboxes = [self.ui.log_spacing_checkbox, self.ui.log_spacing_checkbox_dim2]
        self.units_cbxes = [self.ui.sweep_units_cbx, self.ui.sweep_units_cbx_dim2]
        self.steps_displays = [self.ui.steps_display, self.ui.steps_display_dim2]
        self.sweep_end_spbxs = [self.ui.sweep_end_spbx, self.ui.sweep_end_spbx_dim2]
        self.sweep_start_spbxs = [self.ui.sweep_start_spbx, self.ui.sweep_start_spbx_dim2]
        self.num_steps_spbxs = [self.ui.num_steps_spbx, self.ui.num_steps_spbx_dim2]
        self.step_size_displays = [self.ui.step_size_display, self.ui.step_size_display_dim2]

        # ----------------------------- INSTANTIATE LARGE SCALE OBJECTS (CLASSES/WINDOWS) ------------------------------
        # Create the settings window (but don't show it)
        self.settings = SettingsWindowForm()
        self.toptica = TopticaInstr()
        # self.settings.toptica_instr = self.toptica
        #TODO: Can I delete the next two lines? They are misleading if the UHFLI is used.
        self.lockin = PrologixAdaptedSRLockin()
        self.lockin.settings = self.settings.lia
        self.cg635 = CG635Instrument()
        self.md2000 = MonoDriver()
        self.md2000.settings = self.settings.md2000
        print(str(self.settings.md2000.com_port))

        # ------------------------------- Initialize GUI Object States -------------------------------------------------

        self.addToolBar(NavigationToolbar2QT(self.ui.PlotWidget.canvas, self), )
        self.ui.log_spacing_checkbox.setChecked(False)
        self.ui.log_spacing_checkbox_dim2.setChecked(False)
        self.ui.num_scans_dim2_spbx.setValue(1)
        self.ui.num_steps_spbx_dim2.setValue(1)

        # ------------------------------------ Run any initialization Functions ----------------------------------------
        self.set_icons()
        self.connect_signals_and_slots()
        # ------------------------ MULTI-THREADING STUFF ---------------------------------------------------------------
        self.thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.thread_pool.maxThreadCount())

    @QtCore.pyqtSlot()
    def connect_instruments(self):
        self.settings.ui.status_ind_smb100a.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_toptica.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_sr844.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_sr830.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_md2000.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_cg635.setText(self.label_strings.off_led_str)
        self.settings.ui.status_ind_cryostat.setText(self.label_strings.off_led_str)

        connect_worker = helpers.Worker(self.connect_instruments_worker)
        self.thread_pool.start(connect_worker)

    def connect_instruments_worker(self):
        print('------------------------------------- CONNECTING INSTRUMENTS --------------------------------------\n\n')
        if self.settings.ui.md2000_checkbox.isChecked():
            self.connect_md2000()
        if self.settings.ui.sr830_checkbox.isChecked() or self.settings.ui.sr844_checkbox.isChecked()\
                or self.settings.ui.uhfli_checkbox.isChecked():
            self.connect_lockin()
        if self.settings.ui.cg635_checkbox.isChecked():
            self.connect_cg635()
        if self.settings.ui.toptica_checkbox.isChecked():
            self.connect_toptica()

    def connect_lockin(self):
        print('Setting up Lock-in...')
        if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
            did_comms_fail = self.lockin.start_comms(self.settings.prologix_com_port,
                                                     gpib_address=self.settings.lia.gpib_address,
                                                     model=self.settings.lockin_model)
            print('Comms_failed? ' + str(did_comms_fail))
        elif self.settings.lockin_model == 'UHFLI':
            print('UHFLI chosen')
            self.lockin = ZiLIA()
            print('instantiated')
            did_comms_fail = self.lockin.start_comms(device_id='dev2025')
        else:
            raise ValueError('Invalid Lock-in Model Selected')

        if self.settings.lockin_model == 'SR844':
            if did_comms_fail is True:
                self.settings.ui.status_ind_sr844.setText(self.label_strings.red_led_str)
            else:
                self.settings.ui.sr844_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr844.setText(self.label_strings.grn_led_str)
        elif self.settings.lockin_model == 'SR830':
            if did_comms_fail is True:
                self.settings.ui.status_ind_sr830.setText(self.label_strings.red_led_str)
            else:
                self.settings.ui.sr830_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr830.setText(self.label_strings.grn_led_str)
        elif self.settings.lockin_model == 'UHFLI':
            if did_comms_fail is True:
                self.settings.ui.status_ind_uhfli.setText(self.label_strings.red_led_str)
            else:
                self.settings.ui.uhfli_checkbox.setChecked(True)
                self.settings.ui.status_ind_uhfli.setText(self.label_strings.grn_led_str)
        else:
            raise ValueError('Invalid Lock-in Model Selected')

        if did_comms_fail is False:
            self.lockin.settings = self.settings.uhfli # This needs to be changed so that settings.uhfli contains t
            self.lockin.update_all()
            if self.settings.lockin_model == 'UHFLI':
                self.lockin_delay = self.settings.lockin_settling_factor * self.settings.uhfli.time_constant_value
            else:
                self.lockin_delay = self.settings.lockin_settling_factor * self.settings.lia.time_constant_value
            print('Lockin Settings Set')

    def connect_md2000(self):
        # self.md2000.establish_comms(self.settings.md2000.com_port)
        self.md2000.initialize_mono(self.settings.md2000.com_port)
        if self.md2000.error.status:
            self.md2000.settings.connected = False
            self.settings.instrument_status_changed('md2000', 2)
        else:
            self.md2000.settings.connected = True
            self.md2000.set_home_position(self.settings.md2000.cal_wl)
            self.settings.instrument_status_changed('md2000', 1)

        # self.settings.update_md2000_tab()

    def connect_toptica(self):
        print('---------------------------------- CONNECTING TOPTICA LASER -------------------------------------------')
        self.toptica.start_comms(self.settings.toptica.com_port)
        if self.toptica.error.status:
            print('error status was True (error exists)')
            self.toptica.settings.connected = False
            self.settings.instrument_status_changed('toptica', 2)
        else:
            self.toptica.settings.connected = True
            self.settings.instrument_status_changed('toptica', 1)

        self.settings.update_topt_tab()

    def connect_cg635(self):
        print('-------------------------------------- CONNECTING CG635 -----------------------------------------------')
        # self.cg635.freq_changed_signal.connect(self.cg635_freq_changed_slot)
        did_comms_fail = self.cg635.start_comms(gpib_address=self.settings.cg635_gpib_address,
                                                com_port=self.settings.prologix_com_port)
        print('CG635 Comms_failed? ' + str(did_comms_fail))

        if did_comms_fail is True:
            self.cg635_connected = False
            self.settings.instrument_status_changed('cg635', 2)

        else:
            self.cg635_connected = True
            self.settings.instrument_status_changed('cg635', 1)

    # -------------------------------------- MAIN EXPERIMENT FUNCTIONS -------------------------------------------------

    @helpers.measure_time
    @QtCore.pyqtSlot()
    def start_experiment(self):
        # TODO: Save notes and details to file before the worker
        if self.lockin.connected:
            self.status_message_signal.emit('Getting Ready to Start Experiment...........')

            notes = self.ui.notes_plain_text_edit.toPlainText()

            if self.ui.autosave_checkbox.isChecked():
                # This MUST OCCUR BEFORE THE THREAD
                filename, filetype = self.save_file_dialog()
            else:
                filename = None
                filetype = None
            if filename == '':
                filename = None
                filetype = None
            if filename is not None:
                os.mkdir(filename)
                filename = filename + '\\'
                with open(filename + 'Notes', 'w') as notes_file:
                    notes_file.write(notes)

            self.abort_scan = False  # This should probably go before the if/elif statement
            self.pause_scan = False
            # Add here a save Experiment Notes and details to file
            if self.settings.lockin_outputs == 0:  # 0 is R/Theta
                self.output_name[0] = 'R (V)'
                self.output_name[1] = 'Theta (Degrees)'
            elif self.settings.lockin_outputs == 1:
                self.output_name[0] = 'X (V)'
                self.output_name[1] = 'Y (V)'
            else:
                self.output_name[0] = 'Channel 1 Display'
                self.output_name[1] = 'Channel 2 Display'
            print('Lockin time Constant: ' + str(self.settings.lia.time_constant_value))
            self.lockin_delay = self.settings.lockin_settling_factor * self.settings.lia.time_constant_value
            print('lockin_delay: ' + str(self.lockin_delay))

            # self.prepare_for_collection()

            if self.abscissae[1] is None or self.abscissae[1] == 0:
                self.num_dims = 1
                self.data_type = '1D'
            elif 0 < self.abscissae[1] < 6:
                self.num_dims = 2
                self.data_type = '2D'

                self.ave_data_ch1_df = []
                self.ave_data_ch2_df = []
            else:
                raise ValueError('Invalid Value for abscissa[1] (second independent variable)')

            self.num_scans[0] = self.ui.num_scans_spbx.value()
            self.num_scans[1] = self.ui.num_scans_dim2_spbx.value()

            self.averaging_time = self.ui.averaging_time_spbx.value()

            self.column_headers = [self.abscissa_name[0], self.output_name[0], self.output_name[1]]
            # self.ave_data_df = pd.DataFrame(columns=self.column_headers)

            self.actual_x_values = np.empty((self.step_count[0], 1))
            self.actual_x_values[:] = np.nan
            self.actual_x_values = self.actual_x_values.flatten()

            self.data_details = PlottedData(dims=self.num_dims, output_names=self.output_name, num_scans=self.num_scans,
                                            notes=notes, instr_settings=None)

            data_collection_worker = helpers.Worker(self.collect_data, filename, filetype)
            self.thread_pool.start(data_collection_worker)
        else:
            self.general_error_window(details={'Title': 'Experiment Aborted',
                                               'Text': 'One or more instruments not set up', 'Informative Text': '',
                                               'Details': ''})

    # @helpers.measure_time
    # def prepare_for_collection(self):
    #     print('----------------------------------- Preparing Data Storage Arrays -------------------------------------')
    #
    #     if self.abscissae[1] is None or self.abscissae[1] == 0:
    #         self.num_dims = 1
    #         self.data_type = '1D'
    #     elif 0 < self.abscissae[1] < 6:
    #         self.num_dims = 2
    #         self.data_type = '2D'
    #     else:
    #         raise ValueError('Invalid Value for abscissa[1] (second independent variable)')
    #
    #     self.num_scans[0] = self.ui.num_scans_spbx.value()
    #     self.num_scans[1] = self.ui.num_scans_dim2_spbx.value()
    #
    #     self.averaging_time = self.ui.averaging_time_spbx.value()
    #
    #     self.column_headers = [self.abscissa_name[0], self.output_name[0], self.output_name[1]]
    #     # self.ave_data_df = pd.DataFrame(columns=self.column_headers)
    #
    #     self.actual_x_values = np.empty((self.step_count[0], 1))
    #     self.actual_x_values[:] = np.nan
    #     self.actual_x_values = self.actual_x_values.flatten()
    #
    #     # self.axis_1.clear()
    #     # self.axis_2.clear()
    #     # self.set_1d_plot_properties()

    @helpers.measure_time
    def collect_data(self, filename=None, filetype=None):
        #TODO: Incorporate 2D Data
        # 1. SAMPLING Rate for the SR844 is currently used no matter which lock-in you choose (bad)
        print('---------------------------------- BEGINNING MAIN EXPERIMENT LOOP -------------------------------------')
        mm = 0
        while mm < self.num_scans[1]:
            # Repeat entire 2D scan mm times
            # if self.abort_scan is True:
            #     return
            # while self.pause_scan is True:
            #     time.sleep(0.05)

            if self.num_dims == 2:
                # If 2D data, column headers should be the "actual value" of the second dimension (not yet known)
                self.column_headers_2d = [self.abscissa_name[0] + '\\' + self.abscissa_name[1]]
                self.ave_data_ch1_df.append(pd.DataFrame(columns=self.column_headers_2d))
                self.ave_data_ch2_df.append(pd.DataFrame(columns=self.column_headers_2d))

            ll = 0
            while ll < self.step_count[1]:
                # All stopping points in the second dimension (abscissa[1])
                if self.abort_scan is True:
                    return
                while self.pause_scan is True:
                    time.sleep(0.05)

                # As long as the plot is 1D, we'll have to clear it before each 2nd Dimension change
                line1, line2, line3, line4 = None, None, None, None
                self.axis_1.clear()
                self.axis_2.clear()
                self.set_1d_plot_properties()

                # These storage variables must be refreshed when they are to be reused for the 2nd dimensional scan
                self.ch1_scans_df = pd.DataFrame(columns=[self.abscissa_name[0]] + (np.arange(1, self.num_scans[0] + 1)).tolist())
                self.ch2_scans_df = pd.DataFrame(columns=[self.abscissa_name[0]] + (np.arange(1, self.num_scans[0] + 1)).tolist())
                self.ave_data_df = pd.DataFrame(columns=self.column_headers)

                if self.num_dims == 2:
                    next_step_dim2 = self.step_pts[1][ll]
                    print('Next Step (dim2) is: ' + str(next_step_dim2) + '(' + str(ll + 1) + ' of ' + str(self.step_count[1]) + ')')
                    self.current_position[1] = float(self.set_abscissa(which_abscissa=1, next_step=next_step_dim2))
                    self.axis_1.set_title(str(self.current_position[1]) + self.units[1])
                    self.ave_data_ch1_df[mm].insert(loc=ll+1, column=str(self.current_position[1]), value=np.nan)
                    self.ave_data_ch2_df[mm].insert(loc=ll+1, column=str(self.current_position[1]), value=np.nan)
                else:
                    self.current_position[1] = None

                jj = 0
                while jj < self.num_scans[0]:
                    # if self.abort_scan is True:
                    #     return
                    # while self.pause_scan is True:
                    #     time.sleep(0.05)
                    print('------------------------------------ SCAN %d -----------------------------------------' % jj)
                    ii = 0
                    while ii < self.step_count[0]:
                        # This loops over all the points for abscissa_1
                        if self.abort_scan is True:
                            return
                        while self.pause_scan is True:
                            time.sleep(0.05)

                        next_step = self.step_pts[0][ii]
                        print('Next Step (dim1 ) is: ' + str(next_step) + '(' + str(ii+1) + ' of ' + str(self.step_count[0]) + ')')

                        self.current_position[0] = float(self.set_abscissa(which_abscissa=0, next_step=next_step))

                        self.ch1_scans_df.loc[ii, jj+1], self.ch2_scans_df.loc[ii, jj+1] = self.get_lockin_results()

                        self.distribute_results(ii, jj, ll, mm)

                        line1, line2, line3, line4 = self.plot_results(ii, jj, line1, line2, line3, line4)
                        ii = ii + 1
                    self.save_stuff(filename, filetype, 'jj', sc_idx_1d=jj, sc_idx_2d=mm, manual=False) # 1D scans + ave
                    jj = jj + 1
                self.save_stuff(filename, filetype, 'll', sc_idx_1d=jj, sc_idx_2d=mm, manual=False)  # Ave of 1D scans
                ll = ll + 1
            # self.save_stuff(filename, filetype, 'mm', sc_idx_1d=jj, sc_idx_2d=mm, manual=False)    # Save each 2D scan
            mm = mm+1
        # self.save_stuff(filename, filetype, 'end', sc_idx_1d=jj, sc_idx_2d=mm, manual=False) # Ave of 2Dscans(not yet)
        self.abort_scan = False
        print('------------------------------------- EXPERIMENT COMPLETED --------------------------------------------')

    @helpers.measure_time
    def set_abscissa(self, which_abscissa, next_step):
        wa = which_abscissa
        if self.abscissae[wa] == 0:  # Empty Header line
            pass
        elif self.abscissae[wa] == 1:  # Pump Modulation Frequency
            print('------------------------ SETTING CG635 MODULATION FREQUENCY -----------------------')

            if self.cg635_connected is False:
                print('Cg635 was not connected')

                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                'Text': ' Experiment Aborted',
                                                'Informative Text': 'CG635 Communication is not set up',
                                                'Details': None})
                self.abort_scan = True
                return None
            else:
                self.cg635.set_freq(freq_to_set=next_step, scaling_factor=1)
                if self.cg635.error.status:
                    print('This is a somewhat unhandled error')
                    # error_message_window('Scan Aborted, CG635 Error', inform_text=error)
                    # self.general_error_signal.emit({'Title': ' - Warning - ',
                    #                                 'Text': 'Scan Aborted, CG635 Error',
                    #                                 'Informative Text': error})
                    self.abort_scan = True
                    return
                print('Frequency is now at: ' + str(self.cg635.settings.current_freq))
                actual_pos = self.cg635.settings.current_freq
        elif self.abscissae[wa] == 2:  # Probe Wavelength
            print('------------------------ SETTING PROBE WAVELENGTH -----------------------')
            if self.md2000.settings.connected is False:
                print('MD2000 was not connected')

                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                'Text': ' Experiment Aborted',
                                                'Informative Text': 'Monochromator Communication is not set up',
                                                'Details': None})
                self.abort_scan = True
                return None
            elif self.md2000.error.status:
                print('MD2000 had a pre-existing error')
                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                'Text': ' Experiment Aborted',
                                                'Informative Text': 'Monochromator Communication Error Found',
                                                'Details': None})
                self.abort_scan = True
                return None
            else:
                self.md2000.go_to_wavelength(destination=next_step, backlash_amount=self.settings.md2000.bl_amt,
                                             backlash_bool=self.settings.md2000.bl_bool)
                actual_pos = self.md2000.current_wavelength

        elif self.abscissae[wa] == 3:  # Static Magnetic Field
            print('This case has not been coded yet')
        elif self.abscissae[wa] == 4:  # RF Carrier Frequency
            print('This case has not been coded yet')
        elif self.abscissae[wa] == 5:  # RF Modulation Frequency
            print('This case has not been coded yet')
        elif self.abscissae[wa] == 6:  # TBD
            print('This case has not been coded yet')
        else:
            print('there are this many possible abscissae?')

        return actual_pos

    @helpers.measure_time
    def get_lockin_results(self):
        print('Checking for lock-in issues...')
        # As in overloads, phase locking to reference, etc.
        self.lockin.open_comms()  # Open also sets the correct GPIB address
        self.lockin.comms.write('*CLS\n')
        self.lockin.clear_buffers()

        if self.offset_each is True:

            self.toptica.laser_disable()

            lia_status = self.lockin.check_status()
            kk = 0
            while not lia_status == 0 and kk < 200:
                lia_status = self.lockin.check_status()
                if lia_status == -1:  # Comm failure
                    return
                # print('lia error' + str(lia_error))
                # print('loop iteration: ' + str(kk))
                time.sleep(0.001)
                kk = kk + 1

            if not lia_status == 0:  # -1 cases (comm errors) should be removed by now
                self.pause_scan = True
                # The following should be optimized
                self.lockin_status_warning_signal.emit(str(lia_status))

            print('Pausing for Lock-in settling...')
            print('lockin_delay: ' + str(self.lockin_delay))
            time.sleep(self.lockin_delay)  # Wait for the lock-in output to settle

            if self.settings.ui.scan_auto_sens_checkbox.isChecked():
                print('Optimizing Lock-in Sensitivity...')
                self.lockin.auto_sens()

            self.lockin.comms.write('AOFF 1, 1\n')
            self.toptica.laser_enable()
            self.toptica.laser_start()

        lia_status = self.lockin.check_status()
        kk = 0
        # It may take some time for the lockin internal oscillator  to lock to the reference freq
        while not lia_status == 0 and kk < 200:
            lia_status = self.lockin.check_status()
            if lia_status == -1:  # Comm failure
                return
            # print('lia error' + str(lia_error))
            # print('loop iteration: ' + str(kk))
            time.sleep(0.001)
            kk = kk + 1

        if not lia_status == 0:  # -1 cases (comm errors) should be removed by now
            self.pause_scan = True
            # The following should be optimized
            self.lockin_status_warning_signal.emit(str(lia_status))

        print('Pausing for Lock-in settling...')
        print('lockin_delay: ' + str(self.lockin_delay))
        time.sleep(self.lockin_delay)  # Wait for the lock-in output to settle

        if self.settings.ui.scan_auto_sens_checkbox.isChecked():
            print('Optimizing Lock-in Sensitivity...')
            self.lockin.auto_sens()

        print('Collecting Data....')
        ch1_data, ch2_data = self.lockin.collect_data(self.averaging_time, self.settings.lia.sampling_rate,
                                                      record_both_channels=True)
        print('Averaging New Data...')
        ch1 = np.average(ch1_data)
        ch2 = np.average(ch2_data)
        return ch1, ch2

    @helpers.measure_time
    def distribute_results(self, ii, jj, ll, mm):
        if jj == 0:
            self.actual_x_values[ii] = self.current_position[0]
            self.ch1_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
            self.ch2_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
            self.ave_data_df.loc[ii, self.column_headers[0]] = self.current_position[0]
            if self.num_dims == 2:
                self.ave_data_ch1_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]
                self.ave_data_ch2_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]

        ch1_df_mean = self.ch1_scans_df.iloc[:, 1:].mean(axis=1)  # Average all columns except the first
        ch2_df_mean = self.ch2_scans_df.iloc[:, 1:].mean(axis=1)

        self.ave_data_df.loc[:, self.output_name[0]] = ch1_df_mean
        self.ave_data_df.loc[:, self.output_name[1]] = ch2_df_mean

        if self.num_dims == 2:
            # self.ave_data_ch1_df[mm].loc[:, self.current_position[1]] = ch1_df_mean
            # self.ave_data_ch2_df[mm].loc[:, self.current_position[1]] = ch2_df_mean

            self.ave_data_ch1_df[mm].iloc[:, ll+1] = ch1_df_mean
            self.ave_data_ch2_df[mm].iloc[:, ll+1] = ch2_df_mean

        print('self.ave_data_df:')
        print(self.ave_data_df)

    @helpers.measure_time
    def plot_results(self, ii, jj, line1, line2, line3, line4):
        # x_val_current = self.ch1_scans_df.iloc[0:ii+1, 0].to_numpy()
        print('inside plot results')
        color1 = '#0000FF'  # Blue
        color2 = '#FF0000'  # Red
        self.axis_1.set_xlabel(self.abscissa_name[0])
        self.axis_1.set_ylabel(self.output_name[0], c=color1)

        self.axis_1.tick_params(axis='y', labelcolor=color1)

        self.axis_2.set_ylabel(self.output_name[1], c=color2)

        self.axis_2.tick_params(axis='y', labelcolor=color2)

        if jj == 0:
            if ii > 0:
                line1.remove()
                line2.remove()

            color_plot1 = '#0000FF'  # Blue
            color_plot2 = '#FF0000'  # Red
            # ch_1_array_current (and 2) were both 1d arrays of values. Same for ch_1_array_average
            line1, = self.axis_1.plot(self.ch1_scans_df.iloc[:, 0], self.ch1_scans_df.iloc[:, jj+1], ls='None', marker='o',
                                      markersize=5, c=color_plot1, label='Current Scan')
            # line1, = self.axis_1.plot(self.actual_x_values_current, ch_1_array_current, ls='None', marker='o',
            #                           markersize=5, c=color_plot1, label='Current Scan')
            line2, = self.axis_2.plot(self.ch2_scans_df.iloc[:, 0], self.ch2_scans_df.iloc[:, jj+1], ls='None', marker='o',
                                      markersize=5, c=color_plot2, label='Current Scan')
            # line2, = self.axis_2.plot(self.actual_x_values_current, ch_2_array_current, ls='None', marker='o',
            #                           markersize=5, c=color_plot2, label='Current Scan')
            self.axis_1.legend(loc=2)
            self.axis_2.legend(loc=1)
        elif jj > 0:
            line1.remove()
            line2.remove()

            if ii > 0 or jj > 1:
                line3.remove()
                line4.remove()

            color_plot1 = '#BFBFFF'
            color_plot2 = '#FFBFBF'

            line1, = self.axis_1.plot(self.ch1_scans_df.iloc[:, 0], self.ch1_scans_df.iloc[:, jj+1], ls='None', marker='o',
                                      markersize=5, c=color_plot1, label='Current Scan')
            line2, = self.axis_2.plot(self.ch2_scans_df.iloc[:, 0], self.ch2_scans_df.iloc[:, jj+1], ls='None', marker='o',
                                      markersize=5, c=color_plot2, label='Current Scan')

            # Averages
            line3, = self.axis_1.plot(self.ave_data_df.iloc[:, 0], self.ave_data_df.iloc[:, 1], ls='None', marker='o',
                                      markersize=5, c='#0000FF', label='Average')
            line4, = self.axis_2.plot(self.ave_data_df.iloc[:, 0], self.ave_data_df.iloc[:, 2], ls='None', marker='o',
                                      markersize=5, c='#FF0000', label='Average')

            self.axis_1.legend(loc=2)
            self.axis_2.legend(loc=1)
        self.ui.PlotWidget.canvas.draw()
        return line1, line2, line3, line4

    @helpers.measure_time
    def save_stuff(self, filename=None, filetype=None, loop_index=None, sc_idx_1d=0, sc_idx_2d=0, manual=False):
        if self.data_details is None:
            self.status_message_signal.emit('No stored data to save')
            return

        obs1, obs2 = self.data_details.output_names[:]      # as in observable 1 and 2 (R/Theta or X/Y)
        # If the user requested to save AFTER collecting the data, then a directory will need to be created
        if manual is True:
            filename, filetype = self.save_file_dialog()

            if filename is not None:
                os.mkdir(filename)
                filename = filename + '\\'
            else:
                return

        # If the user didn't cancel saving
        if filename is not None:
            if loop_index == 'jj' or manual is True:
                # After each 1D scan, save that scan
                if self.data_details.num_dims == 1:
                    # Overwrite file to create growing data matrix (number of points (rows) x number of scans (cols)
                    fname = filename + 'Scans - '
                    self.save_data(data_frame=self.ch1_scans_df, filename=(fname + obs1), filetype=filetype)
                    self.save_data(data_frame=self.ch2_scans_df, filename=(fname + obs2), filetype=filetype)
                    if sc_idx_1d > 0 or (manual is True and self.data_details.num_scans[0] > 0):
                        # If more than one scan has occurred, save the average. Overwrite that file after add'l scans
                        self.save_data(data_frame=self.ave_data_df, filename=(filename + 'Ave Data'), filetype=filetype)
                        self.status_message_signal.emit('Updated and Saved Average Data........')
                elif self.data_details.num_dims == 2 and manual is False:
                    # Overwrite file to create growing matrix (number of 1st-D pts (rows) x number of 1st-D scans (cols)
                    # Each 2nd-D pt gets its own file with a distinct name.
                    fname = (filename + str(self.current_position[1]) + self.units[1] + ', Scans - ')
                    self.save_data(data_frame=self.ch1_scans_df, filetype=filetype, filename=fname + obs1)
                    self.save_data(data_frame=self.ch2_scans_df, filetype=filetype, filename=fname + obs2)
                self.status_message_signal.emit('Saved Scan Data.......')

            if self.data_details.num_dims == 2 and (loop_index == 'll' or manual is True):
                # Save each 2D scan (each one is a matrix)
                if manual is False:
                    fn = filename + '2D Scan ' + str(sc_idx_2d) + ' - '
                    self.save_data(data_frame=self.ave_data_ch1_df[sc_idx_2d], filetype=filetype, filename=(fn + obs1))
                    self.save_data(data_frame=self.ave_data_ch2_df[sc_idx_2d], filetype=filetype, filename=(fn + obs2))
                    self.status_message_signal.emit('Saved 2D Scan Data........')
                    # Ideally we would add an if statement to average together multiple 2D scans. But idk how yet
                elif manual is True:
                    fn = filename + '2D Scan ' + str(sc_idx_2d) + ' - '
                    for scan in range(0, len(self.ave_data_ch1_df)):
                        self.save_data(data_frame=self.ave_data_ch1_df[scan], filetype=filetype, filename=(fn + obs1))
                        self.save_data(data_frame=self.ave_data_ch2_df[scan], filetype=filetype, filename=(fn + obs2))
                    self.status_message_signal.emit('Saved 2D Scan Data........')

    # @helpers.measure_time
    # def save_stuff(self, filename=None, filetype=None, loop_index='ii', loop_iteration=0, scan_idx_2d=0, manual=False):
    #
    #     if manual is True:
    #         filename, filetype = self.save_file_dialog()
    #
    #         if filename is not None:
    #             os.mkdir(filename)
    #             filename = filename + '\\'
    #         else:
    #             return
    #
    #     if filename is not None:
    #         if (loop_index == 'jj' or manual is True) and self.data_details.num_scans[0] > 1:
    #             if self.data_details.num_dims == 1:
    #                 self.save_data(data_frame=self.ch1_scans_df,
    #                                filename=(filename + 'Scans - ' + self.data_details.output_names[0]), filetype=filetype)
    #                 self.save_data(data_frame=self.ch2_scans_df,
    #                                filename=(filename + 'Scans - ' + self.data_details.output_names[1]), filetype=filetype)
    #             elif self.data_details.num_dims == 2 and manual is False:
    #                 self.save_data(data_frame=self.ch1_scans_df, filetype=filetype,
    #                                filename=(filename + str(self.current_position[1]) + self.units[1] +
    #                                          ', Scans - ' + self.data_details.output_names[0]))
    #                 self.save_data(data_frame=self.ch2_scans_df, filetype=filetype,
    #                                filename=(filename + str(self.current_position[1]) + self.units[1] +
    #                                          ', Scans - ' + self.data_details.output_names[1]))
    #             print('-------------------------------Saved Scan Data-----------------------------------------')
    #
    #         elif loop_index == 'll':
    #             if self.data_details.num_dims == 2 and self.data_details.num_scans[1] > 1:
    #                 self.save_data(data_frame=self.ave_data_ch1_df[scan_idx_2d], filetype=filetype,
    #                                filename=(filename + '2D Scan ' + str(loop_iteration) + ' - ' + self.data_details.output_names[0]))
    #                 self.save_data(data_frame=self.ave_data_ch2_df[scan_idx_2d], filetype=filetype,
    #                                filename=(filename + '2D Scan ' + str(loop_iteration) + ' - ' + self.data_details.output_names[1]))
    #                 print('-------------------------------Saved 2D Scan Data--------------------------------------')
    #
    #         elif loop_index == 'end' or manual is True:
    #             if self.data_details.num_dims == 1:
    #                 self.save_data(data_frame=self.ave_data_df, filename=(filename + 'Ave Data'), filetype=filetype)
    #             # elif self.data_details.num_dims == 2 and self.data_details.num_scans[1] <= 1:
    #             #     self.save_data(data_frame=self.ave_data_ch1_df[mm], filetype=filetype,
    #             #                    filename=(filename + 'Ave Data Matrix - ' + self.data_details.output_names[0]))
    #             #     self.save_data(data_frame=self.ave_data_ch2_df[mm], filetype=filetype,
    #             #                    filename=(filename + 'Ave Data Matrix - ' + self.data_details.output_names[1]))
    #             print('--------------------------------------- DATA SAVED---------------------------------------------')
    #         else:
    #             raise ValueError('Invalid loop index for saving data')

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
                filename = filename + '.csv'
                data_frame.to_csv(filename, index=None)
            elif filetype == 'Text Files (*.txt)':
                print('generating .txt files')
                filename = filename + '.txt'
                data_frame.to_csv(filename, sep='\t', index=None)

    # @QtCore.pyqtSlot()
    # def save_manual(self):
    #     filename, filetype = self.save_file_dialog()
    #
    #     if filename is not None:
    #         os.mkdir(filename)
    #         filename = filename + '\\'
    #     else:
    #         return
    #
    #     if self.data_details is not None:

        # if self.data_type == '1D':
        #     self.save_data(data_frame=self.ave_data_df, filename=filename, filetype=filetype)
        #     self.save_data(data_frame=self.ch1_scans_df,
        #                                filename=(filename + 'Scans - ' + self.output_name[0]), filetype=filetype)

    def save_file_dialog(self):
        #TODO: Check what happens when no file is selected
        print('inside save file dialog')
        # tc = self.thread_pool.activeThreadCount()
        # print('Active threads: ' + str(tc))
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, file_type = QFileDialog.getSaveFileName(self, "Save File As:", "",
                                                           "CSV Files (*.csv);;Text Files (*.txt);;All Files (*.*)",
                                                           options=options)
        file_name = file_name.split('.txt')[0].split('.csv')[0]  # In case the user included the extension
        return file_name, file_type

    @QtCore.pyqtSlot(dict)
    def general_error_window(self, window_details):
        """
        Expected details(/format) are(/is): {'Title': '<INSERT TITLE HERE>', 'Text': '<INSERT TEXT HERE>',
         'Informative Text': '<INSERT TEXT HERE>', 'Details': '<INSERT DETAILS HERE>'}
        """
        print('Inside the general_error_window')
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(window_details['Title'])
        msg.setText(window_details['Text'])
        msg.setInformativeText(window_details['Informative Text'])
        msg.setDetailedText(window_details['Details'])
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        print('Made it through window setup')
        ret_val = msg.exec()

    @QtCore.pyqtSlot(object)
    def receive_error_signal(self, error_cluster):
        # Call the error window from here
        print('Error Received')
        print('Sender: ' + str(self.sender()))
        print(error_cluster.details)
        window_details = {'Title': ' - Warning - ',
                          'Text': 'Instrument Error Occurred',
                          'Informative Text': error_cluster.details + '\n\nError Code: ' + str(error_cluster.code),
                          'Details': None
                          }
        self.general_error_window(window_details)

    @QtCore.pyqtSlot(str)
    def lockin_status_warning_window(self, error_message):
        print('Trying to generate error_message_window')

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText('Lock-in Status Register Flagged Issue(s)')
        msg.setInformativeText('One or more lock-in issues are present which may affect your results.\n'
                               'LIA Status Register Value is: ' + str(error_message) + '\n\nContinue Anyway?')
        msg.setWindowTitle(' - Warning - ')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Abort)
        # msg.buttonClicked.connect(msgbtn)
        return_value = msg.exec()
        print('msg.clickedButton(): ' + str(msg.clickedButton()))
        print('msg box return value: ' + str(return_value))
        if return_value == QtWidgets.QMessageBox.Abort:
            self.abort_scan = True
        elif return_value == QtWidgets.QMessageBox.Ok:
            self.pause_scan = False

    # ----------------------------------------- Other Window Slots ---------------------------------------------------

    # @QtCore.pyqtSlot()
    # def open_lockin_window(self):
    #     self.lockin_window = LockinWidget()
    #     self.lockin_window.show()

    @QtCore.pyqtSlot()
    def open_help_window(self):
        self.help_window = HelpWindowForm()
        self.help_window.show()

    @QtCore.pyqtSlot()
    def open_settings_window(self):
        self.settings.show()

    @QtCore.pyqtSlot(str)
    def cg635_freq_changed_slot(self, new_freq):
        self.settings.ui.cg635_set_freq_spbx.setValue(float(new_freq))
        self.ui.pump_mod_freq_spbx.setValue(float(new_freq))

    @QtCore.pyqtSlot()
    def cg635_check_pll_status(self):
        print('Checking for Errors')
        response = self.cg635.check_pll_status()
        self.settings.ui.cg635_response_textedit.setText(response)

    @QtCore.pyqtSlot()
    def cg635_write_manual_cmd(self):
        cmd_to_write = self.settings.ui.cg635_write_cmd_lnedt.text()
        response = self.cg635.write_string(cmd_to_write, read=True, manual=True)
        self.settings.ui.cg635_response_textedit.setText(response)

    def enable_all_ui_objects(self):
        self.ui.variable_2_cbx.setEnabled(True)
        self.ui.sweep_end_spbx_dim2.setEnabled(True)
        self.ui.num_steps_spbx_dim2.setEnabled(True)
        self.ui.sweep_start_spbx_dim2.setEnabled(True)

        self.ui.temp_spbx.setEnabled(True)
        self.ui.probe_wl_spbx.setEnabled(True)
        self.ui.rf_freq_spbx.setEnabled(True)
        self.ui.static_field_spbx.setEnabled(True)
        self.ui.pump_mod_freq_spbx.setEnabled(True)
        self.ui.rf_mod_freq_spbx.setEnabled(True)

    def set_1d_plot_properties(self):
        print('inside set_1d_plot_properties')
        print('self.scaling_pref = ' + str(self.scaling_pref[0]))
        self.axis_1.set_xscale(self.scaling_pref[0])
        print('set xscale')
        if self.step_count[0] != 1:
            print('self.step_count was not 1')
            if self.start[0] < self.end[0]:
                print('start < end')
                if self.scaling_pref[0] == 'linear':
                    print('linear case')
                    self.axis_1.set_xlim(left=(self.start[0] - 0.05 * self.scan_range[0]),
                                         right=(self.end[0] + 0.05 * self.scan_range[0]))
                elif self.scaling_pref[0] == 'log':
                    print('log case')
                    self.axis_1.set_xlim(left=(self.start[0] - 0.1 * self.start[0]),
                                         right=(self.end[0] + 0.1 * self.end[0]))
            elif self.start[0] > self.end[0]:
                print('start > end')
                if self.scaling_pref[0] == 'linear':
                    print('linear case')
                    self.axis_1.set_xlim(left=(self.end[0] - 0.05 * self.scan_range[0]),
                                         right=(self.start[0] + 0.05 * self.scan_range[0]))
                elif self.scaling_pref[0] == 'log':
                    print('log case')
                    self.axis_1.set_xlim(left=(self.end[0] - 0.1 * self.end[0]),
                                         right=(self.start[0] + 0.1 * self.start[0]))
        print('limits set')
        self.axis_1.set_xlabel(self.abscissa_name[0])
        print('label set')
        if self.output_variables == 'R/Theta':
            self.axis_2.set_ylim(bottom=-180, top=180)

        self.ui.PlotWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def calc_steps_from_num(self, dim_idx=0):
        idx = dim_idx
        print('inside calc_from_num')

        if self.abscissae[idx] == 0:
            self.scale_factor[idx] = 1
        elif self.abscissae[idx] == 1:
            self.scale_factor[idx] = 10**(3*self.units_cbxes[idx].currentIndex())
        else:
            self.scale_factor[idx] = 1
        self.end[idx] = (self.sweep_end_spbxs[idx].value()) * self.scale_factor[idx]
        self.start[idx] = (self.sweep_start_spbxs[idx].value()) * self.scale_factor[idx]
        self.step_count[idx] = self.num_steps_spbxs[idx].value()
        self.scan_range[idx] = self.end[idx] - self.start[idx]

        if self.log_spacing[idx]:
            print('inside log case')
            self.scaling_pref[idx] = 'log'
            self.step_size_displays[idx].setText('N/A')
            log_start = np.log10(self.start[idx])
            log_end = np.log10(self.end[idx])
            try:
                if self.step_count[idx] != 1:
                    log_step_size = np.abs(log_end - log_start) / (self.step_count[idx] - 1)
                    step_pts = []

                    if self.start[idx] < self.end[idx]:
                        for ii in range(0, self.step_count[idx]):
                            log_next_step = log_start + (ii * log_step_size)
                            step_pts.append(10 ** log_next_step)

                    else:
                        print('attempting inverted scan direction (log scaling')
                        for ii in range(0, self.step_count[idx]):
                            log_next_step = log_start - (ii * log_step_size)
                            step_pts.append(10 ** log_next_step)

                    self.step_pts[idx] = step_pts

                else:
                    self.step_pts[idx] = [self.start[idx]]

                steps_to_display = str(np.round(np.array(self.step_pts[idx]), 3).tolist()).replace(',', '\r')
                self.steps_displays[idx].setText(steps_to_display)

            except:
                print(sys.exc_info()[:])

        else:
            print('inside linear case')
            self.scaling_pref[idx] = 'linear'

            try:
                if self.step_count[idx] != 1:
                    step_size = np.abs(self.end[idx] - self.start[idx]) / (self.step_count[idx] - 1)
                    self.step_size[idx] = step_size
                    self.step_size_displays[idx].setText(str(round(step_size / self.scale_factor[idx], 4)))
                    step_pts = []
                    if self.start[idx] < self.end[idx]:
                        for ii in range(0, self.step_count[idx]):
                            step_pts.append(self.start[idx] + ii * step_size)

                    else:
                        for ii in range(0, self.step_count[idx]):
                            step_pts.append(self.start[idx] - ii * step_size)

                    self.step_pts[idx] = step_pts
                    # Update plot
                else:
                    self.step_pts[idx] = [self.start[idx]]

                steps_to_display = str(np.round(np.array(self.step_pts[idx]), 3).tolist()).replace(',', '\r')
                self.steps_displays[idx].setText(steps_to_display)

            except:
                print(sys.exc_info()[:])

            print('about to rescale plot')
        self.expt_duration()

    # def expt_duration(self):
    #     #TODO:
    #     # 1. This estimate is only valid for the CG635/Lockin experiments. Incorporate the others
    #     # 2. The condition is kind of stupid at the moment but prevents crashes at least
    #     if self.lockin_delay is not None and self.settings.lia.sampling_rate is not None:
    #         averaging_time = self.ui.averaging_time_spbx.value()
    #         data_transfer_time = self.settings.lia.sampling_rate * averaging_time * 0.00132  # This estimate is good
    #         # 0.00132 is for transferring both channels using TRCL (1.32 ms per sample)
    #         freq_set_delay = 0.44  # Estimated using the CG635
    #         check_lia_delay = 0.44  # Very rough estimate. This one depends a lot on situation
    #         plot_data_delay = 0.16
    #         record_data_delay = self.lockin_delay + averaging_time + data_transfer_time + 0.139
    #         self.num_scans[0] = self.ui.num_scans_spbx.value()
    #         print('--------------------- Expt Duration Estimate-----------------')
    #         print('lockin_delay: ' + str(self.lockin_delay))
    #         print('ave_time: ' + str(averaging_time))
    #         print('Sampling rate: ' + str(self.settings.lia.sampling_rate))
    #         print("num_scans: " + str(num_scans))
    #         print('self.step_count: ' + str(self.step_count))
    #         expt_duration_estimate = self.step_count[0] * self.num_scans[0] * (freq_set_delay + check_lia_delay +
    #                                                                 record_data_delay + plot_data_delay)
    #         self.ui.experiment_duration_lnedt.setText(time.strftime('%H:%M:%S', time.gmtime(expt_duration_estimate)))
    #     else:
    #         self.ui.experiment_duration_lnedt.setText('Connect to Instruments...')

    @helpers.measure_time
    def expt_duration(self):
        if self.abscissae[0] == 0 or self.abscissae[0] is None:
            return
        try:
            averaging_time = self.ui.averaging_time_spbx.value()
            sampling_rate = self.settings.lia.sampling_rate
            mono_speed = self.settings.md2000.speed
            mono_delay_offset = 0.78

            num_steps = [self.step_count[0], self.step_count[1]]
            self.num_scans = [self.ui.num_scans_spbx.value(), self.ui.num_scans_dim2_spbx.value()]
            if self.abscissae[1] == 0:
                self.num_scans[1] = 1
                num_steps[1] = 1
            print('Partway done with duration')
            # scan_range = [self.step_pts[0][-1] - self.step_pts[0][0], self.step_pts[1][-1] - self.step_pts[1][0]]
            # ave_step = [scan_range[0] / num_steps[0], scan_range[1] / num_steps[1]]
            scan_range = [None, None]
            ave_step = [None, None]
            abs_set_delay = [0, 0]
            print('about to start idx loop')
            for idx in range(0, 2):
                try:
                    scan_range[idx] = self.step_pts[idx][-1] - self.step_pts[idx][0]
                except TypeError as err:
                    scan_range[idx] = 0

                try:
                    ave_step[idx] = scan_range[idx] / num_steps[idx]
                except TypeError as err:
                    ave_step[idx] = 0

                if self.abscissae[idx] == 0:
                    pass
                elif self.abscissae[idx] == 1:
                    abs_set_delay[idx] = 0.44
                elif self.abscissae[idx] == 2:
                    abs_set_delay[idx] = (2 * ave_step[idx]) / mono_speed + mono_delay_offset
                elif self.abscissae[idx] == 3:
                    abs_set_delay[idx] = 0
                elif self.abscissae[idx] == 4:
                    abs_set_delay[idx] = 0
                elif self.abscissae[idx] == 5:
                    abs_set_delay[idx] = 0
                elif self.abscissae[0] == 6:
                    abs_set_delay[idx] = 0
            print('2nd partway duration')
            data_transfer_time = sampling_rate * averaging_time * 0.00132  # This estimate is good
            # 0.00132 is for transferring both channels using TRCL (1.32 ms per sample)
            check_lia_delay = 0.55  # Very rough estimate. This one depends a lot on situation
            plot_data_delay = 0.16
            record_data_delay = self.lockin_delay + averaging_time + data_transfer_time + 0.139
            print('almost done duration!')
            estimate_1d = self.step_count[0] * self.num_scans[0] * (abs_set_delay[0] + check_lia_delay +
                                                                    record_data_delay + plot_data_delay)
            expt_duration_estimate = (estimate_1d * self.step_count[1] * self.num_scans[1]) +\
                                     (self.step_count[1] * self.num_scans[1] * (abs_set_delay[1]))
            expt_duration_estimate = round(expt_duration_estimate)
            self.ui.experiment_duration_lnedt.setText(time.strftime('%H:%M:%S', time.gmtime(expt_duration_estimate)))
        except TypeError as err:
            print(err)

    @QtCore.pyqtSlot(bool)
    def autosave_checkbox_toggled(self, autosave_on):
        print('autosave on: ' + str(autosave_on))

    @QtCore.pyqtSlot(bool)
    def log_spacing_checkbox_toggled(self, log_spacing_on, dim_idx):
        self.log_spacing[dim_idx] = log_spacing_on
        print('log_spacing on: ' + str(log_spacing_on) + 'for dim_idx ' + str(dim_idx))
        self.calc_steps_from_num(dim_idx=dim_idx)

    @QtCore.pyqtSlot(int)
    def abscissa_changed(self, var_idx, abscissa_idx):
        print('abscissa %d selected for change' % abscissa_idx)
        self.abscissae[abscissa_idx] = var_idx

        if self.abscissae[abscissa_idx] == 0:
            self.abscissae[abscissa_idx] = None
        elif self.abscissae[abscissa_idx] == 1:
            print('Pump Mod Selected')
            self.x_axis_label = 'Pump Modulation Frequency (Hz)'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
            self.units[abscissa_idx] = 'Hz'

            try:
                self.sweep_start_spbxs[abscissa_idx].setValue(self.settings.presets.pump_mod_freq_start)
                self.sweep_end_spbxs[abscissa_idx].setValue(self.settings.presets.pump_mod_freq_end)
                self.num_steps_spbxs[abscissa_idx].setValue(self.settings.presets.pump_mod_freq_steps)

                self.units_cbxes[abscissa_idx].clear()
                self.units_cbxes[abscissa_idx].addItems(['Hz', 'kHz', 'MHz', 'GHz'])
                self.units_cbxes[abscissa_idx].setCurrentIndex(1)
                self.units_cbxes[abscissa_idx].setEnabled(True)

                self.log_spacing_checkboxes[abscissa_idx].setChecked(True)
                self.log_spacing[abscissa_idx] = True

                self.calc_steps_from_num(dim_idx=abscissa_idx)
            except:
                print(sys.exc_info()[:])

        elif self.abscissae[abscissa_idx] == 2:
            print('Probe wl selected')
            self.x_axis_label = 'Probe Wavelength (nm)'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
            self.units[abscissa_idx] = 'nm'

            try:
                self.sweep_start_spbxs[abscissa_idx].setValue(self.settings.presets.probe_wl_start)
                self.sweep_end_spbxs[abscissa_idx].setValue(self.settings.presets.probe_wl_end)
                self.num_steps_spbxs[abscissa_idx].setValue(self.settings.presets.probe_wl_num_steps)

                self.units_cbxes[abscissa_idx].clear()
                self.units_cbxes[abscissa_idx].addItems(['nm'])
                self.units_cbxes[abscissa_idx].setCurrentIndex(0)
                self.units_cbxes[abscissa_idx].setEnabled(False)

                print('set presets')
                self.log_spacing_checkboxes[abscissa_idx].setChecked(False)

                self.calc_steps_from_num(dim_idx=abscissa_idx)
            except:
                print(sys.exc_info()[:])
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Probe Wavelength (nm)')
        elif self.abscissae[abscissa_idx] == 3:
            print('Static Field Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Static Magnetic Field (Gauss)')
        elif self.abscissae[abscissa_idx] == 4:
            print('RF Carrier Freq Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Carrier Frequency (GHz)')
        elif self.abscissae[abscissa_idx] == 5:
            print('RF Mod Freq Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Modulation Frequency (Hz)')

    @QtCore.pyqtSlot(str)
    def experiment_preset_cbx_activated(self, experiment_str):
        print(experiment_str)
        if experiment_str == '-Manual Setup-':
            self.enable_all_ui_objects()
        elif experiment_str == 'Optical Absorption Spectrum':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(2)
            self.ui.variable_2_cbx.setCurrentIndex(0)
            self.ui.variable_2_cbx.setEnabled(False)
            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)

            self.ui.sweep_start_spbx_dim2.setEnabled(False)
            self.ui.sweep_end_spbx_dim2.setEnabled(False)
            self.ui.num_steps_spbx_dim2.setEnabled(False)
            print('Completed Experiment Preset Setup')

        elif experiment_str == 'PL Lifetime':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(1)                               # Pump Modulation Frequency = 1
            self.ui.variable_2_cbx.setCurrentIndex(0)
            self.ui.variable_2_cbx.setEnabled(False)
            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)
            print('Disabled First Set')

            self.ui.sweep_start_spbx_dim2.setEnabled(False)
            self.ui.sweep_end_spbx_dim2.setEnabled(False)
            self.ui.num_steps_spbx_dim2.setEnabled(False)

            print('Completed PL Lifetime Preset Setup')

        elif experiment_str == 'PA Lifetime':
            print('experiment not set up yet')
        elif experiment_str == 'PA Lifetime (Single WL)':
            print('experiment not set up yet')
        else:
            print('experiment/case not set up yet')

    @QtCore.pyqtSlot()
    def pause_btn_clicked(self):
        if self.ui.pause_btn.text() == 'Pause':
            self.pause_scan = True
        elif self.ui.pause_btn.text() == 'Resume':
            self.pause_scan = False

    @QtCore.pyqtSlot()
    def stop_btn_clicked(self):
        self.abort_scan = True
        print('Aborting Scan')

    @QtCore.pyqtSlot(int)
    def set_pump_mod_units(self, idx):
        self.settings.ui.cg635_freq_units_cbx.setCurrentIndex(idx)
        self.ui.pump_mod_freq_units_cbx.setCurrentIndex(idx)
        self.cg635.set_freq_units(idx)

    @QtCore.pyqtSlot()
    def clear_instr_errors(self):
        self.lockin.error = ErrorCluster(status=False, code=0, details='')
        self.cg635.error = ErrorCluster(status=False, code=0, details='')
        self.md2000.error = ErrorCluster(status=False, code=0, details='')
        self.toptica.error = ErrorCluster(status=False, code=0, details='')

    @QtCore.pyqtSlot(str, str, float)  # This is called "overloading" a signal and slot. This is now TWO slots
    @QtCore.pyqtSlot(str, str, int)  # Which require different variable type inputs. str, int is default if unspec'd
    def update_instr_property(self, instr, prop_name, new_val):
        print('Attempting to update ' + instr + prop_name + ' to value: ' + str(new_val))
        if instr == 'lockin':
            setattr(self.lockin.settings, prop_name, new_val)
            setattr(self.settings.lia, prop_name, new_val)
        elif instr == 'md2000':
            setattr(self.md2000.settings, prop_name, new_val)
            setattr(self.settings.md2000, prop_name, new_val)
            self.settings.update_md2000_tab()
        elif instr == 'cg635':
            setattr(self.cg635.settings, prop_name, new_val)
            setattr(self.settings.cg, prop_name, new_val)
        elif instr == 'toptica':
            setattr(self.toptica.settings, prop_name, new_val)
            setattr(self.settings.toptica, prop_name, new_val)
            self.settings.update_topt_tab()
        else:
            raise ValueError('Cannot update ' + instr + ' - invalid instrument identifier')
        self.expt_duration()

    def set_icons(self):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\settings_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionSettings.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\help-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionHelp.setIcon(icon2)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionSave_Data.setIcon(icon3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\connect_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionConnect_All.setIcon(icon4)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\play_pause_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pause_btn.setIcon(icon5)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(r"C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\icons"
                                      r"\arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.go_to_temp_btn.setIcon(icon6)
        self.ui.go_to_probe_wl_btn.setIcon(icon6)
        self.ui.go_to_rf_freq_btn.setIcon(icon6)
        self.ui.go_to_pump_mod_freq_btn.setIcon(icon6)
        self.ui.go_to_rf_mod_freq_btn.setIcon(icon6)
        self.ui.go_to_static_field_btn.setIcon(icon6)
        self.settings.ui.toptica_set_power_btn.setIcon(icon6)
        self.settings.ui.toptica_set_bias_power_btn.setIcon(icon6)

    def connect_signals_and_slots(self):
        """
        Connect signals and slots here. lambda functions are used to expand functionality options by allowing inclusion
        of additional arguments and/or multiple function calls from a single signal, as well as performing simple tasks.
        """

        # TODO:
        # 1. CG635_write_btn could be potentially replaced with the lnedt "Text Edited"
        # -------------------------------------------- ERRORS AND WARNINGS ---------------------------------------------
        self.lockin_status_warning_signal.connect(self.lockin_status_warning_window)
        self.general_error_signal.connect(self.general_error_window)

        self.settings.ui.clear_instr_errors_btn.clicked.connect(self.clear_instr_errors)
        self.lockin.send_error_signal.connect(self.receive_error_signal)
        self.cg635.send_error_signal.connect(self.receive_error_signal)
        self.toptica.send_error_signal.connect(self.receive_error_signal)
        self.md2000.send_error_signal.connect(self.receive_error_signal)

        # ----------------------------------------- PROPERTIES UPDATED -------------------------------------------------
        self.lockin.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('lockin', i, j))
        self.lockin.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('lockin', i, j))

        self.cg635.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('cg635', i, j))
        self.cg635.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('cg635', i, j))

        self.md2000.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('md2000', i, j))
        self.md2000.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('md2000', i, j))

        self.toptica.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('toptica', i, j))
        self.toptica.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('toptica', i, j))

        # --------------------------------------------- GENERAL --------------------------------------------------------
        # self.settings.ui.smb100a_com_port_cmb.currentTextChanged[str].connect(
        # lambda i: self.update_instr_property('smb100a', 'com_port', i))
        self.settings.ui.md2000_com_port_cmb.currentTextChanged[str].connect(
            lambda i: [self.update_instr_property('md2000', 'com_port', i),
                       self.settings.ui.status_ind_md2000.setText(self.label_strings.off_led_str)])

        self.settings.ui.prologix_com_port_cmb.currentTextChanged[str].connect(
            lambda i: [setattr(self, 'settings.prologix_com_port', i),
                       self.settings.ui.status_ind_sr830.setText(self.label_strings.off_led_str),
                       self.settings.ui.status_ind_sr844.setText(self.label_strings.off_led_str)])

        self.settings.ui.toptica_com_port_cmb.currentTextChanged[str].connect(
            lambda i: [self.update_instr_property('toptica', 'com_port', i),
                       self.settings.ui.status_ind_toptica.setText(self.label_strings.off_led_str)])

        self.settings.ui.lockin_delay_scale_spbx.valueChanged[float].connect(
            lambda i: self.update_instr_property('lockin', 'settling_delay_factor', i))

        self.settings.ui.connect_instr_btn.clicked.connect(self.connect_instruments)
        self.ui.log_spacing_checkbox.toggled['bool'].connect(lambda i: self.log_spacing_checkbox_toggled(i, dim_idx=0))
        self.ui.log_spacing_checkbox_dim2.toggled['bool'].connect(
            lambda i: self.log_spacing_checkbox_toggled(i, dim_idx=1))

        # ------------------------------------------ MAIN WINDOW -------------------------------------------------------
        self.status_message_signal[str].connect(lambda i: [self.ui.statusbar.showMessage(i, 5000), print(i)])

        self.ui.pump_mod_freq_units_cbx.activated[int].connect(self.set_pump_mod_units)
        self.ui.pump_mod_freq_spbx.valueChanged[float].connect(
            lambda i: self.cg635.set_freq(i, scaling_factor=10 ** (3 * self.settings.ui.cg635_freq_units_cbx.currentIndex())))

        self.ui.sweep_start_spbx_dim2.valueChanged[float].connect(lambda: self.calc_steps_from_num(dim_idx=1))
        self.ui.sweep_end_spbx_dim2.valueChanged[float].connect(lambda: self.calc_steps_from_num(dim_idx=1))
        self.ui.log_spacing_checkbox_dim2.toggled['bool'].connect(lambda: self.calc_steps_from_num(dim_idx=1))
        self.ui.num_steps_spbx_dim2.valueChanged[int].connect(lambda: self.calc_steps_from_num(dim_idx=1))
        self.ui.sweep_units_cbx_dim2.activated[int].connect(lambda: self.calc_steps_from_num(dim_idx=1))

        self.ui.num_scans_spbx.valueChanged[int].connect(lambda i: setattr(self, 'num_scans[0]', i))

        self.ui.variable_1_cbx.currentIndexChanged[int].connect(lambda i: self.abscissa_changed(i, abscissa_idx=0))
        self.ui.variable_2_cbx.currentIndexChanged[int].connect(lambda i: self.abscissa_changed(i, abscissa_idx=1))

        self.ui.start_btn.clicked.connect(self.start_experiment)
        self.ui.actionSave_Data.triggered.connect(lambda: self.save_stuff(manual=True))

        # ----------------------------------------- TOPTICA LASER ------------------------------------------------------
        self.settings.toptica_enable_signal.connect(self.toptica.laser_enable)
        self.settings.toptica_start_signal.connect(self.toptica.laser_start)
        self.settings.ui.toptica_bias_enable_btn.clicked.connect(self.toptica.laser_enable)
        self.settings.ui.toptica_start_laser_btn.clicked.connect(self.toptica.laser_start)
        self.settings.toptica_stop_signal.connect(self.toptica.laser_disable)
        self.settings.ui.toptica_enable_digital_input_btn.clicked.connect(self.toptica.start_digital_modulation)
        self.settings.ui.toptica_stop_mod_btn.clicked.connect(self.toptica.stop_digital_modulation)

        self.settings.ui.toptica_set_power_btn.clicked.connect(
            lambda: self.toptica.set_power(power_value=self.settings.ui.toptica_power_spbx.value()))

        self.settings.ui.toptica_set_bias_power_btn.clicked.connect(
            lambda: self.toptica.set_power(power_value=self.settings.ui.toptica_bias_spbx.value()))

        # ----------------------------------------- CG635 ----------------------------------------
        self.settings.ui.cg635_run_btn.clicked.connect(self.cg635.run)
        self.settings.ui.cg635_stop_btn.clicked.connect(self.cg635.stop)
        self.settings.ui.cg635_set_current_phase_zero_btn.clicked.connect(self.cg635.set_phase_as_zero)
        self.settings.ui.cg635_check_pll_btn.clicked.connect(self.cg635_check_pll_status)
        self.settings.ui.cg635_write_btn.clicked.connect(self.cg635_write_manual_cmd)
        self.settings.ui.cg635_set_phase_spbx.valueChanged[float].connect(self.cg635.set_phase)
        self.settings.ui.cg635_set_freq_spbx.valueChanged[float].connect(
            lambda i: self.cg635.set_freq(i, scaling_factor=10 ** (3 * self.settings.ui.cg635_freq_units_cbx.currentIndex())))

        self.settings.ui.cg635_max_freq_spbx.valueChanged[float].connect(self.cg635.set_max_freq)
        self.settings.ui.cg635_freq_units_cbx.activated[int].connect(self.set_pump_mod_units)

        # ------------------------------------------- LOCK-IN ----------------------------------------------------------

        # Single parameter changes:
        self.settings.ui.auto_creserve_btn.clicked.connect(self.lockin.auto_crsrv)
        self.settings.ui.auto_dyn_reserve_btn.clicked.connect(self.lockin.auto_dyn_rsrv)
        self.settings.ui.auto_wreserve_btn.clicked.connect(self.lockin.auto_wrsrv)
        self.settings.ui.auto_offset_btn.clicked.connect(self.lockin.auto_offset)
        self.settings.ui.auto_phase_btn.clicked.connect(self.lockin.auto_phase)
        self.settings.ui.auto_sens_btn.clicked.connect(self.lockin.auto_sens)
        self.settings.ui.close_reserve_cbx.activated[int].connect(self.lockin.update_crsrv)
        self.settings.ui.wide_reserve_cbx.activated[int].connect(self.lockin.update_wrsrv)
        self.settings.ui.dynamic_reserve_cbx.activated[int].connect(self.lockin.update_dyn_rsrv)
        self.settings.ui.expand_cbx.activated[int].connect(self.lockin.update_expand)
        self.settings.ui.filter_slope_cbx.activated[int].connect(self.lockin.update_filter_slope)
        self.settings.ui.sr844_harmonic_cbx.activated[int].connect(self.lockin.update_2f)
        self.settings.ui.harmonic_spbx.valueChanged[int].connect(self.lockin.update_harmonic)
        self.settings.ui.phase_spbx.valueChanged[float].connect(self.lockin.update_phase)
        self.settings.ui.input_impedance_cbx.activated[int].connect(self.lockin.update_input_impedance)
        self.settings.ui.outputs_cbx.activated[int].connect(self.lockin.update_outputs)
        self.settings.ui.ref_impedance_cbx.activated[int].connect(self.lockin.update_ref_impedance)
        self.settings.ui.ref_source_cbx.activated[int].connect(self.lockin.update_ref_source)
        self.settings.ui.sampling_rate_cbx.activated[int].connect(self.lockin.update_sampling_rate)
        self.settings.ui.sensitivity_cbx.activated[int].connect(self.lockin.update_sensitivity)
        self.settings.ui.time_constant_cbx.activated[int].connect(self.lockin.update_time_constant)

        # ---------------------------------- MOno ----------------------------------------------------------------------
        self.md2000.status_message_signal[str].connect(lambda i: self.ui.statusbar.showMessage(i))
        self.settings.ui.mono_set_home_btn.clicked.connect(
            lambda i: self.md2000.set_home_position(self.settings.ui.mono_cal_wl_spbx.value()))
        self.settings.ui.mono_set_wl_spbx.valueChanged[float].connect(
            lambda i: self.md2000.go_to_wavelength(i, self.settings.md2000.bl_amt, self.settings.md2000.bl_bool))
        self.settings.ui.mono_bl_comp_chkbx.toggled[bool].connect(lambda i: self.update_md2000_property('bl_bool', i))
        self.settings.ui.mono_speed_spbx.valueChanged[float].connect(self.md2000.set_speed)
# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)            # Defines the instance of the whole application
    app.setStyle('Fusion')                  # I like the way fusion looks
    expt_control_window = MainWindow()      # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    expt_control_window.show()
    sys.exit(app.exec_())
