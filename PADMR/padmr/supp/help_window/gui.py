# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Ryan/AppData/Local/Temp/help_window_UI_20200729OpKrYJ.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 698)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Help"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">I. Overview</span><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    This control software was built to control a Photoinduced Absorption Detected Magnetic Resonance (PADMR) experiment. Collectively, the instruments used to construct this experiment are capable of several other experiments as well, so the intent was to design a software which is capable of treating many experimental parameters alternately as either a constant or as an independent variable. It is our opinion at this time that data collection beyond 2 independent (scanned) variables will be too time consuming to warrant it\'s inclusion in the program. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\"> </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">At this time (2020-08), our intention is to use the SR844 Lock-in Amplifier output as the experimental observable, the physical significance of which depends on which parameter(s) is (are) modulated. For the primary experiment (PADMR), our intention is to use a dual modulation scheme, in which the optical excitation intensity and microwave power are simultaneously amplitude modulated at different frequencies. See section III.ZZZ for more details on this experiment.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\"> </span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">This help section is broken into XX parts:</span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I. Overview</span><span style=\" font-size:8pt; font-style:italic;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">II. Single Instrument Control </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    We have developed a GUI based control program for each instrument involved in the experiment. These can be accessed via the &quot;Instruments&quot; dropdown in the Main Window Menu Bar and are intended to allow quick control of specific experimental parameters without performing a full experiment. These programs can also be opened separately and can be found in YY.</span><span style=\" font-size:8pt;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">III. Experiment Control</span><span style=\" font-size:8pt; font-style:italic;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Since this software is built to control several different experiments, each one which occurred to us at the time of software development has a subsection describing important concepts of the experiment as well as how to carry out that experiment and interpret data.</span><span style=\" font-size:11pt;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">II. Single Instrument Control</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">II.a - General</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">II.b - Monochromator</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">II.c - Lock-in Amplifier (SR844)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    &quot;</span><span style=\" font-size:11pt;\">As a general rule, try to use Low Noise reserve modes if possible. Only increase the reserve if overloads occur. This will provide the best output signal-to-noise and have the least coherent pickup (see below).&quot; - From SR844 Manual</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">II.d - Montana Instruments Cryostat/Magnet</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">ii.e - Pump Laser Control</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">ii.f - ???</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">III. Experiment Control</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:16pt; font-weight:600;\">III.a - General Comments / Proper Lock-in Usage</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">    </span><span style=\" font-family:\'Calibri\'; font-size:12pt;\">See section II.c for discussion of lock-in usage</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt;\">    Ideally we will allow the user to scan ANY of the parameters and view the lock-in output. All other parameters will be set beforehand. This should be easy to accomplish though there are still some complications with respect to what is being modulated.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:16pt; font-weight:600;\">III.b - xy Experiments</span><span style=\" font-size:16pt; font-weight:600;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-style:italic;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:14pt; font-weight:600; font-style:italic;\">III.b.i - Optical Absorption (UV/Vis/NIR)</span><span style=\" font-size:14pt; font-weight:600; font-style:italic;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Independent Variable - Probe Wavelength</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Modulated Variable - Probe Amplitude (Mechanical Chopper)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Constants - Temperature, Magnetic Field</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Not Used - RF, Optical Excitation</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-style:italic;\">Concepts -</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    A standard optical absorption experiment measures the intensity of light transmitted through a sample (</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">) and compares that to the intensity of light transmitted through a blank (</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">). This is often reported as Absorbance, A = -log(</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I/I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">), though technically this equation assumes that reflectance = zero, which is not necessarily a good assumption with solid phase samples (which generally have nonzero reflectance which may not be effectively blanked). Under some circumstances, a qualitative absorption spectrum (absorbance versus probe wavelength) can still be useful. Further, it may be useful to check the absorbance at a single wavelength occasionally during an experiment to monitor sample integrity.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    In the simplest absorption spectrometer, monochromatic light is passed through a sample, and it\'s intensity is measured (as a voltage) with a photodiode. This value is called </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">. The same is done in the presence of a blank, and the resulting voltage is called </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">. Assuming the voltage varies linearly with incident light intensity, these values can be used directly in the equation above. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Another method of measuring optical absorption involves using a lock-in amplifier. The probe light is mechanically chopped at some low frequency (e.g. 500 Hz). The chopped light is then passed through a sample (or blank) and subsequently detected by a photodiode (with built-in transimpedance amplifier). Whereas in the simple spectrometer the photodiode signal was essentially constant with respect to time, here it is modulated at the chopping frequency (the shape of the modulation approaches a square wave). The photodiode voltage highs correspond to fully unblocked probe light (</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">or</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\"> I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">), and the lows correspond to fully blocked probe light (baseline photodiode voltage). If this signal is fed into a lock-in amplifier, and the chopper signal is fed in as the reference frequency, the lock-in amplifier will measure the amplitude of the AC component of the signal. The magnitude (R) of the lock-in amplifier output will correspond to  (</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I - </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">baseline)/C if a sample is present, or  (</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\"> - </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">baseline)/C if a blank is present. C is a constant that arises from the math of lock-in amplification and is not discussed here, but it does not vary with probe wavelength </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-weight:600;\">and probably does not vary with modulation frequency (this I am still unsure of</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">). When measured in this way, the lock-in amplifier therefore provides the same information as direct measurement of the photodiode voltage, just scaled by the normalization constant C (note that the photodiode voltage is also not a true intensity, but is scaled by some constant). If Absorbance is then calculated using the lock-in voltage with a sample and blank in place as </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\"> and </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">I</span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic; vertical-align:sub;\">0</span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">, respectively, the constants cancel.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    Often it is desirable to measure the absorption </span><span style=\" font-family:\'Calibri\'; font-size:11pt; font-style:italic;\">spectrum, </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">in which the absorbance of the sample is measured. In this case, the probe wavelength is scanned, and a lock-in measurement taken at each wavelength. The experiment is repeated with a blank, and the resulting lock-in amplitudes are converted to an absorbance at each wavelength.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">Practice -</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">    --Under Construction--</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:14pt; font-weight:600; font-style:italic;\">III.b.ii - Lifetime Measurements</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt;\">        </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">Independent Variable - Pump Modulation Frequency</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Constants - Probe Wavelength, Temperature, Magnetic Field</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Not Used - RF</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:14pt; font-weight:600; font-style:italic;\">III.b.iii - Photoinduced Absorption (Optical) Spectrum</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt;\">        </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">Independent Variable - Probe Wavelength</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Constants - Pump Modulation Frequency, Temperature, Magnetic Field</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Not Used - RF</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:14pt; font-weight:600; font-style:italic;\">III.b.iii - PADMR (Microwave) Spectrum</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt;\">        </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">Independent Variable - Static Magnetic Field </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Constants - Pump Modulation Frequency, Temperature</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:11pt;\">        Not Used - RF</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt;\">    </span><span style=\" font-family:\'Calibri\'; font-size:11pt;\">This experiment is akin to Field-Swept EPR, except the detection is via lifetime alteration of excited states as a result of RF exposure, rather than microwave power reflected from the cavity.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Calibri\'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:16pt; font-weight:600;\">III.c - xyz Experiments</span><span style=\" font-size:16pt; font-weight:600;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">IV. Software Layout</span><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">a. How to make changes to the code</span><span style=\" font-size:12pt; font-style:italic;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">    </span><span style=\" font-size:11pt; font-style:italic;\">--UNDER CONSTRUCTION--</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">V. Resources</span><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">a. Python</span><span style=\" font-size:12pt; font-style:italic;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">b. ODMR Experiments</span><span style=\" font-size:12pt; font-style:italic;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:12pt; font-style:italic;\">c. Instrument Control Manuals</span><span style=\" font-size:12pt; font-style:italic;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:18pt; font-weight:600; text-decoration: underline;\">VI. Known Improvements that could be made</span><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\"> </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-style:italic;\">Software developed by Ryan Dill</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-style:italic;\">Experimental Design and Construction by Obadiah Reid, Ryan Dill, Justin Johnson, Brian Fluegel, Gajadhar Joshi, and Yilin Shi. </span></p></body></html>"))