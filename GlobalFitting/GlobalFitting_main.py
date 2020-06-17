import sys
import csv
import numpy as np
import seaborn
from math import log10, floor, pi
from decimal import Decimal

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

from main_window_ui import Ui_MainWindow  # importing our generated file
import fit_params_window
import preferences_window_ui

import pandas as pd
import scipy
from scipy.optimize import curve_fit, leastsq, least_squares
import matplotlib

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT, FigureCanvasQTAgg


import matplotlib.colors as colors

# Things that should go in a preferences section:
# 1. Padding the axis or not
# 2. Selecting which axis is time vs wavelength
# 3. Figure details
# 4. Add the option of global optimization
# 5. Alternative global fitting methods?

#TODO
# To do Items:
# 1. Random guesses
# 2. Statistics
# 3. Use output of pseudolinear in fully nonlinear fitting
# 4. Add a description to the help button
# 9. Add DAS and EAS
# 10. Figure settings
# 11. Add colorbar
# 12. Get rounding to actually be in terms of sig figs
# 13. Select region of interest or exclusion

# def round_to_4(unrounded_value, limiting_exponent):
#     """"""
#     return round(unrounded_value, (limiting_exponent-int(floor(log10(abs(unrounded_value))))))


def format_values(input_value, num_decimals, limiting_exponent):
    """"""
    num_decimals = num_decimals
    input_value = float(input_value)
    if input_value > (10**limiting_exponent - 1) or input_value < (10**(-limiting_exponent)):
        format_string = r'%.' + str(num_decimals) + 'E'
        reformatted_value = format_string % Decimal(str(input_value))
    else:
        reformatted_value = str(round(input_value, num_decimals))

    return reformatted_value


def exp_fit_func(taus, times, data, num_times, num_terms):
    taus = np.array(taus)
    print('taus - ' + str(taus))
    num_taus = len(taus)
    time_dependence_matrix = np.zeros((num_times, num_terms))  # These either have to be from an object or fed as args

    for ii in range(0, num_taus):
        tau = taus[ii]
        time_dependence_matrix[:, ii] = np.exp(-times / tau)

    print('shape t-dep ' + str(time_dependence_matrix.shape))
    print('failed right after loop')
    A = time_dependence_matrix
    ATb = np.matmul(A.transpose(), data)
    try:
        ATA_inv = np.linalg.inv(np.matmul(A.transpose(), A))
        print('after ATA_inv')
        x_mat = np.matmul(ATA_inv, ATb)
        fit_func = np.matmul(A, x_mat)
        print('made it nearly to the end')
    except scipy.linalg.LinAlgError as error_details:
        error_message_window(text='Fit Failed', inform_text='During Linear Algebra', details=str(sys.exc_info()[:]))
        fit_func = None
    except Exception as error_details:
        error_message_window(text='Fit Failed', inform_text='During Linear Algebra', details=str(sys.exc_info()[:]))
        fit_func = None

    return fit_func


def error_message_window(text, inform_text, details):
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


def pseudo_linear(taus, times, data, num_times, num_terms):

    fit_func = exp_fit_func(taus, times, data, num_times, num_terms)   # returns None if exception occurs

    if fit_func is None:
        err_vec = None
    else:
        err_mat = fit_func - data
        err_vec = np.ravel(err_mat, order='F')

    return err_vec


def exp_model(x, params, num_exps, offset=False):

    amplitudes = np.zeros(num_exps)
    taus = np.zeros(num_exps)

    if offset is False:
        model = 0
    else:
        model = params[len(params) - 1]
        # Is this right?

    for ii in range(0, num_exps):

        taus[ii] = params[ii]
        amplitudes[ii] = params[ii + num_exps]

        model = model + amplitudes[ii] * np.exp(-x / taus[ii])

    return model


def get_initial_params(fit_model, num_terms, user_guesses, num_wls, offset=False):   # input user guesses as a list
    """ gets global parameters (taus are shared) """
    print('user guesses - ' + str(type(user_guesses)))
    print('user guesses - ' + str(user_guesses))
    # I want taus first since they are shared by all of the wavelengths
    p = np.ones(num_terms * (1 + num_wls))  # All the A values need to be independent (+1 is for the taus)

    # Replace the tau values so that they are not independent
    if fit_model == 'Exponential':
        for ii in range(0, len(user_guesses)):
            print(str(ii))
            p[ii] = user_guesses[ii]
        else:
            pass

    if offset is True:
        offset_guesses = np.ones(num_wls)
        p = np.concatenate(p, offset_guesses)
    print('p length - ' + str(len(p)))
        # Output - single vector with taus first, then As (ordered by term number then wavelength), then Cs (wl ordered)
    return p


