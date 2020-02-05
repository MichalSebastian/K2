# -*- coding: utf-8 -*-
import requests #for fetching data via HTTP
import matplotlib.pyplot as plt #for plotting
from datetime import datetime #for time related functions
import sqlite3 #use SQLite
from sqlite3 import Error

def get_weather(datastr):
    url = "http://api.openweathermap.org/data/2.5/weather"
    r = requests.get(url, params=datastr)
    return r.json()

def get_forecast(datastr):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    r = requests.get(url, params=datastr)
    return r.json()

def plot_forecast(forecast):
    plt.close("all") #closes all active plots
    x=[forecast['list'][i]['dt_txt'] for i in range(40)] #x axis get time data
    x2=[forecast['list'][i]['weather'][0]['description'] for i in range(40)] #x2 axis labels to get weather description
    y1=[forecast['list'][i]['main']['temp'] for i in range(40)] #y1 axis get temperature data
    y2=[forecast['list'][i]['wind']['speed'] for i in range(40)] #y2 axis get wind speed data
    y3=[forecast['list'][i]['main']['humidity'] for i in range(40)] #y3 axis get humidity data
    y4=[forecast['list'][i]['main']['pressure'] for i in range(40)] #y4 axis get pressure data
    fig, ax1 = plt.subplots(figsize=(15,5)) #defining the plot size
    ax2=ax1.twinx() #include two Y axis on single plot and single X axis
    ax1.plot(x,y1, 'bo-') #plot temperature in blue
    ax2.plot(x,y2, 'y-') #plot wind speed in yellow
    ax1.set_ylabel("Temperature [°C]", color='b') #setting the temperature label
    ax2.set_ylabel("Wind speed [m/s]", color='y') #setting the wind label
    ax1.grid(axis="both") #display grid on plot
    ax1.set_xticklabels(x, rotation=90) #rotate the time labels for visibility
    plt.title("5-day weather forecast for "+forecast['city']['name']) #setting the plot label, uses fetched data to display city name
    fig2, ax3 = plt.subplots(figsize=(15,5)) #create second figure
    ax4=ax3.twinx() #include two Y axis on single plot and single X axis
    ax3.bar(x,y3) #bar chart for humidity
    ax4.plot(x,y4, 'ro-') #plot pressure
    plt.xticks(x,x+x2) #display description of weather conditions on xticks (instead of date/time)
    ax3.set_xlabel("Weather conditions") #setting the weather conditions label
    ax3.grid(axis="y") #display horizontal lines on second plot
    ax3.set_xticklabels(x2, rotation=90) #rotate the xtick labels labels for visibility
    ax3.set_ylabel("Humidity [%]", color='b') #setting the humidity label
    ax4.set_ylabel("Atmospheric pressure [mPa]", color='r') #setting the pressure label
    plt.draw() #make sure to draw the plots
    print("\n") #endline after plot
    
    
def display_weather(weather): #display current weather data
    print("Current weather:")
    print("Conditions:",weather['weather'][0]['description'])
    print("Temperature:",weather['main']['temp'],"°C")
    print("Humidity:",weather['main']['humidity'],"%")
    print("Pressure:",weather['main']['pressure'],"hPa")
    print("Wind speed:",weather['wind']['speed'],"m/s")
    print("Wind direction:",weather['wind']['deg'],"°")
    print("\n") #endline after displaying data

def print_db(wheatherdb): #display avg, min, max temperature from database
    c = wheatherdb.cursor()
    c.execute("SELECT AVG(temperature) FROM data")
    temps=c.fetchall()
    print('Average temperature: ',temps)
    c.execute("SELECT MIN(temperature) FROM data")
    temps=c.fetchall()
    print('Lowest temperature: ',temps)
    c.execute("SELECT MAX(temperature) FROM data")
    temps=c.fetchall()
    print('Highest temperature: ',temps)

def create_connection():
    wheatherdb = None 
    try:
        wheatherdb = sqlite3.connect(r".\weather_file.db") #create a database on disk (current folder)
    except Error as e:
        print(e) #print error if error occurs
    if wheatherdb is not None:
        try:
            c = wheatherdb.cursor()
            c.execute(""" CREATE TABLE IF NOT EXISTS data (update_time text PRIMARY KEY, temperature int, pressure int, humidity int, wind_speed int, wind_direction int, clouds int, conditions text); """) #create a table to store weather data
        except Error as e:
            print(e) #print error if error occurs
    else:
        print("Error! cannot create the database connection.")    
    return wheatherdb #return the connection object

def write_to_db(wheatherdb, weather):
    updt_tme=datetime.now() #update current time
    updt_tme=updt_tme.strftime("%d/%m/%Y, %H:%M:%S") #change the date/time format
    row=( #create row of data to store in database
        updt_tme, #stores timestamp as primary key for db table
        weather['main']['temp'],
        weather['main']['pressure'],
        weather['main']['humidity'], 
        weather['wind']['speed'], 
        weather['wind']['deg'],
        weather['clouds']['all'],
        weather['weather'][0]['description'])
    c = wheatherdb.cursor()
    c.execute("insert into data values (?,?,?,?,?,?,?,?)", row) #store data in database
    wheatherdb.commit() #commit the data do database

def main():
    k2 = {"lat": "35.88", "lon": "76.51"} #define coordinates
    key = {"APPID": "8aadfa69e450f31dad65406b2ba9eb34"} #define OpenWeather API key
    unit = {"units": "metric"} #define units, default=metric
    datastr = {**k2, **key, **unit} #create data string for url request
    sleep_time = 3 #time in seconds 
    while True:
        wheatherdb=create_connection() #create database connection
        weather = get_weather(datastr) #fetch weather data
        forecast = get_forecast(datastr) #fetch forecast data
        if weather['cod'] in [200]: #chceck if wheather was correctly updated
            print("Data updating every ", sleep_time, " seconds.", "\n")
            display_weather(weather) #print actual weather data
            write_to_db(wheatherdb,weather) #save actual data to database
            print_db(wheatherdb) #print avg,min,max values from database
        elif weather['cod'] in [429]: #chceck if wheather has hit refresh limit
            print("Error: Too many inquiries (weather).")
        else: #if any other error occured while fetching weather data
           print("An error occured while fetching weather.")
        
        if forecast['cod'] in ['200']: #chceck if forecast was correctly updated
            plot_forecast(forecast) #plot forecast figures
        elif forecast['cod'] in ['429']: #chceck if wheather has hit refresh limit
            print("Error: Too many inquiries (forecast).")
        else: #if any other error occured while fetching forecast data
            print("An error occured while fetching forecast.")
        wheatherdb.close() #close database connection
        plt.pause(sleep_time)  #wait for a defined amount of seconds + fix for not plotting while in loop while using time.sleep()
        
if __name__== "__main__":
  main()
   