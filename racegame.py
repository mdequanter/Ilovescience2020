
import pygame
import sys
from pygame.locals import *
import os

import ssl
import json
import time
from datetime import datetime
import array

import paho.mqtt.client as mqtt
import ssl
import json

import winsound

# ----------------- SETTINGS --------------------------

# set maximum width of screen based on the resolution of your screen
display_width = 800

# set max X and Y coordinates of the playing field
maxY = 2660
maxX = 5550

host = "localhost"
port = 1883
topic = "tags"

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second


tag1 = '27211'
tag2 = '27241'


# -----------------------------------------------------

ratio = maxY/maxX
display_height = int(display_width / ratio)
transformX =  display_height / maxX
transformY =  display_width / maxY

transformX =  display_height / maxX
transformY =  display_width / maxY

fastestTime1 = "00:00.01"
fastestTime2 = "00:00.00"
fastestTime3 = "00:00.00"

x1 = 0
y1 = 0
yaw1 = 0
x2 = 0
y2 = 0
yaw2 = 0


laps1 = []
laps1Counter = 0
lastLap1 = '00:00.00'
currentTag = '00000'

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)


status = "READY"

_image_library = {}


lastX1 = 0

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))

# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    global x1
    global y1
    global yaw1
    global x2
    global y2
    global yaw2
    global tag1
    global tag2

    tag = msg.payload.decode()
    tagContent = json.loads(tag)

    for tag in tagContent:
        for key, value  in tag.items():
            if (key == 'tagId'):
                currentTag = value
            if key == 'data':
                for key2, value2 in value.items():
                    if key2 == 'coordinates':
                        for key3, value3 in value2.items():
                            if  key3 == 'x':
                                if (currentTag == tag1) :
                                    x1 = value3
                                if (currentTag == tag2) :
                                    x2 = value3
                            if key3 == 'y':
                                if (currentTag == tag1) :
                                    y1 = value3
                                if (currentTag == tag2) :
                                    y2 = value3
                    if key2 == 'orientation':
                        for key3, value3 in value2.items():
                            if (key3 == 'yaw') :
                                if (currentTag == tag1):
                                    yaw1 = value3
                                if (currentTag == tag2):
                                    yaw2 = value3
    return


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        image = pygame.image.load(path)
        _image_library[path] = image
    return image


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_status(text):
    largeText = pygame.font.Font('CourierPrime.ttf',70)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/4))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def message_status1(position, text):
    largeText = pygame.font.Font('CourierPrime.ttf',30)
    position = 70 + int(position) * 30
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (400,position)
    screen.blit(TextSurf, TextRect)

def fitText(text):
    if (len(text) < 40) :
        while (len(text) <= 40) :
            text = text + " "
    return text

def print_scoreboard() :
    largeText = pygame.font.Font('CourierPrime.ttf',30)
    text = fitText("Pos   Driver      Last           Best")
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (400,50)
    screen.blit(TextSurf, TextRect)

def countDown(t):
    global timer1
    largeText = pygame.font.Font('CourierPrime.ttf', 70)
    while  t > 0 :
        text = str(t)
        screen.blit(background_image_resised, [0, 0])
        message_status(text)
        time.sleep(1)
        t -= 1
    timer1 = time.time()
    return

def ChronoMeter(timer) :
    timeDiff = datetime.now() - timer
    timeStr = str(timeDiff)
    returnStr = timeStr[2:-4]
    return returnStr

client = mqtt.Client()

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height), RESIZABLE)
background_image = pygame.image.load("backgroundRace.png").convert()
background_image_resised = pygame.transform.scale(background_image, (display_width,display_height ))
#screen.blit(background_image_resised, [0, 0])
pygame.mouse.set_visible(0)


done = False
is_blue = True

clock = pygame.time.Clock()
counter1, text1 = 60, '60'.rjust(3)
counter2, text2 = 60, '60'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)

playfieldWidth = 500
playfieldLenght = 1000


middlefield = playfieldLenght / 2

text1 = ""
text2 = ""



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_BACKSPACE]: status = "PAUZED"
    if pressed[pygame.K_SPACE]:
        status = "COUNTDOWN"
        starttime1 = datetime.now()
        starttime2 = datetime.now()

    if pressed[pygame.K_DELETE]: status = "RESET"
    if pressed[pygame.K_LEFT]: y1 -= 10
    if pressed[pygame.K_RIGHT]: y1 += 10
    if pressed[pygame.K_UP]: x1 -= 10
    if pressed[pygame.K_DOWN]: x1 += 10


    client.loop(timeout=1.0, max_packets=1)

    gameCoX1 = int(x1 * transformX)
    gameCoY1 = int(y1 * transformY)
    gameCoX2 = int(x2 * transformX)
    gameCoY2 = int(y2 * transformY)

    screen.blit(background_image_resised, [0, 0])

    pygame.draw.circle(screen, red,(gameCoY1,gameCoX1),20,20)
    pygame.draw.circle(screen, black,(gameCoY2,gameCoX2),20,20)

    if (status == "READY"):
        message_status("Get ready!")
    if (status == "COUNTDOWN"):
        laps1 = []
        laps1Counter = 0
        laps2 = []
        laps2Counter = 0
        laps3 = []
        laps3Counter = 0
        countDown(3)
        status = "RUN"
    if (status == "PAUZED"):
        message_status("Game Pauzed")
    if (status == "RUN"):
        lapTime1 = ChronoMeter(starttime1)
        lapTime2 = ChronoMeter(starttime2)
        lapTime3 = "00:00.00"

        if (int(x1) < 1500  and int(x1) > 1200  and int(y1) > 0  and int(y1) < 1200 and yaw1 > 3.2 and yaw1 < 5.8):
            if (lapTime1 > "00:02:00"):
                if (len(laps1) > 1):

                    cd = min(laps1)
                else:
                    fastestTime1 = lapTime1
                winsound.Beep(frequency, duration)
                print ("Driver1 passed line")
                laps1Counter += 1
                laps1.append(lapTime1)
                lastLap1 = lapTime1
                starttime1 = datetime.now()

        if (int(x2) < 0 and int(x2) > - 300 and int(y2) > 4200 and int(y2) < 5500 and yaw2 > 1 and yaw2 < 3,9):
            if (lapTime2 > "00:02:00"):
                if (len(laps2) > 1):
                    fastestTime2 = min(laps2)
                else:
                    fastestTime2 = lapTime2
                winsound.Beep(frequency, duration)
                print ("Driver2 passed line")
                laps2Counter += 1
                laps2.append(lapTime2)
                lastLap2 = lapTime2
                starttime2 = datetime.now()

        print_scoreboard()
        message_status1(1,fitText("1     DRIVER 1    " + str(lapTime1) + "       " + str(fastestTime1)))
        message_status1(2,fitText("2     DRIVER 2    " + str(lapTime2) + "       " + str(fastestTime2)))

    if (status == "RESTART"):
        message_status("Restart game ?")

    if (status == "RESET"):
        counter1, text1 = 60, '60'.rjust(3)
        counter2, text2 = 60, '60'.rjust(3)
        status = "READY"

    pygame.display.update()
    pygame.display.flip()
    clock.tick(200)