#Project 13 - Inbraakdetector met foto-opname
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import Button, MotionSensor
from picamera import PiCamera
from time import sleep
from signal import pause

#maak objecten die refereren aan een knop, 
#een bewegingssensor en de PiCamera
button = Button(2)
pir = MotionSensor(4)
camera = PiCamera()

#start de camera
camera.rotation = 0
camera.start_preview()

#maak namen voor afbeeldingen
i = 0

#stop de camera als de drukknop wordt ingedrukt
def stop_camera():
    camera.stop_preview()
    #sluit het programma af
    exit()

#neem een foto als er beweging gedetecteerd wordt
def take_photo():
    global i
    i = i + 1
    camera.capture('/home/pi/Desktop/image_%s.jpg' % i)
    print('Er is een foto gemaakt')
    sleep(10)

#wijs een functie toe die uitgevoerd wordt als de knop ingedrukt wordt
button.when_pressed = stop_camera
#wijs een functie toe die uitgevoerd wordt als er beweging gedetecteerd wordt
pir.when_motion = take_photo

pause()
