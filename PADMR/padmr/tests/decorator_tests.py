from PyQt5 import QtCore
from decorator import decorator
import time


@decorator
def measure_time(f, *args, **kwargs):
    t0 = time.time()
    ret_val = f(*args, **kwargs)
    delta_t = time.time() - t0
    print(f.__name__ + ' took ' + str(delta_t) + ' seconds')
    print(ret_val)
    print(type(ret_val))
    return ret_val

@measure_time
def fn_to_test():
    for ii in range(0, 1000):
        x = ii ** ii
        y = ii * ii
    return x, y

