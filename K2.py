# -*- coding: utf-8 -*-
import requests


def get_weather(datastr):
    url = "http://api.openweathermap.org/data/2.5/weather"
    r = requests.get(url, params=datastr)
    return r.json()
 

k2 = {"lat": "35.88", "lon": "76.51"}
key = {"APPID": "8aadfa69e450f31dad65406b2ba9eb34"}
unit = {"unit": "metric"}
datastr = {**k2, **key, **unit}

weather = get_weather(datastr)

if weather['cod'] in [200]:
    print(weather)
elif weather['cod'] in [429]:
    print("Error: Too many inquiries.")
else:
    print("An error occured.")

        
 


