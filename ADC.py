

#import board
#import busio
import sys
#i2c = busio.I2C(board.SCL, board.SDA) #initializing the I2C connection for the port expanders 

import RPi.GPIO as GPIO #initialize GPIOs on RPi
import time
import smbus


bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Dictionary of the GPIO pins
# We can loop through them using list(GPIO_Pins.values())
# or we can reference a pin by name using GPIO_Pins["name"]
# which will return the pin number as an integer


ADDR = 0x33		# Address of ADC
SETUP = 0x80		# Setup bytes [REG][SEL2][SEL1][SEL0][CLK][BIP/UNI][RST][X]
					#
CONFIG = 0xf0 	# Config bytes [REG][SCAN1][SCAN0][CS3][CS2][CS1][CS0][SGL/DIF]
					# Config bytes that scans AIN0-AIN7 for single-ended  

READ = 0x01
WRITE = 0x00

AIN_0 = 0000
AIN_1 = 0001
AIN_2 = 0010
AIN_3 = 0011
AIN_4 = 0100
AIN_5 = 0101
AIN_6 = 0110
AIN_7 = 0111


def Setup():
	bus.write_byte_data(ADDR,WRITE,SETUP)
	print("setup")

def Config(data):
	bus.write_byte_data(ADDR,WRITE,data)
	print("config")

def Read_Output(channel):
	result = 0x0000
	print str(result)
	configbyte = ((channel <<1) & B00001110) | B01100001
	print str(configbyte)
	Config(configbyte)
	bus.read_byte_data(ADDR, READ, CONFIG)

def Initialize():
		Setup()
		print("setup completed")
		Config(CONFIG)
		print("config completed")
		while i < 8:
			volt = Read_Output(i)
			print str(volt)
			++i

while (1):

	Initialize()


		