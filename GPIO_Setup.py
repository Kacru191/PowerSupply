#! /usr/bin/env python

import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)

# Dictionary of the GPIO pins
# We can loop through them using list(GPIO_Pins.values())
# or we can reference a pin by name using GPIO_Pins["name"]
# which will return the pin number as an integer
GPIO_Pins = {
	"VPT_FLT": 4,
	"VPT_EN": 17,
	"VUSB_FLT": 27,
	"VUSB_EN": 22,
	"ZPI_FLT": 5,
	"ZPI_EN": 6,
	"DPI_FLT": 13,
	"DPI_EN": 19,
	"28V_FLT": 26,
	"28V_EN": 23, 
	"24V_EN": 25,
	"15V_FLT": 12,
	"5V_EN": 16,
	"5V_FLT": 20,
	"15V_EN": 21 }

PE1 = 0x23		# 0001 - Port Expander 1 Address
PE2 = 0x24		# 0110 - Port Expander 2 Address
GPIOA = 0x12	# GPIOA Register Address on Port Expander OLATA register for outputs
GPIOB = 0x13	# GPIOB Register Address on Port Expander

def GPA_Output(Device):
	# Sets all eight bits in the GPIOA register to 0 (output)
	bus.write_byte_data(Device,0x00,0x00)
	bus.write_byte_data(Device, GPIOA, 0)
	bus.write_byte_data(Device,GPIOA,254)


def GPB_Output(Device):
	# Sets all eight bits in the GPIOB register to 0 (output)
	bus.write_byte_data(Device, GPIOB, 0x00)


def Initialize():
	try:
		# Set Port Expander 1's GPA registers to output
		GPA_Output(PE1)
		print("Port Expander 1 GPIOA initialized")
	except:
		print("Error setting PE1 GPA register to output")

	try:
		# Set Port Expander 1's GPB registers to output
		GPB_Output(PE1)
		print("Port Expander 1 GPIOB initialized")
	except:
		print("Error setting PE1 GPB register to output")

	try:
		# Set Port Expander 2's GPA registers to output
		GPA_Output(PE2)
		print("Port Expander 2 GPIOA initialized")
	except:
		print("Error setting PE2 GPA register to output")

	try:
		# Set Port Expander 2's GPB registers to output
		GPB_Output(PE2)
		print("Port Expander 2 GPIOb initialized")
	except:
		print("Error setting PE2 GPB register to output")

	try:
		# Cycle through the list of GPIO pins
		# and set each one as an OUTPUT
		for pin in list(GPIO_Pins.values()):
			GPIO.setup(pin, GPIO.OUT)

		print("GPIO pins initialized")

	except:
		print("Error setting GPIO pins as output")


Initialize()
