
import os
import sys
import pyvisa
import time
import numpy as np
import codecs
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import QFile

from decorator import decorator
import PyQt5

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt5.QtCore import QThreadPool, QRunnable
from Lockin_Amplifier.plotwidget import PlotWidget #(using the same name as in other files will be a problem)
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg

from Lockin_Amplifier.SRS_844_UI import Ui_Form as LockinUiForm
from Lockin_Amplifier.SR_Lockin_using_Prologix_Module import PrologixAdaptedSRLockin

#TODO:
# 1. Figure out why the hell the query button doesn't allow me to query, when it worked immediately before during setup
# 1. Create a presets .ini file so people don't have to check for e.g. dynamic reserve
# 2. Incorporate multiple acquisition modes (i.e. using the lock-in storage versus not using it)
# 3. Incorporate instrument error checks

pyqt = os.path.dirname(PyQt5.__file__)          # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))

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


class LockinWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(LockinWidget, self).__init__(*args, **kwargs)

        self.lockin_ui = LockinUiForm()
        self.lockin_ui.setupUi(self)
        self.resource = None
        self.select_resource_text = '----- Select Resource -----'
        self.lockin_instr = None
        self.output_selector_idx = 0   # X/Y
        self.continue_reading = False
        self.gpib_address = 8

        # ---------------------------------- Initialize GUI Object States --------------------------------------------
        self.lockin_ui.visa_resource_combobox.addItem(self.select_resource_text)

        # ------------------------------------ Initialization Functions -----------------------------------------------
        self.check_resources()

        # Multi-threading Stuff
        self.thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.thread_pool.maxThreadCount())

