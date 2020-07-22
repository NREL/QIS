# -----------Test 1 - Can we communicate with the Prologix adapter using pyvisa directly?---------------------------

import pyvisa
from pyvisa.constants import StopBits, VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD
import sys

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL3::INSTR')

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)

prologix_version = prologix.query('++ver\n')      # returns the version string of the prologix GPIB-USB controller
print(prologix_version)

address_test = prologix.query('++addr\n')   # This command should query the GPIB address (so response should be 8 or
print(address_test)                         # something) This can be used to set the GPIB address: '++addr 8\r'


term_char = prologix.query('++eos\n')    # Query the GPIB termination character setting
print(term_char)                           # "When data from host is received over USB, all non-escaped LF, CR, and
# ESC characters are removed and GPIB terminators, as specified by this command, are appended before sending the data to
# instruments ++eos [0|1|2|3] to set e.g. '++eos 0\r' to set to CR+LF, 1 for CR, 2 for LF, 3 for no appended terminator
# I think this implies that adding the \r manually does nothing since it will be removed and
# either be added or not added automatically depending on the eos state.

spoll = prologix.query('++spoll\n')  # should return a 7-bit numeric value (i.e. 0 to 255). Decomposing this into
print(spoll)                         # individual Bits tells the status of each parameter. (serial poll)

spoll = int(spoll)
# Convert the serial poll to binary
spoll_bits = '{0:08b}'.format(spoll)
print(spoll_bits)
print('76543210')

# The following were used for the mono driver immediately after open_resource
# self.comm.write_termination = None
# self.comm.read_termination = None
#
# # Clear the read and write buffers so you start with a clean slate
# self.comm.flush(VI_WRITE_BUF_DISCARD)
# self.comm.flush(VI_READ_BUF_DISCARD)

prologix.before_close()
prologix.close()

# ---------------------------------- If the rest of the tests fail, try thing 2 ---------------------------------------
# Thing 2 - check if there is a different set of drivers that allows direct GPIB communication (as in the computer
# Recognizes the device as a GPIB port)

# --------------------------------------- Instrument Commands -----------------------------------------------

import pyvisa
from pyvisa.constants import StopBits, VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD
import sys

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL3::INSTR')

prologix_version = prologix.query('++ver\n')
print(prologix_version)

address_test = prologix.query('++addr\n')
print(address_test)

prologix.write('++eos 2\n')       # The SR844 manual says must be terminated with line feed (2) or EOI
                                  # (separate command)

spoll = prologix.query('++spoll\n')
print(spoll)

is_auto_on = prologix.query('++auto\n')
print(is_auto_on)

prologix.write('++auto 1\n')                   # This seems to solve below problem
# Now add in instrument commands:

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)

identification = prologix.query('*IDN?\n')     # This did not work the first time! (timeout)
print(identification)

display_buff_pts = prologix.query('SPTS?\n')
print('Display buff pts: ' + str(display_buff_pts))

prologix.before_close()
prologix.close()

# Thing 3 - Poll the event status register (*ESR?), the Event Status Enable Register (*ESE?), the status byte register
# (*STB?, also serial poll), and service request enable (*SRE?) (controls which bits of status byte generate a service
# request)

# Notes - ReQuested service (RQS) is bit 6 of the status byte

# -----------------------------------------Read Binary data------------------------------------------------------------
import pyvisa
import time

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL3::INSTR')

prologix_version = prologix.query('++ver\n')
print(prologix_version)

address_test = prologix.query('++addr\n')
print(address_test)

prologix.write('++eos 2\n')       # The SR844 manual says must be terminated with line feed (2) or EOI
                              # (separate command)

spoll = prologix.query('++spoll\n')
print(spoll)

prologix.write('++auto 1\n')                   # This seems to solve below problem
# Now add in instrument commands:

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)             # Clear the buffers

# Now add in instrument commands:
identification = prologix.query('*IDN?\n')
print(identification)

prologix.write('REST\n')

display_buff_pts = prologix.query('SPTS?\n')         # Check that the buffer is empty
print('Display buff pts: ' + str(display_buff_pts))

prologix.write('SRAT 13\n')                          # Set the data sample rate to 512 Hz
rate_index = prologix.query('SRAT?\n')
print('rate index: ' + str(rate_index))              # Check that it worked

