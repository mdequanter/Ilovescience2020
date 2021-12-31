#Project 3 - LED  Dimschakelaar
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import PWMLED, MCP3008
from time import sleep

#maak een object genaamd pot dat refereert aan MCP3008 kanaal 0
pot = MCP3008(0)

#maak een PWMLED object genaamd led dat refereert aan GPIO 17
led = PWMLED(17)
counter = 0
while True:
    #pot.value benadert de huidge pot meting
    #if(pot.value < 0.001):
        #als de waarde van de pot heel klein is, wordt de led uitgeschakeld
        #led.value = 0
    #else:
        #wijzig helderheid van de led afhankelijk van de pot waarde
        #led.value = pot.value
    #druk de pot waarde af
    #print (pot.value)
    if (pot.value > 0.9) :
        counter = counter + 1
        print("detected :" + str(counter))
        led.value = 0.9
        sleep(0.05)
    else :
        led.value = 0
    #pauzeer gedurende 0,1 seconde
    #sleep(0.3)
