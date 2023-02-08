from web.settings import DEBUG, MAX_TEMP, MAX_PRESSURE
import datetime, timeloop
from .controller import SGController, curr_id
from .models import SteamGenerator
from pyXSteam.XSteam import XSteam

controller = SGController()
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

# Periodic task handlers
loops_started = False
t1 = timeloop.Timeloop()
t2 = timeloop.Timeloop()

@t1.job(interval=datetime.timedelta(seconds=1))
def set_output():
    try:
        controller.output = {
            'water_temp': controller.temp_sensor_w1.getTemp(),
            'steam_temp_1': controller.temp_sensor_s1.getTemp(),
            'steam_temp_2': controller.temp_sensor_s2.getTemp(),
            'heater_w1': controller.heater_w1.state(),
            'heater_w2': controller.heater_w2.state(),
            'heater_w3': controller.heater_w3.state(),
            'heater_st': controller.heater_s1.state(),
            'valve': controller.valve.state(),
            'save': int(controller.data_save_started),
            'pressure': controller.pressure_sensor.read('pressure'),
            'pid_signal': 0,
            'voltage_ph1': controller.power_meter_ph1.read('voltage'),
            'current_ph1': controller.power_meter_ph1.read('current'),
            'active_power_ph1': controller.power_meter_ph1.read('active_power'),
            'voltage_ph2': controller.power_meter_ph2.read('voltage'),
            'current_ph2': controller.power_meter_ph2.read('current'),
            'active_power_ph2': controller.power_meter_ph2.read('active_power'),
            'voltage_ph3': controller.power_meter_ph3.read('voltage'),
            'current_ph3': controller.power_meter_ph3.read('current'),
            'active_power_ph3': controller.power_meter_ph3.read('active_power'),
        }
    except:
        pass

@t1.job(interval=datetime.timedelta(seconds=1))
def watchdog():
    if(controller.output['water_temp'] >= MAX_TEMP or
        controller.output['steam_temp_1'] >= MAX_TEMP or
        controller.output['steam_temp_2'] >= MAX_TEMP or
        controller.output['pressure'] >= MAX_PRESSURE):

        controller.soft_shutdown()

@t1.job(interval=datetime.timedelta(seconds=2))
def pid_loop():
    curr_temp = controller.output['steam_temp_1']
    curr_press = controller.output['pressure']

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


@t2.job(interval=datetime.timedelta(milliseconds=500))
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

if not loops_started:
    t1.start()
    t2.start()
    loops_started = True