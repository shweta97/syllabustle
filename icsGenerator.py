#!/usr/bin/python

import sys
import ics
import dateparser
import pandas as pd

#Take in filenames containing tables of parsed syllabus information
#and return .ics file containing calendar with all events scheduled.
#Fs = str(sys.argv)

#Maintain list for each data column
#cName = ["Assignment #1", "A2"]
#cWeight = ["75%", "12%"]
#cDate = ["20180201 00:00:00", "2018-02-04"]

#For testing
cName = ["Assignment #1", "A2"]
cWeight = ["75%", "12%"]
cDate = ["20180201 00:00:00", "2018-02-04"]


#Read in file data containing events
##for f in Fs:
    #Helper for file type parsing
    #Append appropriate data to each column list
    #Parse dates to "YYYY-MM-DD" format

#Build dataframe with events for calendar
d = {"name" : cName,
     "weight" : cWeight,
     "date" : cDate}

df = pd.DataFrame(d)

#Helper to apply event to a row
def rowToEvent(row):
    return (ics.event.Event(name=row["name"],
            description=row["weight"],
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