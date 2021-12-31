from datetime import datetime
import paho.mqtt.client as mqtt
import json
import math
import sqlite3
from sqlite3 import Error



# ----------------- SETTINGS --------------------------
tag1 = '27211'
tag2 = '27241'

host = "localhost"
port = 1883
topic = "tags"

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

# -----------------------------------------------------



currentTag = '000000'
coordinates_x = 0
coordinates_y = 0
coordinates_z = 0
acceleration_x = 0
acceleration_y = 0
acceleration_z = 0
orientation_yaw = 0
orientation_roll = 0
orientation_pitch = 0
dataTimestamp = 0





tagContent = []

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))



# callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    global currentTag,dataTimestamp,coordinates_x,coordinates_y,coordinates_z,acceleration_x,acceleration_y,acceleration_z,orientation_yaw,orientation_roll,orientation_pitch

    tag = msg.payload.decode()
    tagContent = json.loads(tag)

    for tag in tagContent:
        for key, value  in tag.items():
            if (key == 'tagId'):
                currentTag = value
            if (key == 'timestamp'):
                dataTimestamp = value
            if key == 'data':
                for key2, value2 in value.items():
                    if key2 == 'coordinates':
                        for key3, value3 in value2.items():
                            if  key3 == 'x':
                                coordinates_x = value3
                            if key3 == 'y':
                                coordinates_y = value3
                            if key3 == 'z':
                                coordinates_z = value3

                    if key2 == 'orientation':
                        for key3, value3 in value2.items():
                            if (key3 == 'yaw') :
                                orientation_yaw = value3
                            if (key3 == 'pitch') :
                                orientation_pitch = value3
                            if (key3 == 'roll') :
                                orientation_roll = value3

                    if key2 == 'acceleration':
                        for key3, value3 in value2.items():
                            if (key3 == 'x') :
                                acceleration_x = value3
                            if (key3 == 'y') :
                                acceleration_y = value3
                            if (key3 == 'y') :
                                acceleration_z = value3
    return


def markErrors(tagId) :
    print ("markErrors")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


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

done = False

database = "karting.db"
conn = sqlite3.connect(database)



while not done:
    client.loop()
    #distance1 = calculateDistance(Xold,x1,Yold,y1)
    if (coordinates_x != 0 and coordinates_y !=0 and coordinates_z!=0) :
        cur = conn.cursor()
        cur.execute("INSERT INTO data (tag,timestamp,coordinates_x,coordinates_y,coordinates_z,acceleration_x,acceleration_y,acceleration_z,orientation_yaw,orientation_roll,orientation_pitch) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (currentTag, dataTimestamp, coordinates_x, coordinates_y, coordinates_z, acceleration_x, acceleration_y,acceleration_z, orientation_yaw, orientation_roll, orientation_pitch))
        conn.commit()




conn.close()

