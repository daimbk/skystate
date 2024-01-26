import datetime
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    API_KEY = "3e0b73d2dc8224f74cc952419a96a60a"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1', None)

        if not city1:
            error_message = 'Please enter a city.'
            context = {'error_message': error_message}
            return JsonResponse(context)

        weather_data1, weekly_forecast1 = fetch_weather_and_forecast(
            city1, API_KEY, current_weather_url, forecast_url)

        context = {
            'weather_data1': weather_data1,
            'weekly_forecast1': weekly_forecast1,
        }

        return JsonResponse(context)
    else:
        return JsonResponse({})


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(
        forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    weekly_forecast = []

    # Start from the second day
    for idx, forecast_data in enumerate(forecast_response.get('daily', [])[1:6]):
        timestamp = forecast_data.get('dt', 0)
        day = datetime.datetime.utcfromtimestamp(timestamp).strftime('%A')
        min_temp = round(forecast_data.get(
            'temp', {}).get('min', 0) - 273.15, 2)
        max_temp = round(forecast_data.get(
            'temp', {}).get('max', 0) - 273.15, 2)
        description = forecast_data.get('weather', [{}])[
            0].get('description', '')
        icon = forecast_data.get('weather', [{}])[0].get('icon', '')

        weekly_forecast.append({
            'day': day,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon,
        })

    return weather_data, weekly_forecast