def err_single_wl(params, x, y, num_exps, fit_model):    #num_exps may not be needed since it can be inferred from len(params)

    if fit_model == 'Exponential':                                  # What's the best way to incorporate the offset?
        err_results = exp_model(x, params, num_exps) - y

    elif fit_model == 'Gaussian Modified Exponential':
        print('Model Not incorporated yet')
        return
    else:
        print('Model Not Incorporated - Else')
        return

    return err_results


def err_global(p_global, x, fit_type, num_terms, include_offset=False):       # num_params is per wavelength trace
    num_wls = len(application.wavelengths)
    num_times = len(x)

    err_all_wls = np.zeros((num_times, num_wls))
    if fit_type == 'Exponential' and include_offset is False:
        num_params = num_terms * 2
        # print(str(num_params))
        params_1wl = np.ones((num_wls, num_params))
        # print('params 1wl' + str(params_1wl.shape))
        for ii in range(0, num_wls):
            for jj in range(0, num_terms):
                params_1wl[ii, jj] = p_global[jj]       # the first few terms are taus, don't depend on wl (ii)
                params_1wl[ii, jj + num_terms] = p_global[jj + num_terms * (ii + 1)]
                                                        # constant offset is not going to work yet

            err_all_wls[:, ii] = err_single_wl(params_1wl[ii, :], x, application.data_values[:, ii], num_terms, fit_type)

    err_all_wls = err_all_wls.transpose()  # I want each kinetic trace before the next (though it may not matter)
    new_length = num_wls * num_times
    err_global_vectorized = np.reshape(err_all_wls, new_length)
    return err_global_vectorized


def reconstruct_2d_data(fit_model, num_terms, params, x, y, include_offset):
    tau = np.zeros(num_terms)
    amp = np.zeros(len(params) - num_terms)

    if fit_model == 'Exponential' and include_offset is False:
        # parse parameters:
        for ii in range(0, num_terms):
            tau[ii] = params[ii]

        for ii in range(0, len(params) - num_terms):
            amp[ii] = params[ii + num_terms]

        amplitudes = np.reshape(amp, (len(y), num_terms))
        rec_data = np.empty((len(x), len(y)))
        new_params = np.empty((len(y), num_terms * 2))

        for ii in range(0, len(y)):
            new_params[ii, :] = np.concatenate((tau, amplitudes[ii, :]))
            rec_data[:, ii] = exp_model(x, new_params[ii, :], num_terms, include_offset)

    else:
        print('Other models not yet supported')
        return

    return rec_data


def fit_data_nlsq(fit_model, data_x, num_terms, user_guesses, num_wls, include_offset=False, *args, **kwargs):
    params_global = get_initial_params(fit_model, num_terms, user_guesses, num_wls)     # A vector of all the parameters
    try:
        params_best, ier = leastsq(err_global, params_global, args=(data_x, fit_model, num_terms, include_offset))
    except Exception as error_details:
        error_message_window(text='Fit Failed:', inform_text='Unsure why', details=str(error_details))

    print('Fitting Completed')
    print(str(params_best[0:num_terms]))          # This will not be correct later on but for the exponential case it is
    reconstructed_data = reconstruct_2d_data(fit_model, num_terms, params_best, data_x, application.wavelengths, include_offset)
    return params_best, ier, reconstructed_data


def fit_data_pseudolinear(fit_model, data_x, num_terms, user_guesses,  num_wls, bounds=None, include_offset=False, *args, **kwargs):
    guesses = np.array(user_guesses)

    print('got in to fit_data_pseudolinear')
    num_times = len(data_x)
    try:
        x_res = least_squares(pseudo_linear, guesses, bounds=bounds, args=(data_x, application.data_values, num_times, num_terms))
        print('Solutions Found - ' + str(x_res.x))
    except Exception as error_details:
        error_message_window(text='Fit Failed:', inform_text='During Matrix Inversion', details=str(error_details))
        print(str(error_details))
        x_res = None

    return x_res


