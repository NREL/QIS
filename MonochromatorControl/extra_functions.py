from math import log10, floor, pi
from decimal import Decimal

def round_to_4(unrounded_value):
    """"""
    return round(unrounded_value, 3-int(floor(log10(abs(unrounded_value)))))

def format_scientific(input_value):
    """"""
    input_value = float(input_value)
    if input_value > 9999 or input_value < 0.01:
        reformatted_value = '%.4E' % Decimal(str(input_value))
    else:
        reformatted_value = str(input_value)

    return reformatted_value

def check_for_zeros_n_empties(func):
    def wrapper(*args):
        result = func(*args)
        result = str(result)
        for arg in args:
            if type(arg) == str:
                if arg == '':
                    result = ''
            elif type(arg) == float or type(arg) == int:
                if arg == 0:
                    result = ''
        return result
    return wrapper

