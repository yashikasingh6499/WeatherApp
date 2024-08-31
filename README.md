## Weatherth: A Streamlit Weather App

**Description**

Weatherth is a weather application built using Streamlit. It fetches real-time weather data from the OpenWeatherMap API and provides a 5-day weather forecast. The app also includes geolocation features to automatically detect the user's location or allows manual city input for weather data. The app also displays the weather data and location on an interactive map.

**Features**

Automatic Location Detection: Detects your current location using your IP address and fetches weather data accordingly.   

Manual Location Entry: Allows users to input a city name to retrieve weather information.  

Current Weather Details: Displays current temperature, min temperature, max temperature, sunrise time, sunset time, humidity, pressure, and weather conditions.  

5-Day Weather Forecast: Provides a 5-day forecast with temperatures and conditions for each day.  

Interactive Map: Shows your location or the entered city on a map.  

**Installation**

*Clone the Repository*

git clone https://github.com/yourusername/weatherth.git  
cd weatherth

*Install Required Packages*

Create a virtual environment and install the necessary Python packages:

python -m venv venv  
source venv/bin/activate  # On Windows use `venv\Scripts\activate`  
pip install -r requirements.txt  

*Run the Application*

streamlit run weatherth.py

This command will open the app in your default web browser.

**How It Works**

Geolocation Handling: When the "Use current location" checkbox is selected, the app attempts to detect your location using IP-based geolocation. If successful, it displays your city, region, and country, and retrieves weather data for your coordinates.

Manual City Entry: If you prefer to enter a city manually, simply type the city name and click the "How's the weather?" button to fetch weather data.

Map Display: The app shows your detected or manually entered location on a map using st.map().

**API and Token Setup**

The app uses the OpenWeatherMap API to retrieve weather data. Replace the placeholder API key in the script with your own API key.
The IP geolocation is handled using the IPinfo service. You can replace the provided token with your own.

**Contact**

For any questions or feedback, please contact Yashika Singh.
