#Project 14 - Bewakingscamera voor thuis - Video in een bestand opnemen
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

import picamera

camera = picamera.PiCamera()

camera.resolution = (640, 480)
camera.start_recording('videotest.h264')
camera.wait_recording(60)
camera.stop_recording()

print('Klaar met opnemen')
