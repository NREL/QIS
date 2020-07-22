# -----------Test 1 - Can we communicate with the Prologix adapter using pyvisa directly?---------------------------
#TODO:
# 1. Poll the event status register (*ESR?), the Event Status Enable Register (*ESE?), the status byte register
# # (*STB?, also serial poll), and service request enable (*SRE?) (controls which bits of status byte generate a service
# # request)
# 2. Incorporate RSQ/SRQ
# 3. Add occasional close visa so it doesn't break

import pyvisa
from pyvisa.constants import StopBits, VI_READ_BUF_DISCARD, VI_WRITE_BUF_DISCARD
import sys
import time
import numpy as np

rm = pyvisa.ResourceManager()
rm.list_resources()

prologix = rm.open_resource('ASRL6::INSTR')

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)

prologix_version = prologix.query('++ver\n')      # returns the version string of the prologix GPIB-USB controller
print(prologix_version)

address_test = prologix.query('++addr\n')   # This command should query the GPIB address (so response should be 8 or
print(address_test)                         # something) This can be used to set the GPIB address: '++addr 8\r'

prologix.write('++addr 8\n')

term_char = prologix.query('++eos\n')    # Query the GPIB termination character setting
print(term_char)                           #

spoll = prologix.query('++spoll\n')  # should return a 7-bit numeric value (i.e. 0 to 255). Decomposing this into
print(spoll)                         # individual Bits tells the status of each parameter. (serial poll)

spoll = int(spoll)
# Convert the serial poll to binary
spoll_bits = '{0:08b}'.format(spoll)
print(spoll_bits)
print('76543210')

prologix.write('++eos 2\n')       # The SR844 manual says must be terminated with line feed (2) or EOI

prologix.write('++auto 1\n')                   # This seems to solve below problem

prologix.write('OUTX 1\n')

identity = prologix.query('*IDN?\n')
print(identity)
# -----------------------------------------Read Binary data------------------------------------------------------------
spoll = prologix.query('++spoll\n')             # Why is spoll breaking things?
print('spoll: ' + str(spoll))

# Clear the buffers
prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)
prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)
prologix.write('REST\n')

prologix.timeout = 3000

display_buff_pts = prologix.query('SPTS?\n')         # Check that the buffer is empty
print('Display buff pts: ' + str(display_buff_pts))
print('b_in_b: ' + str(prologix.bytes_in_buffer))

prologix.write('SRAT 13\n')                          # Set the data sample rate to 512 Hz
rate_index = prologix.query('SRAT?\n')
print('rate index: ' + str(rate_index))              # Check that it worked

prologix.write('STRT\n')                             # Start a scan
time.sleep(10)                                        # Wait 3 seconds (the instrument should still be scanning)

prologix.write('PAUS\n')                             # Paus the scan

display_buff_pts = prologix.query('SPTS?\n')         # Check how many points were collected (should be ~1536) (was 1543 twice in a row)
print('Display buff pts: ' + str(display_buff_pts))  # Was 1538 on the SR844
display_buff_pts = int(display_buff_pts)



## TRCL Read (fastest read)
prologix.timeout = 20000

t0 = time.time()
prologix.write('TRCL? 2,0,%d\n' % display_buff_pts)
test = []
for ii in range(0, display_buff_pts):
    try:
        appendix = prologix.read_bytes(4)
        test.append(appendix)
    except:
        print(sys.exc_info()[:])
        break
print('elapsed time: ' + str(time.time() - t0))   # TRCB- 1.52 seconds to transmit 1543 values (4 bytes each) (~1000Hz)
print('length of test: ' + str(len(test)))        # Using TRCL took 1.109 seconds to transmit 1538 values(4 bytes each)

print('b_in_b ' + str(prologix.bytes_in_buffer))

## Now convert these values into something useful:
mantissas_ch1 = []
exponents_ch1 = []
values_ch1 = []
for ii in range(0, len(test)):
    mantissas_ch1.append(int.from_bytes(test[ii][0:2], 'little', signed=True))  # Get bytes 0 and 1 (not 2)
    exponents_ch1.append(int.from_bytes(test[ii][2:4], 'little', signed=True))  # Get bytes 2 and 3 (4 Doesn't Exist)
    # mantissas_ch1_ints.append(int.from_bytes)
    values_ch1.append(mantissas_ch1[ii] * 2**(exponents_ch1[ii] - 124))
values_ch1_arr = np.array(values_ch1)
print('time after conversion: ' + str(time.time() - t0)) # Took 10.22 seconds to convert 15352 points (X only)
# The value conversion plus a check of bytes in buffer added only 0.035 seconds for 15352 points

fig, ax = plt.subplots()
ax.plot(values_ch1_arr)
plt.show()

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
ascii_results = prologix.query('TRCA? 1,0,%d\n' % display_buff_pts)
dTa = time.time() - t0a
print('ascii time: ' + str(dTa))
print(ascii_results)
# Result (took 5.95 seconds) (took 10.15 seconds second time around (with nonzero values)
# On SR844 took 8.967 seconds with nonzero values

