#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	REAL
XTYP	IDX
YTYP	NODATA
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	1024
XMIN	2800.000000
XWID	1400.000000
*
*	Documentational Text:
*
TITL	'ys20071612'
IRNAM	'Intensity'
XNAM	'Field'
IRUNI	''
XUNI	'G'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    xuser
DATE    07/16/20
TIME    15:54:24
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    CW
OXS1    IADC
AXS1    B0VL
AXS2    NONE
AXS3    
A1CT    0.35
A1SW    0.14
MWFQ    9.381953e+09
MWPW    0.001003
AVGS    2
SPTP    0.08192
RCAG    30
RCHM    1
B0MA    0.001
B0MF    100000
RCPH    0.0
RCOF    0.0
A1RS    1024
RCTC    0.32768
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     fieldCtrl, 1.0

AllegroMode        False
CenterField        3500.00 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            2.000000
MeasuringHall      False
SetToSampleG       False
StaticFieldMon     3480.000 G
SweepDirection     Up
SweepWidth         1400.0 G
WidthTM            200.0 G

.DVC     fieldSweep, 1.0


.DVC     freqCounter, 1.0

FrequencyMon       9.381953 GHz
QMonitBridge       On

.DVC     mwBridge, 1.0

AcqFineTuning      Each Slice Scan
AcqScanFTuning     Off
AcqSliceFTuning    Off
BridgeCalib        100.0
Power              1.003 mW
PowerAtten         23.0 dB
QValue             6600

.DVC     recorder, 1.0

BaselineCorr       Off
NbScansAcc         2
NbScansDone        2
NbScansToDo        2
ReplaceMode        Off
SmoothMode         Auto
SmoothPoints       1

.DVC     scanEnd, 1.0


.DVC     signalChannel, 1.0

AFCTrap            True
AllegroMode        False
AllowShortCt       False
Calibrated         True
ConvTime           81.92 ms
DModAFCTrap        True
DModAmp            1.00 G
DModCalibrated     True
DModDetectSCT      First
DModEliDelay       1.0 us
DModExtLockIn      False
DModExtTrigger     False
DModFieldMod       First
DModGain           60 dB
DModHighPass       True
DModIntegrator     True
DModModOutput      Internal
DModSignalInput    Internal
DModTimeConst      1.28 ms
DoubleModFreq      5.00 kHz
DoubleModPhase     0.0
DoubleMode         False
EliDelay           1.0 us
EnableImag         Disable
ExtLockIn          False
ExtTrigger         False
Gain               30 dB
Harmonic           1
HighPass           True
Integrator         True
IsCalibExp         False
ModAmp             10.000 G
ModFreq            100.00 kHz
ModInput           Internal
ModOutput          Internal
ModPhase           0.0
Offset             0.0 %
QuadMode           False
QuadPhase          90.0
Resolution         1024
Resonator          1
SctNorm            True
SctRevision        SCT
SignalInput        Internal
SpuExtension       False
SweepTime          83.89 s
TimeConst          327.68 ms
TimeExp            False
TuneCaps           39

*
************************************************************
