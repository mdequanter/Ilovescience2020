from datetime import datetime
import math
import sqlite3
from sqlite3 import Error



# ----------------- SETTINGS --------------------------

#measured line x = -590 -> 880, Avg Y :  1268


tag1 = '27211'
tag2 = '27241'
driver1 = 'Maarten'
driver2 = 'An'
minLapTime = 2.00
FinishLinePoint1_X = -700
FinishLinePoint1_Y = 900
FinishLinePoint2_X = 1200
FinishLinePoint2_Y = 1300

# -----------------------------------------------------


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
	
	
def detectFinish(X,Y, timediff):
    global FinishLinePoint1_X, FinishLinePoint1_Y, FinishLinePoint2_X, FinishLinePoint2_Y,minLapTime


    
    if (X > FinishLinePoint1_X and X < FinishLinePoint2_X and Y > FinishLinePoint1_Y and Y < FinishLinePoint2_Y  and timediff > minLapTime):
        return 1
    else:
        return 0




database = "karting.db"
conn = sqlite3.connect(database)

cursor = conn.cursor()
cursor.execute("SELECT tag,timestamp,coordinates_x,coordinates_y FROM data WHERE tag='27241' and lap is NULL order by ID")
rows = cursor.fetchall()

Xold = 0
Yold = 0
timeOld = '00:00:00.0000'
counter = 0
wrong = 0

lapCounter = 0

for row in rows:
    distance = calculateDistance(Xold, row[2], Yold, row[3])
    Xold = row[2]
    Yold = row[3]

    counter = counter+1

    timeStr = str(row[1])[11:-1]
    FMT = '%H:%M:%S.%f'
    timeDiff = str(datetime.strptime(timeStr, FMT) - datetime.strptime(timeOld, FMT))
    timeDiffString = timeDiff[6:-4]
    timeDiffString = float(timeDiffString)
    newLap = detectFinish(row[2],row[3],timeDiffString)

    if (newLap == 1) :
        lapCounter = lapCounter+1
        cursor = conn.cursor()
        cursor.execute("INSERT INTO laps (tag,drivername,lap,laptime,timestamp) VALUES (?,?,?,?,?)",
                    (row[0], driver1, lapCounter, timeDiffString,row[1]))
        conn.commit()
        timeOld = timeStr
conn.close()

