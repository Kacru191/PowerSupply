import board 
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import sys
import time


import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)

chan = AnalogIn(ads,ADS.P0)
print("Channel 1:",chan.voltage,"\n")

chan = AnalogIn(ads,ADS.P1)
print("Channel 2:",chan.voltage,"\n")

chan = AnalogIn(ads,ADS.P2)
print("Channel 3:",chan.voltage,"\n")

chan = AnalogIn(ads,ADS.P3)
print("Channel 4:",chan.voltage,"\n")