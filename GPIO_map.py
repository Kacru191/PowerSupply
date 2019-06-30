




IODIRA = 0x00	# Pin direction register - master set of all Port A registers
IODIRB =0x00	# Pin direction register - master set of all Port B registers
GPIOA = 0x12	# GPIOA Register Address on Port Expander OLATA register for outputs
GPIOB = 0x13	# GPIOB Register Address on Port Expander


def GPA_Output(Device):
	# Sets all eight bits in the GPIOA register to 0 (output)
	bus.write_byte_data(Device,IODIRA,0x00)
	bus.write_byte_data(Device, GPIOA, 0)
	#bus.write_byte_data(Device,GPIO,2)


def GPB_Output(Device):
	# Sets all eight bits in the GPIOB register to 0 (output)
	bus.write_byte_data(Device,IODIRB,0x00)
	bus.write_byte_data(Device, GPIOB, 0x00)


def Initialize():
	#try:
		# Set Port Expander 1's GPA registers to output
		#GPA_Output(PE1)
		#print("Port Expander 1 GPIOA initialized")
	#except:
		#print("Error setting PE1 GPA register to output")

	#try:
		# Set Port Expander 1's GPB registers to output
		#GPB_Output(PE1)
		#print("Port Expander 1 GPIOB initialized")
	#except:
		#print("Error setting PE1 GPB register to output")

	try:
		# Set Port Expander 2's GPA registers to output
		GPA_Output(PE2)
		print("Port Expander 2 GPIOA initialized")
	except:
		print("Error setting PE2 GPA register to output")

	try:
		# Set Port Expander 2's GPB registers to output
		GPB_Output(PE2)
		print("Port Expander 2 GPIOB initialized")
	except:
		print("Error setting PE2 GPB register to output")

	try:
		# Cycle through the list of GPIO pins
		# and set each one as an OUTPUT
		for pin in list(EN_Pins.values()):
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin,GPIO.LOW)
			#print pin
		#GPIO.setup(6,GPIO.OUT)
		print("GPIO pins initialized")

	except:
		print("Error setting GPIO pins as output")


#print get_bool("True or False\n")
#bool(button_1)

#button_state = raw_input("True or False\n")
print button_state

