

#import board
#import busio
import adafruit_mcp230xx
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
EN_Pins = { # Enables on RPi GPIOs

	"VPT_EN": 17,
	"VUSB_EN": 22,
	"ZPI_EN": 6,
	"DPI_EN": 19,
	"28V_EN": 23,
	"24V_EN": 25,
	"5V_EN": 16,
	"15V_EN": 21 }

FLT_Pins = { #Faults on RPi GPIOs

	"VPT_FLT": 4,
	"VUSB_FLT": 27,
	"ZPI_FLT": 5,
	"DPI_FLT": 13,
	"28V_FLT": 26,
	"15V_FLT": 12,
	"5V_FLT": 20,}

GPA1_EN = { #Enables on Port expander #1A

	"PTX_EN":7,
	"VTX_EN":5}

GPA1_FLT ={ #Faults on Port expander #1A

	"PTX_FLT":6,
	"VTX_FLT":4}

GPB1_EN={ #Enables on Port Expander #1B

	"PL_EN":6,
	"DL_EN":4,
	"OBRD_EN":2,
	"DPT_EN":0,}

GPB1_FLT={ #Faults on Port Expander #1B

	"PL_FLT":7,
	"DL_FLT":5,
	"OBRD_FLT":3,
	"DPT_FLT":1}
GPB2_EN={ #Enables on Port Expander #1B

	"MD1_EN":3,
	"MD2_EN":1,
	"OPTO48V_EN":4}

GPB2_FLT={ #Faults on Port Expander #1B

	"MD2_EN":2,
	"MD1_EN":0,
	"OPTO48V_FLT":5}

PE1 = 0x24		# 0001 - Port Expander 1 Address
PE2 = 0x23		# 0110 - Port Expander 2 Address
GPA = 0x12 		# GPA register address
GPB = 0x13 		# GPB register address
IODIRA = 0x00		# Direction of pins for GPA
IODIRB = 0x01		# Direction of pins for GPB
HIGHPINS = 0xFF		# All pins high
LOWPINS = 0x00		# All pins low

flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0 
flag5 = 0

GP_0 = 0x01
GP_1 = 0x02
GP_2 = 0x04
GP_3 = 0x08
GP_4 = 0x10
GP_5 = 0x20
GP_6 = 0x40
GP_7 = 0x80

# Variables to hold current pin state
PINSTATE_A = 0x00		#Pin state for PE1 GPA
PINSTATE_B = 0x00	#Pin state for PE1 GPB
PINSTATE_C  = 0x00 	#Pin state for PE2 GPB


def Change_PinState(Device,GPAB,state):
	bus.write_byte_data(Device,GPAB,state)
	#PINSTATE = Highlow
	#Device: Port Expander #1 or Port Expander #2
	#GP_AB: GPA or GPB
	#HighLow: Drive pin High or Low

def GPA_Output(Device,PINSTATE):
	# Sets all eight bits in the GPIOA register to 0 (output)
	bus.write_byte_data(Device,IODIRA,0x00)
	Change_PinState(Device,GPA,PINSTATE) #write all pins low "off"
	#bus.write_byte_data(Device,GPIOA,Allpins) #write all high
	#print str(PINSTATE)

def GPB_Output(Device,PINSTATE):
	# Sets all eight bits in the GPIOB register to 0 (output)
	bus.write_byte_data(Device, IODIRB, 0x00)
	Change_PinState(Device,GPB,PINSTATE) # writes all pins low "off"
	#bus.write_byte_data(Device, GPIOB, Allpins)
	#print str(PINSTATE)

def Initialize():
	try:
		# Set Port Expander 1's GPA registers to output
		GPA_Output(PE1,PINSTATE_A)
		print("Port Expander 1 GPIOA initialized")
		time.sleep(1)
	except:
		print("Error setting PE1 GPA register to output")
		print(sys.exc_info()[0])

	try:
		# Set Port Expander 1's GPB registers to output
		GPB_Output(PE1,PINSTATE_B)
		print("Port Expander 1 GPIOB initialized")
		time.sleep(1)
	except:
		print("Error setting PE1 GPB register to output")
		print(sys.exc_info()[0])

	try:
		# Set Port Expander 2's GPA registers to output
		GPA_Output(PE2,PINSTATE_C)
		print("Port Expander 2 GPIOA initialized")
		time.sleep(1)
	except:
		print str(PINSTATE_C)
		print("Error setting PE2 GPA register to output")
		print(sys.exc_info()[0])

	try:
		# Set Port Expander 2's GPB registers to output
		GPB_Output(PE2,PINSTATE_C)
		print("Port Expander 2 GPIOb initialized")
		time.sleep(1)
	except:
		print("Error setting PE2 GPB register to output")
		print(sys.exc_info()[0])

	try:
		# Cycle through the list of GPIO pins on RPi
		# and set each one as an OUTPUT
		for pin in list(EN_Pins.values()):
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin,GPIO.LOW) #write all GPIOs low "off"
		time.sleep(1)
		print("GPIO pins initialized")

	except:
		print("Error setting GPIO pins as output")
		print(sys.exc_info()[0])
