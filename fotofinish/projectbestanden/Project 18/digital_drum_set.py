#Project 18 - Digitaal Drumstel
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#importeer de benodigde bibliotheken
import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button
from signal import pause

#maak een object voor de mixer module die geluiden laadt en afspeelt
pygame.mixer.init()

#wijs aan elke knop een drumgeluid toe
button_sounds = {
    Button(2): Sound("samples/drum_cymbal_open.wav"),
    Button(3): Sound("samples/drum_heavy_kick.wav"),
    Button(14): Sound("samples/drum_snare_hard.wav"),
    Button(15): Sound("samples/drum_cymbal_closed.wav"),
    Button(17): Sound("samples/drum_roll.wav"),
    Button(18): Sound("samples/perc_snap.wav"),
    Button(22): Sound("samples/loop_amen_full.wav"),
    Button(27): Sound("samples/loop_mika.wav"),
}

#het geluid wordt afgespeeld als de knop ingedrukt wordt
for button, sound in button_sounds.items():
    button.when_pressed = sound.play

#laat het programma draaien om gebeurtenissen te detecteren
pause()
