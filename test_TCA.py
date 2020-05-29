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
		print("LIDAR1\n")
#		print("Nvidia TX2")
		chan = AnalogIn(ads,ADS.P0)
		volt = chan.voltage
		convert = volt*8.3856 ##Conversion for 28V
		#convert = volt*4.508
#		print("before conversion:", volt, " ")
		print("Voltage:", " ", convert, "V, ")


		chan = AnalogIn(ads,ADS.P1)
		volt1 = chan.voltage
		convert1 = volt1/1.5  ##Conversion for 28V
		#convert1 = volt1/0.728
#		print("before conversion:", volt1," ")
		print("Current:", convert1,"A\n")

		time.sleep(2)
except KeyboardInterrupt:
	print("Stopped")
