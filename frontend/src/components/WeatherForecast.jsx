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
      <form
        onSubmit={(e) => {
          e.preventDefault();
          fetchData();
        }}
      >
        <input
          type="text"
          placeholder="Enter city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button type="submit">Get Weather</button>
      </form>

      {error && <p className="error">{error}</p>}

      {weatherData && (
        <div className="city-container">
          <h1>{weatherData.city}</h1>
          <h2>{weatherData.temperature}°C</h2>
          <p>{weatherData.description}</p>
          <img
            src={`http://openweathermap.org/img/w/${weatherData.icon}.png`}
            alt={weatherData.description}
          />

          <div className="forecast-container">
            {weeklyForecast.map((forecast, index) => (
              <div key={index} className="forecast">
                <h3>{forecast.day}</h3>
                <p>
                  {forecast.min_temp}°C - {forecast.max_temp}°C
                </p>
                <p>{forecast.description}</p>
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
