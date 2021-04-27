# Rohde&schewarz 100kHz-12.75GHz signal generator
# manual: https://www.rohde-schwarz.com/us/manual/r-s-smb100a-rf-and-microwave-signal-generator-operating-manual-manuals-gb1_78701-29347.html

import pyvisa

def RSf(freq):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x0AAD::0x0054::181799::INSTR')    #USB-B cable
    # inst=rm.open_resource('GPIB0::28::INSTR')    #GBIP cable
    inst.write('FREQ '+str(freq)+' MHz')   ##'SOUR1: FREQ 2.8 GHz' SOUR can be omitted

def RSp(level):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x0AAD::0x0054::181799::INSTR')    #USB-B cable
    # inst=rm.open_resource('GPIB0::28::INSTR')    #GBIP cable
    inst.write('POW '+str(level))

def Freqsweep(start, stop, step, dwell, level):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource('USB0::0x0AAD::0x0054::181799::INSTR')    #USB-B cable
    # inst=rm.open_resource('GPIB0::28::INSTR')    #GBIP cable
    inst.write('FREQ:MODE SWE')  ##sets the frequency sweep mode
    inst.write('TRIG:FSW:SOUR EXT')    #trigger=external single
    # inst.write('TRIG:FSW:SOUR SING')    #trigger=single sweep
    inst.write('FREQ:STAR '+str(start)+' MHz')
    inst.write('FREQ:STOP '+str(stop)+' MHz')
    inst.write('SWE:FREQ:STEP '+str(step)+' MHz')
    inst.write('SWE:DWEL '+str(dwell)+' ms')
    inst.write('POW ' + str(level))
    inst.write('SWE:EXEC')


if __name__ == "__main__":
    folder = '/Users/yshi2/Documents/2020.8.19/'
    filename = 'ys20081901'
    freq = 2875  # MHz
    level = -11   # dBm
    start = 2700 # MHz
    stop = 3000  # MHz
    step = 1     # MHz
    dwell = 100  # ms

    Freqsweep(start, stop, step, dwell, level)



    ## set parameters use 'inst.write()'
    # ## read current state
    # inst.write('FREQ 2.876 GHz')   ##'SOUR1: FREQ 2.8 GHz' SOUR can be omitted
    # # x=inst.query('FREQ?')        ##read value
    # # x=inst.query('SWE:RUNN?')    ##0 | 1 | OFF | ON
    # # print(x)
    #
    # inst.write('FREQ:MODE SWE')  ##sets the frequency sweep mode
    # inst.write('FREQ:STAR 2820 MHz')
    # inst.write('FREQ:STOP 2920 MHz')
    #
    # inst.write('FREQ:CENT 2870 MHz')
    # inst.write('FREQ:SPAN 400 MHz')
    # inst.write('SWE:FREQ:STEP 10 MHz')  ##'SWE:FREQ:STEP:LIN 1MHz'
    # # inst.write('SWE:POIN 101')        #will change step:lin
    #
    # inst.write('POW 30')   #power, level
    #
    # # inst.write('TRIG:FSW:SOUR AUTO')      #display not update, but works AUTO, SING, EXT, EAUT
    # # inst.write('TRIG:FSW:SOUR SING')      #need the exec command
    # # inst.write('TRIG:FSW')                #starts a single RF frequency sweep.
    # #
    # # inst.write('SOUR:SWE:FREQ:MODE AUTO') ##sets the triggered sweep mode, i.e. a trigger is required to start sweep
    # # inst.write('SOUR:FREQ:MODE SWE')
    # inst.write('SWE:EXEC')                  ##alone will work, SOUR:SWE:FREQ:EXEC can be omit

