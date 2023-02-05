from django.db import models

class SteamGenerator(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True) # Adds automaticaly timestamp to each measurement
    water_temp = models.FloatField()
    steam_temp_1 = models.FloatField()
    steam_temp_2 = models.FloatField()
    pressure = models.FloatField(null=True)
    heater_water1_power = models.FloatField()
    heater_water2_power = models.FloatField()
    heater_water3_power = models.FloatField()
    heater_steam_power = models.FloatField()
    valve = models.CharField(max_length=10)
    measurement_num = models.IntegerField()
