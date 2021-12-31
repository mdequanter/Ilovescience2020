#Project 2 - LED-zaklamp met drukknop
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from gpiozero import LED, Button
from signal import pause

led = LED(25)
button = Button(2)

button.when_pressed = led.on
button.when_released = led.off

pause()
