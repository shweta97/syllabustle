import ics
import dateparser
import pandas as pd
import datetime

#Take in filenames containing tables of parsed syllabus information
#and return .ics file containing calendar with all events scheduled.

#pick up input file from scr
inputFile = "events.txt"

#df column building
cCourse = []
cStart = []
cName = []
cSDate = []

#Read in file data containing events
#Each file will contain a set of pairs of lines
#such that each pair represents a schedule.
#The first line of the pair is the term start date
#the second is a list of tuples of (Name, Date)

def parseFile(f):
    with open(f, 'r') as file:
        allSchedules = file.readlines()
    file.close()

    #even indices of allSchedules are start dates
    #odd indices are lists of deadlines.
    #for each deadline, fill dataframe with corresponding
    #startDate, Name, and Date.

    i=0
    while i < len(allSchedules)-2:
        for d in eval(allSchedules[i+2]):
            cCourse.append(allSchedules[i].rstrip('\n'))
            cStart.append(allSchedules[i+1].rstrip('\n'))
            cName.append(d[0])
            cSDate.append(d[1])
        i += 3

#parse user input
parseFile(inputFile)

#parse dates to "YYYY-MM-DD" format
#Dateparser applies current year to dates
#when year value is missing - correct for
#courses that span over two years
#(where dateParsed < startDate for the term)

def incrementYear(wrongDate):
    return wrongDate.replace(wrongDate.year + 1)

def incrementDay(moment):
    return moment + datetime.timedelta(days=1)

#fill cEDate prior to indexing
cEDate = cSDate[:]

i=0
while i in range(len(cSDate)):
    cSDate[i] = dateparser.parse(cSDate[i])
    cStart[i] = dateparser.parse(cStart[i])
    #if not possible to parse the record, remove it
    if (cSDate[i] is None) or (cName[i] is None):
        del cCourse[i]
        del cStart[i]
        del cName[i]
        del cSDate[i]
        del cEDate[i]
        #if we enter this if we don't want to run
        #the next as it may fall over non-datetime values
        i -= 1
    if cSDate[i] < cStart[i]:
        cSDate[i] = incrementYear(cSDate[i])
    #cEDate[i] = incrementDay(cSDate[i])
    i += 1


#Build dataframe with events for calendar
d = {"start" : cStart,
     "name" : cName,
     "sdate" : cSDate,
     "edate" : cEDate}

cal = pd.DataFrame(d)

#Helper to apply event to a row
def rowToEvent(row):
    return (ics.event.Event(name=row["name"],
                            begin=row["sdate"],
                            end=row["edate"]))

#.make_all_day() as a non-transormative funcation
def retAllDay(event):
    event.make_all_day()
    return event

#Apply event creation to every event in dataframe and store in new col
cal["event"] = cal.apply(rowToEvent, axis=1)

#Make all deadlines all day events; appear at top of calendar
cal["event"] = cal["event"].apply(retAllDay)

#Create calendar
C = ics.Calendar(events = list(cal["event"]))

#Export build calendar
with open('deadlines.ics', 'w') as file:
    file.writelines(C)
file.close()