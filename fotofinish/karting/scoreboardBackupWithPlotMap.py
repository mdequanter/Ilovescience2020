
import pygame
import sys,math
from pygame.locals import *
import os

import ssl
import json
import time
from datetime import datetime
import array

import ssl
import json


# ----------------- SETTINGS --------------------------

# set maximum width of screen based on the resolution of your screen
display_width = 1248
display_height = 1024
mapWidth = 600

# -----------------------------------------------------

clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)





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

def fitText(text, lenght):
    if (len(text) < lenght) :
        while (len(text) <= lenght) :
            text = text + " "
    return text

def print_scoreboard() :
    global conn

    cursor = conn.cursor()
    cursor.execute("select L.drivername,MIN(L.laptime) as bestLap,count(L.drivername) as laps, (SELECT laptime from laps L2 where L.drivername = L2.drivername order by ID DESC limit 1) as lastlap from laps L group by drivername order by bestLap")
    rows = cursor.fetchall()

    position = 20
    counter = 1

    largeText = pygame.font.Font('CourierPrime.ttf',30)
    text = "Pos      Driver               Best lap     Last lap     lapsCount"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = (5,position)
    screen.blit(TextSurf, TextRect)

    for row in rows:
        position = position + 30

        best = "%.4f" % row[1]
        last = "%.4f" % row[3]

        text = fitText(str(counter),8) + fitText(str(row[0]),20) + fitText(best,12)  + fitText(last,12) + fitText(str(row[2]),8)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.topleft = (5, position)
        counter = counter+1
        screen.blit(TextSurf, TextRect)


def print_bestLaps(laps) :
    global mapWidth,red,blue
    largeText = pygame.font.Font('CourierPrime.ttf',30)
    text = "Best laps"
    TextSurf, TextRect = text_objects(text, largeText)
    position = 5
    TextRect.topleft = (position,200)
    screen.blit(TextSurf, TextRect)
    color = red
    lapCounter = 0
    height = 250
    for lap in laps :
        lapCounter = lapCounter+1
        if (lapCounter > 2) :
            lapCounter = 0
            height = height + 350
            position = 5
            
        if (color == blue) :
            color = red
        else  :
            color = blue
        print_oneBestLap(lap,position,color,height)
        position = position + mapWidth


def getLapPositions(tag,lap) :
    cursor = conn.cursor()
    cursor.execute("SELECT coordinates_x, coordinates_y from data where tag = '" + str(tag) + "' and lap = '" + str(lap) + "' order by ID")
    rows = cursor.fetchall()
    return rows

def print_oneBestLap(lap,position,color,height) :
    global white, black,conn,mapWidth,red


    largeText = pygame.font.Font('CourierPrime.ttf',30)
    text = lap[2] + " " +  "%.4f" % lap[0] + " (round " + str(lap[1]) + ")"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = (position+3,height)
    # draw a rectangle
    pygame.draw.rect(screen, black, pygame.Rect(position, height+30, mapWidth+5, mapWidth/2+5), 2)
    data = getLapPositions(lap[0],lap[2])
    lastx = 0
    lasty = 0

    counter = 0

    firstposx = 0
    firstposy = 0

    for coordinates in data :
        counter = counter+1
        x = math.floor(coordinates[1]/10)
        y = math.floor(coordinates[0]/10)
        if (x > mapWidth ) : x = mapWidth
        if (y > mapWidth/2 ) : y = math.floor(mapWidth/5)
        if (x < 5 ) : x = 5
        if (y < 5 ) : y = 0
        posx = position+x
        posy = height+83+y
        if (counter == 1) :
            firstposx = posx
            firstposy = posy

        if (lastx and lasty) :
            pygame.draw.line(screen, color, (lastx, lasty), (posx, posy), 2)
        lastx = posx
        lasty = posy

    #pygame.draw.line(screen, color, (firstposx, firstposy), (lastx, lasty), 2)

    screen.blit(TextSurf, TextRect)



def countDown(t):
    global timer1
    largeText = pygame.font.Font('CourierPrime.ttf', 70)
    while  t > 0 :
        text = str(t)
        message_status(text)
        time.sleep(1)
        t -= 1
    timer1 = time.time()
    return

def getBestLaps() :
    global conn
    cursor = conn.cursor()
    cursor.execute(
        "select min(laptime) as laptime,lap,drivername from laps L group by drivername order by laptime")
    rows = cursor.fetchall()
    return rows


def ChronoMeter(timer) :
    timeDiff = datetime.now() - timer
    timeStr = str(timeDiff)
    returnStr = timeStr[2:-4]
    return returnStr


import sqlite3

database = "karting.db"
conn = sqlite3.connect(database)


pygame.init()

imagebox_width = 300
imagebox_height = 150


screen = pygame.display.set_mode((display_width, display_height), RESIZABLE)
car1_image = pygame.image.load("fotofinish/car1.jpg").convert()
car1_image_resised = pygame.transform.scale(car1_image, (imagebox_width,imagebox_height ))
car2_image = pygame.image.load("fotofinish/car2.jpg").convert()
car2_image_resised = pygame.transform.scale(car2_image, (imagebox_width,imagebox_height ))
car3_image = pygame.image.load("fotofinish/car3.jpg").convert()
car3_image_resised = pygame.transform.scale(car3_image, (imagebox_width,imagebox_height ))

pygame.mouse.set_visible(0)
screen.fill(white)

done = False


text1 = ""
text2 = ""

status = "RESET"


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game = 'started'

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_BACKSPACE]: status = "PAUZED"
    if pressed[pygame.K_SPACE]:
        status = "RUN"
 
    if pressed[pygame.K_DELETE]: status = "RESET"
    if pressed[pygame.K_LEFT]: y1 -= 10
    if pressed[pygame.K_RIGHT]: y1 += 10
    if pressed[pygame.K_UP]: x1 -= 10
    if pressed[pygame.K_DOWN]: x1 += 10

    screen.fill(white)


    if (status == "READY"):
        message_status("Get ready!")
    if (status == "RUN"):
        print_scoreboard()
        bestLaps = getBestLaps()
        print_bestLaps(bestLaps)


    if (status == "RESTART"):
        message_status("Restart game ?")

    if (status == "RESET"):
        status = "READY"        
        cursor = conn.cursor()
        cursor.execute("DELETE from laps")
        conn.commit()

    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)
