import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import sys
import time


import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)


try:
	while 1:
		chan = AnalogIn(ads,ADS.P0)
		print("Channel 1:",chan.value," ",chan.voltage,"V\n")

		chan = AnalogIn(ads,ADS.P1)
		voltage = chan.voltage
		print("Channel 2:",chan.value," ",voltage,"V\n")

		chan = AnalogIn(ads,ADS.P2)
		print("Channel 3:",chan.value," ",chan.voltage,"V\n")

		chan = AnalogIn(ads,ADS.P3)
		print("Channel 4:",chan.value," ",chan.voltage,"V\n")
		time.sleep(2)
except KeyboardInterrupt:
	print ("Stopped.")