def Power_Off():
	Change_PinState(PE1,GPA,LOWPINS)
	Change_PinState(PE1,GPB,LOWPINS)
	Change_PinState(PE2,GPA,LOWPINS)
	Change_PinState(PE2,GPB,LOWPINS)
	GPIO.cleanup()

#True or false prompt to simulate button press
def get_bool(prompt):
	while True:
		try:
			return {"true":True,"false":False}[raw_input(prompt).lower()]
		except KeyError:
			print "Invalid input please enter True or False"
		
while (1):
	#button on for initalization, turns on converters 
	print "######################\n"
	print " 'a' = Initialize/De-initialize\n"
	print " 'b' = Zack's System\n"
	print " 'c' = Vicki's Sysyem\n"
	print " 'd' = Danyle's System\n"
	print " 'e' = Peter's Sysem\n"
	print " 'f' = Shutdown whole system\n"
	print "#####################\n"
	keypress =raw_input("Press a button:\n")

	if keypress == "a":
			if flag1 == 1:
				print("\Beginning Shutdown...\n")
				#Initialize()
				#time.sleep(1)
				#enable all converter pins 
				#print("Pinstate: %s" % str(PINSTATE))
	
				PINSTATE_C -= GP_4
				#print("Pinstate is now: %s" % hex(PINSTATE))
				#print str(PINSTATE)
				print("Setting 5V_EN to LOW")
				GPIO.output(EN_Pins["5V_EN"],GPIO.LOW)
				print "5V Converter Disabled...\n"
				time.sleep(1)
	
				print("Setting 15V_EN to LOW")
				GPIO.output(EN_Pins["15V_EN"],GPIO.LOW)
				print "15V Converter Disabled...\n"
				time.sleep(1)
		
				print("Setting 24V_EN to LOW")
				GPIO.output(EN_Pins["24V_EN"],GPIO.LOW)
				print "24V Converter Disabled...\n"
				time.sleep(1)
		
				print("Setting 28V_EN to LOW")
				GPIO.output(EN_Pins["28V_EN"],GPIO.LOW)
				print "28V Converter Disabled...\n"
				time.sleep(1)
		
				print("Setting 48V_EN to LOW")
				#print("Pinstate: %s" % str(PINSTATEC))
				#print("Value type in PINSTATE: %s" % type(PINSTATEC))
				#bus.write_byte_data(PE2,GPB,PINSTATEC)
				Change_PinState(PE2,GPB,PINSTATE_C)
				print "48V ConverterDisabled...\n"
				time.sleep(1)

				flag1 = 0
			else:
				print("\nBeginning initialization...\n")
				Initialize()
				time.sleep(1)
				#enable all converter pins 
				#print("Pinstate: %s" % str(PINSTATE))
	
				PINSTATE_C += GP_4
				#print("Pinstate is now: %s" % hex(PINSTATE))
				#print str(PINSTATE)
				print("Setting 5V_EN to HIGH")
				GPIO.output(EN_Pins["5V_EN"],GPIO.HIGH)
				print "5V Converter Enabled...\n"
				time.sleep(1)
	
				print("Setting 15V_EN to HIGH")
				GPIO.output(EN_Pins["15V_EN"],GPIO.HIGH)
				print "15V Converter Enabled...\n"
				time.sleep(1)
		
				print("Setting 24V_EN to HIGH")
				GPIO.output(EN_Pins["24V_EN"],GPIO.HIGH)
				print "24V Converter Enabled...\n"
				time.sleep(1)
		
				print("Setting 28V_EN to HIGH")
				GPIO.output(EN_Pins["28V_EN"],GPIO.HIGH)
				print "28V Converter Enabled...\n"
				time.sleep(1)
		
				print("Setting 48V_EN to HIGH")
				#print("Pinstate: %s" % str(PINSTATEC))
				#print("Value type in PINSTATE: %s" % type(PINSTATEC))
				#bus.write_byte_data(PE2,GPB,PINSTATEC)
				Change_PinState(PE2,GPB,PINSTATE_C)
				print "48V Converter Enabled...\n"
				time.sleep(1)

				print "\n...Intialization complete...\n" 
				flag1 = 1

