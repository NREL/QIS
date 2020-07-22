# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Ryan/AppData/Local/Temp/expt_control_UI_20200708jVRCmj.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1432, 856)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(500, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.PlotWidget = PlotWidget(self.centralwidget)
        self.PlotWidget.setMinimumSize(QtCore.QSize(300, 200))
        self.PlotWidget.setObjectName("PlotWidget")
        self.gridLayout.addWidget(self.PlotWidget, 1, 1, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1432, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuInstruments = QtWidgets.QMenu(self.menubar)
        self.menuInstruments.setObjectName("menuInstruments")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMonochromator = QtWidgets.QAction(MainWindow)
        self.actionMonochromator.setObjectName("actionMonochromator")
        self.actionSR844_Lock_in_Amplifier = QtWidgets.QAction(MainWindow)
        self.actionSR844_Lock_in_Amplifier.setObjectName("actionSR844_Lock_in_Amplifier")
        self.actionCryostat_Magnet = QtWidgets.QAction(MainWindow)
        self.actionCryostat_Magnet.setObjectName("actionCryostat_Magnet")
        self.actionMicrowave_Source = QtWidgets.QAction(MainWindow)
        self.actionMicrowave_Source.setObjectName("actionMicrowave_Source")
        self.actionFunction_Generator_AOM_Driver = QtWidgets.QAction(MainWindow)
        self.actionFunction_Generator_AOM_Driver.setObjectName("actionFunction_Generator_AOM_Driver")
        self.menuInstruments.addSeparator()
        self.menuInstruments.addAction(self.actionMonochromator)
        self.menuInstruments.addAction(self.actionSR844_Lock_in_Amplifier)
        self.menuInstruments.addAction(self.actionCryostat_Magnet)
        self.menuInstruments.addAction(self.actionMicrowave_Source)
        self.menuInstruments.addAction(self.actionFunction_Generator_AOM_Driver)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuInstruments.menuAction())

        self.retranslateUi(MainWindow)
        self.actionMonochromator.triggered.connect(MainWindow.open_mono_window)
        self.actionSR844_Lock_in_Amplifier.triggered.connect(MainWindow.open_lockin_window)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "Plot"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuInstruments.setTitle(_translate("MainWindow", "Instruments"))
        self.actionMonochromator.setText(_translate("MainWindow", "Monochromator"))
        self.actionSR844_Lock_in_Amplifier.setText(_translate("MainWindow", "SR844 (Lock-in Amplifier)"))
        self.actionCryostat_Magnet.setText(_translate("MainWindow", "Cryostat/Magnet"))
        self.actionMicrowave_Source.setText(_translate("MainWindow", "Microwave Source"))
        self.actionFunction_Generator_AOM_Driver.setText(_translate("MainWindow", "Function Generator (AOM Driver)"))
from plotwidget import PlotWidget
