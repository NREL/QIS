import os
import sys
import PyQt5
import pyvisa
from PyQt5.QtWidgets import QApplication, QWidget, QDoubleSpinBox
from PyQt5 import QtCore


from padmr.supp.settings.gui import Ui_Form as Settings_Ui_Form
from padmr.supp.label_strings import LabelStrings
from padmr.supp.icons import led_icons_rc
from padmr.instr.lia.controls import LockinSettings
from padmr.instr.laser.controls import TopticaSettings, TopticaInstr
from padmr.instr.mono.controls import MonoSettings
from padmr.instr.cg635.controls import CG635Settings

#TODO:
# 1. Split "initialize_settings_window" to create also an "update_settings_window"
# 2. Remove all the unnecessary "bools" from the signals (c.f. connect_instr_signal, which works fine)
# 3. Get rid of the silly "set_tab" and "set_all_tabs". Only with the lock-in would you want to change a lot at once
pyqt = os.path.dirname(PyQt5.__file__)  # This and the following line are essential to make guis run
QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))


class Presets:              # Presumably I should incorporate these into the Settings file. It seems silly to have both
    def __init__(self):
        self.probe_wl_start = 400
        self.probe_wl_end = 700
        self.probe_wl_num_steps = 31        # self.probe_wl_step_size = 5

        self.pump_mod_freq_start = 25    # kHz
        self.pump_mod_freq_end = 200000
        self.pump_mod_freq_steps = 3    # later set this to 20 or something

        # self.lockin_sampling_rate = 512     # Hertz
        self.lockin_sampling_duration = 1   # Seconds

        self.temperature = 295
        self.static_field = 0
        self.probe_wl = 513
        self.rf_freq = 9.2


