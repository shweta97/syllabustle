#!/usr/bin/python

import sys
import ics
import dateparser
import pandas as pd

#Take in filenames containing tables of parsed syllabus information
#and return .ics file containing calendar with all events scheduled.

inputFile = str(sys.argv)

#df column building
cStart = []
cName = []
cDate = []

#Read in file data containing events
#Each file will contain a set of pairs of lines
#such that each pair represents a schedule.
#The first line of the pair is the term start date
#the second is a list of tuples of (Name, Date)

def parseFile(f):
    with open(f, 'r') as file:
        allSchedules = f.readlines()
    f.close()
    #even indices of allSchedules are start dates
    #odd indices are lists of deadlines.
    #for each deadline, fill dataframe with corresponding
    #startDate, Name, and Date.
    i = 0
    while i < len(allSchedules):
        for d in allSchedules[i+1]:
            cStart.append(allSchedules[i])
            cName.append(d[0])
            cDate.append(d[1])
        i += 2

#parse user input
parseFile(inputFile)

#parse dates in cDate to "YYYY-MM-DD" format
#Dateparser applies current year to dates
#when year value is missing - correct for
#courses that span over two years
#(where dateParsed < startDate for the term)

#Build dataframe with events for calendar
d = {"name" : cName,
     "date" : cDate}

df = pd.DataFrame(d)

#Helper to apply event to a row
def rowToEvent(row):
    return (ics.event.Event(name=row["name"],
            begin=row["date"]))

#.make_all_day() as a non-transormative funcation
def retAllDay(event):
    event.make_all_day()
    return event

#Apply event creation to every event in dataframe and store in new col
df["event"] = df.apply(rowToEvent, axis=1)

#Make all deadlines all day events; appear at top of calendar
#df["event"] = df["event"].apply(retAllDay)

#Create calendar
C = ics.Calendar(events = list(df["event"]))

#Export build calendar
with open('deadlines.ics', 'w') as file:
    file.writelines(C)
file.close()