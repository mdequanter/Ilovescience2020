
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
import sqlite3

# ----------------- SETTINGS --------------------------

host = "localhost"
port = 1883
topic = "tags"
tag1 = '27211'
tag2 = '27241'


# -----------------------------------------------------

x1 = 0
y1 = 0
yaw1 = 0
x2 = 0
y2 = 0
yaw2 = 0


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

    starttime1 = datetime.now()
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
                                    x1 = value3
                            if key3 == 'y':
                                    y1 = value3
                    if key2 == 'orientation':
                        for key3, value3 in value2.items():
                            if (key3 == 'yaw') :
                                    yaw1 = value3
    #cur = conn.cursor()
    #cur.execute(
    #    "INSERT INTO data (tag,timestamp,coordinates_x,coordinates_y,coordinates_z,acceleration_x,acceleration_y,acceleration_z,orientation_heading,orientation_roll,orientation_pitch) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
    #    (currentTag, starttime1, x1, y1, 0, 0,0,0,yaw1,0,0))
    print (currentTag,x1,y1,yaw1)
    #conn.commit()
    return


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")


client = mqtt.Client()

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)


#database = "karting.db"
#conn = sqlite3.connect(database)

client.loop_forever()
