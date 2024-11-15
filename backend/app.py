import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import joblib
from datetime import datetime, timedelta

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS with options for more control
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# Load your pretrained model here (example with a saved model)
model = tf.keras.models.load_model("C:\\Users\\pavan\\Desktop\\crop-soil-management\\backend\\pest_disease_detection_model.h5")
crop_model = joblib.load('crop_recommendation_model_gb.pkl')

# Your new rainfall data API key (or other relevant API URL)
RAINFALL_API_KEY = 'efcf0df483114e57a314d1d0ed4368fa' 
OPENWEATHER_API_KEY='9ffb5287c2a3e7a844c190bbb6c64f1c' # Replace with the actual key or URL

def get_monthly_precipitation(location):
    """Fetch precipitation data using Weatherbit API and convert it to mm/year."""
    try:
        # Requesting daily forecast for 30 days from Weatherbit API
        weatherbit_url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={RAINFALL_API_KEY}&days=30"
        response = requests.get(weatherbit_url)
        data = response.json()

        # Log the raw response for debugging
        logging.debug(f"Raw response from Weatherbit API: {data}")

        if response.status_code != 200:
            logging.error(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
            return None

        # Initialize total monthly precipitation
        monthly_precipitation = 0

        # Iterate through daily data and sum the daily rainfall (precip)
        for day in data.get('data', []):
            logging.debug(f"Day data: {day}")
            
            # Assuming 'precip' field contains the daily precipitation in mm
            daily_rain = day.get('precip', 0)
            monthly_precipitation += daily_rain  # Sum daily rainfall

        # Log the calculated total monthly precipitation (in mm)
        logging.debug(f"Calculated total monthly precipitation: {monthly_precipitation} mm")
        
        # Convert monthly precipitation to annual (mm/year) assuming same rainfall each month
        if monthly_precipitation<4:
            annual_precipitation = monthly_precipitation * 50

        else:
            annual_precipitation=monthly_precipitation*10     
        logging.debug(f"Calculated annual precipitation: {annual_precipitation} mm/year")

        # Ensure the annual value looks correct
        if annual_precipitation == 0:
            logging.error("No valid daily precipitation data found.")
            return None
        
        return annual_precipitation

    except Exception as e:
        logging.error(f"Error fetching precipitation data: {str(e)}")
        return None


@app.route('/get-weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location not provided"}), 400

    try:
        
        monthly_precipitation = get_monthly_precipitation(location)

        if monthly_precipitation is None:
            return jsonify({"error": "Unable to fetch precipitation data"}), 404

        
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code != 200:
            return jsonify({"error": "Location not found"}), 404

        result = {
            "location": weather_data.get("name"),
            "temperature": f"{weather_data['main']['temp']}°C",
            "humidity": f"{weather_data['main']['humidity']}%",
            "precipitation": f"{monthly_precipitation} mm"  
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/get-crop-recommendation', methods=['GET'])
def get_crop_recommendation():
    location = request.args.get('location')
    N = request.args.get('N', type=int)
    P = request.args.get('P', type=int)
    K = request.args.get('K', type=int)
    ph = request.args.get('ph', type=float)

    if not location or N is None or P is None or K is None or ph is None:
        return jsonify({"error": "Location and soil data (N, P, K, pH) are required"}), 400

    try:
        
        monthly_precipitation = get_monthly_precipitation(location)

        if monthly_precipitation is None:
            return jsonify({"error": "Unable to fetch precipitation data"}), 404

        
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        
        input_data = [[N, P, K, temperature, humidity, ph, monthly_precipitation]]
        predicted_crop = crop_model.predict(input_data)[0]

        return jsonify({
            "location": weather_data.get("name"),
            "temperature": f"{temperature}°C",
            "humidity": f"{humidity}%",
            "rainfall": f"{monthly_precipitation} mm",
            "recommended_crop": predicted_crop
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
