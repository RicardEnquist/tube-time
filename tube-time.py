from cProfile import label
import urllib.request, urllib.parse, urllib.error
import json
import re
import requests
import ssl
import datetime
from tkinter import *

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Define colors
bgcolor = "#4F5257"
signBgColor = "#110F04"
signTextColor = "#DED311"
lineColorGreen = "#00A748"
lineColorBlue = "#0095D2"
lineColorRed = "#E40315"

# Defult line color
lineColor = lineColorGreen

root = Tk()
root.title("Tube-Time")

# Create root geometry
rootWidth = 800
rootHeight = 200
root.geometry(str(rootWidth) + "x" + str(rootHeight))
root.configure(background=bgcolor)

# Add icon
#root.iconphoto(True, Tk.photoimage(file='C:/Users/RicardEnquist/Downloads/tube-time/UX/icon.png'))
root.iconbitmap('icon.ico')

# Create line color field
relWidth = 0.94
relHeight = 0.2
lineColorLabel = Label(root, bg=lineColor).place(relwidth=relWidth, relheight=relHeight, relx=((1-relWidth)/2), rely=1-relHeight)


def getDepartures():
    global station
    station = stationInput.get()
    #stationLabel = Label(root, text=stationInput.get())
    #stationLabel.grid(row=4, column=0)

    stationurl = "https://api.resrobot.se/v2/location.name?"
    paramsStation = dict(
    input = station,
    format = "json",
    key = "9ef9290d-c9ae-409c-9862-2b0e5d847b2a"
    )

    url = stationurl + urllib.parse.urlencode(paramsStation)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    js = json.loads(data)
    stationID = js["StopLocation"][0]["id"]
    print(stationID)

    departureurl = "https://api.resrobot.se/v2/departureBoard?"
    paramsDeparture = dict(
    key = "72d054f6-6680-4584-b7ed-5097956524aa",
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

    arrival1_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][0]["time"], "%H:%M:%S").time())
    arrival2_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][1]["time"], "%H:%M:%S").time())
    arrival3_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(js["Departure"][2]["time"], "%H:%M:%S").time())

    current_time = datetime.datetime.now()
    waiting1_time = (arrival1_time - current_time)
    waiting2_time = (arrival2_time - current_time)
    waiting3_time = (arrival3_time - current_time)
    waiting1_min = waiting1_time.total_seconds() / 60.0
    waiting2_min = waiting2_time.total_seconds() / 60.0
    waiting3_min = waiting3_time.total_seconds() / 60.0

    if waiting1_min < 0:
        departure1 = re.findall("^\S+", js["Departure"][0]["direction"])[0] + " " + "Nu"
        departure2 = re.findall("^\S+", js["Departure"][1]["direction"])[0] + " " + str(int(waiting2_min)) + " min"
        departure3 = re.findall("^\S+", js["Departure"][1]["direction"])[0] + " " + str(int(waiting3_min)) + " min"
    else:
        departure1 = re.findall("^\S+", js["Departure"][0]["direction"])[0] + " " + str(int(waiting1_min)) + " min"
        departure2 = re.findall("^\S+", js["Departure"][1]["direction"])[0] + " " + str(int(waiting2_min)) + " min"
        departure3 = re.findall("^\S+", js["Departure"][1]["direction"])[0] + " " + str(int(waiting3_min)) + " min"

    departure1Label.config(text=departure1)
    departure2Label.config(text=departure2)
    departure3Label.config(text=departure3)

# departure1Label = Label(root)
# departure1Label.grid(row=4, column=0)
# departure2Label = Label(root)
# departure2Label.grid(row=5, column=0)
# departure3Label = Label(root)
# departure3Label.grid(row=6, column=0)

# stationInput = Entry(root, width=50)
# stationInput.grid(row=0, column=0)
# runButton = Button(root, text="Get station", command=getDepartures)
# runButton.grid(row=1, column=0)

root.mainloop()