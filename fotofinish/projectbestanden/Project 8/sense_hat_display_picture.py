#Project 8 - Pong met een SenseHat - Afbeelding weergeven
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

from sense_hat import SenseHat
#verander de volgende regel van opmerking naar code als je de emulator gebruikt 
#from sense_emu import SenseHat

sense = SenseHat()

#rode kleur
X = [255, 0, 0]
#geen kleur
N = [0, 0, 0]

#sad face array
sad_face = [
N, N, X, X, X, X, N, N,
N, X, N, N, N, N, X, N,
X, N, X, N, N, X, N, X,
X, N, N, N, N, N, N, X,
X, N, N, X, X, N, N, X,
X, N, X, N, N, X, N, X,
N, X, N, N, N, N, X, N,
N, N, X, X, X, X, N, N
]

sense.set_pixels(sad_face)
