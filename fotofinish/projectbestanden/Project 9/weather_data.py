#Project 9 - Alles-in-één weerstation met sensoren
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from sense_hat import SenseHat
#from sense_emu import SenseHat

from time import sleep

#maak een object genaamd sense
sense = SenseHat()

while True:
    temperature = sense.temperature
    temperature = str(round(temperature, 2))
    print('Temperatuur: ' + temperature + '*C\n')

    humidity = sense.humidity
    humidity = str(round(humidity, 2))
    print ('Luchtvochtigheid: ' + humidity + '%\n')

    pressure = sense.pressure
    pressure = str(round(pressure, 2))
    print('Druk: ' + pressure + 'hPa\n')

    sleep(1)

