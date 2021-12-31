#Project 8 - Pong met een SenseHat - Tekst weergeven
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from sense_hat import SenseHat
#verander de volgende regel van opmerking naar code als je de emulator gebruikt
#from sense_emu import SenseHat
sense = SenseHat()
sense.show_message('Hallo Wereld!', text_colour = [0, 0, 255])
