#Project 1 - Een LED laten knipperen
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import LED
from time import sleep
from picamera import PiCamera
from PIL import Image
from datetime import datetime
from datetime import timedelta

import RPi.GPIO as GPIO
detector1 = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(detector1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
delay = 0.5
#camera.start_preview()


counter = 0
starttime = datetime.now()
FMT = '%Y-%m-%d %H:%M:%S.%f'

while True:
    sleep(0.2)
    if (GPIO.input(detector1) == 0) :
        print ("low")
        
    if (GPIO.input(detector1) == 1) :
        print ("high")
    
    
        
        

              
    
    
        
        




