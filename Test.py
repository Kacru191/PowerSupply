import sys
import RPi.GPIO as GPIO #initialize GPIOs on RPi
import time
import smbus


bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ADDR = 0x33 
WRITE_CMD = 0x0
READ_CMD = 0x1

#print str (singlebyte)
#bus.write_i2c_block_data(ADDR, WRITE_CMD, [0x80, 0x0f])

byte1 = bus.read_i2c_block_data(ADDR,READ_CMD,1)
print str (byte1)


byte2 = bus.read_i2c_block_data(ADDR,READ_CMD,2)
byte3 = bus.read_i2c_block_data(ADDR,READ_CMD,3)
bytedata = (byte2 << 8) + byte3 

print str(bytedata)

bytemath = bytedata/10.0
print str (bytemath)