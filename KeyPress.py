from pynput.keyboard import Key, Controller 

keyboard = Controller()

if keyboard.press('a'):
	print "'a' pressed"
else:
	print "No key pressed"
