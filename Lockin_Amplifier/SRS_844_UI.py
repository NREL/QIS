# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Ryan/AppData/Local/Temp/SRS_844_UI_2020-07-06flCLjR.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(943, 560)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1)
        self.ref_lineedit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ref_lineedit.setFont(font)
        self.ref_lineedit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ref_lineedit.setObjectName("ref_lineedit")
        self.gridLayout.addWidget(self.ref_lineedit, 14, 6, 1, 2)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 11, 0, 1, 1)
        self.ch1_lineedit = QtWidgets.QLineEdit(Form)
        self.ch1_lineedit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ch1_lineedit.setFont(font)
        self.ch1_lineedit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ch1_lineedit.setObjectName("ch1_lineedit")
        self.gridLayout.addWidget(self.ch1_lineedit, 14, 2, 1, 2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 13, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 1, 1, 1)
        self.ch2_lineedit = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ch2_lineedit.setFont(font)
        self.ch2_lineedit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ch2_lineedit.setObjectName("ch2_lineedit")
        self.gridLayout.addWidget(self.ch2_lineedit, 14, 4, 1, 2)
        self.time_constant_combobox = QtWidgets.QComboBox(Form)
        self.time_constant_combobox.setObjectName("time_constant_combobox")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.time_constant_combobox.addItem("")
        self.gridLayout.addWidget(self.time_constant_combobox, 9, 0, 1, 1)
        self.filter_slope_combobox = QtWidgets.QComboBox(Form)
        self.filter_slope_combobox.setObjectName("filter_slope_combobox")
        self.filter_slope_combobox.addItem("")
        self.filter_slope_combobox.addItem("")
        self.filter_slope_combobox.addItem("")
        self.filter_slope_combobox.addItem("")
        self.gridLayout.addWidget(self.filter_slope_combobox, 9, 1, 1, 1)
        self.start_btn = QtWidgets.QPushButton(Form)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 14, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 13, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 13, 6, 1, 1)
        self.sensitivity_combobox = QtWidgets.QComboBox(Form)
        self.sensitivity_combobox.setObjectName("sensitivity_combobox")
        self.gridLayout.addWidget(self.sensitivity_combobox, 12, 0, 1, 1)
        self.update_settings_btn = QtWidgets.QPushButton(Form)
        self.update_settings_btn.setObjectName("update_settings_btn")
        self.gridLayout.addWidget(self.update_settings_btn, 13, 0, 1, 2)
        self.read_str_textedit = QtWidgets.QPlainTextEdit(Form)
        self.read_str_textedit.setMaximumSize(QtCore.QSize(300, 100))
        self.read_str_textedit.setObjectName("read_str_textedit")
        self.gridLayout.addWidget(self.read_str_textedit, 10, 6, 1, 2)
        self.query_btn = QtWidgets.QPushButton(Form)
        self.query_btn.setMaximumSize(QtCore.QSize(300, 16777215))
        self.query_btn.setObjectName("query_btn")
        self.gridLayout.addWidget(self.query_btn, 9, 6, 1, 2)
        self.write_str_lineedit = QtWidgets.QLineEdit(Form)
        self.write_str_lineedit.setMaximumSize(QtCore.QSize(300, 16777215))
        self.write_str_lineedit.setObjectName("write_str_lineedit")
        self.gridLayout.addWidget(self.write_str_lineedit, 8, 6, 1, 2)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 6, 1, 2)
        self.outputs_selector = QtWidgets.QComboBox(Form)
        self.outputs_selector.setObjectName("outputs_selector")
        self.outputs_selector.addItem("")
        self.outputs_selector.addItem("")
        self.outputs_selector.addItem("")
        self.gridLayout.addWidget(self.outputs_selector, 12, 2, 1, 1)
        self.stop_btn = QtWidgets.QPushButton(Form)
        self.stop_btn.setObjectName("stop_btn")
        self.gridLayout.addWidget(self.stop_btn, 14, 1, 1, 1)
        self.PlotWidget = PlotWidget(Form)
        self.PlotWidget.setObjectName("PlotWidget")
        self.gridLayout.addWidget(self.PlotWidget, 6, 2, 6, 4)
        self.visa_resource_combobox = QtWidgets.QComboBox(Form)
        self.visa_resource_combobox.setObjectName("visa_resource_combobox")
        self.gridLayout.addWidget(self.visa_resource_combobox, 7, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 3, 1, 2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 10, 0, 1, 1)

        self.retranslateUi(Form)
        self.query_btn.clicked.connect(Form.query_btn_clicked)
        self.visa_resource_combobox.activated['QString'].connect(Form.com_port_combobox_activated)
        self.update_settings_btn.clicked.connect(Form.update_settings_btn_clicked)
        self.outputs_selector.activated['int'].connect(Form.output_selector_activated)
        self.start_btn.clicked.connect(Form.start_btn_clicked)
        self.stop_btn.clicked.connect(Form.stop_btn_clicked)
        self.pushButton.clicked.connect(Form.collect_fast_data)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Time Constant"))
        self.label_4.setText(_translate("Form", "Sensitivity"))
        self.label.setText(_translate("Form", "Controls"))
        self.label_7.setText(_translate("Form", "Channel 1"))
        self.label_6.setText(_translate("Form", "Filter Slope"))
        self.time_constant_combobox.setItemText(0, _translate("Form", "100 μs"))
        self.time_constant_combobox.setItemText(1, _translate("Form", "300 μs"))
        self.time_constant_combobox.setItemText(2, _translate("Form", "1     ms"))
        self.time_constant_combobox.setItemText(3, _translate("Form", "3     ms"))
        self.time_constant_combobox.setItemText(4, _translate("Form", "10   ms"))
        self.time_constant_combobox.setItemText(5, _translate("Form", "30   ms"))
        self.time_constant_combobox.setItemText(6, _translate("Form", "100 ms"))
        self.time_constant_combobox.setItemText(7, _translate("Form", "300 ms"))
        self.time_constant_combobox.setItemText(8, _translate("Form", "1        s"))
        self.time_constant_combobox.setItemText(9, _translate("Form", "3        s"))
        self.time_constant_combobox.setItemText(10, _translate("Form", "10      s"))
        self.time_constant_combobox.setItemText(11, _translate("Form", "30      s"))
        self.time_constant_combobox.setItemText(12, _translate("Form", "100    s"))
        self.time_constant_combobox.setItemText(13, _translate("Form", "300    s"))
        self.time_constant_combobox.setItemText(14, _translate("Form", "1      ks"))
        self.time_constant_combobox.setItemText(15, _translate("Form", "3      ks"))
        self.time_constant_combobox.setItemText(16, _translate("Form", "10    ks"))
        self.time_constant_combobox.setItemText(17, _translate("Form", "30    ks"))
        self.filter_slope_combobox.setItemText(0, _translate("Form", "6"))
        self.filter_slope_combobox.setItemText(1, _translate("Form", "12"))
        self.filter_slope_combobox.setItemText(2, _translate("Form", "18"))
        self.filter_slope_combobox.setItemText(3, _translate("Form", "24"))
        self.start_btn.setText(_translate("Form", "Start"))
        self.label_8.setText(_translate("Form", "Channel 2"))
        self.label_9.setText(_translate("Form", "Reference"))
        self.update_settings_btn.setText(_translate("Form", "Update Settings"))
        self.query_btn.setText(_translate("Form", "Query"))
        self.write_str_lineedit.setText(_translate("Form", "*IDN?"))
        self.label_5.setText(_translate("Form", "Write Manual String"))
        self.outputs_selector.setItemText(0, _translate("Form", "X / Y"))
        self.outputs_selector.setItemText(1, _translate("Form", "R / θ"))
        self.outputs_selector.setItemText(2, _translate("Form", "Manual"))
        self.stop_btn.setText(_translate("Form", "Stop"))
        self.label_3.setText(_translate("Form", "Com Port"))
        self.label_10.setText(_translate("Form", "Channel 1"))
        self.pushButton.setText(_translate("Form", "Fast Read"))
from plotwidget import PlotWidget