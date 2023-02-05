from web.settings import DEBUG, MAX_TEMP, MAX_PRESSURE
import datetime
from .controller import SGController, t1, t2, curr_id
from .models import SteamGenerator

controller = SGController()

@t1.job(interval=datetime.timedelta(milliseconds=1000))
def watchdog():
    if(controller.temp_sensor_w1 >= MAX_TEMP or
        controller.temp_sensor_s1 >= MAX_TEMP or
        controller.temp_sensor_s2 >= MAX_TEMP or
        controller.pressure_sensor.read('pressure') >= MAX_PRESSURE):

        controller.soft_shutdown()

@t2.job(interval=datetime.timedelta(milliseconds=5000))
def savedata():
    if controller.data_save_started:
        data = controller.get_output()
        if(DEBUG):
            print("data to db save started\n")
            print(data)

        SteamGenerator.objects.create(
            water_temp = data['water_temp'],
            steam_temp_1 = data['steam_temp_1'],
            steam_temp_2 = data['steam_temp_2'],
            pressure = data['pressure'],
            heater_water1_power = data['heater_1'],
            heater_water2_power = data['heater_2'],
            heater_water3_power = data['heater_3'],
            heater_steam_power = data['heater_st'],
            valve = data['valve'],
            measurement_num = curr_id
            )

        SteamGenerator.save()
    else:
        pass