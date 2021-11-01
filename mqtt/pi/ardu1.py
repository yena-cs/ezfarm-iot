import re
import serial
import time
port = "/dev/ttyUSB0"
port3 = "/dev/ttyACM0"
    
ser = serial.Serial(port, 9600)
ser3 = serial.Serial(port3, 9600)
ser.flushInput()
ser3.flushInput()
s1 = input()
s2 = input()
while True:
    if(s1 == '1'):
        c1 = '1'
        c1 = c1.encode('utf-8')
        ser.write(c1)
    if(s2 == '1'):
        c2 = '1'
        c2 = c2.encode('utf-8')
        ser3.write(c2)

    time.sleep(3)
