import pygame
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import winsound
import math


# ----------------- SETTINGS --------------------------
display_width = 1500

# set max X and Y coordinates of the playing field
maxY = 5383
maxX = 4261


tag1 = '27211'
tag2 = '27241'

host = "localhost"
port = 1883
topic = "tags"

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

# -----------------------------------------------------

ratio = maxY/maxX
display_height = int(display_width / ratio)
transformX =  display_height / maxX
transformY =  display_width / maxY

transformX =  display_height / maxX
transformY =  display_width / maxY


x1 = 0
y1 = 0
yaw1 = 0
x2 = 0
y2 = 0
yaw2 = 0

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)


currentTag = '00000'

_image_library = {}


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


def calculateDistance(Xold,Xnew,Yold,Ynew):
    distance = math.sqrt(((Xnew-Xold)**2)+((Ynew-Yold)**2))
    return distance

client = mqtt.Client()

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)


pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
background_image = pygame.image.load("backgroundRace.png").convert()
background_image_resised = pygame.transform.scale(background_image, (display_width,display_height))


done = False

Xold = 0
Yold = 0

clock = pygame.time.Clock()

screen.blit(background_image_resised, [0, 0])

while not done:
    client.loop(timeout=1.0, max_packets=1)
    distance1 = calculateDistance(Xold,x1,Yold,y1)
    if (distance1 < 1000) :
        gameCoX1 = int(y1 * transformX)
        gameCoY1 = int(x1 * transformY)
        #print(gameCoX1, gameCoY1, distance1)
        pygame.draw.circle(screen, red, (gameCoX1, gameCoY1), 10, 10)
        pygame.display.update()
        pygame.display.flip()
    else :
        print (distance1)

    Xold = x1
    Yold = y1
    #clock.tick(30)

