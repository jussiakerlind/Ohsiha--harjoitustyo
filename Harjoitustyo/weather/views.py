import requests
from django.shortcuts import render

# Create your views here.

def index(request):
    urlw = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b848a2310e96ed83ca6afd65da98fa0d'
    city = 'Tampere'
    weather_request = requests.get(urlw.format(city)).json()

    city_weather = {
        'city' : city,
        'temperature' : weather_request['main']['temp'],
        'description' : weather_request['weather'][0]['description'],
    }

    context = {'city_weather' : city_weather}

    return render(request, 'weather/weather.html', context)