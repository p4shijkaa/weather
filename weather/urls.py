from django.urls import path
from .views import weather_home, weather_history

urlpatterns = [
    path('', weather_home, name='home'),
    path('history/', weather_history, name='history'),
]