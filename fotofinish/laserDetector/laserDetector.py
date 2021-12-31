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

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
camera = PiCamera()
camera.rotation = 0
camera.resolution = (1024,768)
camera.shutter_speed = 1000
camera.exposure_mode = 'sports'
delay = 5
i = 0

FMT = '%Y_%m_%d_%H_%M_%S_%f'



def take_photo():
    global i,FMT

    i = i + 1
    starttime = datetime.now()
    print(starttime)
    camera.capture('/home/pi/fotofinish/'+ str(starttime) + '.jpg')
    #camera.start_preview()
    #camera.stop_preview()
    print ("foto genomen")
    sleep(0.5)



while True:
    status = GPIO.input(20)
    if (status == 0) :
        camera.start_preview()
        take_photo()
        camera.stop_preview()
        
    
