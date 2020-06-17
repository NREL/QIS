# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Ryan/AppData/Local/Temp/preferences_window_uiZMYBQn.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.sci_notn_label = QtWidgets.QLabel(Form)
        self.sci_notn_label.setObjectName("sci_notn_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sci_notn_label)
        self.sigfig_label = QtWidgets.QLabel(Form)
        self.sigfig_label.setObjectName("sigfig_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.sigfig_label)
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.sig_figs_spinner = QtWidgets.QSpinBox(Form)
        self.sig_figs_spinner.setProperty("value", 4)
        self.sig_figs_spinner.setObjectName("sig_figs_spinner")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sig_figs_spinner)
        self.scientific_notation_spinner = QtWidgets.QSpinBox(Form)
        self.scientific_notation_spinner.setProperty("value", 4)
        self.scientific_notation_spinner.setObjectName("scientific_notation_spinner")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.scientific_notation_spinner)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem)

        self.retranslateUi(Form)
        self.scientific_notation_spinner.valueChanged['int'].connect(Form.scientific_notation_limit_changed)
        self.sig_figs_spinner.valueChanged['int'].connect(Form.sig_fig_spinner_value_changed)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sci_notn_label.setText(_translate("Form", "Scientific Notation Limit Exponent"))
        self.sigfig_label.setText(_translate("Form", "Round to How Many Decimal Places?"))
        self.label_3.setText(_translate("Form", "Formatting"))
