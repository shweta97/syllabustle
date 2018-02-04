#!/usr/bin/python

import sys
import ics
import dateparser
import pandas as pd

#Take in filenames containing tables of parsed syllabus information
#and return .ics file containing calendar with all events scheduled.

Fs = str(sys.argv)

#Maintain list for each data column
#cName = []
#cWeight = []
#cDate = []

#For testing
cName = ["Assignment #1", "A2"]
cDate = ["20180201 00:00:00", "02-04"]

#Read in file data containing events
#Each file will contain a list of tuples of Name, Date,
#and possibly some string informaiton relating ot the deadline
#Each file will carry with it term start date

def parseFile(f):
    #first line is course start date
    #second line holds a list of tuples (name,date)

##for f in Fs:
    #Helper for file type parsing

    #Take earliest date in schedule
    #Take latest date in schedule
    #

    #Append appropriate data to each column list
    #Parse dates to "YYYY-MM-DD" format

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