class Preferences:
    def __init__(self):
        self.num_decimals = 4
        self.limiting_exponent = 4
        self.scaling = 'linear'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.addToolBar(NavigationToolbar2QT(self.ui.MplWidget.canvas, self), )
        self.ui.log_scaling_checkbox.setCheckState(QtCore.Qt.Unchecked)

        self.num_decimals = 4
        self.limiting_exponent = 4

        self.wavelength_axis = 'rows'
        self.time_axis = 'columns'   # This should be adjustable outside the code to handle various types of data

        self.rows_values = 0        # the intention is that the values for "time" are in row 0 and wl are in column 0
        self.columns_values = 0     # These might be stupid names and unnecessary in general

        self.plot_full = dict(Left=False, Right=False, Lower=False)

    @QtCore.pyqtSlot(int)
    def log_scaling_cb_state_changed(self, state):
        if state == 2:
            prefs.scaling = 'log'
        elif state == 0:
            prefs.scaling = 'linear'

        if self.plot_full['Left']:
            self.ui.MplWidget.canvas.axes_left.set_yscale(prefs.scaling)
        if self.plot_full['Right']:
            self.ui.MplWidget.canvas.axes_right.set_yscale(prefs.scaling)
        if self.plot_full['Lower']:
            self.ui.MplWidget.canvas.axes_lower.set_yscale(prefs.scaling)
        if self.plot_full['Left'] or self.plot_full['Right'] or self.plot_full['Lower']:
            self.ui.MplWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def load_btn_clicked(self):
        load_file_name, _ = QFileDialog.getOpenFileName(self, 'Load File')

        # If the user doesn't cancel
        if load_file_name != '':
            data_frame = pd.read_csv(load_file_name, delimiter='\t', header=None)

            full_contents = data_frame.to_numpy()
            row_ct, col_ct = full_contents.shape
            self.times = full_contents[0, 1:col_ct]
            self.wavelengths = full_contents[1:row_ct, 0]
            data = full_contents[1:row_ct, 1:col_ct]
            self.data_values = np.transpose(data)

            self.ui.MplWidget.canvas.axes_right.clear()
            self.ui.MplWidget.canvas.axes_lower.clear()
            self.update_surf_plot(x=self.wavelengths, y=self.times, z=self.data_values, side='Left')

    def help_btn_clicked(self):
        print('Does nothing at this time, see read-me file for some information')

    @QtCore.pyqtSlot()
    def clear_btn_clicked(self):
        self.ui.MplWidget.canvas.axes_left.clear()
        self.ui.MplWidget.canvas.axes_right.clear()
        self.ui.MplWidget.canvas.axes_lower.clear()

    @QtCore.pyqtSlot()
    def fit_btn_clicked(self):
        self.OpenFitWindow = FitWindow()
        self.OpenFitWindow.show()

    @QtCore.pyqtSlot()
    def prefs_btn_clicked(self):
        self.PrefsWindow = PreferencesWindow()
        self.PrefsWindow.show()

    def update_surf_plot(self, x=None, y=None, z=None, pad_axes=True, side='Left'):  # , clear=False, label=None):
        if pad_axes is True:
            x_ct = len(x)
            y_ct = len(y)
            delta_x = x[x_ct - 1] - x[x_ct - 2]
            delta_y = y[y_ct - 1] - y[y_ct - 2]
            x = np.append(x, (x[x_ct - 1] + delta_x))
            y = np.append(y, (y[y_ct - 1] + delta_y))

        divnorm = colors.DivergingNorm(vcenter=0)
        if side == 'Left':
            self.ui.MplWidget.canvas.axes_left.clear()
            self.ui.MplWidget.canvas.axes_left.pcolormesh(x, y, z, norm=divnorm, cmap='bwr')
            if prefs.scaling == 'log':
                self.ui.MplWidget.canvas.axes_left.set_yscale('log')

        elif side == 'Right':
            self.ui.MplWidget.canvas.axes_right.clear()
            self.ui.MplWidget.canvas.axes_right.pcolormesh(x, y, z, norm=divnorm, cmap='bwr')
            if prefs.scaling == 'log':
                self.ui.MplWidget.canvas.axes_right.set_yscale('log')

        elif side == 'Lower':
            self.ui.MplWidget.canvas.axes_lower.clear()
            self.ui.MplWidget.canvas.axes_lower.pcolormesh(x, y, z, norm=divnorm, cmap='bwr')
            if prefs.scaling == 'log':
                self.ui.MplWidget.canvas.axes_left.set_yscale('log')

        print('side: ' + side)
        self.plot_full[side] = True
        print('plot_full: ' + str(self.plot_full))
        self.ui.MplWidget.canvas.draw()


