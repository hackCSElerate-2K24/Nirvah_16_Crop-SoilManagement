from flask import Flask, request, jsonify
import requests
import joblib


app = Flask(__name__)






OPENWEATHER_API_KEY = '9ffb5287c2a3e7a844c190bbb6c64f1c'  

@app.route('/get-weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location not provided"}), 400

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200:
            return jsonify({"error": "Location not found"}), 404

        result = {
            "location": weather_data.get("name"),
            "temperature": f"{weather_data['main']['temp']}°C",
            "humidity": f"{weather_data['main']['humidity']}%",
            "precipitation": f"{weather_data.get('rain', {}).get('1h', 0)} mm"  
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-crop-recommendation', methods=['GET'])
def get_crop_recommendation():
    return jsonify({"message": "Crop recommendation feature coming soon"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
