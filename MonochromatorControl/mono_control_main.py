# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 17:26:03 2020

@author: Ryan
"""

import os
import sys
import pyvisa
import time
import numpy as np

from decorator import decorator
import PyQt5

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThreadPool, QRunnable

from MonochromatorControl.mono_control_module import MonoDriver
from MonochromatorControl.mono_control_gui import Ui_MainWindow

pyqt = os.path.dirname(PyQt5.__file__)          # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))

#TODO:
# 1. Make it so that the correct com port is automatically found
# 2. Add an abort button to the initialization
# 3. If I want to import this class from another program and use the functions (not window),
#       what changes do I have to make?
# 4. Get to open from another window (full program)
# 5. Clean up tasks:
#   5a. Get rid of "status_message" in preference for showMessage (don't forget the time must be set)
#   5b. check for redundancies in variable names that could be reused (like stop_moving, stop_motion_bool)
#   5c. Clear stupid error_message variables out
#   5d. Get rid of excessive print functions
# 6. Get current wavelength after scan completes


@decorator
def check_mono_instance(f, *args, **kwargs):
    """ Decorate a function with this whenever the mono must be first initialized (or at least instantiated) before
    a function can effectively run. If the mono has not yet been initialized, the function will not be performed """
    # Note for later - develop this further to check more restrictive conditions
    if moco_window.debug_mode is True:
        print('...begin check_mono_instance decorator...')
        if moco_window.mono_instance is None:
            print('...begin check_mono_instance if case (no mono_instance) ...')
            moco_window.ui.statusbar.showMessage('ACTION FAILED - MONO COMMUNICATION NOT INITIALIZED', 5000)
            print('...end check_mono_instance if case (no mono_instance) ...')
            return
        elif moco_window.mono_instance is not None:
            print('...begin check_mono_instance elif case (mono_instance exists)...')
            pass
        return f(*args, **kwargs)
    else:
        if moco_window.mono_instance is None:
            moco_window.ui.statusbar.showMessage('ACTION FAILED - MONO COMMUNICATION NOT INITIALIZED', 5000)
            return
        elif moco_window.mono_instance is not None:
            pass
        return f(*args, **kwargs)


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


def calculate_scan_points(start, stop, step):
    num_wls = round((stop - start) / step) + 1
    stopping_points = np.empty(num_wls)
    for ii in range(0, num_wls):
        stopping_points[ii] = start + (step * ii)
    print('stopping points: ' + str(stopping_points))
    print('num_wls: ' + str(num_wls))
    return stopping_points, num_wls


class MainWindow(QMainWindow):
    """ This window is for the control of the monochromator"""
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)   # This runs the init method of QMainWindow

        # Load the ui.py file and prepare the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ------------------------------- initialize attribute values - ------------------------------------------------
        # These are attributes of the MainWindow class, not of the ui instance (which is an instance of Ui_MainWindow)
        # They are used as attributes of the program.
        self.mono_instance = None
        self.resource = None
        self.gr_dens = 1200
        self.backlash_compensation = True
        self.debug_mode = False
        self.select_resource_text = '----- Select Resource -----'
        self.backlash_amount = 10
        self.speed = 50
        self.initialized = False
        self.stop_scan = False
        self.zero_wavelength = 0

        # ------------------------------- Initialize GUI Object States -------------------------------------------------
        # These are methods/attributes of the ui instance. They all refer to specific objects which are part of the ui
        # e.g. buttons, spinners, comboboxes, etc.
        # self.ui.visa_resource_combobox.addItem('test')
        self.ui.backlash_checkbox.setCheckState(QtCore.Qt.Checked)
        self.ui.groove_density_combobox.setCurrentIndex(2)
        self.ui.tab_container.setCurrentIndex(0)
        self.ui.visa_resource_combobox.addItem(self.select_resource_text)
        self.ui.backlash_amount_spinner.setValue(self.backlash_amount)
        self.ui.speed_value_spinner.setValue(self.speed)
        # ------------------------------------ Run any initialization Functions ----------------------------------------

        self.check_resources()                  # Find all com ports with attached resources.

        # ------------------------ MULTI-THREADING STUFF ---------------------------------------------------------------
        self.thread_pool = QThreadPool()

        print("Multithreading with maximum %d threads" % self.thread_pool.maxThreadCount())

    # ------------------------------------- Non Slot Method Definitions ------------------------------------------------
    def check_resources(self):                 # If this is only called once, isn't it better not to make it a function?
        rm = pyvisa.ResourceManager()
        all_resources = rm.list_resources()
        if len(all_resources) > 0:
            for ii in all_resources:
                self.ui.visa_resource_combobox.addItem(ii)
        else:
            return

    def update_wavelength(self):
        ii = 1
        while self.mono_instance.continue_updating is True:
            time.sleep(0.01)
            self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))
            ii += 1

    def check_for_status_updates(self):
        print('in the check_for_status_updates fn')
        tmp_message = ''
        ii = 1
        counter = 0
        while True:
            if tmp_message == self.mono_instance.status_message:
                counter += 1
            else:
                counter = 0

            time.sleep(0.1)
            if counter > 100:
                self.mono_instance.status_message = ''
                counter = 0

            tmp_message = self.mono_instance.status_message

            self.ui.statusbar.showMessage(tmp_message, 10000)
            ii += 1

    def initialization_tasks_thread(self):
        try:
            self.mono_instance.initialize_mono()
            self.ui.statusbar.showMessage('Setting Parameters', 5000)
            print('Initialization Success, setting parameters...')
            # self.ui.statusbar.showMessage('Mono Initialized', 5000)
            # self.mono_instance.status_message = 'Setting Speed'
            self.mono_instance.set_speed(self.speed)
            self.initialized = True
            self.mono_instance.status_message = 'Initialization Complete - Remember to Set Current Wavelength'
        except:  # Fix this to make it less broad sometime
            print('Exception Occurred During Initialization - Add this error to code')
            print(str(sys.exc_info()[0]))
            print(str(sys.exc_info()[1]))
            print(str(sys.exc_info()[2]))

        self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))
        print('self.mono_instance.connected: ' + str(self.mono_instance.connected))
        self.mono_instance.busy = False
        self.ui.statusbar.showMessage('Initialization Complete - Remember to Set Home Wavelength', 5000)
        print('-------------------------------------initialization Complete------------------------------------------')

    def scan_worker(self, scan_points, cycles, delay):
        num_wls = len(scan_points)
        for jj in range(0, cycles):
            if self.stop_scan is True:
                break
            else:
                for ii in range(0, num_wls):
                    if self.stop_scan is True:
                        break
                    else:
                        self.ui.statusbar.showMessage('Moving to ' + str(scan_points[ii]) + ' nm', 5000)
                        self.mono_instance.go_to_wavelength(scan_points[ii], self.mono_instance.speed,
                                                            self.backlash_amount, self.backlash_compensation)
                        self.ui.statusbar.showMessage('Pausing at ' + str(scan_points[ii]) + ' nm', 5000)
                        time.sleep(delay)

        time.sleep(0.1)     # This just felt right
        self.ui.statusbar.showMessage('Scan Complete', 5000)
        self.mono_instance.open_visa()
        self.mono_instance.current_wavelength = self.mono_instance.get_current_pos()
        self.mono_instance.close_visa()
        self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))
        self.stop_scan = False
        self.mono_instance.busy = False
        print('----------------------------------Scanning Complete ---------------------------------------------')

    # ------------------------------------------------ HOOK UP SLOTS ---------------------------------------------------
    # SET MONO TAB -------------------------------------
    @QtCore.pyqtSlot()      # It's unclear if these decorators are actually needed, I think it works without them
    def set_com_port(self):
        print('-----------------------------------Set Com Port ----------------------------------------------')
        self.resource = self.ui.visa_resource_combobox.currentText()
        if self.resource == self.select_resource_text:
            self.resource = None
        self.ui.statusbar.showMessage(self.resource, 2000)

    @QtCore.pyqtSlot()
    def set_groove_density(self):
        print('-------------------------------------Set Groove Density-------------------------------------')
        gr_dens_str = self.ui.groove_density_combobox.currentText()
        self.gr_dens = int(gr_dens_str)
        self.ui.statusbar.showMessage('Groove Density set to ' + gr_dens_str + ' gr/mm', 5000)
        if isinstance(self.mono_instance, MonoDriver):
            self.mono_instance.groove_density = self.gr_dens
            self.mono_instance.get_k_number()

    @QtCore.pyqtSlot()
    def clicked_initialize_button(self):
        print('-----------------------------------------Initializing-------------------------------------------------')
        if isinstance(self.resource, str):           # Ideally the conditions here would verify more clearly
            self.mono_instance = MonoDriver(self.resource, self.gr_dens)
            self.mono_instance.busy = True
            self.ui.statusbar.showMessage('Initializing...')
            # If first time initializing, add an updates thread to monitor status constantly
            # This is nice in this script, but it is not exactly the best use of a thread...
            # if self.initialized is False:
            #     print('beginning constant status updates')
            #     updates_thread = Worker(self.check_for_status_updates)
            #     self.thread_pool.start(updates_thread)

            initialization_thread = Worker(self.initialization_tasks_thread)
            self.thread_pool.start(initialization_thread)

        else:
            self.mono_instance.status_message = 'INITIALIZATION FAILED - Resource Selection Failed'
            # self.ui.statusbar.showMessage('INITIALIZATION FAILED - Resource Selection Failed', 5000)
            return

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_home_button(self):
        """ This sets the position (in steps), that the monochromator considers " 0 steps ". Absolute moves are
         with respect to this position. I think it's ok if you move to a different wavelength than the "natural zero"
         i.e. the one it naturally arrives at after initialization, you just have to set the value to what wavelength
         the mono reads """
        print('------------------------------------Setting Home ------------------------------------')
        if self.mono_instance.busy is False:
            print('self.mono_instance.connected inside home btn: ' + str(self.mono_instance.connected))
            self.zero_wavelength = self.ui.calib_wl_spinner.value()
            self.mono_instance.calibration_wavelength = self.zero_wavelength
            self.mono_instance.set_zero_position()
            self.mono_instance.current_wavelength = self.mono_instance.calibration_wavelength
            print('Home wavelength is: ' + str(self.zero_wavelength))
            self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))
            self.ui.statusbar.showMessage('Home Wavelength Set', 5000)

    @QtCore.pyqtSlot()
    def state_changed_bl_compensation(self):
        self.backlash_compensation = self.ui.backlash_checkbox.isChecked()

    @QtCore.pyqtSlot()
    def value_changed_backlash_spinner(self):
        self.backlash_amount = self.ui.backlash_amount_spinner.value()

    # SETUP TAB -------------------------------------
    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_go_to_wl_button(self):
        print('------------------------------------go to wavelength--------------------------------------')
        destination = self.ui.goto_wl_spinner.value()

        if self.mono_instance.busy is False:
            self.mono_instance.busy = True

            self.mono_instance.open_visa()

            worker = Worker(self.mono_instance.go_to_wavelength, destination, self.mono_instance.speed,
                            self.backlash_amount, self.backlash_compensation)
            self.thread_pool.start(worker)

            time.sleep(0.2)

            self.mono_instance.continue_updating = True
            get_pos_worker = Worker(self.update_wavelength)
            self.thread_pool.start(get_pos_worker)

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_nudge_down_button(self):
        print('---------------------------------------nudge down---------------------------------------------')
        if self.mono_instance.busy is False:
            self.mono_instance.busy = True
            nudge_amount = self.ui.nudge_amount_spinner.value()

            nudge_thread = Worker(self.mono_instance.nudge, amount_nm=nudge_amount, higher=False)
            self.thread_pool.start(nudge_thread)

            self.ui.statusbar.showMessage(self.mono_instance.status_message, 5000)
            self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))

            time.sleep(0.2)

            print('trying to update_wavelength')
            self.mono_instance.continue_updating = True
            get_pos_worker = Worker(self.update_wavelength)
            self.thread_pool.start(get_pos_worker)

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_nudge_up_button(self):
        print('---------------------------------------nudge up---------------------------------------')
        if self.mono_instance.busy is False:
            self.mono_instance.busy = True

            nudge_amount = self.ui.nudge_amount_spinner.value()
            nudge_thread = Worker(self.mono_instance.nudge, amount_nm=nudge_amount, higher=True)
            self.thread_pool.start(nudge_thread)

            self.ui.statusbar.showMessage(self.mono_instance.status_message, 5000)
            self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))

            time.sleep(0.2)

            self.mono_instance.continue_updating = True
            get_pos_worker = Worker(self.update_wavelength)
            self.thread_pool.start(get_pos_worker)

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_stop_nudge_button(self):
        print('---------------------------------------stop nudge---------------------------------------')
        self.mono_instance.stop_motion_bool = True
        self.mono_instance.stop_motion()
        self.ui.current_wl_output_lineedit.setText(str(self.mono_instance.current_wavelength))
        self.mono_instance.busy = False

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_speed_set_button(self):
        print('---------------------------------------speed set---------------------------------------')
        speed = self.ui.speed_value_spinner.value()
        self.mono_instance.set_speed(speed)
        self.ui.statusbar.showMessage(self.mono_instance.status_message, 5000)

    # SCAN TAB -------------------------------------
    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_start_scan_button(self):
        print('----------------------------------Start Scan--------------------------------------------')
        start_wl = self.ui.scan_start_wl_spinner.value()
        stop_wl = self.ui.scan_stop_wl_spinner.value()
        step_wl = self.ui.scan_step_spinner.value()
        delay = self.ui.scan_pause_spinner.value()
        cycles = self.ui.scan_cycles_spinner.value()
        self.stop_scan = False

        scan_points, number_wavelengths = calculate_scan_points(start_wl, stop_wl, step_wl)
        if self.mono_instance.busy is False:
            self.mono_instance.busy = True
            worker = Worker(self.scan_worker, scan_points, cycles, delay)
            self.thread_pool.start(worker)

    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_stop_scan_button(self):
        print('-------------------------------------Stop Scan------------------------------------------')
        self.stop_scan = True

    # DEBUG TAB ----------------------------------
    @check_mono_instance
    @QtCore.pyqtSlot()
    def clicked_debug_write_button(self):
        print('---------------------------------------debug write---------------------------------------')
        string_to_write = self.ui.debug_write_str_textbox.toPlainText()
        self.mono_instance.open_visa()
        self.mono_instance.write_str(string_to_write)
        print('closing visa (debug write)')
        self.mono_instance.close_visa()
        self.ui.debug_read_textbox.setPlainText(self.mono_instance.readout)

    @QtCore.pyqtSlot()
    def state_changed_debug_checkbox(self):
        self.debug_mode = self.ui.debug_checkbox.isChecked()

        if self.debug_mode is True:
            self.ui.visa_resource_combobox.addItem('test')
            self.ui.statusbar.showMessage('Now in Debug mode', 5000)
        if self.debug_mode is False:
            test_idx = self.ui.visa_resource_combobox.findText('test')
            self.ui.visa_resource_combobox.removeItem(test_idx)
            self.ui.statusbar.showMessage('Leaving Debug Mode', 5000)

    # --------------------------------------  METHODS (NON SLOTS) ------------------------------------------------------


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)        # Defines the instance of the whole application
    moco_window = MainWindow()          # Declares the instance of the main window class (moco_window.__init__ is called)
    # This ^ is where the gui is prepared before being presented in the next line\/
    moco_window.show()
    sys.exit(app.exec_())
