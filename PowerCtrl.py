import wiringpi

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

	"PTX_EN":72, 			#GPA7
	"VTX_EN":70} 			#GPA5

GPA1_FLT ={ #Faults on Port expander #1A

	"PTX_FLT":71,			#GPA6
	"VTX_FLT":69} 		#GPA4

GPB1_EN={ #Enables on Port Expander #1B

	"PL_EN":79, 			#GPB6
	"DL_EN":77, 			#GPB4
	"OBRD_EN":75, 		#GPB2
	"DPT_EN":73,}		#GPB0

GPB1_FLT={ #Faults on Port Expander #1B

	"PL_FLT":80,			#GPB7
	"DL_FLT":78,			#GPB5
	"OBRD_FLT":76,		#GPB3
	"DPT_FLT":74}			#GPB1
GPB2_EN={ #Enables on Port Expander #1B

	"MD1_EN":92,			#GPB3
	"MD2_EN":90,			#GPB1
	"OPTO48V_EN":93}	#GPB4

GPB2_FLT={ #Faults on Port Expander #1B

	"MD2_EN":91,			#GPB2
	"MD1_EN":89,			#GPB0
	"OPTO48V_FLT":94}	#GPB5

pin_base = 65 			#lowest available starting number for GPIO PE1
pin_base2 = 81		#lowest available starting number for GPIO PE2
PE1 = 0x23 			# Port Expander #1 i2C address
PE2 = 0x24 			# Port Expander #2 i2C address
GPA = 0x12 			# GPA register address
GPB = 0x13 			# GPB register address
IODIRA = 0x00		# Direction of pins for GPA
IODIRB = 0x01		# Direction of pins for GPB
HIGHPINS = 0xFF		# All pins high
LOWPINS = 0x00		# All pins low
OUTPUT = 1
INPUT = 0
HIGH =1
LOW = 0

GP_0 = 0x01
GP_1 = 0x02
GP_2 = 0x04
GP_3 = 0x08
GP_4 = 0x10
GP_5 = 0x20
GP_6 = 0x40
GP_7 = 0x80

wiringpi.wiringPiSetup() #initalize wiringpi
wiringpi.mcp23017Setup(pin_base,PE1) # Setting up pins and i2c address PE1
wiringpi.mcp23017Setup(pin_base2,PE2) # Setting up pins and i2c address PE2

def Power_Off():			#Power off all systems
	for pins in list(GPA1_EN.values()):
		wiringpi.digitalWrite(pins,LOW)
	for pins in list(GPB1_EN.values()):
		wiringpi.digitalWrite(pins,LOW)
	for pins in list(GPB2_EN.values()):
		wiringpi.digitalWrite(pins,LOW)
	for pins in list(EN_Pins.values()):
		GPIO.output(pins,GPIO.LOW)

def Initialize(): 			#Set all pins to outputs

	for pins in list(GPA1_EN.values()):
		wiringpi.pinMode(pins,OUTPUT)
	for pins in list(GPB1_EN.values()):
		wiringpi.pinMode(pins,OUTPUT)
	for pins in list(GPB2_EN.values()):
		wiringpi.pinMode(pins,OUTPUT)

	for pins in list(EN_Pins.values()):
		GPIO.setup(pins,GPIO.OUT)
	Power_Off()	#Set all systems off

def get_bool(prompt):	#True or false prompt to simulate button press
	while True:
		try:
			return {"true":True,"false":False}[input(prompt).lower()]
		except KeyError:
			print ("Invalid input please enter True or False")

while (1):
	#button on for initalization, turns on converters
	button_state = get_bool("\nTrue or False\n")

	if button_state is True:
		print("\nBeginning initialization...\n")
		Initialize()
		time.sleep(1)
		#enable all converter pins
		#print("Pinstate: %s" % str(PINSTATE))

		#print("Pinstate is now: %s" % hex(PINSTATE))
		#print str(PINSTATE)
		print("Setting 5V_EN to HIGH")
		GPIO.output(16,GPIO.HIGH)
		print ("5V Converter Enabled...\n")
		time.sleep(1)

		print("Setting 15V_EN to HIGH")
		GPIO.output(EN_Pins["15V_EN"],GPIO.HIGH)
		print ("15V Converter Enabled...\n")
		time.sleep(1)

		print("Setting 24V_EN to HIGH")
		GPIO.output(EN_Pins["24V_EN"],GPIO.HIGH)
		print ("24V Converter Enabled...\n")
		time.sleep(1)

		print("Setting 28V_EN to HIGH")
		GPIO.output(EN_Pins["28V_EN"],GPIO.HIGH)
		print ("28V Converter Enabled...\n")
		time.sleep(1)

		print("Setting 48V_EN to HIGH")
		#print("Pinstate: %s" % str(PINSTATEC))
		#print("Value type in PINSTATE: %s" % type(PINSTATEC))
		#bus.write_byte_data(PE2,GPB,PINSTATEC)
		wiringpi.digitalWrite(GPB2_EN["OPTO48V_EN"],HIGH)
		print ("48V Converter Enabled...\n")
		time.sleep(1)

		print ("\n...Intialization complete...\n")

	else:
		print ("Initializaton not complete...\n\n\n")