# -------------------------------------------------- Non Slot Methods -------------------------------------------------
    def read_lockin_worker(self):
        if self.output_selector_idx == 0:
            output_str = 'SNAP? ' + '1,2,8\n'
        elif self.output_selector_idx == 1:
            output_str = 'SNAP? ' + '3,5,8\n'
        elif self.output_selector_idx == 2:  # Manual
            output_str = 'SNAP? ' + '9,10,8\n'    # Just whatever is on the displays
        ch1_history = []
        ch2_history = []
        iters = []
        ii = 0
        print('about to start the while loop')
        while self.continue_reading is True:
            t0 = time.time()
            readout, error = self.lockin_instr.write_string(output_str, read=True)
            readout_ch1, readout_ch2, readout_freq = readout.split(',')
            print(readout)
            print(readout_ch1)
            print(readout_ch2)
            self.lockin_ui.ch1_lineedit.setText(readout_ch1)
            self.lockin_ui.ch2_lineedit.setText(readout_ch2)
            self.lockin_ui.ref_lineedit.setText(readout_freq.strip())    # The silliness here removes the \n

            # All this plotting stuff adds about 100 ms (on top of the 30-40 ms required for above).
            # this is useful for live updates but for getting the most out of the instrument it is not a good method
            # (for reference, the maximum sample rate of the instrument is 512 Hz, which is ~66 times faster than this
            # method. If your time constant is low these measurements are likely independent in which case you get 66x
            # more data in the same time period.
            print('loop iteration: ' + str(ii))
            readout_ch1 = float(readout_ch1)
            readout_ch2 = float(readout_ch2)

            ii = ii + 1
            ch1_history.append(readout_ch1)
            ch2_history.append(readout_ch2)
            iters.append(ii)

            ch1_history_array = np.array(ch1_history)
            ch2_history_array = np.array(ch2_history)
            iters_array = np.array(iters)

            self.lockin_ui.PlotWidget.canvas.axes_main.clear()
            self.lockin_ui.PlotWidget.canvas.axes_main.plot(iters_array, ch1_history_array)
            # self.lockin_ui.PlotWidget.canvas.axes_main.plot(iters_array, ch2_history_array)
            self.lockin_ui.PlotWidget.canvas.draw()
            dt = time.time() - t0
            print('Loop time: ' + str(dt) + 'seconds')

    def check_resources(self):                 # If this is only called once, isn't it better not to make it a function?
        self.rm = pyvisa.ResourceManager()
        all_resources = self.rm.list_resources()
        if len(all_resources) > 0:
            for ii in all_resources:
                self.lockin_ui.visa_resource_combobox.addItem(ii)
        else:
            return

    @QtCore.pyqtSlot(int)
    def output_selector_activated(self, output_index):
        self.output_selector_idx = output_index

    @QtCore.pyqtSlot()
    def stop_btn_clicked(self):
        self.continue_reading = False

    @QtCore.pyqtSlot()
    def start_btn_clicked(self):
        self.continue_reading = True
        read_outputs_thread = Worker(self.read_lockin_worker)
        self.thread_pool.start(read_outputs_thread)

    @QtCore.pyqtSlot()
    def query_btn_clicked(self):
        if self.lockin_instr is not None:  # This seems crappy but good enough for now
            print('lockin instr was not None')
            query_text = self.lockin_ui.write_str_lineedit.text()
            print('requested query: ' + query_text)
            query_text = codecs.decode(query_text, 'unicode_escape')
            print('requested escaped query: ' + query_text)

            # query_text = '*IDN?\n'
            response, error = self.lockin_instr.write_string(query_text, read=True)
            if error is True:
                print('Query error')
            else:
                print('response acquired: ' + response)
                self.lockin_ui.read_str_textedit.setPlainText(response)
        else:
            print('lockin instr was none')
        # self.lockin_instr.write('REST\n')

    def get_current_params(self):
        self.time_constant = self.lockin_instr.write_string('OFLT?\n', read=True)
        self.filter_slope = self.lockin_instr.write_string('OFSL?\n', read=True)
        self.input_impedance = self.lockin_instr.write_string('INPZ?\n', read=True)
        self.ref_inp_impedance = self.lockin_instr.write_string('REFZ?\n', read=True)
        self.two_f_detect_mode = self.lockin_instr.write_string('HARM?\n', read=True)
        self.close_dyn_reserve = self.lockin_instr.write_string('CRSV?\n', read=True)
        self.channel_1_disp = self.lockin_instr.write_string('DDEF? 1\n', read=True)
        self.channel_2_disp = self.lockin_instr.write_string('DDEF? 2\n', read=True)
        print('tc: ' + str(self.time_constant))
        print('slope: ' + str(self.filter_slope))
        print('inp z: ' + str(self.input_impedance))
        print('ref inp z: ' + str(self.ref_inp_impedance))
        print('2f detect mode: ' + str(self.two_f_detect_mode))

    @QtCore.pyqtSlot()
    def update_settings_btn_clicked(self):
        print('--------------------------UPDATING SETTINGS-------------------------------')
        # Time Constant
        tc_value_idx = self.lockin_ui.time_constant_combobox.currentIndex()  # 0=100 us, 1=300 us ... 16=10ks, 17=30ks
        self.lockin_instr.write('OFLT %d\n' % tc_value_idx)
        # Dynamic reserve
        # Sensitivity

    @QtCore.pyqtSlot()
    def collect_fast_data(self):
        if self.lockin_instr is not None:
            duration = 10
            sampling_rate = 64
            self.continue_reading = False            # Stop the live update thread
            time.sleep(0.05)                         # This shouldn't be necessary if live updating isn't occurring
            self.lockin_instr.clear_buffers()
            ch_1_data, ch_2_data = self.lockin_instr.collect_data(duration, sampling_rate)
            ch_1_ave = np.average(ch_1_data)
            ch_2_ave = np.average(ch_2_data)
            print(ch_1_ave)
            print(ch_2_ave)
        else:
            pass

    @QtCore.pyqtSlot(str)
    def com_port_combobox_activated(self, combobox_item):
        print(combobox_item)

        if combobox_item == self.select_resource_text:
            self.resource = None
        else:
            self.resource = combobox_item
            print(str(self.resource))
            self.lockin_instr = PrologixAdaptedSR844(self.resource, self.gpib_address)
            comms_failed = self.lockin_instr.test_comms()
            if comms_failed:
                self.lockin_instr = None
                print('comms failed')

# ------------------------------------------------------ Slots --------------------------------------------------------


# ------------------------------------------------- Run the program ---------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Defines the instance of the whole application
    lockin_widget = LockinWidget()  # Declares the instance of the main window class (moco_window.__init__ is called)
    # This ^ is where the gui is prepared before being presented in the next line\/
    lockin_widget.show()
    sys.exit(app.exec_())
