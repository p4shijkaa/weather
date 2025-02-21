from django.test import TestCase
from django.urls import reverse
from .models import WeatherQuery
from .forms import CityForm

class WeatherViewsTest(TestCase):

    def setUp(self):
        # Создаем тестовые данные, если необходимо
        self.city_name = "Moscow"
        self.url_home = reverse('weather_home')
        self.url_history = reverse('history')

    def test_weather_home_get(self):
        # Проверяем, что GET-запрос к weather_home возвращает статус 200
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather_home.html')
        self.assertIsInstance(response.context['form'], CityForm)

    def test_weather_home_post_valid(self):
        # Проверяем, что POST-запрос с валидными данными создает запись в базе данных
        response = self.client.post(self.url_home, {'city': self.city_name})
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertTrue(WeatherQuery.objects.filter(city_name=self.city_name).exists())

    def test_weather_home_post_invalid(self):
        # Проверяем, что POST-запрос с невалидными данными не создает запись
        response = self.client.post(self.url_home, {'city': ''})  # Пустое имя города
        self.assertEqual(response.status_code, 200)  # Ожидаем, что форма будет повторно отображена
        self.assertFormError(response, 'form', 'city', 'Это поле обязательно.')

    def test_weather_history(self):
        # Проверяем, что GET-запрос к weather_history возвращает статус 200
        response = self.client.get(self.url_history)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/weather_history.html')
        self.assertQuerysetEqual(response.context['queries'], WeatherQuery.objects.all().order_by('-timestamp'))