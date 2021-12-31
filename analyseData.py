from datetime import datetime
import math
import sqlite3
from sqlite3 import Error
import csv



# ----------------- SETTINGS --------------------------

#measured line x = -590 -> 880, Avg Y :  1268

driver = {}
driver["27241"] = 'Driver1'
driver["27205"] = 'Driver2'
driver["27211"] = 'Driver3'
minLapTime = 5
FinishLinePoint1_X = 1200
FinishLinePoint1_Y = -500
FinishLinePoint2_X = 1300
FinishLinePoint2_Y = 1200

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


file = open("tagdata.txt", "r")


Xold = 0
Yold = 0
counter = 0
wrong = 0


lapCounter = {}
lapCounter["27241"] = 0
lapCounter["27205"] = 0
lapCounter["27211"] = 0

timeOld = {}
timeOld["27241"] = '00:00:00.0000'
timeOld["27205"] = '00:00:00.0000'
timeOld["27211"] = '00:00:00.0000'


reader = csv.reader(file, delimiter="|")

cursor = conn.cursor()
cursor.execute("DELETE from laps")
conn.commit()

for i, row in enumerate(reader):

    Xold = row[2]
    Yold = row[3]

    counter = counter+1

    timeStr = str(row[0])[11:-1]
    FMT = '%H:%M:%S.%f'
    timeDiff = str(datetime.strptime(timeStr, FMT) - datetime.strptime(timeOld[row[1]], FMT))
    timeDiffString = timeDiff[6:-4]
    timeDiffString = float(timeDiffString)
    newLap = detectFinish(float(row[2]),float(row[3]),timeDiffString)

    if (newLap == 1) :
        lapCounter[row[1]] = lapCounter[row[1]]+1
        cursor = conn.cursor()
        cursor.execute("INSERT INTO laps (tag,drivername,lap,laptime,timestamp) VALUES (?,?,?,?,?)",
                    (row[1], driver[row[1]], lapCounter[row[1]], timeDiffString,row[0]))
        conn.commit()
        timeOld[row[1]] = timeStr

conn.close()

