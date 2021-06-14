#TODO:
# Priorities:
# 1. Determine optimal delay to use for magnet
# 2. Get UHFLI set up
# 3. Toptica signals/slots/error handling
# 4. Get laser to turn on and off with experiment (And also add a "modulation enabled" indicator)
# 5. Finish setting up 2D experiments
# Various:
# -102. Get bandwidth to update along with the other settings.
# -101. Eliminate redundant updating of UHFLI settings
# -100. Get secondary demodulator in line with primary.
# -99. Get SR830 working again with new code
# -98. Fix transient measurements
# -97. Modify so that settings.main ONLY sets up the settings window? (i.e. does not affect the actual settings).
# -95. Fix labelling of plots for transient measurement
# -92. Make an option for non-50% duty cycles (SMB100a)
# -91. Make RnS source Modulation Trigger Impedance changeable
# -90. Add a "pause after each point" option
# -89. Send email or text when experiment complete
# -88. Give "experiment setup" presets their own standardized format (e.g. DeltaT scan, T, BG, etc.)
# -87. Fast scan option? Does every other point on first scan and then the rest on the next scan. Alternates
# -86. Modify so that abort saves current scan even if incomplete
# -85. Automatically save the plot at the end of an experiment
# -84. Lock-in overload causes crashes in comms with other instruments
# -83. Add an option to only auto adjust the sensitivity if specifically overloaded (for data with large dynamic range)
# -81. Add a "hide Average" and "Hide Current Scan" checkbox for the plots
# -80. Add a "record baseline signal" for zero correction (I'm thinking for T scans, but probably it will apply to others)
# -76. Attempting to restart experiment after aborting due to lock-in not locking, caused crash
# -75. Reset Scan Entries when Abscissa is set to 0 (also rename this to ' - None - ' ?)
# -74. Move number of scans to the respective abscissa block (ui objects)
# -73. Change saving so that if only 1 scan, Ave Data is saved (rather than scans)
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
import pyqtgraph as pg
import zhinst
from pyqtgraph import PlotWidget, plot

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QThreadPool, QRunnable  # For multithreading (parallel tasks)
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

import padmr.instr.mono.main
from padmr.instr.mono.controls import MonoDriver
from padmr.instr.mono.main import MainWindow as MonoControl
from padmr.instr.laser.controls import TopticaInstr
from padmr.instr.cg635.controls import CG635Instrument
from padmr.instr.cryostat.controls import CryostatInstr
from padmr.instr.smb100a.controls import SMB100AInstrument

from padmr.instr.lia.main import LockinWidget
from padmr.instr.lia.controls import PrologixAdaptedSRLockin, ErrorCluster
from padmr.instr.zurich_lia.controls import ZiLIA, ErrorCluster
from padmr.gui import Ui_MainWindow as ExptControlMainWindow

from padmr.supp.help_window.main import HelpWindowForm
from padmr.supp.settings.main import SettingsWindowForm
from padmr.supp.label_strings import LabelStrings
from padmr.supp import helpers

pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))


class PlottedData:
    def __init__(self, dims=1, output_names=['Channel 1', 'Channel 2'], num_scans=[1, 1], notes='',
                 instr_settings=None):
        self.num_dims = dims
        self.output_names = output_names
        self.num_scans = num_scans
        self.details = notes
        self.instr_settings = instr_settings

# class ScanData:
#     def __init__(self):
#         self.headers = []
#         self.indep_var = []
#         self.data = []
#     def add_data_point(self, row_idx, col_name):
#         pass

class StoredData:
    def __init__(self):  #, num_scans_2d, num_steps_2d, num_scans, num_steps):
        self.scans_2d = []

    def add_2d_scan(self):
        self.scans_2d.append([])

    def add_2d_step(self, scan_2d_idx):
        self.scans_2d[scan_2d_idx].append([])

    def add_scan(self, sweep_results_dataframe, scan_2d_idx, step_2d_idx):
        while scan_2d_idx > (len(self.scans_2d) - 1):
            self.add_2d_scan()
        while step_2d_idx > (len(self.scans_2d[scan_2d_idx]) - 1):
            self.add_2d_step(scan_2d_idx)

        self.scans_2d[scan_2d_idx][step_2d_idx].append(sweep_results_dataframe)

    def replace_scan(self, sweep_results_dataframe, scan_2d_idx, step_2d_idx, scan_idx):
        self.scans_2d[scan_2d_idx][step_2d_idx][scan_idx] = sweep_results_dataframe

