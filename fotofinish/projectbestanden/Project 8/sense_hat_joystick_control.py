#Project 8 - Pong met een SenseHat - Bediening van de joystick
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from signal import pause

from sense_hat import SenseHat
#verander de volgende regel van opmerking naar code als je de emulator gebruikt

sense = SenseHat()

def move_up(event):
    print('joystick werd omhoog bewogen')

def move_down(event):
    print('joystick werd omlaag bewogen')

def move_right(event):
    print('joystick werd naar rechts bewogen')

def move_left(event):
    print('joystick werd naar links bewogen')

def move_middle(event):
    print('joystick werd ingedrukt')

sense.stick.direction_up = move_up
sense.stick.direction_down = move_down
sense.stick.direction_right = move_right
sense.stick.direction_left = move_left
sense.stick.direction_middle = move_middle

pause()
