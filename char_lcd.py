#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
import datetime
from ctabustracker import CTABusTracker
import config as cfg
import Adafruit_CharLCD as LCD

global busstop, cbt
busstop = '1521'
#busstop = '1427'
cbt = CTABusTracker(cfg.buskey)
timeout = 60*5
refreshinterval = 3.0 # in seconds

# get and parse bus times
times = cbt.get_stop_predictions(busstop)
lcdmessage = ''
for t in times:
	busnum = t['route_id']
	arrivaltime = t['prediction']
	currenttime = cbt.get_time()
	waittime = arrivaltime - currenttime
	lcdmessage+="%-4s%2.0fmin  %s\n"%(busnum, waittime.seconds/60.,
                                     arrivaltime.strftime("%H:%M"))

# get all times into a list of pairs of times
lcdlines = lcdmessage.splitlines()
lcdlines.reverse()
alltimes = []
while lcdlines:
	currentlines = [lcdlines.pop()]
	try:
		currentlines.append(lcdlines.pop())
	except:
		pass
	alltimes.append(currentlines)

# loop through
tstart = datetime.datetime.now()
while int((datetime.datetime.now()-tstart).total_seconds())<timeout:
	for displaylines in alltimes:
		displaystr = '\n'.join(displaylines)
		
		# clear out LCD display
		lcd_rs        = 27
		lcd_en        = 22
		lcd_d4        = 25
		lcd_d5        = 24
		lcd_d6        = 23
		lcd_d7        = 18
		lcd_backlight = 4

		lcd_columns = 16
		lcd_rows    = 2

		lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
		                           lcd_columns, lcd_rows, lcd_backlight)

		lcd.message('Hello\nworld!')
		lcd.clear()
		lcd.show_cursor(True)
		lcd.message('')


		# Raspberry Pi pin configuration:
		lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
		lcd_en        = 24
		lcd_d4        = 23
		lcd_d5        = 17
		lcd_d6        = 21
		lcd_d7        = 22
		lcd_backlight = 16

		# Define LCD column and row size for 16x2 LCD.
		lcd_columns = 16
		lcd_rows    = 2

		# Initialize the LCD using the pins above.
		lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
		                           lcd_columns, lcd_rows, lcd_backlight)

		lcd.clear()
		#lcd.blink(True)
		lcd.message(displaystr)
		time.sleep(refreshinterval)
