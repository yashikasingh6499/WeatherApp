import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API key and base URL setup
api_key = os.getenv("API_KEY")
weather_url = "http://api.openweathermap.org/data/2.5/weather"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
ipinfo_token = os.getenv("IPINFO_TOKEN") #Obtained after registering on ipinfo.io site

# App title and description
st.title("Weatherth")
st.write("""
# Hi! Welcome to Weatherth.
Please enter your location to know if there's any need of umbrella today or not.
""")

# Adding name
st.sidebar.title("About the Developer")
st.sidebar.write("This weather app was developed by Yashika Singh.")

# Info button for PM Accelerator description
if st.sidebar.button("Info about PM Accelerator"):
    st.sidebar.info("""
    *PM Accelerator* Program is designed to support PM professionals through every stage of their career.
    From students looking for entry-level jobs to Directors looking to take on a leadership role, our program has helped over hundreds of students fulfill their career aspirations.
    Our Product Manager Accelerator community are ambitious and committed.
    Through our program they have learnt, honed and developed new PM and leadership skills, giving them a strong foundation for their future endeavours.
    """)

# Using current location
use_location = st.checkbox("Use current location")

# Initialize variables
lat, lon = None, None

# Geolocation handling with IP-based location detection
if use_location:
    try:
        ip_info = requests.get(f"https://ipinfo.io/json?token={ipinfo_token}").json()
        loc = ip_info['loc'].split(',')
        lat, lon = float(loc[0]), float(loc[1])
        city = ip_info['city']
        region = ip_info['region']
        country = ip_info['country']
        st.success(f"Detected location: {city}, {region}, {country}")
        url = f"{weather_url}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    except Exception as e:
        st.error("Failed to detect location. Please enter manually.")
else:
    city = st.text_input("City Name", "")
    if city:
        url = f"{weather_url}?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            coord = data['coord']
            lat = coord['lat']
            lon = coord['lon']
        else:
            st.error("City Not Found or API request failed.")

# Button to fetch weather data
if st.button("How's the weather?"):
    if (use_location and lat and lon) or city:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            sys = data['sys']
            weather = data['weather'][0]

            # Extracting weather details
            temperature = main['temp']
            temp_min = main['temp_min']
            temp_max = main['temp_max']
            humidity = main['humidity']
            pressure = main['pressure']
            weather_description = weather['description']
            icon = weather['icon']

            # Extracting sunrise and sunset times
            sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M:%S')

            # Displaying the weather details
            st.subheader(f"Current Weather in {city if use_location else city.capitalize()}:")
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")
            st.write(f"*Temperature:* {temperature}°C")
            st.write(f"*Min Temperature:* {temp_min}°C")
            st.write(f"*Max Temperature:* {temp_max}°C")
            st.write(f"*Humidity:* {humidity}%")
            st.write(f"*Pressure:* {pressure} hPa")
            st.write(f"*Condition:* {weather_description.capitalize()}")
            st.write(f"*Sunrise:* {sunrise}")
            st.write(f"*Sunset:* {sunset}")

            # Displaying the map 
            if lat and lon:
                st.subheader("Location on Map:")
                map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                st.map(map_data)

            # Fetching and displaying the 5-day forecast
            if use_location:
                forecast_response = requests.get(f"{forecast_url}?lat={lat}&lon={lon}&appid={api_key}&units=metric")
            else:
                forecast_response = requests.get(f"{forecast_url}?q={city}&appid={api_key}&units=metric")

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                st.subheader("5-Day Forecast:")
                forecast_list = forecast_data['list']
                for i in range(0, 40, 8):  # Forecast data is provided every 3 hours, so 8 entries per day
                    forecast = forecast_list[i]
                    date = datetime.fromtimestamp(forecast['dt']).strftime('%A, %d %B')
                    temp = forecast['main']['temp']
                    icon = forecast['weather'][0]['icon']
                    description = forecast['weather'][0]['description']

                    st.write(f"*{date}*")
                    st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")
                    st.write(f"*Temperature:* {temp}°C")
                    st.write(f"*Condition:* {description.capitalize()}")
            else:
                st.error("Failed to retrieve forecast data.")
        else:
            st.error("City Not Found or API request failed.")
    else:
        st.warning("Please enter your city name or use your current location.")
