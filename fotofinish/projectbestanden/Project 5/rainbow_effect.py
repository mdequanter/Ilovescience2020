#Project 5 - Regenboog  LED Strip
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#gebaseerd op Tony DiCola's NeoPixel bibliotheek strandtest voorbeeld

#importeer de benodigde bibliotheken
from neopixel import *
from time import sleep
from gpiozero import Button, MCP3008

#Led-strip configuratie
LED_COUNT = 14 #aantal led pixels
LED_PIN = 18 #GPIO pen verbonden met de pixels (moet PWM ondersteunen!)
LED_FREQ_HZ = 800000 #Led-signaal frequentie in Hz (meestal 800 kHz)
LED_DMA = 5 #DMA-kanaal dat gebruikt wordt voor het opwekken van het signaal (probeer 5)
LED_INVERT = False #stel in op True om het signaal te inverteren

#maak pot objecten om te refereren aan MCP3008 kanaal 0 en 1
pot_brightness = MCP3008(0)
pot_speed = MCP3008(1)

#sluit drukknop aan op GPIO 2, trek omhoog
button_start = Button(2)

#animatie voor het aansturen van variabele
running_animation = False

#genereer regenboogkleuren via 0-255 posities
def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

#teken regenboog die zichzelf uniform verdeelt over alle pixels
def rainbowCycle(strip):
    for j in range(256):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        sleep((pot_speed.value*40)/1000.0)

#functie om de animatie te starten en stoppen
def start_animation():
    global running_animation
    if running_animation == True:
        running_animation = False
    else:
        running_animation = True

#wijs een functie toe die uitgevoerd wordt als de knop wordt ingedrukt
button_start.when_pressed = start_animation

#maak NeoPixel object met de passende configuratie
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, int(pot_brightness.value*255))
#initialiseer de strip
strip.begin()
while True:
    if running_animation == True:
        #stel helderheid van de led-strip in
        strip.setBrightness(int(pot_brightness.value*255))
        rainbowCycle(strip)
