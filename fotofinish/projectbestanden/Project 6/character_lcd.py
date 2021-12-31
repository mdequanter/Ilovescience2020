#Project 6 - Een LCD-herinnering
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

import Adafruit_CharLCD as LCD

#Raspberry Pi pen-configuratie
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4

#definieer de afmeting van het LCD
lcd_columns = 16
lcd_rows = 2

#initialiseer het LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                           lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
#schrijf je bericht
lcd.message('Het werkt\nJe bent geweldig!')
