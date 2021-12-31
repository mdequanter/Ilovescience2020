# !/usr/bin/env python
"""
Author :  Maarten Dequanter
Created : 26/01/2020

I lOVE LOVE SCIENCE 2020

Load all pozyx tags data and load to database (sqlite)




"""
from time import sleep
from datetime import datetime
from datetime import timedelta
from shutil import copyfile
import math


from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, PozyxRegisters, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, SensorData)
from pythonosc.udp_client import SimpleUDPClient

from pypozyx.tools.version_check import perform_latest_version_check

import sqlite3
from sqlite3 import Error

import winsound


# ----------------- SETTINGS --------------------------

#measured line x = -590 -> 880, Avg Y :  1268

driver = {}
driver["27241"] = 'Driver1'
driver["27205"] = 'Driver2'
driver["27211"] = 'Driver3'
driver["27210"] = 'Driver4'
minLapTime =5
FinishLinePoint1_X = -10000
FinishLinePoint1_Y = -10000
FinishLinePoint2_X = 10000
FinishLinePoint2_Y = 700
FinishLevel1 = 0
FinishLevel2 = 79

# -----------------------------------------------------

starttime1 = datetime.now()
f = open("tagdata.txt", "a")

lapCounter = {}
lapCounter["27241"] = 0
lapCounter["27205"] = 0
lapCounter["27211"] = 0
lapCounter["27210"] = 0

timeOld = {}
timeOld["27241"] = '2020-02-20 00:00:00.0000'
timeOld["27205"] = '2020-02-20 00:00:00.0000'
timeOld["27211"] = '2020-02-20 00:00:00.0000'
timeOld["27210"] = '2020-02-20 00:00:00.0000'


xpos = {}
xpos["27241"] = 0
xpos["27205"] = 0
xpos["27211"] = 0
xpos["27210"] = 0

ypos = {}
ypos["27241"] = 0
ypos["27205"] = 0
ypos["27211"] = 0
ypos["27210"] = 0

posCounter =  {}
posCounter["27241"] = 0
posCounter["27205"] = 0
posCounter["27211"] = 0
posCounter["27210"] = 0

x = {}
x["27241"] = 0
x["27205"] = 0
x["27211"] = 0
x["27210"] = 0

y = {}
y["27241"] = 0
y["27205"] = 0
y["27211"] = 0
y["27210"] = 0

#database = "racedb/karting_" + starttime1.strftime("%Y%m%d%H%M%S") + ".db"
database = "racedb/karting.db"
copyfile("karting.db", database)
conn = sqlite3.connect(database)

cursor = conn.cursor()
cursor.execute("DELETE from laps")
conn.commit()

cursor = conn.cursor()
cursor.execute("DELETE from data")
conn.commit()


