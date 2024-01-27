import datetime
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    API_KEY = "3e0b73d2dc8224f74cc952419a96a60a"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1', None)

        weather_data1, weekly_forecast1 = fetch_weather_and_forecast(
            city1, API_KEY, current_weather_url, forecast_url)

        response_data = {
            'weather_data1': weather_data1,
            'weekly_forecast1': weekly_forecast1,
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({})

@csrf_exempt
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    #print("Forecast URL:", forecast_url.format(lat, lon, api_key))

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 0),
        'feels like': round(response['main']['feels_like'] - 273.15, 0),
        'humidity': response['main']['humidity'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    #print("Weather Data:", weather_data)

    weekly_forecast = []
    processed_dates = set()
    today = datetime.datetime.utcnow().date()

    # Iterate through the list of forecasts
    for forecast_data in forecast_response.get('list', []):
        timestamp = forecast_data.get('dt', 0)
        forecast_date = datetime.datetime.utcfromtimestamp(timestamp).date()

        # Skip the current day's forecast
        if forecast_date == today:
            continue

        # Skip if the date has already been processed
        if forecast_date in processed_dates:
            continue

        processed_dates.add(forecast_date)

        day = forecast_date.strftime('%A')
        temperature = round(forecast_data.get('main', {}).get('temp', 0) - 273.15, 0)
        description = forecast_data.get('weather', [{}])[0].get('description', '')
        icon = forecast_data.get('weather', [{}])[0].get('icon', '')
        humidity = forecast_data.get('main', {}).get('humidity', 0)

        daily_forecast = {
            'day': day,
            'temperature': temperature,
            'humidity': humidity,
            'description': description,
            'icon': icon,
        }

        weekly_forecast.append(daily_forecast)
    #print("Weekly Forecast:", weekly_forecast)

    return weather_data, weekly_forecast
