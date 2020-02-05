# K2
K2 is a simple script designed to fetch live weather data (and weather forecast) from OpenWeatherMap.

## Requirements
Use the package manager pip to install required libraries:
```bash
$ pip install -r requirements.txt
```
Written for Python 3.7.

An internet connection is required to fetch the data.

## Usage
Just run the K2.py file.

K2 is preconfigured to display live weather as well as 5-day forecast for K2 summit.
Once run, the script will display live data and store it in a local database file.
Below the live weather, there will be displayed the average temperature from the database, as well as min and max temperature recorded.
At last, the 5-day forecast plot is displayed. The forecast has a resolution of three hours.

The script will automatically refresh every 3 seconds, fetching new data.

The script will loop indefinitely, to stop it use KeboardInterrupt (CTRL + C).

Please note, the database file will not be deleted after closing the script, and if the file exists while launching the script again, new data will be added at the end of the file.

## Customization
If you wish to fetch data for a different geographical location, simply change the coordinates in the "k2" variable:
```python
k2 = {"lat": "35.88", "lon": "76.51"}
```

To change the refresh rate, change the value of "sleep_time" variable:
```python
sleep_time = 3 #time in seconds 
```
