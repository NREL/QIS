import os
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore

from FullControl.settings_window_ui import Ui_Form as Settings_Ui_Form
from FullControl import led_icons_rc

#TODO:
# 1. Split "initialize_settings_window" to create also an "update_settings_window"
# 2. Remove all the unnecessary "bools" from the signals (c.f. connect_instr_signal, which works fine)
# 3. Get rid of the silly "set_tab" and "set_all_tabs". Only with the lock-in would you want to change a lot at once
pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))


class SettingsWindowForm(QWidget):
    update_all_signal = QtCore.pyqtSignal(bool)
    update_tab_signal = QtCore.pyqtSignal(int)

    test_signal = QtCore.pyqtSignal(str)
    cg635_set_phase_signal = QtCore.pyqtSignal(bool)  # Do I need the bools here?
    cg635_zero_phase_signal = QtCore.pyqtSignal(bool)
    cg635_set_freq_signal = QtCore.pyqtSignal(float)    # Done
    cg635_freq_units_changed_signal = QtCore.pyqtSignal(int)
    cg635_check_errors_signal = QtCore.pyqtSignal(bool)
    cg635_manual_cmd_write_signal = QtCore.pyqtSignal(str)

    toptica_enable_signal = QtCore.pyqtSignal()
    toptica_start_signal = QtCore.pyqtSignal()
    toptica_stop_signal = QtCore.pyqtSignal()

    connect_instr_signal = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SettingsWindowForm, self).__init__(*args, **kwargs)

        self.sr844_sens_list = ['100 nV', '300 nV', '1 µV', '3 µV', '10 µV', '30 µV', '100 µV', '300 µV',
                                '1 mV', '3 mV', '10 mV', '30 mV', '100 mV', '300 mV', '1 V']

        self.sr844_tc_list = ['100 µs', '300 µs', '1 ms', '3 ms', '10 ms', '30 ms', '100 ms', '300 ms', '1 s',
                              '3 s', '10 s', '30 s', '100 s', '300 s', '1 ks', '3 ks', '10 ks', '30 ks']

        self.sr830_sens_list = ['2 nV', '5 nV', '10 nV', '20 nV', '50 nV', '100 nV', '200 nV', '500 nV', '1 µV',
                                '2 µV', '5 µV', '10 µV', '20 µV', '50 µV', '100 µV', '200 µV', '500 µV', '1 mV',
                                '2 mV', '5 mV', '10 mV', '20 mV', '50 mV', '100 mV', '200 mV', '500 mV', '1 V']

        self.sr830_tc_list = ['10 µs', '30 µs', '100 µs', '300 µs', '1 ms', '3 ms', '10 ms', '30 ms', '100 ms',
                              '300 ms', '1 s', '3 s', '10 s', '30 s', '100 s', '300 s', '1 ks', '3 ks', '10 ks',
                              '30 ks']

        self.sr844_slope_list = ['No Filter', '6 dB/Oct', '12 dB/Oct', '18 dB/Oct', '24 dB/Oct']

        self.sr830_slope_list = ['6 dB/Oct', '12 dB/Oct', '18 dB/Oct', '24 dB/Oct']

        # Load the ui.py file and prepare the UI
        self.ui = Settings_Ui_Form()
        self.ui.setupUi(self)

        self.ui.tab_widget.setCurrentIndex(0)

        self.read_ini_file()

        if '0' in self.relevant_instruments:
            self.ui.sr844_checkbox.setChecked(True)
        if '1' in self.relevant_instruments:
            self.ui.sr830_checkbox.setChecked(True)
        if '2' in self.relevant_instruments:
            self.ui.md2000_checkbox.setChecked(True)
        if '3' in self.relevant_instruments:
            self.ui.cg635_checkbox.setChecked(True)
        if '4' in self.relevant_instruments:
            self.ui.smb100a_checkbox.setChecked(True)
        if '5' in self.relevant_instruments:
            self.ui.montana_instr_checkbox.setChecked(True)
        if '6' in self.relevant_instruments:
            self.ui.toptica_checkbox.setChecked(True)

        self.initialize_settings_window()

    def read_ini_file(self):
        #TODO:
        # Change Refout To separate harmonic mode and internal/external options for the SR844

        ini_file_object = open(r'initialization_parameters.ini', 'r')
        param_lines = ini_file_object.readlines()
        print('attempting to read initialization file')

        # General Settings
        self.relevant_instruments = param_lines[1].split('#')[0].split()[2].split(',')
        self.prologix_com_port = param_lines[2].split('#')[0].split()[2]
        self.lockin_model_preference = param_lines[3].split('#')[0].split()[2]
        print(self.lockin_model_preference)
        print("prologix com port: " + str(self.prologix_com_port))

        # SR844 Settings
        self.sr844_gpib_address = int(param_lines[20].split('#')[0].split()[2])
        self.sr844_outputs = int(param_lines[21].split('#')[0].split()[2])
        self.sr844_sensitivity = int(param_lines[22].split('#')[0].split()[2])
        self.sr844_filter_slope = int(param_lines[23].split('#')[0].split()[2])
        self.sr844_time_constant = int(param_lines[24].split('#')[0].split()[2])
        self.sr844_wide_reserve = int(param_lines[25].split('#')[0].split()[2])
        self.sr844_close_reserve = int(param_lines[26].split('#')[0].split()[2])
        self.sr844_sampling_rate = int(param_lines[27].split('#')[0].split()[2])
        self.sr844_input_impedance = int(param_lines[28].split('#')[0].split()[2])
        self.sr844_ref_impedance = int(param_lines[29].split('#')[0].split()[2])
        self.sr844_ref_source = int(param_lines[30].split('#')[0].split()[2])
        self.sr844_harmonic = int(param_lines[31].split('#')[0].split()[2])
        self.sr844_expand = int(param_lines[32].split('#')[0].split()[2])

        # SR830 Settings
        self.sr830_gpib_address = int(param_lines[40].split('#')[0].split()[2])
        self.sr830_outputs = int(param_lines[41].split('#')[0].split()[2])
        self.sr830_sensitivity = int(param_lines[42].split('#')[0].split()[2])
        self.sr830_filter_slope = int(param_lines[43].split('#')[0].split()[2])
        self.sr830_time_constant = int(param_lines[44].split('#')[0].split()[2])
        self.sr830_dyn_reserve_mode = int(param_lines[45].split('#')[0].split()[2])
        self.sr830_sampling_rate = int(param_lines[46].split('#')[0].split()[2])
        self.sr830_ref_source = int(param_lines[47].split('#')[0].split()[2])
        self.sr830_harmonic_mode = int(param_lines[48].split('#')[0].split()[2])

        # Mono Settings
        self.mono_resource_name = param_lines[60].split('#')[0].split()[2]
        self.mono_groove_density = int(param_lines[61].split('#')[0].split()[2])
        self.mono_home_wavelength = float(param_lines[62].split('#')[0].split()[2])

        # CG635 Settings
        self.cg635_com_format = int(param_lines[70].split('#')[0].split()[2])
        self.cg635_resource_name = param_lines[71].split('#')[0].split()[2]
        self.cg635_gpib_address = int(param_lines[72].split('#')[0].split()[2])
        self.cg635_freq_units = int(param_lines[73].split('#')[0].split()[2])
        self.cg635_max_freq = int(param_lines[74].split('#')[0].split()[2])

        # Toptica Settings
        self.toptica_com_port = param_lines[100].split('#')[0].split()[2]

        print('CG635 Com Format: ' + str(self.cg635_com_format))
        print('toptica com_port: ' + str(self.toptica_com_port))

    def initialize_settings_window(self):
        # Initialize the general tab
        self.grn_led_str = "<html><head/><body><p><img src=\":/led_icons/GREEN_LED_ON.png\"/></p></body></html>"
        self.red_led_str = "<html><head/><body><p><img src=\":/led_icons/RED_LED_ON.png\"/></p></body></html>"
        self.off_led_str = "<html><head/><body><p><img src=\":/led_icons/RED_LED_OFF.png\"/></p></body></html>"

        self.laser_off_str = "<html><head/><body><p><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "<img src=\":/led_icons/RED_LED_OFF.png\"/><img src=\":/led_icons/RED_LED_OFF.png\"/>" \
                             "</p><p>laser OFF</p></body></html>"

        self.laser_on_str = "<html><head/><body><p><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "<img src=\":/led_icons/RED_LED_ON.png\"/><img src=\":/led_icons/RED_LED_ON.png\"/>" \
                            "</p><p> ! LASER ON ! </p></body></html>"

        self.ui.status_ind_cg635.setText(self.off_led_str)
        self.ui.status_ind_sr830.setText(self.off_led_str)
        self.ui.status_ind_sr844.setText(self.off_led_str)
        self.ui.status_ind_cryostat.setText(self.off_led_str)
        self.ui.status_ind_md2000.setText(self.off_led_str)
        self.ui.status_ind_toptica.setText(self.off_led_str)
        self.ui.status_ind_smb100a.setText(self.off_led_str)


        # Initialize the lock-in tab
        print('----------------------------------Initializing the lock-in Tab-----------------------------------------')
        gpib_address = int(self.sr844_gpib_address)
        self.ui.sr844_gpib_address_spinner.setValue(gpib_address)

        gpib_address = int(self.sr830_gpib_address)
        self.ui.sr830_gpib_address_spinner.setValue(gpib_address)

        self.ui.lockin_model_lineedit.setDisabled(True)
        try:
            if self.lockin_model_preference == 'SR844':
                self.ui.lockin_model_lineedit.setText('SR844 (25 kHz - 200 MHz)')
                self.ui.sr844_checkbox.setChecked(True)
                self.ui.sr830_checkbox.setChecked(False)

                self.ui.sr844_gpib_address_spinner.setDisabled(False)
                self.ui.sr830_gpib_address_spinner.setDisabled(True)
                self.ui.wide_reserve_combobox.setDisabled(False)
                self.ui.close_reserve_combobox.setDisabled(False)
                self.ui.dynamic_reserve_combobox.setDisabled(True)
                self.ui.ref_impedance_combobox.setDisabled(False)
                self.ui.input_impedance_combobox.setDisabled(False)
                self.ui.harmonic_spinner.setDisabled(True)
                self.ui.sr844_harmonic_combobox.setDisabled(False)
                print('(en)(dis)abling done')

                # print('lockin model pref was SR844')
                # self.ui.lockin_model_combobox.setCurrentIndex(0)

                com_number = int(self.prologix_com_port.split('L')[1].split(':')[0])
                self.ui.prologix_com_port_spinner.setValue(com_number)

                print('first set done')
                self.ui.outputs_combobox.setCurrentIndex(self.sr844_outputs)

                # Sensitivity
                self.ui.sensitivity_combobox.clear()
                self.ui.sensitivity_combobox.addItems(self.sr844_sens_list)
                self.ui.sensitivity_combobox.setCurrentIndex(self.sr844_sensitivity)
                #Time Constant
                self.ui.time_constant_combobox.clear()
                self.ui.time_constant_combobox.addItems(self.sr844_tc_list)
                self.ui.time_constant_combobox.setCurrentIndex(self.sr844_time_constant)
                # Filter Slope
                self.ui.filter_slope_combobox.clear()
                self.ui.filter_slope_combobox.addItems(self.sr844_slope_list)
                self.ui.filter_slope_combobox.setCurrentIndex(self.sr844_filter_slope)

                self.ui.wide_reserve_combobox.setCurrentIndex(self.sr844_wide_reserve)
                print('second set done')
                self.ui.close_reserve_combobox.setCurrentIndex(self.sr844_close_reserve)
                self.ui.sampling_rate_combobox.setCurrentIndex(self.sr844_sampling_rate)
                self.ui.input_impedance_combobox.setCurrentIndex(self.sr844_input_impedance)
                self.ui.ref_impedance_combobox.setCurrentIndex(self.sr844_ref_impedance)
                self.ui.ref_source_combobox.setCurrentIndex(self.sr844_ref_source)
                self.ui.sr844_harmonic_combobox.setCurrentIndex(self.sr844_harmonic)
                self.ui.expand_combobox.setCurrentIndex(self.sr844_expand)

            elif self.lockin_model_preference == 'SR830':
                self.ui.lockin_model_lineedit.setText('SR830 (1 mHz - 102 kHz)')
                self.ui.sr830_checkbox.setChecked(True)
                self.ui.sr844_checkbox.setChecked(False)

                self.ui.sr844_gpib_address_spinner.setDisabled(True)
                self.ui.sr830_gpib_address_spinner.setDisabled(False)
                self.ui.wide_reserve_combobox.setDisabled(True)
                self.ui.close_reserve_combobox.setDisabled(True)
                self.ui.dynamic_reserve_combobox.setDisabled(False)
                self.ui.ref_impedance_combobox.setDisabled(True)
                self.ui.input_impedance_combobox.setDisabled(True)
                self.ui.harmonic_spinner.setDisabled(False)
                self.ui.sr844_harmonic_combobox.setDisabled(True)

                print('(en)(dis)abling done')

                # print('lockin model pref was SR830')
                # self.ui.lockin_model_combobox.setCurrentIndex(1)

                com_number = int(self.prologix_com_port.split('L')[1].split(':')[0])
                self.ui.prologix_com_port_spinner.setValue(com_number)

                print('first set done')
                self.ui.outputs_combobox.setCurrentIndex(self.sr830_outputs)
                # Sensitivity
                self.ui.sensitivity_combobox.clear()
                self.ui.sensitivity_combobox.addItems(self.sr830_sens_list)
                self.ui.sensitivity_combobox.setCurrentIndex(self.sr830_sensitivity)
                # Time Constant
                self.ui.time_constant_combobox.clear()
                self.ui.time_constant_combobox.addItems(self.sr830_tc_list)
                self.ui.time_constant_combobox.setCurrentIndex(self.sr830_time_constant)
                # Filter Slope
                self.ui.filter_slope_combobox.clear()
                self.ui.filter_slope_combobox.addItems(self.sr830_slope_list)
                self.ui.filter_slope_combobox.setCurrentIndex(self.sr830_filter_slope)

                self.ui.dynamic_reserve_combobox.setCurrentIndex(self.sr830_dyn_reserve_mode)

                self.ui.sampling_rate_combobox.setCurrentIndex(self.sr830_sampling_rate)
                self.ui.ref_source_combobox.setCurrentIndex(self.sr830_ref_source)
                self.ui.harmonic_spinner.setValue(self.sr830_harmonic_mode)

            # self.lockin_model_changed()
            print('----------------------------------Initializing the cg635 Tab---------------------------------------')
            self.ui.cg635_comm_format_combobox.setCurrentIndex(self.cg635_com_format)
            self.ui.cg635_gpib_spinner.setValue(self.cg635_gpib_address)
            self.ui.cg635_freq_units_combobox.setCurrentIndex(self.cg635_freq_units)
        except ValueError:
            print('.ini file inconsistent with expectations')
            print(str(sys.exc_info()[:]))

    @QtCore.pyqtSlot()
    def connect_instr_btn_clicked(self):
        print('Emitting Signal to connect instruments')
        self.connect_instr_signal.emit()

    @QtCore.pyqtSlot(str, int)
    def instrument_status_changed(self, which_instrument, new_status):
        """
        status=0/1/2 for off/connected/error.
        which_instrument = 'sr844'/'sr830'/'cg635'/'cryostat'/'smb100a'/'md2000'/'toptica'
        """
        # Decide which string is needed to make change
        if new_status == 0:
            text_str = self.off_led_str
        elif new_status == 1:
            text_str = self.grn_led_str
        elif new_status == 2:
            text_str = self.red_led_str
        else:
            print('INVALID ICON STRING')

        # Decide which instrument indicator to change
        if which_instrument == 'cg635':
            self.ui.status_ind_cg635.setText(text_str)
        elif which_instrument == 'sr844':
            self.ui.status_ind_sr844.setText(text_str)
        elif which_instrument == 'sr830':
            self.ui.status_ind_sr830.setText(text_str)
        elif which_instrument == 'md2000':
            self.ui.status_ind_md2000.setText(text_str)
        elif which_instrument == 'cryostat':
            self.ui.status_ind_cryostat.setText(text_str)
        elif which_instrument == 'toptica':
            self.ui.status_ind_toptica.setText(text_str)
        elif which_instrument == 'smb100a':
            self.ui.status_ind_smb100a.setText(text_str)

    @QtCore.pyqtSlot()
    def toptica_start_btn_clicked(self):
        print('------------------------------------ STARTING LASER EMISSION ------------------------------------------')
        self.ui.toptica_emission_indicator.setText(self.laser_on_str)
        self.toptica_start_signal.emit()
        print('ATM, button does not engage laser')

    @QtCore.pyqtSlot()
    def toptica_bias_enable_btn_clicked(self):
        print('------------------------------------ STARTING LASER EMISSION ------------------------------------------')
        self.ui.toptica_emission_indicator.setText(self.laser_on_str)
        self.toptica_enable_signal.emit()
        print('ATM, button does not engage laser')

    @QtCore.pyqtSlot()
    def toptica_stop_btn_clicked(self):
        print('------------------------------------ STOPPING LASER EMISSION ------------------------------------------')
        self.ui.toptica_emission_indicator.setText(self.laser_off_str)
        self.toptica_stop_signal.emit()
        print('ATM, button does not engage laser')

    @QtCore.pyqtSlot()
    def toptica_set_bias_power_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def toptica_set_main_power_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def toptica_ext_en_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def cg635_write_manual_cmd_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def cg635_set_phase_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def cg635_set_freq_btn_clicked(self):
        freq_to_set = self.ui.cg635_set_freq_spinner.value()
        self.cg635_set_freq_signal.emit(freq_to_set)

    @QtCore.pyqtSlot()
    def cg635_define_phase_as_zero_btn_clicked(self):
        pass

    @QtCore.pyqtSlot(int)
    def cg635_freq_units_changed(self, units_index):
        pass

    @QtCore.pyqtSlot()
    def cg635_check_for_errors_btn_clicked(self):
        self.cg635_check_errors_signal.emit(True)

    @QtCore.pyqtSlot()
    def save_as_dflt_btn_clicked(self):
        print('btn does nothing')
        pass

    @QtCore.pyqtSlot(bool)
    def sr830_checkbox_clicked(self, checked):
        print(checked)
        if checked is True:
            self.ui.sr844_checkbox.setChecked(False)
            self.ui.sr830_checkbox.setChecked(True)
            self.lockin_model_preference = 'SR830'
            self.initialize_settings_window()
        else:
            print('Nothing happens in this case')

    @QtCore.pyqtSlot(bool)
    def sr844_checkbox_clicked(self, checked):
        print(checked)
        if checked is True:
            self.ui.sr830_checkbox.setChecked(False)
            self.ui.sr844_checkbox.setChecked(True)
            self.lockin_model_preference = 'SR844'
            self.initialize_settings_window()
        else:
            print('Nothing happens in this case')

    # @QtCore.pyqtSlot()
    # def lockin_model_changed(self):
    #     print('index: ' + str(self.ui.lockin_model_combobox.currentIndex()))
    #     if self.ui.lockin_model_combobox.currentIndex() == 0:
    #         self.lockin_model_preference = 'SR844'
    #     elif self.ui.lockin_model_combobox.currentIndex() == 1:
    #         self.lockin_model_preference = 'SR830'
    #     else:
    #         print('unknowns lockin_model')
    #     self.initialize_settings_window()

    @QtCore.pyqtSlot()
    def cancel_btn_clicked(self):
        # Note that it can't just close the window, it has to reset the settings next time the window is shown (this
        # could also be fixed by getting it so that when actionSettings occurs, settings window ui objets are updated to
        # reflect the settings before showing the window_)
        print('btn does nothing')
        self.instrument_status_changed('cg635', 1)
        pass

    @QtCore.pyqtSlot()
    def set_tab_params_btn_clicked(self, which_tab=None):
        print('set tab starting')
        if which_tab is None:
            which_tab = self.ui.tab_widget.currentIndex()

        if which_tab == 0:
            com_idx = self.ui.prologix_com_port_spinner.value()
            self.prologix_com_port = 'ASRL' + str(com_idx) + '::INSTR'
            print('General Settings tab not set up')
        elif which_tab == 1:
            if self.lockin_model_preference == 'SR844':
                # self.lockin_model_preference = 'SR844'

                self.sr844_gpib_address = self.ui.sr844_gpib_address_spinner.value()
                self.sr844_outputs = self.ui.outputs_combobox.currentIndex()
                self.sr844_sensitivity = self.ui.sensitivity_combobox.currentIndex()
                self.sr844_filter_slope = self.ui.filter_slope_combobox.currentIndex()
                self.sr844_time_constant = self.ui.time_constant_combobox.currentIndex()
                self.sr844_wide_reserve = self.ui.wide_reserve_combobox.currentIndex()
                self.sr844_close_reserve = self.ui.close_reserve_combobox.currentIndex()
                self.sr844_sampling_rate = self.ui.sampling_rate_combobox.currentIndex()
                self.sr844_input_impedance = self.ui.input_impedance_combobox.currentIndex()
                self.sr844_ref_impedance = self.ui.ref_impedance_combobox.currentIndex()
                self.sr844_ref_source = self.ui.ref_source_combobox.currentIndex()
                self.sr844_harmonic = self.ui.sr844_harmonic_combobox.currentIndex()
                self.sr844_expand = self.ui.expand_combobox.currentIndex()

            elif self.lockin_model_preference == 'SR830':

                self.sr830_gpib_address = self.ui.sr830_gpib_address_spinner.value()
                self.sr830_outputs = self.ui.outputs_combobox.currentIndex()
                self.sr830_sensitivity = self.ui.sensitivity_combobox.currentIndex()
                self.sr830_filter_slope = self.ui.filter_slope_combobox.currentIndex()
                self.sr830_time_constant = self.ui.time_constant_combobox.currentIndex()
                self.sr830_dyn_reserve_mode = self.ui.dynamic_reserve_combobox.currentIndex()
                self.sr830_sampling_rate = self.ui.sampling_rate_combobox.currentIndex()
                self.sr830_ref_source = self.ui.ref_source_combobox.currentIndex()
                self.sr830_harmonic_mode = self.ui.sr844_harmonic_combobox.currentIndex()
        elif which_tab == 2:
            print('Mono tab not set up yet')
        elif which_tab == 3:
            print('RnS tab not set up yet')
        elif which_tab == 4:
            print('CG 635 tab not set up with this button')
        else:
            print('Tab not set up yet')

        self.update_tab_signal.emit(which_tab)

    @QtCore.pyqtSlot()
    def set_all_params_btn_clicked(self):
        #TODO:
        # 1. Fix the com ports thing
        # 2. Get this to vary depending on which lockin is used

        # First update the attributes (current tab only?)
        # self.mono_resource_name
        # self.mono_groove_density
        # self.mono_home_wavelength
        for ii in range(0, self.ui.tab_widget.count()):
            self.set_tab_params_btn_clicked(which_tab=ii)

        # Then tell the main window to talk to the instruments
        self.update_all_signal.emit(True)

    @QtCore.pyqtSlot()
    def auto_sens_btn_clicked(self):
        print('btn does nothing')
        pass
# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Defines the instance of the whole application
    app.setStyle('Fusion')
    help_window = SettingsWindowForm()  # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    help_window.show()
    sys.exit(app.exec_())
