from web.settings import DEBUG, MAX_TEMP, MAX_PRESSURE
import datetime, timeloop
from .controller import SGController, curr_id
from .models import SteamGenerator
from pyXSteam.XSteam import XSteam

controller = SGController()
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

# Periodic task handlers
t1 = timeloop.Timeloop()
t2 = timeloop.Timeloop()

@t1.job(interval=datetime.timedelta(milliseconds=500))
def savedata():
    if controller.data_save_started:
        if(DEBUG):
            print("Data save active.\n")

        data = controller.get_output()

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

@t2.job(interval=datetime.timedelta(milliseconds=200))
def watchdog():
    if(controller.temp_sensor_w1 >= MAX_TEMP or
        controller.temp_sensor_s1 >= MAX_TEMP or
        controller.temp_sensor_s2 >= MAX_TEMP or
        controller.pressure_sensor.read('pressure') >= MAX_PRESSURE):

        controller.soft_shutdown()

@t1.job(interval=datetime.timedelta(seconds=2))
def pid_loop():
    curr_temp = controller.temp_sensor_s2.getTemp()
    curr_press = controller.pressure_sensor.read('pressure')

    sat_temp = steamTable.tsat_p(curr_press)
    err = controller.pid(curr_temp)

    if sat_temp <= curr_temp:
        # Liquid to gas phase change
        pass

    else:
        # Liquid heating
        pass

    print(sat_temp)
    print(err)

t1.start()
t2.start()