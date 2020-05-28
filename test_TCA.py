import time
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
import adafruit_tca9548a as TCA


tca = TCA.TCA9548A(i2c)

from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(tca[2])

try:
	while 1:
		chan = AnalogIn(ads,ADS.P0)
		print("Channel 1:", chan.value, " ", chan.voltage, "V\n")
		time.sleep(2)
except KeyboardInterrupt:
	print("Stopped")
