import os
import sys
import pyvisa
import time
import numpy as np

from decorator import decorator
import PyQt5

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThreadPool, QRunnable  # For multithreading (parallel tasks)

from Lockin_Amplifier.SRS_control_main import LockinWidget
from FullControl.expt_control_ui_20200708 import Ui_MainWindow as ExptControlMainWindow
from FullControl.plotwidget import PlotWidget

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


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the ui.py file and prepare the UI
        self.ui = ExptControlMainWindow()
        self.ui.setupUi(self)

        # ------------------------------- initialize attribute values - ------------------------------------------------
        # These are attributes of the MainWindow class, not of the ui instance
        # They are used as attributes of the program.

        # ------------------------------- Initialize GUI Object States -------------------------------------------------

        # ------------------------------------ Run any initialization Functions ----------------------------------------

        # ------------------------ MULTI-THREADING STUFF ---------------------------------------------------------------
        self.thread_pool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.thread_pool.maxThreadCount())

    # -------------------------------------------NON-SLOT METHODS--------------------------------------------------

    # -------------------------------------------SLOT DEFINITIONS ------------------------------------------------------

    @QtCore.pyqtSlot()
    def open_mono_window(self):
        pass

    @QtCore.pyqtSlot()
    def open_lockin_window(self):
        self.lockin_window = LockinWidget()
        self.lockin_window.show()
        pass


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Defines the instance of the whole application
    expt_control_window = MainWindow()  # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    expt_control_window.show()
    sys.exit(app.exec_())
