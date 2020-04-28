import requests
from django.shortcuts import render

import json
# Create your views here.

def index(request):
    
    # Haetaan ip-osoite
    urlip = 'https://api.ipgeolocation.io/getip'
    ip_reqest = requests.get(urlip).json()
    ip = ip_reqest['ip']

    # Haetaan ip-osoitteen avulla pituus- ja leveysaste, eli sijainti
    # HUOM! Laitoin harjoitustyöni versionhallintaan, joten poistin urlista avaimen, jonka sain rajapinnan palvelulta.
    #   Avain tulisi kirjoittaa kohtaan apiKey=, jossa tällä herkellä lukee API_KEY
    urlloc = 'https://api.ipgeolocation.io/ipgeo?apiKey=API_KEY&ip={}&fields=latitude,longitude&output=json'
    location_request = requests.get(urlloc.format(ip)).json()
    location = {
        'lat' : location_request['latitude'],
        'lon' : location_request['longitude'],
    }

    # Haetaan kaupungin 
    # HUOM! Laitoin harjoitustyöni versionhallintaan, joten poistin urlista avaimen, jonka sain rajapinnan palvelulta.
    #   Avain tulisi kirjoittaa kohtaan appid=, jossa tällä herkellä lukee APP_ID   
    urlc = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=APP_ID'
    weather_request = requests.get(urlc.format(location['lat'], location['lon'])).json()

    city_weather = {
        'city' : weather_request['name'],
        'temperature' : weather_request['main']['temp'],
        'description' : weather_request['weather'][0]['description'],
    }

    context = {'city_weather' : city_weather}

    return render(request, 'weather/weather.html', context)


def visual_data():

    # Haetaan ip-osoite
    urlip = 'https://api.ipgeolocation.io/getip'
    ip_reqest = requests.get(urlip).json()
    ip = ip_reqest['ip']

    # Haetaan ip-osoitteen avulla pituus- ja leveysaste, eli sijainti
 
    urlloc = 'https://api.ipgeolocation.io/ipgeo?apiKey=3285427421d342b6af73c2f44b6b961a&ip={}&fields=latitude,longitude&output=json'
    location_request = requests.get(urlloc.format(ip)).json()
    location = {
        'lat' : location_request['latitude'],
        'lon' : location_request['longitude'],
    }

    # Haetaan sijainnin perusteella cnt=jotain verran paikkoja säätietoineen
    urlw = 'http://api.openweathermap.org/data/2.5/find?lat={}&lon={}&cnt=50&units=metric&appid=b848a2310e96ed83ca6afd65da98fa0d'
    city_weather_request = requests.get(urlw.format(location['lat'], location['lon'])).json()
    weather_data = city_weather_request['list']

    # Luodaan tietorakenne, jota voidaan käyttää visualisoinneissa
    weather_info = []
    for data in weather_data:
        info = {
            'location' : data['name'],
            'temperature' : data['main']['temp'],
            'humidity' : data['main']['humidity'],
            'description' : data['weather'][0]['description']
        }
        weather_info.append(info)

    return weather_info


def charts(request):

    return render(request, 'weather/charts.html', {'weather_info' : visual_data()})


def descriptions(request):

    weather_info = {
        'chart' : {'type': 'column'},
        'title' : {'text' : 'Säätilat'},
        'series' : []
    }
    for data in visual_data():
        info = {
            'name' : data['description'],
            'data' : [0]
        }
        if len(weather_info['series']) == 0:
            info['data'][0] += 1
            weather_info['series'].append(info)
        else:
            t = 0
            for i in range(len(weather_info['series'])):
                if info['name'] == weather_info['series'][i]['name']:
                    weather_info['series'][i]['data'][0] += 1
                    t =+ 1
                    break
            if t == 0:
                weather_info['series'].append(info)
                info['data'][0] += 1
    
    return render(request, 'weather/descriptions.html', {'weather_info' : json.dumps(weather_info)})