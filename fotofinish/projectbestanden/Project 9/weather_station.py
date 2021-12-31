#Project 9 - Alles-in-één weerstation met sensoren
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from tkinter import *
from tkinter import ttk
import time
from sense_hat import SenseHat
#from sense_emu import SenseHat

#maak een object genaamd sense
sense = SenseHat()

#maak een venster
window = Tk()
window.title('Lokaal weerstation')
window.geometry('200x480')

#maak een luchtvochtigheid label voor titel en waarde
humidity_label = Label(window, text = 'Luchtvochtigheid', font = ('Helvetica', 18), pady = 3)
humidity_label.pack()

humidity = StringVar()

humidity_value=Label(window, textvariable = humidity,
    font = ('Courier', 20), fg = 'blue', anchor = N, width = 200)
humidity_value.pack()

#maak een luchtvochtigheid canvas
humidity_canvas = Canvas(window, width = 200, height = 200)
humidity_canvas.pack()

#maak een luchtvochtigheid voortgangsbalk
humidity_bar = DoubleVar()

progressbar_humidity = ttk.Progressbar(humidity_canvas, variable = humidity_bar,
    orient = VERTICAL, length = 200, maximum = 100)
progressbar_humidity.pack(fill=X, expand=1)

#maak een temperatuur label voor title en waarde
temperature_label = Label(window, text = 'Temperatuur', font = ('Helvetica', 18),
    anchor = S, width = 200, height = 2)
temperature_label.pack()

temperature=StringVar()

temperature_value = Label(window, textvariable = temperature, font = ('Courier', 20),
    fg = 'red', anchor = N, width = 200)
temperature_value.pack()

#maak een druk label voor titel en waarde
pressure_label = Label(window, text = 'Druk', font = ('Helvetica', 18),
    anchor = S, width = 200, height = 2)
pressure_label.pack()

pressure = StringVar()

pressure_value = Label(window, textvariable = pressure,
    font = ('Courier', 20), fg = 'green', anchor = N, width = 200)
pressure_value.pack()

def update_readings():
    humidity.set(str(round(sense.humidity, 2)) + '%')
    humidity_bar.set(sense.humidity)
    temperature.set(str(round(sense.temperature, 2)) + 'ºC')
    #temperature.set(str(round(sense.temperature*(9/5)+32, 2)) + 'ºF')
    pressure.set(str(round(sense.pressure)) + 'hPa')
    window.update_idletasks()
    window.after(3000, update_readings)

update_readings()
window.mainloop()
