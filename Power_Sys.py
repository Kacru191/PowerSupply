import wiringpi
from time import sleep

pin_base = 65 #lowest available starting number for GPIO PE1
pin_base2 = 81 #lowest available starting number for GPIO PE2
PE1 = 0x23 # Port Expander #1 i2C address
PE2 = 0x24 # Port Expander #2 i2C address

wiringpi.wiringPiSetup() #initalize wiringpi
wiringpi.mcp23017(pin_base,PE1) # Setting up pins and i2c address PE1
wiringpi.mcp23017(pin_base2,PE2) # Setting up pins and i2c address PE2

wiringpi.pinMode(65,
