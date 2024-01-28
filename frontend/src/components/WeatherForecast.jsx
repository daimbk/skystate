import { useState } from "react";

const WeatherComponent = () => {
  const [city, setCity] = useState("");
  const [weatherData, setWeatherData] = useState(null);
  const [weeklyForecast, setWeeklyForecast] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch(`http://localhost:8000/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          city1: city,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const data = await response.json();
      setWeatherData(data.weather_data1);
      setWeeklyForecast(data.weekly_forecast1);
      setError(null);
    } catch (error) {
      setWeatherData(null);
      setWeeklyForecast(null);
      setError("Error fetching data");
    }
  };

  return (
    <div>
      <style>
        {`
          form {
            display: flex;
            flex-direction: column;
            align-items: center;
          }

          input {
            text-align: center;
            padding: 10px 0px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 22px;
            font-size: large;
          }

          button {
            padding: 10px 30px;
            background-color: #691a0c;
            color: #f5d7db;
            border: 1px solid #ccc;
            border-radius: 22px;
            cursor: pointer;
            font-size: large;
            transition: 0.5s ease;
          }

          button:hover {
            background-color: #b82c14;
            color: #ccc;
            transition: 0.5s ease;
          }

          .error {
            color: black;
            margin-top: 15px;
          }

          .city-container {
            margin-top: 3rem;
          }

          .temp {
            font-size: 50px;
          }

          img {
            width: 80px;
            height: auto;
          }

          .uppercase-words::first-line {
            text-transform: uppercase;
          }
        `}
      </style>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!city) {
            setError("Please enter a city.");
            return;
          }
          fetchData();
        }}
      >
        <input
          type="text"
          placeholder="Enter City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button type="submit">Get Weather</button>
      </form>

      {error && <p className="error">{error}</p>}

      {weatherData && (
        <div className="city-container">
          <h2 className="uppercase-words">{weatherData.city}</h2>
          <h1 className="temp">{weatherData.temperature}°C</h1>
          <h3>Feels Like: {weatherData.feels_like}°C</h3>
          <h3>Humidity: {weatherData.humidity}%</h3>
          <p className="uppercase-words">{weatherData.description}</p>
          <img
            src={`http://openweathermap.org/img/w/${weatherData.icon}.png`}
            alt={weatherData.description}
          />

          <div className="forecast-container">
            {weeklyForecast.map((forecast, index) => (
              <div key={index} className="forecast">
                <h3>{forecast.day}</h3>
                <p>{forecast.temperature}°C</p>
                <p>Humidity: {forecast.humidity}%</p>
                <p className="uppercase-words">{forecast.description}</p>
                <img
                  src={`http://openweathermap.org/img/w/${forecast.icon}.png`}
                  alt={forecast.description}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WeatherComponent;
