import urllib.request, urllib.parse, urllib.error
import json
import re
import requests
import ssl
import datetime
from tkinter import *

# Define colors
bgcolor = "#4F5257"
dispBgColor = "#110F04"
dispTextColor = "#DED311"
lineColorGreen = "#00A748"
lineColorBlue = "#0095D2"
lineColorRed = "#E40315"
lineColors = {
    "10": lineColorBlue,
    "11": lineColorBlue,
    "13": lineColorRed,
    "14": lineColorRed,
    "17": lineColorGreen,
    "18": lineColorGreen,
    "19": lineColorGreen,
    }



# Configuration
refInt = 20000
stationKey = "9ef9290d-c9ae-409c-9862-2b0e5d847b2a"
departureKey = "72d054f6-6680-4584-b7ed-5097956524aa"
station = "Akalla"

# TEST VAVLUES TO BE AUTOMATED
lineColor = lineColorGreen

root = Tk()
root.title("Tube-Time")

# Create root geometry
rootWidth = 800
rootHeight = 200
root.geometry(str(rootWidth) + "x" + str(rootHeight))
root.configure(background=bgcolor)

# Add icon
root.iconbitmap('icon.ico')


def getDepartures():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    stationurl = "https://api.resrobot.se/v2/location.name?"
    paramsStation = dict(
    input = station,
    format = "json",
    key = stationKey
    )

    url = stationurl + urllib.parse.urlencode(paramsStation)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    stationID = js["StopLocation"][0]["id"]
    print(stationID)

    departureurl = "https://api.resrobot.se/v2/departureBoard?"
    paramsDeparture = dict(
    key = departureKey,
    id = stationID,
    maxJourneys = 6,
    products = 32,
    passlist = 0,
    format = "json"
    )

    url = departureurl + urllib.parse.urlencode(paramsDeparture)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    print(json.dumps(js, indent=4))

    global departureDirection1
    global departureDirection2
    global departureDirection3
    departureDirection1 = re.findall("^\S+", js["Departure"][0]["direction"])[0]
    departureDirection2= re.findall("^\S+", js["Departure"][1]["direction"])[0]
    departureDirection3 = re.findall("^\S+", js["Departure"][2]["direction"])[0]
  
    #"""Loop all of this shit, for every departure where the name is the same (single direction)"""
    arrival1_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][0]["time"], "%H:%M:%S").time())
    arrival2_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][1]["time"], "%H:%M:%S").time())
    arrival3_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][2]["time"], "%H:%M:%S").time())

    current_time = datetime.datetime.now()
    waiting1_time = (arrival1_time - current_time)
    waiting2_time = (arrival2_time - current_time)
    waiting3_time = (arrival3_time - current_time)

    global departureTime1
    global departureTime2
    global departureTime3

    departureTime1 = str(int(waiting1_time.total_seconds() / 60.0)) + " " + "min"
    departureTime2 = str(int(waiting2_time.total_seconds() / 60.0)) + " " + "min"
    departureTime3 = str(int(waiting3_time.total_seconds() / 60.0)) + " " + "min"
    if (waiting1_time.total_seconds()/60) < 0: departureTime1 = "Nu"
  
    # Update tkinter labels with fresh departure data, re-run at refresh interval
    primDispLabelStation.configure(text=departureDirection1)
    primDispLabelTime.configure(text=departureTime1)
    secDispLabel.configure(text=departureDirection2 + " " + departureTime2)
    lineColorLabel.configure(bg=lineColors.get(js["Departure"][0]["Product"]["num"]))
    root.after(refInt, getDepartures)
    

# Create line color label
relWidth = 0.94
relHeight = 0.2
lineColorLabel = Label(root, bg=lineColorGreen)
lineColorLabel.place(
    relwidth=relWidth,
    relheight=relHeight,
    relx=((1-relWidth)/2),
    rely=1-relHeight)

# Create frame for departure information labels
dispFrame = Frame(root, bg=dispBgColor)
dispFrame.place(
    relwidth=relWidth,
    relheight=0.7,
    relx=((1-relWidth)/2),
    rely=relHeight/2)

# Makes column 0 of frame expand to take up any free space,
# so that column 1 sticks to east
dispFrame.columnconfigure(0, weight=1)

# Upper leftmost label inside dispFrame
primDispLabelStation = Label(
    dispFrame,
    bg=dispBgColor,
    fg=dispTextColor,
    font=("Helvetica 40 bold"),
    padx=10,
    pady=0,
    text="")

primDispLabelStation.grid(
    row = 0,
    column = 0,
    sticky="nw")

# Upper rightmost label inside dispFrame
primDispLabelTime = Label(
    dispFrame,
    bg=dispBgColor,
    fg=dispTextColor,
    font=("Helvetica 40 bold"),
    padx=10,
    pady=0,
    text="")

primDispLabelTime.grid(
    row=0,
    column=1,
    sticky="ne")

# Bottom label inside dispFrame, spans two columns
secDispLabel = Label(
    dispFrame,
    bg=dispBgColor,
    fg=dispTextColor,
    font=("Helvetica 40 bold"),
    padx=10,
    pady=0,
    text="")

secDispLabel.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="sw")

# Bring up empty main window before calling API first time
root.after(10, getDepartures)

root.mainloop()