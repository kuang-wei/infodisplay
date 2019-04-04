#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
from ctabustracker import CTABusTracker
import config as cfg
import Adafruit_CharLCD as LCD

global busstop, cbt
busstop = '1521'
#busstop = '1427'
cbt = CTABusTracker(cfg.buskey)
times = cbt.get_stop_predictions(busstop)
lcdmessage = ''
for t in times:
	busnum = t['route_id']
	arrivaltime = t['prediction']
	currenttime = cbt.get_time()
	waittime = arrivaltime - currenttime
	lcdmessage+="%-4s%2.0fmin  %s\n"%(busnum, waittime.seconds/60.,
                                     arrivaltime.strftime("%H:%M"))

lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
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

# BeagleBone Black configuration:
# lcd_rs        = 'P8_8'
# lcd_en        = 'P8_10'
# lcd_d4        = 'P8_18'
# lcd_d5        = 'P8_16'
# lcd_d6        = 'P8_14'
# lcd_d7        = 'P8_12'
# lcd_backlight = 'P8_7'

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Alternatively specify a 20x4 LCD.
# lcd_columns = 20
# lcd_rows    = 4

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
#time.sleep(0.5)
#lcd.message('Checking bus\nstop 1521...')

# Wait 0.8 seconds
#time.sleep(0.5)


# Stop blinking and showing cursor.
#lcd.show_cursor(False)
#lcd.blink(False)

# Demo scrolling message right/left.
#lcd.clear()
#message = '171 / 6 / 28'
#lcd.message(message)
#for i in range(lcd_columns-len(message)):
#    time.sleep(0.25)
#    lcd.move_right()
#for i in range(lcd_columns-len(message)):
#    time.sleep(0.25)
#    lcd.move_left()

lcd.clear()
#lcd.blink(True)
lcd.message(lcdmessage)
