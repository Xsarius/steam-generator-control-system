from django.db import models

class SteamGenerator(models.Model):
    water_temp = models.FloatField(default=0)
    steam_temp_1 = models.FloatField(default=0)
    steam_temp_2 = models.FloatField(default=0)
    pressure = models.FloatField(null=True)
    heater_water1_power = models.FloatField(default=0)
    heater_water2_power = models.FloatField(default=0)
    heater_water3_power = models.FloatField(default=0)
    heater_steam_power = models.FloatField(default=0)
    valve = models.CharField(max_length=10, default='closed')
    measurement_num = models.IntegerField(default=0)