class FitWindow(QtWidgets.QWidget):
    def __init__(self):
        super(FitWindow, self).__init__()
        self.ui_params_form = fit_params_window.Ui_Form()
        self.ui_params_form.setupUi(self)

        self.fit_model = 'Exponential'
        self.num_terms = 1
        self.fit_method = 'Pseudolinear'

        rowPos = self.ui_params_form.parameters_table.rowCount()
        self.ui_params_form.parameters_table.insertRow(rowPos)
        self.ui_params_form.parameters_table.setItem(rowPos, 0, QtWidgets.QTableWidgetItem("tau_1"))
        self.ui_params_form.parameters_table.setItem(rowPos, 1, QtWidgets.QTableWidgetItem("1"))
        self.ui_params_form.parameters_table.setItem(rowPos, 2, QtWidgets.QTableWidgetItem("0"))
        self.ui_params_form.parameters_table.setItem(rowPos, 3, QtWidgets.QTableWidgetItem("Inf"))

    @QtCore.pyqtSlot(str)
    def fit_method_selected(self, method):
        self.fit_method = method

    @QtCore.pyqtSlot(str)
    def fit_model_selected(self, model):
        print(model)
        self.fit_model = model

    @QtCore.pyqtSlot(int)
    def number_terms_changed(self, num_terms):
        self.num_terms = num_terms
        self.update_table()

    @QtCore.pyqtSlot()
    def done_btn_clicked(self):
        self.get_user_guesses()

    @QtCore.pyqtSlot()
    def apply_btn_clicked(self):
        include_offset = self.ui_params_form.offset_checkbox.isChecked()
        if include_offset:
            print('include_offset is true')
        guesses_are_valid, user_guesses, lower_bounds, upper_bounds = self.get_user_entries()

        # Check that the user_guesses are not all identical
        for ii in range(0, len(user_guesses)):
            for jj in range(0, len(user_guesses)):
                if (user_guesses[ii] == user_guesses[jj]) and (ii != jj):
                    print('guesses are equal, fit aborted')
                    text = 'Guesses cannot be identical - '
                    inform_text = 'Change initial fit parameters to remove identical guesses'
                    details = ''
                    error_message_window(text, inform_text, details)
                    return

        # Prepare the bounds
        lower_bounds = np.array(lower_bounds)
        upper_bounds = np.array(upper_bounds)
        bounds = tuple((lower_bounds, upper_bounds))
        user_bounds = bounds
        num_wls = len(application.wavelengths)

        if guesses_are_valid:
            if self.fit_method == 'Pseudolinear':
                num_times = len(application.times)

                solution = fit_data_pseudolinear(self.fit_model, application.times, self.num_terms, user_guesses, num_wls,
                                                 bounds=user_bounds, include_offset=include_offset)
                if solution is None:
                    return
                else:
                    reconstr_data = exp_fit_func(solution.x, application.times, application.data_values, num_times, self.num_terms)
                    residual_data = application.data_values - reconstr_data

                    reformatted_solution = list()
                    for ii in range(0, len(solution.x)):
                        # Format Solutions
                        reformatted_solution.append(format_values(solution.x[ii], prefs.num_decimals,
                                                                  prefs.limiting_exponent))
                        # self.ui_params_form.parameters_table.setItem(ii, 4, QtWidgets.QTableWidgetItem(str(solution.x[ii])))
                        self.ui_params_form.parameters_table.setItem(ii, 4,
                                                                     QtWidgets.QTableWidgetItem(str(reformatted_solution[ii])))

            elif self.fit_method == 'NLSQ':
                fit_parameters, ier, reconstr_data = fit_data_nlsq(self.fit_model, application.times, self.num_terms,
                                                            user_guesses, num_wls, include_offset)
                print('Fit Parameters found: ' + str(fit_parameters))
                print('ier: ' + str(ier) + '  - (success is 1,2, 3, or 4)')
                residual_data = application.data_values - reconstr_data
            else:
                return

            application.update_surf_plot(application.wavelengths, application.times, reconstr_data,
                                         pad_axes=True, side='Right')
            application.update_surf_plot(application.wavelengths, application.times, residual_data,
                                         pad_axes=True, side='Lower')
        else:
            text = 'All Fields Must Be Numeric'
            inform_text = 'For no bounds use ''-Inf'' and ''Inf'''
            error_message_window(text=text, inform_text=inform_text, details=None)


