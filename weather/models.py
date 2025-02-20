from django.db import models


class WeatherQuery(models.Model):
    city_name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city_name}-{self.timestamp}"

