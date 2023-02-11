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

@t1.job(interval=datetime.timedelta(milliseconds=1000))
def set_output():
    controller.output['water_temp'] = controller.temp_sensor_w1.getTemp(),
    controller.output['steam_temp_1'] = controller.temp_sensor_s1.getTemp(),
    controller.output['steam_temp_2'] = controller.temp_sensor_s2.getTemp(),
    controller.output['heater_w1'] = controller.heater_w1.state(),
    controller.output['heater_w2'] = controller.heater_w2.state(),
    controller.output['heater_w3'] = controller.heater_w3.state(),
    controller.output['heater_st'] = controller.heater_s1.state(),
    controller.output['valve'] = controller.valve.state(),
    controller.output['save'] = controller.data_save_started,
    controller.output['curr_temp_set'] = controller.pid.setpoint,
    controller.output['pid_signal'] = 0,
    controller.output['pressure'] = controller.pressure_sensor.read('pressure'),



@t1.job(interval=datetime.timedelta(seconds=1))
def save_to_file():
    with open(BACKUP_FILE, "a") as backup_file:
        for key, value in controller.output.items():
            backup_file.write('%s:%s' % (key, value))

        backup_file.write('\n')
#         controller.output['voltage_ph1'] = controller.power_meter.read('voltage_ph1')),
#         controller.output['current_ph1'] = controller.power_meter.read('current_ph1')),
#         controller.output['active_power_ph1'] = controller.power_meter.read('active_power_ph1')),
#         controller.output['voltage_ph2'] = controller.power_meter.read('voltage_ph2')),
#         controller.output['current_ph2'] = controller.power_meter.read('current_ph2')),
#         controller.output['active_power_ph2'] = controller.power_meter.read('active_power_ph2')),
#         controller.output['voltage_ph3'] = controller.power_meter.read('voltage_ph3')),
#         controller.output['current_ph3'] = controller.power_meter.read('current_ph3')),
#         controller.output['active_power_ph3'] = controller.power_meter.read('active_power_ph3')),

@t1.job(interval=datetime.timedelta(seconds=1))
def watchdog():
    if(controller.output['water_temp'] >= MAX_TEMP or
        controller.output['steam_temp_1'] >= MAX_TEMP or
        controller.output['steam_temp_2'] >= MAX_TEMP or
        controller.output['pressure'] >= MAX_PRESSURE):

        controller.soft_shutdown()

# @t1.job(interval=datetime.timedelta(milliseconds=200))
# def pid_loop():
#     curr_temp = controller.output['steam_temp_1'])
#     curr_press = controller.output['pressure'])

#     sat_temp = steamTable.tsat_p(curr_press)
#     err = controller.pid(curr_temp)

#     if sat_temp <= curr_temp:
#         # Liquid to gas phase change
#         pass

#     else:
#         # Liquid heating
#         pass

#     prsat_temp)
#     prerr)


@t2.job(interval=datetime.timedelta(milliseconds=200))
def savedata():
    if controller.data_save_started:
        print("Data save active.\n")

        item1 = SteamGenerator.objects.create(
            measurement_num = controller.curr_measurement_id,
            water_temp = controller.output['water_temp'][0],
            steam_temp_1 = controller.output['steam_temp_1'][0],
            steam_temp_2 = controller.output['steam_temp_2'][0],
            pressure = controller.output['pressure'][0],
            heater_water1_power = controller.output['heater_w1'][0],
            heater_water2_power = controller.output['heater_w2'][0],
            heater_water3_power = controller.output['heater_w3'][0],
            heater_steam_power = controller.output['heater_st'][0],
            valve = controller.output['valve'][0]
            )

t1.start()
t2.start()