from datetime import time, datetime,timedelta

import pytz
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
    value = []
    main_data = []
    while a < 7:
        main_city = str(MainCities.objects.get(pk=a))
        m = requests.get(url_m.format(main_city)).json()

        main_cities = {
            'city': main_city,
            'icon': m['weather'][0]['icon'],
            'country': m['sys']['country'],
            'temp': round(m['main']['temp'], 1),
            'timezone': m['timezone'],
            'dt': m['dt'],
            'utc': m['timezone'] / 3600

        }

        a += 1
        main_data.append(main_cities)
        country_codes = main_data[a - 2]["country"]
        country_timezones = pytz.country_timezones[country_codes]
        country_timezone = country_timezones[0]
        current_time = datetime.now(pytz.timezone(country_timezone))
        asd = current_time.strftime('%H:%M')

        value.append(asd)

    return render(request, 'weather/main.html', {"form": form, "main_data": main_data, "value": value})


def forecast(request):
    form = CityForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('forecast')
    a = 1

    url_m = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90'
    value = []
    main_data = []
    while a < 7:
        main_city = str(MainCities.objects.get(pk=a))
        m = requests.get(url_m.format(main_city)).json()

        main_cities = {
            'city': main_city,
            'icon': m['weather'][0]['icon'],
            'country': m['sys']['country'],
            'temp': round(m['main']['temp'], 1),
            'timezone': m['timezone'],
            'dt': m['dt'],
            'utc': m['timezone'] / 3600

        }

        a += 1
        main_data.append(main_cities)
        country_codes = main_data[a - 2]["country"]
        country_timezones = pytz.country_timezones[country_codes]
        country_timezone = country_timezones[0]
        current_time = datetime.now(pytz.timezone(country_timezone))
        asd = current_time.strftime('%H:%M')

        value.append(asd)

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
            'temp': round(c['main']['temp'], 1),
            'feels_like': round(c['main']['feels_like'], 1),
            'temp_min': c['main']['temp_min'],
            'temp_max': c['main']['temp_max'],
            'pressure': c['main']['pressure'],
            'humidity': c['main']['humidity'],
            'wind': c['wind']['speed'],
            'deg': c['wind']['deg'],
            'name': c['name'],
            'timezone': c['timezone'],
            'utc': c['timezone'] / 3600,
            'dt': c['dt'],

        }

        gr = current['dt']
        readable = datetime.fromtimestamp(gr).isoformat()
        date = readable[0:10]
        dateb = {
            'date': date

        }
        current.update(dateb)

        wind_deg = current['deg']

        dirs = ['North', 'North-northeast', 'Northeast', 'East-northeast', 'East', 'East-southeast', 'Southeast',
                'South-southeast', 'South', 'South-southwest', 'Southwest', 'West-southwest', 'West', 'West-northwest',
                'Northwest', 'North-northwest']
        ix = round(wind_deg / (360. / len(dirs)))
        ixx = dirs[ix % len(dirs)]

        dir_dic = {
            'dir': ixx
        }
        current.update(dir_dic)








    except KeyError:
        return redirect('no_data')

    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=3e8c61a2a241410b6fa72b0186291c90'

    r = requests.get(url.format(city)).json()
    a = 0
    list = []
    weather_data = []
    first_day = []
    second_day = []
    third_day = []
    fourth_day = []
    fifth_day = []
    sixth_day = []
    while a < 40:
        weather_forecast = {
            'city': city,
            'data': r['list'][a]['dt_txt'][5:16],
            'day': r['list'][a]['dt_txt'][5:10],
            'description': r['list'][a]['weather'][0]['description'],
            'icon': r['list'][a]['weather'][0]['icon'],
            'wind': r['list'][a]['wind']['speed'],
            'temperature': round(r['list'][a]['main']['temp'], 1),
            'feels_like': r['list'][a]['main']['feels_like'],
            'temp_min': r['list'][a]['main']['temp_min'],
            'pressure': r['list'][a]['main']['pressure'],
            'humidity': r['list'][a]['main']['humidity'],

        }
        a += 1

        weather_data.append(weather_forecast)
        list.append(weather_forecast['day'])

    first = list.count(list[0])
    second = list.count(list[first])
    third = list.count(list[second + first])
    fourth = list.count(list[third + second + first])
    fifth = list.count(list[fourth + third + second + first])
    sixth = list.count(list[fifth + fourth + third + second + first])


    first_day.append(weather_data[0:first])
    second_day.append(weather_data[first:second+first])
    third_day.append(weather_data[second+first:third+second+first])
    fourth_day.append(weather_data[third+second+first:fourth+third+second+first])
    fifth_day.append(weather_data[fourth+third+second+first:fifth+fourth+third+second+first])
    sixth_day.append(weather_data[fifth+fourth+third+second+first:])

    first_day = first_day[0]
    second_day = second_day[0]
    third_day = third_day[0]
    fourth_day = fourth_day[0]
    fifth_day = fifth_day[0]
    sixth_day = sixth_day[0]

    from datetime import date, timedelta

    tomo = date.today() - timedelta(-2)
    to = tomo.strftime('%A')
    third_day[0].update({'day_name':to})

    t_days = date.today() - timedelta(-3)
    td = t_days.strftime('%A')
    fourth_day[0].update({'day_name':td})

    fr_days = date.today() - timedelta(-4)
    tfr = fr_days.strftime('%A')
    fifth_day[0].update({'day_name':tfr})

    s_days = date.today() - timedelta(-5)
    ts = s_days.strftime('%A')
    sixth_day[0].update({'day_name': ts})






    context = {'current': current, 'weather_data': weather_data, 'city': city, "form": form, "main_data": main_data,
            "value": value,'first_day' : first_day, 'second_day':second_day,'third_day':third_day,'fourth_day':fourth_day
              ,'fifth_day':fifth_day,'sixth_day':sixth_day }





    if city_count > 10:
        City.objects.filter().first().delete()
    else:
        pass
    return render(request, 'weather/forecast.html', context)


def no_data(request):
    return render(request, 'weather/no_data.html', )
