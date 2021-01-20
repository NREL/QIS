import sys,os
import os.path
from io import StringIO
import time

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap,QFont, QIcon
from PIL import Image ##PIL is short for pillow
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
#                              QHBoxLayout, QGroupBox, QVBoxLayout)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback

import style   #customer file

import pyvisa
import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
from seabreeze.spectrometers import Spectrometer, list_devices

sys.path.append("/Users/yshi2/Desktop/instrument1")
import FlameS
import replot
import SignalGen
import AWG
import PhotonCnt
import fit1, fit2
import coil
import Oscilloscope

import platform
# print(platform.system())
# windows only
# import ODMRch2
# import NI

#
# class WorkerSignals(QObject):
#     finished = pyqtSignal()
#     error = pyqtSignal(tuple)
#     result = pyqtSignal(object)
#     progress = pyqtSignal(int)
#
#
# class Worker(QRunnable):
#
#     def __init__(self, fn, *args, **kwargs):
#         super(Worker, self).__init__()
#
#         # Store constructor arguments (re-used for processing)
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs
#         self.signals = WorkerSignals()
#
#         # Add the callback to our kwargs
#         self.kwargs['progress_callback'] = self.signals.progress
#
#     @pyqtSlot()
#     def run(self):
#         try:
#             result = self.fn(*self.args, **self.kwargs)
#         except:
#             traceback.print_exc()
#             exctype, value = sys.exc_info()[:2]
#             self.signals.error.emit((exctype, value, traceback.format_exc()))
#         else:
#             self.signals.result.emit(result)  # Return the result of the processing
#         finally:
#             self.signals.finished.emit()  # Done



class ProgramWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

    # def __init__(self, *args, **kwargs):
    #     super(ProgramWindow, self).__init__(*args, **kwargs)

        self.setup_main_window()
        self.set_window_layout()

        # self.q=False
        # self.threadpool = QThreadPool()
        # # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # # self.timer.timeout.connect(self.recurring_timer)
        # self.timer.timeout.connect(self.func31)
        # self.timer.start()


    def setup_main_window(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize( 1000, 700  )
        self.setWindowTitle( "NV Diamond" )


    def set_window_layout(self):
        self.toolBar()
        self.tabWigdet()
        self.mainlayout()
        self.layout0()
        self.widget1()
        self.layout1()
        self.widget2()
        self.layout2()
        self.widget3()
        self.layout3()
        self.widget4()
        self.layout4()
        self.widget5()
        self.layout5()

    def toolBar(self):
        ##########################Main Menu###############
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # required to shown menu bar on Mac
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        code = menubar.addMenu("Code")
        helpMenu = menubar.addMenu("Help")

        ###########################Sub Menu Items################
        new = QAction("New Project", self)
        new.setShortcut("Ctrl+O")
        file.addAction(new)
        open = QAction("Open", self)
        file.addAction(open)
        exit = QAction("Exit", self)
        exit.setIcon((QIcon("icons/exit.png")))
        exit.triggered.connect(self.exitFunc)
        file.addAction(exit)

        ################ToolBar###################
        self.tb = self.addToolBar("My Toolbar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.newTb = QAction(QIcon('icons/folder.png'), "New", self)
        self.tb.addAction(self.newTb)
        self.tb.addSeparator()
        self.openTb = QAction(QIcon('icons/empty.png'), "Open", self)
        self.tb.addAction(self.openTb)
        self.tb.addSeparator()
        self.saveTb = QAction(QIcon('icons/save1.png'), "Save", self)
        self.tb.addAction(self.saveTb)
        self.tb.addSeparator()
        self.exitTb = QAction(QIcon('icons/stop1.png'), "Exit", self)
        self.exitTb.triggered.connect(self.exitFunc)
        self.tb.addAction(self.exitTb)
        self.tb.actionTriggered.connect(self.btnFunc)
        self.tb.addSeparator()

    def tabWigdet(self):
        self.tabs=QTabWidget()
        # self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setStyleSheet('QTabBar::tab { height: 50px; width: 150px; font-size: 18pt; }')#font-family: Courier;
        # self.tabs.setStyleSheet('QTabBar::tab { height: 50px; width: 300px; background: blue; }')

        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tab4=QWidget()
        self.tab5=QWidget()
        self.tabs.addTab(self.tab1, QtGui.QIcon("icons/zoom.png"), "  Fluorescence ")
        self.tabs.addTab(self.tab2, QtGui.QIcon("icons/zoom.png"), " ODMR ")
        self.tabs.addTab(self.tab3, QtGui.QIcon("icons/zoom.png"), "  T1  ")
        self.tabs.addTab(self.tab4, QtGui.QIcon("icons/zoom.png"), "  Curve Fitting  ")
        self.tabs.addTab(self.tab5, QtGui.QIcon("icons/zoom.png"), "  Other  ")

        f = open('par/par0.txt', "r")
        temp = f.read().splitlines()
        self.tabs.setCurrentIndex(int(temp[0]))


    def mainlayout(self):
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.addLayout(self.mainLeftLayout, 20)
        self.mainLayout.addLayout(self.mainRightLayout, 80)
        self.mainRightLayout.addWidget(self.tabs)

    def layout0(self):
        self.L01 = QVBoxLayout()
        self.L02 = QVBoxLayout()
        self.L03 = QVBoxLayout()
        self.mainLeftLayout.addLayout(self.L01, 50)
        self.mainLeftLayout.addLayout(self.L02, 20)
        self.mainLeftLayout.addLayout(self.L03, 30)

        self.l01 = QLabel("Available Equipment:")
        self.l02 = QLabel()
        self.l02.setStyleSheet(style.l02())
        self.l02.setAlignment(QtCore.Qt.AlignTop)
        self.l02.setWordWrap(True)
        self.l02.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.b01 = QPushButton("Check Equipment")
        self.b01.setToolTip("Check available equipment; make sure they are connected")
        self.b01.clicked.connect(self.checkeq)
        self.L01.addWidget(self.l01,10)
        self.L01.addWidget(self.l02,80)
        self.L01.addWidget(self.b01,10)

        self.l03 = QLabel("Current Folder:")
        # self.e01=QTextEdit(self)
        # self.e01.setText('/Users/yshi2/Documents/2020.12.28UI')
        # self.e01.setAcceptRichText(False)
        self.l04 = QLabel()
        self.l04.setStyleSheet(style.l02())
        self.l04.setAlignment(QtCore.Qt.AlignTop)
        self.l04.setWordWrap(True)
        self.l04.setTextInteractionFlags(Qt.TextSelectableByMouse)

        f = open('par/par0.txt', "r")
        temp = f.read().splitlines()
        self.l04.setText(temp[1])

        self.b02 = QPushButton("Change Folder")
        self.b02.setToolTip("Change folder that stores your spectrum")
        self.b02.clicked.connect(self.changefolder)
        self.L02.addWidget(self.l03)
        self.L02.addWidget(self.l04)
        self.L02.addWidget(self.b02)

        self.img = QLabel()
        self.pixmap = QPixmap('icons/nrel.png')
        self.smaller_pixmap = self.pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.img.setPixmap(self.smaller_pixmap)
        self.l05 = QLabel('version2.0\nSpring, 2021\n Golden, CO')
        self.L03.addWidget(self.img)
        self.L03.addWidget(self.l05)



################ Fluorescence ###################
    def layout1(self):
        L1 = QVBoxLayout()
        self.topbox1 = QGroupBox( "Parameters" )
        self.topbox1.setStyleSheet(style.top1())
        self.bottombox1 = QGroupBox( "" )
        self.bottombox1.setStyleSheet(style.bottom1())
        L1.addWidget(self.topbox1, 90)
        L1.addWidget(self.bottombox1, 10)
        self.tab1.setLayout(L1)

        #### top ####
        self.gridLayout1 = QGridLayout()

        self.l101=QLabel("Wavelength Low (nm)\n Min.250")
        self.l102=QLabel("Wavelength High (nm)\n Max 900")
        self.l103=QLabel("Integration Time (us)")
        self.e101=QLineEdit()
        self.e102=QLineEdit()
        self.e103=QLineEdit()

        self.l104=QLabel("File Name")
        self.l105=QLabel("Figure Title")
        self.e104 = QLineEdit()
        self.e105 = QLineEdit()

        self.l106=QLabel("Equipment is Ocean Optics UV-Vis spectrometer, Model: Flame S")
        self.l106.setWordWrap(True)
        self.l107 = QLabel("Re-plot a fluorescence spectrum in current folder:")
        self.l107.setWordWrap(True)

        f = open('par/par1.txt', "r")
        temp = f.read().splitlines()
        self.e101.setText(temp[0])  #550
        self.e102.setText(temp[1])   #800
        self.e103.setText(temp[2])   #1000000
        self.e104.setText(temp[3])   #ys20122901
        self.e105.setText(temp[4])   #Fluorescence

        self.l120=QLabel("")

        self.gridLayout1.addWidget(self.l101,0,0,1,2)
        self.gridLayout1.addWidget(self.l102,1,0,1,2)
        self.gridLayout1.addWidget(self.l103,2,0,1,2)
        self.gridLayout1.addWidget(self.l104,3,0,1,2)
        self.gridLayout1.addWidget(self.l105,4,0,1,2)

        self.gridLayout1.addWidget(self.e101,0,2,1,3)
        self.gridLayout1.addWidget(self.e102,1,2,1,3)
        self.gridLayout1.addWidget(self.e103,2,2,1,3)
        self.gridLayout1.addWidget(self.e104,3,2,1,3)
        self.gridLayout1.addWidget(self.e105,4,2,1,3)

        self.gridLayout1.addWidget(self.l106,0,6,1,3)
        self.gridLayout1.addWidget(self.l107,1,6,1,3)
        self.gridLayout1.addWidget(self.b14, 2,6,1,1)
        self.gridLayout1.addWidget(self.l120,0,5,1,1)

        self.L11 = QVBoxLayout()
        self.L11.addLayout(self.gridLayout1)
        self.L11.setContentsMargins(20, 10, 20, 10)
        self.topbox1.setLayout(self.L11)

        #### bottom ####
        self.bottomLayout1=QHBoxLayout()
        self.bottomL11 = QVBoxLayout()
        self.bottomL12 = QVBoxLayout()
        self.bottomL13 = QVBoxLayout()
        self.bottomL14 = QVBoxLayout()

        self.l11 = QLabel("START")
        self.l11.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL11.addWidget(self.l11)
        self.bottomL11.addWidget(self.b11)

        self.l12 = QLabel("STOP")
        self.l12.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL12.addWidget(self.l12)
        self.bottomL12.addWidget(self.b12)

        self.l13 = QLabel("SAVE")
        self.l13.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL13.addWidget(self.l13)
        self.bottomL13.addWidget(self.b13)

        self.l14 = QLabel("Hint:")
        self.l15 = QLabel()
        self.l15.setStyleSheet(style.l02())
        self.l15.setAlignment(QtCore.Qt.AlignTop)
        self.l15.setWordWrap(True)
        self.l15.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.bottomL14.addWidget(self.l14, 10)
        self.bottomL14.addWidget(self.l15, 90)

        self.bottomLayout1.addLayout(self.bottomL11)
        self.bottomLayout1.addLayout(self.bottomL12)
        self.bottomLayout1.addLayout(self.bottomL13)
        self.bottomLayout1.addLayout(self.bottomL14)
        self.bottombox1.setLayout(self.bottomLayout1)


    def widget1(self):
        self.b11 = QToolButton()
        self.b11.setIcon(QIcon("icons/start1.png"))
        self.b11.setIconSize(QSize(50, 50))
        self.b11.setToolTip("View fluorescence spectrum continuously")
        self.b11.clicked.connect(self.func11)

        self.b12 = QToolButton()
        self.b12.setIcon(QIcon("icons/stop1.png"))
        self.b12.setIconSize(QSize(50, 50))
        self.b12.setToolTip("Stop fluorescence spectrum acquisition")
        self.b12.clicked.connect(self.func12)

        self.b13 = QToolButton()
        self.b13.setIcon(QIcon("icons/save1.png"))
        self.b13.setIconSize(QSize(50, 50))
        self.b13.setToolTip("Save spectrum as csv file in current folder")
        self.b13.clicked.connect(self.func13)

        self.b14 = QPushButton("Re-plot")
        # self.b14.setIcon(QIcon("icons/start.png"))
        # self.b11.setIconSize(QSize(64, 64))
        # self.b14.setToolTip("Replot a spectrum acquired in current folder")
        self.b14.clicked.connect(self.func14)


########################## ODMR ###############
    def layout2(self):
        L2 = QVBoxLayout()
        self.topbox2 = QGroupBox("Parameters: Optically Detected Magnetic Resonance")
        self.topbox2.setStyleSheet(style.top2())
        self.bottombox2 = QGroupBox("")
        self.bottombox2.setStyleSheet(style.bottom2())
        L2.addWidget(self.topbox2, 90)
        L2.addWidget(self.bottombox2, 10)
        self.tab2.setLayout(L2)

        #### top ####
        self.gridLayout2 = QGridLayout()

        self.l201 = QLabel("Start Frequency (MHz)")
        self.l202 = QLabel("Stop Frequency (MHz)")
        self.l203 = QLabel("Step (MHz)")
        self.e201 = QLineEdit()
        self.e202 = QLineEdit()
        self.e203 = QLineEdit()

        self.l204 = QLabel("Dwell Time (ms)")
        self.l205 = QLabel("Scan Number")
        self.l206 = QLabel("Data Rate (samples/s)")
        self.e204 = QLineEdit()
        self.e205 = QLineEdit()
        self.e206 = QLineEdit()

        self.l207 = QLabel("Trigger Pulse Period (s)")
        self.l208 = QLabel("Trigger Pulse Duty Cycle")
        self.l209 = QLabel("Microwave Power (dBm)")
        self.e207 = QLineEdit()
        self.e208 = QComboBox()
        self.e208.addItems(["0.2","0.4","0.5"])
        self.e209 = QLineEdit()

        self.l211 = QLabel("Magnetic Field (G)")
        self.e211 = QLineEdit()
        self.l212 = QLabel("Coil Constant (G/A)")
        self.e212 = QLineEdit()
        self.l213 = QLabel("Coil Resistance (Ohm)")
        self.e213 = QLineEdit()
        self.e214 = QLabel("(You may use functions in 'Other' tab to get these two values.)")
        self.e214.setWordWrap(True)

        self.l214 = QLabel("Power Supply Current (A)")
        self.e215 = QLabel()
        self.l215 = QLabel("(Max. 10 A)")

        self.l216 = QLabel("Power Supply Voltage (V)")
        self.e217 = QLabel()
        self.l217 = QLabel("(Max. 20 V)")

        self.l218 = QLabel("File Name")
        self.l219 = QLabel("Figure Title")
        self.e218 = QLineEdit()
        self.e219 = QLineEdit()

        f = open('par/par2.txt', "r")
        temp = f.read().splitlines()
        self.e201.setText(temp[0])  #2700
        self.e202.setText(temp[1])   #3000
        self.e203.setText(temp[2])   #'1'
        self.e204.setText(temp[3])  #'100'
        self.e205.setText(temp[4])  #'1'
        self.e206.setText(temp[5])  #'5000'
        self.e207.setText(temp[6])   #'1'
        self.e208.setCurrentText(temp[7])  #'0.2'
        self.e209.setText(temp[8])    #'12'
        self.e211.setText(temp[9])    #'0'
        self.e212.setText(temp[10])   #'13.0584'
        self.e213.setText(temp[11])   #'0.8'
        self.e215.setText(temp[12])   #'0' I
        self.e217.setText(temp[13])   #'0' V
        self.e218.setText(temp[14])   #'ys20122902'
        self.e219.setText(temp[15])   #'Diamond'
        self.l04.setText(temp[16])

        self.l200 = QLabel("")

        self.gridLayout2.addWidget(self.l201, 0, 0, 1, 3)
        self.gridLayout2.addWidget(self.l202, 1, 0, 1, 3)
        self.gridLayout2.addWidget(self.l203, 2, 0, 1, 3)
        self.gridLayout2.addWidget(self.l204, 3, 0, 1, 3)
        self.gridLayout2.addWidget(self.l205, 4, 0, 1, 3)
        self.gridLayout2.addWidget(self.l206, 5, 0, 1, 3)
        self.gridLayout2.addWidget(self.l207, 6, 0, 1, 3)
        self.gridLayout2.addWidget(self.l208, 7, 0, 1, 3)
        self.gridLayout2.addWidget(self.l209, 8, 0, 1, 3)

        self.gridLayout2.addWidget(self.e201, 0, 3, 1, 2)
        self.gridLayout2.addWidget(self.e202, 1, 3, 1, 2)
        self.gridLayout2.addWidget(self.e203, 2, 3, 1, 2)
        self.gridLayout2.addWidget(self.e204, 3, 3, 1, 2)
        self.gridLayout2.addWidget(self.e205, 4, 3, 1, 2)
        self.gridLayout2.addWidget(self.e206, 5, 3, 1, 2)
        self.gridLayout2.addWidget(self.e207, 6, 3, 1, 2)
        self.gridLayout2.addWidget(self.e208, 7, 3, 1, 2)
        self.gridLayout2.addWidget(self.e209, 8, 3, 1, 2)

        #right panel
        self.gridLayout2.addWidget(self.l211, 0, 6, 1, 2)
        self.gridLayout2.addWidget(self.e211, 0, 8, 1, 2)
        self.gridLayout2.addWidget(self.b24,  0, 10, 1, 1)

        self.gridLayout2.addWidget(self.b25,  1, 10, 1, 1)

        self.gridLayout2.addWidget(self.l212, 2, 6, 1, 2)
        self.gridLayout2.addWidget(self.e212, 2, 8, 1, 2)
        self.gridLayout2.addWidget(self.l213, 3, 6, 1, 2)
        self.gridLayout2.addWidget(self.e213, 3, 8, 1, 2)
        self.gridLayout2.addWidget(self.e214, 2, 10, 2, 1)

        self.gridLayout2.addWidget(self.l214, 4, 6, 1, 2)
        self.gridLayout2.addWidget(self.e215, 4, 8, 1, 2)
        self.gridLayout2.addWidget(self.l215, 4, 10, 1, 1)

        self.gridLayout2.addWidget(self.l216, 5, 6, 1, 2)
        self.gridLayout2.addWidget(self.e217, 5, 8, 1, 2)
        self.gridLayout2.addWidget(self.l217, 5, 10, 1, 1)

        self.gridLayout2.addWidget(self.l218, 7, 6, 1, 2)
        self.gridLayout2.addWidget(self.l219, 8, 6, 1, 2)
        self.gridLayout2.addWidget(self.e218, 7, 8, 1, 3)
        self.gridLayout2.addWidget(self.e219, 8, 8, 1, 3)

        self.gridLayout2.addWidget(self.b26,  9, 10, 1, 1)
        self.gridLayout2.addWidget(self.l200, 0, 5, 1, 1)

        self.L21 = QVBoxLayout()
        self.L21.addLayout(self.gridLayout2)
        self.L21.setContentsMargins(20, 10, 20, 10)
        self.topbox2.setLayout(self.L21)

        #### bottom ####
        self.bottomLayout2 = QHBoxLayout()
        self.bottomL21 = QVBoxLayout()
        self.bottomL22 = QVBoxLayout()
        self.bottomL23 = QVBoxLayout()
        self.bottomL24 = QVBoxLayout()

        self.l21 = QLabel("START")
        self.l21.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL21.addWidget(self.l21)
        self.bottomL21.addWidget(self.b21)

        self.l22 = QLabel("STOP")
        self.l22.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL22.addWidget(self.l22)
        self.bottomL22.addWidget(self.b22)

        self.l23 = QLabel("REPLOT")
        self.l23.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL23.addWidget(self.l23)
        self.bottomL23.addWidget(self.b23)

        self.l24 = QLabel("Hint:")
        self.l25 = QLabel()
        self.l25.setStyleSheet(style.l02())
        self.l25.setAlignment(QtCore.Qt.AlignTop)
        self.l25.setWordWrap(True)
        self.l25.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.bottomL24.addWidget(self.l24, 10)
        self.bottomL24.addWidget(self.l25, 90)

        self.bottomLayout2.addLayout(self.bottomL21)
        self.bottomLayout2.addLayout(self.bottomL22)
        self.bottomLayout2.addLayout(self.bottomL23)
        self.bottomLayout2.addLayout(self.bottomL24)
        self.bottombox2.setLayout(self.bottomLayout2)

        if(platform.system() == 'Darwin'):# 'Linux'  # or 'Windows'/'Darwin'
            self.b21.setEnabled(False)
            self.b22.setEnabled(False)
            self.l25.setText('National Instrument equipment not available on Mac.\n'
                             'Other functions on this tab still available, like field and re-plot.')
        if(platform.system() == 'Linux'):# 'Linux'  # or 'Windows'/'Darwin'
            self.b21.setEnabled(False)
            self.b22.setEnabled(False)
            self.l25.setText('National Instrument equipment not available on Linux.\n'
                             'Other functions on this tab still available, like field and re-plot.')

    def widget2(self):
        ################ ODMR ###################

        self.b21 = QToolButton()
        self.b21.setIcon(QIcon("icons/start1.png"))
        self.b21.setIconSize(QSize(50, 50))
        self.b21.setToolTip("Start microwave frequency scan and acquire ODMR spectrum")
        self.b21.clicked.connect(self.func21)

        self.b22 = QToolButton()
        self.b22.setIcon(QIcon("icons/stop1.png"))
        self.b22.setIconSize(QSize(50, 50))
        self.b22.setToolTip("Stop current data acquisition")
        self.b22.clicked.connect(self.func22)

        self.b23 = QToolButton()
        self.b23.setIcon(QIcon("icons/plot1.png"))
        self.b23.setIconSize(QSize(50, 50))
        self.b23.setToolTip("Re-plot an ODMR spectrum in current folder")
        self.b23.clicked.connect(self.func23)

        self.b24 = QPushButton("Set Field")
        self.b24.setToolTip("Send current to power supply")
        self.b24.clicked.connect(self.func24)

        self.b25 = QPushButton("Zero Field")
        self.b25.setToolTip("Set magnetic field to 0")
        self.b25.clicked.connect(self.func25)

        self.b26 = QPushButton("Reset Default Values")
        self.b26.setToolTip("Reset to recommended values")
        self.b26.clicked.connect(self.func26)


########################## T1 ######################
    def layout3(self):
        L3 = QVBoxLayout()
        self.topbox3 = QGroupBox( "Parameters: Spin Lattice Relaxation Time T1" )
        self.topbox3.setStyleSheet(style.top3())
        self.bottombox3 = QGroupBox( "" )
        self.bottombox3.setStyleSheet(style.bottom3())
        L3.addWidget(self.topbox3, 90)
        L3.addWidget(self.bottombox3, 10)
        self.tab3.setLayout(L3)

        #### top ####
        self.gridLayout3 = QGridLayout()

        self.l301=QLabel("Trigger Pulse Frequency (Hz)")
        self.l302=QLabel("Trigger Pulse Period (ms)")
        self.l303 = QLabel("Laser Pulse1 length (us)")
        self.l304 = QLabel("Laser Pulse2 length (us)")
        self.l305 = QLabel("Microwave Pulse length (us)")
        self.e301 = QLineEdit()
        self.e303 = QLineEdit()
        self.e304 = QLineEdit()
        self.e305 = QLineEdit()

        self.l306 = QLabel("Counter gate (us)")
        self.e306 = QComboBox()
        self.e306.addItem("0.9")
        self.e306.addItems(["0.5", "0.6", "0.7", "0.8", "1", "1.1", "1.2"])

        self.l307 = QLabel()
        self.t1 = QPixmap('icons/t1.png')
        self.small = self.t1.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.l307.setPixmap(self.small)
        self.l307.setPixmap(self.t1)

        self.l311=QLabel("Microwave Frequency (MHz)")
        self.l312=QLabel("Microwave Power Level (dBm)")
        self.e311 = QLineEdit()
        self.e312=QLineEdit()

        self.l313=QLabel("Gap start (us)")
        self.l314 = QCheckBox("Gap step (us)", self)  #Lec7 check box
        # self.l314.setEnabled(True)
        self.l314.toggle()
        self.l315=QLabel("     Gap stop (us)")
        self.e313 = QLineEdit()
        self.e314 = QComboBox()
        self.e314.addItem("50")
        self.e314.addItems(["1", "5", "10", "25", "100"])
        self.e315 = QLineEdit()


        self.l316=QLabel("Counter TSET (x10e-7)")
        self.l317=QLabel("Counter Cycle (2000 max.)")
        self.l318 = QLabel("X2000 Cycle (Averages)")
        self.l319 = QLabel("Repeat Measurements#")
        self.l320 = QLabel("File Name")
        self.e316 = QLineEdit()
        self.e317 = QLineEdit()
        self.e318 = QLineEdit()
        self.e319 = QLineEdit()
        self.e320 = QLineEdit()

        # self.l320=QLabel("AWG Channel1 Period (us)")
        # self.l321=QLabel("AWG Channel2 Period (us)")
        # self.e320 = QLineEdit()
        # self.e320.setText('5000')
        # self.e321 = QLineEdit()
        # self.e321.setText('5000')

        f = open('par/par3.txt', "r")
        temp = f.read().splitlines()
        self.e301.setText(temp[0])  #200
        self.e303.setText(temp[1])   #'30'
        self.e304.setText(temp[2])  #'2'
        self.e305.setText(temp[3])  #'50'
        self.e306.setCurrentText(temp[4])  #'0.9'
        self.e311.setText(temp[5])  #'2877'
        self.e312.setText(temp[6])    #'15'
        self.e313.setText(temp[7])   #'50'
        self.e314.setCurrentText(temp[8])  #'50'
        self.e315.setText(temp[9])   #'400'
        self.e316.setText(temp[10])   #'9E3'
        self.e317.setText(temp[11])   #'2000'
        self.e318.setText(temp[12])   #'1'
        self.e319.setText(temp[13])   #'1'
        self.e320.setText(temp[14])   #'T1'

        T = int(1000 / int(self.e301.text()))
        self.e302 = QLabel(str(T))

        self.l330 = QLabel("")

        # addWidget(self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
        self.gridLayout3.addWidget(self.l330,1,10)
        self.gridLayout3.addWidget(self.l301,1,0,1,7)
        self.gridLayout3.addWidget(self.l302,2,0,1,7)
        self.gridLayout3.addWidget(self.l303,3,0,1,7)
        self.gridLayout3.addWidget(self.l304,4,0,1,7)
        self.gridLayout3.addWidget(self.l305,5,0,1,7)
        self.gridLayout3.addWidget(self.l306,6,0,1,7)
        self.gridLayout3.addWidget(self.l307,7,0,5,9)

        self.gridLayout3.addWidget(self.e301, 1, 7, 1, 3)
        self.gridLayout3.addWidget(self.e302, 2, 7, 1, 3)
        self.gridLayout3.addWidget(self.e303, 3, 7, 1, 3)
        self.gridLayout3.addWidget(self.e304, 4, 7, 1, 3)
        self.gridLayout3.addWidget(self.e305, 5, 7, 1, 3)
        self.gridLayout3.addWidget(self.e306, 6, 7, 1, 3)

        self.gridLayout3.addWidget(self.l311,1,11,1,6)
        self.gridLayout3.addWidget(self.l312,2,11,1,6)
        self.gridLayout3.addWidget(self.l313,3,11,1,6)
        self.gridLayout3.addWidget(self.l314,4,11,1,6)
        self.gridLayout3.addWidget(self.l315,5,11,1,6)
        self.gridLayout3.addWidget(self.l316,6,11,1,6)
        self.gridLayout3.addWidget(self.l317,7,11,1,6)
        self.gridLayout3.addWidget(self.l318,8,11,1,6)
        self.gridLayout3.addWidget(self.l319,9,11,1,6)
        self.gridLayout3.addWidget(self.l320,10,11,1,6)

        self.gridLayout3.addWidget(self.e311, 1, 17, 1, 3)
        self.gridLayout3.addWidget(self.e312, 2, 17, 1, 3)
        self.gridLayout3.addWidget(self.e313, 3, 17, 1, 3)
        self.gridLayout3.addWidget(self.e314, 4, 17, 1, 3)
        self.gridLayout3.addWidget(self.e315, 5, 17, 1, 3)
        self.gridLayout3.addWidget(self.e316, 6, 17, 1, 3)
        self.gridLayout3.addWidget(self.e317, 7, 17, 1, 3)
        self.gridLayout3.addWidget(self.e318, 8, 17, 1, 3)
        self.gridLayout3.addWidget(self.e319, 9, 17, 1, 3)
        self.gridLayout3.addWidget(self.e320, 10, 17, 1, 3)

        self.gridLayout3.addWidget(self.b34,  11, 17, 1, 3)

        self.L31 = QVBoxLayout()
        self.gridLayout3.setContentsMargins(10, 10, 10, 10)
        self.L31.addLayout(self.gridLayout3)
        self.topbox3.setLayout(self.L31)

        #### bottom ####
        self.bottomLayout3=QHBoxLayout()
        self.bottomL31 = QVBoxLayout()
        self.bottomL32 = QVBoxLayout()
        self.bottomL33 = QVBoxLayout()
        self.bottomL34 = QVBoxLayout()

        self.l31 = QLabel("START")
        self.l31.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL31.addWidget(self.l31)
        self.bottomL31.addWidget(self.b31)

        self.l32 = QLabel("STOP")
        self.l32.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL32.addWidget(self.l32)
        self.bottomL32.addWidget(self.b32)

        self.l33 = QLabel("SAVE")
        self.l33.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL33.addWidget(self.l33)
        self.bottomL33.addWidget(self.b33)

        self.l34 = QLabel("Hint:")
        self.l35 = QLabel()
        self.l35.setStyleSheet(style.l02())
        self.l35.setAlignment(QtCore.Qt.AlignTop)
        self.l35.setWordWrap(True)
        self.l35.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.bottomL34.addWidget(self.l34, 10)
        self.bottomL34.addWidget(self.l35, 90)
        # self.console3=QTextEdit(self)
        # self.console3 = QListWidget()
        # self.console3.resize(200, 10)

        self.bottomLayout3.addLayout(self.bottomL31)
        self.bottomLayout3.addLayout(self.bottomL32)
        self.bottomLayout3.addLayout(self.bottomL33)
        self.bottomLayout3.addLayout(self.bottomL34)
        self.bottombox3.setLayout(self.bottomLayout3)


    def widget3(self):
        self.b31 = QToolButton()
        self.b31.setIcon(QIcon("icons/start1.png"))
        self.b31.setIconSize(QSize(50, 50))
        self.b31.setToolTip("Start")
        self.b31.clicked.connect(self.func31)

        self.b32 = QToolButton()
        self.b32.setIcon(QIcon("icons/stop1.png"))
        self.b32.setIconSize(QSize(50, 50))
        self.b32.setToolTip("Stop")
        self.b32.clicked.connect(self.func32)

        self.b33 = QToolButton()
        self.b33.setIcon(QIcon("icons/save1.png"))
        self.b33.setIconSize(QSize(50, 50))
        self.b33.setToolTip("Save T1 data")
        self.b33.clicked.connect(self.func33)

        self.b34 = QPushButton("Reset Default Values")
        self.b34.setToolTip("Reset to recommended values")
        self.b34.clicked.connect(self.func34)


############## Fit T1 ##################

    def layout4(self):
        L4 = QVBoxLayout()
        self.topbox4 = QGroupBox( "Fitting Single Exponential Curve: a * (exp(+-x / t)) + b" )
        self.topbox4.setStyleSheet(style.top4())
        self.bottombox4 = QGroupBox("")
        self.bottombox4.setStyleSheet(style.bottom4())
        L4.addWidget(self.topbox4, 90)
        L4.addWidget(self.bottombox4, 10)
        self.tab4.setLayout(L4)

        #### top ####
        self.gridLayout4 = QGridLayout()

        self.l401 = QRadioButton("Decreasing Curve", self)  # Lec9 radio button
        self.l401.setChecked(True)
        self.l402 = QRadioButton("Increasing Curve", self)
        # self.l403 = QCheckBox("Fit and Plot", self)  #Lec7 check box
        # self.l403.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.l404 = QComboBox()
        # self.l404.addItems(["2", "3", "4", "5", "6", "7", "8"])
        # self.l405=QLabel("samples together")
        self.l403 = QLabel("Fit and Plot")
        self.l404 = QLabel("0")
        self.l405 = QLabel("sample(s)")


        self.l411=QLabel("Gap Start (us)")
        self.l412=QLabel("Gap Step (us)")
        self.l413=QLabel("Gap Stop (us)")
        self.e411 = QLineEdit()
        self.e412 = QComboBox()
        self.e412.addItem("50")
        self.e412.addItems(["1", "5", "10", "25", "100"])
        self.e413 = QLineEdit()

        self.l414 = QLabel("Iteration")
        self.e414 = QLineEdit()

        self.l415 = QLabel("Initial Values:")
        self.l416 = QLabel("a")
        self.l417 = QLabel("t")
        self.l418 = QLabel("b")
        self.l416.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.l417.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.l418.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.e416=QLineEdit()
        self.e417=QLineEdit()
        self.e418=QLineEdit()

        self.l421 = QLabel('')
        self.l421.setStyleSheet(style.label1())
        self.l421.setAlignment(QtCore.Qt.AlignTop)
        self.l421.setWordWrap(True)
        self.l421.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.l422 = QLabel("Figure Title")
        self.l423 = QLabel("Figure Legend") #:\n(multiple samples separat by ↵ )")
        self.l423.setWordWrap(True)
        self.e422=QLineEdit()
        self.e423 = QTextEdit()
        self.e423.setAcceptRichText(False)
        self.e423.setPlainText("FND in DI Water")

        self.l424 = QLabel("Reference Values\n for [a, t, b]:")
        self.e424 = QLabel("[10, 10, -20]\n[-100, 100, 40]\n[10, 40, 20]")
        self.l425 = QLabel("(multiple samples separate by ↵ )")

        f = open('par/par4.txt', "r")
        temp = f.read().splitlines()
        self.l404.setText(temp[0])  #'2'
        self.e411.setText(temp[1])  #'250'
        self.e412.setCurrentText(temp[2])  #'50'
        self.e413.setText(temp[3])  #'700'
        self.e414.setText(temp[4])  #'500000'
        self.e416.setText(temp[5])  #'-100'
        self.e417.setText(temp[6])  #'100'
        self.e418.setText(temp[7])  #'40'
        self.e422.setText(temp[8])  #'T1 Relaxation'
        self.e423.setText(temp[9])  #'FND in DI water'

        self.l420 = QLabel("")
        self.e415 = QLabel("")

        ## 20 grids
        self.gridLayout4.addWidget(self.l411,0,0,1,5)
        self.gridLayout4.addWidget(self.l412,1,0,1,5)
        self.gridLayout4.addWidget(self.l413,2,0,1,5)
        self.gridLayout4.addWidget(self.l414,3,0,1,5)
        self.gridLayout4.addWidget(self.l415,4,0,1,5)
        self.gridLayout4.addWidget(self.l416,5,0,1,5)
        self.gridLayout4.addWidget(self.l417,6,0,1,5)
        self.gridLayout4.addWidget(self.l418,7,0,1,5)
        self.gridLayout4.addWidget(self.l424,8,0,1,5)

        self.gridLayout4.addWidget(self.e411,0,5,1,3)
        self.gridLayout4.addWidget(self.e412,1,5,1,3)
        self.gridLayout4.addWidget(self.e413,2,5,1,3)
        self.gridLayout4.addWidget(self.e414,3,5,1,3)
        self.gridLayout4.addWidget(self.e415,4,5,1,3)
        self.gridLayout4.addWidget(self.e416,5,5,1,3)
        self.gridLayout4.addWidget(self.e417,6,5,1,3)
        self.gridLayout4.addWidget(self.e418,7,5,1,3)
        self.gridLayout4.addWidget(self.e424,8,5,1,3)

        self.gridLayout4.addWidget(self.b45, 9,5,1,3)

        self.gridLayout4.addWidget(self.b44, 0,9,1,10)
        self.gridLayout4.addWidget(self.l421,1,9,2,10)
        self.gridLayout4.addWidget(self.l422,3,9,1,2)
        self.gridLayout4.addWidget(self.l423,4,9,4,2)

        self.gridLayout4.addWidget(self.e422,3,11,1,8)  #title
        self.gridLayout4.addWidget(self.e423,4,11,5,8)   #legend
        self.gridLayout4.addWidget(self.l425,9,11,1,8)   #legend

        self.gridLayout4.addWidget(self.l420,0,8,1,1)

        #top box layout
        self.L41 = QHBoxLayout() #top main box
        self.L41.setContentsMargins(10, 40, 20, 10)

        self.L42 = QVBoxLayout()
        self.L43 = QVBoxLayout()
        self.L42.setContentsMargins(10, 0, 10, 0)
        self.L42.setContentsMargins(10, 0, 10, 0)
        self.L41.addLayout(self.L42, 40)  #x,y input
        self.L41.addLayout(self.L43, 60)  #values

        self.L44 = QVBoxLayout()
        self.L45 = QHBoxLayout()
        self.L46 = QHBoxLayout()
        self.L42.addLayout(self.L44, 10)
        self.L42.addLayout(self.L45, 80)  #x,y
        self.L42.addLayout(self.L46, 10)

        self.L47 = QVBoxLayout()
        self.L48 = QVBoxLayout()
        self.L45.addLayout(self.L47)  #x
        self.L45.addLayout(self.L48)  #y

        self.l406 = QLabel("Enter Fluorescence Data: \n  ○ data points separate by ↵ or space\n"
                           "  ○ multiple samples separate by , \n  ○ use Generate button to help with x")
        self.l406.setWordWrap(True)
        self.L44.addWidget(self.l406)

        self.l407 = QLabel("x")
        self.l407.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.l407.setWordWrap(True)
        self.e407 = QTextEdit()
        self.e407.setAcceptRichText(False)
        self.L47.addWidget(self.l407)
        self.L47.addWidget(self.e407)

        self.l408 = QLabel("y")
        self.l408.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.e408 = QTextEdit()
        self.e408.setAcceptRichText(False)
        self.L48.addWidget(self.l408)
        self.L48.addWidget(self.e408)

        self.L46.addWidget(self.l403)  #plot n samples
        self.L46.addWidget(self.l404)
        self.L46.addWidget(self.l405)
        self.L46.addStretch()  #layout only

        self.L49 = QHBoxLayout()
        self.L40 = QVBoxLayout()
        self.L43.addLayout(self.L49, 5)
        self.L43.addLayout(self.L40, 95)

        self.L49.addWidget(self.l401)
        self.L49.addWidget(self.l402)
        self.L40.addLayout(self.gridLayout4)

        self.topbox4.setLayout(self.L41)

        #### bottom ####
        self.bottomLayout4=QHBoxLayout()
        self.bottomL41 = QVBoxLayout()
        self.bottomL42 = QVBoxLayout()
        self.bottomL43 = QVBoxLayout()
        self.bottomL44 = QVBoxLayout()

        self.l41 = QLabel("Fit 1")
        self.l41.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL41.addWidget(self.l41)
        self.bottomL41.addWidget(self.b41)

        self.l42 = QLabel("Fit Multiple")
        self.l42.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL42.addWidget(self.l42)
        self.bottomL42.addWidget(self.b42)

        self.l43 = QLabel("Plot Raw")
        self.l43.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomL43.addWidget(self.l43)
        self.bottomL43.addWidget(self.b43)

        self.l44 = QLabel("Hint:")
        self.l45 = QLabel()
        self.l45.setStyleSheet(style.l02())
        self.l45.setAlignment(QtCore.Qt.AlignTop)
        self.l45.setWordWrap(True)
        self.l45.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.bottomL44.addWidget(self.l44, 10)
        self.bottomL44.addWidget(self.l45, 90)

        self.bottomLayout4.addLayout(self.bottomL41)
        self.bottomLayout4.addLayout(self.bottomL42)
        self.bottomLayout4.addLayout(self.bottomL43)
        self.bottomLayout4.addLayout(self.bottomL44)
        self.bottombox4.setLayout(self.bottomLayout4)


    def widget4(self):
        self.b41 = QToolButton()
        self.b41.setIcon(QIcon("icons/start1.png"))
        self.b41.setIconSize(QSize(50, 50))
        self.b41.setToolTip("Fit")
        self.b41.clicked.connect(self.func41)

        self.b42 = QToolButton()
        self.b42.setIcon(QIcon("icons/start2.png"))
        self.b42.setIconSize(QSize(50, 50))
        self.b42.setToolTip("Fit")
        self.b42.clicked.connect(self.func42)

        self.b43 = QToolButton()
        self.b43.setIcon(QIcon("icons/plot1.png"))
        self.b43.setIconSize(QSize(50, 50))
        self.b43.setToolTip("Plot Raw")
        self.b43.clicked.connect(self.func43)

        self.b44 = QPushButton("Generate x Values")
        self.b44.setToolTip("Generate x values based on start, step and stop")
        self.b44.clicked.connect(self.func44)

        self.b45 = QPushButton("Reset Values")
        self.b45.setToolTip("Reset to recommended values")
        self.b45.clicked.connect(self.func45)

########## other useful functions  ########

    def layout5(self):
        L5 = QHBoxLayout()
        self.box51 = QGroupBox("Calculate Coil Magnetic Field")
        self.box52 = QGroupBox("Trigger Generator")
        self.box53 = QGroupBox("Oscilloscope")
        self.box54 = QGroupBox("Other")
        self.box51.setStyleSheet(style.tab51())
        self.box52.setStyleSheet(style.tab52())
        self.box53.setStyleSheet(style.tab53())
        self.box54.setStyleSheet(style.tab54())

        ##### tab 51 #####
        self.l501 = QLabel("Coil Radius (cm)")
        self.l502 = QLabel("Turns")
        self.l503 = QLabel("Current (A)")
        self.e501 = QLineEdit()
        self.e501.setText('7')
        self.e502 = QLineEdit()
        self.e502.setText('135')
        self.e503 = QLineEdit()
        self.e503.setText('0')

        self.g51 = QGridLayout()
        self.g51.addWidget(self.l501, 0, 0)  #grid layout
        self.g51.addWidget(self.l502, 1, 0)
        self.g51.addWidget(self.l503, 2, 0)
        self.g51.addWidget(self.e501, 0, 1)
        self.g51.addWidget(self.e502, 1, 1)
        self.g51.addWidget(self.e503, 2, 1)


        ### all coils  ####
        self.l511 = QLabel("x Position (cm)\n(off center)")
        self.l512 = QLabel("Coil Distance (cm)")
        self.l513 = QLabel("Coil Gauge")
        self.l514 = QLabel("Resistances\n (ohm/1000ft)")
        self.e511 = QLineEdit()
        self.e511.setText('0')
        self.e512 = QLineEdit()
        self.e512.setText('10')
        self.e513 = QComboBox()
        self.e513.addItem("12")
        self.e513.addItems(["10", "13", "14", "20", "22", "24"])
        self.e514 = QLineEdit()
        self.e514.setText('1.588')

        self.l515 = QLabel("Wire Length (m)")
        self.l516 = QLabel("Wire Length (ft)")
        self.l517 = QLabel("Resistance (ohm)")
        self.l518 = QLabel("Voltage (V)")
        self.e515 = QLabel("N/A")
        self.e516 = QLabel("N/A")
        self.e517 = QLabel("N/A")
        self.e518 = QLabel("N/A")
        self.e515.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e515.setStyleSheet(style.label522())
        self.e516.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e516.setStyleSheet(style.label522())
        self.e517.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e517.setStyleSheet(style.label522())
        self.e518.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e518.setStyleSheet(style.label522())

        self.l519 = QLabel("Coil Constant (G/A)")
        self.l510 = QLabel("Field at x (G)")
        self.e519 = QLabel("13.0584")
        self.e510 = QLabel("0")
        self.e519.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e519.setStyleSheet(style.label522())
        self.e510.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e510.setStyleSheet(style.label522())

        self.g56 = QGridLayout()
        self.g56.addWidget(self.l511, 0, 0)
        self.g56.addWidget(self.l512, 1, 0)
        self.g56.addWidget(self.l513, 2, 0)
        self.g56.addWidget(self.l514, 3, 0)
        self.g56.addWidget(self.b53,  4, 0, 1, 2)

        self.g56.addWidget(self.l515, 5, 0)
        self.g56.addWidget(self.l516, 6, 0)
        self.g56.addWidget(self.l517, 7, 0)
        self.g56.addWidget(self.l518, 8, 0)
        self.g56.addWidget(self.l519, 9, 0)
        self.g56.addWidget(self.l510, 10, 0)

        self.g56.addWidget(self.e511, 0, 1)
        self.g56.addWidget(self.e512, 1, 1)
        self.g56.addWidget(self.e513, 2, 1)
        self.g56.addWidget(self.e514, 3, 1)

        self.g56.addWidget(self.e515, 5, 1)
        self.g56.addWidget(self.e516, 6, 1)
        self.g56.addWidget(self.e517, 7, 1)
        self.g56.addWidget(self.e518, 8, 1)
        self.g56.addWidget(self.e519, 9, 1)
        self.g56.addWidget(self.e510, 10, 1)

        ## hem coil ####
        self.g55 = QGridLayout()
        self.l551 = QLabel("From current calculate field:")
        self.l552 = QLabel("B (G)")
        self.e552 = QLabel('0')
        self.e552.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e552.setStyleSheet(style.label522())

        self.l553 = QLabel("From field calculate current:")
        self.l554 = QLabel("B (G)")
        self.l555 = QLabel("I (A)")
        self.e554 = QLineEdit()
        self.e554.setText('0')
        self.e555 = QLabel('0')
        self.e555.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.e555.setStyleSheet(style.label522())

        self.l550 = QLabel(" ")

        self.g55.addWidget(self.l551, 0, 0, 1, 2)
        self.g55.addWidget(self.b51,  1, 0, 1, 2)
        self.g55.addWidget(self.l552, 2, 0, 1, 1)
        self.g55.addWidget(self.e552, 2, 1, 1, 1)
        self.g55.addWidget(self.l550, 3, 0, 1, 1)

        self.g55.addWidget(self.l553, 4, 0, 1, 2)
        self.g55.addWidget(self.l554, 5, 0, 1, 1)
        self.g55.addWidget(self.e554, 5, 1, 1, 1)
        self.g55.addWidget(self.b52,  6, 0, 1, 2)
        self.g55.addWidget(self.l555, 7, 0, 1, 1)
        self.g55.addWidget(self.e555, 7, 1, 1, 1)


        ##### tab 52 trigger #####
        self.l521=QLabel("Trigger Pulse Frequency (Hz)")
        self.l522=QLabel("Trigger Pulse Period (ms)")
        self.l523=QLabel("Trigger Pulse Duty Cycle")
        self.l524=QLabel("Trigger Pulse Delay (s)")
        self.e521=QLineEdit()
        self.e521.setText('200')
        T=int(1000/int(self.e521.text()))
        self.e522=QLabel(str(T))
        self.e523=QLineEdit()
        self.e523.setText('0.1')
        self.e524=QLineEdit()
        self.e524.setText('0')
        self.l525=QLabel("")


        self.g52 = QGridLayout()
        self.g52.addWidget(self.l521, 0, 0)
        self.g52.addWidget(self.l522, 1, 0)
        self.g52.addWidget(self.l523, 2, 0)
        self.g52.addWidget(self.l524, 3, 0)
        self.g52.addWidget(self.b54,  4, 0)

        self.g52.addWidget(self.e521, 0, 1)
        self.g52.addWidget(self.e522, 1, 1)
        self.g52.addWidget(self.e523, 2, 1)
        self.g52.addWidget(self.e524, 3, 1)
        self.g52.addWidget(self.b55,  4, 1)
        self.g52.addWidget(self.l525,  5, 0, 1, 2)

        ##### tab 53 scope #############
        self.l531 = QLabel("Channel")
        self.l532 = QLabel("Filename")
        self.l533 = QLabel("Title")
        self.e531 = QComboBox()
        self.e531.addItems(["1", "2", "3", "4"])
        self.e532=QLineEdit()
        self.e532.setText('ys20123001')
        self.e533=QLineEdit()
        self.e533.setText("Infiniium Oscilloscope")
        self.e534 = QLabel("")

        self.g53 = QGridLayout()
        self.g53.addWidget(self.l531, 0, 0)
        self.g53.addWidget(self.l532, 1, 0)
        self.g53.addWidget(self.l533, 2, 0)
        self.g53.addWidget(self.e531, 0, 1)
        self.g53.addWidget(self.e532, 1, 1)
        self.g53.addWidget(self.e533, 2, 1)
        self.g53.addWidget(self.b56,  3, 1)
        self.g53.addWidget(self.e534, 4, 0)

        self.box55 = QGroupBox("Helmolz coil: R = d")
        self.box55.setStyleSheet(style.tab55())
        self.box56 = QGroupBox("General case")
        self.box56.setStyleSheet(style.tab55())

        #### overall layout  ######
        self.L5left  = QVBoxLayout()
        self.L5right = QVBoxLayout()
        L5.addLayout(self.L5left, 60)  # left: field
        L5.addLayout(self.L5right, 40)  # right: other
        self.tab5.setLayout(L5)

        self.L51  = QHBoxLayout()
        self.L511 = QVBoxLayout()
        self.L512 = QVBoxLayout()
        self.L513 = QHBoxLayout()
        self.L514 = QHBoxLayout()

        self.L52 = QVBoxLayout()
        self.L53 = QVBoxLayout()
        self.L54 = QVBoxLayout()

        self.box51.setLayout(self.L51)
        self.L51.addLayout(self.L511, 40)  #left
        self.L51.addLayout(self.L512, 60)  #right
        self.L511.setContentsMargins(10, 30, 0, 10)
        self.L512.setContentsMargins(0, 30, 10, 10)

        self.img3 = QLabel()
        self.pixmap3 = QPixmap('icons/coil.png')
        self.small3 = self.pixmap3.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.img3.setPixmap(self.small3) #small3
        self.img3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.l5111 = QLabel("Coil Geometry")
        self.l5111.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.L511.addWidget(self.img3, 40)
        self.L511.addWidget(self.l5111, 5)
        self.L511.addWidget(self.box55, 55)  #hem

        self.g51.setContentsMargins(20, 0, 20, 0)
        self.L512.addLayout(self.g51, 30)
        self.L512.addWidget(self.box56, 70)  #general

        self.g55.setContentsMargins(5, 20, 5, 5)
        self.g56.setContentsMargins(5, 20, 5, 5)
        self.L513.addLayout(self.g55)  #hem
        self.box55.setLayout(self.L513)
        self.L514.addLayout(self.g56)  #general
        self.box56.setLayout(self.L514)

        self.g52.setContentsMargins(5, 20, 5, 5)
        self.g53.setContentsMargins(5, 20, 5, 5)
        self.L52.addLayout(self.g52)  #trigger
        self.L53.addLayout(self.g53)  #scope
        self.box52.setLayout(self.L52)
        self.box53.setLayout(self.L53)
        self.box54.setLayout(self.L54)

        self.L5left.addWidget(self.box51)
        self.L5right.addWidget(self.box52, 40)  # trigger
        self.L5right.addWidget(self.box53, 30)  # scope
        self.L5right.addWidget(self.box54, 30)  # other

        self.l541 = QLabel("More to come...")
        self.L54.addWidget(self.l541)

        if(platform.system() == 'Darwin'):# 'Linux'  # or 'Windows'/'Darwin'
            self.b54.setEnabled(False)
            self.b55.setEnabled(False)
            self.l525.setText('National Instrument equipment not available on Mac.\n')
        if(platform.system() == 'Linux'):# 'Linux'  # or 'Windows'/'Darwin'
            self.b54.setEnabled(False)
            self.b55.setEnabled(False)
            self.l525.setText('National Instrument equipment not available on Linux.\n')


    def widget5(self):
        self.b51 = QPushButton("Calculate Field")
        self.b51.setToolTip("Field")
        self.b51.clicked.connect(self.func51)

        self.b52 = QPushButton("Calculate Current")
        self.b52.setToolTip("Field")
        self.b52.clicked.connect(self.func52)

        self.b53 = QPushButton("Calculate Coil Parameters")
        self.b53.setToolTip("For coil design")
        self.b53.clicked.connect(self.func53)

        self.b54 = QPushButton("Generate 1 Pulse")
        self.b54.setToolTip("")
        self.b54.clicked.connect(self.func54)

        self.b55 = QPushButton("Generate Continuously")
        self.b55.setToolTip("Generate pulse train")
        self.b55.clicked.connect(self.func55)

        self.b56 = QPushButton("Transfer Data")
        self.b56.setToolTip("Transfer spectrum of selected channel from scope to computer")
        self.b56.clicked.connect(self.func56)

#########################
####### FUNCTIONS #######
#########################

    def checkeq(self):
        rm = pyvisa.ResourceManager()
        equipment = rm.list_resources()
        eqlist=''.join(equipment)
        eqnum = len(eqlist)
        if eqnum == 0 :
            self.l02.setText('No equipment found.\n\n !  Please check if there is any USB, GBIP, Ethernet cables connected.')
        else:
            self.l02.setText(str(eqnum) + ' Equipment found:\n\n' + eqlist)


    def changefolder(self):
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self, 'Select an awesome directory')
        # print(foo_dir)
        self.l04.setText(foo_dir)


####### fluorescence ######
    def func11(self):
        devices = list_devices()
        if (len(devices)==0):
            self.l15.setText('Spectrometer is not connected.')
        else:
            level = int(self.e209.text())

            if os.path.isfile('par/par1.txt'):
                os.remove('par/par1.txt')
            with open('par/par1.txt', 'a') as f:
                f.write(self.e101.text() + '\n')
                f.write(self.e102.text() + '\n')
                f.write(self.e103.text() + '\n')
                f.write(self.e104.text() + '\n')
                f.write(self.e105.text() + '\n')

            self.b13.setEnabled(False)
            wavelength1 = int(self.e101.text())
            wavelength2 = int(self.e102.text())
            integ = int(self.e103.text())
            title = self. l105.text()

            # old_stdout = sys.stdout
            # sys.stdout = mystdout = StringIO()
            FlameS.FlameS_view(wavelength1, wavelength2, integ, title)
            # sys.stdout = old_stdout
            # self.l15.setText(mystdout.getvalue())
            # mystdout.close()
            self.l15.setText('Watch console output for real time updates.')

    def func12(self):
        self.l15.setText('Close Fluorescence Spectrum Window to Stop Acquisition.')


    def func13(self):
        devices = list_devices()
        if (len(devices)==0):
            self.l15.setText('Spectrometer is not connected.')
        else:
            folder = self.l04.text()
            filename = self.e104.text()
            if(os.path.isfile(folder + '/' + filename + ".csv")):
                mbox = QMessageBox.question(self, "Warning!", "File already exists and will be overwritten", QMessageBox.Ok | QMessageBox.Cancel)
                if mbox == QMessageBox.Cancel:
                    return

            wavelength1 = int(self.e101.text())
            wavelength2 = int(self.e102.text())
            integ = int(self.e103.text())
            title = self. e105.text()

            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            FlameS.FlameS_view(wavelength1, wavelength2, integ, folder, filename, title)
            sys.stdout = old_stdout
            self.l15.setText(mystdout.getvalue())
            mystdout.close()
            # self.l15.setText('Fluorescence spectrum has been saved as csv file in current folder.')

    def func14(self):
        folder = self.l04.text()
        filename = self.e104.text()
        title = self.e105.text()
        if not os.path.isfile(folder + '/' + filename +'.csv'):
            self.l15.setText('Fluorescence spectrum is not found in current folder.')
        elif not os.path.isfile(folder + '/' + filename +'wl.csv'):
            self.l15.setText('Wavelength file is not found in current folder.')
        else:
            replot.plotflu(folder, filename, title)
            self.l15.setText('Plot success!')



####### ODMR ######
    def func21(self):  #run ODMR
        folder = self.l04.text()
        filename = self.e218.text()
        title = self.e219.text()

        start = int(self.e201.text())
        stop = int(self.e202.text())
        step = int(self.e203.text())
        dwelltime = int(self.e204.text())
        scannum = int(self.e205.text())
        rate = int(self.e206.text())
        period = int(self.e207.text())
        duty_cycle = int(self.e208.text())
        level = int(self.e209.text())

        if os.path.isfile('par/par2.txt'):
            os.remove('par/par2.txt')
        with open('par/par2.txt', 'a') as f:
            f.write(self.e201.text() + '\n')
            f.write(self.e202.text() + '\n')
            f.write(self.e203.text() + '\n')
            f.write(self.e204.text() + '\n')
            f.write(self.e205.text() + '\n')
            f.write(self.e206.text() + '\n')
            f.write(self.e207.text() + '\n')
            f.write(self.e208.currentText() + '\n')
            f.write(self.e209.text() + '\n')
            f.write(self.e211.text() + '\n')
            f.write(self.e212.text() + '\n')
            f.write(self.e213.text() + '\n')
            f.write(self.e215.text() + '\n')
            f.write(self.e217.text() + '\n')
            f.write(self.e218.text() + '\n')
            f.write(self.e219.text() + '\n')
            f.write(self.l04.text() + '\n')

        SignalGen.Freqsweep(start, stop, step, dwelltime, level)

        if(platform.system() == 'Windows'):# 'Linux'  # or 'Windows'/'Darwin'
            import ODMRch2
            self.l25.setText('Watch console output for real time updates.')
            ODMRch2.ODMR(start, stop, step, dwelltime, rate, scannum, period, duty_cycle, filename, folder, title)


    def func22(self):  #stop
        self.l25.setText('Press Enter to stop current data acquisition.')

    def func23(self):  #replot
        folder = self.l04.text()
        filename = self.e218.text()

        if not os.path.isfile(folder + '/' + filename +'.csv'):
            self.l25.setText('File is not found in current folder.')
        else:
            title = self.e219.text()
            start = int(self.e201.text())
            stop = int(self.e202.text())
            step = int(self.e203.text())
            dwelltime = int(self.e204.text())
            rate = int(self.e206.text())

            replot.plotO(start, stop, step, dwelltime, rate, filename, folder, title)
            self.l25.setText('Plot success!')

    def func24(self): #send current to power supply
        field = float(self.e211.text())
        cc = float(self.e212.text())
        resi = float(self.e213.text())
        if cc <= 0:
            self.l25.setText('Coil constant value error')
        elif resi <=0:
            self.l25.setText('Coil resistance value error')
        else:
            current = field / cc
            current = round(current, 4)
            volti = resi * current
            volti = round(volti, 4)
            if current > 10 or current < -10:
                self.l25.setText('Current cannot exceed 10 A.')
            elif volti >20 or volti < -20:
                self.l25.setText('Voltage cannot exceed 20 V.')
            else:
                self.e215.setText(str(current))
                self.e217.setText(str(volti))
                #function to send I   #####################!!!!!!
                self.l25.setText('Field set successfully.')

                if current >=9.5 or current <= -9.5:
                    self.l25.setText("Field set. High current risk!\n "
                                 "Please don't exceed 20 min and watch for messages on power supply.")


    def func25(self): #send 0 current to power supply
        self.e211.setText('0')
        self.e215.setText('0')
        self.e217.setText('0')
        # function to send 0 I   #####################!!!!!!
        self.l25.setText('Field turned off.')
        pass

    def func26(self):  #reset values
        self.e201.setText('2700')
        self.e202.setText('3000')
        self.e203.setText('1')
        self.e204.setText('100')
        self.e205.setText('1')
        self.e206.setText('5000')
        self.e207.setText('1')
        self.e208.setCurrentText('0.2')
        self.e209.setText('12')

        self.e211.setText('0')
        self.e212.setText('13.0584')
        self.e213.setText('0.8')
        self.e215.setText('0')
        self.e217.setText('0')
        self.e218.setText('ys')
        self.e219.setText('Diamond')

        # current = float(self.e211.text()) / float(self.e212.text())
        # self.e214 = QLabel(str(current))



####### T1 ######
    def func31(self):   #run T1

        t1 = time.time()
        folder = self.l04.text()
        freq = int(self.e311.text())
        level = int(self.e312.text())
        SignalGen.Freqset(freq, level)

        freq_NI = int(self.e301.text())
        delay = 0
        duty_cycle = 0.1

        if(platform.system() == 'Windows'):# 'Linux'  # or 'Windows'/'Darwin'
            import NI
            NI.continuetrigger(freq_NI, delay, duty_cycle)

        period1 = int(1000000/freq_NI)  #us
        period2 = period1
        pulse1 = int(self.e303.text())
        pulse2 = int(self.e304.text())
        uwpulse = int(self.e305.text())
        gate = int(self.e306.text())

        gap1 = int(self.e313.text())   #start
        if (self.l314.isChecked()):
            gap2 = int(self.e314.currentText())   #step
            gap3 = int(self.e315.text())   #stop
            gaps = np.arange(gap1, gap2+gap3, gap2)
        else:
            gaps = [gap1]

        TSET = int(self.e316.text())
        cycle = int(self.e317.text())
        div = int(self.e318.text())
        scan = int(self.e319.text())

        y = []
        for i in range(scan):
            for gap in gaps:
                # print("gap is: " + str(gap))
                AWG.AWG(period1, period2, pulse1, pulse2, gap, uwpulse)
                N = 0
                for j in range(div):
                    if self.q:
                        # return
                        pass
                    else:
                        # print (j)
                        N += PhotonCnt.Photoncounter(TSET, pulse1, gap, gate, cycle)
                print(N)
                y.append(N)
                time.sleep(1)
            print('\nscan #', i + 1, 'done\n')

        t2 = time.time()
        print("time is: ", t2 - t1)

        self.l35 = QLabel(' '.join([str(elem) for elem in y]))

        plt.plot(gaps, y)
        plt.title('T1 Measurement')
        plt.xlabel('Gap between Laser Pulses, us')
        plt.ylabel('Fluorescence Counts')
        plt.show()


    def func32(self):  #stop experiment... not working yet
        # self.q = True
        sys.exit()


    def func33(self):
        folder = self.e319.text()
        filename = self.e320.text()

        if os.path.isfile(folder + '/' + filename +'.txt'):
            self.l25.setText('File already exist, please re-name.')
        else:
            text_file = open(filename +".txt", "w")
            text_file.write(self.e35.text())
            text_file.close()
            # self.l35.setText('Fluorescence counts data saved as txt file.')


    def func34(self):  #reset values
        self.e301.setText('200')
        T = int(1000 / int(self.e301.text()))
        self.e302 = QLabel(str(T))
        self.e303.setText('30')
        self.e304.setText('2')
        self.e305.setText('50')
        self.e306.setCurrentText('0.9')
        self.e311.setText('2877')
        self.e312.setText('15')
        self.e313.setText('50')
        self.e314.setCurrentText('50')
        self.e315.setText('400')
        self.e316.setText('9E3')
        self.e317.setText('2000')
        self.e318.setText('1')
        self.e319.setText('1')
        self.e320.setText('T1')


####### Tab4  curve fitting ######
    # #check input value
    def func41(self): #fit 1 sample

        p0 = [int(self.e416.text()), int(self.e417.text()), int(self.e418.text())]
        text = self.e407.toPlainText()
        flulist=text.split()
        x=[]
        for i in range(len(flulist)):
            x.append(int(flulist[i]))

        text = self.e408.toPlainText()
        flulist=text.split()
        y=[]
        for i in range(len(flulist)):
            y.append(int(flulist[i]))

        iter = int(self.e414.text())
        title = self.e422.text()
        legend1 = self.e423.toPlainText()

        self.l404.setText('1')
        if (self.l401.isChecked()):
            T1v = fit2.fit2one(p0, x, y, iter, legend1, title, color='#1f77b4')
        else:
            T1v = fit1.fit1one(p0, x, y, iter, legend1, title, color='#1f77b4')
        self.l45.setText('T1 value:\n'+ str(T1v))


    def func42(self):  #plot multiple samples
        p0 = [int(self.e416.text()), int(self.e417.text()), int(self.e418.text())]

        text = self.e407.toPlainText()
        list1 = text.split(',')
        n = len(list1)
        x=[]
        for i in range(n):
            flulist=list1[i].split()
            x1=[]
            for i in range(len(flulist)):
                x1.append(int(flulist[i]))
            x.append(x1)

        text = self.e408.toPlainText()
        list1 = text.split(',')
        n = len(list1)
        y=[]
        for i in range(n):
            flulist=list1[i].split()
            y1=[]
            for i in range(len(flulist)):
                y1.append(int(flulist[i]))
            y.append(y1)

        iter = int(self.e414.text())
        title = self.e422.text()
        color = ['#1f77b4', 'orange', 'red', 'green']  # 'Default blue'

        text = self.e423.toPlainText()
        list1 = text.splitlines()
        legend1 = []
        for i in range(len(list1)):
            legend1.append(list1[i])

        self.l404.setText(str(n))
        if (self.l401.isChecked()):
            T1v = fit2.fit2n(p0, x, y, iter, legend1, title, color, n)
        else:
            T1v = fit1.fit1one(p0, x, y, iter, legend1, title, color='#1f77b4')
        T1value = ' '.join([str(elem) for elem in T1v])
        self.l45.setText('T1 value:\n'+ T1value)


    def func43(self):  #replot

        text = self.e407.toPlainText()
        flulist = text.split()
        x = []
        for i in range(len(flulist)):
            x.append(int(flulist[i]))

        text = self.e408.toPlainText()
        flulist=text.split()
        y=[]
        for i in range(len(flulist)):
            y.append(int(flulist[i]))

        title = self.e422.text()
        legend1 = self.e423.toPlainText()

        plt.plot(x, y, 'o')
        plt.legend([legend1])
        plt.xlabel('Time between double pulses, µs')
        plt.ylabel('Fluorescence Counts, AU')
        plt.title(title)
        plt.show()


    def func44(self):  #generate x values
        gap1 = int(self.e411.text())   #start
        # if (self.l314.isChecked()):
        gap2 = int(self.e412.currentText())   #step
        gap3 = int(self.e413.text())   #stop
        x = np.arange(gap1, gap2+gap3, gap2)
        x1 = str(x)
        self.l421.setText(x1[1:-1])

    def func45(self):  #reset values
        self.l404.setCurrentText('2')
        self.e411.setText('250')
        self.e412.setCurrentText('50')
        self.e413.setText('700')
        self.e414.setText('500000')
        self.e416.setText('-100')
        self.e417.setText('100')
        self.e418.setText('40')
        self.e422.setText('T1 Relaxation')
        self.e423.setText('FND in DI Water')

    def func51(self):
        R = float(self.e501.text()) * 0.01  #
        n = int(self.e502.text())
        I = float(self.e503.text())
        B = coil.hemI(n, R, I)
        B = round(B, 2)
        self.e552.setText(str(B))

    def func52(self):
        R = float(self.e501.text()) * 0.01
        n = int(self.e502.text())
        B = float(self.e554.text())
        I = coil.hemB(n, R, B)
        I = round(I, 2)
        self.e555.setText(str(I))

    def func53(self):
        R = float(self.e501.text()) * 0.01
        n = int(self.e502.text())
        I = float(self.e503.text())
        x = float(self.e511.text()) *0.01
        d = float(self.e512.text()) *0.01
        resi = float(self.e514.text())
        cc, B, lenm, lenft, vol, resis = coil.coils(x, d, n, R, I, resi)
        print(cc)
        print(B)

        self.e515.setText(str(lenm))
        self.e516.setText(str(lenft))
        self.e517.setText(str(resis))
        self.e518.setText(str(vol))
        self.e519.setText(str(cc))
        self.e510.setText(str(B))

    def func54(self):
        freq_NI = int(self.e521.text())
        delay = float(self.e522.text())
        duty_cycle = float(self.e523.text())
        if(platform.system() == 'Windows'):# 'Linux'  # or 'Windows'/'Darwin'
            import NI
            NI.singletrigger(freq_NI, delay, duty_cycle)

    def func55(self):
        freq_NI = int(self.e521.text())
        delay = float(self.e522.text())
        duty_cycle = float(self.e523.text())
        if (platform.system() == 'Windows'):  # 'Linux'  # or 'Windows'/'Darwin'
            import NI
            self.l525.setText('Generating pulse train. Press Enter to interrupt')
            NI.continuetrigger(freq_NI, delay, duty_cycle)

    def func56(self):
        channel = int(self.e531.text())
        filename = int(self.e531.text())
        title = int(self.e531.text())
        Oscilloscope.scoperec(channel, filename, title)
        self.l534.setText('Spectrum on the Oscilloscope has been successfully transfered to your computer!')



    def exitFunc(self):
        mbox=QMessageBox.information(self,"Warning","Are you sure to exit?",QMessageBox.No|QMessageBox.Yes,QMessageBox.Yes)
        if mbox==QMessageBox.Yes:

            if os.path.isfile('par/par0.txt'):
                os.remove('par/par0.txt')
            with open('par/par0.txt', 'a') as f:
                f.write(str(self.tabs.currentIndex()) + '\n')
                f.write(self.l04.text() + '\n')
            sys.exit()

    def btnFunc(self,btn):
        if btn.text()=="New":
            print("You clicked new button")
        elif btn.text() =="Open":
            print("You clicked open button")
        else:
            print("You clicked save button")



def main():
    app = QApplication(sys.argv)
    programWindow = ProgramWindow()

    programWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



    #        self.L31.addStretch()  #layout only
