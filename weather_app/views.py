from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=508d8d9f9ae3d082fa313bbc1fc3a6e5"
    err_msg = ""

    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=new_city).count()

            if existing_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Invalid City'
            else:
                err_msg = "You've already added this city"
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'
    form = CityForm()

    weather_data = []

    cities = City.objects.all()
    for city in cities:
        r = requests.get(url.format(city)).json()
        print(r)

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data': weather_data, 'form': form, 'message': message, 'message_class': message_class}

    return render(request, 'weather_app/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
