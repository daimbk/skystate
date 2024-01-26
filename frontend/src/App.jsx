import "./App.css";
import WeatherComponent from "./components/WeatherForecast";

function App() {
  return (
    <div>
      <h1 className="title">Welcome to SkyState</h1>
      <WeatherComponent />
    </div>
  );
}

export default App;
