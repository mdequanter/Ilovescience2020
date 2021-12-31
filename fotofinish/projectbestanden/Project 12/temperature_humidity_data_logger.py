#Project 12 - Datalogger voor temperatuur en luchtvochtigheid
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
import Adafruit_DHT
import time

#verander de onderstaande regels naar code of opmerking afhankelijk van je sensor
#sensor = Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT22
#sensor = Adafruit_DHT.AM2302

#DHT-pen aangesloten op GPIO 4
sensor_pin = 4

#maak een variabele om de while-lus aan te sturen
running = True

#nieuw .txt bestand gemaakt met kopregel
file = open('sensor_readings.txt', 'w')
file.write('time and date, temperature, humidity\n')

#oneindige lus
while running:
    try:
        #uitlezen van luchtvochtigheid en temperatuur
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

        #maak van onderstaande regel code om te converteren naar Fahrenheit
        #temperature = temperature * 9/5.0 + 32

        #soms wordt er niets uitgelezen en zijn de resultaten nul
        #de volgende instructie zorgt ervoor dat alleen geldige uitgelezen waarden opgeslagen worden
        if humidity is not None and temperature is not None:
            #druk temperatuur en luchtvochtigheid af 
            print('Temperatuur = ' + str(temperature) + ', Luchtvochtigheid = ' + str(humidity))
            #sla tijd, datum, temperatuur en luchtvochtigheid op in een .txt bestand
            file.write(time.strftime('%H:%M:%S %d/%m/%Y') + ', ' +
                str(temperature) + ', '+ str(humidity) + '\n')
        else:
            print('Uitlezen mislukt. Probeer nogmaals!')
        #wacht 10s tussen elke keer dat de sensor uitgelezen wordt
        time.sleep(10)
    #als KeyboardInterrupt aangesproken wordt, stop de lus en sluit het .txt bestand
    except KeyboardInterrupt:
        print ('Programma gestopt')
        running = False
        file.close()
