#Project 4 - Een grafische gebruikersinterface voor een meerkleurige LED
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
from gpiozero import PWMLED
from tkinter import *

#wijzig de RGB led kleur
def change_color(self):
    red.value = red_slider.get()
    green.value = green_slider.get()
    blue.value = blue_slider.get()
    print(self)

#sluit het venster
def close_window():
    window.destroy()
    
#maak een PWMLED object voor elke kleur
red = PWMLED(23)
green = PWMLED(24)
blue = PWMLED(25)

#maak venster
window = Tk()
window.title("RGB LED Controller")
window.geometry("300x200")

#maak drie schuiven om elke RGB led aan te sturen
red_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL,
        label="Rood", troughcolor="red", length=200, command=change_color)
red_slider.pack()

green_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL,
        label="Groen", troughcolor="green", length=200, command=change_color)
green_slider.pack()

blue_slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL,
        label="Blauw", troughcolor="blue", length=200, command=change_color)
blue_slider.pack()

#maak knop om te sluiten
close_button = Button(window, text="Sluiten", command=close_window)
close_button.pack()

mainloop()
