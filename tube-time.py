import urllib.request, urllib.parse, urllib.error
import json
import re
import requests
import ssl
import datetime

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# serviceurl = "https://api.resrobot.se/v2/departureBoard?"
# params = dict(
#     key = "72d054f6-6680-4584-b7ed-5097956524aa",
#     id = "740021668",
#     maxJourneys = 6,
#     products = 32,
#     passlist = 0,
#     format = "json"
#     )

serviceurl = "https://api.resrobot.se/v2/location.name?"
place = input("Hållplats: ")
params = dict(
    input = place,
    format = "json",
    key = "9ef9290d-c9ae-409c-9862-2b0e5d847b2a"
    )



url = serviceurl + urllib.parse.urlencode(params)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
js = json.loads(data)

print(json.dumps(js, indent=4))

for dep in range(len(js["Departure"])):
    break
    #if js["Departure"][0]
    #print("avgångar")


#print(re.findall("^\S+", js["Departure"][0]["direction"])[0] + ": " + js["Departure"][0]["time"])

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
    print(re.findall("^\S+", js["Departure"][0]["direction"])[0], "Nu", " ", end='')
    print(re.findall("^\S+", js["Departure"][1]["direction"])[0], int(waiting2_min), "min", " ", end='')
    print(re.findall("^\S+", js["Departure"][2]["direction"])[0], int(waiting3_min), "min")
else:
    print(re.findall("^\S+", js["Departure"][0]["direction"])[0], int(waiting1_min), "min", " ", end='')
    print(re.findall("^\S+", js["Departure"][1]["direction"])[0], int(waiting2_min), "min", " ", end='')
    print(re.findall("^\S+", js["Departure"][2]["direction"])[0], int(waiting3_min), "min")