prologix.write('STRT\n')                             # Start a scan
time.sleep(3)                                        # Wait 3 seconds (the instrument should still be scanning)

prologix.write('PAUS\n')                             # Paus the scan

display_buff_pts = prologix.query('SPTS?\n')         # Check how many points were collected (should be ~1536) (was 1543 twice in a row)
print('Display buff pts: ' + str(display_buff_pts))
display_buff_pts = int(display_buff_pts)

prologix.timeout = 20000

# t0a = time.time()
# ascii_results = prologix.query('TRCA? 1,0,%d\n' % display_buff_pts)
# dTa = time.time() - t0a
# print('ascii time: ' + str(dTa))
# print(ascii_results)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# FORMAT IS SLIGHTLY DIFFERENT FOR SR810!!!! CHANNEL 1 IS ASSUMED!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
prologix.timeout = 20000
t0a = time.time()
ascii_results = prologix.query('TRCA? 0,%d\n' % display_buff_pts)
dTa = time.time() - t0a
print('ascii time: ' + str(dTa))
print(ascii_results)
# Result (took 5.95 seconds) (took 10.15 seconds second time around (with nonzero values)


# I predict these will fail - THEFIRST ONE DID AT LEAST
# t0b = time.time()
# binary_results = prologix.query('TRCB? 0,%d\n' % display_buff_pts)
# dTb = time.time() - t0b
# print('binary time: ' + str(dTb))
# print(binary_results)

# t0c = time.time()
# unnorm_binary_results = prologix.query('TRCL? 1,0,%d\n' % display_buff_pts)
# dTc = time.time() - t0c
# print('unnorm binary time: ' + str(dTc))
# print(unnorm_binary_results)

# When the above fail: (These failed also)
# t0b = time.time()
# binary_results = prologix.query_binary_values('TRCB? 0,%d\n' % display_buff_pts, datatype='d', is_big_endian=False) # If f does not work, try 'd'
# dTb = time.time() - t0b
# print('binary time: ' + str(dTb))
# print(binary_results)
#
# t0b = time.time()
# binary_results = prologix.query_bytes('TRCB? 0,%d\n' % display_buff_pts, datatype='d', is_big_endian=False) # If f does not work, try 'd'
# dTb = time.time() - t0b
# print('binary time: ' + str(dTb))
# print(binary_results)

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)   # NEed to do this more than once sometimes (do it in a loop and check b_in_b

# -------------------------------------------------------------------------------
# --------------------- I got responses by doing this: -------------------------
# -------------------------------------------------------------------------------

prologix.bytes_in_buffer        # Check if there is already some shit in the buffer
prologix.write('TRCB? 0,%d\n' % display_buff_pts)
# This doesn't incorporate a delay to allow the buffer to build up is the problem
x = prologix.bytes_in_buffer
# for ii in range(1, 1000):    # this didn't work (maybe b_in_b doen'st update quickly)
#     time.sleep(0.1)
#     y = prologix.bytes_in_buffer
#     if y == x:
#         break
time.sleep(8)
b_in_b = prologix.bytes_in_buffer
test = prologix.read_bytes(b_in_b)
print(prologix.bytes_in_buffer)  # This worked but I am not getting all of the bytes...

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ THIS WORKS: ----------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# display_buff_pts = int(display_buff_pts)
print(prologix.bytes_in_buffer)        # Check if there is already some shit in the buffer
prologix.write('TRCB? 0,%d\n' % display_buff_pts)
# This doesn't incorporate a delay to allow the buffer to build up is the problem
# x = prologix.bytes_in_buffer

test = []
t0 = time.time()
for ii in range(1, 1543):
    try:
        appendix = prologix.read_bytes(4)
        test.append(appendix)
        print(appendix)
        print(ii)
    except:
        print(sys.exc_info()[:])
        break
print('elapsed time: ' + str(time.time() - t0))   # Took 1.52 seconds to transmit 1543 values (4 bytes each) (~1000Hz)
print('length of test: ' + str(len(test)))

