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

def twos_comp(val, bits):
	if (val & (1 << (bits - 1))) != 0:
		val = val - (1 << bits)
	return val

bus.write_i2c_block_data(ADDR, WRITE_CMD, [0x0])
print "Writing setup and configuration bits"
bus.write_i2c_block_data(ADDR, WRITE_CMD, [0x80, 0x0f])
#sudo i2cdetect -y 0
val = bus.read_i2c_block_data(ADDR,READ_CMD,2)
print "Raw bytes: " + str(val)
bytedata = (val[0] << 4) | (val[1]>>5)
print "Shifted bits: " + str(bytedata) 

#print str(bytedata) 

bytedata = twos_comp(bytedata, 10)
print("Two's complement: " + str(bytedata))