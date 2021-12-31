#Project 8 - Pong met een SenseHat - Specifieke LED's op laten lichten
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from sense_hat import SenseHat
#verander de volgende regel van opmerking naar code als je de emulator gebruikt
#from sense_emu import SenseHat
sense = SenseHat()
#stel blauwe pixel in
sense.set_pixel(0, 1, 0, 0, 255)
#stel groene pixel in
sense.set_pixel(7, 6, 0, 255, 0)
#stel roze pixel in
sense.set_pixel(2, 5, 255, 51, 153)
