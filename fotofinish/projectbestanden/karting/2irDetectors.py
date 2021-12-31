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
import sqlite3
from sqlite3 import Error



import RPi.GPIO as GPIO
detector1 = 20
detector2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(detector1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(detector2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
delay = 0.5

minLapTime = 3

#camera.start_preview()

FMT = '%Y-%m-%d %H:%M:%S.%f'

counter = 0
starttime = datetime.now()
firstEdge = False

lastPulse = 1

lapCounter = {}
lapCounter[1] = 0
lapCounter[2] = 0
lapCounter[3] = 0
lapCounter[4] = 0
lapCounter[5] = 0
lapCounter[6] = 0
lastTime = {}
lastTime[1] = 99
lastTime[2] = 99
lastTime[3] = 99
lastTime[4] = 99
lastTime[5] = 99
lastTime[6] = 99


database = "karting.db"
conn = sqlite3.connect(database)

cursor = conn.cursor()
cursor.execute("DELETE from laps")
conn.commit()

counter = 0

while True:
        
    status = GPIO.input(detector1)
    statusLowIR = GPIO.input(detector2)
    
    if (statusLowIR == 0) :
        if (status == 0 and lastPulse == 1) :
            counter = counter+1
            if (counter == 1):
                firstPulseTime = datetime.now()
                starttime = datetime.now()            
        lastPulse = status
    
    nowString = str(datetime.now())
    starttimeString = str(starttime)
    
    if (len(nowString) == 19) :
        nowString = nowString + ".000000"
    if (len(starttimeString) == 19) :
        starttimeString = starttimeString + ".000000"

    diff = datetime.strptime(nowString, FMT) - datetime.strptime(starttimeString, FMT)
    difference = diff.seconds + diff.microseconds / 1000000
        
    if (difference > 0.5 and statusLowIR == 1 ) :
        if (counter >=1) :
            driver = counter
            lapCounter[driver] = lapCounter[driver]+1
            drivername = "driver " + str(driver) 
            
            
            
            lastTimeString = str(lastTime[driver])
            firstPulseTimeString = str(firstPulseTime)
            
                

            if (lastTime[driver] != 99) :                
                if (len(lastTimeString) == 19) :
                    lastTimeString = lastTimeString + ".000000"
                if (len(firstPulseTimeString) == 19) :
                    firstPulseTimeStringString = firstPulseTimeStringString + ".000000"
                diff = datetime.strptime(firstPulseTimeString, FMT) - datetime.strptime(lastTimeString, FMT)
                difference = diff.seconds + diff.microseconds / 1000000
                lapTime = difference
            else :
                lapTime = 99
                
            if (lapTime > minLapTime) :
                print (driver,lapTime)
                lastTime[driver] = datetime.now()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO laps (tag,drivername,lap,laptime,timestamp) VALUES (?,?,?,?,?)",
                               (driver,drivername,lapCounter[driver],lapTime, str(datetime.now())))
                conn.commit()
            

        counter = 0
        starttime = datetime.now()


        
        

              
    
    
        
        




