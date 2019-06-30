import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
print "GPIO 6 on"
GPIO.output(6,GPIO.HIGH)
time.sleep(1)
print "GPIO 22 on"
GPIO.output(22,GPIO.HIGH)
print "GPIO 19 On"
GPIO.output(19,GPIO.HIGH)
#print "GPIO 5 off"
#GPIO.output(5,GPIO.HIGH)
print "GPIO 17 on"
GPIO.output(17,GPIO.HIGH)
time.sleep(1)
#print "LED off" 
#GPIO.output(6,GPIO.LOW)

#GPIO.cleanup()