class MainWindow(QMainWindow):
    sr_lockin_status_warning_signal = QtCore.pyqtSignal(str)
    general_error_signal = QtCore.pyqtSignal(dict)
    status_message_signal = QtCore.pyqtSignal(str)
    results_are_in_signal = QtCore.pyqtSignal([int, int])
    change_plot_title_signal = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

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
        self.cryostat_connected = False
        # self.toptica_connected = False
        self.is_debug_mode = False

        self.offset_each = False
        self.label_strings = LabelStrings()

        self.abort_scan = False
        self.pause_scan = False
        self.experiment_in_progress = False

        self.lockin_delay = 0

        # ---- Plot Stuff---
        self.x_axis_label = None
        self.abscissa_name = ['Indep Var 1', 'Indep Var 2']
        self.output_name = ['Channel 1', 'Channel 2']

        self.plot1 = None
        self.plot2 = None
        self.plot3 = None
        self.plot4 = None
        self.ui.PlotWidget.setBackground('w')
        self.ui.PlotWidget2.setBackground('w')

        self.line_width = 1
        self.marker_size = (self.line_width / 1.2)
        self.line_style = QtCore.Qt.SolidLine

        # self.scan_range = None
        self.output_variables = 'R/Theta'
        self.column_headers = ['Independent Variable', 'Channel 1', 'Channel 2']
        self.data_details = None

        self.abscissae = [None, None]
        self.units = [None, None]
        abs_set_delay = [0, 0]

        self.is_recording_transient = False
        self.num_dims = 1
        self.num_scans = [1, 1]
        self.averaging_time = 0
        self.is_averaging_pts = False

        self.scale_factor = [1, 1]
        self.end = [0, 0]
        self.start = [0, 0]
        self.step_count = [1, 1]
        self.scan_range = [0, 0]
        self.current_position = [None, None]
        self.log_spacing = [False, False]
        self.step_pts = [None, None]
        self.is_x_log_scaled = [False, False]
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
        self.toptica.settings = self.settings.toptica
        self.sr_lockin = PrologixAdaptedSRLockin()
        self.sr_lockin.settings = self.settings.lia
        self.zi_lockin = ZiLIA()
        print('Lockins Instantiated...')
        self.cg635 = CG635Instrument()
        self.md2000 = MonoDriver()
        self.cryostat = CryostatInstr()
        self.cryostat.settings = self.settings.cryostat
        self.smb100a = SMB100AInstrument()
        self.md2000.settings = self.settings.md2000
        print(str(self.settings.md2000.com_port))

        # ------------------------------- Initialize GUI Object States -------------------------------------------------

        # self.addToolBar(NavigationToolbar2QT(self.ui.PlotWidget.canvas, self), )
        self.ui.log_spacing_checkbox.setChecked(False)
        self.ui.log_spacing_checkbox_dim2.setChecked(False)
        self.ui.num_scans_dim2_spbx.setValue(1)
        self.ui.num_steps_spbx_dim2.setValue(1)
        self.ui.averaging_time_spbx.setDisabled(True)
        self.ui.scatter_pt_size_cbx.setCurrentIndex(2)

        self.sweep_start_spbxs[0].setEnabled(False)
        self.sweep_start_spbxs[1].setEnabled(False)
        self.sweep_end_spbxs[0].setEnabled(False)
        self.sweep_end_spbxs[1].setEnabled(False)

        # Disable while under construction:
        self.ui.is_recording_transient_chkbx.setEnabled(False)
        self.ui.average_each_point_checkbox.setEnabled(False)
        # ------------------------------------ Run any initialization Functions ----------------------------------------
        self.set_icons()
        self.connect_signals_and_slots()
        self.calc_steps_from_num()
        self.set_1d_plot_properties()
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
        if self.settings.ui.cryostat_checkbox.isChecked():
            self.connect_cryostat()
        if self.settings.ui.smb100a_checkbox.isChecked():
            self.connect_smb100a()

    def connect_cryostat(self):
        """If connection is "actively refused" - likely the IP address or port number is incorrect."""
        print('Setting up Cryostat...')
        did_comms_fail = self.cryostat.start_comms(cryostation_ip='169.254.252.134', cryostation_port=7773)

        if did_comms_fail is True:
            self.cryostat.settings.connected = False
            self.settings.instrument_status_changed('cryostat', 2)
        elif did_comms_fail is False:
            self.cryostat.settings.connected = True
            self.settings.instrument_status_changed('cryostat', 1)

            self.cryostat.check_instrument()

    def connect_lockin(self):
        print('Setting up Lock-in...')
        print(self.settings.lockin_model)
        self.settings.prologix_com_port = self.settings.ui.prologix_com_port_cmb.currentText()
        if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
            # self.sr_lockin = PrologixAdaptedSRLockin()
            if self.settings.lockin_model == 'SR844':
                self.settings.lia.gpib_address = self.settings.ui.sr844_gpib_address_spbx.value()
            else:
                self.settings.lia.gpib_address = self.settings.ui.sr830_gpib_address_spbx.value()

            did_comms_fail = self.sr_lockin.start_comms(self.settings.prologix_com_port,
                                                     gpib_address=self.settings.lia.gpib_address,
                                                     model=self.settings.lockin_model)
            print('Comms_failed? ' + str(did_comms_fail))
        elif self.settings.lockin_model == 'UHFLI':
            print('UHFLI chosen')

            did_comms_fail = self.zi_lockin.start_comms(device_id='dev2025')
        else:
            raise ValueError('Invalid Lock-in Model Selected')

        if self.settings.lockin_model == 'SR844':
            if did_comms_fail is True:
                self.settings.ui.status_ind_sr844.setText(self.label_strings.red_led_str)
            elif did_comms_fail is False:
                self.settings.ui.sr844_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr844.setText(self.label_strings.grn_led_str)
        elif self.settings.lockin_model == 'SR830':
            if did_comms_fail is True:
                self.settings.ui.status_ind_sr830.setText(self.label_strings.red_led_str)
            elif did_comms_fail is False:
                self.settings.ui.sr830_checkbox.setChecked(True)
                self.settings.ui.status_ind_sr830.setText(self.label_strings.grn_led_str)
        elif self.settings.lockin_model == 'UHFLI':
            if did_comms_fail is True:
                self.settings.ui.status_ind_uhfli.setText(self.label_strings.red_led_str)

                self.zi_lockin.settings = self.settings.lia  # This needs to be changed so that settings.uhfli contains t
                self.zi_lockin.update_all()
                self.zi_lockin_delay = self.settings.settling_delay_factor * self.zi_lockin.settings.time_constant_value
                self.settings.ui.is_record_phase.setChecked(False)
                self.settings.ui.is_record_phase.setDisabled(True)
            elif did_comms_fail is False:
                self.settings.ui.uhfli_checkbox.setChecked(True)
                self.settings.ui.status_ind_uhfli.setText(self.label_strings.grn_led_str)

                self.zi_lockin.settings = self.settings.uhfli  # This needs to be changed so that settings.uhfli contains t
                self.zi_lockin.update_all()
                self.zi_lockin_delay = self.settings.settling_delay_factor * self.settings.uhfli.time_constant_value
                self.settings.ui.is_record_phase.setDisabled(False)
                # self.settings.init_lockin_tab()
        else:
            raise ValueError('Invalid Lock-in Model Selected')


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

    def connect_smb100a(self):
        print('------------------------------------- CONNECTING SMB100A ----------------------------------------------')
        did_comms_fail = self.smb100a.start_comms()
        print('SMB100A Comms Failed? ' + str(did_comms_fail))

        if did_comms_fail is True:
            self.smb100a_connected = False
            self.settings.instrument_status_changed('smb100a', 2)
        else:
            self.smb100a_connected = True
            self.settings.instrument_status_changed('smb100a', 1)
            self.smb100a.get_current_settings()

    # -------------------------------------- MAIN EXPERIMENT FUNCTIONS -------------------------------------------------

    @helpers.measure_time
    @QtCore.pyqtSlot()
    def start_experiment(self):
        # TODO: Save notes and details to file before the worker
        if self.sr_lockin.connected or self.zi_lockin.connected:
            self.experiment_in_progress = True
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
            # if self.settings.lia.outputs == 0:  # 0 is R/Theta
            #     self.output_name[0] = 'R (V)'
            #     self.output_name[1] = 'Theta (Degrees)'
            # elif self.settings.lia.outputs == 1:
            #     self.output_name[0] = 'X (V)'
            #     self.output_name[1] = 'Y (V)'
            # elif self.settings.lia.outputs == 2:
            #     self.output_name[0] = 'Aux1 (V)'
            #     self.output_name[1] = 'Unknown'
            # else:
            #     self.output_name[0] = 'Channel 1 Display'
            #     self.output_name[1] = 'Channel 2 Display'
            print('Lockin time Constant: ' + str(self.settings.lia.time_constant_value))
            print('settling delay factor: ' + str(self.settings.settling_delay_factor))
            self.settings.settling_delay_factor = self.settings.ui.lockin_delay_scale_spbx.value()
            print('settling delay factor: ' + str(self.settings.settling_delay_factor))
            if self.settings.lia.model == 'SR844' or self.settings.lia.model == 'SR830':
                self.lockin_delay = self.settings.settling_delay_factor * self.settings.lia.time_constant_value
            elif self.settings.lia.model == 'UHFLI':
                # self.sr_lockin_delay = 0.1
                self.lockin_delay = self.settings.settling_delay_factor * self.settings.time_constant_value
            print('lockin_delay: ' + str(self.lockin_delay))

            if self.ui.is_recording_transient_chkbx.isChecked():
                self.is_recording_transient = True
                self.transient_duration = self.ui.time_trace_window_length_spbx.value()
            else:
                self.is_recording_transient = False

            # self.prepare_for_collection()

            if self.abscissae[1] is None or self.abscissae[1] == 0:
                self.num_dims = 1
                self.data_type = '1D'
                self.get_abs_name(0)
            elif 0 < self.abscissae[1] < 6:
                self.num_dims = 2
                self.data_type = '2D'

                self.ave_data_ch1_df = []
                self.ave_data_ch2_df = []
                self.get_abs_name(0)
                self.get_abs_name(1)
            else:
                raise ValueError('Invalid Value for abscissa[1] (second independent variable)')

            if (self.abscissae[0] == 4 or self.abscissae[1] == 4) and self.smb100a_connected:
                print('Turning on RF Source Output')
                self.smb100a.run()

            self.num_scans[0] = self.ui.num_scans_spbx.value()
            self.num_scans[1] = self.ui.num_scans_dim2_spbx.value()

            # # Create a data storage structure
            # self.data_stored = []

            # self.all_scans_dim1 = []
            self.averaging_time = self.ui.averaging_time_spbx.value()

            # Before UHFLI
            # self.column_headers = [self.abscissa_name[0], self.output_name[0], self.output_name[1]]

            # Make a setting so that the user doesn't have to record ALL of these:

            # self.column_headers = [self.abscissa_name[0], 'X (Vrms)', 'Y (Vrms)', 'R (Vrms)', 'Theta (deg)',
            #                        'Aux In 1', 'Aux In 2', 'Frequency', 'Phase']

            self.column_headers = [self.abscissa_name[0]]
            if self.settings.ui.is_record_x.isChecked():
                self.column_headers.append('X (Vrms)')
            if self.settings.ui.is_record_y.isChecked():
                self.column_headers.append('Y (Vrms)')
            if self.settings.ui.is_record_r.isChecked():
                self.column_headers.append('R (Vrms)')
            if self.settings.ui.is_record_theta.isChecked():
                self.column_headers.append('Theta (deg)')
            if self.settings.ui.is_record_auxin1.isChecked():
                self.column_headers.append('Aux In 1')
            if self.settings.ui.is_record_auxin2.isChecked():
                self.column_headers.append('Aux In 2')
            if self.settings.ui.is_record_freq.isChecked():
                self.column_headers.append('Frequency')
            if self.settings.ui.is_record_phase.isChecked():
                self.column_headers.append('Phase')

            self.ui.upper_plot_obs_cmbx.addItems(self.column_headers[1:6])
            self.ui.upper_plot_obs_cmbx.setCurrentIndex(0)
            self.ui.lower_plot_obs_cmbx.addItems(self.column_headers[1:6])
            self.ui.lower_plot_obs_cmbx.setCurrentIndex(1)

            # self.ave_data_df = pd.DataFrame(columns=self.column_headers)

            self.actual_x_values = np.empty((self.step_count[0], 1))
            self.actual_x_values[:] = np.nan
            self.actual_x_values = self.actual_x_values.flatten()

            # self.data_details = PlottedData(dims=self.num_dims, output_names=self.output_name, num_scans=self.num_scans,
            #                                 notes=notes, instr_settings=None)

            self.data_details = PlottedData(dims=self.num_dims, num_scans=self.num_scans,
                                            notes=notes, instr_settings=None)

            self.set_1d_plot_properties()

            self.clear_plots()

            if not self.is_debug_mode:
                data_collection_worker = helpers.Worker(self.collect_data, filename, filetype)
                self.thread_pool.start(data_collection_worker)
            else:
                self.collect_data(filename, filetype)
        else:
            self.general_error_signal.emit({'Title': ' - Warning - ',
                                            'Text': ' Experiment Aborted',
                                            'Informative Text': 'One or more instruments not set up',
                                            'Details': None})


    @helpers.measure_time
    def collect_data(self, filename=None, filetype=None):
        #TODO: Incorporate 2D Data
        # 1. SAMPLING Rate for the SR844 is currently used no matter which lock-in you choose (bad)
        print('---------------------------------- BEGINNING MAIN EXPERIMENT LOOP -------------------------------------')
        # Create a data storage structure
        self.stored_data = StoredData()

        # At the beginning of each scan, add that scan to the stored data
        dim2_scan_num = 0
        while dim2_scan_num < self.num_scans[1]:
            # Repeat entire 2D scan dim2_scan_num times

            if self.num_dims == 2:
                pass

            dim2_step_num = 0
            while dim2_step_num < self.step_count[1]:
                # All stopping points in the second dimension (abscissa[1])
                if self.abort_scan is True:
                    return
                while self.pause_scan is True:
                    time.sleep(0.05)

                # These storage variables must be refreshed when they are to be reused for the 2nd dimensional scan
                if not self.is_recording_transient:
                    # self.current_scan = pd.DataFrame(columns=self.column_headers)

                    self.ave_data_df = pd.DataFrame(columns=self.column_headers)

                else:
                    self.status_message_signal.emit('Transient Recording Under Construction...')

                    # Before UHFLI:
                    # num_times = int((self.transient_duration * self.settings.lia.sampling_rate))
                    # period = 1 / self.settings.lia.sampling_rate
                    # self.ch1_scans_df = pd.DataFrame(
                    #     # columns=[self.abscissa_name[0]] + (np.linspace(0, self.transient_duration, num_times)).tolist())
                    #     columns=[self.abscissa_name[0]] + (np.arange(0, num_times)).tolist())
                    # self.ch2_scans_df = pd.DataFrame(
                    #     # columns=[self.abscissa_name[0]] + (np.linspace(0, self.transient_duration, num_times)).tolist())
                    #     columns=[self.abscissa_name[0]] + (np.arange(0, num_times)).tolist())
                    # self.ave_data_df = pd.DataFrame(columns=self.column_headers)

                if self.num_dims == 2:
                    self.status_message_signal.emit('2D Experiments Under Construction')
                    # Before UHFLI
                    next_step_dim2 = self.step_pts[1][dim2_step_num]
                    print('Next Step (dim2) is: ' + str(next_step_dim2) + '(' + str(dim2_step_num + 1) + ' of ' + str(self.step_count[1]) + ')')
                    self.current_position[1] = float(self.set_abscissa(which_abscissa=1, next_step=next_step_dim2))
                    # self.axis_1.set_title(str(self.current_position[1]) + self.units[1])

                else:
                    self.current_position[1] = None

                scan_num = 0
                while scan_num < self.num_scans[0]:
                    self.ready_for_new_scan(which_abscissa=0)
                    self.current_scan = pd.DataFrame(columns=self.column_headers)
                    # Before each scan, add the empty scan data to the stored data
                    self.stored_data.add_scan(self.current_scan, dim2_scan_num, dim2_step_num)


                    # self.all_scans_dim1.append(self.current_scan)
                    print('------------------------------------ SCAN %d -----------------------------------------' % scan_num)
                    self.change_plot_title_signal.emit('Scan %d' % (scan_num + 1))
                    step_num = 0
                    while step_num < self.step_count[0]:  # INNERMOST LOOP
                        # This loops over all the points for abscissa_1
                        if self.abort_scan is True:
                            return
                        while self.pause_scan is True:
                            time.sleep(0.05)

                        next_step = self.step_pts[0][step_num]
                        print('Next Step (dim1 ) is: ' + str(next_step) + '(' + str(step_num + 1) + ' of ' + str(self.step_count[0]) + ')')

                        cur_pos = self.set_abscissa(which_abscissa=0, next_step=next_step);

                        # At the moment, set_abscissa is typically the source of self.abort_scan=True
                        if cur_pos is None and self.abort_scan is True:
                            return

                        self.current_position[0] = float(cur_pos)

                        if not self.is_recording_transient:
                            self.current_sample = self.get_lockin_results()

                        elif self.is_recording_transient:   # Each output is a full time trace now
                            self.status_message_signal.emit('Transient Measurement Under Construction...')

                        self.distribute_results(step_num, scan_num, dim2_step_num, dim2_scan_num)

                        if not self.is_debug_mode:
                            self.results_are_in_signal.emit(step_num, scan_num)     # Lets the UI know it's time to plot results
                        elif self.is_debug_mode:
                            self.plot_results(step_num, scan_num)

                        # Update the stored data container
                        self.stored_data.replace_scan(self.current_scan, dim2_scan_num, dim2_step_num, scan_num)

                        step_num = step_num + 1
                    # Save data after each scan (add scan)
                    # self.stored_data.add_scan(self.current_scan, dim2_scan_num, dim2_step_num)
                    self.save_stuff(filename, filetype, 'scan_num', sc_idx_1d=scan_num, sc_idx_2d=dim2_scan_num,
                                    manual=False)  # 1D scans + ave
                    scan_num = scan_num + 1
                # End of each 2nd Dim Step (i.e. end of each 1st Dim Sweep)
                # self.save_stuff_uhfli(filename, filetype, 'dim2_step_num', sc_idx_1d=scan_num, sc_idx_2d=dim2_scan_num, manual=False)  # Ave of 1D scans
                dim2_step_num = dim2_step_num + 1
            # End of each 2nd Dim Scan
            # self.save_stuff(filename, filetype, 'dim2_scan_num', sc_idx_1d=scan_num, sc_idx_2d=dim2_scan_num, manual=False)    # Save each 2D scan
            dim2_scan_num = dim2_scan_num + 1
        # self.save_stuff(filename, filetype, 'end', sc_idx_1d=scan_num, sc_idx_2d=dim2_scan_num, manual=False) # Ave of 2Dscans(not yet)
        self.abort_scan = False
        self.experiment_in_progress = False
        print('------------------------------------- EXPERIMENT COMPLETED --------------------------------------------')

    @helpers.measure_time
    def set_abscissa(self, which_abscissa, next_step):
        wa = which_abscissa
        if self.abscissae[wa] is None or self.abscissae[wa] == 0:  # Empty Header line
            print('No Abscissa - Step is Point Number')
            actual_pos = next_step
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
            # I think that case 1 is redundant since an error.status should be True until comms are established
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
                                                'Details': ('Error Code: ' + str(self.cryostat.error.code))})
                self.abort_scan = True
                return None
            else:
                self.md2000.go_to_wavelength(destination=next_step, backlash_amount=self.settings.md2000.bl_amt,
                                             backlash_bool=self.settings.md2000.bl_bool)
                actual_pos = self.md2000.settings.cur_wl

        elif self.abscissae[wa] == 3:  # Static Magnetic Field
            print('------------------------ SETTING MAGNETIC FIELD -------------------------')
            if self.cryostat.error.status:
                print('Cryostat had a pre-existing error')
                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                'Text': ' Experiment Aborted',
                                                'Informative Text': 'Cryostat Error Found',
                                                'Details': ('Error Code: ' + str(self.cryostat.error.code))})
                self.abort_scan = True
                return None
            else:
                self.cryostat.set_field(target_field=next_step)
                if self.cryostat.error.status:
                    self.general_error_signal.emit({'Title': ' - Warning - ',
                                                    'Text': ' Experiment Aborted',
                                                    'Informative Text': 'Error Occurred while setting field',
                                                    'Details': ('Error Code: ' + str(self.cryostat.error.code))})
                    self.abort_scan = True
                actual_pos = self.cryostat.settings.current_field
                print('Waiting magnet_settling_time = ' + str(self.cryostat.settings.magnet_settling_time) + ' seconds')
                time.sleep(self.cryostat.settings.magnet_settling_time)

        elif self.abscissae[wa] == 4:  # RF Carrier Frequency
            print('------------------------ SETTING RF FREQUENCY -------------------------')
            if self.smb100a.error.status:
                print('SMB100A had a pre-existing error')
                self.general_error_signal.emit({'Title': ' - Warning - ',
                                                'Text': ' Experiment Aborted',
                                                'Informative Text': 'SMB100A Error Found',
                                                'Details': ('Error Code: ' + str(self.smb100a.error.code))})
                self.abort_scan = True
                return None
            else:
                units = self.units_cbxes[wa].currentText()

                self.smb100a.set_freq(freq_to_set=next_step, units=units)
                if self.smb100a.error.status:
                    self.general_error_signal.emit({'Title': ' - Warning - ',
                                                    'Text': ' Experiment Aborted',
                                                    'Informative Text': 'Error Occurred while setting field',
                                                    'Details': ('Error Code: ' + str(self.smb100a.error.code))})
                    self.abort_scan = True
                if units == 'Hz':
                    scale_fac = 1
                elif units == 'kHz':
                    scale_fac = 1E3
                elif units == 'MHz':
                    scale_fac = 1E6
                elif units == 'GHz':
                    scale_fac = 1E9

                actual_pos = self.smb100a.get_freq() / scale_fac

        elif self.abscissae[wa] == 5:  # RF Modulation Frequency
            print('This case has not been coded yet')
        elif self.abscissae[wa] == 6:  # Lock-in Internal Ref Frequency
            print('Attempting to set internal reference frequency...')
            if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
                if self.sr_lockin.error.status:
                    print('Lock-in had a pre-existing error')
                    self.general_error_signal.emit({'Title': ' - Warning - ',
                                                    'Text': ' Experiment Aborted',
                                                    'Informative Text': 'Cryostat Error Found',
                                                    'Details': ('Error Code: ' + str(self.sr_lockin.error.code))})
                    self.abort_scan = True
                    return None
                else:
                    self.sr_lockin.update_freq(target_freq=next_step)
                    actual_pos = self.sr_lockin.settings.frequency
                    print('Actual pos: ' + str(actual_pos))
            elif self.settings.lockin_model == 'UHFLI':
                print('UHFLI Not set up for internal reference sweeps')

        else:
            print('there are this many possible abscissae?')

        return actual_pos

    @helpers.measure_time
    def ready_for_new_scan(self, which_abscissa=0):
        print('Preparing for next scan')
        wa = which_abscissa
        if self.abscissae[wa] == 3:     # Magnet is what's being set
            if self.settings.cryostat.is_zero_magnet_between_scans:
                self.status_message_signal.emit('Re-Zeroing Magnet...')
                self.cryostat.zero_magnet()
                for ii in range(0, 63):     # I measured it once to take 61 seconds
                    time.sleep(1)
                    self.status_message_signal.emit('Zeroing Magnet... %s seconds remaining' % (62 - ii))
                self.status_message_signal.emit('Magnet Zeroed')
            else:
                self.status_message_signal.emit('Pausing for Magnet Settling...')
                time.sleep(self.settings.cryostat.magnet_prescan_settling_time)

        else:
            print('No instruments have pre-scan requirements except the magnet yet.')


    @helpers.measure_time
    def get_lockin_results(self):
        print('Checking for lock-in issues...')
        # As in overloads, phase locking to reference, etc.

        if self.settings.lockin_model == 'SR830' or self.settings.lockin_model == 'SR844':
            self.sr_lockin.open_comms()  # Open also sets the correct GPIB address
            self.sr_lockin.comms.write('*CLS\n')
            self.sr_lockin.clear_buffers()

            lia_status = self.sr_lockin.check_status()
            kk = 0
            # It may take some time for the lockin internal oscillator  to lock to the reference freq
            # Not yet sure how to check if PLL is locked with UHFLI
            while not lia_status == 0 and kk < 200:
                lia_status = self.sr_lockin.check_status()
                if lia_status == -1:  # Comm failure
                    return
                # print('lia error' + str(lia_error))
                # print('loop iteration: ' + str(kk))
                time.sleep(0.001)
                kk = kk + 1

            if not lia_status == 0:  # -1 cases (comm errors) should be removed by now
                self.pause_scan = True
                # The following should be optimized
                self.sr_lockin_status_warning_signal.emit(str(lia_status))

        print('Pausing for Lock-in settling...')
        print('lockin_delay: ' + str(self.lockin_delay))
        time.sleep(self.lockin_delay)  # Wait for the lock-in output to settle

        # Perform a "global synchronization"
        # self.sr_lockin.daq.sync()

        if self.settings.ui.scan_auto_sens_checkbox.isChecked():
            print('Optimizing Lock-in Sensitivity...')
            if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
                self.sr_lockin.auto_sens()
            elif self.settings.lockin_model == 'UHFLI':
                self.zi_lockin.auto_sens()

        print('Collecting Data....')

        if not self.is_averaging_pts and not self.is_recording_transient:  # Single snapshot measurement at each point
            if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
                sample = self.sr_lockin.collect_sample()
            elif self.settings.lockin_model == 'UHFLI':
                sample = self.zi_lockin.collect_sample()

        elif self.is_averaging_pts and not self.is_recording_transient:  # If averaging lockin results
            print('Averaging Results under construction')
            # if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
            #     ch1_data, ch2_data = self.sr_lockin.collect_data(self.averaging_time,
            #                                                   self.settings.lia.sampling_rate_idx,
            #                                                   record_both_channels=True)
            #     print('Averaging New Data...')
            #     ch1 = np.average(ch1_data)
            #     ch2 = np.average(ch2_data)
            # elif self.settings.lockin_model == 'UHFLI':
            #     print('Averaging Results not set up on UHFLI')

        elif self.is_recording_transient:
            print('Transient Measurements under construction')
            # if self.settings.lockin_model == 'SR844' or self.settings.lockin_model == 'SR830':
            #     ch1, ch2 = self.sr_lockin.collect_data(self.transient_duration, self.settings.lia.sampling_rate_idx,
            #                                         record_both_channels=True)
            # elif self.settings.lockin_model == 'UHFLI':
            #     print('Transient measurements not set up on UHFLI')

        return sample


    @helpers.measure_time
    def distribute_results(self, step_num, scan_num, dim2_step_num, dim2_scan_num):
        # x = self.sample["x"]
        self.actual_x_values[step_num] = self.current_position[0]

        self.current_scan.loc[step_num, self.abscissa_name[0]] = self.current_position[0]
        self.ave_data_df.loc[step_num, self.column_headers[0]] = self.current_position[0]

        if 'X (Vrms)' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'X (Vrms)'] = self.current_sample["x"]
        if 'Y (Vrms)' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Y (Vrms)'] = self.current_sample["y"]
        if 'R (Vrms)' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'R (Vrms)'] = self.current_sample["R"]
        if 'Theta (deg)' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Theta (deg)'] = self.current_sample["theta"]
        if 'Aux In 1' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Aux In 1'] = self.current_sample["auxin0"]
        if 'Aux In 2' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Aux In 2'] = self.current_sample["auxin1"]
        if 'Frequency' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Frequency'] = self.current_sample["frequency"]
        if 'Phase' in self.current_scan.columns:
            self.current_scan.loc[step_num, 'Phase'] = self.current_sample["phase"]

        # self.all_scans_dim1[scan_num] = self.current_scan
        if scan_num == 0:
            # self.actual_x_values[step_num] = self.current_position[0]
            #
            # self.current_scan.loc[step_num, self.abscissa_name[0]] = self.current_position[0]
            # self.ave_data_df.loc[step_num, self.column_headers[0]] = self.current_position[0]
            # Before UHFLI:
            # self.ch1_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
            # self.ch2_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
            # self.ave_data_df.loc[ii, self.column_headers[0]] = self.current_position[0]
            if self.num_dims == 2:
                pass
                # Before UHFLI:
                # self.ave_data_ch1_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]
                # self.ave_data_ch2_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]
        num_cols = len(self.column_headers)
        for ii in range(0, num_cols):
            for jj in range(0, step_num+1):
                cur_sum = 0
                for kk in range(0, len(self.stored_data.scans_2d[dim2_scan_num][dim2_step_num])):
                    cur_sum = cur_sum + self.stored_data.scans_2d[dim2_scan_num][dim2_step_num][kk].loc[jj, self.column_headers[ii]]
                self.ave_data_df.loc[jj, self.column_headers[ii]] = cur_sum / (scan_num + 1)

        # Before UHFLI:
        # ch1_df_mean = self.ch1_scans_df.iloc[:, 1:].mean(axis=1)  # Average all columns except the first
        # ch2_df_mean = self.ch2_scans_df.iloc[:, 1:].mean(axis=1)

        # ch1_df_mean = self.ch1_scans_df.iloc[:, 1:].mean(axis=1)  # Average all columns except the first
        # ch2_df_mean = self.ch2_scans_df.iloc[:, 1:].mean(axis=1)

        # self.ave_data_df.loc[:, self.output_name[0]] = ch1_df_mean
        # self.ave_data_df.loc[:, self.output_name[1]] = ch2_df_mean

        if self.num_dims == 2:
            pass
            # Before UHFLI:
            # self.ave_data_ch1_df[mm].iloc[:, ll+1] = ch1_df_mean
            # self.ave_data_ch2_df[mm].iloc[:, ll+1] = ch2_df_mean

        # print('self.ave_data_df:')
        # print(self.ave_data_df)

    # @helpers.measure_time
    # def distribute_results(self, ii, jj, ll, mm):
    #     if jj == 0:
    #         self.actual_x_values[ii] = self.current_position[0]
    #         self.ch1_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
    #         self.ch2_scans_df.loc[ii, self.abscissa_name[0]] = self.current_position[0]
    #         self.ave_data_df.loc[ii, self.column_headers[0]] = self.current_position[0]
    #         if self.num_dims == 2:
    #             self.ave_data_ch1_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]
    #             self.ave_data_ch2_df[mm].loc[ii, self.column_headers_2d] = self.current_position[0]
    #
    #     ch1_df_mean = self.ch1_scans_df.iloc[:, 1:].mean(axis=1)  # Average all columns except the first
    #     ch2_df_mean = self.ch2_scans_df.iloc[:, 1:].mean(axis=1)
    #
    #     self.ave_data_df.loc[:, self.output_name[0]] = ch1_df_mean
    #     self.ave_data_df.loc[:, self.output_name[1]] = ch2_df_mean
    #
    #     if self.num_dims == 2:
    #         # self.ave_data_ch1_df[mm].loc[:, self.current_position[1]] = ch1_df_mean
    #         # self.ave_data_ch2_df[mm].loc[:, self.current_position[1]] = ch2_df_mean
    #
    #         self.ave_data_ch1_df[mm].iloc[:, ll + 1] = ch1_df_mean
    #         self.ave_data_ch2_df[mm].iloc[:, ll + 1] = ch2_df_mean
    #
    #     print('self.ave_data_df:')
    #     print(self.ave_data_df)

    def clear_plots(self):
        if self.plot1 is not None:
            self.ui.PlotWidget.removeItem(self.plot1)
            self.plot1 = None
        if self.plot2 is not None:
            self.ui.PlotWidget2.removeItem(self.plot2)
            self.plot2 = None
        if self.plot3 is not None:
            self.ui.PlotWidget.removeItem(self.plot3)
            self.plot3 = None
        if self.plot4 is not None:
            self.ui.PlotWidget2.removeItem(self.plot4)
            self.plot4 = None

    @helpers.measure_time
    @QtCore.pyqtSlot(int, int)
    def plot_results(self, ii, jj):
        print('inside plot results 2')
        color1 = '#0000FF'  # Blue
        color2 = '#FF0000'  # Red
        if ii == 0:
            print('Cleared Plots')
            self.ui.PlotWidget.clear()
            self.ui.PlotWidget2.clear()
            # self.ui.PlotWidget.update()
            # self.ui.PlotWidget2.update()
        # self.set_1d_plot_properties()
        if not self.is_recording_transient:
            upper_plot_y_axis = self.ui.upper_plot_obs_cmbx.currentText()
            lower_plot_y_axis = self.ui.lower_plot_obs_cmbx.currentText()
            self.ui.PlotWidget.setLabels(left=upper_plot_y_axis)
            self.ui.PlotWidget2.setLabels(left=lower_plot_y_axis)

            cur_scan = self.current_scan.to_numpy(np.float32)
            cur_x = cur_scan[:, 0]

            cur_ch1 = self.current_scan.loc[:, upper_plot_y_axis].to_numpy(np.float32)
            cur_ch2 = self.current_scan.loc[:, lower_plot_y_axis].to_numpy(np.float32)

            ave_ch1 = self.ave_data_df.loc[:, upper_plot_y_axis].to_numpy(np.float32)
            ave_ch2 = self.ave_data_df.loc[:, lower_plot_y_axis].to_numpy(np.float32)

        else:
            pass
            # ch1_scans = self.ch1_scans_df.to_numpy(np.float32)
            # ch2_scans = self.ch2_scans_df.to_numpy(np.float32)
            #
            # print('ch1_scans[0]: ' + str(ch1_scans[ii, 0]))
            # print('ch1_scans[1]: ' + str(ch1_scans[ii, 1]))
            #
            # cur_ch1 = ch1_scans[ii, 1:]
            # cur_ch2 = ch2_scans[ii, 1:]
            # cur_length = len(cur_ch1)
            # actual_dur = cur_length / self.settings.lia.sampling_rate
            # cur_x = np.linspace(0, actual_dur, cur_length)
            # ave_data = self.ave_data_df.to_numpy(np.float32)


        if jj == 0 and ii == 0:
            color_plot1 = '#0000FF'  # Blue
            self.ui.PlotWidget.addLegend()
            self.ui.PlotWidget2.addLegend()

            if self.line_style is None:
                print('If No Line')

                self.plot1 = self.ui.PlotWidget.plot(cur_x, cur_ch1,
                                                pen=None, symbol='o', symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')
                # self.ui.PlotWidget.addLegend()

                self.plot2 = self.ui.PlotWidget2.plot(cur_x, cur_ch1,
                                                 pen=None, symbol='o', symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')
                # self.ui.PlotWidget2.addLegend()
            else:
                print('If Line Plot (else case)')
                # self.ui.PlotWidget.addLegend()
                self.plot1 = self.ui.PlotWidget.plot(cur_x, cur_ch1,
                                        pen=pg.mkPen(color_plot1, width=self.line_width), symbol='o',
                                        symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')

                # self.ui.PlotWidget2.addLegend()
                self.plot2 = self.ui.PlotWidget2.plot(cur_x, cur_ch2,
                                         pen=pg.mkPen(color_plot1, width=self.line_width), symbol='o',
                                         symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')

        elif jj == 0 and ii > 0:
            self.plot1.setData(cur_x, cur_ch1)
            self.plot2.setData(cur_x, cur_ch2)

        elif jj > 0 and ii == 0:
            print('Second Scan Plotting')
            print('attempting to remove lines')
            self.ui.PlotWidget.removeItem(self.plot1)
            self.ui.PlotWidget2.removeItem(self.plot2)
            # self.plot1.setData(cur_x, cur_ch1)
            # self.plot2.setData(cur_x, cur_ch2)
            color_plot1 = '#AFAFFF'

            if self.line_style is None:
                print('No Line style - second Scan')
                self.plot1 = self.ui.PlotWidget.plot(cur_x, cur_ch1,
                                        pen=None, symbol='o', symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')

                self.plot2 = self.ui.PlotWidget2.plot(cur_x, cur_ch2,
                                         pen=None, symbol='o', symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')

            else:
                print('Lines - second Scan')
                self.plot1 = self.ui.PlotWidget.plot(cur_x, cur_ch1,
                                        pen=pg.mkPen(color_plot1, width=1), symbol='o',
                                        symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')
                self.plot2 = self.ui.PlotWidget2.plot(cur_x, cur_ch2,
                                         pen=pg.mkPen(color_plot1, width=1), symbol='o',
                                         symbolPen=color_plot1, symbolSize=self.marker_size, name='Current Scan')

            if self.line_style is None:
                print('No lines - Average')
                self.plot3 = self.ui.PlotWidget.plot(self.actual_x_values, ave_ch1,
                                        pen=None, symbol='o', symbolPen='#FF0000', symbolSize=self.marker_size, name='Average')
                # self.ui.PlotWidget.addLegend()
                self.plot4 = self.ui.PlotWidget2.plot(self.actual_x_values, ave_ch2,
                                         pen=None, symbol='o', symbolPen='#FF0000', symbolSize=self.marker_size, name='Average')
                # self.ui.PlotWidget2.addLegend()
            else:
                print('Lines - Average')
                self.plot3 = self.ui.PlotWidget.plot(self.actual_x_values, ave_ch1,
                                        pen=pg.mkPen('#FF0000', width=1), symbol='o',
                                        symbolPen='#FF0000', symbolSize=self.marker_size, name='Average')
                # self.ui.PlotWidget.addLegend()
                self.plot4 = self.ui.PlotWidget2.plot(self.actual_x_values, ave_ch2,
                                         pen=pg.mkPen('#FF0000', width=1), symbol='o',
                                         symbolPen='#FF0000', symbolSize=self.marker_size, name='Average')
                # self.ui.PlotWidget2.addLegend()
        elif jj > 0 and ii > 0:
            print('Second Scan Plotting')
            self.plot1.setData(cur_x, cur_ch1)
            self.plot2.setData(cur_x, cur_ch2)

            self.plot3.setData(self.actual_x_values, ave_ch1)
            self.plot4.setData(self.actual_x_values, ave_ch2)
        return

    # @helpers.measure_time
    # def save_stuff(self, filename=None, filetype=None, loop_index=None, sc_idx_1d=0, sc_idx_2d=0, manual=False):
    #     if self.data_details is None:
    #         self.status_message_signal.emit('No stored data to save')
    #         return
    #
    #     obs1, obs2 = self.data_details.output_names[:]      # as in observable 1 and 2 (R/Theta or X/Y)
    #     # If the user requested to save AFTER collecting the data, then a directory will need to be created
    #     if manual is True:
    #         filename, filetype = self.save_file_dialog()
    #
    #         if filename is not None:
    #             os.mkdir(filename)
    #             filename = filename + '\\'
    #         else:
    #             return
    #
    #     # If the user didn't cancel saving
    #     if filename is not None:
    #         if loop_index == 'jj' or manual is True:
    #             # After each 1D scan, save that scan
    #             if self.data_details.num_dims == 1:
    #                 # Overwrite file to create growing data matrix (number of points (rows) x number of scans (cols)
    #                 fname = filename + 'Scans - '
    #                 self.save_data(data_frame=self.ch1_scans_df, filename=(fname + obs1), filetype=filetype)
    #                 self.save_data(data_frame=self.ch2_scans_df, filename=(fname + obs2), filetype=filetype)
    #                 if sc_idx_1d > 0 or (manual is True and self.data_details.num_scans[0] > 0):
    #                     # If more than one scan has occurred, save the average. Overwrite that file after add'l scans
    #                     self.save_data(data_frame=self.ave_data_df, filename=(filename + 'Ave Data'), filetype=filetype)
    #                     self.status_message_signal.emit('Updated and Saved Average Data........')
    #             elif self.data_details.num_dims == 2 and manual is False:
    #                 # Overwrite file to create growing matrix (number of 1st-D pts (rows) x number of 1st-D scans (cols)
    #                 # Each 2nd-D pt gets its own file with a distinct name.
    #                 fname = (filename + str(self.current_position[1]) + self.units[1] + ', Scans - ')
    #                 self.save_data(data_frame=self.ch1_scans_df, filetype=filetype, filename=fname + obs1)
    #                 self.save_data(data_frame=self.ch2_scans_df, filetype=filetype, filename=fname + obs2)
    #             self.status_message_signal.emit('Saved Scan Data.......')
    #
    #         if self.data_details.num_dims == 2 and (loop_index == 'll' or manual is True):
    #             # Save each 2D scan (each one is a matrix)
    #             if manual is False:
    #                 fn = filename + '2D Scan ' + str(sc_idx_2d) + ' - '
    #                 self.save_data(data_frame=self.ave_data_ch1_df[sc_idx_2d], filetype=filetype, filename=(fn + obs1))
    #                 self.save_data(data_frame=self.ave_data_ch2_df[sc_idx_2d], filetype=filetype, filename=(fn + obs2))
    #                 self.status_message_signal.emit('Saved 2D Scan Data........')
    #                 # Ideally we would add an if statement to average together multiple 2D scans. But idk how yet
    #             elif manual is True:
    #                 fn = filename + '2D Scan ' + str(sc_idx_2d) + ' - '
    #                 for scan in range(0, len(self.ave_data_ch1_df)):
    #                     self.save_data(data_frame=self.ave_data_ch1_df[scan], filetype=filetype, filename=(fn + obs1))
    #                     self.save_data(data_frame=self.ave_data_ch2_df[scan], filetype=filetype, filename=(fn + obs2))
    #                 self.status_message_signal.emit('Saved 2D Scan Data........')

    @helpers.measure_time
    def save_stuff(self, filename=None, filetype=None, loop_index=None, sc_idx_1d=0, sc_idx_2d=0, manual=False):
        if self.data_details is None:
            self.status_message_signal.emit('No stored data to save')
            return

        # obs1, obs2 = self.data_details.output_names[:]  # as in observable 1 and 2 (R/Theta or X/Y)
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
            if loop_index == 'scan_num' or manual is True:
                # After each 1D scan, save that scan
                if self.data_details.num_dims == 1:
                    # Create a new file for each scan
                    fname = filename + 'Scan ' + str(sc_idx_1d)
                    self.save_data(data_frame=self.current_scan, filename=fname, filetype=filetype)

                    if sc_idx_1d > 0 or (manual is True and self.data_details.num_scans[0] > 0):
                        # If more than one scan has occurred, save the average. Overwrite that file after add'l scans
                        self.save_data(data_frame=self.ave_data_df, filename=(filename + 'Ave Data'), filetype=filetype)
                        self.status_message_signal.emit('Updated and Saved Average Data........')
                elif self.data_details.num_dims == 2 and manual is False:
                    # Create a folder for each 2D scan
                    fname_2d = filename + '\\2D Scan ' + str(sc_idx_2d)
                    if not os.path.isdir(fname_2d):
                        os.mkdir(fname_2d)
                    filename = fname_2d + '\\'

                    # Overwrite file to create growing matrix (number of 1st-D pts (rows) x number of 1st-D scans (cols)
                    # Each 2nd-D pt gets its own file with a distinct name.
                    print('2D Data Under Construction')
                    fname = (filename + str(self.current_position[1]) + self.units[1] + ', Sweep ' + str(sc_idx_1d))
                    # self.save_data(data_frame=self.ch1_scans_df, filetype=filetype, filename=fname + obs1)
                    # self.save_data(data_frame=self.ch2_scans_df, filetype=filetype, filename=fname + obs2)
                    self.save_data(data_frame=self.current_scan, filename=fname, filetype=filetype)

                    if sc_idx_1d > 0 or (manual is True and self.data_details.num_scans[0] > 0):
                        dir_name_ave = filename + '\\Average'
                        if not os.path.isdir(dir_name_ave):
                            os.mkdir(dir_name_ave)
                        # If more than one scan has occurred, save the average. Overwrite that file after add'l scans
                        self.save_data(data_frame=self.ave_data_df, filename=(dir_name_ave + '\\' + str(self.current_position[1]) + self.units[1]), filetype=filetype)
                        self.status_message_signal.emit('Updated and Saved Average Data........')
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

    def load_file_dialog(self):
        print('inside save file dialog')
        # tc = self.thread_pool.activeThreadCount()
        # print('Active threads: ' + str(tc))
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getOpenFileName(self, "Load File:", r'C:\Users\padmr\Desktop\Data', options=options)

        return file_name


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

    # @QtCore.pyqtSlot()
    # def start_time_trace(self):
    #     print('Starting Time Trace...')
    #     # I'll need to know how long the measurement should be
    #     # And the sampling rate. Sampling rate is already set
    #     window_length = self.ui.time_trace_window_length_spbx.value()
    #     s_rat = self.settings.lia.sampling_rate_idx


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
    def sr_lockin_status_warning_window(self, error_message):
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


    @QtCore.pyqtSlot()
    def open_help_window(self):
        self.help_window = HelpWindowForm()
        self.help_window.show()

    @QtCore.pyqtSlot()
    def open_settings_window(self):
        self.settings.show()
        self.settings.setWindowState(self.settings.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.settings.activateWindow()

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

    @QtCore.pyqtSlot()
    def cryostat_write_manual_cmd(self):
        cmd_to_write = self.settings.ui.cryostat_write_cmd_lnedt.text()
        print(cmd_to_write)
        response = self.cryostat.comms.send_command_get_response(cmd_to_write)
        self.settings.ui.cryostat_response_lnedt.setText(response)

    @QtCore.pyqtSlot()
    def smb100a_write_manual_cmd(self):
        cmd_to_write = self.settings.ui.smb100a_write_cmd_lnedt.text()
        print(cmd_to_write)
        response = self.smb100a.write_string(cmd_to_write, read=True, manual=True)
        self.settings.ui.smb100a_response_textedit.setText(response)

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

    @helpers.measure_time
    def set_1d_plot_properties(self):
        print('inside set_1d_plot_properties2')
        print('self.is_x_log_scaled = ' + str(self.is_x_log_scaled[0]))
        # self.ui.PlotWidget.setLogMode(x=self.is_x_log_scaled[0])
        # self.ui.PlotWidget2.setLogMode(x=self.is_x_log_scaled[0])

        # self.ui.PlotWidget.setLabels(bottom=self.abscissa_name[0], left=self.output_name[0])
        # self.ui.PlotWidget2.setLabels(bottom=self.abscissa_name[0], left=self.output_name[1])

        self.ui.PlotWidget.setLabels(bottom=self.abscissa_name[0])
        self.ui.PlotWidget2.setLabels(bottom=self.abscissa_name[0])
        # self.axis_1.set_xscale(self.is_x_log_scaled[0])
        print('set xscale')
        if self.step_count[0] != 1:
            print('self.step_count was not 1')
            if self.start[0] < self.end[0]:
                print('start < end')
                if not self.is_x_log_scaled[0]:
                    print('linear case')
                    self.ui.PlotWidget.setXRange((self.start[0] - 0.05 * self.scan_range[0]),
                                                 (self.end[0] + 0.05 * self.scan_range[0]),  padding=0.05)
                    self.ui.PlotWidget2.setXRange((self.start[0] - 0.05 * self.scan_range[0]),
                                                  (self.end[0] + 0.05 * self.scan_range[0]),  padding=0.05)
                    # self.axis_1.set_xlim(left=(self.start[0] - 0.05 * self.scan_range[0]),
                    #                      right=(self.end[0] + 0.05 * self.scan_range[0]))
                elif self.is_x_log_scaled[0]:
                    print('log case')
                    self.ui.PlotWidget.setXRange((self.start[0] - 0.1 * self.start[0]),
                                                 (self.end[0] + 0.1 * self.end[0]), padding=0.05)
                    self.ui.PlotWidget2.setXRange((self.start[0] - 0.1 * self.start[0]),
                                                  (self.end[0] + 0.1 * self.end[0]), padding=0.05)
                    # self.axis_1.set_xlim(left=(self.start[0] - 0.1 * self.start[0]),
                    #                      right=(self.end[0] + 0.1 * self.end[0]))
            elif self.start[0] > self.end[0]:
                print('start > end')
                if not self.is_x_log_scaled[0]:
                    print('linear case')
                    self.ui.PlotWidget.setXRange((self.end[0] - 0.05 * self.scan_range[0]),
                                                 (self.start[0] + 0.05 * self.scan_range[0]), padding=0.05)
                    self.ui.PlotWidget2.setXRange((self.end[0] - 0.05 * self.scan_range[0]),
                                                 (self.start[0] + 0.05 * self.scan_range[0]), padding=0.05)
                    # self.axis_1.set_xlim(left=(self.end[0] - 0.05 * self.scan_range[0]),
                    #                      right=(self.start[0] + 0.05 * self.scan_range[0]))
                elif self.is_x_log_scaled[0]:
                    print('log case')
                    self.ui.PlotWidget.setXRange((self.end[0] - 0.1 * self.end[0]),
                                                 (self.start[0] + 0.1 * self.start[0]), padding=0.05)
                    self.ui.PlotWidget2.setXRange((self.end[0] - 0.1 * self.end[0]),
                                                  (self.start[0] + 0.1 * self.start[0]), padding=0.05)
                    # self.axis_1.set_xlim(left=(self.end[0] - 0.1 * self.end[0]),
                    #                      right=(self.start[0] + 0.1 * self.start[0]))
        print('limits set')
        print(str(self.abscissa_name[0]))
        # self.ui.PlotWidget.setLabel('bottom', self.abscissa_name[0])
        # self.ui.PlotWidget2.setLabel('bottom', self.abscissa_name[0])
        # self.axis_1.set_xlabel(self.abscissa_name[0])
        print('label set')
        if self.is_recording_transient:
            self.ui.PlotWidget.setXRange(0, self.transient_duration, padding=0.05)
            self.ui.PlotWidget2.setXRange(0, self.transient_duration, padding=0.05)
        # if self.output_name[1] == 'Theta (Degrees)':
        #     self.ui.PlotWidget2.setYRange(-180, 180, padding=0.05)
        #     self.axis_2.set_ylim(bottom=-180, top=180)
        # else:  # self.output_variables == 'X/Y':
            # print('Auto scaling should be true')
            # self.ui.PlotWidget2.enableAutoRange(axis='y')
            # self.ui.PlotWidget2.setAutoVisible(y=True)
            # self.ui.PlotWidget2.autoRange(padding=0.05)
            # self.axis_2.set_ylim(auto=True)
        # self.ui.PlotWidget.enableAutoRange(axis='y')
        # self.ui.PlotWidget.setAutoVisible(y=True)
        # self.ui.PlotWidget.autoRange(padding=0.05)
        # self.ui.PlotWidget.setLogMode(x=self.is_x_log_scaled[0])
        # self.ui.PlotWidget2.setLogMode(x=self.is_x_log_scaled[0])

        t0 = time.time()
        QApplication.processEvents()
        print('Process Events Duration: ' + str(time.time() - t0))

    # def set_1d_plot_properties(self):
    #     print('inside set_1d_plot_properties')
    #     print('self.is_x_log_scaled = ' + str(self.is_x_log_scaled[0]))
    #     self.axis_1.set_xscale(self.is_x_log_scaled[0])
    #     print('set xscale')
    #     if self.step_count[0] != 1:
    #         print('self.step_count was not 1')
    #         if self.start[0] < self.end[0]:
    #             print('start < end')
    #             if self.is_x_log_scaled[0] == 'linear':
    #                 print('linear case')
    #                 self.axis_1.set_xlim(left=(self.start[0] - 0.05 * self.scan_range[0]),
    #                                      right=(self.end[0] + 0.05 * self.scan_range[0]))
    #             elif self.is_x_log_scaled[0] == 'log':
    #                 print('log case')
    #                 self.axis_1.set_xlim(left=(self.start[0] - 0.1 * self.start[0]),
    #                                      right=(self.end[0] + 0.1 * self.end[0]))
    #         elif self.start[0] > self.end[0]:
    #             print('start > end')
    #             if self.is_x_log_scaled[0] == 'linear':
    #                 print('linear case')
    #                 self.axis_1.set_xlim(left=(self.end[0] - 0.05 * self.scan_range[0]),
    #                                      right=(self.start[0] + 0.05 * self.scan_range[0]))
    #             elif self.is_x_log_scaled[0] == 'log':
    #                 print('log case')
    #                 self.axis_1.set_xlim(left=(self.end[0] - 0.1 * self.end[0]),
    #                                      right=(self.start[0] + 0.1 * self.start[0]))
    #     print('limits set')
    #     self.axis_1.set_xlabel(self.abscissa_name[0])
    #     print('label set')
    #     if self.output_name[1] == 'Theta (Degrees)':
    #         self.axis_2.set_ylim(bottom=-180, top=180)
    #     else:  # self.output_variables == 'X/Y':
    #         print('Auto scaling should be true')
    #         self.axis_2.set_ylim(auto=True)
    #
    #     self.line1, = self.axis_1.plot([])
    #     self.line2, = self.axis_2.plot([])
    #     self.line3, = self.axis_1.plot([])
    #     self.line4, = self.axis_2.plot([])
    #
    #     # plt.show(False)
    #     # plt.draw()
    #     self.ui.PlotWidget.canvas.draw()
    #     self.axis_1_background = self.ui.PlotWidget.canvas.copy_from_bbox(self.axis_1.bbox)
    #     self.axis_2_background = self.ui.PlotWidget.canvas.copy_from_bbox(self.axis_2.bbox)
    #
    #     plt.show(block=False)

    @QtCore.pyqtSlot()
    def calc_steps_from_num(self, dim_idx=0):
        idx = dim_idx
        print('inside calc_from_num')
        self.step_count[idx] = self.num_steps_spbxs[idx].value()

        if not self.experiment_in_progress:
            self.clear_plots()
            # if self.plot1 is not None:
            #     self.ui.PlotWidget.removeItem(self.plot1)
            #     self.plot1 = None
            # if self.plot2 is not None:
            #     self.ui.PlotWidget2.removeItem(self.plot2)
            #     self.plot2 = None
            # if self.plot3 is not None:
            #     self.ui.PlotWidget.removeItem(self.plot3)
            #     self.plot3 = None
            # if self.plot4 is not None:
            #     self.ui.PlotWidget2.removeItem(self.plot4)
            #     self.plot4 = None

        if self.abscissae[idx] is None or self.abscissae[idx] == 0:
            self.scale_factor[idx] = 1
            self.start[idx] = 1
            self.end[idx] = self.step_count[idx]
            self.sweep_start_spbxs[idx].setEnabled(True)
            self.sweep_end_spbxs[idx].setEnabled(True)
            self.sweep_start_spbxs[idx].setValue(self.start[idx])
            self.sweep_end_spbxs[idx].setValue(self.end[idx])
            self.sweep_start_spbxs[idx].setEnabled(False)
            self.sweep_end_spbxs[idx].setEnabled(False)
            self.log_spacing_checkboxes[idx].blockSignals(True)     # Prevents infinite recursion
            self.log_spacing_checkboxes[idx].setChecked(False)
            self.log_spacing_checkboxes[idx].blockSignals(False)
            self.log_spacing[idx] = False
        elif self.abscissae[idx] == 1:
            self.scale_factor[idx] = 10**(3*self.units_cbxes[idx].currentIndex())
            self.end[idx] = (self.sweep_end_spbxs[idx].value()) * self.scale_factor[idx]
            self.start[idx] = (self.sweep_start_spbxs[idx].value()) * self.scale_factor[idx]
        else:
            self.scale_factor[idx] = 1
            self.end[idx] = (self.sweep_end_spbxs[idx].value()) * self.scale_factor[idx]
            self.start[idx] = (self.sweep_start_spbxs[idx].value()) * self.scale_factor[idx]

        self.scan_range[idx] = self.end[idx] - self.start[idx]

        if self.log_spacing[idx]:
            print('inside log case')
            self.is_x_log_scaled[idx] = True
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
            self.is_x_log_scaled[idx] = False

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
        self.set_1d_plot_properties()


    @helpers.measure_time
    def expt_duration(self):
        if self.abscissae[0] == 0 or self.abscissae[0] is None:
            return
        try:
            self.settings.settling_delay_factor = self.settings.ui.lockin_delay_scale_spbx.value()
            self.lockin_delay = self.settings.settling_delay_factor * self.settings.lia.time_constant_value
            print('lockin_delay: ' + str(self.lockin_delay))

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
                elif self.abscissae[idx] == 1:      # Pump Mod Freq
                    abs_set_delay[idx] = 0.44
                elif self.abscissae[idx] == 2:      # Probe WL
                    abs_set_delay[idx] = (2 * ave_step[idx]) / mono_speed + mono_delay_offset
                elif self.abscissae[idx] == 3:      # Magnetic Field
                    abs_set_delay[idx] = 0
                elif self.abscissae[idx] == 4:      # RF Freq
                    abs_set_delay[idx] = 0.385
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

        if not self.abscissae[abscissa_idx] == 0:
            self.sweep_start_spbxs[0].setEnabled(True)
            self.sweep_start_spbxs[1].setEnabled(True)
            self.sweep_end_spbxs[0].setEnabled(True)
            self.sweep_end_spbxs[1].setEnabled(True)

        if self.abscissae[abscissa_idx] == 0:
            self.abscissae[abscissa_idx] = None
            self.sweep_start_spbxs[0].setEnabled(False)
            self.sweep_start_spbxs[1].setEnabled(False)
            self.sweep_end_spbxs[0].setEnabled(False)
            self.sweep_end_spbxs[1].setEnabled(False)
        elif self.abscissae[abscissa_idx] == 1:
            print('Pump Mod Selected')
            self.get_abs_name(abscissa_idx)
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
            self.get_abs_name(abscissa_idx)
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
            self.get_abs_name(abscissa_idx)
            self.units[abscissa_idx] = 'G'

            try:
                self.sweep_start_spbxs[abscissa_idx].setValue(self.settings.presets.field_start)
                self.sweep_end_spbxs[abscissa_idx].setValue(self.settings.presets.field_end)
                self.num_steps_spbxs[abscissa_idx].setValue(self.settings.presets.field_num_steps)

                self.units_cbxes[abscissa_idx].clear()
                self.units_cbxes[abscissa_idx].addItems(['G'])
                self.units_cbxes[abscissa_idx].setCurrentIndex(0)
                self.units_cbxes[abscissa_idx].setEnabled(False)

                print('set presets')
                self.log_spacing_checkboxes[abscissa_idx].setChecked(False)

                self.calc_steps_from_num(dim_idx=abscissa_idx)
            except:
                print(sys.exc_info()[:])

            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('Static Magnetic Field (Gauss)')
        elif self.abscissae[abscissa_idx] == 4:
            print('RF Carrier Freq Selected')
            # if abscissa_idx == 0:
            #     self.units[abscissa_idx] = self.ui.sweep_units_cbx.currentText()
            # elif abscissa_idx == 1:
            #     self.units[abscissa_idx] = self.ui.sweep_units_cbx_dim2.currentText()
            #
            # self.x_axis_label = 'RF Frequency (' + self.units[abscissa_idx] + ')'
            # self.abscissa_name[abscissa_idx] = self.x_axis_label


            try:
                self.sweep_start_spbxs[abscissa_idx].setValue(self.settings.presets.rf_freq_start)
                self.sweep_end_spbxs[abscissa_idx].setValue(self.settings.presets.rf_freq_end)
                self.num_steps_spbxs[abscissa_idx].setValue(self.settings.presets.rf_freq_num_steps)

                self.units_cbxes[abscissa_idx].clear()
                self.units_cbxes[abscissa_idx].addItems(['Hz', 'kHz', 'MHz', 'GHz'])
                self.units_cbxes[abscissa_idx].setCurrentIndex(2)
                self.units_cbxes[abscissa_idx].setEnabled(True)

                # self.units[abscissa_idx] = self.units_cbxes[abscissa_idx].currentText()
                #
                # self.x_axis_label = 'RF Frequency (' + self.units[abscissa_idx] + ')'
                # self.abscissa_name[abscissa_idx] = self.x_axis_label
                self.get_abs_name(abscissa_idx)

                self.log_spacing_checkboxes[abscissa_idx].setChecked(False)
                self.log_spacing[abscissa_idx] = False

                self.calc_steps_from_num(dim_idx=abscissa_idx)
            except:
                print(sys.exc_info()[:])
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Carrier Frequency (GHz)')
        elif self.abscissae[abscissa_idx] == 5:
            print('RF Mod Freq Selected')
            # self.ui.PlotWidget.canvas.axes_main.set_xlabel('RF Modulation Frequency (Hz)')
        elif self.abscissae[abscissa_idx] == 6:
            print('Lockin Ref Freq Selected')
        else:
            print('This case not coded yet')

    @QtCore.pyqtSlot()
    def get_abs_name(self, abscissa_idx):
        self.units[abscissa_idx] = self.units_cbxes[abscissa_idx].currentText()
        if self.abscissae[abscissa_idx] is None or self.abscissae[abscissa_idx] == 0:
            self.x_axis_label = 'Meas. Point Index'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 1:
            self.x_axis_label = 'Pump Modulation Frequency (Hz)'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 2:
            self.x_axis_label = 'Probe Wavelength (nm)'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 3:
            self.x_axis_label = 'Static Magnetic Field (G)'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 4:
            self.x_axis_label = 'RF Frequency (' + self.units[abscissa_idx] + ')'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 5:
            self.x_axis_label = 'RF Mod Frequency (' + self.units[abscissa_idx] + ')'
            self.abscissa_name[abscissa_idx] = self.x_axis_label
        elif self.abscissae[abscissa_idx] == 6:
            pass

    @QtCore.pyqtSlot(str)
    def experiment_preset_cbx_activated(self, experiment_str):
        print(experiment_str)
        if experiment_str == '-Manual Setup-':
            self.enable_all_ui_objects()

        elif experiment_str == 'Optical Absorption Spectrum':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(2)
            self.disable_dim2()

            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)
            self.ui.go_to_rf_freq_btn.setEnabled(False)
            self.ui.go_to_rf_mod_freq_btn.setEnabled(False)

        elif experiment_str == 'EPR Spectrum (Field-Swept)':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(3)
            self.disable_dim2()

            self.ui.probe_wl_spbx.setEnabled(False)
        elif experiment_str == 'PL Lifetime':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(1)                               # Pump Modulation Frequency = 1
            self.disable_dim2()

            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)
            self.ui.go_to_rf_freq_btn.setEnabled(False)
            self.ui.go_to_rf_mod_freq_btn.setEnabled(False)

        elif experiment_str == 'PA Lifetime (Single WL)':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(1)
            self.disable_dim2()

            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)
            self.ui.go_to_rf_freq_btn.setEnabled(False)
            self.ui.go_to_rf_mod_freq_btn.setEnabled(False)

        elif experiment_str == 'PA Spectrum (Single Pump Mod Freq)':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(2)
            self.disable_dim2()

            self.ui.rf_freq_spbx.setEnabled(False)
            self.ui.rf_mod_freq_spbx.setEnabled(False)
            self.ui.go_to_rf_freq_btn.setEnabled(False)
            self.ui.go_to_rf_mod_freq_btn.setEnabled(False)
        elif experiment_str == 'PA Lifetime/Spectrum (xyz)':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(1)
            self.ui.variable_2_cbx.setCurrentIndex(2)
        elif experiment_str == 'PL-DMR Magnetic Spectrum (Field-Swept)' or \
                experiment_str == 'PA-DMR Magnetic Spectrum (Field-Swept)':
            self.enable_all_ui_objects()
            self.ui.variable_1_cbx.setCurrentIndex(3)
            self.disable_dim2()
        else:
            print('experiment/case not set up yet')

    def disable_dim2(self, is_disabling=True):
        if is_disabling:
            self.ui.variable_2_cbx.setCurrentIndex(0)
            self.ui.variable_2_cbx.setEnabled(False)

            self.ui.sweep_start_spbx_dim2.setEnabled(False)
            self.ui.sweep_end_spbx_dim2.setEnabled(False)
            self.ui.num_steps_spbx_dim2.setEnabled(False)
        else:
            self.ui.variable_2_cbx.setCurrentIndex(0)
            self.ui.variable_2_cbx.setEnabled(True)

            self.ui.sweep_start_spbx_dim2.setEnabled(True)
            self.ui.sweep_end_spbx_dim2.setEnabled(True)
            self.ui.num_steps_spbx_dim2.setEnabled(True)

    @QtCore.pyqtSlot()
    def pause_btn_clicked(self):
        if not self.pause_scan:
            self.pause_scan = True
            self.ui.pause_btn.setText('Resume')
        elif self.pause_scan:
            self.pause_scan = False
            self.ui.pause_btn.setText('Pause')

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
        self.sr_lockin.error = ErrorCluster(status=False, code=0, details='')
        self.zi_lockin.error = ErrorCluster(status=False, code=0, details='')
        self.cg635.error = ErrorCluster(status=False, code=0, details='')
        self.md2000.error = ErrorCluster(status=False, code=0, details='')
        self.toptica.error = ErrorCluster(status=False, code=0, details='')
        self.smb100a.error = ErrorCluster(status=False, code=0, details='')

    @QtCore.pyqtSlot(int)
    def set_marker_settings(self, selector_index):
        if selector_index == 0:
            self.marker_size = 1
            self.line_style = None
        if selector_index == 1:
            self.marker_size = 10
            self.line_style = None
        if selector_index == 2:
            self.line_width = 1
            self.marker_size = (self.line_width / 1.2)
            self.line_style = QtCore.Qt.SolidLine

    @QtCore.pyqtSlot(bool, float)
    def update_tc_bandwidth(self, tf_primary, time_constant):

        order = self.settings.ui.uhfli_filter_order_cbx.currentIndex() + 1
        scaling_factor = zhinst.utils.bwtc_scaling_factor(order)
        bw_3db = scaling_factor / (time_constant * 2 * np.pi)

        if tf_primary:
            self.settings.ui.uhfli_filter_bandwidth_spbx.setValue(bw_3db)
        elif not tf_primary:
            self.settings.ui.uhfli_filter_bandwidth_spbx_2.setValue(bw_3db)

    @QtCore.pyqtSlot()
    def save_or_load_uhfli_settings(self, tf_save):
        if tf_save:
            filename, _ = self.save_file_dialog()
            if filename == '':
                filename = None
            if filename is not None:
                self.zi_lockin.save_settings(filename)
        elif not tf_save:
            filename = self.load_file_dialog()
            if filename == '':
                filename = None
            if filename is not None:
                self.zi_lockin.load_settings(filename)

    @QtCore.pyqtSlot(object, int)
    def toggle_item_enabled(self, object_name, determiner_value):
        if object_name == self.settings.ui.uhfli_freq_spbx:
            print('object name comparison worked')
            if determiner_value == 0:
                self.settings.ui.uhfli_freq_spbx.setDisabled(False)
            elif determiner_value > 0:
                self.settings.ui.uhfli_freq_spbx.setDisabled(True)

    @QtCore.pyqtSlot(str, str, float)  # This is called "overloading" a signal and slot. This is now TWO slots
    @QtCore.pyqtSlot(str, str, int)  # Which require different variable type inputs. str, int is default if unspec'd
    def update_instr_property(self, instr, prop_name, new_val):
        print('Attempting to update ' + instr + ' ' + prop_name + ' to value: ' + str(new_val) + '\n')
        if instr == 'sr_lockin':
            setattr(self.sr_lockin.settings, prop_name, new_val)
            setattr(self.settings.lia, prop_name, new_val)
        elif instr == 'zi_lockin':
            setattr(self.zi_lockin.settings, prop_name, new_val)
            setattr(self.settings.lia, prop_name, new_val)
        elif instr == 'md2000':
            setattr(self.md2000.settings, prop_name, new_val)
            setattr(self.settings.md2000, prop_name, new_val)
            self.settings.update_md2000_tab()
            if prop_name == 'cur_wl':
                self.ui.wavelength_lnedt.setText(str(self.md2000.settings.cur_wl) + ' nm')
        elif instr == 'cg635':
            setattr(self.cg635.settings, prop_name, new_val)
            setattr(self.settings.cg, prop_name, new_val)
            if prop_name == 'current_freq':
                self.ui.pump_mod_freq_lnedt.setText(str(self.cg635.settings.current_freq))
        elif instr == 'toptica':
            setattr(self.toptica.settings, prop_name, new_val)
            setattr(self.settings.toptica, prop_name, new_val)
            self.settings.update_topt_tab()
        elif instr == 'cryostat':
            setattr(self.cryostat.settings, prop_name, new_val)
            setattr(self.settings.cryostat, prop_name, new_val)
            self.settings.update_cryostat_tab()
            if prop_name == 'current_field':
                self.ui.field_lnedt.setText(str(self.cryostat.settings.current_field) + ' G')
            if prop_name == 'current_temp':
                self.ui.temp_lnedt.setText(str(self.cryostat.settings.current_temp) + ' K')
        elif instr == 'smb100a':
            self.settings.update_smb100a_tab()
            setattr(self.smb100a.settings, prop_name, new_val)
            setattr(self.settings.smb100a, prop_name, new_val)
            if prop_name == 'current_freq':
                self.settings.ui.smb100a_set_freq_spbx.blockSignals(True)       # Prevents infinite recursion
                self.settings.ui.smb100a_set_freq_spbx.setValue(new_val)
                self.settings.ui.smb100a_set_freq_spbx.blockSignals(False)
            elif prop_name == 'mod_freq':
                self.settings.ui.smb100a_set_mod_freq_spbx.blockSignals(True)
                self.settings.ui.smb100a_set_mod_freq_spbx.setValue(new_val)
                self.settings.ui.smb100a_set_mod_freq_spbx.blockSignals(False)
            elif prop_name == 'current_power':
                self.settings.ui.smb100a_set_power_spbx.blockSignals(True)
                self.settings.ui.smb100a_set_power_spbx.setValue(new_val)
                self.settings.ui.smb100a_set_power_spbx.blockSignals(False)
            elif prop_name == 'pulse_mod_status':
                self.settings.ui.smb100a_modulate_checkbox.blockSignals(True)
                self.settings.ui.smb100a_modulate_checkbox.setChecked(bool(new_val))
                self.settings.ui.smb100a_modulate_checkbox.blockSignals(False)

        else:
            raise ValueError('Cannot update ' + instr + ' - invalid instrument identifier')
        self.expt_duration()

    def set_icons(self):
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\settings_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionSettings.setIcon(icon1)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\help-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionHelp.setIcon(icon2)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionSave_Data.setIcon(icon3)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\connect_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionConnect_All.setIcon(icon4)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\play_pause_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pause_btn.setIcon(icon5)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        small_pts_icon = QtGui.QIcon()
        small_pts_icon.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                      r"\small_pts_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        large_pts_icon = QtGui.QIcon()
        large_pts_icon.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                               r"\large_pts_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        line_plot_icon = QtGui.QIcon()
        line_plot_icon.addPixmap(QtGui.QPixmap(r"C:\Users\padmr\Desktop\QIS\PADMR\padmr\supp\icons"
                                               r"\line_plot_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.ui.go_to_temp_btn.setIcon(icon6)
        self.ui.go_to_probe_wl_btn.setIcon(icon6)
        self.ui.go_to_rf_freq_btn.setIcon(icon6)
        self.ui.go_to_pump_mod_freq_btn.setIcon(icon6)
        self.ui.go_to_rf_mod_freq_btn.setIcon(icon6)
        self.ui.go_to_static_field_btn.setIcon(icon6)
        self.settings.ui.toptica_set_power_btn.setIcon(icon6)
        self.settings.ui.toptica_set_bias_power_btn.setIcon(icon6)
        self.settings.ui.cryostat_send_cmd_btn.setIcon(icon6)
        self.settings.ui.cg635_write_btn.setIcon(icon6)
        self.ui.scatter_pt_size_cbx.setItemIcon(0, small_pts_icon)
        self.ui.scatter_pt_size_cbx.setItemIcon(1, large_pts_icon)
        self.ui.scatter_pt_size_cbx.setItemIcon(2, line_plot_icon)


    def connect_signals_and_slots(self):
        """
        Connect signals and slots here. lambda functions are used to expand functionality options by allowing inclusion
        of additional arguments and/or multiple function calls from a single signal, as well as performing simple tasks.
        """

        # TODO:
        # 1. CG635_write_btn could be potentially replaced with the lnedt "Text Edited"
        # -------------------------------------------- ERRORS AND WARNINGS ---------------------------------------------
        self.sr_lockin_status_warning_signal.connect(self.sr_lockin_status_warning_window)
        self.general_error_signal.connect(self.general_error_window)

        self.settings.ui.clear_instr_errors_btn.clicked.connect(self.clear_instr_errors)
        self.sr_lockin.send_error_signal.connect(self.receive_error_signal)
        self.cg635.send_error_signal.connect(self.receive_error_signal)
        self.toptica.send_error_signal.connect(self.receive_error_signal)
        self.md2000.send_error_signal.connect(self.receive_error_signal)
        self.cryostat.send_error_signal.connect(self.receive_error_signal)

        # ----------------------------------------- PROPERTIES UPDATED -------------------------------------------------
        self.zi_lockin.settings_checked_signal[dict].connect(lambda i: self.settings.set_uhfli_settings_states(i))

        self.sr_lockin.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('sr_lockin', i, j))
        self.sr_lockin.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('sr_lockin', i, j))

        self.cg635.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('cg635', i, j))
        self.cg635.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('cg635', i, j))

        self.md2000.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('md2000', i, j))
        self.md2000.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('md2000', i, j))

        self.toptica.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('toptica', i, j))
        self.toptica.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('toptica', i, j))

        self.cryostat.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('cryostat', i, j))
        self.cryostat.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('cryostat', i, j))

        self.smb100a.property_updated_signal[str, int].connect(lambda i, j: self.update_instr_property('smb100a', i, j))
        self.smb100a.property_updated_signal[str, float].connect(lambda i, j: self.update_instr_property('smb100a', i, j))

        # --------------------------------------------- GENERAL --------------------------------------------------------
        # self.settings.ui.smb100a_com_port_cmb.currentTextChanged[str].connect(
        # lambda i: self.update_instr_property('smb100a', 'com_port', i))
        self.results_are_in_signal[int, int].connect(lambda i, j: self.plot_results(i, j))
        self.change_plot_title_signal[str].connect(lambda i: self.ui.plot_title_label.setText(i))

        self.settings.ui.debug_mode_checkbox.toggled[bool].connect(lambda i: setattr(self, 'is_debug_mode', i))
        self.settings.ui.refresh_com_ports_btn.clicked.connect(self.settings.check_com_ports)
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
            lambda i: self.update_instr_property('sr_lockin', 'settling_delay_factor', i))

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
        self.ui.average_each_point_checkbox.toggled[bool].connect(
            lambda i: setattr(self, 'is_averaging_pts', i))
        self.ui.average_each_point_checkbox.toggled[bool].connect(
            lambda i: self.ui.averaging_time_spbx.setEnabled(i))

        self.ui.num_scans_spbx.valueChanged[int].connect(lambda i: setattr(self, 'num_scans[0]', i))

        self.ui.variable_1_cbx.currentIndexChanged[int].connect(lambda i: self.abscissa_changed(i, abscissa_idx=0))
        self.ui.variable_2_cbx.currentIndexChanged[int].connect(lambda i: self.abscissa_changed(i, abscissa_idx=1))

        self.ui.start_btn.clicked.connect(self.start_experiment)
        self.ui.actionSave_Data.triggered.connect(lambda: self.save_stuff(manual=True))

        self.ui.scatter_pt_size_cbx.activated[int].connect(lambda i: self.set_marker_settings(i))
        # self.ui.record_time_trace_btn.clicked.connect(self.start_time_trace)
        self.ui.is_recording_transient_chkbx.toggled[bool].connect(lambda i: self.disable_dim2(i))
        self.ui.is_recording_transient_chkbx.toggled[bool].connect(lambda i: self.ui.average_each_point_checkbox.setDisabled(i))
        # self.ui.is_recording_transient_chkbx.toggled[bool].connect(
        #     lambda i: setattr(self, 'is_averaging_pts', i))

        # ----------------------------------------- TOPTICA LASER ------------------------------------------------------
        self.settings.toptica_enable_signal.connect(self.toptica.laser_enable)
        self.settings.toptica_start_signal.connect(self.toptica.laser_start)
        self.settings.ui.toptica_bias_enable_btn.clicked.connect(self.toptica.laser_enable)
        self.settings.ui.toptica_start_laser_btn.clicked.connect(self.toptica.laser_start)
        self.settings.toptica_stop_signal.connect(self.toptica.laser_disable)
        self.settings.ui.toptica_enable_digital_input_btn.clicked.connect(self.toptica.start_digital_modulation)
        self.settings.ui.toptica_stop_mod_btn.clicked.connect(self.toptica.stop_digital_modulation)

        self.settings.ui.toptica_set_power_btn.clicked.connect(
            lambda: self.toptica.set_power(power_setpoint=self.settings.ui.toptica_power_spbx.value()))

        self.settings.ui.toptica_set_bias_power_btn.clicked.connect(
            lambda: self.toptica.set_power(power_setpoint=self.settings.ui.toptica_bias_spbx.value()))

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

        # ---------------------------------------- SRS LOCK-IN ---------------------------------------------------------

        # Single parameter changes:
        self.settings.ui.auto_creserve_btn.clicked.connect(self.sr_lockin.auto_crsrv)
        self.settings.ui.auto_dyn_reserve_btn.clicked.connect(self.sr_lockin.auto_dyn_rsrv)
        self.settings.ui.auto_wreserve_btn.clicked.connect(self.sr_lockin.auto_wrsrv)
        self.settings.ui.auto_offset_btn.clicked.connect(self.sr_lockin.auto_offset)
        self.settings.ui.auto_phase_btn.clicked.connect(self.sr_lockin.auto_phase)
        self.settings.ui.auto_sens_btn.clicked.connect(self.sr_lockin.auto_sens)
        self.settings.ui.close_reserve_cbx.activated[int].connect(self.sr_lockin.update_crsrv)
        self.settings.ui.wide_reserve_cbx.activated[int].connect(self.sr_lockin.update_wrsrv)
        self.settings.ui.dynamic_reserve_cbx.activated[int].connect(self.sr_lockin.update_dyn_rsrv)
        self.settings.ui.expand_cbx.activated[int].connect(self.sr_lockin.update_expand)
        self.settings.ui.filter_slope_cbx.activated[int].connect(self.sr_lockin.update_filter_slope)
        self.settings.ui.sr844_harmonic_cbx.activated[int].connect(self.sr_lockin.update_2f)
        self.settings.ui.harmonic_spbx.valueChanged[int].connect(self.sr_lockin.update_harmonic)
        self.settings.ui.phase_spbx.valueChanged[float].connect(self.sr_lockin.update_phase)
        self.settings.ui.input_impedance_cbx.activated[int].connect(self.sr_lockin.update_input_impedance)
        # self.settings.ui.outputs_cbx.activated[int].connect(self.sr_lockin.update_outputs)
        self.settings.ui.ref_impedance_cbx.activated[int].connect(self.sr_lockin.update_ref_impedance)
        self.settings.ui.ref_source_cbx.activated[int].connect(self.sr_lockin.update_ref_source)
        self.settings.ui.sampling_rate_cbx.activated[int].connect(self.sr_lockin.update_sampling_rate)
        self.settings.ui.sensitivity_cbx.activated[int].connect(self.sr_lockin.update_sensitivity)
        self.settings.ui.time_constant_cbx.activated[int].connect(self.sr_lockin.update_time_constant)

        # ---------------------------------- MOno ----------------------------------------------------------------------
        self.md2000.status_message_signal[str].connect(lambda i: self.ui.statusbar.showMessage(i))
        self.settings.ui.mono_set_home_btn.clicked.connect(
            lambda i: self.md2000.set_home_position(self.settings.ui.mono_cal_wl_spbx.value()))
        self.settings.ui.mono_set_wl_spbx.valueChanged[float].connect(
            lambda i: self.md2000.go_to_wavelength(i, self.settings.md2000.bl_amt, self.settings.md2000.bl_bool))
        self.settings.ui.mono_bl_comp_chkbx.toggled[bool].connect(lambda i: self.update_md2000_property('bl_bool', i))
        self.settings.ui.mono_speed_spbx.valueChanged[float].connect(self.md2000.set_speed)

        # --------------------------------- CRYOSTAT -------------------------------------------------------------------
        self.settings.ui.cryostat_send_cmd_btn.clicked.connect(self.cryostat_write_manual_cmd)
        self.ui.go_to_static_field_btn.clicked.connect(
            lambda i: self.cryostat.set_field(self.ui.static_field_spbx.value()))
        self.settings.ui.cryostat_magnet_settling_time_sbpx.valueChanged[float].connect(
            lambda i: self.update_instr_property('cryostat', 'magnet_settling_time', i))
        self.settings.ui.cryostat_zero_magnet_now_btn.clicked.connect(self.cryostat.zero_magnet)
        self.settings.ui.cryostat_delay_between_scans_spbx.valueChanged[float].connect(
            lambda i: self.update_instr_property('cryostat', 'magnet_prescan_settling_time', i))
        self.settings.ui.cryostat_zero_between_scans_chkbx.toggled[bool].connect(
            lambda i: self.update_instr_property('cryostat', 'is_zero_magnet_between_scans', i))

        # ----------------------------------- SMB100A (Microwave Source) -----------------------------------------------
        self.settings.ui.smb100a_run_btn.clicked.connect(self.smb100a.run)
        self.settings.ui.smb100a_stop_btn.clicked.connect(self.smb100a.stop)
        self.settings.ui.smb100a_send_cmd_btn.clicked.connect(self.smb100a_write_manual_cmd)
        self.settings.ui.smb100a_modulate_checkbox.toggled[bool].connect(lambda i: self.smb100a.toggle_modulation(i))
        self.settings.ui.smb100a_set_freq_spbx.valueChanged[float].connect(
            lambda i: self.smb100a.set_freq(i, self.settings.ui.smb100a_freq_units_cbx.currentText()))
        self.settings.ui.smb100a_set_power_spbx.valueChanged[float].connect(lambda i: self.smb100a.set_power(i))
        self.settings.ui.smb100a_set_mod_freq_spbx.valueChanged[float].connect(
            lambda i: self.smb100a.set_pulse_mod_freq(i, self.settings.ui.smb100a_mod_freq_units.currentText()))
        self.settings.ui.smb100a_mod_source_cmb.activated[str].connect(
            lambda i: self.update_instr_property('smb100a', 'mod_source', i))
        self.settings.ui.smb100a_mod_source_cmb.activated[str].connect(
            lambda i: self.smb100a.set_pulse_mod_settings(i))

        # --------------------------------------------------------------------------------------------------------------
        # ----------------------------------- UHFLI (Zurich Instr Lockin) ----------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # React to UI interactions
        self.settings.ui.uhfli_get_current_settings_btn.clicked.connect(
            lambda: self.zi_lockin.get_current_settings(
                demodulator=self.settings.ui.uhfli_demodulator_idx_spbx.value()
            )
        )

        self.settings.ui.uhfli_save_settings_btn.clicked.connect(lambda: self.save_or_load_uhfli_settings(tf_save=True))

        self.settings.ui.uhfli_load_settings_btn.clicked.connect(lambda: self.save_or_load_uhfli_settings(tf_save=False))
        self.settings.ui.uhfli_input_cbx.currentIndexChanged[int].connect(
            lambda i: self.zi_lockin.set_input(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(), input_idx=i))
        self.settings.ui.uhfli_range_spbx.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_range(input_idx=self.settings.ui.uhfli_input_cbx.currentIndex(), input_range=i))
        self.settings.ui.uhfli_range_spbx_2.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_range(input_idx=self.settings.ui.uhfli_input_cbx_2.currentIndex(), input_range=i))
        self.settings.ui.uhfli_input_impedance_cbx.activated.connect(
            lambda i: self.zi_lockin.set_input_impedance(input_idx=self.settings.ui.uhfli_input_cbx.currentIndex(),
                                                         desired_imp_idx=self.settings.ui.uhfli_input_impedance_cbx.currentIndex()))
        self.settings.ui.uhfli_input_coupling_cbx.activated.connect(
            lambda i: self.zi_lockin.set_input_coupling(input_idx=self.settings.ui.uhfli_input_cbx.currentIndex(),
                                                        desired_coupling_idx=self.settings.ui.uhfli_input_coupling_cbx.currentIndex()))

        # Reference mode manual (internal) vs external. Disable Frequency spinbox if external control
        self.settings.ui.uhfli_ref_mode_cbx.activated[int].connect(
            lambda i: [
                self.zi_lockin.set_mode(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(), trigger_mode_idx=i),
                self.toggle_item_enabled(object_name=self.settings.ui.uhfli_freq_spbx, determiner_value=i)
            ]
        )

        self.settings.ui.uhfli_freq_spbx.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_ref_freq(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(), target_freq=i)
        )

        self.settings.ui.uhfli_harm_spbx.valueChanged[int].connect(
            lambda i: self.zi_lockin.set_harmonic(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(), harmonic=i)
        )

        self.settings.ui.uhfli_phase_spbx.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_phase(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(), target_phase=i)
        )

        self.settings.ui.uhfli_filter_order_cbx.activated[int].connect(
            lambda i: [
                self.zi_lockin.set_filter_order(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(),
                                                      filter_order=i+1),
                self.update_tc_bandwidth(tf_primary=True, time_constant=self.settings.ui.uhfli_time_constant_spbx.value())
            ]
        )

        self.settings.ui.uhfli_time_constant_spbx.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_time_constant(tf_primary=True,
                                                       demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(),
                                                       target_tc=i/1000)
        )

        self.settings.ui.uhfli_time_constant_spbx_2.valueChanged[float].connect(
            lambda i: self.zi_lockin.set_time_constant(tf_primary=False,
                                                       demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx_2.value(),
                                                       target_tc=i/1000)
        )

        self.settings.ui.uhfli_sinc_filtering_chkbx.toggled[bool].connect(
            lambda i: self.zi_lockin.toggle_sinc_filter(demod_idx=self.settings.ui.uhfli_demodulator_idx_spbx.value(),
                                                        tf_enable_sinc=i)
        )

        # Update UI based on emitted signals (e.g. responses from the device)
        self.zi_lockin.tc_updated_primary_signal_zi[float].connect(
                lambda i: [
                    self.settings.ui.uhfli_time_constant_spbx.setValue(i*1000),
                    self.update_tc_bandwidth(tf_primary=True, time_constant=i)
                ]
        )
        self.zi_lockin.tc_updated_secondary_signal_zi[float].connect(
                lambda i: [
                 self.settings.ui.uhfli_time_constant_spbx_2.setValue(i*1000),
                 self.update_tc_bandwidth(tf_primary=False, time_constant=i)
                ]
        )


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)            # Defines the instance of the whole application
    app.setStyle('Fusion')                  # I like the way fusion looks
    expt_control_window = MainWindow()      # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    expt_control_window.show()
    sys.exit(app.exec_())
