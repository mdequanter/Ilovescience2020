#Project 7 - Mini weervoorspeller
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#import necessary libraries
import time
import Adafruit_SSD1306
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Raspberry Pi pen configuratie
RST = 24

#128x32 scherm met hardware I2C
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

#128x64 scherm met hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

#stel je unieke OpenWeatherMap.org URL in
open_weather_map_url = 'http://api.openweathermap.org/data/2.5/weather?q=Porto,PT&APPID=801d2603e9f2e1c70e042e4f5f6e0381'

#initialiseer het scherm
disp.begin()

while True:
    #wis het scherm
    disp.clear()
    disp.display()

    #maak een lege afbeelding om te tekenen
    #zorg voor het maken van een afbeelding met modus '1' voor 1-bit kleur
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    #laat object voor het, tekenen in de afbeelding, tekenen
    draw = ImageDraw.Draw(image)

    #teken een met zwart gevulde rechthoek om de afbeelding te wissen
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    #definieer constanten om tekengebied te definiëren
    padding = 2
    top = padding
    #beweeg van links naar rechts, waarbij de huidige x-positie bijgehouden wordt
    x = padding

    #laad het standaard lettertype
    font = ImageFont.load_default()

    #openWeatherMap.org verzoek om weergegevens
    weather_data = requests.get(open_weather_map_url)

    #geef locatie weer
    location = weather_data.json().get('name') + ' - ' + weather_data.json().get('sys').get('country')
    draw.text((x, top), location,  font=font, fill=255)

    #geef beschrijving weer
    description = 'Desc ' + weather_data.json().get('weather')[0].get('main')
    draw.text((x, top+10), description,  font=font, fill=255)

    #temperature
    raw_temperature = weather_data.json().get('main').get('temp')-273.15

    #temperatuur in Celsius
    temperature = 'Temp ' + str(raw_temperature) + '*C'
    #verander dit van opmerking naar code voor temperatuur in Fahrenheit
    ##temperature = 'Temp ' + str(raw_temperature*(9/5.0)+32) + '*F'
    #geef temperatuur weer
    draw.text((x, top+20), temperature, font=font, fill=255)

    #geef druk weer
    pressure = 'Pres ' + str(weather_data.json().get('main').get('pressure')) + 'hPa'
    draw.text((x, top+30), pressure, font=font, fill=255)

    #geef vochtigheid weer
    humidity = 'Humi ' + str(weather_data.json().get('main').get('humidity')) + '%'
    draw.text((x, top+40), humidity, font=font, fill=255)

    #geef wind weer
    wind = 'Wind ' + str(weather_data.json().get('wind').get('speed')) + 'mps ' + str(weather_data.json().get('wind').get('deg')) + '*'
    draw.text((x, top+50), wind, font=font, fill=255)

    #geef afbeelding weer
    disp.image(image)
    disp.display()
    time.sleep(10)
