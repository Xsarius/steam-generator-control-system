from web.settings import DEBUG, MAX_TEMP, MAX_PRESSURE
import datetime, simple_pid, os
from .controller import SGController, t1, curr_id
from .models import SteamGenerator

controller = SGController()
pid = simple_pid.PID(Kp=os.environ.get("P_COEF"),Ki=os.environ.get("I_COEF"), Kd=os.environ.get("D_COEF"))

def save_data_to_db(data):
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


@t1.job(interval=datetime.timedelta(seconds=1))
def watchdog():
    if(controller.temp_sensor_w1 >= MAX_TEMP or
        controller.temp_sensor_s1 >= MAX_TEMP or
        controller.temp_sensor_s2 >= MAX_TEMP or
        controller.pressure_sensor.read('pressure') >= MAX_PRESSURE):

        controller.soft_shutdown()

@t1.job(interval=datetime.timedelta(seconds=1))
def savedata():
    if controller.data_save_started:
        data = controller.get_output()
        save_data_to_db(data)
    else:
        pass

# @t1.job(interval=datetime.timedelta(seconds=200))