# -------------------------------------------------------------------------------
# --------------------- I got responses by doing this: -------------------------
# -------------------------------------------------------------------------------

# prologix.bytes_in_buffer        # Check if there is already some shit in the buffer
# prologix.write('TRCB? 0,%d\n' % display_buff_pts)
# # This doesn't incorporate a delay to allow the buffer to build up is the problem
# x = prologix.bytes_in_buffer
# # for ii in range(1, 1000):    # this didn't work (maybe b_in_b doen'st update quickly)
# #     time.sleep(0.1)
# #     y = prologix.bytes_in_buffer
# #     if y == x:
# #         break
# time.sleep(8)
# b_in_b = prologix.bytes_in_buffer
# test = prologix.read_bytes(b_in_b)
# print(prologix.bytes_in_buffer)  # This worked but I am not getting all of the bytes...

# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ THIS WORKS: ----------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

print(prologix.bytes_in_buffer)        # Check if there is already some shit in the buffer
display_buff_pts = prologix.query('SPTS?\n')
print('Display buff pts: ' + str(display_buff_pts))
display_buff_pts = int(display_buff_pts)


prologix.timeout = 2000

prologix.write('TRCB? 1,0,%d\n' % display_buff_pts)
test = []
t0 = time.time()
for ii in range(1, 1539):
    try:
        appendix = prologix.read_bytes(4)
        test.append(appendix)
        print(appendix)
        print(ii)
    except:
        print(sys.exc_info()[:])
        break
print('elapsed time: ' + str(time.time() - t0))   # Took 1.52 seconds to transmit 1543 values (4 bytes each) (~1000Hz)
print('length of test: ' + str(len(test)))        # With SR844 took 1.604 seconds for 1538 values

b_in_b = prologix.bytes_in_buffer
# test = prologix.read_bytes(b_in_b)
print(prologix.bytes_in_buffer)

# --------------------------------------- Fast Data transfer -----------------------------------------------

spoll = prologix.query('++spoll\n')
print(spoll)

prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)
prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)
prologix.write('REST\n')                               # Clear the buffer (should also clear BOTH buffers with pyvisa)

display_buff_pts = int(prologix.query('SPTS?\n'))        # Check that the buffer is empty
print('Display buff pts: ' + str(display_buff_pts))

prologix.write('SRAT 10\n')                          # Set the data sample rate to 64 Hz (go up to 13/512 if works)
rate_index = prologix.query('SRAT?\n')
print('rate index: ' + str(rate_index))              # Check that it worked

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IT WORKED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

FastBuf = []                           # Set up an array to contain the data
prologix.timeout = 15000
sample_rate = 64
nSamples = 10*sample_rate

prologix.write('FAST1; STRD\n')
prologix.write('++auto 1\n')

t0 = time.time()
for ii in range(0, nSamples*2):            # This will by 10 seconds at 64 Hz
    FastBuf.append(prologix.read_bytes(2))      # Reading X and Y separately seems simpler
    print(ii)

prologix.write('PAUS\n')
dTfast = time.time() - t0
print(str(dTfast) + str(' seconds'))
prologix.timeout = 3000                              # Set timeout short again

print('b_in_b: ' + str(prologix.bytes_in_buffer))

prologix.flush(VI_WRITE_BUF_DISCARD)                # Clear any remaining buffers before any new commands
prologix.flush(VI_READ_BUF_DISCARD)
prologix.flush(VI_WRITE_BUF_DISCARD)
prologix.flush(VI_READ_BUF_DISCARD)

display_buff_pts = int(prologix.query('SPTS?\n'))
print('Display buff pts: ' + str(display_buff_pts))

prologix.write('REST\n')

# This took 10.520 seconds for range(0,640) points at 64Hz (should take 10 seconds)
# Took 10.524 seconds for range(0, 10240) points at 512 Hz

# It seems that the byte order is little endian, so to convert a pair of bytes:
# int_result = int.from_bytes(FastBuf[ii], 'little, signed=True)

# ------------------- Convert the values to integers -------------------------------
values_conv = []
for ii in range(0, len(FastBuf)):
    values_conv.append(int.from_bytes(FastBuf[ii], 'little', signed=True))
values_floats = np.array(values_conv) / 29788           # 29788 corresponds to +Full_scale (sensitivity/Expand)

X = values_floats[::2]
Y = values_floats[1::2]

ave_X = np.average(X)
ave_Y = np.average(Y)
# For converting 1280 points (640 X,Y pairs), time required was 0.00399 seconds (could probably do this in real time)
# For converting 10240 points (5120 X,Y pairs), time required was 0.032 seconds
still_fast = prologix.query('FAST?\n')               # Check if fast read was automatically turned off
print('Fast? (0 is no) ' + str(still_fast))

# -------- IT WORKED ----------- 10.497 seconds total taken

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


# open close test
prologix = rm.open_resource('ASRL6::INSTR')
ver_test = prologix.query('++ver\n')
print(ver_test)
identity = prologix.query('*IDN?\n')
print(identity)
prologix.before_close()
prologix.close()
