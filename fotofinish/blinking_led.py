#Project 1 - Een LED laten knipperen
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import LED
from time import sleep

#maak een object genaamd led dat refereert aan GPIO 25
led = LED(25)

#maak een variabele genaamd delay die refereert aan de vertragingstijd in seconden
delay = 1

while True:
    #stel led in op aan voor de duur van de vertragingstijd
    led.on()
    print('Led ingesteld op aan')
    sleep(delay)
    #stel led in op uit voor de duur van de vertragingstijd
    led.off()
    print('Led ingesteld op uit')
    sleep(delay)