class SettingsWindowForm(QWidget):

    lockin_property_updated_signal = QtCore.pyqtSignal(str, int)
    cg635_property_updated_signal = QtCore.pyqtSignal(str, int)

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

        self.presets = Presets()
        # Prepare settings objects for each instrument. These are redundant at the moment (each instrument has
        # an identical settings object), but for the moment, this seems like the best way to do things.
        self.lia = LockinSettings()
        self.cg = CG635Settings()
        self.toptica = TopticaSettings()
        self.md2000 = MonoSettings()

        self.label_strings = LabelStrings()

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

        ini_file_object = open(r'C:\Users\ryand\OneDrive\Documents\PythonProjects\QIS\PADMR\padmr\supp\settings'
                               r'\initialization_parameters.ini', 'r')
        param_lines = ini_file_object.readlines()
        print('attempting to read initialization file')

        # General Settings
        self.relevant_instruments = param_lines[1].split('#')[0].split()[2].split(',')
        self.prologix_com_port = param_lines[2].split('#')[0].split()[2]
        self.lockin_model_preference = param_lines[3].split('#')[0].split()[2]
        self.lia.model = self.lockin_model_preference

        self.lia.settling_delay_factor = int(param_lines[4].split('#')[0].split()[2])
        # self.lia.settling_delay_factor = self.lockin_delay_scaling_factor

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
        self.md2000.com_port = param_lines[60].split('#')[0].split()[2]
        self.md2000.gr_dens_idx = int(param_lines[61].split('#')[0].split()[2])
        self.md2000.cal_wl = float(param_lines[62].split('#')[0].split()[2])
        self.md2000.bl_amt = float(param_lines[63].split('#')[0].split()[2])
        self.md2000.bl_bool = bool(param_lines[64].split('#')[0].split()[2])
        self.md2000.speed = float(param_lines[65].split('#')[0].split()[2])

        # CG635 Settings
        self.cg635_resource_name = param_lines[70].split('#')[0].split()[2]
        self.cg635_gpib_address = int(param_lines[71].split('#')[0].split()[2])
        self.cg635_freq_units = int(param_lines[72].split('#')[0].split()[2])
        self.cg635_max_freq = int(param_lines[73].split('#')[0].split()[2])

        # Toptica Settings
        self.toptica.com_port = param_lines[100].split('#')[0].split()[2]

        # Experiment Setup Presets
        self.presets.probe_wl_start = float(param_lines[120].split('#')[0].split()[2])
        self.presets.probe_wl_end = float(param_lines[121].split('#')[0].split()[2])
        self.presets.probe_wl_num_steps = int(param_lines[122].split('#')[0].split()[2])
        self.presets.pump_mod_freq_start = float(param_lines[123].split('#')[0].split()[2])
        self.presets.pump_mod_freq_end = float(param_lines[124].split('#')[0].split()[2])
        self.presets.pump_mod_freq_steps = int(param_lines[125].split('#')[0].split()[2])

        self.presets.lockin_sampling_duration = float(param_lines[127].split('#')[0].split()[2])
        self.presets.temperature = float(param_lines[128].split('#')[0].split()[2])
        self.presets.static_field = float(param_lines[129].split('#')[0].split()[2])
        self.presets.probe_wl = float(param_lines[130].split('#')[0].split()[2])
        self.presets.rf_freq = float(param_lines[131].split('#')[0].split()[2])
        print('toptica com_port: ' + str(self.toptica.com_port))

    def init_lockin_tab(self):
        # Initialize the lock-in tab
        print('----------------------------------Initializing the lock-in Tab-----------------------------------------')
        gpib_address = int(self.sr844_gpib_address)
        self.ui.sr844_gpib_address_spbx.setValue(gpib_address)

        gpib_address = int(self.sr830_gpib_address)
        self.ui.sr830_gpib_address_spbx.setValue(gpib_address)

        self.ui.lockin_model_lnedt.setDisabled(True)

        self.ui.lockin_delay_scale_spbx.setValue(self.lia.settling_delay_factor)
        try:
            print('Inside Try')
            # First set the values that do not depend on which lock-in you're using
            self.ui.outputs_cbx.setCurrentIndex(self.lia.outputs)
            self.ui.sampling_rate_cbx.setCurrentIndex(self.lia.sampling_rate)
            self.ui.ref_source_cbx.setCurrentIndex(self.lia.reference_source)
            self.ui.expand_cbx.setCurrentIndex(self.lia.expand)

            # These are specific to the SR830 but do not interfere with the SR844
            self.ui.dynamic_reserve_cbx.setCurrentIndex(self.lia.dynamic_reserve)
            self.ui.harmonic_spbx.setValue(self.lia.harmonic)

            # These are specific to the SR844, but do not interfere with the SR830:
            self.ui.wide_reserve_cbx.setCurrentIndex(self.lia.wide_reserve)
            self.ui.close_reserve_cbx.setCurrentIndex(self.lia.close_reserve)
            self.ui.input_impedance_cbx.setCurrentIndex(self.lia.input_impedance)
            self.ui.ref_impedance_cbx.setCurrentIndex(self.lia.reference_impedance)
            self.ui.sr844_harmonic_cbx.setCurrentIndex(self.lia.twoF_detect_mode)
            print('About to start if statement')
            if self.lia.model == 'SR844':
                # Disable ui objects that relate only to the SR830
                print('lockin.model == SR844')
                self.ui.lockin_model_lnedt.setText('SR844 (25 kHz - 200 MHz)')
                self.ui.sr844_checkbox.setChecked(True)
                self.ui.sr830_checkbox.setChecked(False)

                self.ui.sr844_gpib_address_spbx.setDisabled(False)
                self.ui.sr830_gpib_address_spbx.setDisabled(True)
                self.ui.wide_reserve_cbx.setDisabled(False)
                self.ui.close_reserve_cbx.setDisabled(False)
                self.ui.dynamic_reserve_cbx.setDisabled(True)
                self.ui.ref_impedance_cbx.setDisabled(False)
                self.ui.input_impedance_cbx.setDisabled(False)
                self.ui.harmonic_spbx.setDisabled(True)
                self.ui.sr844_harmonic_cbx.setDisabled(False)

                self.lia.sens_list = self.lia.sr844_sens_list
                self.lia.tc_list = self.lia.sr844_tc_list
                self.lia.tc_numeric_list = self.lia.sr844_tc_options
                self.lia.slope_list = self.lia.sr844_slope_list

                self.lia.gpib_address = self.sr844_gpib_address
                self.lia.sensitivity = self.sr844_sensitivity
                self.lia.time_constant = self.sr844_time_constant
                self.lia.filter_slope = self.sr844_filter_slope

            elif self.lia.model == 'SR830':
                print('lockin_model=SR830')
                # Disable ui objects that relate only to the SR830
                self.ui.lockin_model_lnedt.setText('SR830 (1 mHz - 102 kHz)')
                self.ui.sr830_checkbox.setChecked(True)
                self.ui.sr844_checkbox.setChecked(False)

                self.ui.sr844_gpib_address_spbx.setDisabled(True)
                self.ui.sr830_gpib_address_spbx.setDisabled(False)
                self.ui.wide_reserve_cbx.setDisabled(True)
                self.ui.close_reserve_cbx.setDisabled(True)
                self.ui.dynamic_reserve_cbx.setDisabled(False)
                self.ui.ref_impedance_cbx.setDisabled(True)
                self.ui.input_impedance_cbx.setDisabled(True)
                self.ui.harmonic_spbx.setDisabled(False)
                self.ui.sr844_harmonic_cbx.setDisabled(True)

                self.lia.sens_list = self.lia.sr830_sens_list
                self.lia.tc_list = self.lia.sr830_tc_list
                self.lia.tc_numeric_list = self.lia.sr830_tc_options
                self.lia.slope_list = self.lia.sr830_slope_list

                self.lia.gpib_address = self.sr830_gpib_address
                self.lia.sensitivity = self.sr830_sensitivity
                self.lia.time_constant = self.sr830_time_constant
                self.lia.filter_slope = self.sr830_filter_slope
                print('Finished if statement')
            print('Outside of if statement')
            # These require first determining which lock-in will be used:
            self.ui.sensitivity_cbx.clear()
            print(str(self.lia.sens_list))
            print(str(self.lia.sensitivity))
            self.ui.sensitivity_cbx.addItems(self.lia.sens_list)
            self.ui.sensitivity_cbx.setCurrentIndex(self.lia.sensitivity)
            print('Added sens_list')

            self.ui.time_constant_cbx.clear()
            self.ui.time_constant_cbx.addItems(self.lia.tc_list)
            self.ui.time_constant_cbx.setCurrentIndex(self.lia.time_constant)

            self.ui.filter_slope_cbx.clear()
            self.ui.filter_slope_cbx.addItems(self.lia.slope_list)
            self.ui.filter_slope_cbx.setCurrentIndex(self.lia.filter_slope)

            # self.lockin_model_changed()
        except ValueError:
            print('.ini file inconsistent with expectations')
            print(str(sys.exc_info()[:]))
        except Exception:
            print(str(sys.exc_info()[:]))

    def update_md2000_tab(self):
        self.ui.mono_bl_comp_spbx.setValue(self.md2000.bl_amt)
        self.ui.mono_cal_wl_spbx.setValue(self.md2000.cal_wl)
        self.ui.mono_gr_dens_cbx.setCurrentIndex(self.md2000.gr_dens_idx)
        self.ui.mono_speed_spbx.setValue(self.md2000.speed)
        self.md2000.gr_dens_val = self.md2000.gr_dens_opts[self.md2000.gr_dens_idx]
        self.ui.mono_act_wl_lnedt.setText(str(self.md2000.cur_wl))
        self.ui.mono_bl_comp_chkbx.setChecked(self.md2000.bl_bool)

    def initialize_settings_window(self):
        # Initialize the general tab

        self.ui.status_ind_cg635.setText(self.label_strings.off_led_str)
        self.ui.status_ind_sr830.setText(self.label_strings.off_led_str)
        self.ui.status_ind_sr844.setText(self.label_strings.off_led_str)
        self.ui.status_ind_cryostat.setText(self.label_strings.off_led_str)
        self.ui.status_ind_md2000.setText(self.label_strings.off_led_str)
        self.ui.status_ind_toptica.setText(self.label_strings.off_led_str)
        self.ui.status_ind_smb100a.setText(self.label_strings.off_led_str)

        self.check_com_ports()

        self.init_lockin_tab()
        self.update_md2000_tab()

        print('----------------------------------Initializing the cg635 Tab---------------------------------------')
        self.ui.cg635_gpib_spbx.setValue(self.cg635_gpib_address)
        self.ui.cg635_freq_units_cbx.setCurrentIndex(self.cg635_freq_units)

        self.update_topt_tab()

    def check_com_ports(self):
        rm = pyvisa.ResourceManager()
        resources = list(rm.list_resources())
        resources.insert(0, '')
        self.ui.md2000_com_port_cmb.addItems(resources)
        self.ui.md2000_com_port_cmb.setCurrentText(self.md2000.com_port)

        self.ui.cryostat_com_port_cmb.addItems(resources)

        self.ui.toptica_com_port_cmb.addItems(resources)
        self.ui.toptica_com_port_cmb.setCurrentText(self.toptica.com_port)

        self.ui.prologix_com_port_cmb.addItems(resources)
        self.ui.prologix_com_port_cmb.setCurrentText(self.prologix_com_port)

        self.ui.smb100a_com_port_cmb.addItems(resources)

    @QtCore.pyqtSlot(str, int)
    def instrument_status_changed(self, which_instrument, new_status):
        """
        status=0/1/2 for off/connected/error.
        which_instrument = 'sr844'/'sr830'/'cg635'/'cryostat'/'smb100a'/'md2000'/'toptica'
        """
        # Decide which string is needed to make change
        if new_status == 0:
            text_str = self.label_strings.off_led_str
        elif new_status == 1:
            text_str = self.label_strings.grn_led_str
        elif new_status == 2:
            text_str = self.label_strings.red_led_str #red_led_str
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

    # @QtCore.pyqtSlot(str, int)
    # def lockin_property_updated(self, property_name, new_value):
    #     print('Updating ' + property_name + ' Stored Setting')
    #     print('old value: ' + str(getattr(self.lia, property_name)))
    #     setattr(self.lia, property_name, new_value)
    #     print('new value: ' + str(getattr(self.lia, property_name)))
    #
    # @QtCore.pyqtSlot(str, int)
    # def cg635_property_updated(self, property_name, new_value):
    #     print('Updating ' + property_name + ' Stored Setting')
    #     print('old value: ' + str(getattr(self.cg, property_name)))
    #     setattr(self.cg, property_name, new_value)
    #     print('new value: ' + str(getattr(self.cg, property_name)))

    @QtCore.pyqtSlot()
    def toptica_start_btn_clicked(self):
        print('------------------------------------ STARTING LASER EMISSION ------------------------------------------')
        # self.ui.toptica_emission_indicator.setText(self.laser_on_str)
        # self.toptica_start_signal.emit()
        print('ATM, button does not engage laser')

    @QtCore.pyqtSlot()
    def toptica_bias_enable_btn_clicked(self):
        print('------------------------------------ STARTING LASER EMISSION ------------------------------------------')
        # self.ui.toptica_emission_indicator.setText(self.laser_on_str)
        # self.toptica_enable_signal.emit()

    @QtCore.pyqtSlot()
    def toptica_stop_btn_clicked(self):
        print('------------------------------------ STOPPING LASER EMISSION ------------------------------------------')
        self.ui.toptica_emission_indicator.setText(self.label_strings.laser_off_str)
        self.toptica_stop_signal.emit()
        print('ATM, button does not engage laser')

    @QtCore.pyqtSlot(str, int)
    @QtCore.pyqtSlot(str, float)
    def update_topt_tab(self):
        self.ui.toptica_power_spbx.setValue(self.toptica.power / 1000)

        self.ui.toptica_bias_spbx.setValue(self.toptica.bias_power)

        if self.toptica.laser_status == 0:
            self.ui.toptica_emission_indicator.setText(self.label_strings.laser_off_str)
        elif self.toptica.laser_status == 1:
            self.ui.toptica_emission_indicator.setText(self.label_strings.laser_on_str)

        if self.toptica.mod_on == 0:
            self.ui.toptica_mod_indicator.setText(self.label_strings.dig_mod_off_str)
        elif self.toptica.mod_on == 1:
            self.ui.toptica_mod_indicator.setText(self.label_strings.dig_mod_on_str)

    @QtCore.pyqtSlot()
    def toptica_set_bias_power_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def toptica_set_main_power_btn_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def toptica_ext_en_btn_clicked(self):
        pass

    # @QtCore.pyqtSlot()
    # def cg635_set_phase_btn_clicked(self):
    #     pass

    # @QtCore.pyqtSlot()
    # def cg635_set_freq_btn_clicked(self):
    #     freq_to_set = self.ui.cg635_set_freq_spbx.value()
    #     self.cg635_set_freq_signal.emit(freq_to_set)

    # @QtCore.pyqtSlot()
    # def cg635_define_phase_as_zero_btn_clicked(self):
    #     pass

    # @QtCore.pyqtSlot(int)
    # def cg635_freq_units_changed(self, units_index):
    #     pass

    # @QtCore.pyqtSlot()
    # def cg635_check_for_errors_btn_clicked(self):
    #     self.cg635_check_errors_signal.emit(True)

    @QtCore.pyqtSlot()
    def save_as_dflt_btn_clicked(self):
        print('btn does nothing')
        pass

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
    def sr844_gpib_address_changed(self, new_addr):
        self.sr844_gpib_address = new_addr
        self.lockin_property_updated_signal.emit('gpib_address', new_addr)

    @QtCore.pyqtSlot(int)
    def sr830_gpib_address_changed(self, new_addr):
        self.sr830_gpib_address = new_addr
        self.lockin_property_updated_signal.emit('gpib_address', new_addr)

    @QtCore.pyqtSlot(int)
    def cg635_gpib_address_changed(self, new_addr):
        self.cg635_property_updated_signal.emit('gpib_address', new_addr)


# ------------------------------------------------ RUN THE PROGRAM -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Defines the instance of the whole application
    app.setStyle('Fusion')
    help_window = SettingsWindowForm()  # Declares the instance of the main window class
    # This ^ is where the gui is prepared before being presented in the next line\/
    help_window.show()
    sys.exit(app.exec_())
