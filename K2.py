# -*- coding: utf-8 -*-
import requests #for fetching data via HTTP
import matplotlib.pyplot as plt #for plotting
import time #for time related functions

def get_weather(datastr):
    url = "http://api.openweathermap.org/data/2.5/weather"
    r = requests.get(url, params=datastr)
    return r.json()

def get_forecast(datastr):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    r = requests.get(url, params=datastr)
    return r.json()

def plot_forecast(forecast):
    x=[forecast['list'][i]['dt_txt'] for i in range(40)] #x axis get time data
    y1=[forecast['list'][i]['main']['temp'] for i in range(40)] #y1 axis get temperature data
    y2=[forecast['list'][i]['wind']['speed'] for i in range(40)] #y2 axis get wind speed data
    
    fig, ax1 = plt.subplots(figsize=(15,5))
    ax2=ax1.twinx() #include two Y axis on single plot and single X axis
    ax1.plot(x,y1, 'bo-') #plot temperature in blue
    ax2.plot(x,y2, 'y-') #plot wind speed in yellow
    ax1.set_ylabel("Temperature [°C]", color='b') #setting the temperature label
    ax2.set_ylabel("Wind speed [m/s]", color='y') #setting the wind label
    ax1.grid(axis="both") #display grid on plot
    ax1.set_xticklabels(x, rotation=90) #rotate the time labels for visibility
    plt.title("5-day weather forecast for "+forecast['city']['name']) #setting the plot label, uses fetched data to display city name
    plt.pause(0.0001)  #fix for not plotting while in loop
    print("\n") #endline after plot
    
def display_weather(weather):
    print("Current weather:")
    print("Conditions:",weather['weather'][0]['description'])
    print("Temperature:",weather['main']['temp'],"°C")
    print("Humidity:",weather['main']['humidity'],"%")
    print("Pressure:",weather['main']['pressure'],"hPa")
    print("Wind speed:",weather['wind']['speed'],"m/s")
    print("Wind direction:",weather['wind']['deg'],"°")
    print("\n") #endline after displaying data

k2 = {"lat": "35.88", "lon": "76.51"} #define coordinates
key = {"APPID": "8aadfa69e450f31dad65406b2ba9eb34"} #define OpenWeather API key
unit = {"units": "metric"} #define units, default=metric
datastr = {**k2, **key, **unit} #create data string for url request
sleep_time = 5 #time

while True:
    weather = get_weather(datastr) #fetch weather data
    forecast = get_forecast(datastr) #fetch forecast data
    
    if weather['cod'] in [200]: #chceck if wheather was correctly updated
        display_weather(weather)
    elif weather['cod'] in [429]: #chceck if wheather has hit refresh limit
        print("Error: Too many inquiries (weather).")
    else: #if any other error occured while fetching weather data
       print("An error occured while fetching weather.")
    
    if forecast['cod'] in ['200']: #chceck if forecast was correctly updated
        plot_forecast(forecast)
    elif forecast['cod'] in ['429']: #chceck if wheather has hit refresh limit
        print("Error: Too many inquiries (forecast).")
    else: #if any other error occured while fetching forecast data
        print("An error occured while fetching forecast.")
    
    time.sleep(sleep_time) #wait for a defined amount of seconds
    