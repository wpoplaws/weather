from django.shortcuts import render
import requests

from weather.forms import CityForm


def forecast(request):



    url_c = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90&lang=pl'
    city_c = 'Stalowa Wola'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    c = requests.get(url_c.format(city_c)).json()

    current = {
        'city': city_c,
        'lon': c['coord']['lon'],
        'lat': c['coord']['lat'],
        'description': c['weather'][0]['description'],
        'icon': c['weather'][0]['icon'],
        'temp': c['main']['temp'],
        'feels_like': c['main']['feels_like'],
        'temp_min': c['main']['temp_min'],
        'temp_max': c['main']['temp_max'],
        'pressure': c['main']['pressure'],
        'humidity': c['main']['humidity'],
        'wind': c['wind']['speed'],
        'name': c['name'],

    }

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90&lang=pl'
    city = 'Stalowa Wola'

    r = requests.get(url.format(city)).json()
    a = 0
    weather_data = []
    while a < 40:
        weather_forecast = {
            'city': city,
            'data': r['list'][a]['dt_txt'],
            'description': r['list'][a]['weather'][0]['description'],
            'wind': r['list'][a]['wind']['speed'],
            'temperature': r['list'][a]['main']['temp'],
            'feels_like': r['list'][a]['main']['feels_like'],
            'temp_min': r['list'][a]['main']['temp_min'],
            'pressure': r['list'][a]['main']['pressure'],
            'humidity': r['list'][a]['main']['humidity'],

        }
        a += 1
        print(a)
        weather_data.append(weather_forecast)

    context = {'current': current, 'weather_data': weather_data, 'form' : form}

    return render(request, 'weather/main.html', context)



