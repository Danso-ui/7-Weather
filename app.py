# TODO - IMPORTING THE NEEDED LIBRARIES
import os
import requests
from pprint import pprint
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

key = os.getenv("OPENWEATHER_API_KEY")


# TODO - CITY AND API KEY
city = "Kumasi"

# TODO - GETTING LONGITUDE AND LATITUDE FOR THE ACTUAL DATA
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
response = requests.get(url)
data = response.json()
longitude = data["coord"]["lon"]
latitude = data["coord"]["lat"]

# TODO - THE ACTUAL DATA
url2 = "https://api.openweathermap.org/data/3.0/onecall"
params = {
    "lat" : latitude,
    "lon" : longitude,
    "appid" : key,
    "units": "metric"
}
response = requests.get(url2, params=params)
data2 = response.json()
# print(data2)

# TODO - GETTING THE TEMPERATURE, HUMIDITY, WIND SPEED, CONDITION, AND ICON
current_icon_code = data2['current']['weather'][0]['icon']

current_weather = {
    "temp": data2['current']['temp'], # ->℃
    "humidity": data2['current']['humidity'], # -> %
    "wind_speed": data2['current']['wind_speed'], # -> m/s
    "description": data2['current']['weather'][0]['description'],
    "icon_url": f"https://openweathermap.org/img/wn/{current_icon_code}@2x.png",
    "pressure": data2['current']['pressure'],
    "feels_like": data2['current']['feels_like'],
    "timezone": data2['timezone'].split("/")[1].replace("_", " "),
    "day": dt.fromtimestamp(data2['current']['dt']).strftime("%A, %b %d %Y"),
    "time": dt.fromtimestamp(data2['current']['dt']).strftime("%I:%M %p")
}
# pprint(current_weather)

# TODO - THE NEXT 5 DAYS DATA
forecast = []

for i in range(1, 7):
    daily_icon_code = data2['daily'][i]['weather'][0]['icon']

    day_data = {
        "temp": data2['daily'][i]['temp']['day'], # -> ℃
        "humidity": data2['daily'][i]['humidity'], # -> %
        "wind_speed": data2['daily'][i]['wind_speed'], # -> m/s
        "description": data2['daily'][i]['weather'][0]['description'],
        "icon_url": f"https://openweathermap.org/img/wn/{daily_icon_code}@2x.png",
        "day": dt.fromtimestamp(data2['daily'][i]['dt']).strftime("%A, %b %d %Y")
    }
    forecast.append(day_data)
pprint(forecast)