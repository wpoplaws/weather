from django.shortcuts import render, redirect
import requests

from weather.forms import CityForm
from weather.models import City, MainCities


def main(request):
    form = CityForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('forecast')
    a = 1

    url_m = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90'


    main_data = []
    while a < 7:
        main_city = str(MainCities.objects.get(pk=a))
        m = requests.get(url_m.format(main_city)).json()
        main_cities = {
            'city': main_city,
            'icon': m['weather'][0]['icon'],
            'temp': m['main']['temp'],

        }
        a += 1

        main_data.append(main_cities)
    print(main_data[0]['city'])

    return render(request, 'weather/main.html', {"form": form,"main_data": main_data,})


def forecast(request):
    city_count = City.objects.count()
    if city_count == 0:
        return redirect('main')

    else:
        cityy = City.objects.last()
        city = str(cityy).title()
        url_c = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90'

        c = requests.get(url_c.format(city)).json()
    try:
        current = {
            'city': city,
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
    except KeyError:
        return redirect('no_data')

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90'

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

        weather_data.append(weather_forecast)

    context = {'current': current, 'weather_data': weather_data, 'city': city}
    if city_count > 10:
        City.objects.filter().first().delete()
    else:
        pass
    return render(request, 'weather/forecast.html', context)


def no_data(request):
    return render(request, 'weather/no_data.html', )
