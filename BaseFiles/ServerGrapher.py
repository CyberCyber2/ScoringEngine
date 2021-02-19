import pandas as pd
import time
from pandas import Series
import matplotlib.pyplot as plot
import numpy as np
import os,sys
from datetime import datetime
#################################
def find(df, user, time): #returns the points at the row with a specific user and time
    for i, row in df.iterrows():
        if row.time == time and row.user == user:
            return row.points
    return 0

def getLatestPts(user):
    file = ".parsed.csv"
    last_match = None
    for line in open(str(file)):
        if user in line:
            last_match =  str(line.split(",")[1])
    return last_match

while (True): #Results in an error until first POST requests come in and the file Output.csv is created
    os.system("awk -F, '!seen[$1$3]++' Output.csv > .parsed.csv") #remove duplicate time rows
    parsedFile = ".parsed.csv"
    df = pd.read_csv(parsedFile, names = ["user", "points", "time"])

    #Array of all possible times and points. If one user has a time that user2 doesnt; user 2's points at the missing time is 0
    uniqueTimesStr = df["time"].unique() #unique time values from file
    uniqueTimesInt = [int(numeric_string) for numeric_string in uniqueTimesStr]
    uniquePointsStr = df["points"] #.unique()
    uniquePointsInt = [int(numeric_string) for numeric_string in uniquePointsStr]
    maxX = max(uniqueTimesInt)
    maxPts = max(uniquePointsInt)
    minX = min(uniqueTimesInt)
    minPts = min(uniquePointsInt)
    #list of users to create graphs for
    uniqueUsers =  df["user"].unique()
    npUTI = np.array(uniqueTimesInt) #convert the array to be numpy compatable
    filled_arr = list(range(int(npUTI[-1])+1)) #fill in "missing" values in the array

    for currUser in uniqueUsers: #for every unique user in the .csv(column1)
        xValuesToPlot = sorted(filled_arr) #Array of all the needed x values
        yValuesToPlot = [] #if a certain xValueToPlot does not exist for a user; make their points(y value) there 0
        for tt in xValuesToPlot: #tt is every time value in the array xValuesToPlot
            yValuesToPlot.append(int(find(df, currUser, tt)))
            print(currUser + "'s points at time " + str(tt) + " are " + str(find(df, currUser, tt)))
        ####################
        #plot.plot(xValuesToPlot,yValuesToPlot, 'ro')

        x=np.array(xValuesToPlot)
        y=np.array(yValuesToPlot)
        plot.plot(x,y,color ="blue")
        plot.xlim((minX,maxX))
        plot.ylim(minPts,maxPts + 1)
        plot.axhline(y=0, linewidth=0.5, color = "black")
        plot.suptitle(currUser + " Score: " + str(getLatestPts(currUser)), fontsize=20)
        plot.xlabel('Minutes Elapsed', fontsize=16)
        plot.ylabel('Score' , fontsize=16)
        plot.savefig(currUser + ".png")
        plot.legend()
        #plot.show()
        plot.clf()
        #plot.show(block=True);

    #Make The Website#
    os.system('touch ScoreReport.html')
    os.system('chmod 777 *')
    h = open('ScoreReport.html','w')
    h.write('<!DOCTYPE html> <html> <head> <meta name="viewport" content="width=device-width, initial-scale=1"> <style> * { box-sizing: border-box; } .column { float: left; padding: 10px; height: 1500px; } .left, .right { width: 25%; } .middle { width: 50%; } .row:after { content: ""; display: table; clear: both; }</style> </head> <body><div class="row"> <div class="column left" style="background-color:#0d60bf;"></div> <div class="row"> <div class="column middle" style="background-color:#fff;"><h1 style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Score Report</span></h1><h2 style="text-align: center;"><br /><span style="font-family: arial, helvetica, sans-serif;">' +'</span></h2><p> </p>')
    h.write('<p><span style="font-family: arial, helvetica, sans-serif; text-align: center;"><strong>' + "Report Generated at: " + str(datetime.utcnow()) + ' </strong></span></p>')
    h.write('<style> div { background-image: url(https://i.pinimg.com/originals/15/79/25/157925e28f33c43a30973791b2f787f4.jpg); background-blend-mode: lighten; } </style>')
    h.write('<hr class="line2"><br>')
    for usr in uniqueUsers:
        h.write('<img src=' + usr + '.png' + ' alt="Graph" width="350" height="250">')
    h.write('<img src=' + 'InjectSLA' + '.png' + ' alt="Graph" width="550" height="450">')
    h.write('</div> <div class="row"> <div class="column right" style="background-color:#0d60bf;"></div> </body>')
    h.write('<meta http-equiv="refresh" content="20">')
    h.write('<footer><h6>Cyber Club</h6></footer>')
    time.sleep(20)
