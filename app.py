import os
import requests as r
from dotenv import load_dotenv
from datetime import datetime as dt
from flask import Flask, render_template, request

load_dotenv()

key = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    # 1. Initialize as None/Empty so the page loads cleanly on a GET request
    current_weather = None
    forecast = []

    if request.method == "POST":
        # Capture form data (might be city, might be lat/lon)
        city = request.form.get("city")
        lat = request.form.get("lat")
        lon = request.form.get("lon")

        # Set these up to be filled in by one of the scenarios below
        latitude = None
        longitude = None

        # --- SCENARIO A: The user used the search bar ---
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
            response = r.get(url)

            # Only proceed if the API actually found the city (Status 200)
            if response.status_code == 200:
                data = response.json()
                longitude = data["coord"]["lon"]
                latitude = data["coord"]["lat"]

        # --- SCENARIO B: The user clicked "Use my current location" ---
        elif lat and lon:
            latitude = lat
            longitude = lon

        # --- FINAL STEP: If we successfully got coordinates from either A or B ---
        if latitude and longitude:

            # Fetch OneCall Data
            url2 = "https://api.openweathermap.org/data/3.0/onecall"
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": key,
                "units": "metric"
            }
            response2 = r.get(url2, params=params)
            data2 = response2.json()

            # Build current_weather dictionary
            current_icon_code = data2['current']['weather'][0]['icon']

            current_weather = {
                "temp": data2['current']['temp'],  # ->℃
                "humidity": data2['current']['humidity'],  # -> %
                "wind_speed": data2['current']['wind_speed'],  # -> m/s
                "description": data2['current']['weather'][0]['description'],
                "icon_url": f"https://openweathermap.org/img/wn/{current_icon_code}@2x.png",
                "pressure": data2['current']['pressure'],
                "feels_like": data2['current']['feels_like'],
                "timezone": data2['timezone'].split("/")[1].replace("_", " "),
                "day": dt.fromtimestamp(data2['current']['dt']).strftime("%A, %b %d %Y"),
                "time": dt.fromtimestamp(data2['current']['dt']).strftime("%I:%M %p")
            }

            # Build forecast list (0 to 7 = Today + 6 future days)
            for i in range(1, 7):
                daily_icon_code = data2['daily'][i]['weather'][0]['icon']

                day_data = {
                    "temp": data2['daily'][i]['temp']['day'],  # -> ℃
                    "humidity": data2['daily'][i]['humidity'],  # -> %
                    "wind_speed": data2['daily'][i]['wind_speed'],  # -> m/s
                    "description": data2['daily'][i]['weather'][0]['description'],
                    "icon_url": f"https://openweathermap.org/img/wn/{daily_icon_code}@2x.png",
                    "day": dt.fromtimestamp(data2['daily'][i]['dt']).strftime("%A, %b %d %Y")
                }
                forecast.append(day_data)

    # Render the HTML page, passing the data along!
    return render_template("index.html", current_weather=current_weather, forecast=forecast)


if __name__ == "__main__":
    app.run(debug=True)