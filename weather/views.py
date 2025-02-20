from django.shortcuts import render, redirect
import requests
from .models import WeatherQuery
from .forms import CityForm
from django.conf import settings


def check_weathers_params(city_name):
    api_key = settings.API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url=url)
    return response.json()


def weather_home(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city']
            weather_data = check_weathers_params(city_name)

            if weather_data.get("main"):
                temperature = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"]
                WeatherQuery.objects.create(
                    city_name=city_name,
                    temperature=temperature,
                    description=description
                )
            return redirect('history')

    else:
        form = CityForm()
    return render(request, 'weather/weather_home.html', {'form': form})


def weather_history(request):
    queries = WeatherQuery.objects.all().order_by('-timestamp')
    return render(request, 'weather/weather_history.html', {'queries': queries})
