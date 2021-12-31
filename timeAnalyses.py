import pygame
import sys
from pygame.locals import *
import csv
import math
import asyncio


pygame.init()
screen = pygame.display.set_mode((1000,1000))
myfont = pygame.font.Font(None, 60)
screen.fill((255,255,255))

inp = ""


def loadData(tag) :

    global screen

    screen.fill((255, 255, 255))

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    color = black

    file = open("tagdataOld.txt", "r")
    reader = csv.reader(file, delimiter="|")

    x = 0
    y = 0
    counter = 0
    xpos = 0
    ypos = 0

    for i, row in enumerate(reader):

        if (i < 750) :

            if (row[1] == tag) :

                print (i)

                x = float(row[2])
                y = float(row[3])
                x = math.floor(x)
                y = math.floor(y)

                xpos = xpos + x
                ypos = ypos + y

                counter = counter+1

                if (counter == 5) :
                    xpos = (xpos/50)*2
                    ypos = (ypos/50)*2
                    counter = 0
                    print (row[0],str(xpos),str(ypos))
                    pygame.draw.circle(screen, color, (math.floor(xpos), math.floor(ypos)), 2, 2)
                    pygame.display.update()

            '''
            x = float(row[2])/10
            y = float(row[3]+2000)/10
            x = math.floor(x)
            y = math.floor(y)

            xpos = xpos+x
            ypos = ypos+y

            
            if (row[1] == '27211') :
                color = blue
            if (row[1] == '27245') :
                color = red
            if (row[1] == '27205') :
                color = black
            '''
    '''
    xpos = xpos/10
    ypos = ypos/10

    print (xpos,ypos)
    pygame.draw.circle(screen, color, (math.floor(xpos), math.floor(ypos)), 2, 2)
    pygame.display.update()
    '''

async def detectKeys() :

    line = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        print ('loading 27211')
                        loadData('27211')
                    if event.key == pygame.K_2:
                        print ('loading 27205')
                        loadData('27205')
                    if event.key == pygame.K_3:
                        print ('loading 27241')
                        loadData('27241')
detectKeys()


async def main():
    detectKeysTask = asyncio.create_task(detectKeys())
    await detectKeysTask


asyncio.run(main())



