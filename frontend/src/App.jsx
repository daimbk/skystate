import "./App.css";
import WeatherComponent from "./components/WeatherForecast";
import Blob from "./components/Blob";

function App() {
  return (
    <div>
      <h1 className="title">Welcome to SkyState</h1>
      <WeatherComponent />
      <Blob />
    </div>
  );
}

export default App;
