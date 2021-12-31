#Project 6 - Een LCD-herinnering
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: https://nostarch.com/RaspberryPiProject

import Adafruit_CharLCD as LCD
import time

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
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
            lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#schrijf je bericht
title = "Niet vergeten!"
reminder = "Je hebt volgende week maandag een afspraak bij de dokter"

#stel de vertraging in voor het scrollen
delay = 0.3

#schrijf een functie om het bericht te laten scrollen
def scroll_text(reminder, delay):
    padding = " " * lcd_columns
    scroll_message = padding + reminder + " "
    for i in range(len(scroll_message)):
        lcd.set_cursor(0, 1)
        lcd.message(scroll_message[i:(i+lcd_columns)])
        time.sleep(delay)

#scroll het bericht in een oneindige lus
lcd.clear()
lcd.home()
lcd.message(title)

while(True):
    scroll_text(reminder, delay)