class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, pozyx, osc_udp_client, tag_ids, anchors, algorithm=PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY,
                 dimension=PozyxConstants.DIMENSION_2D, height=50):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.tag_ids = tag_ids
        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")
        print(" - System will manually calibrate the tags")
        print("")
        print(" - System will then auto start positioning")
        print("")
        if None in self.tag_ids:
            for device_id in self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None] + self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")

        self.setAnchorsManual(save_to_flash=False)

        self.printPublishAnchorConfiguration()

    def loop(self):
        """Performs positioning and prints the results."""
        for tag_id in self.tag_ids:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag_id)
            if status == POZYX_SUCCESS:
                self.printPublishPosition(position, tag_id)
            # else:
            # self.printPublishErrorCode("positioning", tag_id)

    def printPublishPosition(self, position, network_id):
        global starttime1
        global conn
        global f
        global timeOld
        global x,y,xpos,ypos,posCounter

        sensor_data = SensorData()
        self.pozyx.getAllSensorData(sensor_data, network_id)

        chronotime = ChronoMeter(starttime1)
        starttime1 = datetime.now()


        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}, sensor: {}, updated: {}".format("0x%0.4x" % network_id,
                                                                                          position.x, position.y,
                                                                                          position.z,
                                                                                          sensor_data.euler_angles,
                                                                                          chronotime)
        #print (chronotime)

        #cur = conn.cursor()
        #cur.execute("INSERT INTO data (tag,timestamp,coordinates_x,coordinates_y,coordinates_z,acceleration_x,acceleration_y,acceleration_z,orientation_heading,orientation_roll,orientation_pitch) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        #            (network_id, starttime1, position.x, position.y, position.z,sensor_data.acceleration.x,sensor_data.acceleration.y,sensor_data.acceleration.z,sensor_data.euler_angles.heading,sensor_data.euler_angles.roll,sensor_data.euler_angles.pitch))
        #conn.commit()

        content = str(starttime1) + "|" + str(network_id) + "|" + str(position.x)  + "|" + str(position.y)  + "|" + str(sensor_data.euler_angles.heading)  + "\n"
        #f.write(content)

        network_id = str(network_id)

        x[network_id] = float(position.x)
        y[network_id] = float(position.y)
        x[network_id] = math.floor(x[network_id])
        y[network_id] = math.floor(y[network_id])

        xpos[network_id] = xpos[network_id] + x[network_id]
        ypos[network_id] = ypos[network_id] + y[network_id]

        posCounter[network_id] = posCounter[network_id]+1


        FMT = '%Y-%m-%d %H:%M:%S.%f'
        diff = datetime.strptime(str(starttime1), FMT) - datetime.strptime(str(timeOld[network_id]), FMT)
        difference = diff.seconds + diff.microseconds / 1000000
        if (difference > 99.99) :
            difference = 99.99
        newLap = detectFinish(float(position.x), float(position.y),float(sensor_data.euler_angles.roll), float(difference))


        #if (network_id == '27211') :
        #    print (position.x,position.y,sensor_data.euler_angles.roll)

        if (newLap == 1):
            lapCounter[network_id] = lapCounter[network_id] + 1
            cursor = conn.cursor()
            cursor.execute("INSERT INTO laps (tag,drivername,lap,laptime,timestamp) VALUES (?,?,?,?,?)",
                           (network_id, driver[network_id], lapCounter[network_id], difference, starttime1))
            conn.commit()
            #print(network_id, timeOld[network_id], str(starttime1),str(difference) )
            timeOld[network_id] = starttime1


        if (posCounter[network_id] == 5):
            xpos[network_id] = (xpos[network_id] / 5)
            ypos[network_id] = (ypos[network_id] / 5)
            posCounter[network_id] = 0
            if (lapCounter[network_id] >=1) :
                cur = conn.cursor()
                cur.execute("INSERT INTO data (tag,timestamp,coordinates_x,coordinates_y,acceleration_x,acceleration_y,lap) VALUES (?,?,?,?,?,?,?)",(network_id, starttime1, xpos[network_id], ypos[network_id], 0, 0,lapCounter[network_id]))
                conn.commit()

        if (newLap == 1):
            winsound.Beep(8000, 100)

        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def setAnchorsManual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters([PozyxRegisters.POSITIONING_NUMBER_OF_ANCHORS], tag_id)

            self.printPublishConfigurationResult(status, tag_id)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error_%s" % operation, [0, error_code[0]])

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.pos.x, anchor.pos.y, anchor.pos.z])
                sleep(0.025)


def ChronoMeter(timer):
    timeDiff = datetime.now() - timer
    timeStr = str(timeDiff)
    returnStr = timeStr[5:-4]
    return returnStr


def detectFinish(X, Y,level, timediff):
    global FinishLinePoint1_X, FinishLinePoint1_Y, FinishLinePoint2_X, FinishLinePoint2_Y, minLapTime,FinishLevel1,FinishLevel2

    if (timediff > minLapTime and level > FinishLevel1 and level < FinishLevel2):
        return 1
    else:
        return 0


if __name__ == "__main__":
    # Check for the latest PyPozyx version. Skip if this takes too long or is not needed by setting to False.
    check_pypozyx_version = True
    if check_pypozyx_version:
        perform_latest_version_check()

    # shortcut to not have to find out the port yourself.
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # enable to send position data through OSC
    use_processing = True

    # configure if you want to route OSC to outside your localhost. Networking knowledge is required.
    ip = "127.0.0.1"
    network_port = 8888

    # IDs of the tags to position, add None to position the local tag as well.
    tag_ids = [0x6a4B,0x6a4a]
    #tag_ids = [0x6a4a]

    # necessary data for calibration
    anchors = [DeviceCoordinates(0x6A21, 1, Coordinates(130, 0, 990)),
               DeviceCoordinates(0x6A40, 1, Coordinates(2660, 0, 990)),
               DeviceCoordinates(0x6A38, 1, Coordinates(130, 5550, 990)),
               DeviceCoordinates(0x6A15, 1, Coordinates(2660, 5550, 990))]

    # positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING OR POSITIONING_ALGORITHM_UWB_ONLY
    algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
    # positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
    dimension = PozyxConstants.DIMENSION_2D
    # height of device, required in 2.5D positioning
    height = 50

    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    pozyx = PozyxSerial(serial_port)

    r = MultitagPositioning(pozyx, osc_udp_client, tag_ids, anchors,
                            algorithm, dimension, height)
    r.setup()

    while True:
        r.loop()
