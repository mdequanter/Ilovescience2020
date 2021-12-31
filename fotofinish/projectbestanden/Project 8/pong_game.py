#Project 8 - Pong met een SenseHat
#latest code updates available at: https://github.com/RuiSantosdotme/RaspberryPiProject
#project updates at: www.visualsteps.nl/raspberrypi/projectbestanden

#gebaseerd op het raspberrypi.org Sense HAT Pong voorbeeld

#importeer de benodigde bibliotheken
from random import randint
from time import sleep

#gebruik deze regel als je het Sense HAT board gebruikt
from sense_hat import SenseHat

#verander de volgende regel van opmerking naar code als je de emulator gebruikt
#from sense_emu import SenseHat

#maak een object genaamd sense
sense = SenseHat()

#stel de positie van de bat, willekeurige positie van de bal en de snelheid in
y = 4
ball_position = [int(randint(2,6)), int(randint(1,6))]
ball_velocity = [1, 1]

#rode kleur
X = [255, 0, 0]
#geen kleur
N = [0, 0, 0]

#sad face array
sad_face = [
N, N, X, X, X, X, N, N,
N, X, N, N, N, N, X, N,
X, N, X, N, N, X, N, X,
X, N, N, X, N, N, N, X,
X, N, N, X, N, N, N, X,
X, N, X, N, N, X, N, X,
N, X, N, N, N, N, X, N,
N, N, X, X, X, X, N, N
]

#teken de bat op y-positie
def draw_bat():
    sense.set_pixel(0, y, 0, 255, 0)
    sense.set_pixel(0, y+1, 0, 255, 0)
    sense.set_pixel(0, y-1, 0, 255, 0)

#beweeg de bat omhoog
def move_up(event):
    global y
    if y > 1 and event.action=='ingedrukt':
        y -= 1

#beweeg de bat omlaag
def move_down(event):
    global y
    if y < 6 and event.action=='ingedrukt':
        y += 1

#beweeg de bal naar de volgende positie
def draw_ball():
    #bal weergegeven op huidige positie
    sense.set_pixel(ball_position[0], ball_position[1], 75, 0, 255)
    #volgende positie van de bal
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]
    #if bal raakt plafond, bereken volgende positie
    if ball_position[0] == 7:
        ball_velocity[0] = -ball_velocity[0]
    #if bal raakt muur, bereken volgende positie
    if ball_position[1] == 0 or ball_position[1] == 7:
        ball_velocity[1] = -ball_velocity[1]
    #if ball bereikt positie 0, speler verliest en het spel wordt afgesloten
    if ball_position[0] == 0:
        sleep(0.25)
        sense.set_pixels(sad_face)
        quit()
    #if bal raakt de bat, bereken volgende positie van de bal
    if ball_position[0] == 1 and y - 1 <= ball_position[1] <= y+1:
        ball_velocity[0] = -ball_velocity[0]
        
#wanneer de joystick omhoog of omlaag beweegt, zet dat de overeenkomstige functie in gang
sense.stick.direction_up = move_up
sense.stick.direction_down = move_down

#voer het spel uit
while True:
    sense.clear()
    draw_bat()
    draw_ball()
    sleep(0.25)