#################################################
################################################
	button_state2 = get_bool("\nTrue2 or False2\n")

	if button_state2 is True:
		print ("\n...Powering on Zack's system...\n")
		GPIO.output(EN_Pins["ZPI_EN"],GPIO.HIGH)
		print ("Zack's Pi On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPB2_EN["MD1_EN"],HIGH)
		print ("Motor Drive On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPB2_EN["MD2_EN"],HIGH)
		print ("Steering Drive On\n")
		time.sleep(1)

		print ("\n!!!Power on Successful!!!\n")
	else:
		GPIO.output(EN_Pins["ZPI_EN"],GPIO.LOW)
		wiringpi.digitalWrite(GPB2_EN["MD1_EN"],LOW)
		wiringpi.digitalWrite(GPB2_EN["MD2_EN"],LOW)
		print ("\n???Powered OFF???\n") 
############################################
	button_state3 = get_bool("\nTrue3 or False3\n")

	if button_state3 is True:
		print ("\n...Powering on Vicki's system...\n")
		GPIO.output(EN_Pins["VPT_EN"],GPIO.HIGH)
		print ("Vicki's Pan & Tilt On\n")
		time.sleep(1)

		GPIO.output(EN_Pins["VUSB_EN"],GPIO.HIGH)
		print ("Vicki's USB On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPA1_EN["VTX_EN"],HIGH)
		print ("Vicki's TX2 On\n")
		time.sleep(1)

		print ("\n!!!Power on Successful!!!\n") 
	else:
		GPIO.output(EN_Pins["VPT_EN"],GPIO.LOW)
		GPIO.output(EN_Pins["VUSB_EN"],GPIO.LOW)
		wiringpi.digitalWrite(GPA1_EN["VTX_EN"],LOW)
		print ("???Powered OFF???") 
###########################################
	button_state4 = get_bool("\nTrue4 or False4\n")

	if button_state4 is True:
		print ("\n...Powering on Danyle's system...\n")
		GPIO.output(EN_Pins["DPI_EN"],GPIO.HIGH)
		print ("Danyle's Tegra Nano On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPB1_EN["DL_EN"],HIGH)
		print ("Danyle's Lidar On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPB1_EN["DPT_EN"],HIGH)
		print ("Danyle's Pan & Tilt On\n")
		time.sleep(1)

		print ("\n!!!Power on Successful!!!\n")
	else:
		GPIO.output(EN_Pins["DPI_EN"],GPIO.LOW)
		wiringpi.digitalWrite(GPB1_EN["DL_EN"],LOW)
		wiringpi.digitalWrite(GPB1_EN["DPT_EN"],LOW)
		print ("\n???Powered OFF???\n")
########################################
	button_state5 = get_bool("\nTrue5 or False5\n")

	if button_state5 is True:
		print ("\n...Powering on Peter's system...\n")

		wiringpi.digitalWrite(GPA1_EN["PTX_EN"],HIGH)
		print ("Peter's TX2 On\n")
		time.sleep(1)

		wiringpi.digitalWrite(GPB1_EN["PL_EN"],HIGH)
		print ("Peter's LIDAR On\n")
		time.sleep(1)

		print ("\n!!!Power on Successful!!!\n")
	else:
		wiringpi.digitalWrite(GPA1_EN["PTX_EN"],LOW)
		wiringpi.digitalWrite(PE1,GPB1_EN["PL_EN"],LOW)
		print ("\n???Powered OFF???\n")
#########################################
########################################

	button_off = get_bool("\nTurn Off?(True or False)\n")

	if button_off is True:
		print ("Powering off all systems ")
		Power_Off()
		#GPIO.cleanup()

	else:
		print ("Systems Still on...")