# fit_model, num_terms, data_x, user_guesses, num_wls, include_offset=False, *args, **kwargs):
    @QtCore.pyqtSlot()
    def offset_cb_toggled(self):
        pass

    # -------------------- non slot methods ------------------------------------------
    def update_table(self):
        if self.fit_model == 'Exponential':
            row_pos = self.ui_params_form.parameters_table.rowCount()
            while row_pos < self.num_terms:
                self.ui_params_form.parameters_table.insertRow(row_pos)
                self.ui_params_form.parameters_table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem("tau_" + str(row_pos + 1)))
                guess_val = str(10**row_pos)
                self.ui_params_form.parameters_table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(guess_val))
                self.ui_params_form.parameters_table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem("0"))
                self.ui_params_form.parameters_table.setItem(row_pos, 3, QtWidgets.QTableWidgetItem("Inf"))
                row_pos += 1
            while row_pos > self.num_terms:
                self.ui_params_form.parameters_table.removeRow(row_pos - 1)
                row_pos -= 1
        elif self.fit_model == 'Gaussian Modified Exponential':
            print('this model has not been incorporated yet')
            return
        else:
            print('model unincorporated')
            return

    def get_user_entries(self):
        guesses_are_valid = True
        guesses = []
        lower_bounds = []
        upper_bounds = []
        for ii in range(0, self.num_terms):
            print('in get__user_entries')
            tmp = self.ui_params_form.parameters_table.item(ii, 1).text()
            if tmp == 'Inf' or tmp == 'inf':
                tmp = np.inf
            elif tmp == '-Inf' or tmp == '-inf':
                tmp = -np.inf
            elif not tmp.isnumeric():
                print('got inside the nonnumeric case - guesses')
                guesses_are_valid = False
            else:
                tmp = float(tmp)
            guesses.append(tmp)

            tmp2 = self.ui_params_form.parameters_table.item(ii, 2).text()
            if tmp2 == 'Inf' or tmp2 == 'inf':
                tmp2 = np.inf
            elif tmp2 == '-Inf' or tmp2 == '-inf':
                tmp2 = -np.inf
            elif not tmp2.isnumeric():
                print('got inside the nonnumeric case - lower_bounds')
                guesses_are_valid = False
            else:
                tmp2 = float(tmp2)
            lower_bounds.append(tmp2)

            tmp3 = self.ui_params_form.parameters_table.item(ii, 3).text()
            print('type tmp3: ' + str(type(tmp3)))
            if tmp3 == 'Inf' or tmp3 == 'inf':
                tmp3 = np.inf
            elif tmp3 == '-Inf' or tmp3 == '-inf':
                tmp3 = -np.inf
            elif not tmp3.isnumeric():
                print('got inside the nonnumeric case - upper_bounds')
                guesses_are_valid = False
            else:
                tmp3 = float(tmp3)
            upper_bounds.append(tmp3)

        print('finished get user entries')
        return guesses_are_valid, guesses, lower_bounds, upper_bounds


class PreferencesWindow(QtWidgets.QWidget):
    def __init__(self):
        super(PreferencesWindow, self).__init__()
        self.ui_prefs_form = preferences_window_ui.Ui_Form()
        self.ui_prefs_form.setupUi(self)

        self.ui_prefs_form.scientific_notation_spinner.setValue(prefs.limiting_exponent)
        self.ui_prefs_form.sig_figs_spinner.setValue(prefs.num_decimals)


    @QtCore.pyqtSlot(int)
    def scientific_notation_limit_changed(self, limit_value):
        prefs.limiting_exponent = limit_value

    @QtCore.pyqtSlot(int)
    def sig_fig_spinner_value_changed(self, spinner_value):
        prefs.num_decimals = spinner_value


prefs = Preferences()

app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
