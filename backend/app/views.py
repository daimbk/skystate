# views.py

import datetime
import requests

from django.shortcuts import render

def index(request):
    API_KEY = "3e0b73d2dc8224f74cc952419a96a60a"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1', None)

        if not city1:
            error_message = 'Please enter a city.'
            context = {'error_message': error_message}
            return render(request, 'C:\\Users\\shahb\\Documents\\Course Work\\Undergraduate-Course-Work\\Web Development\\skystate\\backend\\templates\\index.html', context)

        weather_data1, weekly_forecast1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if not weather_data1:
            error_message = f'Error fetching weather data for {city1}. Please enter a valid city.'
            context = {'error_message': error_message}
            return render(request, 'C:\\Users\\shahb\\Documents\\Course Work\\Undergraduate-Course-Work\\Web Development\\skystate\\backend\\templates\\index.html', context)

        context = {
            'weather_data1': weather_data1,
            'weekly_forecast1': weekly_forecast1,
        }

        return render(request, 'C:\\Users\\shahb\\Documents\\Course Work\\Undergraduate-Course-Work\\Web Development\\skystate\\backend\\templates\\index.html', context)
    else:
        return render(request, 'C:\\Users\\shahb\\Documents\\Course Work\\Undergraduate-Course-Work\\Web Development\\skystate\\backend\\templates\\index.html')


# views.py

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    print("Current Weather Response:", response)  # Add this line for debugging
    print("Forecast Response:", forecast_response)  # Add this line for debugging

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    weekly_forecast = []

    for idx, forecast_data in enumerate(forecast_response.get('daily', [])[1:6]):  # Start from the second day
        timestamp = forecast_data.get('dt', 0)
        day = datetime.datetime.utcfromtimestamp(timestamp).strftime('%A')
        min_temp = round(forecast_data.get('temp', {}).get('min', 0) - 273.15, 2)
        max_temp = round(forecast_data.get('temp', {}).get('max', 0) - 273.15, 2)
        description = forecast_data.get('weather', [{}])[0].get('description', '')
        icon = forecast_data.get('weather', [{}])[0].get('icon', '')

        weekly_forecast.append({
            'day': day,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon,
        })

    return weather_data, weekly_forecast