#################################################
################################################
	##button_state2 = get_bool("\nTrue2 or False2\n")

	elif keypress is 'b':
		if flag2 == 1:
			print "Powering Down Zack's system...\n"

			PINSTATE_C -= GP_1
			Change_PinState(PE2,GPB,PINSTATE_C)
			print "Steering Drive Down\n" 
			time.sleep(1)

			PINSTATE_C -= GP_3
			Change_PinState(PE2,GPB,PINSTATE_C)
			print "Motor Drive Down\n" 
			time.sleep(1)

			GPIO.output(EN_Pins["ZPI_EN"],GPIO.LOW)
			print "Zack's Pi Down\n"
			time.sleep(1)
			
			print "\n???Powered OFF???\n" 
			
			flag2 = 0
		else:
			print "\n...Powering on Zack's system...\n"
			GPIO.output(EN_Pins["ZPI_EN"],GPIO.HIGH)
			print "Zack's Pi On\n"
			time.sleep(1)

			PINSTATE_C += GP_3
			Change_PinState(PE2,GPB,PINSTATE_C)
			print "Motor Drive On\n" 
			time.sleep(1)

			PINSTATE_C += GP_1
			Change_PinState(PE2,GPB,PINSTATE_C)
			print "Steering Drive On\n" 
			time.sleep(1)

			flag2 = 1

			print "\n!!!Power on Successful!!!\n" 

############################################
	#button_state3 = get_bool("\nTrue3 or False3\n")

	elif keypress is 'c':
		if flag3 == 1:
			print "\n...Powering down Vicki's system...\n" 
			GPIO.output(EN_Pins["VPT_EN"],GPIO.LOW)
			print "Vicki's Pan & Tilt Down\n"
			time.sleep(1)

			GPIO.output(EN_Pins["VUSB_EN"],GPIO.LOW)
			print "Vicki's USB Down\n"
			time.sleep(1)

			PINSTATE_A -= GP_5
			Change_PinState(PE1,GPA,PINSTATE_A)
			print "Vicki's TX2 Down\n" 
			time.sleep(1)

			print "???Powered OFF???" 

			flag3 = 0
		else:
			print "\n...Powering on Vicki's system...\n" 
			GPIO.output(EN_Pins["VPT_EN"],GPIO.HIGH)
			print "Vicki's Pan & Tilt On\n"
			time.sleep(1)

			GPIO.output(EN_Pins["VUSB_EN"],GPIO.HIGH)
			print "Vicki's USB On\n"
			time.sleep(1)

			PINSTATE_A += GP_5
			Change_PinState(PE1,GPA,PINSTATE_A)
			print "Vicki's TX2 On\n" 
			time.sleep(1)

			print "\n!!!Power on Successful!!!\n"

			flag3 =1

###########################################
	#button_state4 = get_bool("\nTrue4 or False4\n")

	elif keypress is 'd':
		if flag4 == 1:
			PINSTATE_B -= GP_0
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Danyle's Pan & Tilt Down\n" 
			time.sleep(1)

			PINSTATE_B -= GP_4
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Danyle's Lidar Down\n" 
			time.sleep(1)

			print "\n...Powering down Danyle's system...\n" 
			GPIO.output(EN_Pins["DPI_EN"],GPIO.LOW)
			print "Danyle's Tegra Nano Down\n"
			time.sleep(1)

			print "\n???Powered OFF!!!!\n" 

			flag4 = 0

		else:
			print "\n...Powering on Danyle's system...\n" 
			GPIO.output(EN_Pins["DPI_EN"],GPIO.HIGH)
			print "Danyle's Tegra Nano On\n"
			time.sleep(1)

			PINSTATE_B += GP_4
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Danyle's Lidar On\n" 
			time.sleep(1)

			PINSTATE_B += GP_0
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Danyle's Pan & Tilt On\n" 
			time.sleep(1)

			print "\n!!!Power on Successful!!!\n" 
			
			flag4 =1 
		
########################################
	#button_state5 = get_bool("\nTrue5 or False5\n")

	elif keypress is 'e':
		if flag5 == 1:
			print "\n...Powering down Peter's system...\n" 

			PINSTATE_A -= GP_7
			Change_PinState(PE1,GPA,PINSTATE_A)
			print "Peter's TX2 down\n" 
			time.sleep(1)

			PINSTATE_B -= GP_6
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Peter's LIDAR down\n" 
			time.sleep(1)

			print "\n!!!Power down Successful!!!\n" 
			flag5 = 0 
		else:
			print "\n...Powering on Peter's system...\n" 

			PINSTATE_A += GP_7
			Change_PinState(PE1,GPA,PINSTATE_A)
			print "Peter's TX2 On\n" 
			time.sleep(1)

			PINSTATE_B += GP_6
			Change_PinState(PE1,GPB,PINSTATE_B)
			print "Peter's LIDAR On\n" 
			time.sleep(1)

			print "\n!!!Power on Successful!!!\n" 
			flag5 = 1

#########################################
########################################

	elif keypress is 'f':
		print "\n....All systems OFF\n "
		Power_Off()
		#GPIO.cleanup()

	else:
		print "Invalid Button Pressed..."
