import React, { useState } from "react";
import axios from "axios";
import './WeatherAndCrop.css';

function WeatherAndCrop() {
  const [location, setLocation] = useState("");
  const [N, setN] = useState("");
  const [P, setP] = useState("");
  const [K, setK] = useState("");
  const [ph, setPh] = useState("");
  const [weather, setWeather] = useState(null);
  const [cropRecommendation, setCropRecommendation] = useState(null);
  const [error, setError] = useState(null);

  const apiUrl = "http://127.0.0.1:5000"; // Local Flask API URL

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setWeather(null);
    setCropRecommendation(null);
    try {
      // Fetch weather data
      const weatherResponse = await axios.get(`${apiUrl}/get-weather?location=${location}`);
      setWeather(weatherResponse.data);

      // Fetch crop recommendation data, including the soil parameters (N, P, K, pH)
      const cropResponse = await axios.get(`${apiUrl}/get-crop-recommendation`, {
        params: {
          location,
          N: parseInt(N),
          P: parseInt(P),
          K: parseInt(K),
          ph: parseFloat(ph),
        }
      });
      if (cropResponse.data.recommended_crop) {
        setCropRecommendation(cropResponse.data.recommended_crop);
      } else {
        setError("Could not retrieve crop recommendations.");
      }
    } catch (err) {
      setError("Oops! Something went wrong. Please make sure your data is correct and try again.");
      setWeather(null);
      setCropRecommendation(null);
    }
  };

  return (
    <div className="weather-crop-container">
      <div className="card animate__animated animate__fadeInUp">
        <h2>Get Weather & Crop Recommendations</h2>
        <p>Provide your location and some details about the soil to get personalized weather and crop suggestions.</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter your location"
            className="large-input"
          />
          <p>Enter soil condition:</p>
          <div className="grid grid-cols-2 gap-6">
            <input
              type="number"
              value={N}
              onChange={(e) => setN(e.target.value)}
              placeholder="N"
              className="small-input"
            />
            <input
              type="number"
              value={P}
              onChange={(e) => setP(e.target.value)}
              placeholder="P"
              className="small-input"
            />
            <input
              type="number"
              value={K}
              onChange={(e) => setK(e.target.value)}
              placeholder="K"
              className="small-input"
            />
            <input
              type="number"
              value={ph}
              onChange={(e) => setPh(e.target.value)}
              placeholder="pH"
              className="small-input"
            />
          </div>
          <button type="submit">Get Recommendations</button>
        </form>

        {weather && (
          <div className="weather-card animate__animated animate__fadeInUp">
            <h3>Weather Info</h3>
            <p><strong>Temperature:</strong> {weather.temperature}</p>
            <p><strong>Humidity:</strong> {weather.humidity}</p>
            <p><strong>Precipitation:</strong> {weather.precipitation}</p>
          </div>
        )}

        {cropRecommendation && (
          <div className="crop-card animate__animated animate__fadeInUp">
            <h3>Recommended Crop</h3>
            <p>{cropRecommendation}</p>
          </div>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

export default WeatherAndCrop;
