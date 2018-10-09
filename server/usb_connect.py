import serial
import io
import sys
import time

device = sys.argv[1]

if device == None:
    device = '/dev/ttyUSB0'

ser = serial.Serial(device)  # open serial port
ser.baudrate = 1152000
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1  # timeout in seconds
ser.xonxoff = False
ser.inter_byte_timeout = None
print(ser.name)         # check which port was really used

ser.flushInput()
ser.flushOutput()

separator_start = '____start____'
separator_end = '____end____'
def read_data(ser, buf=b''):
    # Read enough data for a message
    while separator_start not in buf:
        buf += ser.read(ser.inWaiting())

    # Remove the garbage before the message start position
    start_pos = buf.find(separator_start)
    buf = buf[start_pos:]
    
    cnt = 0
    # Wait for the whole message
    while not (separator_start in buf and separator_end in buf):
        buf += ser.read(ser.inWaiting())
        cnt += 1

    # Locate message separators
    end_pos = buf.find(separator_end)
    start_pos = buf.find(separator_start)

    # Save the beginning of the next message if any
    new_msg = buf[end_pos + len(separator_end):]
    
    # Extract the message
    msg = buf[start_pos+len(separator_start):end_pos]
    
    return [msg, new_msg]

i = 0
line = []
msgs = [b'', b'']
running = True
try:
    while True:
        msgs = read_data(ser, msgs[1])
        msg = msgs[0]
        if msg == 'save_image':
            print('save command')
        else:
            i += 1
            ct = time.localtime()
            ct_str = '{0}{1}{2}_{3}{4}{5}'.format(ct.tm_year, ct.tm_mon, ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec)
            f = open("images/img_{1}_{0}_{2}.jpg".format(i, ser.name.replace('/', '_'), ct_str), 'wb')  # open in binary
            f.write(msg)
            f.close()
            print(ct_str)
            print('image saved', len(msg))
        
except:
    ser.close()  # close port
    raise
