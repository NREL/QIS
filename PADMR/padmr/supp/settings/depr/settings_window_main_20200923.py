import os
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore

from FullControl.settings_window_ui import Ui_Form as Settings_Ui_Form
from FullControl import led_icons_rc
from Lockin_Amplifier.lockin_control_module import LockinSettings


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
    clear_instr_errors_signal = QtCore.pyqtSignal()

    # Lockin Signals
    lockin_2f_signal = QtCore.pyqtSignal(int)
    lockin_auto_crsrv_signal = QtCore.pyqtSignal()
    lockin_auto_dyn_rsrv_signal = QtCore.pyqtSignal()
    lockin_auto_wrsrv_signal = QtCore.pyqtSignal()
    lockin_auto_offset_signal = QtCore.pyqtSignal()
    lockin_auto_phase_signal = QtCore.pyqtSignal()
    lockin_wide_reserve_signal = QtCore.pyqtSignal(int)
    lockin_close_reserve_signal = QtCore.pyqtSignal(int)
    lockin_dynamic_reserve_signal = QtCore.pyqtSignal(int)
    lockin_expand_signal = QtCore.pyqtSignal(int)
    lockin_filter_slope_signal = QtCore.pyqtSignal(int)
    lockin_harmonic_signal = QtCore.pyqtSignal(int)
    lockin_phase_signal = QtCore.pyqtSignal()
    lockin_input_impedance_signal = QtCore.pyqtSignal(int)
    lockin_outputs_signal = QtCore.pyqtSignal(int)
    lockin_ref_impedance_signal = QtCore.pyqtSignal(int)
    lockin_ref_source_signal = QtCore.pyqtSignal(int)
    lockin_sampling_rate_signal = QtCore.pyqtSignal(int)
    lockin_sensitivity_signal = QtCore.pyqtSignal(int)
    lockin_time_constant_signal = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(SettingsWindowForm, self).__init__(*args, **kwargs)

        # Load the ui.py file and prepare the UI
        self.ui = Settings_Ui_Form()
        self.ui.setupUi(self)

        self.ui.tab_widget.setCurrentIndex(0)

        self.lia = LockinSettings()
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
        self.lia.model = self.lockin_model_preference

        self.lockin_delay_scaling_factor = int(param_lines[4].split('#')[0].split()[2])
        self.lia.settling_delay_factor = self.lockin_delay_scaling_factor

        self.lockin_outputs = int(param_lines[5].split('#')[0].split()[2])
        self.lia.outputs = self.lockin_outputs

        self.lockin_sampling_rate = int(param_lines[6].split('#')[0].split()[2])
        self.lia.sampling_rate = self.lockin_sampling_rate

        self.lockin_ref_source = int(param_lines[7].split('#')[0].split()[2])
        self.lia.reference_source = self.lockin_ref_source

        print(self.lockin_model_preference)
        print("prologix com port: " + str(self.prologix_com_port))

        # SR844 Settings
        self.sr844_gpib_address = int(param_lines[20].split('#')[0].split()[2])
        # self.sr844_outputs = int(param_lines[21].split('#')[0].split()[2])      # This is now deprecated
        self.sr844_sensitivity = int(param_lines[22].split('#')[0].split()[2])
        self.sr844_filter_slope = int(param_lines[23].split('#')[0].split()[2])
        self.sr844_time_constant = int(param_lines[24].split('#')[0].split()[2])
        self.lia.wide_reserve = int(param_lines[25].split('#')[0].split()[2])
        self.lia.close_reserve = int(param_lines[26].split('#')[0].split()[2])
        # self.sr844_sampling_rate = int(param_lines[27].split('#')[0].split()[2])
        self.lia.input_impedance = int(param_lines[28].split('#')[0].split()[2])
        self.lia.reference_impedance = int(param_lines[29].split('#')[0].split()[2])
        # self.sr844_ref_source = int(param_lines[30].split('#')[0].split()[2])
        self.sr844_harmonic = int(param_lines[31].split('#')[0].split()[2])
        self.lia.twoF_detect_mode = self.sr844_harmonic
        self.lia.expand = int(param_lines[32].split('#')[0].split()[2])

        # SR830 Settings
        self.sr830_gpib_address = int(param_lines[40].split('#')[0].split()[2])
        # self.sr830_outputs = int(param_lines[41].split('#')[0].split()[2])      # This is now deprecated
        self.sr830_sensitivity = int(param_lines[42].split('#')[0].split()[2])
        self.sr830_filter_slope = int(param_lines[43].split('#')[0].split()[2])
        self.sr830_time_constant = int(param_lines[44].split('#')[0].split()[2])
        self.lia.dynamic_reserve = int(param_lines[45].split('#')[0].split()[2])
        # self.sr830_sampling_rate = int(param_lines[46].split('#')[0].split()[2])
        # self.sr830_ref_source = int(param_lines[47].split('#')[0].split()[2])
        self.sr830_harmonic_mode = int(param_lines[48].split('#')[0].split()[2])
        self.lia.harmonic = self.sr830_harmonic_mode
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
            print('Inside Try')
            # First set the values that do not depend on which lock-in you're using
            com_number = int(self.prologix_com_port.split('L')[1].split(':')[0])
            self.ui.prologix_com_port_spinner.setValue(com_number)
            self.ui.outputs_combobox.setCurrentIndex(self.lia.outputs)
            self.ui.sampling_rate_combobox.setCurrentIndex(self.lia.sampling_rate)
            self.ui.ref_source_combobox.setCurrentIndex(self.lia.reference_source)
            self.ui.expand_combobox.setCurrentIndex(self.lia.expand)

            # These are specific to the SR830 but do not interfere with the SR844
            self.ui.dynamic_reserve_combobox.setCurrentIndex(self.lia.dynamic_reserve)
            self.ui.harmonic_spinner.setValue(self.lia.harmonic)

            # These are specific to the SR844, but do not interfere with the SR830:
            self.ui.wide_reserve_combobox.setCurrentIndex(self.lia.wide_reserve)
            self.ui.close_reserve_combobox.setCurrentIndex(self.lia.close_reserve)
            self.ui.input_impedance_combobox.setCurrentIndex(self.lia.input_impedance)
            self.ui.ref_impedance_combobox.setCurrentIndex(self.lia.reference_impedance)
            self.ui.sr844_harmonic_combobox.setCurrentIndex(self.lia.twoF_detect_mode)
            print('About to start if statement')
            if self.lia.model == 'SR844':
                # Disable ui objects that relate only to the SR830
                print('lockin.model == SR844')
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

                self.lia.sens_list = self.lia.sr844_sens_list
                self.lia.tc_list = self.lia.sr844_tc_list
                self.lia.tc_numeric_list = self.lia.sr844_tc_options
                self.lia.slope_list = self.lia.sr844_slope_list

                self.lia.sensitivity = self.sr844_sensitivity
                self.lia.time_constant = self.sr844_time_constant
                self.lia.filter_slope = self.sr844_filter_slope

            elif self.lia.model == 'SR830':
                print('lockin_model=SR830')
                # Disable ui objects that relate only to the SR830
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

                self.lia.sens_list = self.lia.sr830_sens_list
                self.lia.tc_list = self.lia.sr830_tc_list
                self.lia.tc_numeric_list = self.lia.sr830_tc_options
                self.lia.slope_list = self.lia.sr830_slope_list

                self.lia.sensitivity = self.sr830_sensitivity
                self.lia.time_constant = self.sr830_time_constant
                self.lia.filter_slope = self.sr830_filter_slope
                print('Finished if statement')
            print('Outside of if statement')
            # These require first determining which lock-in will be used:
            self.ui.sensitivity_combobox.clear()
            print(str(self.lia.sens_list))
            print(str(self.lia.sensitivity))
            self.ui.sensitivity_combobox.addItems(self.lia.sens_list)
            self.ui.sensitivity_combobox.setCurrentIndex(self.lia.sensitivity)
            print('Added sens_list')

            self.ui.time_constant_combobox.clear()
            self.ui.time_constant_combobox.addItems(self.lia.tc_list)
            self.ui.time_constant_combobox.setCurrentIndex(self.lia.time_constant)

            self.ui.sensitivity_combobox.clear()
            self.ui.sensitivity_combobox.addItems(self.lia.sens_list)
            self.ui.filter_slope_combobox.setCurrentIndex(self.lia.filter_slope)

            # self.lockin_model_changed()
            print('----------------------------------Initializing the cg635 Tab---------------------------------------')
            self.ui.cg635_comm_format_combobox.setCurrentIndex(self.cg635_com_format)
            self.ui.cg635_gpib_spinner.setValue(self.cg635_gpib_address)
            self.ui.cg635_freq_units_combobox.setCurrentIndex(self.cg635_freq_units)
        except ValueError:
            print('.ini file inconsistent with expectations')
            print(str(sys.exc_info()[:]))
        except Exception:
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

    @QtCore.pyqtSlot(str, int)
    def lockin_property_updated(self, property_name, new_value):
        print('Updating ' + property_name + ' Stored Setting')
        print('old value: ' + str(getattr(self.lia, property_name)))
        setattr(self.lia, property_name, new_value)
        print('new value: ' + str(getattr(self.lia, property_name)))

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

    # @QtCore.pyqtSlot(int)
    # def lockin_2f_detect_changed(self, idx):
    #     self.lockin_2f_signal.emit(idx)
    #
    # @QtCore.pyqtSlot()
    # def lockin_auto_crsrv_clicked(self):
    #     self.lockin_auto_crsrv_signal.emit()
    #
    # @QtCore.pyqtSlot()
    # def lockin_auto_dyn_rsrv_clicked(self):
    #     self.lockin_auto_dyn_rsrv_signal.emit()
    #
    # @QtCore.pyqtSlot()
    # def lockin_auto_wrsrv_clicked(self):
    #     self.lockin_auto_wrsrv_signal.emit()
    #
    # @QtCore.pyqtSlot()
    # def lockin_auto_offset_clicked(self):
    #     self.lockin_auto_offset_signal.emit()
    #
    # @QtCore.pyqtSlot()
    # def lockin_auto_phase_clicked(self):
    #     self.lockin_auto_phase_signal.emit()
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_close_reserve_changed(self, idx):
    #     self.lockin_close_reserve_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_dynamic_reserve_changed(self, idx):
    #     self.lockin_dynamic_reserve_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_expand_changed(self, idx):
    #     self.lockin_expand_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_filter_slope_changed(self, idx):
    #     self.lockin_filter_slope_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_harmonic_spinner_changed(self, value):
    #     self.lockin_harmonic_signal.emit(value)
    #
    # @QtCore.pyqtSlot()
    # def lockin_phase_spinner_changed(self):
    #     self.lockin_phase_signal.emit()
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_input_impedance_changed(self, idx):
    #     self.lockin_input_impedance_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_outputs_changed(self, idx):
    #     self.lockin_outputs_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_ref_impedance_changed(self, idx):
    #     self.lockin_ref_impedance_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_ref_source_changed(self, idx):
    #     self.lockin_ref_source_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_sampling_rate_changed(self, idx):
    #     self.lockin_sampling_rate_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_sensitivity_changed(self, idx):
    #     self.lockin_sensitivity_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_time_constant_changed(self, idx):
    #     self.lockin_time_constant_signal.emit(idx)
    #
    # @QtCore.pyqtSlot(int)
    # def lockin_wide_reserve_changed(self, idx):
    #     self.lockin_wide_reserve_signal.emit(idx)

    @QtCore.pyqtSlot(bool)
    def sr830_checkbox_clicked(self, checked):
        print(checked)
        try:
            if checked is True:
                self.ui.sr844_checkbox.setChecked(False)
                self.ui.sr830_checkbox.setChecked(True)
                self.lia.model = 'SR830'
                self.initialize_settings_window()
            else:
                print('Nothing happens in this case')
        except:
            print(sys.exc_info()[:])

    @QtCore.pyqtSlot(bool)
    def sr844_checkbox_clicked(self, checked):
        print(checked)
        try:
            if checked is True:
                self.ui.sr830_checkbox.setChecked(False)
                self.ui.sr844_checkbox.setChecked(True)
                self.lia.model = 'SR844'
                self.initialize_settings_window()
            else:
                print('Nothing happens in this case')
        except:
            print(sys.exc_info()[:])

    @QtCore.pyqtSlot(int)
    def cg635_comm_format_changed(self, value):
        self.cg635_com_format = value

    @QtCore.pyqtSlot(int)
    def sr844_gpib_address_changed(self, new_addr):
        self.sr844_gpib_address = new_addr

    @QtCore.pyqtSlot(int)
    def sr830_gpib_address_changed(self, new_addr):
        self.sr830_gpib_address = new_addr

    @QtCore.pyqtSlot(int)
    def cg635_gpib_address_changed(self, new_addr):
        self.cg635_gpib_address = new_addr

    @QtCore.pyqtSlot(int)
    def prologix_com_port_changed(self, new_port):
        self.prologix_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot(int)
    def md2000_com_port_changed(self, new_port):
        self.md2000_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot(int)
    def cg635_com_port_changed(self, new_port):
        self.cg635_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot(int)
    def smb100a_com_port_changed(self, new_port):
        self.smb100a_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot(int)
    def cryostat_com_port_changed(self, new_port):
        self.cryostat_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot(int)
    def toptica_com_port_changed(self, new_port):
        self.toptica_com_port = 'ASRL%d::INSTR' % new_port

    @QtCore.pyqtSlot()
    def clear_instr_errors_btn_clicked(self):
        self.clear_instr_errors_signal.emit()

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


    # @QtCore.pyqtSlot()
    # def set_tab_params_btn_clicked(self, which_tab=None):
    #     print('set tab starting')
    #     if which_tab is None:
    #         which_tab = self.ui.tab_widget.currentIndex()
    #
    #     if which_tab == 0:
    #         com_idx = self.ui.prologix_com_port_spinner.value()
    #         self.prologix_com_port = 'ASRL' + str(com_idx) + '::INSTR'
    #         print('General Settings tab not set up')
    #     elif which_tab == 1:
    #         self.lia.outputs = self.ui.outputs_combobox.currentIndex()
    #         self.lia.sampling_rate = self.ui.sampling_rate_combobox.currentIndex()
    #         self.lia.reference_source = self.ui.ref_source_combobox.currentIndex()
    #
    #         self.lia.sensitivity = self.ui.sensitivity_combobox.currentIndex()
    #         self.lia.filter_slope = self.ui.filter_slope_combobox.currentIndex()
    #         self.lia.time_constant = self.ui.time_constant_combobox.currentIndex()
    #         self.lia.wide_reserve = self.ui.wide_reserve_combobox.currentIndex()
    #         self.lia.close_reserve = self.ui.close_reserve_combobox.currentIndex()
    #
    #         self.lia.input_impedance = self.ui.input_impedance_combobox.currentIndex()
    #         self.lia.reference_impedance = self.ui.ref_impedance_combobox.currentIndex()
    #         self.lia.twoF_detect_mode = self.ui.sr844_harmonic_combobox.currentIndex()
    #         self.lia.harmonic = self.ui.harmonic_spinner.value()
    #         self.lia.expand = self.ui.expand_combobox.currentIndex()
    #         self.lia.dynamic_reserve = self.ui.dynamic_reserve_combobox.currentIndex()
    #         self.sr844_gpib_address = self.ui.sr844_gpib_address_spinner.value()
    #         self.sr830_gpib_address = self.ui.sr830_gpib_address_spinner.value()
    #         if self.lia.model == 'SR844':
    #             self.lia.gpib_address = self.sr844_gpib_address
    #         elif self.lia.model == 'SR830':
    #             self.lia.gpib_address = self.sr830_gpib_address
    #     elif which_tab == 2:
    #         print('Mono tab not set up yet')
    #     elif which_tab == 3:
    #         print('RnS tab not set up yet')
    #     elif which_tab == 4:
    #         print('CG 635 tab not set up with this button')
    #     else:
    #         print('Tab not set up yet')
    #
    #     self.update_tab_signal.emit(which_tab)

    # @QtCore.pyqtSlot()
    # def set_all_params_btn_clicked(self):
    #     #TODO:
    #     # 1. Fix the com ports thing
    #     # 2. Get this to vary depending on which lockin is used
    #
    #     # First update the attributes (current tab only?)
    #     # self.mono_resource_name
    #     # self.mono_groove_density
    #     # self.mono_home_wavelength
    #     for ii in range(0, self.ui.tab_widget.count()):
    #         self.set_tab_params_btn_clicked(which_tab=ii)
    #
    #     # Then tell the main window to talk to the instruments
    #     self.update_all_signal.emit(True)

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
