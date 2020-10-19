from PyQt5 import QtCore
from decorator import decorator
import time


@decorator
def measure_time(f, *args, **kwargs):
    t0 = time.time()
    ret_vals = f(*args, **kwargs)
    delta_t = time.time() - t0
    print(f.__name__ + ' took ' + str(delta_t) + ' seconds')
    return ret_vals


class Worker(QtCore.QRunnable):
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