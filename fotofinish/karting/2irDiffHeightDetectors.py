#Project 1 - Een LED laten knipperen
#latest code updatels available at: https://github.com/RuiSantosdotme/RaspberryPiProject
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


counter = 0
starttime = datetime.now()


lapCounter = {}
lapCounter[1] = 0
lapCounter[2] = 0
lapCounter[3] = 0
lapCounter[4] = 0
lapCounter[5] = 0
lapCounter[6] = 0
lastTime = {}
lastTime[1] = datetime.now()
lastTime[2] = datetime.now()
lastTime[3] = datetime.now()
lastTime[4] = datetime.now()
lastTime[5] = datetime.now()
lastTime[6] = datetime.now()

lastPulse = {}
lastPulse[1] = datetime.now()
lastPulse[2] = datetime.now()
lastPulse[3] = datetime.now()
lastPulse[4] = datetime.now()
lastPulse[5] = datetime.now()
lastPulse[6] = datetime.now()


lastStatus1 = 1
lastStatus2 = 1

database = "karting.db"
conn = sqlite3.connect(database)

cursor = conn.cursor()
cursor.execute("DELETE from laps")
conn.commit()

counter = 0

def chronoTimer(date1,date2) :

    FMT = '%Y-%m-%d %H:%M:%S.%f'
    
    date1 = str(date1)
    date2 = str(date2)

    if (len(date1) == 19) :
        date1 = date1 + ".000000"
    if (len(date2) == 19) :
        date2 = date2 + ".000000"

    diff = datetime.strptime(date2, FMT) - datetime.strptime(date1, FMT)
    difference = diff.seconds + diff.microseconds / 1000000
    
    return difference

def safeLap(driver,drivername,lapcounter,lapTime) :
    global conn
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO laps (tag,drivername,lap,laptime,timestamp) VALUES (?,?,?,?,?)",
                   (driver,drivername,lapcounter,lapTime, str(datetime.now())))
    conn.commit()
    
    print (drivername,lapcounter, lapTime)
    


while True:
        
    status1 = GPIO.input(detector1)
    status2 = GPIO.input(detector2)
    
    if (status1 == 1 and lastStatus1 == 0) :
        lastPulse[1] = datetime.now()

    if (status2 == 1 and lastStatus2 == 0) :
        lastPulse[2] = datetime.now()

    lastStatus1 = status1
    lastStatus2 = status2
    
    chrono1 = chronoTimer(lastPulse[1],datetime.now())
    chrono2 = chronoTimer(lastPulse[2],datetime.now())
    
    AbsoluteDifference = abs(chrono1-chrono2)
    
    #print (chrono1, chrono2)

    if (chrono2 > 0.1 and chrono2 < 0.5) :
        if (AbsoluteDifference > 0.5) :
            difference  = chronoTimer(lastTime[1],datetime.now())
            if (difference > minLapTime) :
                lapCounter[1] = lapCounter[1] + 1
                lastTime[1] = datetime.now()
                safeLap(1,"driver 1",lapCounter[1],difference)
        else :
            difference  = chronoTimer(lastTime[2],datetime.now())
            if (difference > minLapTime) :
                lapCounter[2] = lapCounter[2] + 1
                lastTime[2] = datetime.now()
                safeLap(2,"driver 2",lapCounter[2],difference)
                
    if (chrono1 > 0.1 and chrono1 < 0.5 and AbsoluteDifference > 0.5) :
        difference  = chronoTimer(lastTime[1],datetime.now())
        if (difference > minLapTime) :
            lapCounter[1] = lapCounter[1] + 1
            lastTime[1] = datetime.now()
            safeLap(1,"driver 1",lapCounter[1],difference)

    sleep(0.0005)