time.sleep(8)
b_in_b = prologix.bytes_in_buffer
test = prologix.read_bytes(b_in_b)
print(prologix.bytes_in_buffer)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# # I don't know if this will work: (but who cares about this format anyways)
# t0c = time.time()
# unnorm_binary_results = prologix.query_binary_values('TRCL? 1,0,%d\n' % display_buff_pts, datatype='h', is_big_endian=False)
# dTc = time.time() - t0c
# print('unnorm binary time: ' + str(dTc))
# print(unnorm_binary_results)

prologix.before_close()
prologix.close()
# --------------------------------------- Multiple Inline Commands -----------------------------------------------
import pyvisa
import time

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL5::INSTR')

prologix_version = prologix.query('++ver\n')
print(prologix_version)

address_test = prologix.query('++addr\n')
print(address_test)

term_char = prologix.query('++eos 2\n')       # The SR844 manual says must be terminated with line feed (2) or EOI
print(term_char)                              # (separate command)

spoll = prologix.query('++spoll\n')
print(spoll)

# Now add in instrument commands:
identification = prologix.query('*IDN?\n')
print(identification)

prologix.write('REST; SPTS?; SRAT?\n')        # This does work but the buffer should be cleared first (and multiple
                                            # reads may need to be done)
readout = prologix.read()
print(readout)

readout2 = prologix.query('REST; SPTS?; SRAT?\n')
print(readout2)

# If the above don't work, see if it's because they're mixed commands/queries

prologix.before_close()
prologix.close()

# --------------------------------------- Listener/Talker stuff -----------------------------------------------
import pyvisa
import time
import numpy as np

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL5::INSTR')

prologix_version = prologix.query('++ver\n')
print(prologix_version)

address_test = prologix.query('++addr\n')
print(address_test)

term_char = prologix.query('++eos 2\n')       # The SR844 manual says must be terminated with line feed (2) or EOI
print(term_char)                              # (separate command)

spoll = prologix.query('++spoll\n')
print(spoll)

# Now add in instrument commands:
identification = prologix.query('*IDN?\n')
print(identification)

prologix.write('REST\n')                               # Clear the buffer (should also clear BOTH buffers with pyvisa)

display_buff_pts = prologix.query('SPTS?\n')         # Check that the buffer is empty
print('Display buff pts: ' + str(display_buff_pts))

prologix.write('SRAT 10\n')                          # Set the data sample rate to 64 Hz (go up to 13/512 if works)
rate_index = prologix.query('SRAT?\n')
print('rate index: ' + str(rate_index))              # Check that it worked

FastBuf = []                           # Set up an array to contain the data

prologix.timeout = 15000                             # Set timeout very long

# I think '++auto 1' should make the instrument a talker and therefore the computer/Prologix a listener)
# The length of the loop determines how long to record data for. Output is
# 2x16-bit signed integers (X and Y) per sample, assume same endianness as before
#  if read_binary values   doesn't work try something more like this:
# FastBuf[ii:(ii + nBytes)] = prologix.read_bytes(64)  # Will have to play with chunk length here (4 bytes: X and Y?)
# read_raw may also be a good troubleshooting function

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IT WORKED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
prologix.write('FAST1; STRD\n')
prologix.write('++auto 1\n')

t0 = time.time()
nBytes = 640
for ii in range(0, 640):            # This will by 10 seconds at 64 Hz
    FastBuf.append(prologix.read_bytes(4))

dTfast = time.time() - t0
print(dTfast + str(' seconds'))
# IT might be nice to find a way to check how many bytes were read (or are waiting to be read)

prologix.write('PAUS\n')
prologix.timeout = 3000                              # Set timeout short again

# -------- IT WORKED ----------- 10.497 seconds total taken

still_fast = prologix.query('FAST?\n')               # Check if fast read was automatically turned off
print('Fast? (0 is no) ' + str(still_fast))

display_buff_pts = prologix.query('SPTS?\n')         # Check how many points were collected (should be ~1536)
print('Display buff pts: ' + str(display_buff_pts))

len_fastBuf = len(FastBuf)                           # IF this worked then len_fastBuf == display_buff_pts
print('len_fastBuf: ' + str(len_fastBuf))

print(str(FastBuf))

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IT WORKED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#
# Now you'll have to convert the values into arrays of X and Y (should be easy relatively speaking)

prologix.before_close()
prologix.close()
