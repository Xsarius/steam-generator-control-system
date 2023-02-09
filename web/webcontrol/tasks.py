from web.settings import MAX_TEMP, MAX_PRESSURE, BACKUP_FILE
import datetime, timeloop
from .controller import SGController
from .models import SteamGenerator
from pyXSteam.XSteam import XSteam

controller = SGController()
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

# Periodic task handlers
t1 = timeloop.Timeloop()
t2 = timeloop.Timeloop()

@t1.job(interval=datetime.timedelta(milliseconds=500))
def set_output():
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
        'pid_signal': 0,
    }

    try:
        controller.output += {
            'pressure': controller.pressure_sensor.read('pressure'),
            'voltage_ph1': controller.power_meter.read('voltage_ph1'),
            'current_ph1': controller.power_meter.read('current_ph1'),
            'active_power_ph1': controller.power_meter.read('active_power_ph1'),
            'voltage_ph2': controller.power_meter.read('voltage_ph2'),
            'current_ph2': controller.power_meter.read('current_ph2'),
            'active_power_ph2': controller.power_meter.read('active_power_ph2'),
            'voltage_ph3': controller.power_meter.read('voltage_ph3'),
            'current_ph3': controller.power_meter.read('current_ph3'),
            'active_power_ph3': controller.power_meter.read('active_power_ph3'),
        }
    except:
        print("2")

    with open(BACKUP_FILE, "a") as backup_file:
        for key, value in controller.output.items():
            backup_file.write('%s:%s' % (key, value))

        backup_file.write('\n')

@t1.job(interval=datetime.timedelta(seconds=1))
def watchdog():
    if(controller.output['water_temp'] >= MAX_TEMP or
        controller.output['steam_temp_1'] >= MAX_TEMP or
        controller.output['steam_temp_2'] >= MAX_TEMP or
        controller.output['pressure'] >= MAX_PRESSURE):

        controller.soft_shutdown()

# @t1.job(interval=datetime.timedelta(seconds=2))
# def pid_loop():
#     curr_temp = controller.output['steam_temp_1']
#     curr_press = controller.output['pressure']

#     sat_temp = steamTable.tsat_p(curr_press)
#     err = controller.pid(curr_temp)

#     if sat_temp <= curr_temp:
#         # Liquid to gas phase change
#         pass

#     else:
#         # Liquid heating
#         pass

#     print(sat_temp)
#     print(err)


@t2.job(interval=datetime.timedelta(milliseconds=500))
def savedata():
    if controller.data_save_started:
        print("Data save active.\n")

        SteamGenerator.objects.create(
            measurement_num = controller.curr_measurement_id,
            water_temp = controller.output['water_temp'],
            steam_temp_1 = controller.output['steam_temp_1'],
            steam_temp_2 = controller.output['steam_temp_2'],
            pressure = controller.output['pressure'],
            heater_water1_power = controller.output['heater_1'],
            heater_water2_power = controller.output['heater_2'],
            heater_water3_power = controller.output['heater_3'],
            heater_steam_power = controller.output['heater_st'],
            valve = controller.output['valve'],
            )

        SteamGenerator.save()

t1.start()
t2.start(block=True)