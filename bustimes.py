from ctabustracker import CTABusTracker
import config as cfg
import Adafruit_CharLCD as LCD
import time
import datetime

global busstop, cbt
busstop = '1521'
cbt = CTABusTracker(cfg.buskey)

def printtime(cbt, busstop, timeout=5*60.):
	times = cbt.get_stop_predictions(busstop)

	# parse the bus times at the bus stop
	lcdmessage = ''
	for t in times:
		busnum = t['route_id']
		arrivaltime = t['prediction']
		currenttime = cbt.get_time()
		waittime = arrivaltime - currenttime
		print("%4s is arriving at %s in %2.0f minutes"%(busnum,
												arrivaltime.strftime("%H:%M"),
												waittime.seconds/60.))
		print("%-4s%2.0fmin %s"%(busnum, waittime.seconds/60.,
								 arrivaltime.strftime("%H:%M")))
		lcdmessage+="%-4s%2.0fmin %s\n"%(busnum, waittime.seconds/60.,
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
	while int((datetime.datetime.now()-tstart).total_seconds()*1000)<timeout:
		for displaylines in alltimes:
			lcddisplay(displaylines)
			time.sleep(1.2)

def lcddisplay(message):
	# reset LCD or else LCD will fail
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
	
	# real defintions
	lcd_rs        = 25
	lcd_d4        = 23
	lcd_d5        = 17
	lcd_d6        = 21
	lcd_d7        = 22
	lcd_backlight = 16
	lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
	lcd.message(message)

if __name__ == '__main__':
	printtime(cbt, busstop)
