from django.db import models

# Create your models here.
class SteamGenerator(models.Model):
    water_temp = models.FloatField(default=0)
    steam_temp_1 = models.FloatField(default=0)
    steam_temp_2 = models.FloatField(default=0)
    pressure = models.FloatField(default=0, null=True)
    heater_water1_power = models.FloatField(default=0)
    heater_water2_power = models.FloatField(default=0)
    heater_water3_power = models.FloatField(default=0)
    heater_steam_power = models.FloatField(default=0)
    valve = models.CharField(max_length=10)
    measurement_num = models.IntegerField(default=0)
